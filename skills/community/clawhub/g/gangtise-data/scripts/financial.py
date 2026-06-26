import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import TextIOWrapper
from typing import List, Optional, Set, Tuple

import pandas as pd
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import (
    BALANCE_FIELD_CN,
    CASH_FLOW_FIELD_CN,
    GTS_AUTHORIZATION,
    FINANCIAL_REPORT_BALANCE_URL,
    FINANCIAL_REPORT_CASH_FLOW_URL,
    FINANCIAL_REPORT_CASH_FLOW_QUARTERLY_URL,
    FINANCIAL_REPORT_INCOME_URL,
    FINANCIAL_REPORT_INCOME_QUARTERLY_URL,
    INCOME_FIELD_CN,
    check_version,
    format_response,
)

# 命令行使用 Q1~Q4、Q0；发往 open 接口时映射为官方 period 枚举
FINANCIAL_PERIOD_CLI_TO_API = {
    "Q1": "q1",
    "Q2": "interim",
    "Q3": "q3",
    "Q4": "annual",
    "Q0": "latest",
}

# 财务报表共有元数据列（不参与「数值全空」判定中的「数值列」）
META_FIELDS_EN: Set[str] = {
    "securityCode",
    "companyName",
    "endDate",
    "fiscalYear",
    "period",
    "reportType",
    "companyType",
    "currency",
    "unit",
}

FINANCIAL_GRANULARITY_ARG_ALIASES = {
    "accumulated": "accumulated",
    "累计": "accumulated",
    "quarterly": "quarterly",
    "单季度": "quarterly",
}


def _normalize_financial_granularity(s: str) -> Tuple[Optional[str], Optional[str]]:
    if not s or not str(s).strip():
        return "accumulated", None
    key = str(s).strip().lower()
    if key in FINANCIAL_GRANULARITY_ARG_ALIASES:
        return FINANCIAL_GRANULARITY_ARG_ALIASES[key], None
    raw = str(s).strip()
    if raw in FINANCIAL_GRANULARITY_ARG_ALIASES:
        return FINANCIAL_GRANULARITY_ARG_ALIASES[raw], None
    return None, f"granularity 无效: {s}，可选 accumulated/累计、quarterly/单季度"


def _resolve_financial_report_url(
    table_type: str,
    granularity: str,
) -> Tuple[Optional[str], Optional[str]]:
    if table_type == "balance":
        if granularity != "accumulated":
            return None, "granularity=quarterly 仅对利润表和现金流量表有效，资产负债表仅支持 accumulated"
        return FINANCIAL_REPORT_BALANCE_URL, None
    if table_type == "income":
        return (
            FINANCIAL_REPORT_INCOME_QUARTERLY_URL
            if granularity == "quarterly"
            else FINANCIAL_REPORT_INCOME_URL
        ), None
    if table_type == "cashflow":
        return (
            FINANCIAL_REPORT_CASH_FLOW_QUARTERLY_URL
            if granularity == "quarterly"
            else FINANCIAL_REPORT_CASH_FLOW_URL
        ), None
    return None, f"table-type 无效: {table_type}"

TABLE_TYPE_LABEL_CN = {
    "income": "利润表",
    "balance": "资产负债表",
    "cashflow": "现金流量表",
}

TABLE_TYPE_ARG_ALIASES = {
    "income": "income",
    "profit": "income",
    "pl": "income",
    "利润表": "income",
    "balance": "balance",
    "bs": "balance",
    "资产负债表": "balance",
    "cashflow": "cashflow",
    "cf": "cashflow",
    "现金流量表": "cashflow",
}


def _normalize_table_type(s: str) -> Tuple[Optional[str], Optional[str]]:
    if not s or not str(s).strip():
        return "income", None
    key = str(s).strip().lower()
    if key in TABLE_TYPE_ARG_ALIASES:
        return TABLE_TYPE_ARG_ALIASES[key], None
    raw = str(s).strip()
    if raw in TABLE_TYPE_ARG_ALIASES:
        return TABLE_TYPE_ARG_ALIASES[raw], None
    return None, f"table-type 无效: {s}，可选 income/利润表、balance/资产负债表、cashflow/现金流量表"

META_FIELD_CN = {k: INCOME_FIELD_CN[k] for k in META_FIELDS_EN}

TABLE_TYPE_TO_FIELD_MAP = {
    "income": INCOME_FIELD_CN,
    "balance": BALANCE_FIELD_CN,
    "cashflow": CASH_FLOW_FIELD_CN,
}

META_CN_LABELS: Set[str] = {INCOME_FIELD_CN[k] for k in META_FIELDS_EN}


def _load_security_codes_from_file(path: str) -> List[str]:
    full_path = path
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"证券文件不存在: {path}")
    df = pd.read_csv(full_path)
    if "security_code" not in df.columns:
        raise ValueError("证券文件须包含 security_code 列（完整证券代码如 600519.SH）")
    return [str(x) for x in df["security_code"].dropna().tolist()]


def _looks_like_security_code(s: str) -> bool:
    t = s.strip().upper()
    return bool(re.match(r"^(\d{6}|[A-Z]?\d+)\.[A-Z]{2,4}$", t))


def _normalize_security_code(s: str) -> Optional[str]:
    if not s or not str(s).strip():
        return None
    t = str(s).strip()
    if not _looks_like_security_code(t):
        return None
    return t.upper()


def _fmt_yyyymmdd(val) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    t = str(val).strip()
    if len(t) == 8 and t.isdigit():
        return f"{t[:4]}-{t[4:6]}-{t[6:8]}"
    return t


def _map_financial_periods_cli_to_api(
    periods: Optional[List[str]],
) -> Tuple[List[str], Optional[str]]:
    """将 Q1~Q4、Q0 转为 open 接口 period 列表；默认 Q0→latest。"""
    if not periods:
        return ["latest"], None
    out: List[str] = []
    for p in periods:
        k = p.strip().upper()
        if k not in FINANCIAL_PERIOD_CLI_TO_API:
            return (
                [],
                f"period 仅支持 Q1/Q2/Q3/Q4/Q0（一季报/中报/三季报/年报/最新），无效: {p}",
            )
        out.append(FINANCIAL_PERIOD_CLI_TO_API[k])
    return out, None


def _parse_income_statement_body(body: dict) -> pd.DataFrame:
    if not body or str(body.get("code", "")) != "000000" or body.get("status") is False:
        return pd.DataFrame()
    block = body.get("data") or {}
    field_list = block.get("fieldList") or []
    rows = block.get("list") or []
    if not field_list or not rows:
        return pd.DataFrame()
    records = []
    for row in rows:
        if not isinstance(row, (list, tuple)):
            continue
        n = min(len(field_list), len(row))
        if n == 0:
            continue
        records.append({field_list[i]: row[i] for i in range(n)})
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def _drop_empty_value_rows_and_cols(df: pd.DataFrame) -> pd.DataFrame:
    """删除数值列全为空的行，以及数值列全为空的列（元数据列保留至仍有行）。"""
    if df.empty:
        return df
    d = df.copy()
    value_cols = [c for c in d.columns if c not in META_FIELDS_EN]
    if not value_cols:
        return d
    for c in value_cols:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    row_keep = d[value_cols].notna().any(axis=1)
    d = d.loc[row_keep].reset_index(drop=True)
    if d.empty:
        return d
    empty_val_cols = [c for c in value_cols if c in d.columns and d[c].notna().sum() == 0]
    d = d.drop(columns=empty_val_cols, errors="ignore")
    return d


def _rename_columns_for_table(df: pd.DataFrame, table_type: str) -> pd.DataFrame:
    field_map = TABLE_TYPE_TO_FIELD_MAP.get(table_type)
    if field_map:
        return df.rename(columns=lambda c: field_map.get(c, c))
    return df.rename(columns=lambda c: META_FIELD_CN.get(c, c))


def _round_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for c in d.columns:
        if c in META_CN_LABELS or c in META_FIELDS_EN:
            continue
        d[c] = pd.to_numeric(d[c], errors="coerce").round(2)
    return d


def _fetch_financial_report(
    report_url: str,
    headers: dict,
    security_code: str,
    start_date: Optional[str],
    end_date: Optional[str],
    fiscal_year: Optional[List[str]],
    period: List[str],
    report_type: List[str],
    field_list: List[str],
) -> pd.DataFrame:
    payload: dict = {
        "securityCode": security_code,
        "period": period,
        "reportType": report_type,
        "fieldList": field_list,
    }
    if start_date:
        payload["startDate"] = start_date
    else:
        payload["startDate"] = None
    if end_date:
        payload["endDate"] = end_date
    else:
        payload["endDate"] = None
    if fiscal_year:
        payload["fiscalYear"] = fiscal_year
    else:
        payload["fiscalYear"] = None
    try:
        r = requests.post(report_url, headers=headers, json=payload, timeout=120)
        if r.status_code != 200:
            return pd.DataFrame()
        body = r.json()
        return _parse_income_statement_body(body)
    except Exception:
        return pd.DataFrame()


def financial_data(
    securities: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fiscal_year: Optional[List[str]] = None,
    period: Optional[List[str]] = None,
    report_type: Optional[List[str]] = None,
    field_list: Optional[List[str]] = None,
    table_type: str = "income",
    granularity: str = "accumulated",
):
    usage: dict = {}
    if GTS_AUTHORIZATION is None:
        return format_response(
            {"state": "error", "message": "未配置 gangtise 授权，无法调用 open 接口", "data": [], "usage": usage},
            "financial",
        )

    table_norm, table_err = _normalize_table_type(table_type)
    if table_err:
        return format_response(
            {"state": "error", "message": table_err, "data": [], "usage": usage},
            "financial",
        )
    granularity_norm, granularity_err = _normalize_financial_granularity(granularity)
    if granularity_err:
        return format_response(
            {"state": "error", "message": granularity_err, "data": [], "usage": usage},
            "financial",
        )

    report_url, report_url_err = _resolve_financial_report_url(table_norm, granularity_norm)
    if report_url_err:
        return format_response(
            {"state": "error", "message": report_url_err, "data": [], "usage": usage},
            "financial",
        )

    table_label = TABLE_TYPE_LABEL_CN[table_norm]

    headers = {"Authorization": GTS_AUTHORIZATION}

    period_list, period_err = _map_financial_periods_cli_to_api(period)
    if period_err:
        return format_response(
            {"state": "error", "message": period_err, "data": [], "usage": usage},
            "financial",
        )
    report_list = report_type if report_type is not None else ["consolidated"]
    fields = field_list if field_list is not None else []

    codes: List[str] = []
    for sec in securities:
        c = _normalize_security_code(sec)
        if c:
            codes.append(c)
    if not codes:
        return format_response(
            {
                "state": "error",
                "message": "未找到有效证券代码，请仅输入完整代码（如 600519.SH）",
                "data": [],
                "usage": usage,
            },
            "financial",
        )

    frames: List[pd.DataFrame] = []
    with ThreadPoolExecutor(max_workers=min(len(codes), 8)) as ex:
        futs = [
            ex.submit(
                _fetch_financial_report,
                report_url,
                headers,
                code,
                start_date,
                end_date,
                fiscal_year,
                period_list,
                report_list,
                fields,
            )
            for code in codes
        ]
        for fut in as_completed(futs):
            part = fut.result()
            if not part.empty:
                frames.append(part)

    if not frames:
        return format_response(
            {"state": "error", "message": f"未找到{table_label}数据", "data": [], "usage": usage},
            "financial",
        )

    data = pd.concat(frames, ignore_index=True)

    data = data.drop(columns=["category", "announcementDate"], errors="ignore")

    if "endDate" in data.columns:
        data["endDate"] = data["endDate"].map(_fmt_yyyymmdd)

    data = _drop_empty_value_rows_and_cols(data)
    if data.empty:
        return format_response(
            {"state": "error", "message": f"过滤空值后无{table_label}数据", "data": [], "usage": usage},
            "financial",
        )

    data = _rename_columns_for_table(data, table_norm)
    data = _round_numeric_values(data)
    if "证券代码" in data.columns and "财报截止日期" in data.columns:
        data = data.sort_values(
            by=["证券代码", "财报截止日期"],
            ascending=[True, False],
        ).reset_index(drop=True)

    col_map = {
        "证券简称": "security_abbr",
        "证券代码": "security_code",
        "财报截止日期": "date",
    }
    for col in list(data.columns):
        if col in col_map:
            data.rename(columns={col: col_map[col]}, inplace=True)
    front = ["security_abbr", "security_code", "date"]
    columns = [c for c in front if c in data.columns] + [
        c for c in data.columns if c not in front
    ]
    data = data[columns]

    success_label = "、".join(codes[:3]) + "等" if len(codes) > 3 else "、".join(codes)
    parts = [
        {
            "data": data.to_dict(orient="records"),
            "module": "financial",
            "type": "data",
        }
    ]
    return format_response(
        {
            "state": "success",
            "message": f"已找到{success_label}{table_label}数据",
            "data": parts,
            "usage": usage,
        },
        "financial",
    )


def main():
    import argparse

    try:
        if not check_version():
            update_sh = os.path.join(script_dir, "update.sh")
            print(f"[WARNING] 存在 Gangtise data 版本更新，可以执行 {update_sh} 更新，请与用户确认是否更新\n")
    except Exception:
        print("[WARNING] 检查 Gangtise data 版本失败\n")

    parser = argparse.ArgumentParser(
        description="查询财务报表：利润表 / 资产负债表 / 现金流量表（open financial-report）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--table-type",
        default="income",
        help="报表：income|利润表、balance|资产负债表、cashflow|现金流量表",
    )
    parser.add_argument(
        "-g",
        "--granularity",
        default="accumulated",
        help="口径：accumulated|累计、quarterly|单季度（仅利润表/现金流量表）",
    )
    parser.add_argument("-sd", "--start-date", default=None, help="开始日期 yyyy-MM-dd")
    parser.add_argument("-ed", "--end-date", default=None, help="结束日期 yyyy-MM-dd")
    parser.add_argument(
        "--fiscal-year",
        default=None,
        help="财报年度，逗号分隔，如 2024,2025",
    )
    parser.add_argument(
        "--period",
        default="Q0",
        help="报告期：Q1/Q2/Q3/Q4/Q0（一季报/中报/三季报/年报/最新），逗号分隔；默认 Q0",
    )
    parser.add_argument(
        "--report-type",
        default="consolidated",
        help="报表类型：consolidated/consolidatedRestated/standalone/standaloneRestated，逗号分隔",
    )
    parser.add_argument(
        "--field-list",
        default=None,
        help="指定科目英文字段名，逗号分隔；不传则 fieldList=[] 取全部",
    )
    parser.add_argument("--securities", default=None, help="证券代码逗号分隔")
    parser.add_argument("--securities-file", default=None, help="csv 含 security_code 列")
    args = parser.parse_args()

    fy: Optional[List[str]] = None
    if args.fiscal_year:
        fy = [x.strip() for x in args.fiscal_year.replace("，", ",").split(",") if x.strip()]

    period_list = [
        x.strip() for x in args.period.replace("，", ",").split(",") if x.strip()
    ]
    report_list = [x.strip() for x in args.report_type.replace("，", ",").split(",") if x.strip()]

    fl: Optional[List[str]] = None
    if args.field_list:
        fl = [x.strip() for x in args.field_list.replace("，", ",").split(",") if x.strip()]

    securities: Optional[List[str]] = None
    if args.securities:
        securities = [x.strip() for x in args.securities.replace("，", ",").split(",") if x.strip()]
    if not securities and args.securities_file:
        try:
            securities = _load_security_codes_from_file(args.securities_file)
        except Exception as e:
            print(f"根据证券文件解析证券失败: {e}")
            sys.exit(1)

    if not securities:
        parser.error("必须至少提供 --securities 或 --securities-file")

    out = financial_data(
        securities=securities,
        start_date=args.start_date,
        end_date=args.end_date,
        fiscal_year=fy,
        period=period_list if period_list else None,
        report_type=report_list if report_list else None,
        field_list=fl,
        table_type=args.table_type,
        granularity=args.granularity,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
