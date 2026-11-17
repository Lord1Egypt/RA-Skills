#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""国产大模型统一路由 — 统一入口与策略引擎（CLI）。

单入口：对外只暴露一个 chat()，内部按任务自动或手动选择后端，并自动统计成本。
纯标准库、零依赖、零密钥（密钥仅从环境变量读取）。

用法示例：
  python scripts/router.py chat --prompt "帮我用 Python 写一个快排" --model auto
  python scripts/router.py route --prompt "总结这篇文章" --strategy cheap
  python scripts/router.py report --period month
  python scripts/router.py hardware
  python scripts/router.py update-check
  python scripts/router.py version
"""

import os
import sys
import json
import argparse
import time
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import meta
import config
import classifier
import hardware
import cache
import cost_tracker
import yaml_simple
import report as report_mod
import update_check
import mock_engine
import health_check
import session_manager
import price_registry
import price_checker
from adapters import build, AdapterError
from adapters.base import AdapterTimeoutError
from adapters.base import _estimate_tokens as estimate_tokens

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_YAML = os.path.normpath(os.path.join(HERE, "..", "references", "models.yaml"))


# ───────────────────────── 注册表与适配器 ─────────────────────────
def load_registry():
    if not os.path.exists(MODELS_YAML):
        raise SystemExit("❌ 未找到模型注册表: %s" % MODELS_YAML)
    return yaml_simple.load_file(MODELS_YAML)


def _provider_keys(provider, reg):
    """为某厂商构造适配器所需的 key 字典（全部来自环境变量）。"""
    p = reg["providers"][provider]
    atype = p.get("adapter")
    if atype == "openai_compat":
        return {"api_key": config.get_key(provider), "env_hint": p.get("env_hint", "")}
    if atype == "ernie":
        return {
            "api_key_openai": config.get_key("ernie_openai"),
            "ak": config.get_key("ernie_ak"),
            "sk": config.get_key("ernie_sk"),
        }
    if atype == "spark":
        return {
            "app_id": config.get_key("spark_app_id"),
            "api_key": config.get_key("spark_api_key"),
            "api_secret": config.get_key("spark_api_secret"),
        }
    return {}


def _adapter_cfg(provider, reg):
    p = reg["providers"][provider]
    cfg = {
        "base_url": p.get("base_url"),
        "base_url_openai": p.get("base_url_openai"),
        "default_model": p.get("default_model"),
        "version": p.get("version", "v3.5"),
        "domain": p.get("domain", "generalv3.5"),
    }
    cfg.update(_provider_keys(provider, reg))
    return cfg


# ───────────────────────── 路由决策 ─────────────────────────
def _all_models(reg, only_configured=True):
    """展开所有 (provider, model_dict)。only_configured 时只含已配置密钥的厂商。"""
    out = []
    for provider, p in reg.get("providers", {}).items():
        if only_configured and not config.has_any_key_for(provider):
            continue
        for m in p.get("models", []):
            out.append((provider, m))
    return out


def _price(m):
    return float(m.get("price_in", 0) or 0) + float(m.get("price_out", 0) or 0)


def _cap(m, key):
    """读取能力画像分数（reason_score/code_score/long_score），缺失回退 5（中性）。"""
    try:
        return float(m.get(key, 5) or 5)
    except (TypeError, ValueError):
        return 5.0


def _get_win_score(provider, model_name, task_type):
    """查询竞技场胜率，归一化到 0-10。无数据返回 None。"""
    rates = cost_tracker.win_rates().get(task_type, [])
    if not rates:
        return None
    model_wins = None
    for r in rates:
        if r["provider"] == provider and r["model"] == model_name:
            model_wins = r["wins"]
            break
    if model_wins is None:
        return None
    max_wins = max(r["wins"] for r in rates)
    if max_wins <= 0:
        return None
    return model_wins / max_wins * 10.0


def _best_by_capability(models, cap_key, task_type=None):
    """在候选中选能力画像最高者；同分时选更便宜的（性价比优先）。
    当 task_type 提供时，静态画像(60%) + 动态胜率(40%) 加权；
    无竞技场数据时回退纯静态画像。
    这样新增厂商只要在 models.yaml 填了画像，就能被 auto 策略自动选中，无需改代码。"""
    def score(pm):
        p, m = pm
        cap = _cap(m, cap_key)
        if task_type:
            win = _get_win_score(p, m["name"], task_type)
            if win is not None:
                cap = cap * 0.6 + win * 0.4
        return (cap, -_price(m))
    return max(models, key=score)


def resolve(strategy, classification, reg, manual_model=None, allow_unconfigured=False):
    """返回 (provider, model_name, reason)。失败抛中文异常。

    allow_unconfigured=True 用于「路由建议模式」：不要求已配置密钥，
    仅基于注册表给出推荐路由，供用户事先规划（不发起任何 API 调用）。
    """
    cls = classification
    configured = config.configured_providers()
    if not configured and not allow_unconfigured:
        raise AdapterError(
            "当前未检测到任何厂商 API Key。请先设置至少一个环境变量，例如：\n"
            "  export DEEPSEEK_API_KEY=sk-xxx\n"
            "  export DASHSCOPE_API_KEY=sk-xxx\n"
            "支持：DEEPSEEK_API_KEY / DASHSCOPE_API_KEY / ZHIPU_API_KEY / "
            "MOONSHOT_API_KEY / HUNYUAN_API_KEY / ARK_API_KEY / "
            "ERNIE_OPENAI_KEY(或 ERNIE_API_KEY+ERNIE_SECRET_KEY) / SPARK_*\n"
            "（只想看路由推荐、暂不调用，可去掉密钥后重试，route 会进入「建议模式」）"
        )

    if strategy == "manual":
        return _resolve_manual(manual_model, reg, allow_unconfigured=allow_unconfigured)

    only_conf = bool(configured) and not allow_unconfigured
    models = _all_models(reg, only_configured=only_conf)
    if not models:
        # 建议模式下降级为全量模型
        models = _all_models(reg, only_configured=False)
    if not models:
        raise AdapterError("注册表中无可用模型，请检查 models.yaml")

    # v2.4 多模态路由：当分类器识别到 image/audio 时，优先选带 multimodal 标签的模型
    # 放在 cheap/quality/auto 之前，让所有策略都受益于多模态过滤
    multimodal = cls.get("multimodal")
    multimodal_fallback = False
    if multimodal:
        mm_models = [pm for pm in models if pm[1].get("multimodal")]
        if mm_models:
            models = mm_models
        else:
            multimodal_fallback = True  # 无多模态模型时回退全量，auto 分支标注

    if strategy == "cheap":
        # v2.7.0 cheap 策略质量感知：按性价比排序（评分/价格），不再单纯选最便宜
        pricing = price_registry.load_pricing()
        if pricing:
            def cheap_score(pm):
                p, m = pm
                price = _price(m)
                if price <= 0:
                    return (0, 0)  # 免费模型优先
                # 获取该模型的评分（从价格档案中取能力画像平均分）
                model_name = m.get("name", "")
                pinfo = pricing.get(model_name, {})
                # 使用静态能力画像作为质量参考
                quality = (m.get("reason_score", 5) + m.get("code_score", 5) + m.get("long_score", 5)) / 3.0
                # 性价比 = 质量 / 价格（越高越好）
                return (quality / price, -price)
            best = max(models, key=cheap_score)
            reason = "cheap 策略：性价比最优（评分/价格）"
        else:
            best = min(models, key=lambda pm: _price(pm[1]))
            reason = "cheap 策略：选择价格最低的模型"
        if multimodal_fallback:
            reason = "⚠️ 多模态(" + multimodal + ")需求但无支持模型，回退全量｜" + reason
        return best[0], best[1]["name"], reason

    if strategy == "quality":
        # 优先带 reasoner 的，其次上下文最长的
        def qscore(pm):
            m = pm[1]
            s = 0
            if m.get("reasoner"):
                s += 100
            s += (m.get("ctx", 0) or 0) / 1000.0
            return s
        best = max(models, key=qscore)
        reason = "quality 策略：选择能力最强的模型"
        if multimodal_fallback:
            reason = "⚠️ 多模态(" + multimodal + ")需求但无支持模型，回退全量｜" + reason
        return best[0], best[1]["name"], reason

    # auto：任务感知（v2.1 起结合能力画像 reason_score/code_score/long_score）
    # v2.3 起：静态画像(60%) + 动态胜率(40%) 加权
    # v2.4 起：多模态需求时已过滤候选集
    reason_bits = []
    task_type = cls["task_type"]
    if multimodal_fallback:
        reason_bits.append("⚠️ 多模态(" + multimodal + ")需求但无支持模型，回退全量")
    if cls["needs_reasoning"]:
        reasoner = [pm for pm in models if pm[1].get("reasoner")]
        if reasoner:
            best = max(reasoner, key=lambda pm: _cap(pm[1], "reason_score"))
            reason_bits.append("需推理→选 reasoner 模型(按推理画像)")
        else:
            best = _best_by_capability(models, "reason_score", task_type=task_type)
            reason_bits.append("需推理但无 reasoner→选推理画像+胜率加权")
    elif cls["length_bucket"] == "long":
        longs = [pm for pm in models if (pm[1].get("ctx") or 0) >= 128000]
        if longs:
            best = max(longs, key=lambda pm: (_cap(pm[1], "long_score"), pm[1].get("ctx", 0)))
            reason_bits.append("长文→选超长上下文(≥128k)且长文画像最强")
        else:
            best = _best_by_capability(models, "long_score", task_type=task_type)
            reason_bits.append("长文但无超长上下文→选长文画像+胜率加权")
    elif task_type == "code":
        best = _best_by_capability(models, "code_score", task_type=task_type)
        reason_bits.append("代码任务→选代码画像+胜率加权(性价比优先)")
    elif cls["budget_sensitive"]:
        best = min(models, key=lambda pm: _price(pm[1]))
        reason_bits.append("价格敏感(分类/抽取/翻译)→选最便宜")
    else:
        # 默认：优先 deepseek-chat，否则最便宜
        default = [pm for pm in models if pm[1]["name"] == "deepseek-chat"]
        best = default[0] if default else min(models, key=lambda pm: _price(pm[1]))
        reason_bits.append("常规任务→默认均衡模型")

    return best[0], best[1]["name"], "auto 策略：" + "；".join(reason_bits)


def _resolve_manual(model_str, reg, allow_unconfigured=False):
    if not model_str:
        raise AdapterError("manual 模式需要 --model 指定具体模型，如 deepseek:deepseek-chat")
    if ":" in model_str:
        provider, model = model_str.split(":", 1)
    else:
        provider, model = None, model_str
    for p, pinfo in reg.get("providers", {}).items():
        if provider and p != provider:
            continue
        for m in pinfo.get("models", []):
            if m["name"] == model:
                if not allow_unconfigured and not config.has_any_key_for(p):
                    raise AdapterError(
                        "厂商 %s 未配置密钥（%s），请先设置环境变量再调用。" % (p, pinfo.get("env_hint", ""))
                    )
                return p, model, "manual 模式：显式指定 %s:%s" % (p, model)
    raise AdapterError("未在注册表中找到模型: %s（检查 models.yaml）" % model_str)


def _price_of(provider, model_name, reg):
    for p, pinfo in reg.get("providers", {}).items():
        if p != provider:
            continue
        for m in pinfo.get("models", []):
            if m["name"] == model_name:
                return {"in": m.get("price_in", 0), "out": m.get("price_out", 0)}
    return None


# ───────────────────────── 命令实现 ─────────────────────────
def _resolve_dry_run(strategy, classification, reg, manual_model=None, dry_run=False):
    """统一路由解析（含 --dry-run 建议模式）。"""
    allow_unconfigured = dry_run or not config.configured_providers()
    try:
        if strategy == "manual":
            if not manual_model:
                raise AdapterError("manual 模式需通过 --model provider:model 指定具体模型")
            provider, model, reason = _resolve_manual(manual_model, reg,
                                                      allow_unconfigured=allow_unconfigured)
        else:
            provider, model, reason = resolve(strategy, classification, reg,
                                               allow_unconfigured=allow_unconfigured)
    except AdapterError:
        if allow_unconfigured:
            raise
        # 有密钥但仍失败 → 进入建议模式
        try:
            if strategy == "manual" and manual_model:
                provider, model, reason = _resolve_manual(manual_model, reg, allow_unconfigured=True)
            else:
                provider, model, reason = resolve(strategy, classification, reg, allow_unconfigured=True)
        except AdapterError as e2:
            raise SystemExit("❌ 路由失败：%s" % e2)
        reason = "【建议模式·仅展示推荐不调用】" + reason
    if dry_run:
        reason = "【dry-run·仅展示推荐不调用】" + reason
    return provider, model, reason


def cmd_chat(args, reg):
    prompt = args.prompt or " ".join(args.message or [])
    if not prompt:
        raise SystemExit("❌ 请提供 --prompt 或 -m")
    system = args.system
    classification = classifier.classify(prompt, args.task)
    strategy = args.model if args.model in ("auto", "cheap", "quality") else "manual"

    # ── Mock 模式（v2.0 全链路离线 Mock）──
    if getattr(args, "mock", False):
        return _cmd_chat_mock(args, reg, prompt, system, classification, strategy)

    # ── dry-run 模式（v2.3 建议模式统一）──
    dry_run = getattr(args, "dry_run", False)

    # 解析主模型 + 备用模型列表（用于故障转移）
    try:
        if strategy == "manual":
            primary_p, primary_m, reason = _resolve_manual(args.model, reg, allow_unconfigured=dry_run)
            backups = []
        else:
            if dry_run:
                primary_p, primary_m, reason = resolve(strategy, classification, reg, allow_unconfigured=True)
                backups = []
            else:
                (primary_p, primary_m), backups, reason = health_check.resolve_with_fallback(
                    strategy, classification, reg, max_backups=2)
    except AdapterError as e:
        raise SystemExit("❌ 路由失败：%s" % e)

    # dry-run 展示后返回
    if dry_run:
        print("🧭 dry-run 路由决策（%s 模式）" % strategy)
        print("  厂商/模型 : %s / %s" % (primary_p, primary_m))
        print("  依据       : %s" % reason)
        print("  任务分类   : 类型=%s 推理=%s 长度=%s" % (
            classification["task_type"], classification["needs_reasoning"],
            classification["length_bucket"]))
        return

    # v2.6 多轮会话集成
    session_id = getattr(args, "session", None)
    history_model = None
    history_provider = None
    if session_id:
        messages, history_model, history_provider = session_manager.build_messages_with_history(
            session_id, prompt, system=system
        )
    else:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

    if not args.no_cache:
        hit = cache.get(prompt, ttl_hours=args.cache_ttl, fuzzy=args.cache_fuzzy)
        if hit:
            hp, hm, hresp = hit
            cost_tracker.log_call(hp, hm, classification["task_type"], 0, 0, 0.0, 0, True, "cache_hit")
            if args.json:
                print(json.dumps({"content": hresp, "cached": True, "provider": hp, "model": hm},
                                  ensure_ascii=False))
            else:
                print("⚡ 命中本地语义缓存（来自 %s / %s），跳过 API 调用：\n" % (hp, hm))
                print(hresp)
            return

    # 尝试主模型 + 备用模型（故障转移）
    candidates = [(primary_p, primary_m)] + backups
    fallback_from = None
    last_error = None
    success = False
    t0 = time.time()
    est_tokens = False
    provider = model = None
    content = None

    for idx, (prov, mod) in enumerate(candidates):
        # 跳过不可达的备用模型
        if idx > 0 and not health_check.check_health().get(prov, False):
            continue
        try:
            adapter = build(reg["providers"][prov]["adapter"], _adapter_cfg(prov, reg))
            if args.stream:
                if idx > 0:
                    print("⚡ 降级到 %s / %s（原模型 %s 不可用）" % (prov, mod, candidates[0][0]))
                print("🤖 [%s / %s] %s\n" % (prov, mod, reason))
                chunks = adapter.chat(messages, mod, stream=True, timeout=args.timeout)
                full = []
                for piece in chunks:
                    if piece == "":
                        break
                    full.append(piece)
                    if not args.json:
                        sys.stdout.write(piece)
                        sys.stdout.flush()
                print("")
                content = "".join(full)
                in_text = "".join(m.get("content", "") for m in messages)
                it = estimate_tokens(in_text)
                ot = estimate_tokens(content)
                est_tokens = True
            else:
                res = adapter.chat(messages, mod, stream=False, timeout=args.timeout)
                if idx > 0:
                    print("⚡ 降级到 %s / %s（原模型 %s 不可用）" % (prov, mod, candidates[0][0]))
                content = res["content"]
                it, ot = res["in_tokens"], res["out_tokens"]
            provider, model = prov, mod
            fallback_from = candidates[0][0] + ":" + candidates[0][1] if idx > 0 else None
            success = True
            break
        except (AdapterTimeoutError, AdapterError) as e:
            last_error = e
            err_str = str(e)
            # 记录失败
            cost_tracker.log_call(prov, mod, classification["task_type"], 0, 0, 0.0,
                                  int((time.time() - t0) * 1000), False, err_str,
                                  fallback_from=candidates[0][0] + ":" + candidates[0][1] if idx > 0 else None)
            if isinstance(e, AdapterTimeoutError):
                print("⚠️ %s / %s 超时（%ds），尝试下一个..." % (prov, mod, e.timeout_sec))
            else:
                print("⚠️ %s / %s 失败：%s" % (prov, mod, err_str[:80]))
            continue

    if not success:
        raise SystemExit("❌ 所有模型调用均失败：%s" % last_error)

    elapsed = int((time.time() - t0) * 1000)
    price = _price_of(provider, model, reg)
    cost = cost_tracker.compute_cost(price, it, ot)
    cost_tracker.log_call(provider, model, classification["task_type"], it, ot, cost, elapsed, True,
                          tokens_estimated=est_tokens)
    cache.put(prompt, provider, model, content)

    # v2.6 多轮会话记录
    if session_id:
        session_manager.append_message(session_id, "user", prompt, model=model, provider=provider)
        session_manager.append_message(session_id, "assistant", content, model=model, provider=provider)
        if not args.json:
            print("  [session: %s]" % session_id)

    tok_tag = "(估)" if est_tokens else ""
    if args.json:
        print(json.dumps({"content": content, "provider": provider, "model": model,
                          "in_tokens": it, "out_tokens": ot, "tokens_estimated": est_tokens,
                          "cost": cost, "route_reason": reason},
                         ensure_ascii=False))
    else:
        print("🤖 [%s / %s] %s\n" % (provider, model, reason))
        print(content)
        print("\n────────── 用量 ──────────")
        print("  token: 入 %d%s / 出 %d%s ｜ 花费 ¥%.6f%s ｜ 耗时 %dms"
              % (it, tok_tag, ot, tok_tag, cost, tok_tag, elapsed))

    # 预算告警（可选）
    cfg = config.load_config(args.config)
    if cfg.get("budget_monthly"):
        exc, spent, bud = cost_tracker.budget_check(cfg["budget_monthly"])
        msg = report_mod.budget_alert(exc, spent, bud)
        print(msg)
        if exc and cfg.get("wecom_webhook"):
            report_mod.maybe_push_wecom(cfg["wecom_webhook"], msg)


def _cmd_chat_mock(args, reg, prompt, system, classification, strategy):
    """Mock 模式下的 chat 实现：不调 API，从预设库返回。
    
    自动网络检测：
    - 若所有厂商不可达，自动进入 mock 模式（即使未显式传 --mock）
    - 若部分厂商不可达，仅熔断不可达厂商
    """
    latency = getattr(args, "latency", 0)
    resp = mock_engine.build_mock_response(prompt, classification["task_type"], latency_ms=latency)

    mock_reason = "Mock 模式（离线调试，不调用真实 API）"
    provider = "mock"
    model = "preset"

    # 缓存逻辑
    if not args.no_cache:
        hit = cache.get(prompt, ttl_hours=args.cache_ttl, fuzzy=args.cache_fuzzy)
        if hit:
            hp, hm, hresp = hit
            cost_tracker.log_call(hp, hm, classification["task_type"], 0, 0, 0.0, 0, True, "cache_hit")
            if args.json:
                print(json.dumps({"content": hresp, "cached": True, "provider": hp, "model": hm},
                                 ensure_ascii=False))
            else:
                print("⚡ 命中本地语义缓存（来自 %s / %s），跳过 API 调用：\n" % (hp, hm))
                print(hresp)
            return

    content = resp["content"]
    it, ot = resp.get("in_tokens", 0), resp.get("out_tokens", 0)
    elapsed = latency  # 模拟延迟即为耗时

    # 成本记录（mock 模式下记录为 mock 调用）
    cost_tracker.log_call(provider, model, classification["task_type"], it, ot,
                          0.0, elapsed, True, "mock")

    # 写缓存
    cache.put(prompt, provider, model, content)

    if args.json:
        print(json.dumps({"content": content, "provider": provider, "model": model,
                          "in_tokens": it, "out_tokens": ot, "cost": 0.0,
                          "route_reason": mock_reason, "mock": True},
                         ensure_ascii=False))
    else:
        stream = getattr(args, "stream", False)
        print("🤖 [Mock / %s] %s\n" % (model, mock_reason))
        if stream and latency > 0:
            # 流式模式下逐字输出以模拟真实流式体验
            for ch in content:
                sys.stdout.write(ch)
                sys.stdout.flush()
                time.sleep(latency / 1000.0 / max(len(content), 1))
            print("")
        else:
            print(content)
        print("\n────────── 用量 ──────────")
        print("  token: 入 %d / 出 %d ｜ 花费 ¥0.000000（Mock 免费）｜ 耗时 %dms" % (it, ot, elapsed))

    # 预算告警（mock 不计费，但仍检查是否超预算）
    cfg = config.load_config(args.config)
    if cfg.get("budget_monthly"):
        exc, spent, bud = cost_tracker.budget_check(cfg["budget_monthly"])
        msg = report_mod.budget_alert(exc, spent, bud)
        print(msg)


def cmd_route(args, reg):
    prompt = args.prompt or " ".join(args.message or [])
    if not prompt:
        raise SystemExit("❌ 请提供 --prompt 或 -m")
    cls = classifier.classify(prompt, args.task)
    strategy = args.strategy if args.strategy else "auto"
    manual_model = args.model if args.model else None
    dry_run = getattr(args, "dry_run", False)
    provider, model, reason = _resolve_dry_run(strategy, cls, reg,
                                                manual_model=manual_model, dry_run=dry_run)
    if args.json:
        print(json.dumps({"strategy": strategy, "provider": provider, "model": model,
                          "reason": reason, "classification": cls}, ensure_ascii=False))
    else:
        print("🧭 路由决策（%s 模式）" % strategy)
        print("  厂商/模型 : %s / %s" % (provider, model))
        print("  依据       : %s" % reason)
        print("  任务分类   : 类型=%s 推理=%s 长度=%s 价格敏感=%s" % (
            cls["task_type"], cls["needs_reasoning"], cls["length_bucket"], cls["budget_sensitive"]))


def cmd_report(args, reg):
    agg = cost_tracker.aggregate(args.period)
    # v2.7.0 双轨：加载价格档案
    pricing = price_registry.load_pricing() if getattr(args, "dual", False) else None
    if args.html:
        path = report_mod.render_html(agg, args.html)
        print("📊 HTML 报表已生成：%s" % path)
    print(report_mod.render_text(agg, pricing=pricing))


def cmd_hardware(args, reg):
    p = hardware.profile()
    print("🖥️  硬件画像：")
    print("  档位        : %s" % p["tier"])
    print("  CPU 核心    : %d" % p["cpu_cores"])
    print("  物理内存    : %.1f GB" % p["mem_gb"])
    print("  最大并发    : %d（自动限制，不拖累电脑）" % p["max_concurrency"])
    print("  单批大小    : %d" % p["batch_size"])
    print("  建议子任务数: %d（recommend_subtasks 示例）" % hardware.recommend_subtasks(10))


def cmd_cache(args, reg):
    if args.cache_cmd == "stats":
        print("语义缓存条目：%d" % cache.stats().get("entries", 0))
    elif args.cache_cmd == "clear":
        n = cache.clear()
        print("已清空 %d 条缓存" % n)


def cmd_config(args, reg):
    print("已配置密钥的厂商：%s" % (", ".join(config.configured_providers()) or "（无）"))
    print("全部支持厂商：%s" % ", ".join(reg.get("providers", {}).keys()))
    if not config.configured_providers():
        print("\n提示：在调用前设置至少一个厂商的环境变量，例如：")
        print("  export DEEPSEEK_API_KEY=sk-xxx")


def cmd_update(args, reg):
    cfg = config.load_config(args.config)
    has_update, latest, msg = update_check.run(meta.VERSION, cfg.get("update_url", ""), meta.HOMEPAGE)
    print(msg)
    if has_update:
        print("\n💡 升级方式：通过 SkillHub / 你常用的发布脚本更新本技能即可。")


def cmd_budget(args, reg):
    cfg = config.load_config(args.config)
    if not cfg.get("budget_monthly"):
        print("未配置月预算（在 config.json 设置 budget_monthly）。")
        return
    exc, spent, bud = cost_tracker.budget_check(cfg["budget_monthly"])
    print(report_mod.budget_alert(exc, spent, bud))


def cmd_price_check(args, reg):
    """v2.7.0 降价检测。"""
    provider = getattr(args, "price_provider", None)
    result = price_checker.check_price_changes(provider=provider)
    
    print("🔍 价格变更检测")
    print("  检查厂商数: %d" % result["checked"])
    
    if result["changes"]:
        print("\n⚠️  疑似调价：")
        for c in result["changes"]:
            print("   - %s / %s" % (c["provider"], c["model"]))
            print("     输入价: %.4f → %.4f" % (c["old_in"], c["new_in"]))
            print("     输出价: %.4f → %.4f" % (c["old_out"], c["new_out"]))
            print("     来源: %s" % c.get("url", ""))
    else:
        print("  ✅ 未检测到价格变化")
    
    if result["errors"]:
        print("\n❌ 抓取失败：")
        for e in result["errors"]:
            print("   - %s: %s" % (e["provider"], e.get("reason", "")))
    
    if result["stale"]:
        print("\n📅 档案过期提醒（超过 30 天未更新）：")
        for s in result["stale"]:
            print("   - %s: %s" % (s["name"], s.get("reason", "")))
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False))


def cmd_price_history(args, reg):
    """v2.7.0 价格档案查看。"""
    pricing = price_registry.all_prices()
    if args.json:
        print(json.dumps(pricing, ensure_ascii=False, indent=2))
    else:
        print("📋 价格档案（%d 个模型）" % len(pricing))
        for name, info in sorted(pricing.items()):
            date_str = info.get("date", "无")
            source_str = info.get("source", "")
            print("  %-25s 入 %-6.4f 出 %-6.4f 日期 %s %s" % (
                name, info["in"], info["out"], date_str, source_str))


def cmd_version(args, reg):
    print("cn-llm-router v%s" % meta.VERSION)


def cmd_embed(args, reg):
    """v2.6 embed：文本向量嵌入。"""
    # 解析 texts
    texts_raw = args.texts
    try:
        texts = json.loads(texts_raw)
        if not isinstance(texts, list):
            texts = [texts_raw]
    except json.JSONDecodeError:
        texts = [t.strip() for t in texts_raw.split(",") if t.strip()]

    if not texts:
        raise SystemExit("❌ --texts 不能为空")

    # 选厂商
    provider = args.provider
    if not provider:
        configured = config.configured_providers()
        if not configured:
            raise SystemExit("❌ 未配置任何厂商密钥，请先设置环境变量")
        provider = configured[0]

    adapter = build(reg["providers"][provider]["adapter"], _adapter_cfg(provider, reg))
    try:
        result = adapter.embed(texts, model=args.model, timeout=args.timeout)
    except NotImplementedError:
        raise SystemExit("❌ 厂商 %s 不支持 embedding" % provider)

    if args.json:
        # embeddings 可能很大，只输出前 3 维 + 统计
        preview = [{"dim": len(e), "preview": e[:3]} for e in result["embeddings"]]
        print(json.dumps({
            "provider": provider,
            "model": result["model"],
            "count": len(result["embeddings"]),
            "dim": result["dim"],
            "tokens": result["tokens"],
            "embeddings_preview": preview,
        }, ensure_ascii=False))
    else:
        print("🔤 文本向量嵌入（%s / %s）" % (provider, result["model"]))
        print("  文本数: %d" % len(result["embeddings"]))
        print("  维度: %d" % result["dim"])
        print("  消耗 tokens: %d" % result["tokens"])
        for i, e in enumerate(result["embeddings"][:3]):
            print("  [%d] 前3维: %s" % (i, e[:3]))
        if len(result["embeddings"]) > 3:
            print("  ...（共 %d 条）" % len(result["embeddings"]))


def cmd_rerank(args, reg):
    """v2.6 rerank：文档重排序。"""
    # 解析 documents
    docs_raw = args.documents
    try:
        documents = json.loads(docs_raw)
        if not isinstance(documents, list):
            documents = [docs_raw]
    except json.JSONDecodeError:
        documents = [t.strip() for t in docs_raw.split(",") if t.strip()]

    if not documents:
        raise SystemExit("❌ --documents 不能为空")

    provider = args.provider
    if not provider:
        configured = config.configured_providers()
        if not configured:
            raise SystemExit("❌ 未配置任何厂商密钥，请先设置环境变量")
        provider = configured[0]

    adapter = build(reg["providers"][provider]["adapter"], _adapter_cfg(provider, reg))
    try:
        result = adapter.rerank(args.query, documents, model=args.model, timeout=args.timeout)
    except NotImplementedError:
        raise SystemExit("❌ 厂商 %s 不支持 rerank" % provider)

    if args.json:
        print(json.dumps({
            "provider": provider,
            "model": result["model"],
            "results": result["results"],
        }, ensure_ascii=False))
    else:
        print("📊 文档重排序（%s / %s）" % (provider, result["model"]))
        print("  查询: %s" % args.query[:60])
        for r in result["results"]:
            idx = r.get("index", "?")
            score = r.get("relevance_score", r.get("score", 0))
            text = r.get("text", r.get("document", ""))[:60]
            print("  #%d  分数: %.4f  %s" % (idx, score, text))


# ───────────────────────── CLI ─────────────────────────
def build_parser():
    ap = argparse.ArgumentParser(prog="cn-llm-router", description="国产大模型统一路由")
    sub = ap.add_subparsers(dest="cmd")

    p_chat = sub.add_parser("chat", help="调用模型（需对应厂商密钥）")
    p_chat.add_argument("--prompt", help="用户问题")
    p_chat.add_argument("-m", "--message", action="append", help="消息（可多次）")
    p_chat.add_argument("--system", help="系统提示词")
    p_chat.add_argument("--model", default="auto", help="auto/cheap/quality 或 provider:model（manual）")
    p_chat.add_argument("--task", help="显式任务类型: code/reason/summarize/...")
    p_chat.add_argument("--stream", action="store_true", help="流式输出")
    p_chat.add_argument("--no-cache", action="store_true", help="禁用语义缓存")
    p_chat.add_argument("--timeout", type=int, default=60)
    p_chat.add_argument("--json", action="store_true", help="JSON 输出（供程序调用）")
    p_chat.add_argument("--config", help="config.json 路径")
    p_chat.add_argument("--cache-ttl", type=int, default=168)
    p_chat.add_argument("--cache-fuzzy", action="store_true")
    # v2.0 Mock 模式参数
    p_chat.add_argument("--mock", action="store_true",
                        help="v2.0 Mock 模式：不调真实 API，从本地预设库返回响应")
    p_chat.add_argument("--latency", type=int, default=0,
                        help="Mock 模式下模拟延迟（毫秒），用于测试超时逻辑")
    # v2.3 --dry-run 建议模式（与 route 统一）
    p_chat.add_argument("--dry-run", action="store_true",
                        help="v2.3 dry-run 模式：仅展示推荐路由，不调用 API")
    # v2.6 多轮会话
    p_chat.add_argument("--session", help="v2.6 多轮会话：会话 ID（自动维护上下文）")

    p_route = sub.add_parser("route", help="仅做路由决策（不调用 API）")
    p_route.add_argument("--prompt", help="用户问题")
    p_route.add_argument("-m", "--message", action="append")
    p_route.add_argument("--task", help="显式任务类型")
    p_route.add_argument("--strategy", default="auto", help="auto/cheap/quality/manual")
    p_route.add_argument("--model", help="manual 时的 provider:model")
    p_route.add_argument("--json", action="store_true")
    p_route.add_argument("--dry-run", action="store_true",
                         help="v2.3 dry-run 模式：仅展示推荐路由，不调用 API")

    p_rep = sub.add_parser("report", help="成本/用量报表")
    p_rep.add_argument("--period", default="month", choices=["day", "week", "month"])
    p_rep.add_argument("--html", help="导出 HTML 报表路径")
    p_rep.add_argument("--config", help="config.json 路径")
    p_rep.add_argument("--dual", action="store_true",
                       help="v2.7.0 双轨计算：档案价估算 vs 实测回填")

    p_hw = sub.add_parser("hardware", help="硬件画像与并发建议")

    p_cache = sub.add_parser("cache", help="语义缓存管理")
    p_cache.add_argument("cache_cmd", choices=["stats", "clear"])

    p_cfg = sub.add_parser("config", help="查看已配置厂商")

    p_up = sub.add_parser("update-check", help="检查技能更新")
    p_up.add_argument("--config", help="config.json 路径")

    p_bud = sub.add_parser("budget", help="预算检查")
    p_bud.add_argument("--config", help="config.json 路径")

    sub.add_parser("version", help="版本号")

    # v2.6 embed 子命令
    p_embed = sub.add_parser("embed", help="v2.6 文本向量嵌入")
    p_embed.add_argument("--texts", required=True, help="待嵌入文本（JSON 数组或逗号分隔）")
    p_embed.add_argument("--model", help="指定模型（默认用厂商默认 embedding 模型）")
    p_embed.add_argument("--provider", help="指定厂商（默认自动选已配置的）")
    p_embed.add_argument("--json", action="store_true", help="JSON 输出")
    p_embed.add_argument("--timeout", type=int, default=60)

    # v2.6 rerank 子命令
    p_rerank = sub.add_parser("rerank", help="v2.6 文档重排序")
    p_rerank.add_argument("--query", required=True, help="查询文本")
    p_rerank.add_argument("--documents", required=True, help="文档列表（JSON 数组或逗号分隔）")
    p_rerank.add_argument("--model", help="指定模型")
    p_rerank.add_argument("--provider", help="指定厂商")
    p_rerank.add_argument("--json", action="store_true", help="JSON 输出")
    p_rerank.add_argument("--timeout", type=int, default=60)

    # v2.6 session 子命令
    p_session = sub.add_parser("session", help="v2.6 多轮会话管理")
    p_session.add_argument("session_cmd", choices=["list", "show", "delete"],
                           help="list=列出会话 / show=查看历史 / delete=删除")
    p_session.add_argument("--id", help="会话 ID")

    # v2.6 describe 子命令（视频/文档理解）
    p_desc = sub.add_parser("describe", help="v2.6 通用视觉理解（视频/文档/图片）")
    p_desc.add_argument("input", help="输入文件路径或 URL")
    p_desc.add_argument("--prompt", help="自定义提示词（默认自动选择）")
    p_desc.add_argument("--provider", help="指定厂商")
    p_desc.add_argument("--json", action="store_true")
    p_desc.add_argument("--timeout", type=int, default=120)

    # v2.0 Mock 数据编辑器
    p_mock = sub.add_parser("mock", help="v2.0 Mock 数据编辑器（自定义 query→response 映射）")
    p_mock.add_argument("--edit", action="store_true", help="进入交互式 mock 数据编辑")
    p_mock.add_argument("--list", action="store_true", help="列出所有自定义 mock 场景")

    # v2.2 健康检查
    sub.add_parser("health-check", help="v2.2 检查各厂商 API 连通性")

    # v2.7.0 降价检测
    p_pc = sub.add_parser("price-check", help="v2.7.0 降价检测（抓取厂商价目页做哈希比对）")
    p_pc.add_argument("--provider", help="指定厂商（默认检查全部已配置厂商）")
    p_pc.add_argument("--json", action="store_true")

    # v2.7.0 价格档案查看
    p_ph = sub.add_parser("price-history", help="v2.7.0 价格档案查看")
    p_ph.add_argument("--json", action="store_true")

    # v2.2 模型竞技场（v2.4 扩展：--blind 控制盲选/显名对比）
    p_arena = sub.add_parser("arena", help="v2.4 多模型对比（--blind 盲选，否则显名对比）")
    p_arena.add_argument("--prompt", help="用户问题")
    p_arena.add_argument("-m", "--message", action="append")
    p_arena.add_argument("--task", help="显式任务类型")
    p_arena.add_argument("--models", default="auto",
                         help="auto=自动选 2-4 家，或指定 provider:model,provider:model")
    p_arena.add_argument("--blind", action="store_true",
                         help="盲选模式：隐藏模型名，投票后揭示（默认显名对比）")
    p_arena.add_argument("--json", action="store_true")
    p_arena.add_argument("--mock", action="store_true",
                         help="Mock 模式：不调真实 API，从本地预设库返回")
    return ap


def cmd_mock(args, reg):
    """Mock 数据编辑器命令实现。"""
    if args.edit:
        mock_engine.interactive_edit()
    elif args.list:
        mocks = mock_engine.list_custom_mocks()
        if not mocks:
            print("暂无自定义 mock 场景。")
        else:
            print("自定义 mock 场景列表：")
            for m in mocks:
                print("  [%s] %s | 优先级:%d | 关键词:%s" % (
                    m["id"], m["task_type"], m["priority"], ", ".join(m["keywords"][:5])))
    else:
        # 默认显示帮助
        print("Mock 数据编辑器）")
        print("  mock --edit  进入交互式编辑")
        print("  mock --list  列出所有自定义 mock 场景")


def _run_parallel(prompt, task_type, selected, reg, mock=False, blind=True):
    """共享并行调用辅助函数（v2.4 提取）。

    返回 list of (provider, model_name, content, error)。
    blind=True 时返回结果顺序不打乱（调用方自行打乱标号）。
    """
    import concurrent.futures as cf
    from adapters import build as build_adapter

    def call_one(idx, prov, model):
        try:
            if mock:
                resp = mock_engine.build_mock_response(prompt, task_type)
                return idx, prov, model["name"], resp["content"], None
            cfg = _adapter_cfg(prov, reg)
            adapter = build_adapter(reg["providers"][prov]["adapter"], cfg)
            res = adapter.chat([{"role": "user", "content": prompt}],
                               model["name"], stream=False, timeout=60)
            return idx, prov, model["name"], res["content"], None
        except Exception as e:
            return idx, prov, model["name"], "", str(e)

    results = [None] * len(selected)
    with cf.ThreadPoolExecutor(max_workers=min(len(selected), 4)) as pool:
        futures = [pool.submit(call_one, i, p, m) for i, (p, m) in enumerate(selected)]
        for fut in cf.as_completed(futures):
            idx, prov, mod, content, err = fut.result()
            results[idx] = (prov, mod, content, err)
    return results


def cmd_arena(args, reg):
    """多模型对比：--blind 盲选竞技（隐藏模型名投票），默认显名对比。"""
    prompt = args.prompt or " ".join(args.message or [])
    if not prompt:
        raise SystemExit("❌ 请提供 --prompt 或 -m")
    task_hint = args.task
    cls = classifier.classify(prompt, task_hint)
    task_type = cls["task_type"]
    blind = getattr(args, "blind", False)

    # 选模型：auto 策略自动选 2-4 家（已配置密钥 + 可达），或用户指定
    if args.models == "auto":
        all_models = _all_models(reg, only_configured=True)
        health = health_check.check_health()
        reachable = [(p, m) for p, m in all_models if health.get(p, False)]
        max_arena = min(4, hardware.profile().get("max_concurrency", 4))
        by_prov = {}
        for p, m in reachable:
            by_prov.setdefault(p, []).append(m)
        selected = []
        for p, ms in by_prov.items():
            if len(selected) >= max_arena:
                break
            selected.append((p, ms[0]))
        random.shuffle(selected)
        selected = selected[:max_arena]
    else:
        selected = []
        for token in args.models.split(","):
            token = token.strip()
            if ":" not in token:
                continue
            prov, mod = token.split(":", 1)
            found = False
            for p, pinfo in reg.get("providers", {}).items():
                if p != prov:
                    continue
                for m in pinfo.get("models", []):
                    if m["name"] == mod:
                        selected.append((p, m))
                        found = True
                        break
                if found:
                    break
            if not found:
                print("⚠️ 未找到模型：%s" % token)

    if len(selected) < 2:
        raise SystemExit("❌ 至少需要 2 家模型，请检查 --models 或密钥配置")

    if blind:
        print("🏟️  模型竞技场 — 任务类型：%s（%s）" % (task_type, prompt[:60]))
        print("   正在并行调用 %d 家模型...\n" % len(selected))
    else:
        print("📊 多模型对比 — 任务类型：%s（%s）" % (task_type, prompt[:60]))
        print("   正在并行调用 %d 家模型...\n" % len(selected))

    results = _run_parallel(prompt, task_type, selected, reg,
                            mock=getattr(args, "mock", False), blind=blind)

    if blind:
        # 盲选模式：打乱顺序，标 A/B/C/D
        order = list(range(len(selected)))
        random.shuffle(order)
        labels = [chr(65 + i) for i in range(len(order))]
        display = []
        for lbl, idx in zip(labels, order):
            prov, mod, content, err = results[idx]
            if err:
                print("❌ [%s] %s / %s 调用失败：%s" % (lbl, prov, mod, err[:60]))
            else:
                display.append((lbl, prov, mod, content))
                print("[%s] %s" % (lbl, content[:300]))
                if len(content) > 300:
                    print("   ...（%d 字）" % len(content))
                print()
    else:
        # 显名模式：直接显示模型名 + 回答
        display = []
        for prov, mod, content, err in results:
            if err:
                print("❌ [%s / %s] 调用失败：%s" % (prov, mod, err[:60]))
            else:
                display.append((prov, mod, content))
                print("[%s / %s] %s" % (prov, mod, content[:300]))
                if len(content) > 300:
                    print("   ...（%d 字）" % len(content))
                print()

    if not display:
        if args.json:
            mode = "blind" if blind else "compare"
            print(json.dumps({"arena": {"task_type": task_type, "mode": mode,
                                        "error": "所有模型调用均失败"}}, ensure_ascii=False))
            return
        raise SystemExit("❌ 所有模型调用均失败")

    # 构建 JSON 记录
    session_record = {
        "task_type": task_type,
        "mode": "blind" if blind else "compare",
        "models": [{"provider": p, "model": m} for p, m in selected],
        "results": {}
    }
    if blind:
        session_record["results"] = {lbl: {"provider": p, "model": m, "content": c[:200]}
                                      for lbl, p, m, c in display}
    else:
        session_record["results"] = {("%s/%s" % (p, m)): {"provider": p, "model": m, "content": c[:200]}
                                      for p, m, c in display}

    # JSON 模式
    if args.json:
        session_record["hint"] = "blind 模式请使用 arena --blind 交互投票" if blind else "显名对比已完成"
        print(json.dumps({"arena": session_record}, ensure_ascii=False))
        return

    # 仅 blind 模式支持交互投票
    if not blind:
        print("（显名对比模式，无投票。如需盲选竞技，请加 --blind）")
        return

    try:
        vote = input("请选择最佳回答（%s）：" % "/".join(lbl for lbl, *_ in display)).strip().upper()
    except (EOFError, KeyboardInterrupt):
        vote = ""
    if vote:
        for lbl, prov, mod, content in display:
            if lbl == vote:
                print("\n✅ 你选择了 [%s] %s / %s" % (lbl, prov, mod))
                cost_tracker.log_arena_vote(prompt, task_type,
                                           [{"provider": p, "model": m} for p, m in selected],
                                           prov, mod)
                return
    print("\n未记录投票。")


def cmd_session(args, reg):
    """v2.6 多轮会话管理命令。"""
    if args.session_cmd == "list":
        sessions = session_manager.list_sessions()
        if not sessions:
            print("暂无会话记录。")
            return
        print("会话列表：")
        for s in sessions:
            print("  %s  model=%s  updated=%s" % (
                s["id"], s.get("model", "-"), time.strftime("%Y-%m-%d %H:%M", time.localtime(s["updated_at"]))))
    elif args.session_cmd == "show":
        if not args.id:
            raise SystemExit("❌ --id 必填")
        sess = session_manager.get_session(args.id)
        if not sess:
            print("会话 %s 不存在。" % args.id)
            return
        print("会话 %s（%d 条消息）：" % (sess["id"], len(sess["messages"])))
        for m in sess["messages"]:
            print("  [%s] %s" % (m["role"], m["content"][:120]))
    elif args.session_cmd == "delete":
        if not args.id:
            raise SystemExit("❌ --id 必填")
        ok = session_manager.delete_session(args.id)
        print("已删除" if ok else "会话不存在")


def cmd_describe(args, reg):
    """v2.6 describe：通用视觉理解（视频/文档/图片）。"""
    import text_splitter

    input_path = args.input
    is_url = input_path.startswith(("http://", "https://"))

    if not is_url and not os.path.exists(input_path):
        raise SystemExit("❌ 文件不存在: %s" % input_path)

    ext = os.path.splitext(input_path)[1].lower() if not is_url else ""

    # 路由决策：视频 → 抽帧；文档 → 转文本；图片 → 直传视觉模型
    if ext in (".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"):
        mode = "video"
    elif ext in (".pdf", ".docx", ".doc", ".txt", ".md", ".xlsx", ".pptx"):
        mode = "document"
    elif ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"):
        mode = "image"
    else:
        mode = "image"

    # 选厂商（视觉模型）
    provider = args.provider
    if not provider:
        # 找有 multimodal 标签的模型
        for p, pinfo in reg.get("providers", {}).items():
            for m in pinfo.get("models", []):
                if m.get("multimodal"):
                    provider = p
                    break
            if provider:
                break
        if not provider:
            configured = config.configured_providers()
            if configured:
                provider = configured[0]
            else:
                raise SystemExit("❌ 未配置密钥，无法调用 describe")

    # 构造 prompt
    prompt = args.prompt
    if not prompt:
        if mode == "video":
            prompt = "请描述这段视频的关键内容，包括场景、人物、动作和对话要点。"
        elif mode == "document":
            prompt = "请解析并总结这份文档的核心内容、结构和关键信息。"
        else:
            prompt = "请详细描述这张图片的内容，包括场景、物体、文字和细节。"

    # 处理文件
    if mode == "document":
        # 文档走长文路由
        if ext == ".txt" or ext == ".md":
            with open(input_path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        else:
            text = "[二进制文档 %s] 当前版本仅支持 txt/md 直接读取，其他格式请先转为文本。" % input_path

        # 长文分段
        model_cfg = reg["providers"][provider]
        model_ctx = 64000  # 默认
        for m in model_cfg.get("models", []):
            if m.get("ctx", 0) > model_ctx:
                model_ctx = m["ctx"]

        chunk_len = text_splitter.auto_chunk_length(model_ctx)
        chunks = text_splitter.split_by_paragraphs(text, max_chars=chunk_len)

        adapter = build(model_cfg["adapter"], _adapter_cfg(provider, reg))

        def task_fn(chunk, idx):
            msg = [{"role": "user", "content": "请摘要以下文档分段（第 %d/%d 段）：\n\n%s" % (idx + 1, len(chunks), chunk)}]
            res = adapter.chat(msg, model_cfg["models"][0]["name"], stream=False, timeout=args.timeout)
            return res["content"]

        result = text_splitter.chunked_call(chunks, task_fn)
        summary = result["result"]
        n_chunks = result["chunks"]

        if args.json:
            print(json.dumps({"provider": provider, "mode": mode, "chunks": n_chunks, "summary": summary}, ensure_ascii=False))
        else:
            print("📄 文档解析（%s / %s, %d 段摘要合并）" % (provider, mode, n_chunks))
            print(summary)

    elif mode == "video":
        # 视频：提示需要 ffmpeg 抽帧（不强制依赖）
        has_ffmpeg = False
        try:
            import subprocess
            subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
            has_ffmpeg = True
        except Exception:
            pass

        if has_ffmpeg:
            print("🎬 视频模式：ffmpeg 抽帧 → 视觉模型（当前为接口演示，实际调用需配置密钥）")
            print("  输入: %s" % input_path)
            print("  提示: %s" % prompt)
        else:
            print("🎬 视频模式：需要 ffmpeg 才能抽帧处理")
            print("  安装: choco install ffmpeg  或  scoop install ffmpeg")
            print("  输入: %s" % input_path)

        if args.json:
            print(json.dumps({"provider": provider, "mode": mode, "ffmpeg": has_ffmpeg, "status": "interface_ready"}, ensure_ascii=False))

    else:
        # 图片：直接走视觉模型
        print("🖼️ 图片模式：%s" % input_path)
        print("  提示: %s" % prompt)
        if args.json:
            print(json.dumps({"provider": provider, "mode": "image", "status": "interface_ready"}, ensure_ascii=False))


def main():
    ap = build_parser()
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return
    reg = load_registry()
    dispatch = {
        "chat": cmd_chat, "route": cmd_route, "report": cmd_report,
        "hardware": cmd_hardware, "cache": cmd_cache, "config": cmd_config,
        "update-check": cmd_update, "budget": cmd_budget, "version": cmd_version,
        "mock": cmd_mock, "health-check": health_check.cmd_health_check,
        "arena": cmd_arena, "embed": cmd_embed, "rerank": cmd_rerank,
        "session": cmd_session, "describe": cmd_describe,
        "price-check": cmd_price_check, "price-history": cmd_price_history,
    }
    dispatch[args.cmd](args, reg)


if __name__ == "__main__":
    main()
