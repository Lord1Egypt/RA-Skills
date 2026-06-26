import os
import re
import sys
from datetime import date, datetime, timedelta
from io import TextIOWrapper
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

import pandas as pd
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import (
    GTS_AUTHORIZATION,
    QUOTE_ADJUST_FACTOR_URL,
    QUOTE_MINUTE_URL,
    QUOTE_HK_URL,
    QUOTE_URL,
    check_version,
    format_response,
)

# 与 open 日 K 文档一致
_FIELD_LIST = [
    "securityCode",
    "tradeDate",
    "open",
    "high",
    "low",
    "close",
    "preClose",
    "change",
    "pctChange",
    "volume",
    "amount",
]

API_FIELD_TO_CN = {
    "securityCode": "证券代码",
    "tradeDate": "日期",
    "open": "开盘价",
    "high": "最高价",
    "low": "最低价",
    "close": "收盘价",
    "preClose": "昨收价",
    "change": "涨跌额",
    "pctChange": "涨跌幅",
    "volume": "成交量",
    "amount": "成交额",
}

MINUTE_FIELD_LIST = [
    "securityCode",
    "tradeTime",
    "open",
    "high",
    "low",
    "close",
    "change",
    "pctChange",
    "volume",
    "amount",
]

MINUTE_API_FIELD_TO_CN = {
    "securityCode": "证券代码",
    "tradeTime": "日期",
    "open": "开盘价",
    "high": "最高价",
    "low": "最低价",
    "close": "收盘价",
    "change": "涨跌额",
    "pctChange": "涨跌幅",
    "volume": "成交量",
    "amount": "成交额",
}

def _last_day_of_month(d: date) -> date:
    if d.month == 12:
        return date(d.year, 12, 31)
    return date(d.year, d.month + 1, 1) - timedelta(days=1)


def _month_date_chunks(start_date: str, end_date: str) -> List[Tuple[str, str]]:
    s = datetime.strptime(start_date[:10], "%Y-%m-%d").date()
    e = datetime.strptime(end_date[:10], "%Y-%m-%d").date()
    out: List[Tuple[str, str]] = []
    cur = s
    while cur <= e:
        month_start = cur.replace(day=1)
        month_end = _last_day_of_month(month_start)
        seg_s = cur
        seg_e = min(e, month_end)
        out.append((seg_s.isoformat(), seg_e.isoformat()))
        cur = seg_e + timedelta(days=1)
    return out


def normalize_adjust_mode(raw: Optional[str]) -> str:
    """返回 none | forward | backward；默认前复权 forward。"""
    if raw is None or not str(raw).strip():
        return "forward"
    s = str(raw).strip()
    sl = s.lower()
    if sl in {"none", "raw", "no", "noadj", "unadjusted"} or s == "不复权":
        return "none"
    if sl in {"forward", "qfq"} or s == "前复权":
        return "forward"
    if sl in {"backward", "hfq"} or s == "后复权":
        return "backward"
    return "forward"


def _adj_price_suffix(mode: str) -> str:
    return "(前复权)" if mode == "forward" else "(后复权)"


def _fetch_adjust_factor_body(
    headers: dict,
    security_list: List[str],
    start_date: str,
    end_date: str,
    limit: int,
) -> Tuple[pd.DataFrame, Optional[str]]:
    payload = {
        "securityList": security_list,
        "startDate": start_date[:10],
        "endDate": end_date[:10],
        "limit": min(int(limit), 10000),
    }
    try:
        r = requests.post(QUOTE_ADJUST_FACTOR_URL, headers=headers, json=payload, timeout=300)
        if r.status_code != 200:
            return pd.DataFrame(), r.text
        body = r.json()
    except Exception as ex:
        return pd.DataFrame(), str(ex)
    return _parse_kline_body(body), None


def fetch_adjust_factors_batched(
    headers: dict,
    security_list: List[str],
    start_date: str,
    end_date: str,
    limit_per_request: int,
) -> Tuple[pd.DataFrame, Optional[str]]:
    """按自然月拆请求，合并去重，降低单次超 10000 行风险。"""
    chunks = _month_date_chunks(start_date, end_date)
    parts: List[pd.DataFrame] = []
    errs: List[str] = []
    for sd, ed in chunks:
        df, err = _fetch_adjust_factor_body(headers, security_list, sd, ed, limit_per_request)
        if err:
            errs.append(f"{sd}~{ed}: {err}")
            continue
        if not df.empty:
            parts.append(df)
    if errs and not parts:
        return pd.DataFrame(), "；".join(errs)
    if not parts:
        return pd.DataFrame(), "复权因子接口无数据" if not errs else "；".join(errs)
    merged = pd.concat(parts, ignore_index=True)
    if "securityCode" in merged.columns and "tradeDate" in merged.columns:
        merged = merged.drop_duplicates(subset=["securityCode", "tradeDate"], keep="last")
    warn = "；".join(errs) if errs else None
    return merged, warn


def _apply_daily_adjust_with_factors(data: pd.DataFrame, factors: pd.DataFrame, mode: str) -> Tuple[pd.DataFrame, Optional[str]]:
    """
    使用独立 adjustFactor 接口返回的因子调整日 K。
    前复权：P'(t) = P(t) × F(t) / F(t_latest)，t_latest 为本结果中该证券最后交易日。
    后复权：P'(t) = P(t) × F(t) / F(t_earliest)，t_earliest 为本结果中该证券首个交易日。
    """
    if factors.empty:
        return data, "未获取到复权因子，无法计算复权行情"
    need = {"证券代码", "日期", "开盘价", "最高价", "最低价", "收盘价"}
    if not need.issubset(data.columns):
        return data, "行情数据缺少 OHLC 列，无法复权"

    fac = factors.rename(columns={"securityCode": "证券代码", "tradeDate": "日期", "adjustFactor": "_f"})
    fac["日期"] = pd.to_datetime(fac["日期"], errors="coerce").dt.strftime("%Y-%m-%d")
    fac["证券代码"] = fac["证券代码"].astype(str).str.upper()
    fac["_f"] = pd.to_numeric(fac["_f"], errors="coerce")

    d = data.copy()
    d["_dt"] = pd.to_datetime(d["日期"], errors="coerce")
    d["日期"] = d["_dt"].dt.strftime("%Y-%m-%d")
    d["证券代码"] = d["证券代码"].astype(str).str.upper()

    d = d.merge(fac[["证券代码", "日期", "_f"]], on=["证券代码", "日期"], how="left")
    d = d.sort_values(by=["证券代码", "_dt"])
    d["_f"] = d.groupby("证券代码", sort=False)["_f"].ffill().bfill()

    missing = d["_f"].isna() | (d["_f"] == 0)
    if missing.any():
        ub = d.loc[missing, "证券代码"].drop_duplicates()
        bad = ub.head(20).tolist()
        hint = ",".join(bad)
        if len(ub) > 20:
            hint += "…"
        return data, f"部分交易日缺少有效复权因子（证券示例：{hint}），无法完成复权"

    d = d.sort_values(by=["证券代码", "_dt"])
    if mode == "forward":
        d["_f_anchor"] = d.groupby("证券代码", sort=False)["_f"].transform("last")
    else:
        d["_f_anchor"] = d.groupby("证券代码", sort=False)["_f"].transform("first")

    mult = d["_f"] / d["_f_anchor"]
    mult = mult.mask(d["_f_anchor"].isna() | (d["_f_anchor"] == 0))

    suffix = _adj_price_suffix(mode)
    for col in ["开盘价", "最高价", "最低价", "收盘价"]:
        if col in d.columns:
            v = pd.to_numeric(d[col], errors="coerce")
            d[f"{col}{suffix}"] = (v * mult).round(2)

    close_adj = f"收盘价{suffix}"
    d = d.sort_values(by=["证券代码", "_dt"])
    d[f"昨收价{suffix}"] = d.groupby("证券代码", sort=False)[close_adj].shift(1)
    ca = pd.to_numeric(d[close_adj], errors="coerce")
    pa = pd.to_numeric(d[f"昨收价{suffix}"], errors="coerce")
    d[f"涨跌额{suffix}"] = (ca - pa).round(4)
    pct = (ca - pa) / pa * 100
    pct = pct.replace([float("inf"), float("-inf")], pd.NA)
    d[f"涨跌幅{suffix}"] = pct.round(4)

    drop_cols = ["开盘价", "最高价", "最低价", "收盘价", "昨收价", "涨跌额", "涨跌幅", "_dt", "_f", "_f_anchor"]
    d = d.drop(columns=[c for c in drop_cols if c in d.columns], errors="ignore")
    return d, None


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


def _parse_kline_body(body: dict) -> pd.DataFrame:
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


def _fetch_kline_data(url: str, headers: dict, payload: dict) -> Tuple[pd.DataFrame, Optional[str]]:
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=300)
        if r.status_code != 200:
            return pd.DataFrame(), r.text
        body = r.json()
    except Exception as e:
        return pd.DataFrame(), str(e)

    data = _parse_kline_body(body)
    if data.empty:
        return pd.DataFrame(), "未找到行情数据"
    return data, None


def quote_data(
    securities: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 5000,
    all_market: bool = False,
    data_type: str = "daily",
    adjust_mode: Optional[str] = None,
):
    usage: dict = {}
    if GTS_AUTHORIZATION is None:
        return format_response(
            {"state": "error", "message": "未配置 gangtise 授权，无法调用 open 接口", "data": [], "usage": usage},
            "quote",
        )

    headers = {"Authorization": GTS_AUTHORIZATION}
    data_type = (data_type or "daily").strip().lower()
    if data_type not in {"daily", "minute"}:
        return format_response(
            {"state": "error", "message": "type 仅支持 daily 或 minute", "data": [], "usage": usage},
            "quote",
        )
    if data_type == "minute":
        if adjust_mode is not None and normalize_adjust_mode(adjust_mode) != "none":
            return format_response(
                {
                    "state": "error",
                    "message": "分钟 K 不支持复权调整，请使用 type=daily（日 K）",
                    "data": [],
                    "usage": usage,
                },
                "quote",
            )
        adj_mode = "none"
    else:
        adj_mode = normalize_adjust_mode(adjust_mode)

    if not end_date:
        end_date = date.today().strftime("%Y-%m-%d")
    if not start_date:
        start_date = date.today().strftime("%Y-%m-%d")

    security_list: Optional[List[str]] = None
    if not all_market:
        codes: List[str] = []
        if securities:
            for s in securities:
                c = _normalize_security_code(s)
                if c:
                    codes.append(c)
        if not codes:
            return format_response(
                {
                    "state": "error",
                    "message": "未找到有效证券代码，请仅输入完整代码（如 600519.SH），或使用 --all-market",
                    "data": [],
                    "usage": usage,
                },
                "quote",
            )
        security_list = codes
    else:
        security_list = ["all"]

    data_parts: List[pd.DataFrame] = []
    request_errors: List[str] = []
    request_markets: List[str] = []
    capped_limit = min(limit, 10000)
    extra_notes: List[str] = []

    if data_type == "daily":
        payload: dict = {
            "startDate": start_date,
            "endDate": end_date,
            "limit": capped_limit,
            "fieldList": list(_FIELD_LIST),
        }
        if security_list is not None:
            payload["securityList"] = security_list

        # 股票代码包含 .HK 时，按文档走港股接口；其余代码走原有接口
        if all_market:
            data_a, err_a = _fetch_kline_data(QUOTE_URL, headers, payload)
            if err_a:
                request_errors.append(f"A股接口请求失败: {err_a}")
            elif not data_a.empty:
                data_parts.append(data_a)
                request_markets.append("A股")
        else:
            hk_codes = [c for c in (security_list or []) if c.upper().endswith(".HK")]
            other_codes = [c for c in (security_list or []) if not c.upper().endswith(".HK")]

            if other_codes:
                payload_a = dict(payload)
                payload_a["securityList"] = other_codes
                data_a, err_a = _fetch_kline_data(QUOTE_URL, headers, payload_a)
                if err_a:
                    request_errors.append(f"A股接口请求失败: {err_a}")
                elif not data_a.empty:
                    data_parts.append(data_a)
                    request_markets.append("A股")

            if hk_codes:
                payload_hk = dict(payload)
                payload_hk["securityList"] = hk_codes
                data_hk, err_hk = _fetch_kline_data(QUOTE_HK_URL, headers, payload_hk)
                if err_hk:
                    request_errors.append(f"港股接口请求失败: {err_hk}")
                elif not data_hk.empty:
                    data_parts.append(data_hk)
                    request_markets.append("港股")
    else:
        if all_market:
            return format_response(
                {
                    "state": "error",
                    "message": "minute 类型不支持 --all-market，请指定 --securities / --securities-file",
                    "data": [],
                    "usage": usage,
                },
                "quote",
            )
        # 分钟接口仅支持 securityCode 单值；这里对 securities 并发请求再聚合。
        minute_codes = list(dict.fromkeys(security_list or []))
        if not minute_codes:
            return format_response(
                {"state": "error", "message": "minute 类型未找到有效证券代码", "data": [], "usage": usage},
                "quote",
            )

        def _fetch_one_minute(code: str) -> Tuple[str, pd.DataFrame, Optional[str]]:
            payload_one = {
                "securityCode": code,
                "startTime": start_date,
                "endTime": end_date,
                "limit": capped_limit,
                "fieldList": list(MINUTE_FIELD_LIST),
            }
            data_one, err_one = _fetch_kline_data(QUOTE_MINUTE_URL, headers, payload_one)
            return code, data_one, err_one

        max_workers = min(8, max(1, len(minute_codes)))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_fetch_one_minute, code) for code in minute_codes]
            for fut in as_completed(futures):
                code, data_one, err_one = fut.result()
                if err_one:
                    request_errors.append(f"{code} 请求失败: {err_one}")
                elif not data_one.empty:
                    data_parts.append(data_one)
                    request_markets.append(code)

    if not data_parts:
        error_message = "；".join(request_errors) if request_errors else "未找到行情数据"
        return format_response(
            {"state": "error", "message": error_message, "data": [], "usage": usage},
            "quote",
        )

    data = pd.concat(data_parts, ignore_index=True)

    field_map = API_FIELD_TO_CN if data_type == "daily" else MINUTE_API_FIELD_TO_CN
    rename_map = {k: v for k, v in field_map.items() if k in data.columns}
    data = data.rename(columns=rename_map)

    if "证券代码" in data.columns:
        data["证券简称"] = data["证券代码"].astype(str)
    else:
        data["证券简称"] = ""

    if "日期" in data.columns:
        if data_type == "minute":
            data["日期"] = pd.to_datetime(data["日期"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data["日期"] = pd.to_datetime(data["日期"], errors="coerce").dt.strftime("%Y-%m-%d")
    if start_date:
        sd = pd.to_datetime(start_date, errors="coerce")
        data = data[pd.to_datetime(data["日期"], errors="coerce") >= sd]
    if end_date:
        ed = pd.to_datetime(end_date, errors="coerce")
        data = data[pd.to_datetime(data["日期"], errors="coerce") <= ed]
    if "日期" in data.columns:
        data = data.dropna(subset=["日期"])

    if data.empty:
        return format_response(
            {"state": "error", "message": "日期范围内未找到行情数据", "data": [], "usage": usage},
            "quote",
        )

    if data_type == "daily" and adj_mode != "none":
        fac_codes = security_list if security_list is not None else ["all"]
        factors, fac_warn = fetch_adjust_factors_batched(
            headers, fac_codes, start_date, end_date, capped_limit
        )
        if fac_warn:
            extra_notes.append(f"复权因子接口：{fac_warn}")
        data, adj_err = _apply_daily_adjust_with_factors(data, factors, adj_mode)
        if adj_err:
            return format_response(
                {"state": "error", "message": adj_err, "data": [], "usage": usage},
                "quote",
            )

    preferred = [
        "证券简称",
        "证券代码",
        "日期",
        "开盘价",
        "最高价",
        "最低价",
        "收盘价",
        "昨收价",
        "涨跌额",
        "涨跌幅",
        "成交量",
        "成交额",
    ]
    if data_type == "daily" and adj_mode != "none":
        sfx = _adj_price_suffix(adj_mode)
        preferred = [
            "证券简称",
            "证券代码",
            "日期",
            f"开盘价{sfx}",
            f"最高价{sfx}",
            f"最低价{sfx}",
            f"收盘价{sfx}",
            f"昨收价{sfx}",
            f"涨跌额{sfx}",
            f"涨跌幅{sfx}",
            "成交量",
            "成交额",
        ]
    if data_type == "minute":
        preferred = [c for c in preferred if c not in {"昨收价"}]
    cols = [c for c in preferred if c in data.columns]
    cols += [c for c in data.columns if c not in cols]
    data = data[cols]

    if "证券代码" in data.columns and "日期" in data.columns:
        data = data.sort_values(
            by=["证券代码", "日期"],
            ascending=[True, False],
        ).reset_index(drop=True)
    elif "日期" in data.columns:
        data = data.sort_values(by=["日期"], ascending=[False]).reset_index(drop=True)

    col_map = {
        "证券简称": "security_abbr",
        "证券代码": "security_code",
        "日期": "date",
    }
    for col in list(data.columns):
        if col in col_map:
            data.rename(columns={col: col_map[col]}, inplace=True)
    front_columns = ["security_abbr", "security_code", "date"]
    columns = [c for c in front_columns if c in data.columns] + [
        c for c in data.columns if c not in front_columns
    ]
    data = data[columns]
    data = data.drop(columns=["security_abbr"])

    k_label = "日K" if data_type == "daily" else "分钟K"
    if all_market:
        title = f"全市场（或未指定证券）{k_label}行情数据"
    elif security_list and len(security_list) > 1:
        title = f"{security_list[0]}等{len(security_list)}只证券{k_label}行情数据"
    elif security_list and len(security_list) == 1:
        title = f"{security_list[0]}{k_label}行情数据"
    else:
        title = f"{k_label}行情数据"
    if request_markets:
        if data_type == "daily":
            title = f"{title}（{'+'.join(request_markets)}）"

    if data_type == "daily":
        adj_title = {"none": "不复权", "forward": "前复权", "backward": "后复权"}[adj_mode]
        title = f"{title}·{adj_title}"

    msg = f"已找到{title}"
    if extra_notes:
        msg += "\n" + "\n".join(extra_notes)

    parts = [
        {
            "data": data.to_dict(orient="records"),
            "module": "quote",
            "type": "data",
        }
    ]
    return format_response(
        {
            "state": "success",
            "message": msg,
            "data": parts,
            "usage": usage,
        },
        "quote",
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
        description="查询 A/港股历史 K 线（type=daily/minute）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    today_str = date.today().strftime("%Y-%m-%d")
    parser.add_argument("-sd", "--start-date", default=today_str, help="开始日期 yyyy-MM-dd")
    parser.add_argument("-ed", "--end-date", default=today_str, help="结束日期 yyyy-MM-dd")
    parser.add_argument(
        "--securities",
        default=None,
        help="证券代码逗号分隔（完整代码如 600519.SH）；与 --all-market 二选一",
    )
    parser.add_argument(
        "--securities-file",
        default=None,
        help="csv 须含 security_code 列",
    )
    parser.add_argument(
        "--all-market",
        action="store_true",
        help="不传 securityList，按接口约定拉全市场（数据量可能极大，请配合日期区间与 limit）",
    )
    parser.add_argument("--limit", type=int, default=5000, help="单次请求最大行数（上限 10000）")
    parser.add_argument(
        "--type",
        dest="data_type",
        choices=["daily", "minute"],
        default="daily",
        help="K线类型：daily（日K）或 minute（分钟K，仅A股且不支持all-market）",
    )
    parser.add_argument(
        "--adjust",
        default=None,
        help="复权方式（仅日 K）：forward/qfq/前复权（默认）、backward/hfq/后复权、none/raw/不复权",
    )
    args = parser.parse_args()

    if args.all_market and (args.securities or args.securities_file):
        parser.error("--all-market 时不要使用 --securities / --securities-file")
    if args.data_type == "minute" and args.all_market:
        parser.error("minute 类型不支持 --all-market，请指定 --securities / --securities-file")

    securities: Optional[List[str]] = None
    if args.securities:
        securities = [x.strip() for x in args.securities.replace("，", ",").split(",") if x.strip()]
    if not securities and args.securities_file:
        try:
            securities = _load_security_codes_from_file(args.securities_file)
        except Exception as e:
            print(f"根据证券文件解析证券失败: {e}")
            sys.exit(1)

    if not args.all_market and not securities:
        parser.error("请指定 --securities / --securities-file，或使用 --all-market")

    out = quote_data(
        securities=securities,
        start_date=args.start_date,
        end_date=args.end_date,
        limit=args.limit,
        all_market=args.all_market,
        data_type=args.data_type,
        adjust_mode=args.adjust,
    )
    print(out)


if __name__ == "__main__":
    encoding = "utf-8"
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding=encoding, errors="ignore")
    main()
