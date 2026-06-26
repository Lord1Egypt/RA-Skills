import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from io import TextIOWrapper
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import GTS_AUTHORIZATION, check_version, format_response

EARNING_FORECAST_URL = "https://open.gangtise.com/application/open-fundamental/earning_forecast"

ALL_CONSENSUS_FIELDS: List[str] = [
    "netIncome",
    "netIncomeYoy",
    "eps",
    "pe",
    "bps",
    "pb",
    "peg",
    "roe",
    "ps",
]

CONSENSUS_CN: Dict[str, str] = {
    "netIncome": "归母净利润",
    "netIncomeYoy": "归母净利润同比增速(%)",
    "eps": "每股收益",
    "pe": "市盈率",
    "bps": "每股净资产",
    "pb": "市净率",
    "peg": "PEG",
    "roe": "净资产收益率",
    "ps": "市销率",
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


def _normalize_consensus_list(consensus_list: Optional[List[str]]) -> Tuple[List[str], Optional[str]]:
    if not consensus_list:
        return list(ALL_CONSENSUS_FIELDS), None
    out: List[str] = []
    seen = set()
    for item in consensus_list:
        key = str(item).strip()
        if not key:
            continue
        if key not in ALL_CONSENSUS_FIELDS:
            return [], f"consensus-list 含无效指标: {key}，可选值为 {','.join(ALL_CONSENSUS_FIELDS)}"
        if key not in seen:
            seen.add(key)
            out.append(key)
    return (out if out else list(ALL_CONSENSUS_FIELDS)), None


def _parse_earning_forecast_body(body: dict, consensus_fields: List[str]) -> pd.DataFrame:
    if not body or str(body.get("code", "")) != "000000" or body.get("status") is False:
        return pd.DataFrame()

    block = body.get("data") or {}
    security_code = block.get("securityCode")
    security_name = block.get("securityName")
    update_list = block.get("updateList") or []
    if not security_code or not update_list:
        return pd.DataFrame()

    records: List[dict] = []
    for update_item in update_list:
        if not isinstance(update_item, dict):
            continue
        d = str(update_item.get("date") or "").strip()
        if not d:
            continue
        field_list = update_item.get("fieldList") or []
        for field_item in field_list:
            if not isinstance(field_item, dict):
                continue
            forecast_year = str(field_item.get("forecastYear") or "").strip()
            if not forecast_year:
                continue
            row = {
                "security_abbr": security_name,
                "security_code": security_code,
                "date": d,
                "预测年份": forecast_year,
            }
            for f in consensus_fields:
                cn = CONSENSUS_CN[f]
                row[cn] = field_item.get(f)
            records.append(row)

    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)

    metric_cols = [CONSENSUS_CN[f] for f in consensus_fields]
    for c in metric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").round(4)

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df = df.dropna(subset=["date"])

    front = ["security_abbr", "security_code", "date", "预测年份"]
    cols = [c for c in front if c in df.columns] + [c for c in metric_cols if c in df.columns]
    cols += [c for c in df.columns if c not in cols]
    df = df[cols]
    return df


def _fetch_one_security_forecast(
    sec: str,
    start_date: str,
    end_date: str,
    consensus_fields: List[str],
    headers: dict,
) -> Tuple[str, pd.DataFrame, bool, Optional[str]]:
    def _request_once(req_start_date: str, req_end_date: str) -> Tuple[pd.DataFrame, Optional[str]]:
        payload = {
            "securityCode": sec,
            "startDate": req_start_date,
            "endDate": req_end_date,
            "consensusList": consensus_fields,
        }
        try:
            r = requests.post(EARNING_FORECAST_URL, headers=headers, json=payload, timeout=120)
            if r.status_code != 200:
                return pd.DataFrame(), f"接口请求失败: HTTP {r.status_code}"
            body = r.json()
            return _parse_earning_forecast_body(body, consensus_fields), None
        except Exception as e:
            return pd.DataFrame(), f"接口请求异常: {e}"

    df, req_err = _request_once(start_date, end_date)
    if req_err:
        return sec, pd.DataFrame(), False, req_err

    fallback_used = False
    # 当目标为单日且无数据时，仅向前回退一天重试一次。
    if df.empty and start_date == end_date:
        try:
            d = pd.to_datetime(start_date, errors="coerce")
            if pd.notna(d):
                prev_date = (d.date() - timedelta(days=1)).strftime("%Y-%m-%d")
                df_prev, prev_err = _request_once(prev_date, prev_date)
                if prev_err:
                    return sec, pd.DataFrame(), False, prev_err
                if not df_prev.empty:
                    df = df_prev
                    fallback_used = True
        except Exception:
            pass

    return sec, df, fallback_used, None


def earning_forecast_data(
    securities: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    consensus_list: Optional[List[str]] = None,
):
    usage: dict = {}
    if GTS_AUTHORIZATION is None:
        return format_response(
            {"state": "error", "message": "未配置 gangtise 授权，无法调用 open 接口", "data": [], "usage": usage},
            "earning_forecast",
        )

    codes: List[str] = []
    for sec in securities:
        c = _normalize_security_code(sec)
        if c:
            codes.append(c)
    if not codes:
        return format_response(
            {"state": "error", "message": "未找到有效证券代码，请输入完整代码（如 600519.SH）", "data": [], "usage": usage},
            "earning_forecast",
        )

    if not end_date:
        end_date = date.today().strftime("%Y-%m-%d")
    if not start_date:
        start_date = end_date

    consensus_fields, consensus_err = _normalize_consensus_list(consensus_list)
    if consensus_err:
        return format_response(
            {"state": "error", "message": consensus_err, "data": [], "usage": usage},
            "earning_forecast",
        )

    headers = {"Authorization": GTS_AUTHORIZATION}

    frames: List[pd.DataFrame] = []
    fallback_codes: List[str] = []
    request_errors: List[str] = []
    with ThreadPoolExecutor(max_workers=min(len(codes), 8)) as ex:
        futs = [
            ex.submit(
                _fetch_one_security_forecast,
                code,
                start_date,
                end_date,
                consensus_fields,
                headers,
            )
            for code in codes
        ]
        for fut in as_completed(futs):
            sec, df_one, fallback_used, req_err = fut.result()
            if req_err:
                request_errors.append(f"{sec}: {req_err}")
                continue
            if not df_one.empty:
                frames.append(df_one)
            if fallback_used:
                fallback_codes.append(sec)

    if not frames:
        err_msg = "未找到盈利预测数据"
        if request_errors:
            err_msg = "；".join(request_errors)
        return format_response(
            {"state": "error", "message": err_msg, "data": [], "usage": usage},
            "earning_forecast",
        )

    df = pd.concat(frames, ignore_index=True)
    df = df.sort_values(by=["security_code", "date", "预测年份"], ascending=[True, False, True]).reset_index(drop=True)
    df = df.drop(columns=["security_abbr"], errors="ignore")

    parts = [
        {
            "data": df.to_dict(orient="records"),
            "module": "earning_forecast",
            "type": "data",
        }
    ]
    success_securities = "、".join(codes[:3]) + "等" if len(codes) > 3 else "、".join(codes)
    fallback_note = ""
    if fallback_codes:
        show = "、".join(sorted(set(fallback_codes))[:3])
        fallback_note = f"（以下证券当日无数据，已回退前一日：{show}"
        if len(set(fallback_codes)) > 3:
            fallback_note += "等"
        fallback_note += "）"

    return format_response(
        {
            "state": "success",
            "message": f"已找到{success_securities}盈利预测数据{fallback_note}",
            "data": parts,
            "usage": usage,
        },
        "earning_forecast",
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
        description="查询券商盈利预测（open earning_forecast）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    today_str = date.today().strftime("%Y-%m-%d")
    parser.add_argument("--securities", default=None, help="证券代码逗号分隔")
    parser.add_argument("--securities-file", default=None, help="csv 须含 security_code 列")
    parser.add_argument("-sd", "--start-date", default=today_str, help="开始日期 yyyy-MM-dd")
    parser.add_argument("-ed", "--end-date", default=today_str, help="结束日期 yyyy-MM-dd")
    parser.add_argument(
        "--consensus-list",
        default=None,
        help=f"一致预期指标，逗号分隔；可选 {','.join(ALL_CONSENSUS_FIELDS)}；不传默认全部",
    )
    args = parser.parse_args()

    consensus: Optional[List[str]] = None
    if args.consensus_list:
        consensus = [x.strip() for x in args.consensus_list.replace("，", ",").split(",") if x.strip()]

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

    out = earning_forecast_data(
        securities=securities,
        start_date=args.start_date,
        end_date=args.end_date,
        consensus_list=consensus,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
