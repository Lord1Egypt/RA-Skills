#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B 类三项上移的**客户端编排层**：coze 优先 + 本地末位兜底。

2026-11-04 按 ct-base §20.19.7 红线 2 落地。对应 Coze 端 0.4.00 的三个新 source：

    lit_rrf      RRF 跨源排名融合（连 build_source_ranks 一起上移）
    lit_prisma   PRISMA-2020 机器初筛 + 四段流程计数
    prospero     PROSPERO 系统评价注册检索（纯执行器，只接 raw_query）

设计约束
--------
* **不取消本地引擎**：coze 不可用 / 返回错误信封 / 结构不符 / 编排层异常，
  一律静默降级到调用方注入的 ``local_fn()``，功能不丢失。这与 0.3.95
  ``_dispatch_merge`` 的「源码保护型纯薄客户端、无兜底」口径不同，别混淆。
* **不反向依赖 scripts/**：本模块在 ``adapters/`` 层，本地三份引擎
  （source_registry / screen_prisma / fetch_prospero）由调用方以无参回调
  ``local_fn`` 注入，避免 adapters → scripts 的循环 import。
* **返回形状与本地引擎逐字一致**，调用点只需把「本地调用」换成「本模块调用」，
  后续代码零改动：
      rrf_fuse       -> list[work]
      prisma_screen  -> {"works": [...], "prisma": {...}}
      prospero_fetch -> payload dict（键 works/query/hit_count/count/...）或 None
* **契约差异适配**：Coze 三节点统一返回 ``projects`` 键，本地 RRF/PRISMA
  消费 ``works``（列表）、PROSPERO 消费 payload 的 ``works`` 键并落盘
  ``prospero.json``；本层负责 projects -> works 映射与产物补写。
* **权重不制造第二份真源**：云端 lit_rrf 默认等权 1.0，本地 rrf_fuse 默认取
  ``SOURCE_REGISTRY.rrf_weight``。这里显式从同一张注册表取权重下发，
  保证 coze 与本地结果等价（canary 可比对）。
* **检索式构造留本地**：prospero 节点是纯执行器，raw_query 由客户端
  ``fetch_prospero._build_query()`` 构造后下发，云端不拼检索式。

线上当前仍是 0.3.99（白名单无这三个 source）：调用会 fail-closed 返回错误，
本层自动降级本地，生产行为不变；0.4.00 部署后才真正切到云端。
"""
import json

from adapters import fetch_prospero
from adapters import source_registry
from adapters._coze_strategy import call_coze_strategy

__all__ = ["rrf_fuse", "prisma_screen", "prospero_fetch"]

# RRF / PRISMA 是纯计算零外网；PROSPERO 云端要访问 www.crd.york.ac.uk，
# 节点内部 timeout=45 + 最多 3 次重试，薄客户端读超时给宽一点。
_TIMEOUT_PURE = 180
_TIMEOUT_NET = 240


def _weights():
    """与本地 source_registry.rrf_fuse(weights=None) 缺省完全一致的权重表。

    云端不持有 SOURCE_REGISTRY，必须由客户端显式下发，否则默认是等权 1.0，
    与本地加权结果漂移。
    """
    return {s["display"]: s["rrf_weight"]
            for s in source_registry.SOURCE_REGISTRY.values()}


def _try_coze(source, payload_obj, log_fn, timeout):
    """调薄客户端并做结构校验；任何不可用一律返回 None（交调用方降级本地）。

    call_coze_strategy 已把「节点 _error 信封里的 error」拦下返回 None，
    这里再校验一次 status / error 是双保险：SSE 解析把 project_list 合并进
    顶层 final 后，避免出现 status != ok 却缺 error 字段的半坏结果被采信。
    """
    try:
        final = call_coze_strategy(source, payload_obj,
                                   log_fn=log_fn, timeout=timeout)
    except Exception as e:  # noqa: BLE001 - 编排层异常不得抛断主管线
        log_fn("[coze:%s] 编排层异常，降级本地: %s: %s"
               % (source, type(e).__name__, e))
        return None
    if not isinstance(final, dict):
        return None
    if final.get("error") or final.get("status") not in (None, "ok"):
        return None
    return final


def rrf_fuse(works, payloads_snapshot, local_fn, log_fn=print, k=60,
             prefer_local=False):
    """RRF 融合：coze lit_rrf 优先（连 build_source_ranks 一起上移）。

    prefer_local（2026-11-14）：整次 run 全部命中本地搜索缓存时置 True。
    RRF 是「确定性规则、零 IO」的纯计算节点（coze_contract §4），本地
    source_registry.rrf_fuse 与云端逐字等价；此时走云端只是把整个 works
    数组序列化往返一次，白耗 1 次 Coze 请求与配额，却拿不到任何新信息。
    故缓存命中 run 直接走本地引擎。默认 False，非缓存命中路径行为不变。

    Args:
        works:             去重 / 打分后的统一 work 列表。
        payloads_snapshot: 与本地 ``build_source_ranks(payloads)`` **同一时刻、
                           同一输入**的 payloads 快照。云端据此重算 ranks，
                           保证与本地兜底等价（不能用后续被 append 扩充的
                           payloads，否则两端 ranks 不一致）。
        local_fn:          无参回调，返回 ``source_registry.rrf_fuse(works,
                           _source_ranks)`` 的结果。
    Returns:
        list[work]，按 rrf_score 降序；每条带 rrf_score / _source_ranks。
    """
    if prefer_local:
        log_fn("[coze:lit_rrf] 缓存命中 run：纯计算节点走本地，跳过 Coze 请求")
        return local_fn()
    final = _try_coze("lit_rrf", {
        "works": works,
        "payloads": payloads_snapshot,
        "k": k,
        "weights": _weights(),
    }, log_fn, _TIMEOUT_PURE)
    if final is not None and isinstance(final.get("projects"), list):
        log_fn("[coze:lit_rrf] 云端融合完成（%d works, %d ranks）"
               % (len(final["projects"]), final.get("source_ranks_count") or 0))
        return final["projects"]
    log_fn("[coze:lit_rrf] 不可用，降级本地 source_registry.rrf_fuse")
    return local_fn()


def prisma_screen(works, params, local_fn, log_fn=print, prefer_local=False):
    """PRISMA 机器初筛：coze lit_prisma 优先。

    prefer_local（2026-11-14）：整次 run 全部命中本地搜索缓存时置 True。
    lit_prisma 是「确定性规则、零 LLM、零 IO」的纯计算节点，本地
    screen_prisma.screen 与云端逐字等价（selfcheck_b_pipeline 断言）。
    缓存命中时仍发 Coze 请求是纯粹的请求放大，故直接走本地。

    Args:
        works:    统一 work 列表。
        params:   dict，键与 screen_prisma.screen() 一致 ——
                  topic / review_type / safety / duplicates_removed /
                  exclude_non_original / require_types。
        local_fn: 无参回调，返回 ``screen_prisma.screen(...)`` 的结果。
    Returns:
        {"works": [...], "prisma": {...}}，与本地逐字同形。
    """
    payload = {"works": works}
    payload.update(params)
    if prefer_local:
        log_fn("[coze:lit_prisma] 缓存命中 run：纯计算节点走本地，跳过 Coze 请求")
        return local_fn()
    final = _try_coze("lit_prisma", payload, log_fn, _TIMEOUT_PURE)
    if (final is not None and isinstance(final.get("projects"), list)
            and isinstance(final.get("prisma"), dict)):
        log_fn("[coze:lit_prisma] 云端初筛完成（%d works）" % len(final["projects"]))
        return {"works": final["projects"], "prisma": final["prisma"]}
    log_fn("[coze:lit_prisma] 不可用，降级本地 screen_prisma.screen")
    return local_fn()


def prospero_fetch(topic, review_type, year_from, year_to, safety,
                   max_results, out, token, local_fn, log_fn=print):
    """PROSPERO 注册检索：coze prospero（公开 POST 执行器）优先。

    硬边界：
      * raw_query 由客户端 ``fetch_prospero._build_query()`` 构造，云端只执行；
      * 传了正式 token 时直接走本地（云端节点只做公开 POST，不支持 token 头，
        劫持过去反而丢掉调用方已配置的 GET/token 路径）；
      * coze 成功时补写 ``out``（prospero.json），保持审计产物与本地路径一致。

    Args:
        local_fn: 无参回调，返回 ``fetch_prospero.fetch(...)`` 的 payload。
    Returns:
        payload dict（键与本地 fetch 一致）或 None。
    """
    if token:
        log_fn("[coze:prospero] 检测到正式 token，保持本地 fetch 路径")
        return local_fn()
    raw_query = fetch_prospero._build_query(
        topic, review_type, year_from, year_to, safety)
    final = _try_coze("prospero", {
        "raw_query": raw_query,
        "max_results": max_results,
    }, log_fn, _TIMEOUT_NET)
    if final is not None and isinstance(final.get("projects"), list):
        works = final["projects"]
        payload = {
            "source": "PROSPERO",
            "query": final.get("query") or raw_query,
            "review_type": review_type,
            "year_from": year_from,
            "year_to": year_to,
            "safety": safety,
            "hit_count": final.get("hit_count"),
            "count": final.get("count", len(works)),
            "works": works,
        }
        if out:
            try:
                with open(out, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=2)
            except Exception as e:  # noqa: BLE001 - 落盘失败不影响结果
                log_fn("[coze:prospero] 写 %s 失败（不影响结果）: %s" % (out, e))
        log_fn("[coze:prospero] 云端检索完成（%d works）" % len(works))
        return payload
    log_fn("[coze:prospero] 不可用，降级本地 fetch_prospero.fetch")
    return local_fn()
