import os
import re
import sys
from datetime import date, timedelta
from io import TextIOWrapper
from typing import List, Optional

import pandas as pd
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import GTS_AUTHORIZATION, check_version, format_response

GANGTISE_FUNDAMENTAL_DOMAIN = os.getenv(
    "GANGTISE_DOMAIN", "https://open.gangtise.com/application/open-fundamental"
)
TOP_HOLDERS_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/capital-structure/top-holders"

HOLDER_TYPE_MAP = {
    "top10": "top10",
    "top10float": "top10Float",
    "top10Float": "top10Float",
}
PERIOD_MAP = {
    "q1": "q1",
    "interim": "interim",
    "q3": "q3",
    "annual": "annual",
    "latest": "latest",
}


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


def _normalize_holder_type(holder_type: str) -> Optional[str]:
    if not holder_type:
        return None
    key = str(holder_type).strip()
    if key in HOLDER_TYPE_MAP:
        return HOLDER_TYPE_MAP[key]
    low = key.lower()
    return HOLDER_TYPE_MAP.get(low)


def _normalize_periods(period: Optional[List[str]]) -> Optional[List[str]]:
    if not period:
        return ["latest"]
    out: List[str] = []
    for p in period:
        k = str(p).strip().lower()
        if not k:
            continue
        if k in PERIOD_MAP and PERIOD_MAP[k] not in out:
            out.append(PERIOD_MAP[k])
    return out or ["latest"]


def _normalize_fiscal_year(fiscal_year: Optional[List[str]]) -> Optional[List[str]]:
    if not fiscal_year:
        return None
    out: List[str] = []
    for y in fiscal_year:
        ys = str(y).strip()
        if len(ys) == 4 and ys.isdigit() and ys not in out:
            out.append(ys)
    return out or None


def _parse_shareholder_body(body: dict, holder_type: str, security_code: str) -> pd.DataFrame:
    if not body or str(body.get("code", "")) != "000000" or body.get("status") is False:
        return pd.DataFrame()
    block = body.get("data") or {}
    rows = block.get("list") or []
    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame()

    df.insert(0, "security_code", security_code)
    df.insert(1, "holder_type", holder_type)
    df = df.rename(
        columns={
            "reportPeriod": "date",
            "rank": "rank",
            "shareholderName": "shareholder_name",
            "shareholderType": "shareholder_type",
            "holdingNum": "holding_num",
            "holdingPct": "holding_pct",
            "chgNum": "chg_num",
            "chgPct": "chg_pct",
            "shareCategory": "share_category",
        }
    )
    return df


def _fetch_shareholder(
    headers: dict,
    security_code: str,
    holder_type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fiscal_year: Optional[List[str]] = None,
    period: Optional[List[str]] = None,
) -> pd.DataFrame:
    payload = {
        "securityCode": security_code,
        "holderType": holder_type,
        "period": period or ["latest"],
    }
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date
    if fiscal_year:
        payload["fiscalYear"] = fiscal_year

    try:
        r = requests.post(TOP_HOLDERS_URL, headers=headers, json=payload, timeout=120)
        if r.status_code != 200:
            return pd.DataFrame()
        body = r.json()
        return _parse_shareholder_body(body, holder_type=holder_type, security_code=security_code)
    except Exception:
        return pd.DataFrame()


def shareholder_data(
    securities: List[str],
    holder_type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fiscal_year: Optional[List[str]] = None,
    period: Optional[List[str]] = None,
):
    usage: dict = {}
    if GTS_AUTHORIZATION is None:
        return format_response(
            {"state": "error", "message": "未配置 gangtise 授权，无法调用 open 接口", "data": [], "usage": usage},
            "shareholder",
        )

    normalized_holder_type = _normalize_holder_type(holder_type)
    if not normalized_holder_type:
        return format_response(
            {
                "state": "error",
                "message": "holderType 仅支持 top10 或 top10Float",
                "data": [],
                "usage": usage,
            },
            "shareholder",
        )

    fy = _normalize_fiscal_year(fiscal_year)
    periods = _normalize_periods(period)
    headers = {"Authorization": GTS_AUTHORIZATION}

    if not end_date and start_date:
        end_date = date.today().strftime("%Y-%m-%d")
    if not start_date and end_date:
        start_date = (date.fromisoformat(end_date) - timedelta(days=365 * 3)).strftime("%Y-%m-%d")

    securities_codes: List[str] = []
    for sec in securities:
        c = _normalize_security_code(sec)
        if c:
            securities_codes.append(c)
    if not securities_codes:
        return format_response(
            {
                "state": "error",
                "message": "未找到有效证券代码，请仅输入完整代码（如 600519.SH）",
                "data": [],
                "usage": usage,
            },
            "shareholder",
        )

    frames: List[pd.DataFrame] = []
    for code in securities_codes:
        df_one = _fetch_shareholder(
            headers=headers,
            security_code=code,
            holder_type=normalized_holder_type,
            start_date=start_date,
            end_date=end_date,
            fiscal_year=fy,
            period=periods,
        )
        if not df_one.empty:
            frames.append(df_one)

    if not frames:
        return format_response(
            {"state": "error", "message": "未找到股东数据", "data": [], "usage": usage},
            "shareholder",
        )

    data = pd.concat(frames, ignore_index=True)
    if "date" in data.columns:
        data["_dt"] = pd.to_datetime(data["date"], errors="coerce")
        data = data.sort_values(by=["security_code", "_dt", "rank"], ascending=[True, False, True]).reset_index(drop=True)
        data = data.drop(columns=["_dt"], errors="ignore")

    for c in ["holding_num", "holding_pct", "chg_num", "chg_pct"]:
        if c in data.columns:
            data[c] = pd.to_numeric(data[c], errors="coerce")

    success_label = "、".join(securities_codes[:3]) + "等" if len(securities_codes) > 3 else "、".join(securities_codes)
    parts = [{"data": data.to_dict(orient="records"), "module": "top_holders", "type": "data"}]
    return format_response(
        {
            "state": "success",
            "message": f"已找到{success_label}股东数据",
            "data": parts,
            "usage": usage,
        },
        "shareholder",
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
        description="查询前十大股东/前十大流通股东（open top-holders）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--holder-type", required=True, help="股东类型：top10 或 top10Float")
    parser.add_argument("-sd", "--start-date", default=None, help="开始日期 yyyy-MM-dd")
    parser.add_argument("-ed", "--end-date", default=None, help="结束日期 yyyy-MM-dd")
    parser.add_argument("--fiscal-year", default=None, help="财报年度，逗号分隔，如 2024,2025")
    parser.add_argument(
        "--period",
        default="latest",
        help="报告期：q1/interim/q3/annual/latest，逗号分隔；默认 latest",
    )
    parser.add_argument("--securities", default=None, help="证券代码逗号分隔")
    parser.add_argument("--securities-file", default=None, help="csv 含 security_code 列")
    args = parser.parse_args()

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

    fy: Optional[List[str]] = None
    if args.fiscal_year:
        fy = [x.strip() for x in args.fiscal_year.replace("，", ",").split(",") if x.strip()]
    period_list = [x.strip() for x in args.period.replace("，", ",").split(",") if x.strip()]

    out = shareholder_data(
        securities=securities,
        holder_type=args.holder_type,
        start_date=args.start_date,
        end_date=args.end_date,
        fiscal_year=fy,
        period=period_list if period_list else None,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
