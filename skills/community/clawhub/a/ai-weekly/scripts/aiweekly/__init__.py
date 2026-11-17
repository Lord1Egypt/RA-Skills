"""aiweekly · AI 周报生成器内部包。

设计原则：
- 按职责垂直切分（P1#1 已全部落地，20 模块）：
    utils              — 日期解析 / 网络 IO / 代理 / 区域探测 / 重试退避 / JSON 读写
    translate          — 本地 Ollama 英文中译 + 健康探测
    news               — 外部合并 / 信源归一 / 摘要压缩 / 语言判定 / 重要度评分
    leaderboard_sources — 多源池抓取（LMArena / HF / OpenCompass / SuperCLUE / ModelScope）
    leaderboard        — 多源榜合并 / 快照兜底 / 成本与档案富化 / 选型结论
    leaderboard_fetch  — 单源抓取执行 / 健康记录（SOURCES / LB_CRITERIA / _collect_source_results / _record_health / HEALTH_PATH；P0#4 硬守护拆出，避免 leaderboard.py 越 800 行）
    leaderboard_checks  — 榜单资料卡权威覆盖校验（P0#4 硬守护拆出）
    leaderboard_snapshot — 榜单时序快照 / 本地缓存 / 国内权威榜兜底快照的读写与清洗
    market             — 市场规模与融资数据 / Chart.js 构建 / 本周信号 × 趋势洞察桥接
    market_snapshot    — 外置市场快照读取 / 兜底常量 / 过期判定与体检
    insights           — 看点卡 / 导语 / 关键词彩标 / 受众 chips（全部服务端预渲染）
    model_meta         — 模型元数据查找（成本 / 上下文 / 许可证 / 币种）
    render             — HTML 渲染 + XSS 安全序列化
    charts_svg         — 服务端内联 SVG 图表（零 JS / 零 Canvas 依赖）
    canon              — 模型名归一化原语（叶子模块，拆解 leaderboard↔model_meta / ↔leaderboard_checks 循环依赖）
    const              — 硬约束常量
    errors             — 错误码体系
    health             — 源健康检查
    diagnostics        — 运行告警的「人话翻译」（错误提示渲染）
    cli_utils          — 构建时通用工具（_CountingWriter / _parse_csv_arg 等，从主入口下沉）
- 公开 API 通过包级 re-export 暴露；外部仍可用 `from generate_site import generate`（兼容垫层）。
  体量较大的 leaderboard / market / insights 不在包级 re-export，按需
  `from aiweekly.leaderboard import fetch_all_leaderboards` 或经 generate_site 垫层取用。
- 模块内部私有函数以下划线前缀，模块级 `__all__` 显式声明对外接口。
- 可测试性（P1#6）：`_http_get` / `_probe` / `_detect_region` / `_retry_fetch` /
  `_ollama_translate` 均接受注入参数（opener / probe / sleeper / client），单测可脱网。

变更请同步更新 CHANGELOG.md 与 references/SKILL_full.md §10.1 的模块清单。
"""
from aiweekly.utils import (
    _UA,
    _PROXY_OVERRIDE,
    _SOCKS_ACTIVE,
    _resolved_proxy,
    _configure_proxy,
    _build_opener,
    _http_get,
    _probe,
    _detect_region,
    _retry_fetch,
    _parse_date_arg,
    _parse_snapshot_date,
)
from aiweekly.translate import (
    Translator,
    OllamaUnavailable,
    ollama_health,
    ollama_base_url,
    _ollama_translate,
)
from aiweekly.news import (
    SUMMARY_MAX,
    SUMMARY_TARGET,
    MUSTREAD_TOP_N,
    LEADERBOARD_STALE_DAYS,
    SOURCE_ALIASES,
    SOURCE_AUTHORITY,
    CATEGORY_WEIGHT,
    DEFAULT_SOURCE_AUTHORITY,
    DEFAULT_CATEGORY_WEIGHT,
    OPEN_SOURCE_PROVIDERS,
    merge_external_news,
    format_news_items,
    _normalize_source,
    _detect_lang,
    _normalize_summary,
    _is_open_source,
    _score_news,
    get_default_ranking,
)

__all__ = [
    # utils
    "_UA", "_PROXY_OVERRIDE", "_SOCKS_ACTIVE",
    "_resolved_proxy", "_configure_proxy", "_build_opener",
    "_http_get", "_probe", "_detect_region", "_retry_fetch",
    "_parse_date_arg", "_parse_snapshot_date",
    # translate
    "Translator", "OllamaUnavailable", "ollama_health", "ollama_base_url", "_ollama_translate",
    # news
    "SUMMARY_MAX", "SUMMARY_TARGET", "MUSTREAD_TOP_N", "LEADERBOARD_STALE_DAYS",
    "SOURCE_ALIASES", "SOURCE_AUTHORITY", "CATEGORY_WEIGHT",
    "DEFAULT_SOURCE_AUTHORITY", "DEFAULT_CATEGORY_WEIGHT", "OPEN_SOURCE_PROVIDERS",
    "merge_external_news", "format_news_items",
    "_normalize_source", "_detect_lang", "_normalize_summary",
    "_is_open_source", "_score_news", "get_default_ranking",
]