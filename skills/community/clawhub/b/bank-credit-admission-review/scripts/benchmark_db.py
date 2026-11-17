#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业基准本地数据库 —— 采集入库、分位数计算、企业比对。

用途：为授信准入审查提供"同行业上市公司平均水平"作为尺度，
      解决四维分析中"这家企业资产负债率 78% 到底算不算高"的问题。

架构说明（重要）：
    财汇MCP 只能由 Agent 调用，本脚本不联网、不直连 MCP。
    标准流程为：Agent 调 MCP 取数 → 保存原始返回 JSON → 本脚本 ingest 入库。
    脚本可直接解析 MCP 原始返回结构（headInfo + data 二维数组），
    无需 Agent 手工转换字段，避免转换环节引入错误。

子命令：
    init      建库（幂等）
    ingest    导入数据（支持 MCP 原始返回格式）
    compute   计算行业分位数基准
    query     查询行业基准
    compare   单家企业 vs 行业基准，输出分位定位
    status    库存概览

依赖：Python 3.8+ 标准库，无第三方依赖。
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime

DEFAULT_DB = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "industry_benchmark.db")

# ---------------------------------------------------------------------------
# 指标方向性：决定分位数如何解读
#   lower_better  —— 数值越低越稳健（杠杆类）
#   higher_better —— 数值越高越稳健（盈利、流动性、规模）
#   neutral       —— 仅作规模参考，不判优劣
# ---------------------------------------------------------------------------
INDICATOR_DIRECTION = {
    "资产负债率": "lower_better",
    "有息负债率": "lower_better",
    "净负债率": "lower_better",
    "产权比率": "lower_better",
    "流动比率": "higher_better",
    "速动比率": "higher_better",
    "利息保障倍数": "higher_better",
    "销售毛利率": "higher_better",
    "销售净利率": "higher_better",
    "净资产收益率": "higher_better",
    "总资产报酬率": "higher_better",
    "归母净利润": "higher_better",
    "净利润": "higher_better",
    "营业总收入": "higher_better",
    "营业收入": "higher_better",
    "经营活动现金流量净额": "higher_better",
    "经营现金流": "higher_better",
    "总资产": "neutral",
    "资产总计": "neutral",
    "净资产": "neutral",
    "所有者权益合计": "neutral",
}

# 比率型指标的极端值剔除阈值（单位与指标一致）。
# 当净资产近零时，ROE/ROA 会数学爆炸（如 705%、-445%），并非真实经营水平，
# 须从分位数分布中剔除，避免污染行业中枢；其困境已由资产负债率/净利润等维度捕获。
# 阈值取 ±100%（ROE/ROA 超过该区间几乎必然源于分母近零），净利率放宽至 ±200%。
RATIO_OUTLIER_CAP = {
    "净资产收益率": 100.0,
    "总资产报酬率": 100.0,
    "销售净利率": 200.0,
}

# 行业层级字段名
LEVEL_COLUMNS = {
    "l1": "industry_l1",
    "l2": "industry_l2",
    "l3": "industry_l3",
    "l4": "industry_l4",
}
LEVEL_LABELS = {
    "l1": "国标门类",
    "l2": "国标大类",
    "l3": "国标中类",
    "l4": "国标小类",
}

# 计算基准所需的最小样本量。低于此值仍会计算，但标记为参考性不足。
MIN_SAMPLE = 5
MIN_SAMPLE_RELIABLE = 15


# ===========================================================================
# 建库
# ===========================================================================
SCHEMA = """
CREATE TABLE IF NOT EXISTS companies (
    uscc            TEXT PRIMARY KEY,
    company_name    TEXT NOT NULL,
    industry_l1     TEXT,
    industry_l2     TEXT,
    industry_l3     TEXT,
    industry_l4     TEXT,
    is_listed       TEXT,
    source          TEXT,
    updated_at      TEXT
);

CREATE INDEX IF NOT EXISTS idx_comp_l2 ON companies(industry_l2);
CREATE INDEX IF NOT EXISTS idx_comp_l3 ON companies(industry_l3);
CREATE INDEX IF NOT EXISTS idx_comp_name ON companies(company_name);

CREATE TABLE IF NOT EXISTS financials (
    uscc            TEXT NOT NULL,
    company_name    TEXT NOT NULL,
    year            INTEGER NOT NULL,
    period          TEXT NOT NULL DEFAULT '年报',
    indicator       TEXT NOT NULL,
    value           REAL,
    unit            TEXT,
    source          TEXT,
    fetched_at      TEXT,
    PRIMARY KEY (uscc, year, period, indicator)
);

CREATE INDEX IF NOT EXISTS idx_fin_ind ON financials(indicator, year);
CREATE INDEX IF NOT EXISTS idx_fin_uscc ON financials(uscc);

CREATE TABLE IF NOT EXISTS benchmarks (
    industry_level  TEXT NOT NULL,
    industry_name   TEXT NOT NULL,
    year            INTEGER NOT NULL,
    period          TEXT NOT NULL DEFAULT '年报',
    indicator       TEXT NOT NULL,
    direction       TEXT,
    n               INTEGER,
    p10             REAL,
    p25             REAL,
    p50             REAL,
    p75             REAL,
    p90             REAL,
    mean            REAL,
    min_v           REAL,
    max_v           REAL,
    neg_count       INTEGER,
    unit            TEXT,
    reliability     TEXT,
    computed_at     TEXT,
    PRIMARY KEY (industry_level, industry_name, year, period, indicator)
);

CREATE TABLE IF NOT EXISTS ingest_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ts              TEXT,
    kind            TEXT,
    rows_in         INTEGER,
    rows_written    INTEGER,
    note            TEXT
);
"""


def connect(db_path):
    d = os.path.dirname(db_path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def cmd_init(args):
    conn = connect(args.db)
    conn.executescript(SCHEMA)
    ensure_extra_columns(conn)
    conn.commit()
    conn.close()
    print("数据库已就绪：%s" % args.db)
    return 0


# ===========================================================================
# 数据导入
# ===========================================================================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 指标列名形如「资产负债率-2025年年报」「归母净利润-2024年年报」
PERIOD_RE = re.compile(r"^(?P<ind>.+?)-(?P<year>\d{4})年(?P<period>年报|中报|一季报|三季报|Q\d)$")


def parse_indicator_header(name):
    """从 MCP headInfo 的 name 字段拆出「指标名 / 年度 / 报告期」。"""
    m = PERIOD_RE.match(name or "")
    if not m:
        return None
    return m.group("ind"), int(m.group("year")), m.group("period")


def extract_records(payload):
    """兼容多层包装，定位到 records 节点。"""
    node = payload
    if isinstance(node, dict) and "data" in node and isinstance(node["data"], dict):
        node = node["data"]
    if isinstance(node, dict) and "records" in node:
        node = node["records"]
    if not isinstance(node, dict) or "data" not in node or "headInfo" not in node:
        raise ValueError("未能定位 MCP records 结构（需含 data 与 headInfo）")
    return node["data"], node["headInfo"]


def ingest_companies(conn, payload, source, default_year=None):
    """导入行业公司清单（filter_companies_by_basic_info 返回）。"""
    rows, head = extract_records(payload)
    fields = [h.get("field") for h in head]

    def idx(*names):
        for n in names:
            if n in fields:
                return fields.index(n)
        return None

    i_name = idx("company_name")
    i_uscc = idx("unified_social_credit_code")
    i_l1 = idx("national_standard_industry_category")
    i_l2 = idx("national_standard_industry_major_category")
    i_l3 = idx("national_standard_industry_medium_category")
    i_l4 = idx("national_standard_industry_minor_category")
    i_listed = idx("listingStatus")

    if i_name is None or i_uscc is None:
        raise ValueError("公司清单缺少 company_name 或 unified_social_credit_code 列")

    written = 0
    for r in rows:
        def g(i):
            return r[i] if i is not None and i < len(r) else None
        conn.execute("""
            INSERT INTO companies
                (uscc, company_name, industry_l1, industry_l2, industry_l3,
                 industry_l4, is_listed, source, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(uscc) DO UPDATE SET
                company_name=excluded.company_name,
                industry_l1=COALESCE(excluded.industry_l1, companies.industry_l1),
                industry_l2=COALESCE(excluded.industry_l2, companies.industry_l2),
                industry_l3=COALESCE(excluded.industry_l3, companies.industry_l3),
                industry_l4=COALESCE(excluded.industry_l4, companies.industry_l4),
                is_listed=COALESCE(excluded.is_listed, companies.is_listed),
                source=excluded.source,
                updated_at=excluded.updated_at
        """, (g(i_uscc), g(i_name), g(i_l1), g(i_l2), g(i_l3), g(i_l4),
              g(i_listed), source, now()))
        written += 1
    return len(rows), written


def ingest_financials(conn, payload, source, industry=None, level="l2",
                      is_listed="已上市"):
    """导入财务指标（get_company_financial_metrics 返回）。

    列名内嵌年度与报告期，逐列解析后拆成长表记录。

    若传入 industry，则对尚未建档的公司自动补建公司记录并打上行业标签——
    这样采集时无需单独导入一次公司清单，一步到位。
    """
    rows, head = extract_records(payload)
    fields = [h.get("field") for h in head]
    names = [h.get("name") for h in head]
    units = [h.get("unit") for h in head]

    i_name = fields.index("company_name") if "company_name" in fields else None
    i_uscc = (fields.index("unified_social_credit_code")
              if "unified_social_credit_code" in fields else None)
    if i_name is None:
        raise ValueError("财务数据缺少 company_name 列")

    # 找出所有可解析的指标列
    metric_cols = []
    for i, nm in enumerate(names):
        parsed = parse_indicator_header(nm)
        if parsed:
            metric_cols.append((i, parsed[0], parsed[1], parsed[2], units[i]))

    if not metric_cols:
        raise ValueError("未识别到任何「指标-YYYY年报告期」格式的指标列")

    written = 0
    skipped_no_uscc = 0
    auto_created = 0
    ind_col = LEVEL_COLUMNS.get(level, "industry_l2")
    for r in rows:
        cname = r[i_name] if i_name < len(r) else None
        uscc = r[i_uscc] if (i_uscc is not None and i_uscc < len(r)) else None
        if not uscc:
            # 无统一社会信用代码时回退用公司名查库
            cur = conn.execute(
                "SELECT uscc FROM companies WHERE company_name=?", (cname,))
            hit = cur.fetchone()
            if hit:
                uscc = hit["uscc"]
            else:
                skipped_no_uscc += 1
                continue

        # 自动补建公司档案，避免必须先单独导入公司清单
        if industry:
            exists = conn.execute(
                "SELECT 1 FROM companies WHERE uscc=?", (uscc,)).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO companies (uscc, company_name, %s, is_listed, "
                    "source, updated_at) VALUES (?,?,?,?,?,?)" % ind_col,
                    (uscc, cname, industry, is_listed,
                     source + "·自动建档", now()))
                auto_created += 1
            else:
                conn.execute(
                    "UPDATE companies SET %s = COALESCE(%s, ?) WHERE uscc = ?"
                    % (ind_col, ind_col), (industry, uscc))

        for (ci, ind, yr, period, unit) in metric_cols:
            if ci >= len(r):
                continue
            val = r[ci]
            if val is None or val == "":
                continue
            try:
                val = float(val)
            except (TypeError, ValueError):
                continue
            conn.execute("""
                INSERT INTO financials
                    (uscc, company_name, year, period, indicator, value,
                     unit, source, fetched_at)
                VALUES (?,?,?,?,?,?,?,?,?)
                ON CONFLICT(uscc, year, period, indicator) DO UPDATE SET
                    value=excluded.value,
                    company_name=excluded.company_name,
                    unit=excluded.unit,
                    source=excluded.source,
                    fetched_at=excluded.fetched_at
            """, (uscc, cname, yr, period, ind, val, unit, source, now()))
            written += 1
    if skipped_no_uscc:
        print("提示：%d 行因无统一社会信用代码且公司名未入库而跳过，"
              "建议先导入该行业公司清单。" % skipped_no_uscc, file=sys.stderr)
    if auto_created:
        print("已自动补建 %d 家公司档案，行业标签：%s（%s）"
              % (auto_created, industry, LEVEL_LABELS.get(level, level)))
    return len(rows), written


def cmd_ingest(args):
    conn = connect(args.db)
    conn.executescript(SCHEMA)

    if args.input == "-":
        payload = json.load(sys.stdin)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            payload = json.load(f)

    source = args.source or "MCP·预警通"

    kind = args.kind
    if kind == "auto":
        _, head = extract_records(payload)
        names = [h.get("name") for h in head]
        kind = "financials" if any(parse_indicator_header(n) for n in names) \
            else "companies"
        print("自动识别数据类型：%s" % kind)

    if kind == "companies":
        rin, rw = ingest_companies(conn, payload, source)
        print("公司清单导入完成：读取 %d 行，写入 %d 家。" % (rin, rw))
    else:
        rin, rw = ingest_financials(conn, payload, source,
                                    industry=args.industry, level=args.level)
        print("财务指标导入完成：读取 %d 行，写入 %d 条指标记录。" % (rin, rw))

    conn.execute("INSERT INTO ingest_log (ts, kind, rows_in, rows_written, note) "
                 "VALUES (?,?,?,?,?)", (now(), kind, rin, rw, args.note or ""))
    conn.commit()
    conn.close()
    return 0


# ===========================================================================
# 分位数计算
# ===========================================================================
def percentile(sorted_vals, q):
    """线性插值分位数，q 取 0~100。"""
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    pos = (len(sorted_vals) - 1) * q / 100.0
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def percentile_rank(sorted_vals, x):
    """返回 x 在样本中的百分位排名（0~100）。"""
    if not sorted_vals:
        return None
    below = sum(1 for v in sorted_vals if v < x)
    equal = sum(1 for v in sorted_vals if v == x)
    return (below + 0.5 * equal) / len(sorted_vals) * 100.0


def outlier_flag(indicator, v):
    """比率型指标极端值判定（分母近零导致比率失真）。"""
    cap = RATIO_OUTLIER_CAP.get(indicator)
    if cap is None or v is None:
        return False
    return abs(v) > cap


def clean_values(indicator, vals):
    """剔除比率型指标失真极端值，返回 (clean_vals, removed_vals)。

    兜底原则：比率型指标分子或分母近零时数值会爆炸/坍塌，已非经营水平可比口径，
    剔除后行业中枢更稳健；被剔除主体的困境由其他维度（资产负债率、净利润）体现。
    """
    removed = [v for v in vals if outlier_flag(indicator, v)]
    clean = [v for v in vals if not outlier_flag(indicator, v)]
    return clean, removed


def ensure_extra_columns(conn):
    """为 benchmarks 表补充后续新增列（幂等，避免重复建表时报错）。"""
    for col, ctype in (("outlier_count", "INTEGER"), ("outlier_note", "TEXT")):
        try:
            conn.execute("ALTER TABLE benchmarks ADD COLUMN %s %s" % (col, ctype))
        except sqlite3.OperationalError:
            pass


def cmd_compute(args):
    conn = connect(args.db)
    conn.executescript(SCHEMA)
    ensure_extra_columns(conn)
    col = LEVEL_COLUMNS[args.level]

    where = ["c.%s IS NOT NULL" % col, "f.value IS NOT NULL"]
    params = []
    if args.industry:
        where.append("c.%s = ?" % col)
        params.append(args.industry)
    if args.year:
        where.append("f.year = ?")
        params.append(args.year)
    if args.listed_only:
        where.append("c.is_listed = '已上市'")

    sql = """
        SELECT c.%s AS ind_name, f.year, f.period, f.indicator, f.value, f.unit
        FROM financials f
        JOIN companies c ON c.uscc = f.uscc
        WHERE %s
    """ % (col, " AND ".join(where))

    groups = {}
    for row in conn.execute(sql, params):
        key = (row["ind_name"], row["year"], row["period"], row["indicator"])
        groups.setdefault(key, {"vals": [], "unit": row["unit"]})
        groups[key]["vals"].append(row["value"])

    written = 0
    for (key_ind, year, period, indicator), pack in groups.items():
        raw = sorted(pack["vals"])
        clean, removed = clean_values(indicator, raw)
        n = len(clean)
        if n < args.min_sample:
            continue
        direction = INDICATOR_DIRECTION.get(indicator, "neutral")
        reliability = ("充足" if n >= MIN_SAMPLE_RELIABLE
                       else "偏少-仅供参考")
        oc = len(removed)
        cap = RATIO_OUTLIER_CAP.get(indicator)
        onote = ("剔除 %d 个失真极端值（分母近零，超出±%g%%）"
                 % (oc, cap)) if (oc and cap) else None
        conn.execute("""
            INSERT INTO benchmarks
                (industry_level, industry_name, year, period, indicator,
                 direction, n, p10, p25, p50, p75, p90, mean, min_v, max_v,
                 neg_count, unit, reliability, computed_at,
                 outlier_count, outlier_note)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(industry_level, industry_name, year, period, indicator)
            DO UPDATE SET
                direction=excluded.direction, n=excluded.n,
                p10=excluded.p10, p25=excluded.p25, p50=excluded.p50,
                p75=excluded.p75, p90=excluded.p90, mean=excluded.mean,
                min_v=excluded.min_v, max_v=excluded.max_v,
                neg_count=excluded.neg_count, unit=excluded.unit,
                reliability=excluded.reliability, computed_at=excluded.computed_at,
                outlier_count=excluded.outlier_count,
                outlier_note=excluded.outlier_note
        """, (args.level, key_ind, year, period, indicator, direction, n,
              percentile(clean, 10), percentile(clean, 25), percentile(clean, 50),
              percentile(clean, 75), percentile(clean, 90),
              sum(clean) / n, clean[0], clean[-1],
              sum(1 for v in clean if v < 0), pack["unit"], reliability, now(),
              oc, onote))
        written += 1

    conn.commit()
    conn.close()
    print("基准计算完成：层级 %s（%s），生成/更新 %d 组基准。"
          % (args.level, LEVEL_LABELS[args.level], written))
    return 0


# ===========================================================================
# 查询与比对
# ===========================================================================
def fmt(v, unit=None, nd=2):
    """按单位智能格式化。万元金额超过 1 亿自动折算为亿元，避免长串数字难读。"""
    if v is None:
        return "—"
    if unit == "万元" and abs(v) >= 10000:
        return "%.2f亿" % (v / 10000.0)
    if unit == "万元":
        return "%.0f万" % v
    s = "%.*f" % (nd, v)
    if unit == "%":
        s += "%"
    elif unit:
        s += unit
    return s


def fmt_deviation(val, median, unit=None):
    """偏离度表述。

    中位数为负或接近零时，百分比偏离会产生误导——例如行业中位亏损 26 亿、
    本企业亏损 885 亿，算出「-3217%」看起来像方向相反。此类情形改用绝对差额。
    """
    if median is None:
        return "—"
    diff = float(val) - median
    if median > 0 and abs(median) > 1e-9:
        return "%+.1f%%" % (diff / median * 100.0)
    # 中位数为负或为零：用绝对差额，并明确方向
    return "%s%s" % ("+" if diff >= 0 else "-", fmt(abs(diff), unit))


def cmd_query(args):
    conn = connect(args.db)
    conn.executescript(SCHEMA)
    ensure_extra_columns(conn)
    where = ["industry_level = ?"]
    params = [args.level]
    if args.industry:
        where.append("industry_name = ?")
        params.append(args.industry)
    if args.year:
        where.append("year = ?")
        params.append(args.year)
    if args.indicator:
        where.append("indicator = ?")
        params.append(args.indicator)

    rows = list(conn.execute(
        "SELECT * FROM benchmarks WHERE %s ORDER BY industry_name, year DESC, "
        "indicator" % " AND ".join(where), params))
    conn.close()

    if not rows:
        print("未查到匹配的行业基准。请确认已 ingest 数据并执行 compute。")
        return 1

    if args.format == "json":
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=2))
        return 0

    cur_key = None
    for r in rows:
        key = (r["industry_name"], r["year"])
        if key != cur_key:
            cur_key = key
            print("\n## %s ｜ %s年报 ｜ 口径：%s"
                  % (r["industry_name"], r["year"], LEVEL_LABELS[r["industry_level"]]))
            print("\n| 指标 | 样本数 | P10 | P25 | 中位数 | P75 | P90 | 均值 | 为负家数 | 极值剔除 | 可靠性 |")
            print("|---|---|---|---|---|---|---|---|---|---|---|")
        u = r["unit"]
        print("| %s | %d | %s | %s | **%s** | %s | %s | %s | %d | %s | %s |" % (
            r["indicator"], r["n"], fmt(r["p10"], u), fmt(r["p25"], u),
            fmt(r["p50"], u), fmt(r["p75"], u), fmt(r["p90"], u),
            fmt(r["mean"], u), r["neg_count"] or 0,
            (str(r["outlier_count"]) if r["outlier_count"] else "—"),
            r["reliability"]))
    print("\n> 「为负家数」用于识别行业整体亏损或资不抵债的程度，"
          "行业下行期须结合该列判断基准本身是否已被劣化。")
    onotes = sorted(set(r["outlier_note"] for r in rows if r["outlier_note"]))
    if onotes:
        print("> **极端值处理**：" + "；".join(onotes)
              + "。该等主体因净资产近零导致比率失真，已剔除出分位数分布，"
                "其困境由资产负债率/净利润等维度体现。")
    print("> 数据来源：财汇MCP（企业预警通）同行业上市公司年报数据。")
    return 0


def interpret(direction, rank):
    """把百分位排名翻译成审查语言。"""
    if rank is None:
        return "—", "—"
    if direction == "lower_better":
        if rank >= 90:
            return "显著劣于同业", "高风险"
        if rank >= 75:
            return "劣于同业", "关注"
        if rank >= 50:
            return "略高于行业中位", "一般"
        if rank >= 25:
            return "优于行业中位", "良好"
        return "显著优于同业", "良好"
    if direction == "higher_better":
        if rank <= 10:
            return "显著劣于同业", "高风险"
        if rank <= 25:
            return "劣于同业", "关注"
        if rank <= 50:
            return "略低于行业中位", "一般"
        if rank <= 75:
            return "优于行业中位", "良好"
        return "显著优于同业", "良好"
    return "规模参考项", "—"


# 章节中文序号（模块级，供 compare 与定性分支共用同一计数器）
CN_NUM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

# ===========================================================================
# 规模分层（门当户对 · 用户指令 2026-08-19）
# 按最近年报营收（万元）分层：大型 ≥100亿 / 中型 20–100亿 / 中小型 5–20亿 / 小型微 <5亿
# ===========================================================================
SCALE_TIERS = (
    (1000000, "大型（≥100 亿）", float("inf")),
    (200000, "中型（20–100 亿）", 1000000),
    (50000, "中小型（5–20 亿）", 200000),
    (0, "小型微（<5 亿）", 50000),
)


def scale_bounds(revenue_wan):
    """返回 (层级标签, 区间下限万, 区间上限万)。营收缺失时返回 (None, None, None)。"""
    if revenue_wan is None:
        return None, None, None
    for lo, label, hi in SCALE_TIERS:
        if revenue_wan >= lo:
            return label, lo, hi
    return "小型微（<5 亿）", 0, 50000


def peer_usccs_by_scale(conn, col, industry, year, lo, hi):
    """取同行业同年中营收处于 [lo, hi) 万元区间的公司 uscc 集合（同规模层同业）。"""
    return set(r[0] for r in conn.execute(
        "SELECT c.uscc FROM companies c "
        "JOIN financials f ON f.uscc = c.uscc "
        "WHERE c.%s=? AND f.year=? AND f.indicator='营业总收入' "
        "AND f.value IS NOT NULL AND f.value >= ? AND f.value < ?"
        % col, (industry, year, lo, hi)))


def _heading(lines, sec, title):
    """按同一计数器追加「N、标题」章节，保证定性分支与定量分支编号连续。"""
    sec[0] += 1
    idx = CN_NUM[sec[0] - 1] if sec[0] <= len(CN_NUM) else str(sec[0])
    lines.append("## %s、%s" % (idx, title))
    lines.append("")


def emit_industry_divergence(lines, sec, declared, benchmark_used, actual_business):
    """行业名实背离标注。declared=国标行业；benchmark_used=本次比对实际所用行业基准；
    actual_business=经核查的实际主业。数值路径与零数据路径共用。"""
    _heading(lines, sec, "行业名实校验（⚠ 国标行业与实际主业背离）")
    lines.append("- 国标行业分类为「%s」，但经核查实际主业为「%s」。"
                 % (declared, actual_business or benchmark_used))
    if benchmark_used and benchmark_used != declared:
        lines.append("- 二者严重背离，以「%s」口径的上市公司基准衡量会系统性失真；"
                     "本报告已改以**实际主业（%s）**对应行业基准复核。"
                     % (declared, benchmark_used))
    else:
        lines.append("- 二者严重背离，以「%s」口径的上市公司基准衡量会系统性失真；"
                     "建议改以**实际主业**对应行业基准复核（如可行）。"
                     % declared)
    lines.append("")


def emit_qualitative(conn, lines, industry, year, level, profile, sec):
    """数据荒漠型 / 非上市主体的定性规模定位与能力边界声明。

    当企业无公开财务数据（metrics 为空）时，定量分位比对失效，转为：
      ① 以行业基准中位数作规模锚，对企业体量做定性定位；
      ② 行业名实校验（国标行业 vs 实际主业是否背离）；
      ③ 能力边界声明（公开数据稀缺，置信度 LOW）；
      ④ 「缺口即风险」默认授信建议。
    """
    def bm(ind):
        return conn.execute(
            "SELECT p50, unit, n, neg_count FROM benchmarks "
            "WHERE industry_level=? AND industry_name=? AND year=? AND indicator=?",
            (level, industry, year, ind)).fetchone()

    rev = bm("营业总收入")
    netp = bm("归母净利润")
    alr = bm("资产负债率")

    _heading(lines, sec, "定性规模定位（数据荒漠型主体）")
    lines.append("本企业**未取到公开财务数据**（财汇MCP 及公开渠道均无年报/评级/担保/"
                 "司法记录），无法做定量分位比对，以下仅以行业基准作方向性参照。")
    lines.append("")
    if rev and rev["p50"] is not None:
        u = rev["unit"]
        lines.append("- **体量锚**：%s 上市公司中位营业总收入 **%s**（样本 %d 家）。"
                     % (industry, fmt(rev["p50"], u), rev["n"]))
    rc = profile.get("registered_capital_wan")
    if rc is not None:
        rc_s = ("%.2f亿" % (rc / 10000.0)) if rc >= 10000 else ("%.0f万" % rc)
        if rev and rev["p50"]:
            try:
                import math
                ratio = rev["p50"] / float(rc)  # 同为「万元」口径，无量纲
                order = int(math.floor(math.log10(ratio))) if ratio > 0 else 0
                lines.append("- **注册资本 %s**，约为行业中位营收的 1/%d（低约 %d 个数量级），"
                             "属微型主体，与上市公司基准不具直接可比性，仅可作方向性参照。"
                             % (rc_s, int(ratio), order))
            except (TypeError, ValueError, ZeroDivisionError):
                lines.append("- **注册资本 %s**。" % rc_s)
        else:
            lines.append("- **注册资本 %s**。" % rc_s)
    if profile.get("employee_count") is not None:
        lines.append("- **参保/员工人数**：约 %s 人。" % profile["employee_count"])
    if profile.get("scale_label"):
        lines.append("- **企业规模标注**：%s。" % profile["scale_label"])
    lines.append("")

    # 行业名实校验
    declared = profile.get("declared_industry") or industry
    if profile.get("industry_match", True) is False:
        emit_industry_divergence(lines, sec, declared, industry,
                                 profile.get("actual_business"))
    elif profile.get("actual_business"):
        _heading(lines, sec, "行业名实校验")
        lines.append("- 国标行业「%s」与实际主营「%s」经核查**一致**，基准可比性可接受。"
                     % (industry, profile.get("actual_business")))
        lines.append("")

    # 能力边界声明
    _heading(lines, sec, "能力边界声明（非上市 / 数据稀缺主体）")
    lines.append("- 本企业为非上市（或数据未披露）主体，**公开披露信息极度有限**："
                 "财务、评级、担保、司法等多渠道常为零记录，本工具的分析置信度为 **LOW**。")
    lines.append("- 行业基准以上市公司为尺度，其在融资、治理、信披上系统性优于非上市主体，"
                 "以其衡量会**低估**相对风险——非上市客户的真实风险中枢通常更高。")
    lines.append("- 受公开数据可得性限制，对这类主体的「试手」式检索已触及信息天花板，"
                 "结论仅供**方向性参考**，不能替代现场尽调与借款人提供的审计财报。")
    lines.append("")

    # 缺口即风险 默认授信建议
    _heading(lines, sec, "「缺口即风险」默认授信建议")
    lines.append("- 在取得可靠财务数据前，按**缺口即风险**原则，建议**暂不予信用授信**。")
    lines.append("- 若业务确需介入，须同时满足：① 借款人提供**审计财务报表**；"
                 "② **足额强担保 / 抵质押**覆盖；③ 严格 KYC——凭统一社会信用代码（USCC）"
                 "排除同名/关联失信主体（曾发现同名不同码主体标注严重违法失信）；"
                 "④ 现场尽调核实实际经营与流水。")
    lines.append("")


def cmd_compare(args):
    conn = connect(args.db)
    conn.executescript(SCHEMA)
    ensure_extra_columns(conn)

    if args.input == "-":
        payload = json.load(sys.stdin)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            payload = json.load(f)

    company = payload.get("company") or "（未命名主体）"
    industry = payload.get("industry") or args.industry
    year = payload.get("year") or args.year
    level = payload.get("level") or args.level
    metrics = payload.get("metrics") or {}
    profile = payload.get("profile") or {}
    uscc = payload.get("uscc")
    is_listed = payload.get("is_listed", profile.get("is_listed"))
    has_metrics = bool({k: v for k, v in metrics.items() if v is not None})

    if not industry or not year:
        print("错误：需提供 industry 与 year（可写在输入 JSON 中或用命令行参数）。",
              file=sys.stderr)
        return 2

    col = LEVEL_COLUMNS[level]
    lines = []
    lines.append("# 行业基准比对：%s" % company)
    lines.append("")
    lines.append("| 项 | 值 |")
    lines.append("|---|---|")
    lines.append("| 比对行业 | %s（%s） |" % (industry, LEVEL_LABELS[level]))
    lines.append("| 比对年度 | %s 年报 |" % year)
    lines.append("| 基准来源 | 财汇MCP（企业预警通）同行业上市公司 |")
    if is_listed is not None:
        lines.append("| 是否上市 | %s |" % ("是" if is_listed else "否（非上市）"))
    if uscc:
        lines.append("| 统一社会信用代码 | %s |" % uscc)
    if profile.get("registered_capital_wan") is not None:
        rc = profile["registered_capital_wan"]
        rc_s = ("%.2f亿" % (rc / 10000.0)) if rc >= 10000 else ("%.0f万" % rc)
        lines.append("| 注册资本 | %s |" % rc_s)
    if profile.get("controller"):
        lines.append("| 实际控制人 | %s |" % profile["controller"])
    if profile.get("scale_label"):
        lines.append("| 企业规模 | %s |" % profile["scale_label"])
    if profile.get("actual_business"):
        lines.append("| 实际主业（核查） | %s |" % profile["actual_business"])
    # 规模匹配（门当户对）：客户营收 → 规模层 → 同层同业样本
    target_rev = metrics.get("营业总收入") if has_metrics else None
    scale_label, scale_lo, scale_hi = scale_bounds(target_rev)
    same_scale_uscc = None
    same_scale_n = 0
    scale_warns = []
    if target_rev is not None:
        try:
            trv = float(target_rev)
            scale_label, scale_lo, scale_hi = scale_bounds(trv)
            same_scale_uscc = peer_usccs_by_scale(
                conn, col, industry, year, scale_lo, scale_hi)
            same_scale_n = len(same_scale_uscc)
            lines.append("| 客户规模层 | %s（营收 %s） |" % (
                scale_label, fmt(trv, "万元")))
            lines.append("| 同层同业样本 | %d 家（营收 %s 至 %s 区间） |" % (
                same_scale_n,
                fmt(scale_lo, "万元") if scale_lo and scale_lo > 0 else "0",
                fmt(scale_hi, "万元") if scale_hi and scale_hi != float("inf") else "+∞"))
            # 量级悬殊降级检查：客户营收 vs 行业基准中位营收
            rev_b = conn.execute(
                "SELECT p50 FROM benchmarks WHERE industry_level=? "
                "AND industry_name=? AND year=? AND indicator='营业总收入'",
                (level, industry, year)).fetchone()
            if rev_b and rev_b["p50"]:
                med = rev_b["p50"]
                ratio = trv / float(med) if med else None
                if ratio is not None and (ratio < 0.1 or ratio > 10):
                    scale_warns.append(
                        "客户营收（%s）与行业基准中位营收（%s）相差超过 10 倍（比值 %.2f），"
                        "定量分位对比**降级为规模校正解读 / 定性定位**，"
                        "分位结论仅供方向参考，不得直接用于定级。"
                        % (fmt(trv, "万元"), fmt(med, "万元"), ratio))
        except (TypeError, ValueError):
            scale_warns.append("客户「营业总收入」数值无法解析，跳过规模分层。")
    lines.append("")

    rows = []
    gaps = []
    warns = []
    # 同层样本的原始值缓存（按指标），供同层分位计算
    same_scale_cache = {}

    def same_scale_vals(ind):
        """取同规模层同业在某指标上的原始值（缓存）。"""
        if ind not in same_scale_cache:
            if same_scale_uscc and same_scale_n > 0:
                marks = ",".join("?" * len(same_scale_uscc))
                same_scale_cache[ind] = [r[0] for r in conn.execute(
                    "SELECT f.value FROM financials f WHERE f.uscc IN (%s) "
                    "AND f.year=? AND f.indicator=? AND f.value IS NOT NULL"
                    % marks,
                    list(same_scale_uscc) + [year, ind])]
            else:
                same_scale_cache[ind] = []
        return same_scale_cache[ind]

    for ind, val in metrics.items():
        b = conn.execute("""
            SELECT * FROM benchmarks
            WHERE industry_level=? AND industry_name=? AND year=? AND indicator=?
        """, (level, industry, year, ind)).fetchone()
        if not b:
            gaps.append("指标「%s」在 %s %s年 尚无行业基准，"
                        "需先采集该指标的同业数据后复算。" % (ind, industry, year))
            continue
        if val is None:
            gaps.append("指标「%s」未提供企业实际值，无法比对。" % ind)
            continue

        # 取回原始样本，剔除比率型失真极端值后算百分位排名
        raw_vals = [r[0] for r in conn.execute("""
            SELECT f.value FROM financials f JOIN companies c ON c.uscc=f.uscc
            WHERE c.%s=? AND f.year=? AND f.indicator=? AND f.value IS NOT NULL
        """ % col, (industry, year, ind))]
        clean_vals, _ = clean_values(ind, raw_vals)
        own_outlier = outlier_flag(ind, float(val))
        rank = percentile_rank(clean_vals, float(val)) if clean_vals else None
        # 同规模层分位（门当户对）
        s_rank = None
        if same_scale_uscc and same_scale_n >= 5:
            s_raw = same_scale_vals(ind)
            s_clean, _ = clean_values(ind, s_raw)
            if s_clean:
                s_rank = percentile_rank(s_clean, float(val))
        if own_outlier:
            # 本企业自身比率失真（分母近零），排名无意义，转人工复核并标记高风险
            judge, level_txt = "数据失真(分母近零)", "高风险"
            warns.append("指标「%s」本企业数值 %s 已超出合理区间（分母近零导致比率失真），"
                         "不得据此排名，须结合净资产/资产负债率人工复核。"
                         % (ind, fmt(float(val), b["unit"])))
        else:
            judge, level_txt = interpret(b["direction"], rank)
        dev = fmt_deviation(val, b["p50"], b["unit"])

        rows.append((ind, val, b, rank, judge, level_txt, dev, s_rank))

        if b["reliability"] != "充足":
            warns.append("指标「%s」行业样本仅 %d 家，基准代表性不足，"
                         "结论须审慎采用。" % (ind, b["n"]))

    sec = [0]

    if rows:
        _heading(lines, sec, "指标分位定位")
        lines.append("| 指标 | 本企业 | 行业中位 | 行业P25 | 行业P75 | 样本数 | 所处分位 | 同层分位 | 偏离中位 | 判断 |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for (ind, val, b, rank, judge, level_txt, dev, s_rank) in rows:
            u = b["unit"]
            s_rank_s = ("第 %.0f 分位" % s_rank) if s_rank is not None else "—"
            lines.append("| %s | **%s** | %s | %s | %s | %d | %s | %s | %s | %s |" % (
                ind, fmt(float(val), u), fmt(b["p50"], u), fmt(b["p25"], u),
                fmt(b["p75"], u), b["n"],
                ("第 %.0f 分位" % rank) if rank is not None else "—",
                s_rank_s,
                dev, judge))
        lines.append("")
        if same_scale_uscc and same_scale_n >= 5:
            hi_s = fmt(scale_hi, "万元") if scale_hi and scale_hi != float("inf") else "+∞"
            lo_s = fmt(scale_lo, "万元") if scale_lo and scale_lo > 0 else "0"
            lines.append("> **门当户对说明**：上表「同层分位」基于**同规模层**同业样本"
                         "（%d 家，营收 %s–%s 区间）计算，避免与重量级同业直接对比失真；"
                         "「所处分位」为全行业口径，两者差异越大说明规模效应越显著。"
                         % (same_scale_n, lo_s, hi_s))
            lines.append("")

        adverse = [r for r in rows if r[5] in ("高风险", "关注")]
        _heading(lines, sec, "比对结论")
        if adverse:
            lines.append("本次比对共 %d 项指标，其中 **%d 项弱于同业**（全行业口径），具体为："
                         % (len(rows), len(adverse)))
            lines.append("")
            for (ind, val, b, rank, judge, level_txt, dev, s_rank) in adverse:
                u = b["unit"]
                s_txt = ("；同层分位 %.0f" % s_rank) if s_rank is not None else ""
                lines.append("- **%s**：本企业 %s，行业中位 %s（样本 %d 家），"
                             "处于第 %.0f 分位%s，%s（%s）"
                             % (ind, fmt(float(val), u), fmt(b["p50"], u),
                                b["n"], rank, s_txt, judge, level_txt))
        else:
            lines.append("本次比对共 %d 项指标，**未发现显著弱于同业的项目**。"
                         % len(rows))
        lines.append("")

        # 同层口径结论：若全行业劣于同业但同层不劣（或反之），须提示规模校正
        if same_scale_uscc and same_scale_n >= 5:
            flipped = []
            for (ind, val, b, rank, judge, level_txt, dev, s_rank) in rows:
                if rank is None or s_rank is None:
                    continue
                all_bad = judge in ("高风险", "关注")
                s_judge, _ = interpret(b["direction"], s_rank)
                s_bad = s_judge in ("高风险", "关注")
                if all_bad != s_bad:
                    flipped.append((ind, judge, s_judge))
            if flipped:
                lines.append("> **规模校正提示**：以下指标在全行业口径与同规模层口径下判定方向不一致，"
                             "建议以**同层口径**为主作评级依据（避免小体量客户被重量级同业拉低基准）：")
                for ind, j_all, j_s in flipped:
                    lines.append("- %s：全行业口径「%s」 → 同规模层口径「%s」"
                                 % (ind, j_all, j_s))
                lines.append("")

        # 行业整体处于困境时，须提示"未弱于同业"不等于"无风险"
        stressed = [r for r in rows
                    if (r[2]["neg_count"] or 0) > r[2]["n"] * 0.4
                    and r[2]["direction"] == "higher_better"]
        if stressed:
            b0 = stressed[0][2]
            lines.append("> **行业景气提示**：本行业 %s 项指标中，"
                         "%d/%d 家样本为负值，行业整体处于下行区间。"
                         "此时「与同业持平」不等于「经营稳健」，"
                         "须结合行业周期判断，避免以劣质基准掩盖个体风险。"
                         % (stressed[0][0], b0["neg_count"], b0["n"]))
            lines.append("")

    # 行业名实背离标注（数值路径同样需要：威新式"国标软件"实为"地产平台"）
    if profile.get("industry_match", True) is False:
        declared = profile.get("declared_industry") or industry
        emit_industry_divergence(lines, sec, declared, industry,
                                 profile.get("actual_business"))

    if warns or scale_warns:
        _heading(lines, sec, "基准可靠性提示")
        for w in (warns + scale_warns):
            lines.append("- %s" % w)
        lines.append("")

    # 零数据 / 非上市主体：自动转入定性规模定位 + 能力边界声明
    if not has_metrics:
        gaps.append("本企业无公开财务数据（财务/评级/担保/司法多渠道为零），全部财务指标缺失，"
                    "无法做定量比对；信息缺口本身即构成授信风险，须补审计财报后复评。")
        emit_qualitative(conn, lines, industry, year, level, profile, sec)

    _heading(lines, sec, "信息缺口")
    if gaps:
        for g in gaps:
            lines.append("- %s" % g)
    else:
        lines.append("- 无。所比对指标均已取得对应行业基准。")
    lines.append("")

    _heading(lines, sec, "方法论局限（须随报告一并披露）")
    lines.append("1. **样本为上市公司，非授信客户总体。** 上市公司在融资渠道、"
                 "治理规范性、信息披露质量上系统性优于非上市企业，"
                 "以其为尺度衡量非上市客户会**低估**相对风险，宜作偏乐观参照。")
    lines.append("2. **行业分类采用国标口径，与实际经营范围可能存在偏差。** "
                 "多元化经营主体按主营归类，跨业务比对须人工复核可比性。")
    lines.append("3. **比率型指标已做失真剔除。** 对净资产收益率/总资产报酬率/销售净利率"
                 "中因分母近零导致超出±100%（净利率±200%）的极端值已剔除出分位数分布，"
                 "并在基准表「极值剔除」列披露数量；其余维度的极端亏损或一次性损益仍会拉动分布，"
                 "已在基准表列示样本数、极值与为负家数供交叉判断。")
    lines.append("4. 本比对为辅助参考，**不替代正式审批决策**。")

    out = "\n".join(lines)
    if args.format == "json":
        print(json.dumps({
            "company": company, "industry": industry, "year": year,
            "is_listed": is_listed, "qualitative_mode": (not has_metrics),
            "scale": {
                "customer_scale": scale_label,
                "customer_revenue_wan": target_rev,
                "same_scale_peers": same_scale_n,
                "same_scale_range": [scale_lo, scale_hi],
                "scale_warnings": scale_warns,
            } if target_rev is not None else None,
            "items": [{
                "indicator": r[0], "value": r[1], "median": r[2]["p50"],
                "p25": r[2]["p25"], "p75": r[2]["p75"], "n": r[2]["n"],
                "unit": r[2]["unit"], "percentile_rank": r[3],
                "same_scale_rank": r[7],
                "judgement": r[4], "risk_level": r[5], "deviation": r[6]
            } for r in rows],
            "gaps": gaps, "warnings": warns,
            "profile": profile,
        }, ensure_ascii=False, indent=2))
    else:
        print(out)
    conn.close()
    return 0


def cmd_report(args):
    """生成数据库更新报告：已覆盖行业、基准速览、最近导入记录。

    用途：按用户要求，每次 ingest/compute 后运行，说明「更新/修改了什么、
    样本、分位、异常剔除、来源」，便于快速掌握本地库变化。
    """
    conn = connect(args.db)
    conn.executescript(SCHEMA)
    ensure_extra_columns(conn)

    lines = []
    lines.append("# 行业基准库 · 更新报告")
    lines.append("")
    lines.append("生成时间：%s" % now())
    lines.append("")
    try:
        size = os.path.getsize(args.db) / 1024.0
        lines.append("数据库体积：%.1f KB（SQLite 文本库，单行业约数十 KB，"
                     "全市场亦仅数 MB，磁盘占用可忽略）" % size)
    except OSError:
        pass
    lines.append("")

    rows = list(conn.execute("""
        SELECT c.industry_l2 AS ind, COUNT(DISTINCT c.uscc) AS n,
               COUNT(DISTINCT f.indicator) AS inds,
               MIN(f.year) AS y0, MAX(f.year) AS y1
        FROM companies c LEFT JOIN financials f ON f.uscc = c.uscc
        WHERE c.industry_l2 IS NOT NULL
        GROUP BY c.industry_l2 ORDER BY n DESC
    """))
    if rows:
        lines.append("## 已覆盖行业（尺度基准）")
        lines.append("")
        lines.append("| 行业 | 公司数 | 指标种类 | 年度范围 |")
        lines.append("|---|---|---|---|")
        for r in rows:
            span = ("%s–%s" % (r["y0"], r["y1"])) if r["y0"] else "无财务数据"
            lines.append("| %s | %d | %d | %s |"
                         % (r["ind"], r["n"], r["inds"] or 0, span))
        lines.append("")

    b_rows = list(conn.execute(
        "SELECT industry_name, year, indicator, n, p10, p50, p75, p90, "
        "unit, reliability, outlier_count FROM benchmarks "
        "ORDER BY industry_name, year DESC, indicator"))
    if b_rows:
        lines.append("## 各行业基准速览（分位数尺度）")
        lines.append("")
        lines.append("| 行业 | 年度 | 指标 | 样本 | P10 | 中位 | P75 | P90 | 单位 | 可靠性 | 极值剔除 |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in b_rows:
            oc = r["outlier_count"]
            lines.append("| %s | %s | %s | %d | %s | **%s** | %s | %s | %s | %s | %s |" % (
                r["industry_name"], r["year"], r["indicator"], r["n"],
                fmt(r["p10"], r["unit"]), fmt(r["p50"], r["unit"]),
                fmt(r["p75"], r["unit"]), fmt(r["p90"], r["unit"]),
                r["unit"] or "—", r["reliability"],
                (str(oc) if oc else "—")))
        lines.append("")

    logs = list(conn.execute(
        "SELECT * FROM ingest_log ORDER BY id DESC LIMIT ?", (args.last,)))
    if logs:
        lines.append("## 本次 / 最近更新记录（你要求的更新报告）")
        lines.append("")
        for l in logs:
            lines.append("- %s ｜ 类型 %s ｜ 读取 %d 行 ｜ 写入 %d 条 %s"
                         % (l["ts"], l["kind"], l["rows_in"] or 0,
                            l["rows_written"] or 0,
                            ("｜ 备注：" + l["note"]) if l["note"] else ""))
        lines.append("")
        lines.append("> 说明：每次经 MCP 新拉数据并执行 `ingest`/`compute` 后，"
                     "运行 `benchmark_db.py report` 即可生成此更新报告，列明"
                     "「更新/修改了什么、样本、分位、异常剔除、来源」，供你快速掌握本地库变化。")
    else:
        lines.append("## 更新记录")
        lines.append("")
        lines.append("- 暂无导入记录。")

    print("\n".join(lines))
    conn.close()
    return 0


def cmd_status(args):
    conn = connect(args.db)
    conn.executescript(SCHEMA)
    print("# 行业基准库概览")
    print("")
    print("数据库：%s" % args.db)
    try:
        size = os.path.getsize(args.db) / 1024.0
        print("体积：%.1f KB" % size)
    except OSError:
        pass
    print("")

    c = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    f = conn.execute("SELECT COUNT(*) FROM financials").fetchone()[0]
    b = conn.execute("SELECT COUNT(*) FROM benchmarks").fetchone()[0]
    print("| 表 | 记录数 |")
    print("|---|---|")
    print("| 公司维表 | %d |" % c)
    print("| 财务指标明细 | %d |" % f)
    print("| 行业基准 | %d |" % b)
    print("")

    rows = list(conn.execute("""
        SELECT c.industry_l2 AS ind, COUNT(DISTINCT c.uscc) AS n,
               COUNT(DISTINCT f.indicator) AS inds,
               MIN(f.year) AS y0, MAX(f.year) AS y1
        FROM companies c LEFT JOIN financials f ON f.uscc = c.uscc
        WHERE c.industry_l2 IS NOT NULL
        GROUP BY c.industry_l2 ORDER BY n DESC
    """))
    if rows:
        print("## 已覆盖行业（国标大类）")
        print("")
        print("| 行业 | 公司数 | 指标种类 | 年度范围 |")
        print("|---|---|---|---|")
        for r in rows:
            span = ("%s–%s" % (r["y0"], r["y1"])) if r["y0"] else "无财务数据"
            print("| %s | %d | %d | %s |" % (r["ind"], r["n"], r["inds"] or 0, span))
        print("")

    logs = list(conn.execute(
        "SELECT * FROM ingest_log ORDER BY id DESC LIMIT 5"))
    if logs:
        print("## 最近导入记录")
        print("")
        for l in logs:
            print("- %s ｜ %s ｜ 写入 %d 条 %s"
                  % (l["ts"], l["kind"], l["rows_written"] or 0,
                     ("｜ " + l["note"]) if l["note"] else ""))
    conn.close()
    return 0


# ===========================================================================
def main():
    p = argparse.ArgumentParser(
        description="行业基准本地数据库：采集入库、分位数计算、企业比对")
    p.add_argument("--db", default=DEFAULT_DB, help="数据库路径")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="建库")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("ingest", help="导入 MCP 返回数据")
    sp.add_argument("-i", "--input", required=True, help="JSON 文件路径，- 表示标准输入")
    sp.add_argument("-k", "--kind", default="auto",
                    choices=["auto", "companies", "financials"])
    sp.add_argument("--industry",
                    help="导入财务数据时，为尚未建档的公司自动打上该行业标签，"
                         "可省去单独导入公司清单")
    sp.add_argument("--level", default="l2", choices=["l1", "l2", "l3", "l4"],
                    help="--industry 对应的行业层级，默认 l2（国标大类）")
    sp.add_argument("--source", help="来源标注，默认「MCP·预警通」")
    sp.add_argument("--note", help="备注")
    sp.set_defaults(func=cmd_ingest)

    sp = sub.add_parser("compute", help="计算行业分位数基准")
    sp.add_argument("--level", default="l2", choices=["l1", "l2", "l3", "l4"])
    sp.add_argument("--industry", help="仅计算指定行业")
    sp.add_argument("--year", type=int, help="仅计算指定年度")
    sp.add_argument("--min-sample", type=int, default=MIN_SAMPLE)
    sp.add_argument("--listed-only", action="store_true", help="仅用已上市样本")
    sp.set_defaults(func=cmd_compute)

    sp = sub.add_parser("query", help="查询行业基准")
    sp.add_argument("--level", default="l2", choices=["l1", "l2", "l3", "l4"])
    sp.add_argument("--industry")
    sp.add_argument("--year", type=int)
    sp.add_argument("--indicator")
    sp.add_argument("-f", "--format", default="markdown",
                    choices=["markdown", "json"])
    sp.set_defaults(func=cmd_query)

    sp = sub.add_parser("compare", help="单家企业 vs 行业基准（无财务数据自动转定性定位）")
    sp.add_argument("-i", "--input", required=True,
                    help="企业指标 JSON，- 表示标准输入")
    sp.add_argument("--industry")
    sp.add_argument("--year", type=int)
    sp.add_argument("--level", default="l2", choices=["l1", "l2", "l3", "l4"])
    sp.add_argument("-f", "--format", default="markdown",
                    choices=["markdown", "json"])
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("status", help="库存概览")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("report", help="生成数据库更新报告")
    sp.add_argument("--last", type=int, default=5,
                    help="显示最近 N 条导入记录（默认 5）")
    sp.set_defaults(func=cmd_report)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
