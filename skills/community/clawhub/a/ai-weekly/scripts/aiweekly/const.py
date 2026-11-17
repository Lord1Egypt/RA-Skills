"""aiweekly.const — 硬约束常量集中声明（P2-1：边界条件集中声明）。

所有影响输出大小、性能、质量的限制都定义在此处，便于维护和调整。

变更时同步更新 SKILL.md 第二节「硬约束」小节和 README「已知限制」。
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 新闻抓取限制
# ---------------------------------------------------------------------------
NEWS_MAX_ITEMS: int = 100         # 单次抓取上限，超过截取前 N 条
NEWS_MIN_SCORE: float = 0.0       # 新闻最低重要度评分（低于此值被过滤）
NEWS_DATE_CUTOFF_DAYS: int = 7    # 超过 N 天前的新闻标注 [n天前]
NEWS_SUMMARY_MAX_CHARS: int = 120  # 摘要最大字符数（触发归一化）

# ---------------------------------------------------------------------------
# 排行榜限制
# ---------------------------------------------------------------------------
LEADERBOARD_TOP_N: int = 50       # 每榜最多显示条数（超过截取 top N）
LEADERBOARD_MAX_MODELS: int = 50  # 单榜最大模型数（防止 HTML 过大）
LEADERBOARD_STALE_DAYS: int = 3   # 排行榜快照距报告日超过此天数即视为「非本周抓取」并告警（周报语义：>3 天即非本周）。P2-5 单一来源：模板端经 meta.snapshot_stale_threshold 同源引用。

# ---------------------------------------------------------------------------
# 图表数据限制
# ---------------------------------------------------------------------------
CHART_MAX_DATA_POINTS: int = 20   # 单条趋势线最大数据点数（超出处以平均值）
MARKET_DATA_SOURCE_REQUIRED: bool = True  # 市场数据是否强制要求来源（True=必须搜索）

# ---------------------------------------------------------------------------
# HTML 输出限制
# ---------------------------------------------------------------------------
HTML_MAX_SIZE_BYTES: int = 5 * 1024 * 1024  # 建议 ≤5MB（超过会自动压缩 Chart.js 数据）
CHART_JS_COMPRESS_THRESHOLD: int = 3 * 1024 * 1024  # 超过此大小触发压缩

# ---------------------------------------------------------------------------
# 内容生成限制
# ---------------------------------------------------------------------------
SUMMARY_TARGET_CHARS: int = 600   # 摘要目标长度（避免截断）
MUSTREAD_TOP_N: int = 8           # 评分最高的前 N 条标记为必读
SELECTION_NOTES_MAX_LENGTH: int = 200  # 选型结论最大字符数

# ---------------------------------------------------------------------------
# 部署限制
# ---------------------------------------------------------------------------
DEPLOY_TIMEOUT_SECONDS: int = 120  # 单次部署超时（秒）
DEPLOY_MAX_RETRIES: int = 2       # 部署失败重试次数

# ---------------------------------------------------------------------------
# 网络限制
# ---------------------------------------------------------------------------
HTTP_TIMEOUT_SECONDS: int = 30    # 单次 HTTP 请求超时
HTTP_MAX_RETRIES: int = 3         # 失败重试次数
HTTP_RETRY_DELAY_SECONDS: float = 1.0  # 重试间隔

# ---------------------------------------------------------------------------
# 译文源（远程 / 离线）—— P0(v3.4.7)：默认开启，无本地 Ollama 也有中文
# ---------------------------------------------------------------------------
# 远程译文源（GitHub Pages 上每周随周报发布的累计译文，175+ 条）。
# 默认开启：没有本地 Ollama 的用户也能拿到中文，不再「强依赖本地模型」。
DEFAULT_TRANSLATIONS_URL: str = (
    "https://elisabeth15501.github.io/ai-weekly/translations.json"
)
# 离线译文包（随技能附带，完全断网时改用 --translations-url 指向本文件）。
# 由发布流程从 gh-pages 同步，路径相对技能根目录。
OFFLINE_TRANSLATIONS_FILE: str = "translations_offline.json"

# ---------------------------------------------------------------------------
# 翻译链路默认值（唯一来源）
# ---------------------------------------------------------------------------
# 原先这 5 个值在 generate_site.py 的 add_argument 与 render.py 的形参默认值里
# 各写一遍，改一处必漏另一处；集中到此处后两端都引用常量（见 clean_code_audit A5/M1）。
TRANSLATE_MODEL_DEFAULT: str = "qwen2.5:7b"   # 非推理模型更快
TRANSLATE_WORKERS_DEFAULT: int = 3            # CPU 本地推理下过高会互相抢资源导致超时丢条
TRANSLATE_TIMEOUT_DEFAULT: int = 45           # 单条翻译超时（秒）
TRANSLATE_RETRIES_DEFAULT: int = 2            # 失败重试次数（总尝试 = retries + 1）
TRANSLATE_NUM_PREDICT_DEFAULT: int = 600      # 译文 token 上限（摘要偏长避免截断）

# ---------------------------------------------------------------------------
# 关键词搜索源默认值（唯一来源）
# ---------------------------------------------------------------------------
# 关键词点击跳转的可切换搜索源 {name: url}；CLI 默认值与 render 层兜底共用同一串。
DEFAULT_SEARCH_SOURCES_JSON: str = (
    '{"baidu":"https://www.baidu.com/s?wd=",'
    '"google":"https://www.google.com/search?q=",'
    '"arxiv":"https://arxiv.org/search/?query="}'
)

__all__ = [
    "NEWS_MAX_ITEMS", "NEWS_MIN_SCORE", "NEWS_DATE_CUTOFF_DAYS", "NEWS_SUMMARY_MAX_CHARS",
    "LEADERBOARD_TOP_N", "LEADERBOARD_MAX_MODELS", "LEADERBOARD_STALE_DAYS",
    "CHART_MAX_DATA_POINTS", "MARKET_DATA_SOURCE_REQUIRED",
    "HTML_MAX_SIZE_BYTES", "CHART_JS_COMPRESS_THRESHOLD",
    "SUMMARY_TARGET_CHARS", "MUSTREAD_TOP_N", "SELECTION_NOTES_MAX_LENGTH",
    "DEPLOY_TIMEOUT_SECONDS", "DEPLOY_MAX_RETRIES",
    "HTTP_TIMEOUT_SECONDS", "HTTP_MAX_RETRIES", "HTTP_RETRY_DELAY_SECONDS",
    "DEFAULT_TRANSLATIONS_URL", "OFFLINE_TRANSLATIONS_FILE",
    "TRANSLATE_MODEL_DEFAULT", "TRANSLATE_WORKERS_DEFAULT", "TRANSLATE_TIMEOUT_DEFAULT",
    "TRANSLATE_RETRIES_DEFAULT", "TRANSLATE_NUM_PREDICT_DEFAULT",
    "DEFAULT_SEARCH_SOURCES_JSON",
]
