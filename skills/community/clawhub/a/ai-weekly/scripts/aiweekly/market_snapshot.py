"""市场快照子系统：外置快照文件的读取、兜底常量、过期判定与体检（HON-2）。

从 `market.py` 拆出（P0#4 体量门禁：market.py 曾达971 行 > 800 上限）。

为什么单独成文件：
- 快照是**有状态的**（进程内只解析一次，保证同一份报告里as_of / 过期判定 /
  页脚来源三处口径一致）。把它和「图表构建 / 信号桥接」这种无状态逻辑混在一个
  模块里，会让两者的import 顺序互相牵制。
- 本模块是快照状态的**唯一真身**。`_SNAPSHOT` / `_SNAPSHOT_LOAD_ERROR` 定义在此，
  `market.py` 一律通过 `market_snapshot._SNAPSHOT` **按属性读取**，
  不得用 `from ... import _SNAPSHOT` 做值拷贝——那会让调用方改到副本、
  真身不变，从而读到过期状态（这正是回归测试要守的点）。

快照外置（HON-2）：
- 数值基准不再是躺在代码里的常量，而来自 `assets/market_snapshot.json`
  （含 as_of / retrieved_at / provenance），便于版本化与过期检测。
- **拿不到该文件时回退到本模块内的 `_FALLBACK_*` 常量，并把 `snapshot_stale()`
  置为 True** —— 页脚与各图来源行会显式标注「使用代码内默认值（已过期）」，
  绝不静默显示旧数（静默回落等于把 bug 换了个藏身处）。
- 署名口径见 `assets/market_snapshot.json` 的 `honesty_note`：这些机构是**人工誊录**的
  静态基线，从未被本skill 网络抓取；每周真正实时抓取的是 fetch_ai_news.py 的 14 个 RSS 源。
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

__all__ = [
    "SKILL_DIR", "SNAPSHOT_PATH", "SNAPSHOT_STALE_DAYS",
    "load_snapshot", "snapshot_age_days", "snapshot_stale",
    "snapshot_status_text", "run_snapshot_check",
]

# 技能根目录：assets/market_snapshot.json 与 leaderboard_fetch.py 用同一套定位方式
SKILL_DIR = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = SKILL_DIR / "assets" / "market_snapshot.json"
# 快照超过该天数即视为过期（--check-snapshot 默认阈值，可CLI 覆盖）。
# 90 天 ≈ 一个季度：市场基线是季度级数字，超过一个季度没更新就不该再当"当前口径"用。
SNAPSHOT_STALE_DAYS = 90

# ISO 周粒度的 as_of（形如 2026-W32）
_ISO_WEEK_RE = re.compile(r"(\d{4})-W(\d{1,2})")


# ============ 快照外置（HON-2）============
# 以下 `_FALLBACK_*` 是**快照文件缺失时的兜底常量**，与外置前的取值逐字一致。
# 保留它们不是为了"代码里还得有一份数"，而是为了文件读不到时报告仍能出图——
# 但此时 snapshot_stale() 为 True，页面必须显式标注「已过期」（见 _FALLBACK_NOTE）。
_FALLBACK_MARKET_LABELS = ['2020','2021','2022','2023','2024','2025','2026E','2027F','2028F']
_FALLBACK_MARKET_DATA = [103, 134, 176, 229, 299, 391, 540, 705, 921]
_FALLBACK_FUNDING_LABELS = ['23Q1','23Q2','23Q3','23Q4','24Q1','24Q2','24Q3','24Q4','25Q1','25Q2','25Q3','25Q4','26Q1','26Q2']
_FALLBACK_FUNDING_DATA = [72.4, 72.4, 72.4, 72.4, 79.9, 79.9, 79.9, 79.9, 110.0, 110.0, 110.0, 110.0, 305.0, 205.0]
_FALLBACK_CN_MARKET_LABELS = ['2024','2025','2026E']
_FALLBACK_CN_MARKET_DATA = [9188, 12000, 17000]
_FALLBACK_CN_FUNDING_LABELS = ['2024','2025','2026H1']
_FALLBACK_CN_FUNDING_DATA = [391.51, 656.04, 3076.82]
_FALLBACK_CN_STRUCTURE_LABELS = ['大模型', '具身智能', 'AIGC 应用', '基础层']
_FALLBACK_CN_STRUCTURE_DATA = [1598, 906, 596, 725]
_FALLBACK_CN_CONCENTRATION_LABELS = ['TOP3 大模型', 'TOP4–30 名', '其他赛道']
_FALLBACK_CN_CONCENTRATION_DATA = [930, 770, 1376]

_FALLBACK_MARKET_SOURCE = "Grand View Research 2026（全球 AI 市场规模，CAGR 30.6%；海外机构，静态快照引用）"
_FALLBACK_FUNDING_SOURCE = "Crunchbase / CB Insights（全球 AI 融资，H1 2026 口径；海外机构，静态快照引用）"
_FALLBACK_CN_MARKET_SOURCE = "中国信通院 · 中商产业研究院《2025–2030 中国人工智能产业现状调查》（中国核心产业规模）"
_FALLBACK_CN_FUNDING_SOURCE = "新浪创投Plus 2025 国内一级市场 AI 行业统计 + IT桔子 2026H1（一级市场股权融资，标签「人工智能」）"

# 兜底时追加到 4 个来源串尾部的显式标注——不允许静默回落
_FALLBACK_NOTE = "【已过期：快照文件缺失，使用代码内默认值】"

# 旧 BASE_SOURCES（快照文件缺失时的兜底署名名单）。快照可用时以文件里的 sources 为准。
# used_for 照抄各机构在 DEFAULT_*_SOURCE 里真实承担的引用关系——降级时若一律留空，
# 渲染层会把7 家真正被引用的机构误标成「未引用其数字」，那是降级路径上的新失实。
_FALLBACK_SOURCES = [
    ("Grand View Research", "https://www.grandviewresearch.com", "全球 AI 市场规模图"),
    ("Crunchbase", "https://crunchbase.com", "全球 AI 融资图（H1 2026 口径）"),
    ("CB Insights", "https://www.cbinsights.com", "全球 AI 融资图（2023–2025 年度基准）"),
    ("中国信通院", "https://www.caict.ac.cn", "中国 AI 市场规模图"),
    ("IT桔子", "https://www.itjuzi.com", "中国 AI 融资图 / 赛道结构图 / 头部集中度图"),
    ("新浪创投Plus", "https://venture.sina.com.cn", "中国 AI 融资图（2025 全年）"),
    ("Stanford HAI", "https://hai.stanford.edu", ""),
    ("LMMarketCap", "https://lmmarketcap.com", ""),
]


def _parse_snapshot_date(raw) -> date | None:
    """快照的 as_of / retrieved_at -> date；解析不了返回 None（不当场抛）。

    接受 ``YYYY-MM-DD`` 与 ``YYYY-Www``（ISO 周，与 as_of 实际取值同形）。
    周粒度按该周的**周一**计，用于算过期天数。
    """
    s = str(raw or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        pass
    # ISO 周形如 2026-W32：不能用 strptime —— %G 强制要求同时给星期指令（%u/%w/%a/%A），
    # 而快照里的 as_of 不带星期，故走 fromisocalendar（year, week, 1=周一）。
    m = _ISO_WEEK_RE.fullmatch(s)
    if m:
        try:
            return date.fromisocalendar(int(m.group(1)), int(m.group(2)), 1)
        except ValueError:
            return None  # 非法周号（如 W53 而该年只有 52 周）
    return None


# 模块级快照状态：进程内只解析一次（多次读同一文件没有收益，且要保证
# 「同一份报告里 as_of / 过期判定 / 页脚来源」三处口径一致，不会各读各的）。
_SNAPSHOT: dict = {}
_SNAPSHOT_LOAD_ERROR: str = ""


def load_snapshot(path=None) -> dict:
    """读取 ``assets/market_snapshot.json``；读不到或结构不对返回 ``{}``。

    best-effort：不在此抛异常——快照缺失不该让整份报告打挂，
    但会把原因记进 ``_SNAPSHOT_LOAD_ERROR`` 并让 ``snapshot_stale()`` 为真，
    使页面显式标注「已过期」。
    """
    global _SNAPSHOT, _SNAPSHOT_LOAD_ERROR
    p = Path(path) if path else SNAPSHOT_PATH
    try:
        raw = p.read_text(encoding="utf-8")
    except OSError as e:
        #只带文件名不带绝对路径：这段文案会渲染进发布的 HTML，
        # 带上开发机的 C:\Users\... 会把本地目录结构泄进公开产物。
        _SNAPSHOT, _SNAPSHOT_LOAD_ERROR = {}, f"快照文件不可读（{p.name}：{e.strerror or type(e).__name__}）"
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        _SNAPSHOT, _SNAPSHOT_LOAD_ERROR = {}, f"快照文件不是合法 JSON（{p.name}：{e}）"
        return {}
    if not isinstance(data, dict) or not isinstance(data.get("series"), list):
        _SNAPSHOT, _SNAPSHOT_LOAD_ERROR = {}, "快照文件结构异常：缺 series 数组"
        return {}
    _SNAPSHOT, _SNAPSHOT_LOAD_ERROR = data, ""
    return data


def _series(key: str) -> dict:
    """按key 取快照里的单条序列（含 labels / values / provenance）。"""
    for item in _SNAPSHOT.get("series", []):
        if isinstance(item, dict) and item.get("key") == key:
            return item
    return {}


def _labels_values(key: str, fb_labels, fb_values):
    """取序列的 (labels, values)，任何缺项都回退兜底常量（由 snapshot_stale 负责标注）。"""
    s = _series(key)
    labels, values = s.get("labels"), s.get("values")
    if not (isinstance(labels, list) and labels
            and isinstance(values, list) and len(values) == len(labels)):
        return fb_labels, fb_values
    return list(labels), list(values)


def snapshot_age_days(today: date | None = None) -> int | None:
    """快照距今多少天；无法判定返回 None（调用方须据此报警，不得当作"新鲜"）。"""
    ref = today or date.today()
    d = _parse_snapshot_date(_SNAPSHOT.get("retrieved_at")) or _parse_snapshot_date(
        _SNAPSHOT.get("as_of"))
    if d is None:
        return None
    return (ref - d).days


def snapshot_stale(max_age_days: int = SNAPSHOT_STALE_DAYS, today: date | None = None) -> bool:
    """快照是否不可用于当"当前口径"用。

    三种情况都算 stale（宁可报警也不静默用旧数）：
      * 文件读不到 / 结构不对；
      * retrieved_at 与 as_of 都解析不出日期（无法证明新鲜）；
      * 距今超过 max_age_days。
    """
    if not _SNAPSHOT:
        return True
    age = snapshot_age_days(today)
    if age is None:
        return True
    return age > max_age_days


def snapshot_status_text(max_age_days: int = SNAPSHOT_STALE_DAYS, today: date | None = None) -> str:
    """页脚 / 各图来源行用的快照状态标注；新鲜时返回空串（不制造噪音）。

    过期时给出可执行信息：快照截止日 + 距今天数 + 缺文件的具体原因。
    """
    if not snapshot_stale(max_age_days, today):
        return ""
    if not _SNAPSHOT:
        return _FALLBACK_NOTE + f"（{_SNAPSHOT_LOAD_ERROR or '原因未知'}）"
    age = snapshot_age_days(today)
    as_of = _SNAPSHOT.get("as_of") or "未知"
    if age is None:
        return f"【已过期：快照 {as_of} 的日期无法解析，无法证明其新鲜度】"
    return f"【已过期：快照截止 {as_of}，距今 {age} 天 > {max_age_days} 天】"


def run_snapshot_check(max_age_days: int = SNAPSHOT_STALE_DAYS,
                       today: date | None = None) -> int:
    """``--check-snapshot`` 入口：打印快照体检结论，过期 / 缺失返回非 0。

    与 ``--health-check`` 同为"只检查不生成"的独立子命令，故沿用其返回码风格
    （调用方 ``sys.exit(rc)``）。
    """
    print("📊 市场快照检查（assets/market_snapshot.json）", flush=True)
    if not _SNAPSHOT:
        print(f"  ❌ 快照不可用：{_SNAPSHOT_LOAD_ERROR or '文件不存在'}", flush=True)
        print(f"     ↳ 生成时会回退代码内默认值，页面将标注「{_FALLBACK_NOTE}」。",
              flush=True)
        print("     ↳ 修法：确认 assets/market_snapshot.json 在库内（注意 data/ 被 .gitignore 忽略，"
              "快照必须放assets/）。", flush=True)
        return 1
    print(f"  ✅ 已载入快照：as_of={_SNAPSHOT.get('as_of') or '未标注'} · "
          f"retrieved_at={_SNAPSHOT.get('retrieved_at') or '未标注'}", flush=True)
    print(f"     序列 {len(_SNAPSHOT.get('series', []))} 条 · "
          f"署名机构 {len(_SNAPSHOT.get('sources', []))} 家 · "
          f"基准机构 {(_SNAPSHOT.get('source') or {}).get('name') or '未标注'}", flush=True)
    age = snapshot_age_days(today)
    if age is None:
        print("  ❌ 无法解析 retrieved_at / as_of 为日期，不能证明快照新鲜度", flush=True)
        print("     ↳ 请在快照文件里补retrieved_at（YYYY-MM-DD）。", flush=True)
        return 1
    if age > max_age_days:
        print(f"  ❌ 快照已过期：距今 {age} 天 > 阈值 {max_age_days} 天"
              f"（as_of={_SNAPSHOT.get('as_of')}）", flush=True)
        print("     ↳ 这批市场数字是人工誊录的静态基线，不会自动更新；"
              "请复核来源后更新快照的 retrieved_at 与 series。", flush=True)
        return 1
    print(f"  ✅ 新鲜度通过：距今 {age} 天 ≤ 阈值 {max_age_days} 天", flush=True)
    print("     ↳ 注意：新鲜 ≠ 实时。这些机构从未被本skill 抓取，"
          "「新鲜」只说明誊录时间不算久。", flush=True)
    return 0