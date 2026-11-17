# -*- coding: utf-8 -*-
# ca_core.py — 采集器核心：常量 / 定价加载 / 日期 / 纯函数
# （从 collect_usage_data.py 拆分，2026-09-02）
#
# 模型单价（元 / 1M tokens）来源：联网查证 2026-07-29；限时免费截止日随官方活动更新。
# 本模块不含任何 IO；路由类别名（auto / 三档）单价由「所有计费模型均价」估算。

import argparse
import calendar
import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


__all__ = ['ALL_CUSTOM_MODELS', 'ALL_LOCAL_MODELS', 'ALL_ROUTER_MODELS', 'CACHE_DISCOUNT', 'CUSTOM_LOCAL_PRICING', 'DB_PATH', 'DEFAULT_BLENDED_PER_MILLION', 'DEFAULT_MODEL', 'DELISTED_MODELS', 'DISCOVERED_EXTERNAL', 'DISCOVERED_LOCAL', 'DISCOVERED_ROUTER', 'DISPLAY_MERGE', 'GLM52_FAMILY', 'GLM52_RATE', 'HOME', 'LOW_CONFIDENCE', 'LOW_CONFIDENCE_BIAS', 'MEDIA_EXTS', 'MODEL_PRICING', 'MODE_RATES_META', 'ORPHAN_KEY', 'ORPHAN_LABEL', 'PERIOD_DAYS', 'PERIOD_LABELS', 'PERIOD_NEXT', 'PERIOD_SHORT', 'PER_MILLION', 'PROJECTS_DIR', 'ROUTER_ALIASES', 'ROUTER_HOSTS', 'ROUTER_VENDORS', 'SCHEDULED_PRICING', 'SESSIONS_DIR', 'SILICONFLOW_VENDOR_PREFIXES', 'SYSTEM_REMINDER_RE', 'TASK_RULES_PATH', 'TASK_TYPE_RULES', 'TIER_ALIASES', 'TIER_CANON', 'TIER_LABELS', 'TIMED_FREE', 'TRACES_DIR', 'TZ', 'UNNAMED_LABEL', 'USAGE_LOG_PATH', 'USER_CUSTOM_MODELS', 'WB_DIR', 'WORKBUDDY_SESSIONS', '_CHEAPER_ALT', '_PRICING', '_PRICING_LOCAL_LOADED', '_build_sid_to_title', '_load_acc_product_config', '_load_pricing_config', '_to_num', 'call_time_of', 'canonical_tier', 'compute_cost', 'discover_custom_models', 'effective_tokens_of', 'glm52_discount_multiplier', 'is_router_like', 'is_scheduled_free', 'is_timed_free', 'iso_to_date', 'iso_to_dt', 'load_task_rules', 'low_confidence_reason', 'low_confidence_bias', 'merge_display_key', 'normalize_model', 'parse_channel', 'parse_date_range', 'price_of', 'resolve_date_range', 'resolve_model', 'score_task_types', 'trace_cost', 'ts_to_date', 'ts_to_dt', '_router_avg_unit_price']
TIMED_FREE = {
    # 兜底种子值；运行时 _load_pricing_config() 会从 pricing.json 合并覆盖，
    # 以 pricing.json 的 timed_free 段为准（权威源）。
    "hy3": "2026-10-31",
}

LOW_CONFIDENCE = {
    # 兜底种子值（通常为空）；运行时由 pricing.json 的 low_confidence 段覆盖（权威源）。
    # 语义：该模型的「静态单价 × token」估算与实际计费存在**已知系统性偏差**
    # （服务端时段减免 / 用户配额，静态价表无法表达），报告应标为低置信度、不参与成本结论。
    # 键为模型名，值为给用户看的原因说明。
}

LOW_CONFIDENCE_BIAS = {
    # 兜底种子值（通常为空）；运行时由 pricing.json 的 low_confidence_bias 段覆盖（权威源）。
    # 语义：与 low_confidence 同键，值为偏差方向 —— over=估算高于实际 / under=估算低于实际 /
    # mixed=方向不明。渲染层据此画 ⚠↑ / ⚠↓。
    # ⚠️ 必须先在此处定义：_load_pricing_config() 在模块加载早期（下方）就会读取它来
    # 初始化 cfg，若只在 _PRICING 生成后再赋值会触发 NameError。
}

SCHEDULED_PRICING = {
    # 兜底种子值（通常为空）；运行时由 pricing.json 的 scheduled_pricing 段覆盖（权威源）。
    # 语义：模型名 -> 规则列表；按调用的【时刻】（日期 + 小时 + 星期）改写静态单价。
    # 每条规则字段：
    #   from/until : 'YYYY-MM-DD'，生效日期区间（含端点）；缺省表示不限
    #   dow        : 星期列表，1=周一 … 7=周日（也接受 mon/tue/.../sun）；缺省表示不限
    #   hours      : 'HH:MM-HH:MM' 列表（北京时间，左闭右开）；支持跨午夜 23:00-08:00
    #   effect     : free=免费 / peak=高峰价 / discount=打折
    #   factor     : peak / discount 的倍率（缺省 peak=2.0、discount=1.0）
    #   note       : 给用户看的说明（报告可渲染）
    # 解决的根本问题：静态价表只能表达「模型 -> 单价」，无法表达「夜间免费 / 峰谷双档 /
    # 限期促销」这类**按时刻变化**的服务端规则 —— 这正是低置信度偏差的主要来源。
    # ⚠️ 与 LOW_CONFIDENCE_BIAS 同理：必须先在此处定义，否则 _load_pricing_config() 冷启动
    # 读它会触发 NameError（曾踩过一次，整个技能 import 即崩）。
}

MODEL_PRICING = {
    # —— WorkBuddy 官方内置模型（与 scripts/pricing.json 保持一致；仅作兜底，运行时以 pricing.json 为准）——
    # 路由别名：无单一单价，由代码估算（见 ROUTER_ALIASES）
    "auto": None,            # WorkBuddy 智能路由：执行时自动调配最适合模型
    # —— 腾讯混元（官方 RMB）——
    "hy3": {"input": 1.0, "output": 4.0},           # 腾讯混元官方：输入1 / 输出4（限时免费至 2026-10-31）
    "hy4-preview": {"input": 6.0, "output": 18.0},  # 腾讯混元 Hy4 preview（2026-08-28 发布开源，WorkBuddy 首发）：输入6 / 输出18（缓存命中0.3）；WorkBuddy 2 周限免
    # —— 智谱 GLM 系列（bigmodel.cn 国内官方 RMB，非 Z.ai 美元折算）——
    "glm-5.2": {"input": 8.0, "output": 28.0},      # 智谱官方 1M 上下文：输入8 / 输出28
    "glm-5.1": {"input": 8.0, "output": 28.0},      # 智谱官方：输入8 / 输出28
    "glm-5.3-flash": {"input": 0.8, "output": 2.8}, # 智谱 GLM-5.3-Flash（320B-A18B 开源，2026-08-26 发布）：输入0.8 / 输出2.8（缓存命中0.23），约为 GLM-5.3 的 1/10
    "glm-5v-turbo": {"input": 5.0, "output": 22.0}, # 智谱官方多模态：输入5 / 输出22
    # —— MiniMax（官方 RMB）——
    "minimax-m3": {"input": 2.1, "output": 8.4},    # MiniMax 官方分档价：≤512K 输入2.1/输出8.4/缓存命中0.42（=$0.30/$1.20×7），>512K 4.2/16.8（2026-10-20 修正，原 ¥1/¥4 误记）
    "minimax-m3.1-flash": {"input": 1.0, "output": 4.0, "cache_hit_input": 0.1},  # MiniMax M3.1 Flash（2026-10-19 正式发布，Space Bunny 正式版）：官方 ¥1/¥4/缓存0.1
    "minimax-m2.7": {"input": 2.1, "output": 8.4},  # MiniMax 官方：输入2.1 / 输出8.4
    # —— Kimi（官方 RMB）——
    "kimi-k3": {"input": 20.0, "output": 100.0},    # Kimi K3 官方：输入20 / 输出100
    "kimi-k2.7-code": {"input": 6.5, "output": 27.0}, # Kimi 官方：输入6.5 / 输出27
    "kimi-k2.8-preview": {"input": 6.5, "output": 27.0, "cache_hit_input": 1.7},  # Kimi K2.8 Preview（2026-09-11 上线，kimi-for-coding 升级）：¥6.5/¥27/缓存1.7
    "kimi-k2.6": {"input": 6.5, "output": 27.0},    # Kimi 官方：输入6.5 / 输出27
    # —— DeepSeek（官方 RMB 永久价）——
    "deepseek-v4-flash": {"input": 1.0, "output": 2.0}, # 官方：输入1 / 输出2
    "deepseek-v4-pro": {"input": 3.0, "output": 6.0},  # 官方永久价：输入3 / 输出6
    # —— Anthropic Claude（Claude Code 数据源；美元刊例价按 ~7.2 折算 CNY 的估算值，详见 pricing.json 注释）——
    "claude-opus-4": {"input": 108.0, "output": 540.0},   # Opus 4/4.5：$15/$75 per MTok 折算
    "claude-opus-4-5-20251101": {"input": 108.0, "output": 540.0},
    "claude-sonnet-4": {"input": 21.6, "output": 108.0},  # Sonnet 4/4.5：$3/$15 per MTok 折算
    "claude-sonnet-4-20250514": {"input": 21.6, "output": 108.0},
    "claude-haiku-4": {"input": 5.76, "output": 28.8},    # Haiku 4/4.5：$0.8/$4 per MTok 折算
    "claude-haiku-4-20250514": {"input": 5.76, "output": 28.8},
    "mimo-v2.6-pro": {"input": 3.0, "output": 6.0, "cache_hit_input": 0.025},  # 小米 MiMo-V2.6-Pro（2026-09-22 发布）：官方 ¥3/¥6/缓存0.025
    "step-5-preview": {"input": 7.2, "output": 19.44},  # 阶跃 Step 5 Preview（StepFun 旗舰）：官方直连 API ¥7.2/¥19.44（美元×7.2 估算），WorkBuddy 限免至 2026-10-25
}

DEFAULT_MODEL = "glm-5.2"

def resolve_model(name):
    """把 trace 兜底字面量 'default' 映射到用户默认付费模型；其余名原样返回。

    仅 'default' 被替换——'auto'(router)、真实模型名、'custom-local:*' 均不动。
    """
    if normalize_model(name) == "default":
        return DEFAULT_MODEL
    return name

ROUTER_ALIASES = {"auto", "default"}

TIER_ALIASES = {"fast-model", "balanced-model", "extreme-model", "deep-model"}

TIER_CANON = {"extreme-model": "deep-model"}

TIER_LABELS = {"fast-model": "快速", "balanced-model": "均衡", "deep-model": "极致",
               "extreme-model": "极致"}

UNNAMED_LABEL = "未命名会话"

ORPHAN_LABEL = "未关联会话"

ORPHAN_KEY = "__orphan__"

def _build_sid_to_title(sessions):
    """构建 session_id → 显示标题 映射；本地库无标题的会话归为 UNNAMED_LABEL。"""
    return {s["id"]: (s.get("custom_title") or s.get("title") or UNNAMED_LABEL) for s in sessions}

def is_router_like(model):
    """判断模型名是否为「路由类别名」（auto / default / 三档），均无单一真实底层模型。"""
    return model in ROUTER_ALIASES or model in TIER_ALIASES

def _router_avg_unit_price(pairs):
    """等权平均一组 (input_unit_price, output_unit_price) 对。

    用于路由别名（auto / 三档）自身无单一单价时，取「所有计费模型」均价作代表性估值。
    返回 (avg_ip, avg_op)；空输入返回 (None, None)。
    调用方负责先排除路由类别名与单价=0 的项（见 ca_sources / ca_aggregate 的两处调用）。
    """
    pairs = list(pairs)
    if not pairs:
        return None, None
    avg_ip = sum(ip for ip, op in pairs) / len(pairs)
    avg_op = sum(op for ip, op in pairs) / len(pairs)
    return avg_ip, avg_op

def canonical_tier(model):
    """把档位模型名归一为配置缓存规范 id（extreme-model → deep-model）；非档位原样返回。"""
    return TIER_CANON.get(model, model)

SILICONFLOW_VENDOR_PREFIXES = (
    "zai-org/",
    "z.ai/",
    "moonshotai/",
    "meituan-longcat/",
    "qwen/",
    "thudm/",
    "deepseek-ai/",
)

ROUTER_VENDORS = {
    "openrouter", "request", "requesty", "haimaker", "lockllm", "groq", "together",
    "fireworks", "cloudflare", "portkey", "truefoundry", "nanogpt", "tokenmix",
    "eden", "edenai", "helicone", "bifrost", "oneapi", "litellm", "ai21",
    # 国内聚合 / 路由网关
    "302", "volcengine", "openllmapi",
}

ROUTER_HOSTS = (
    "openrouter.com", "requesty.ai", "haimaker.ai", "lockllm", "groq.com",
    "api.groq.com", "together.xyz", "fireworks.ai", "cloudflare.com",
    "workers.ai", "portkey.ai", "truefoundry.ai", "tokenmix.ai", "eden.ai",
    # 国内聚合 / 路由网关 host
    "302.ai", "volces.com", "ark.cn-beijing.volces.com", "openllmapi.com",
)

DEFAULT_BLENDED_PER_MILLION = 1.0

CACHE_DISCOUNT = 0.1
PER_MILLION = 1_000_000  # 每百万 token / 每百万积分换算分母（成本货币化统一口径）

def effective_tokens_of(total_tokens, cached_tokens):
    """计费等效 token：原始 token 减去缓存命中享受的折扣量（cached 是 input 子集）。

    返回整数——token 是离散单位，浮点减法会产生 4,437,750.399999999 这类噪声，
    取整后再聚合可避免报告里出现无意义的浮点尾巴。
    """
    return max(int(round(total_tokens - (cached_tokens or 0) * (1 - CACHE_DISCOUNT))), 0)

HOME = Path.home()

WB_DIR = HOME / ".workbuddy"

TRACES_DIR = WB_DIR / "traces"

SESSIONS_DIR = WB_DIR / "sessions"

PROJECTS_DIR = WB_DIR / "projects"

DB_PATH = WB_DIR / "workbuddy.db"

USAGE_LOG_PATH = WB_DIR / "usage-log.json"

WORKBUDDY_SESSIONS = HOME / "WorkBuddy"

TZ = timezone(timedelta(hours=8))

def ts_to_date(ts, tz=TZ):
    """Unix 毫秒时间戳 → 'YYYY-MM-DD' 字符串"""
    if ts is None:
        return None
    return datetime.fromtimestamp(ts / 1000, tz).strftime("%Y-%m-%d")

def normalize_model(name):
    """模型名归一化：去空白、转小写；保留 :free 等后缀（其决定免费）。"""
    if not name:
        return "default"
    return name.strip().lower()

GLM52_FAMILY = {"glm-5.2", "glm-5.2-x", "glm-5.2x"}

GLM52_RATE = {"glm-5.2": 0.79, "glm-5.2-x": 0.50, "glm-5.2x": 0.50}

def glm52_discount_multiplier(model_name):
    """返回 GLM-5.2 家族消耗的折扣系数；非家族模型返回 1.0（不改其他模型计费）。

    系数按模型名确定：glm-5.2=0.79x（官方基础消耗速度），glm-5.2-x=0.5x（夜间折扣版，
    WorkBuddy 把「晚间调用 glm-5.2」记录为 -x）。夜间折扣已编码进模型名，无需时段判定。
    """
    return GLM52_RATE.get(normalize_model(model_name), 1.0)

CUSTOM_LOCAL_PRICING = {}

def _load_acc_product_config():
    """读取 WorkBuddy 服务端推送的产品配置缓存，提取官方积分倍率（models[].credits）。

    这是 「档位倍率权威数据源」：本地缓存优先，缺/坏则回退手工 mode_rates。
    返回 dict：{path, mtime, loaded, multipliers}，multipliers 为 {id: float|None}
    （credits 为 null 的模型标 None，表示未知，绝不按 0 处理）。
    文件缺失 / JSON 损坏 / 任何异常都安全降级为 loaded=False、空表，不向上抛。
    ⚠️ 该文件是内部产物、无稳定性承诺，且存在 conversation-product-spill 副本——只取 canonical
        那份 acc-product-config-v3.json，忽略 spill。
    """
    info = {"path": None, "mtime": None, "loaded": False, "multipliers": {}}
    try:
        cache_dir = Path(os.path.expanduser("~/.workbuddy/cache"))
        target = cache_dir / "acc-product-config-v3.json"  # 仅 canonical，勿读 spill 副本
        if not target.exists():
            return info
        data = json.loads(target.read_text(encoding="utf-8"))
        mult = {}
        for m in (data.get("models") or []):
            mid = m.get("id")
            if not mid:
                continue
            cr = m.get("credits")
            if cr is None:
                mult[mid] = None
            elif isinstance(cr, str) and cr.startswith("x"):
                try:
                    mult[mid] = float(cr[1:])
                except ValueError:
                    mult[mid] = None
            elif isinstance(cr, (int, float)):
                mult[mid] = float(cr)
        info["path"] = str(target)
        info["mtime"] = target.stat().st_mtime
        info["loaded"] = True
        info["multipliers"] = mult
    except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
        print(f"[WARN] 读取 acc-product-config-v3.json 失败，回退手工 mode_rates：{e}", file=sys.stderr)
    return info

def _load_pricing_config():
    """从 pricing.json 加载发布版定价，再合并 pricing.local.json 用户本地覆盖。

    额外加载档位估算单价（mode_rates）并并入 MODEL_PRICING，使档位别名可计价；
    并读取服务端配置缓存（acc-product-config-v3.json）用官方 credits 倍率覆盖 mode_rates 的
    multiplier（¥ 估算单价仍以手工锚定为准，因官方只给倍率不给 ¥）。
    """
    here = Path(__file__).resolve().parent
    cfg = {
        "models": dict(MODEL_PRICING),
        "timed_free": dict(TIMED_FREE),
        "low_confidence": dict(LOW_CONFIDENCE),
        "low_confidence_bias": dict(LOW_CONFIDENCE_BIAS),
        "scheduled_pricing": {k: list(v) for k, v in SCHEDULED_PRICING.items()},
        "custom_local": dict(CUSTOM_LOCAL_PRICING),
        "default_model": DEFAULT_MODEL,
        "delisted_models": set(),
        "user_custom_models": set(),
        "display_merge": {},
        "mode_rates": {},
        "mode_rates_meta": {},
    }
    cfg_path = here / "pricing.json"
    if cfg_path.exists():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(data.get("models"), dict):
                cfg["models"].update(data["models"])
            if isinstance(data.get("timed_free"), dict):
                cfg["timed_free"].update(data["timed_free"])
            if isinstance(data.get("low_confidence"), dict):
                # 成本置信度：模型名 -> 偏差原因说明；跳过 _comment 等元数据键
                cfg["low_confidence"].update(
                    {normalize_model(k): str(v) for k, v in data["low_confidence"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(data.get("low_confidence_bias"), dict):
                # 偏差方向：模型名 -> over/under/mixed；与 low_confidence 同键。
                # 渲染层据此画 ⚠↑/⚠↓，让用户一眼看出 L2 数字是虚高还是虚低。
                cfg["low_confidence_bias"].update(
                    {normalize_model(k): str(v).strip().lower() for k, v in data["low_confidence_bias"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(data.get("scheduled_pricing"), dict):
                # 时段定价：模型名 -> 规则列表（effect: free / peak / discount）。
                # 按调用时刻改写静态单价；未命中任何规则时完全不影响既有行为（零回归）。
                cfg["scheduled_pricing"].update(
                    {normalize_model(k): list(v) if isinstance(v, (list, tuple)) else [v]
                     for k, v in data["scheduled_pricing"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(data.get("delisted"), dict):
                # 已下架的官方模型：仍并入 models 以便历史调用计价，并记录到下架集合供报告标注
                cfg["models"].update(data["delisted"])
                cfg["delisted_models"].update(normalize_model(k) for k in data["delisted"])
            if isinstance(data.get("user_custom_models"), (list, tuple, set)):
                # 用户声明覆盖：这些模型名虽可能经 gateway 调用，但实为外部 API 自定义接入
                cfg["user_custom_models"].update(normalize_model(x) for x in data["user_custom_models"])
            if isinstance(data.get("custom_local"), dict):
                cfg["custom_local"].update(data["custom_local"])
            if isinstance(data.get("display_merge"), dict):
                # 显示层合并：变体名 -> 基础模型名（仅影响报告分组，不影响逐 trace 计费）
                cfg["display_merge"].update(
                    {normalize_model(k): str(v) for k, v in data["display_merge"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(data.get("mode_rates"), dict):
                # 档位估算单价（倍率锚定法）：fast / balanced / extreme →
                # {alias, label, multiplier, input, output}。并入 cfg["mode_rates"]。
                cfg["mode_rates"] = dict(data["mode_rates"])
            if data.get("default_model"):
                cfg["default_model"] = str(data["default_model"])
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"[WARN] 读取 pricing.json 失败，回退内置定价：{e}", file=sys.stderr)

    local_loaded = False
    local_path = here / "pricing.local.json"
    if local_path.exists():
        try:
            local = json.loads(local_path.read_text(encoding="utf-8"))
            if isinstance(local.get("models"), dict):
                cfg["models"].update(local["models"])
            if isinstance(local.get("delisted"), dict):
                cfg["models"].update(local["delisted"])
                cfg["delisted_models"].update(normalize_model(k) for k in local["delisted"])
            if isinstance(local.get("custom_local"), dict):
                cfg["custom_local"].update(local["custom_local"])
            if isinstance(local.get("user_custom_models"), (list, tuple, set)):
                cfg["user_custom_models"].update(normalize_model(x) for x in local["user_custom_models"])
            if isinstance(local.get("timed_free"), dict):
                cfg["timed_free"].update(local["timed_free"])
            if isinstance(local.get("low_confidence"), dict):
                cfg["low_confidence"].update(
                    {normalize_model(k): str(v) for k, v in local["low_confidence"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(local.get("low_confidence_bias"), dict):
                # 本地覆盖也允许改偏差方向
                cfg["low_confidence_bias"].update(
                    {normalize_model(k): str(v).strip().lower() for k, v in local["low_confidence_bias"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(local.get("display_merge"), dict):
                cfg["display_merge"].update(
                    {normalize_model(k): str(v) for k, v in local["display_merge"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(local.get("scheduled_pricing"), dict):
                # 本地覆盖允许新增 / 改写时段规则；同模型名整段替换，不做逐条合并
                cfg["scheduled_pricing"].update(
                    {normalize_model(k): list(v) if isinstance(v, (list, tuple)) else [v]
                     for k, v in local["scheduled_pricing"].items()
                     if not str(k).startswith("_")}
                )
            if isinstance(local.get("mode_rates"), dict):
                # 本地覆盖也允许改档位估算单价（优先级高于发布版 pricing.json）
                cfg["mode_rates"].update(local["mode_rates"])
            if local.get("default_model"):
                cfg["default_model"] = str(local["default_model"])
            local_loaded = True
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"[WARN] 读取 pricing.local.json 失败（数据格式错误/文件不存在/权限不足），忽略本地覆盖：{e}", file=sys.stderr)
    # ── 档位（mode_rates）并入 MODEL_PRICING + 官方倍率覆盖 ──
    acc = _load_acc_product_config()
    mode_rates = dict(cfg.get("mode_rates") or {})
    auto_estimate = bool(mode_rates.pop("auto_estimate", False))
    # 用官方 credits 倍率覆盖各档 multiplier（¥ 估算单价仍以手工锚定为准）
    for _name, t in mode_rates.items():
        if _name.startswith("_") or not isinstance(t, dict):
            continue
        alias = t.get("alias") or canonical_tier(_name)
        if alias in acc.get("multipliers", {}):
            ov = acc["multipliers"][alias]
            if ov is not None:
                t["multiplier"] = ov
        # 把 ¥ 估算单价写入 MODEL_PRICING，使 price_of(tier_alias) 直接可计价
        ip = t.get("input")
        op = t.get("output")
        if ip is not None and op is not None:
            cfg["models"][alias] = {"input": float(ip), "output": float(op)}
    cfg["mode_rates_meta"] = {
        "auto_estimate": auto_estimate,
        "config_cache_loaded": acc.get("loaded", False),
        "config_cache_path": acc.get("path"),
        "config_cache_mtime": acc.get("mtime"),
        # 最终生效的档位单价表（剔除 _comment 等元数据键）
        "rates": {k: v for k, v in mode_rates.items()
                  if not k.startswith("_") and isinstance(v, dict)},
    }
    return cfg, local_loaded

_PRICING, _PRICING_LOCAL_LOADED = _load_pricing_config()

MODEL_PRICING = _PRICING["models"]

TIMED_FREE = _PRICING["timed_free"]

# 成本置信度：模型名 -> 偏差原因说明。为空表示该模型估算可信。
LOW_CONFIDENCE = _PRICING["low_confidence"]

# 成本置信度偏差方向：与 LOW_CONFIDENCE 同键，值为 over/under/mixed（机读）。
LOW_CONFIDENCE_BIAS = _PRICING.get("low_confidence_bias", {})

# 时段定价：模型名 -> 规则列表，按调用时刻改写静态单价（见 SCHEDULED_PRICING 注释）。
SCHEDULED_PRICING = _PRICING.get("scheduled_pricing", {})

CUSTOM_LOCAL_PRICING = _PRICING["custom_local"]

DEFAULT_MODEL = _PRICING["default_model"]

DELISTED_MODELS = _PRICING.get("delisted_models", set())

DISPLAY_MERGE = _PRICING.get("display_merge", {})

MODE_RATES_META = _PRICING.get("mode_rates_meta", {})

def merge_display_key(name):
    """把模型名按 display_merge 映射为显示用的基础模型名；未配置则原样返回。"""
    if not name:
        return name
    return DISPLAY_MERGE.get(normalize_model(name), name)

USER_CUSTOM_MODELS = _PRICING.get("user_custom_models", set())

def discover_custom_models():
    """从 WorkBuddy 用户模型配置(~/.workbuddy/models.json)自动识别「用户自建模型」，并区分本地/外部。

    返回 (local, external) 两个集合：
      - local：Ollama 本地推理（vendor="ollama" 或 url 含 localhost:11434）。零 API 成本，
        报告里标 🏠、单价强制 0、不计入账单总额。
      - external：外部 API 接口自建（vendor="custom" 或 url 含 openrouter）。可能仍有费用，标 🔧。
    即使模型名也命中官方集（如 GLM-4.7-Flash 同时是官方下架模型），只要用户以自定义端点
    配置即优先判为自定义，避免被误标为官方网关（解决"撞名官方模型走 gateway"的误识别）。
    官方模型被重配（vendor=Kimi/DeepSeek/GLM）不标记。文件缺失/解析失败返回空集，
    回退到 pricing.local.json 的 user_custom_models 人工兜底。
    """
    local = set()
    external = set()
    router = set()
    path = os.path.expanduser("~/.workbuddy/models.json")
    try:
        with open(path, encoding="utf-8") as _f:
            data = json.load(_f)
    except (OSError, json.JSONDecodeError):
        return local, external, router
    entries = data if isinstance(data, list) else data.get("models", [])
    for e in entries:
        if not isinstance(e, dict):
            continue
        mid = normalize_model(e.get("id", ""))
        if not mid:
            continue
        vendor = (e.get("vendor") or "").lower()
        url = (e.get("url") or "").lower()
        # 智能路由 / 聚合网关（外部 API）：一次调用可能落到不同底层模型或上游 host。
        # 通过 vendor 或 url host 识别（权威来源是 models.json，与本地/外部识别同源）。
        is_router = vendor in ROUTER_VENDORS or any(h in url for h in ROUTER_HOSTS)
        if "localhost:11434" in url:
            local.add(mid)
        elif vendor == "ollama":
            local.add(mid)
        elif vendor == "custom" or "openrouter" in url or is_router:
            external.add(mid)
            if is_router:
                router.add(mid)
    return local, external, router

# 懒加载：导入期不读取 ~/.workbuddy/models.json，避免在生成 WorkBuddy / Claude / Codex 等
# 其它产品报告时越权访问用户模型配置（满足 ClawHub 比例性原则）。仅当用户显式涉及自建模型
# （custom-local）时，由聚合层按需调用 ensure_custom_models_discovered() 触发发现。
DISCOVERED_LOCAL: set = set()
DISCOVERED_EXTERNAL: set = set()
DISCOVERED_ROUTER: set = set()
ALL_LOCAL_MODELS: set = set()
ALL_ROUTER_MODELS: set = set()
ALL_CUSTOM_MODELS: set = set(USER_CUSTOM_MODELS)

_DISCOVERED_CACHE = None


def ensure_custom_models_discovered():
    """按需发现用户自建模型（读取 ~/.workbuddy/models.json）。

    幂等：多次调用只读取一次。原地变更 DISCOVERED_*/ALL_* 集合（消费者以名字 import，
    持有同一对象引用），保证跨模块可见。仅供涉及自建模型的报告路径触发。
    """
    global _DISCOVERED_CACHE, DISCOVERED_LOCAL, DISCOVERED_EXTERNAL, DISCOVERED_ROUTER
    global ALL_LOCAL_MODELS, ALL_ROUTER_MODELS, ALL_CUSTOM_MODELS
    if _DISCOVERED_CACHE is not None:
        return _DISCOVERED_CACHE
    local, external, router = discover_custom_models()
    _DISCOVERED_CACHE = (local, external, router)
    DISCOVERED_LOCAL.clear(); DISCOVERED_LOCAL |= local
    DISCOVERED_EXTERNAL.clear(); DISCOVERED_EXTERNAL |= external
    DISCOVERED_ROUTER.clear(); DISCOVERED_ROUTER |= router
    ALL_LOCAL_MODELS.clear(); ALL_LOCAL_MODELS |= local
    ALL_ROUTER_MODELS.clear(); ALL_ROUTER_MODELS |= router
    ALL_CUSTOM_MODELS.clear(); ALL_CUSTOM_MODELS |= USER_CUSTOM_MODELS | local | external
    return _DISCOVERED_CACHE

def parse_channel(raw_model_id):
    """从模型标识符解析「API 接口通道」。

    模型标识符本身编码了接口位置（并非独立字段，trace 还会把前缀剥掉）：
      - "auto"                       → ("router", "auto")             WorkBuddy 默认网关内的智能路由
      - "custom-local:GLM-4.5-air"   → ("custom-local", "glm-4.5-air") 用户自建本地接口
      - "inclusionai/...:free"       → ("openrouter-free", raw)        OpenRouter 免费网关（凭 :free 判定）
      - "custom-local:z.ai/GLM-5.2"  → ("custom-local", "z.ai/GLM-5.2") 用户自建接口（含 / 但非免费）
      - "glm-5.2" / "hy3" 等裸名     → ("gateway", raw)                WorkBuddy 默认网关
    返回 (channel, base_model)。base_model 为去掉通道前缀后的底层模型名。
    """
    raw = (raw_model_id or "default").strip()
    n = raw.lower()
    if n == "auto":
        return ("router", "auto")
    # 档位（路由三档）：快速 / 均衡 / 极致。归入独立 "tier" 通道，与 legacy auto 区分，
    # 且不复用 router 早期返回——tier 有显式估算单价（见 price_of 的 gateway 分支命中 MODEL_PRICING）。
    # 规范 id 经 TIER_CANON 把 trace 字面量 extreme-model 归一为配置缓存的 deep-model。
    if n in TIER_ALIASES:
        return ("tier", canonical_tier(n))
    # OpenRouter 免费档：含 :free 后缀即免费（无论是否套了 custom-local 前缀）→ 价 0
    # 注意：仅凭 / 不再判定为 openrouter-free——SiliconFlow 等聚合网关也用 Vendor/Model 命名，
    # 其中不少是付费模型（如 z.ai/GLM-5.2），凭 / 当免费会少算钱。
    if ":free" in n:
        return ("openrouter-free", raw)
    if n.startswith("custom-local:"):
        return ("custom-local", raw[len("custom-local:"):].strip())
    # Claude Code 外部入口：claude-code: 前缀标识来自 Claude Code 数据源的模型，
    # 计价走官方 Anthropic 刊例价（见 price_of 的 claude-code 分支命中 MODEL_PRICING）。
    if n.startswith("claude-code:"):
        return ("claude-code", raw[len("claude-code:"):].strip())
    # Codex CLI 外部入口：codex: 前缀标识来自 Codex 数据源的模型，
    # 计价走 OpenAI 刊例价（见 price_of 的 codex 分支命中 MODEL_PRICING）。
    if n.startswith("codex:"):
        return ("codex", raw[len("codex:"):].strip())
    # 千问办公外部入口：qwenwork: 前缀标识来自 QwenWork 数据源，模型位是**档位**
    # （flash / pro / qwork-lite / qmodel_latest）而非裸模型名。千问办公按积分订阅
    # 计费、无公开单 token 刊例价，故 pricing.json 故意不配这些档位：
    # 未命中单价时按通用约定「计入 token、不计成本、报告提示补价路径」处理。
    if n.startswith("qwenwork:"):
        return ("qwenwork", raw[len("qwenwork:"):].strip())
    # SiliconFlow 等第三方 API 接入：trace 中保留 Vendor/Model 前缀，但 sessions.model
    # 可能未带 custom-local: 前缀；凭 vendor 前缀强制判为 custom-local，避免混入官方入口。
    if any(n.startswith(p) for p in SILICONFLOW_VENDOR_PREFIXES):
        return ("custom-local", raw)
    return ("gateway", raw)

_HOUR_RANGE_RE = re.compile(r"^(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})$")

# 星期别名：1=周一 … 7=周日（与 datetime.isoweekday() 一致，便于直接比对）
_DOW_ALIASES = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6, "sun": 7}


def iso_to_dt(iso_str, tz=TZ):
    """ISO 8601 字符串 → datetime（tz 感知，默认北京时间）；解析失败返回 None。

    无时区后缀的朴素时间戳按北京时间解释（官方用量导出即此格式）。
    """
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(str(iso_str).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def call_time_of(started_at, date_str=None, tz=TZ):
    """把一次调用的 started_at 解析成 price_of 的时段入参字典。

    兼容两种输入：Unix 毫秒时间戳（int/float 或纯数字字符串）与 ISO 8601 字符串
    （trace 与各适配器的 started_at 两种写法都见过，见 collect_usage_data._parse_started_at）。
    返回 {'as_of_date', 'as_of_hour', 'as_of_dow'}；解析不到的维度为 None —— 规则判定
    对缺失维度采取「不套用该维度规则」的保守策略，宁可少打折也不乱打折。

    >>> call_time_of('2026-09-12 11:30:00')['as_of_hour']
    11
    """
    dt = None
    if isinstance(started_at, bool):
        dt = None
    elif isinstance(started_at, (int, float)):
        dt = ts_to_dt(started_at, tz)
    elif isinstance(started_at, str) and started_at.strip():
        s = started_at.strip()
        try:
            dt = ts_to_dt(int(s), tz)
        except ValueError:
            dt = iso_to_dt(s, tz)
    if dt is None:
        return {"as_of_date": date_str or None, "as_of_hour": None, "as_of_dow": None}
    return {
        "as_of_date": dt.strftime("%Y-%m-%d"),
        "as_of_hour": dt.hour,
        "as_of_dow": dt.isoweekday(),
    }


def _dow_set(raw):
    """把规则的 dow 字段解析成 {1..7} 集合；无法识别的项丢弃。"""
    out = set()
    for x in raw or ():
        if isinstance(x, bool):
            continue
        if isinstance(x, int):
            if 1 <= x <= 7:
                out.add(x)
            continue
        key = str(x).strip().lower()[:3]
        if key in _DOW_ALIASES:
            out.add(_DOW_ALIASES[key])
    return out


def _hour_ranges(raw):
    """把规则的 hours 字段解析成 [(start_hour, end_hour), ...]；非法项丢弃。"""
    out = []
    for item in raw or ():
        m = _HOUR_RANGE_RE.match(str(item).strip())
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(3))
        if 0 <= a <= 23 and 0 <= b <= 23:
            out.append((a, b))
    return out


def _hour_in(hour, ranges):
    """判断 hour 是否落在任一时段内（左闭右开；end<=start 视为跨午夜）。"""
    if hour is None:
        return False
    for a, b in ranges:
        if a <= b:
            if a <= hour < b:
                return True
        elif hour >= a or hour < b:  # 跨午夜，如 23:00-08:00
            return True
    return False


def _schedule_matches(sched, as_of_date=None, as_of_hour=None, as_of_dow=None):
    """判断一条时段规则是否命中该调用时刻。

    缺失的维度按「不命中」处理：规则声明了 hours 但拿不到 as_of_hour 时不生效，
    避免把白天的调用误判进夜间免费。
    """
    if not isinstance(sched, dict):
        return False
    if sched.get("from") and (not as_of_date or as_of_date < str(sched["from"])):
        return False
    if sched.get("until") and (not as_of_date or as_of_date > str(sched["until"])):
        return False
    dows = _dow_set(sched.get("dow"))
    if dows and as_of_dow not in dows:
        return False
    hrs = _hour_ranges(sched.get("hours"))
    if hrs and not _hour_in(as_of_hour, hrs):
        return False
    return True


def scheduled_rule_for(model_name, as_of_date=None, as_of_hour=None, as_of_dow=None):
    """返回该模型在该时刻命中的**第一条**时段规则（dict）；无命中返回 None。

    规则按配置顺序判定，故更特殊的规则应写在前面。
    """
    schedules = SCHEDULED_PRICING.get(normalize_model(model_name)) or []
    if isinstance(schedules, dict):  # 容错：允许配置成单条规则而非列表
        schedules = [schedules]
    for sched in schedules:
        if _schedule_matches(sched, as_of_date, as_of_hour, as_of_dow):
            return sched
    return None


def is_scheduled_free(model_name, as_of_date=None, as_of_hour=None, as_of_dow=None):
    """该模型在该时刻是否被时段规则判为免费（effect=free）。"""
    sched = scheduled_rule_for(model_name, as_of_date, as_of_hour, as_of_dow)
    return bool(sched) and str(sched.get("effect") or "").strip().lower() == "free"


def resolve_scheduled_price(ip, op, model_name, as_of_date=None, as_of_hour=None,
                            as_of_dow=None, model_entry=None):
    """按命中规则改写静态单价，返回 (ip, op, sched)；未命中/单价缺失时原样返回 (ip, op, None)。

    effect 语义：
      free     → (0.0, 0.0)
      peak     → 优先取 model_entry 的 peak_input/peak_output；否则基础价 × factor（缺省 2.0）
      discount → 基础价 × factor（缺省 1.0，即不变）
    未识别的 effect 视为不生效，返回 (ip, op, None)。
    """
    sched = scheduled_rule_for(model_name, as_of_date, as_of_hour, as_of_dow)
    if not sched or ip is None or op is None:
        return ip, op, None
    effect = str(sched.get("effect") or "").strip().lower()
    try:
        factor = float(sched.get("factor")) if sched.get("factor") is not None else None
    except (TypeError, ValueError):
        factor = None
    if effect == "free":
        return 0.0, 0.0, sched
    if effect == "peak":
        entry = model_entry if isinstance(model_entry, dict) else {}
        pip, pop = entry.get("peak_input"), entry.get("peak_output")
        if pip is not None and pop is not None:
            return float(pip), float(pop), sched
        return ip * (factor if factor is not None else 2.0), op * (factor if factor is not None else 2.0), sched
    if effect == "discount":
        return ip * (factor if factor is not None else 1.0), op * (factor if factor is not None else 1.0), sched
    return ip, op, None


def is_timed_free(model_name, as_of_date):
    """判断模型在 as_of_date('YYYY-MM-DD') 是否处于限时免费期内（含截止当天）。

    仅看「模型名 + 日期」：与通道无关（hy3 无论走默认网关还是 custom-local 都适用）。
    无截止配置或日期缺失则返回 False。
    """
    if not as_of_date:
        return False
    deadline = TIMED_FREE.get(normalize_model(model_name))
    return bool(deadline) and as_of_date <= deadline

def low_confidence_reason(model_name):
    """返回该模型「成本估算不可信」的原因说明；可信则返回空字符串。

    用于报告把受服务端时段 / 配额减免影响的模型标为「低置信度」，
    并提示用户不要据此做预算。数据源为 pricing.json 的 low_confidence 段
    （可用 pricing.local.json 覆盖）。
    """
    if not model_name:
        return ""
    return LOW_CONFIDENCE.get(normalize_model(model_name), "") or ""


def low_confidence_bias(model_name):
    """返回该模型低置信度偏差方向（机读）：'over' / 'under' / 'mixed' / ''（空=可信）。

    与 low_confidence_reason 配套，供报告渲染方向箭头
    （⚠↑ 高估 / ⚠↓ 低估 / ⚠ 方向不明），让用户一眼看出 L2 静态估算
    是虚高还是虚低。数据源为 pricing.json 的 low_confidence_bias 段。
    """
    if not model_name:
        return ""
    return LOW_CONFIDENCE_BIAS.get(normalize_model(model_name), "") or ""

def price_of(model_name, channel=None, as_of_date=None, as_of_hour=None, as_of_dow=None):
    """返回 (input_per_million, output_per_million) 元；未配置 / 未知返回 (None, None)。

    channel 为空时自动从 model_name 解析（支持 custom-local:/:free/auto 等编码）。
    as_of_date('YYYY-MM-DD') 用于限时免费判定：若模型在该日期处于 TIMED_FREE 期内，返回 (0.0, 0.0)。

    时段定价：as_of_hour(0-23) 与 as_of_dow(1=周一…7=周日) 让「夜间免费 /
    峰谷双档 / 限期促销」这类**按时刻变化**的服务端规则得以生效（见 SCHEDULED_PRICING）。
    三者可只传部分；缺失维度按「不套用该维度规则」处理（见 _schedule_matches）。
    """
    model_name = resolve_model(model_name)
    if channel is None:
        channel, model_name = parse_channel(model_name)
    if channel == "openrouter-free":
        return (0.0, 0.0)
    # 本地模型（Ollama / localhost:11434）零 API 成本：强制归零，杜绝借用同名官方价
    # （如 custom-local 通道的 glm-4.5-air 原本会查到官方下架价 1.2/8.0）。不计入账单总额。
    # 注意去前缀：显式传入 channel 时 model_name 可能仍带 custom-local: 前缀。
    if normalize_model(model_name.split("custom-local:", 1)[-1]) in ALL_LOCAL_MODELS:
        return (0.0, 0.0)
    if channel == "router":
        return (None, None)
    # 限时免费：在截止日（含）之前的调用免费（与通道无关，gateway / custom-local 均适用）
    if as_of_date and is_timed_free(model_name, as_of_date):
        return (0.0, 0.0)
    # —— 取静态基础单价 ——
    entry = None
    if channel == "custom-local":
        # 优先用用户覆盖表；否则默认对齐默认网关下同名模型的单价
        entry = CUSTOM_LOCAL_PRICING.get(normalize_model(model_name)) or None
    if entry is None:
        # Claude Code / Codex 外部入口与 gateway 同源：均按裸模型名查官方刊例价
        # （通道前缀已在 parse_channel 去掉；OpenAI 模型单价见 pricing.json 的 codex 估算段）。
        entry = MODEL_PRICING.get(normalize_model(model_name))
    if entry is None:
        return (None, None)
    ip, op = entry.get("input"), entry.get("output")
    if ip is None or op is None:
        return (ip, op)
    # —— 时段定价：夜间免费 / 峰谷双档 / 限期促销 ——
    ip, op, _matched = resolve_scheduled_price(
        ip, op, model_name, as_of_date, as_of_hour, as_of_dow, model_entry=entry)
    return (ip, op)

def compute_cost(input_tokens, output_tokens, model_name, channel=None,
                 as_of_date=None, as_of_hour=None, as_of_dow=None):
    """按输入/输出单价精确计算成本（元）。未配置单价返回 None。"""
    ip, op = price_of(model_name, channel, as_of_date=as_of_date,
                      as_of_hour=as_of_hour, as_of_dow=as_of_dow)
    if ip is None or op is None:
        return None
    return round((input_tokens / PER_MILLION) * ip + (output_tokens / PER_MILLION) * op, 4)

def trace_cost(input_tokens, output_tokens, model_name, channel=None,
               as_of_date=None, as_of_hour=None, as_of_dow=None):
    """用于既有表格的成本：配置了单价用精确值；未配置回退历史 blended 估算，保持现有显示不破。"""
    c = compute_cost(input_tokens, output_tokens, model_name, channel,
                     as_of_date=as_of_date, as_of_hour=as_of_hour, as_of_dow=as_of_dow)
    if c is None:
        return round((input_tokens + output_tokens) / PER_MILLION * DEFAULT_BLENDED_PER_MILLION, 4)
    return c

def ts_to_dt(ts, tz=TZ):
    """Unix 毫秒时间戳 → datetime"""
    if ts is None:
        return None
    return datetime.fromtimestamp(ts / 1000, tz)

def iso_to_date(iso_str, tz=TZ):
    """ISO 8601 字符串 → 'YYYY-MM-DD' 字符串"""
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.astimezone(tz).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def token_active_session_ids(traces):
    """「有 token 活动」的唯一口径：会话有 trace 且该条 trace 的 total_tokens > 0。

    §一 会话总数补充、§4.2 每会话分布、§五/§十 任务类型计数都由它派生。
    各节曾经各自定义（一处看「有 trace」、一处看「有 token」），千问办公这种
    字符估算口径下偶发 0-token 会话，就会让 §5=8 而 §1=7 当场打架。
    """
    ids = set()
    for t in traces or []:
        sid = t.get("session_id")
        if sid and (t.get("total_tokens") or 0) > 0:
            ids.add(sid)
    return ids


def parse_date_range(days):
    """返回 (start_date, end_date) 字符串（滚动 N 天，含今天）"""
    end = datetime.now(TZ)
    start = end - timedelta(days=days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

PERIOD_DAYS = {
    "day": 1,
    "week": 7,
    "month": 30,
    "year": 365,
}

PERIOD_LABELS = {
    "day": "日报",
    "week": "周报",
    "month": "月报",
    "year": "年报",
    "custom": "自定义报告",
}

PERIOD_SHORT = {
    "day": "当日",
    "week": "本周",
    "month": "本月",
    "year": "本年",
    "custom": "本期",
}

PERIOD_NEXT = {
    "day": "次日",
    "week": "下周",
    "month": "下月",
    "year": "明年",
    "custom": "下期",
}

def _to_num(v, default=0):
    """安全地把值转成 float；无法转换（脏数据/字符串/None）时回退默认值，避免整段采集崩溃。"""
    try:
        return float(v)
    except (TypeError, ValueError):
        return default

def resolve_date_range(period=None, days=None, start=None, end=None):
    """解析时间窗口，返回 (start_date, end_date, period_key, period_label)。

    优先级：绝对日期(start+end) > 自定义天数(days) > 预设周期(period)。
    - 绝对日期：直接使用给定起止（含两端）。
    - 自定义天数：最近 N 天（滚动窗口，含今天）。
    - 预设周期（日历对齐，与生成时刻无关）：
      day=今天 / week=当前日历周(周一~周日) / month=当前自然月(1日~月底) / year=当前自然年(1/1~12/31)。
    """
    if start and end:
        # 若起止恰好对应标准周期长度，识别为对应报告类型（而非「自定义报告」），
        # 使「报告类型」能以日历日期呈现：
        #   单日 → 日报；完整 7 天 → 周报；完整月 → 月报；完整年 → 年报。
        try:
            sd = datetime.strptime(start, "%Y-%m-%d")
            ed = datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"无效的 --start/--end 日期：需要 YYYY-MM-DD 格式，"
                f"收到 start={start!r} end={end!r}"
            )
        span = (ed - sd).days + 1
        today = datetime.now(TZ).date()
        if span == 1:
            return start, end, "day", PERIOD_LABELS["day"]
        # 完整自然年（1/1~12/31）或 年初至今（1/1~今年内且至今日）→ 年报
        if sd.month == 1 and sd.day == 1 and ed.year == sd.year:
            if (ed.month == 12 and ed.day == 31) or ed.date() >= today:
                return start, end, "year", PERIOD_LABELS["year"]
        # 完整自然月 → 月报
        if sd.day == 1 and ed.year == sd.year and ed.month == sd.month:
            last_day = calendar.monthrange(sd.year, sd.month)[1]
            if ed.day == last_day:
                return start, end, "month", PERIOD_LABELS["month"]
        # 完整 7 天 → 周报
        if span == 7:
            return start, end, "week", PERIOD_LABELS["week"]
        return start, end, "custom", PERIOD_LABELS["custom"]
    if days is not None:
        e = datetime.now(TZ)
        s = e - timedelta(days=days)
        return (s.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d"),
                "custom", f"自定义（最近 {days} 天）")
    pk = period or "week"
    today = datetime.now(TZ).date()
    if pk == "day":
        d = today.strftime("%Y-%m-%d")
        return d, d, "day", PERIOD_LABELS["day"]
    if pk == "week":
        # 当前日历周（周一 ~ 周日，ISO 周），不论生成日在周中还是周末
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        return (monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d"),
                "week", PERIOD_LABELS["week"])
    if pk == "month":
        # 当前自然月（1 日 ~ 月底），不论生成日在月内哪一天
        first = today.replace(day=1)
        last = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        return (first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d"),
                "month", PERIOD_LABELS["month"])
    if pk == "year":
        # 当前自然年（1/1 ~ 12/31）
        y = today.year
        return f"{y}-01-01", f"{y}-12-31", "year", PERIOD_LABELS["year"]
    # 兜底（choices 已约束，正常不会到这）：保留滚动窗口行为
    n = PERIOD_DAYS.get(pk, 7)
    e = datetime.now(TZ)
    s = e - timedelta(days=n)
    return s.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d"), pk, PERIOD_LABELS.get(pk, "周报")

TASK_TYPE_RULES = [
    # 1. 技能安装 —— 明确安装技能的表述
    ("技能安装", [r"skillhub\s+install", r"安装.*skill", r"install.*skill", r"技能安装",
                   r"添加.*技能", r"下载.*skill|skill.*下载", r"技能\s*添加"]),
    # 2. 技能开发 —— 创作/打包新的技能
    ("技能开发", [r"SKILL\.md", r"skill.*creat", r"skill.*develop", r"技能.*创建", r"技能.*开发",
                   r"打包.*skill", r"开发.*skill", r"skill\s*开发", r"从零.*skill",
                   r"封装.*skill", r"技能.*封装", r"skill\s*打包"]),
    # 3. 报告生成 —— 生成周报、月报等报告类任务
    ("报告生成", [r"周报", r"weekly.*report", r"report.*generat", r"AI.*report",
                   r"生成.*报告", r"报告.*生成", r"月报", r"年报", r"日报",
                   r"生成.*摘要", r"统计.*报告", r"分析.*报告"]),
    # 4. Bug修复 —— 调试、错误处理
    ("Bug修复", [r"bug", r"修复", r"fix", r"误报", r"debug", r"调试", r"错误", r"速率限制",
                r"报错", r"错误.*修复", r"bug.*fix", r"异常.*处理"]),
    # 5. 内容生成 —— 创作类任务（优先级高于代码开发，避免“创建团队”误判）
    ("内容生成", [r"短剧", r"剧本", r"分镜", r"小说", r"文案", r"故事", r"剧情",
                  r"台词", r"旁白", r"文生图", r"文生视频", r"图生视频", r"AI生成.*图",
                  r"图像生成", r"长文本", r"中长文本", r"连续.*生成", r"content.*generat",
                  r"创作", r"角色设定.*(短剧|剧本|小要|分镜)",
                  r"脚本.*编写", r"剧本.*创作", r"视频脚本", r"配音稿",
                  r"营销文案", r"广告语", r"产品描述", r"产品文案",
                  # 生成物指纹（含已删除）：图片/视频生成工具调用 + 媒体文件名。
                  r"imagegen", r"videogen",
                  r"\[artifacts\][^\]]*\.(png|jpe?g|gif|webp|mp4|webm|mov)",
                  r"生成.*图片", r"生成.*视频"]),
    # 6. 代码开发 —— 编程类任务
    ("代码开发", [r"编程", r"python", r"练习", r"编写.*代码", r"实现.*功能", r"新增.*功能",
                  r"编码", r"写代码", r"代码实现", r"实现.*算法", r"调试.*脚本",
                  r"github", r"上传.*代码", r"添加.*支持", r"多格式", r"代码.*编写",
                  r"函数.*实现", r"模块.*开发", r"package.*json", r"requirements.*txt"]),
    # 7. 自动化配置 —— 自动化任务配置（高置信短语，避免 incidental 命中）
    ("自动化配置", [r"自动化.*任务", r"配置.*自动化", r"设置.*自动化", r"定时.*任务",
                   r"schedul", r"领券", r"提醒", r"每日.*任务", r"每日.*提醒",
                   r"cron.*表达式", r"周期.*任务", r"任务.*调度", r"自动化.*脚本"]),
    # 8. 环境搭建 —— 开发环境配置
    ("环境搭建", [r"SkillHub", r"环境搭建", r"配置.*python", r"install.*cli", r"环境变量",
                  r"python.*环境", r"虚拟环境.*构建", r"conda", r"poetry",
                  r"依赖.*安装", r"package.*install", r"node.*环境"]),
    # 9. 研究学习 —— 学习、调研、参考资料
    ("研究学习", [r"第一性原理", r"first\s*principle", r"学习", r"研究", r"教程",
                  r"调研", r"趋势", r"对比", r"了解", r"用途", r"主线",
                  r"学习.*笔记", r"知识.*总结", r"原理.*分析", r"文档.*阅读",
                  r"官方.*文档", r"指南.*学习"]),
    # 10. 代码分析 —— 分析、审查、诊断
    ("代码分析", [r"hermes", r"agent.*prompt", r"解构", r"分析.*项目", r"代码.*分析", r"代码结构",
                  r"健康检查", r"审查", r"解读", r"诊断", r"代码.*审查",
                  r"性能.*分析", r"代码.*诊断", r"项目.*分析"]),
    # 11. 文档编写 —— 文档、规范、流程
    ("文档编写", [r"指南", r"guide", r"文档", r"workflow", r"规范", r"流程", r"交付",
                   r"编写.*文档", r"文档.*编写", r"操作手册", r"使用说明",
                   r"安装指南", r"配置指南", r"API.*文档"]),
]

# ── 任务分类规则外置 + 加权评分 ──────────────────────────────────────
# 规则优先从 scripts/task_rules.json 读取（可由用户直接编辑，含权重）；
# 文件缺失或解析失败时回退到上方内置 TASK_TYPE_RULES（全部权重 1.0）。

TASK_RULES_PATH = Path(__file__).resolve().parent / "task_rules.json"

_TASK_SCORING_DEFAULTS = {
    "default_weight": 1.0,        # patterns 未标 w 时的默认权重
    "repeat_decay": 0.35,         # 同一 pattern 重复命中的衰减系数（防刷词）
    "length_bonus_per_char": 0.012,   # pattern 字面越长越具体，微加分
    "max_length_bonus": 0.6,      # 长度加分上限
    "low_confidence_threshold": 0.25,  # 置信度低于此值视为不确定
    "auto_word_boundary": True,   # 纯 ASCII 词 pattern 自动加 \b（修 fix→prefix 误匹配）
}

_TASK_TYPES_FALLBACK = [
    {"name": name, "priority": i, "patterns": [{"p": p, "w": 1.0} for p in pats]}
    for i, (name, pats) in enumerate(TASK_TYPE_RULES, 1)
]


def load_task_rules(path=None):
    """加载任务分类规则。返回 (types, meta, source)。

    types: [{"name", "priority", "patterns": [{"p", "w"}]}]
    meta:  评分参数字典（含 default_weight / repeat_decay 等）
    source: "task_rules.json" 或 "builtin"
    文件缺失 / 解析失败 / 结构不合法 → 静默回退内置规则，绝不抛异常。
    """
    p = Path(path) if path else TASK_RULES_PATH
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            types_raw = data.get("types")
            if isinstance(types_raw, dict) and types_raw:
                meta = dict(_TASK_SCORING_DEFAULTS)
                meta.update(data.get("_meta", {}).get("scoring", {}) or {})
                types = []
                for name, spec in types_raw.items():
                    if not isinstance(spec, dict):
                        continue
                    pats = []
                    for item in spec.get("patterns", []):
                        if isinstance(item, str) and item:
                            pats.append({"p": item, "w": float(meta["default_weight"])})
                        elif isinstance(item, dict) and item.get("p"):
                            try:
                                w = float(item.get("w", meta["default_weight"]))
                            except (TypeError, ValueError):
                                w = float(meta["default_weight"])
                            pats.append({"p": str(item["p"]), "w": w})
                    if pats:
                        try:
                            prio = int(spec.get("priority", 999))
                        except (TypeError, ValueError):
                            prio = 999
                        types.append({"name": str(name), "priority": prio, "patterns": pats})
                if types:
                    types.sort(key=lambda t: (t["priority"], t["name"]))
                    return types, meta, "task_rules.json"
        except (json.JSONDecodeError, OSError, AttributeError):
            pass
    return _TASK_TYPES_FALLBACK, dict(_TASK_SCORING_DEFAULTS), "builtin"


_ASCII_WORD_RE = re.compile(r"^[A-Za-z0-9_]+$")


def _compiled_patterns(types, meta):
    """把规则编译为 [(type_name, priority, regex, weight)]，含词边界处理。"""
    out = []
    for t in types:
        for item in t["patterns"]:
            pat = item["p"]
            if meta.get("auto_word_boundary") and _ASCII_WORD_RE.match(pat):
                # 纯 ASCII 词（如 fix / python）：两侧加 \b，避免 fix 误匹配 prefix
                pat = r"\b" + pat + r"\b"
            try:
                out.append((t["name"], t["priority"], re.compile(pat, re.IGNORECASE), item["w"]))
            except re.error:
                continue  # 用户写坏的正则直接跳过，不让整个分类崩掉
    return out


def score_task_types(text, types=None, meta=None):
    """对文本做加权评分，返回所有任务类型的得分明细（核心）。

    评分模型：
      - 每个 pattern 基础分 = 权重 w + 长度加分（pattern 越长越具体）；
      - 同一 pattern 重复命中按几何级数衰减（1 + d + d² + …，d=repeat_decay），
        多个**不同** pattern 命中则各自累加——信号多样性比刷词更有说服力；
      - 纯 ASCII 词自动加词边界。
    返回 {"scores": {类型: 分}, "top": 类型|None, "second": 分, "confidence": 0~1}。
    """
    if types is None or meta is None:
        types, meta, _src = load_task_rules()
    text = (text or "").lower()
    if not text.strip():
        return {"scores": {}, "top": None, "second": 0.0, "confidence": 0.0}
    scores = {}
    for tname, _prio, rx, w in _compiled_patterns(types, meta):
        hits = len(rx.findall(text))
        if not hits:
            continue
        length_bonus = min(len(rx.pattern) * meta["length_bonus_per_char"], meta["max_length_bonus"])
        base = w + length_bonus
        d = meta["repeat_decay"]
        # 几何级数：1 + d + d² + … (hits 项)，重复命中收益递减但非零
        gain = base * (1 - d ** hits) / (1 - d) if d > 0 else base * hits
        scores[tname] = scores.get(tname, 0.0) + gain
    if not scores:
        return {"scores": {}, "top": None, "second": 0.0, "confidence": 0.0}
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_name, top_score = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0.0
    confidence = (top_score - second) / top_score if top_score > 0 else 0.0
    return {"scores": scores, "top": top_name, "second": second,
            "confidence": round(min(confidence, 1.0), 4)}

SYSTEM_REMINDER_RE = re.compile(r"<system-reminder.*?</system-reminder>", re.DOTALL)

MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp",
              ".mp4", ".webm", ".mov", ".avi", ".mkv", ".mp3", ".wav"}

_CHEAPER_ALT = {
    "glm-5.2": ("minimax-m3", "简单/模板类任务可迁移至 MiniMax-M3（约 ¥1/百万 tokens）"),
    "glm-5.1": ("minimax-m3", "简单任务可迁移至 MiniMax-M3（约 ¥1/百万 tokens）"),
    "glm-5": ("minimax-m3", "简单问答/抽取类任务可迁移至 MiniMax-M3（约 ¥1/百万 tokens）"),
    "glm-4.7": ("minimax-m3", "简单任务可迁移至 MiniMax-M3（约 ¥1/百万 tokens）"),
    "deepseek-v4-pro": ("deepseek-v4-flash", "简单检索/改写类任务可迁移至 DeepSeek-V4-Flash（约 ¥1/百万 tokens）"),
    "hy3": ("minimax-m3", "如非限时免费期，简单问答/抽取类任务可迁移至 MiniMax-M3"),
}
