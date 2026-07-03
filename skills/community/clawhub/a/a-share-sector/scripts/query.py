#!/usr/bin/env python3
"""A股板块行情查询工具 — 数据来源：东方财富（经 akshare）"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime


def ensure_akshare() -> None:
    clear_proxy_env()
    try:
        import akshare  # noqa: F401
    except ImportError:
        print("正在安装依赖 akshare pandas ...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "akshare", "pandas", "-q"]
        )


def clear_proxy_env() -> None:
    """避免本地代理导致东方财富接口 403。"""
    import os

    for key in list(os.environ.keys()):
        if "proxy" in key.lower():
            del os.environ[key]


def fmt_money(value: float) -> str:
    if value is None or (isinstance(value, float) and value != value):
        return "-"
    value = float(value)
    sign = "+" if value > 0 else ""
    av = abs(value)
    if av >= 1e8:
        return f"{sign}{value / 1e8:.2f}亿"
    if av >= 1e4:
        return f"{sign}{value / 1e4:.2f}万"
    return f"{sign}{value:.0f}"


def fmt_volume(hands: float) -> str:
    if hands is None or (isinstance(hands, float) and hands != hands):
        return "-"
    hands = float(hands)
    if hands >= 1e8:
        return f"{hands / 1e8:.2f}亿手"
    if hands >= 1e4:
        return f"{hands / 1e4:.2f}万手"
    return f"{hands:.0f}手"


def fmt_pct(value: float) -> str:
    if value is None or (isinstance(value, float) and value != value):
        return "-"
    return f"{float(value):+.2f}%"


def flow_label(value: float) -> str:
    if value is None or (isinstance(value, float) and value != value):
        return "-"
    if value > 0:
        return f"流入 {fmt_money(value)}"
    if value < 0:
        return f"流出 {fmt_money(abs(value))}"
    return "持平"


def split_main_flow(net: float | None) -> tuple[float | None, float | None]:
    """将主力净流入拆成流入、流出（东方财富接口仅提供净值）。"""
    if net is None or (isinstance(net, float) and net != net):
        return None, None
    net = float(net)
    if net > 0:
        return net, None
    if net < 0:
        return None, abs(net)
    return None, None


def fmt_flow_in(value: float | None) -> str:
    if value is None or (isinstance(value, float) and value != value):
        return "-"
    return fmt_money(value)


def fmt_flow_out(value: float | None) -> str:
    if value is None or (isinstance(value, float) and value != value):
        return "-"
    return fmt_money(value)


def filter_by_iso_date(df, iso_date: str):
    """按 YYYY-MM-DD 过滤行情/资金流 DataFrame（兼容 str 与 date 类型）。"""
    import pandas as pd

    if df is None or df.empty:
        return df
    dates = pd.to_datetime(df["日期"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df[dates == iso_date]


def parse_date(date_str: str | None) -> tuple[str | None, str | None]:
    """解析日期，返回 (YYYY-MM-DD, YYYYMMDD)；None 表示查当天实时数据。"""
    if not date_str:
        return None, None
    raw = date_str.strip()
    if re.fullmatch(r"\d{8}", raw):
        iso = f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
        return iso, raw
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return raw, raw.replace("-", "")
    raise SystemExit(f"日期格式无效：{date_str}，请使用 YYYY-MM-DD 或 YYYYMMDD")


def is_today(iso_date: str) -> bool:
    return iso_date == date.today().isoformat()


def board_type_to_sector_type(board_type: str) -> str:
    mapping = {
        "industry": "行业资金流",
        "concept": "概念资金流",
        "region": "地域资金流",
    }
    return mapping[board_type]


def fetch_board_spot(board_type: str):
    import akshare as ak

    if board_type == "industry":
        return ak.stock_board_industry_name_em()
    if board_type == "concept":
        return ak.stock_board_concept_name_em()
    raise ValueError(f"板块类型 {board_type} 暂无实时行情列表，请用 fund-flow 命令")


def fetch_board_fund_flow(board_type: str, indicator: str = "今日"):
    import akshare as ak

    sector_type = board_type_to_sector_type(board_type)
    return ak.stock_sector_fund_flow_rank(indicator=indicator, sector_type=sector_type)


def fetch_stock_fund_flow(indicator: str = "今日"):
    import akshare as ak

    return ak.stock_individual_fund_flow_rank(indicator=indicator)


def resolve_board_name(boards_df, name: str) -> str:
    if name in boards_df["板块名称"].values:
        return name
    matched = boards_df[boards_df["板块名称"].str.contains(name, na=False)]
    if matched.empty:
        raise SystemExit(f"未找到板块「{name}」，请检查名称或使用 list 命令查看")
    if len(matched) > 1:
        print("匹配到多个板块，使用第一个：")
        for row in matched.head(5).itertuples():
            print(f"  - {row.板块名称}")
    return matched.iloc[0]["板块名称"]


def fetch_board_stocks(board_type: str, board_name: str):
    import akshare as ak

    if board_type == "industry":
        return ak.stock_board_industry_cons_em(symbol=board_name)
    if board_type == "concept":
        return ak.stock_board_concept_cons_em(symbol=board_name)
    raise ValueError(f"暂不支持 {board_type} 类型的成份股查询")


def stock_market(code: str) -> str:
    code = str(code).zfill(6)
    if code.startswith(("6", "5", "9")):
        return "sh"
    return "sz"


def fetch_stock_hist_flow(code: str, iso_date: str) -> dict | None:
    """获取个股在指定日期的主力资金流（净流入及流入/流出拆分）。"""
    import akshare as ak

    try:
        df = ak.stock_individual_fund_flow(stock=str(code).zfill(6), market=stock_market(code))
    except Exception:
        return None
    if df is None or df.empty:
        return None
    row = filter_by_iso_date(df, iso_date)
    if row.empty:
        return None
    flow_col = next((c for c in df.columns if "主力净流入" in c and "净额" in c), None)
    if not flow_col:
        return None
    net = float(row.iloc[0][flow_col])
    inflow, outflow = split_main_flow(net)
    return {"主力净流入": net, "主力流入": inflow, "主力流出": outflow}


def fetch_stock_day(
    code: str,
    name: str,
    iso_date: str,
    compact_date: str,
    *,
    with_flow: bool = False,
) -> dict | None:
    """获取单只股票在指定日期的行情。"""
    import akshare as ak
    import pandas as pd

    code = str(code).zfill(6)
    try:
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=compact_date,
            end_date=compact_date,
            adjust="",
        )
    except Exception:
        return None
    if df is None or df.empty:
        return None

    row = filter_by_iso_date(df, iso_date)
    if row.empty:
        row = df.iloc[[-1]]
        if str(row.iloc[0]["日期"]) != iso_date and pd.to_datetime(row.iloc[0]["日期"]).strftime("%Y-%m-%d") != iso_date:
            return None
    row = row.iloc[0]

    turnover = row["换手率"] if "换手率" in row.index else None
    flow_data = fetch_stock_hist_flow(code, iso_date) if with_flow else None
    result = {
        "代码": code,
        "名称": name,
        "涨跌幅": float(row["涨跌幅"]),
        "最新价": float(row["收盘"]),
        "成交量": float(row["成交量"]),
        "成交额": float(row["成交额"]),
        "换手率": float(turnover) if turnover == turnover else None,
        "主力净流入": None,
        "主力流入": None,
        "主力流出": None,
    }
    if flow_data:
        result.update(flow_data)
    return result


def fetch_board_stocks_hist(
    board_type: str,
    board_name: str,
    iso_date: str,
    compact_date: str,
    *,
    with_flow: bool = False,
    workers: int = 8,
) -> list[dict]:
    stocks_df = fetch_board_stocks(board_type, board_name)
    codes = stocks_df["代码"].astype(str).str.zfill(6).tolist()
    names = dict(zip(stocks_df["代码"].astype(str).str.zfill(6), stocks_df["名称"]))
    total = len(codes)
    print(f"正在查询 {board_name} 共 {total} 只成份股 ({iso_date})...", file=sys.stderr)

    results: list[dict] = []
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(fetch_stock_day, c, names.get(c, ""), iso_date, compact_date, with_flow=with_flow): c
            for c in codes
        }
        for fut in as_completed(futs):
            done += 1
            if done % 20 == 0 or done == total:
                print(f"  进度 {done}/{total}", file=sys.stderr)
            item = fut.result()
            if item is not None:
                results.append(item)
    return results


def fetch_board_hist_row(board_type: str, board_name: str, iso_date: str, compact_date: str):
    """获取单个板块在指定日期的历史行情行。"""
    import akshare as ak
    import pandas as pd

    if board_type == "industry":
        df = ak.stock_board_industry_hist_em(
            symbol=board_name,
            period="日k",
            start_date=compact_date,
            end_date=compact_date,
            adjust="",
        )
    elif board_type == "concept":
        df = ak.stock_board_concept_hist_em(
            symbol=board_name,
            period="daily",
            start_date=compact_date,
            end_date=compact_date,
            adjust="",
        )
    else:
        return None

    if df is None or df.empty:
        return None

    row = filter_by_iso_date(df, iso_date)
    if row.empty:
        row = df.iloc[[-1]]
        last_date = pd.to_datetime(row.iloc[0]["日期"]).strftime("%Y-%m-%d")
        if last_date != iso_date:
            return None
    return row.iloc[0]


def fetch_board_hist_flow(board_name: str, iso_date: str) -> dict | None:
    """获取单个板块在指定日期的主力资金流。"""
    import akshare as ak

    try:
        df = ak.stock_sector_fund_flow_hist(symbol=board_name)
    except Exception:
        return None
    if df is None or df.empty:
        return None
    row = filter_by_iso_date(df, iso_date)
    if row.empty:
        return None
    flow_col = next((c for c in df.columns if "主力净流入" in c and "净额" in c), None)
    if not flow_col:
        return None
    net = float(row.iloc[0][flow_col])
    inflow, outflow = split_main_flow(net)
    return {"主力净流入": net, "主力流入": inflow, "主力流出": outflow}


def apply_flow_fields(row: dict, net: float | None) -> None:
    inflow, outflow = split_main_flow(net)
    row["主力净流入"] = net
    row["主力流入"] = inflow
    row["主力流出"] = outflow


def fetch_boards_hist(
    board_type: str,
    iso_date: str,
    compact_date: str,
    *,
    with_flow: bool = False,
    workers: int = 8,
) -> list[dict]:
    spot_df = fetch_board_spot(board_type)
    names = spot_df["板块名称"].tolist()
    total = len(names)
    print(f"正在查询 {iso_date} 共 {total} 个板块...", file=sys.stderr)

    def _fetch(name: str) -> dict | None:
        row = fetch_board_hist_row(board_type, name, iso_date, compact_date)
        if row is None:
            return None
        item = {
            "板块": name,
            "涨跌幅": float(row["涨跌幅"]),
            "成交量": float(row["成交量"]),
            "成交额": float(row["成交额"]),
            "主力净流入": None,
            "主力流入": None,
            "主力流出": None,
        }
        if with_flow:
            flow = fetch_board_hist_flow(name, iso_date)
            if flow:
                item.update(flow)
        return item

    results: list[dict] = []
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_fetch, n): n for n in names}
        for fut in as_completed(futs):
            done += 1
            if done % 100 == 0 or done == total:
                print(f"  进度 {done}/{total}", file=sys.stderr)
            item = fut.result()
            if item is not None:
                results.append(item)
    return results


def ensure_realtime_only(args, command: str) -> None:
    iso_date, _ = parse_date(getattr(args, "date", None))
    if iso_date and not is_today(iso_date):
        raise SystemExit(
            f"{command} 命令暂不支持历史日期查询，请去掉 --date 或使用 overview / fund-flow。"
        )


def print_overview_table(title: str, df, *, show_flow: bool) -> None:
    print(f"## {title}")
    if show_flow:
        print("| 板块 | 涨跌幅 | 成交量 | 主力流入 | 主力流出 |")
        print("| --- | ---: | ---: | ---: | ---: |")
    else:
        print("| 板块 | 涨跌幅 | 成交量 |")
        print("| --- | ---: | ---: |")

    for _, r in df.iterrows():
        vol = fmt_volume(r.get("成交量"))
        if show_flow:
            print(
                f"| {r['板块']} | {fmt_pct(r['涨跌幅'])} | {vol} | "
                f"{fmt_flow_in(r.get('主力流入'))} | {fmt_flow_out(r.get('主力流出'))} |"
            )
        else:
            print(f"| {r['板块']} | {fmt_pct(r['涨跌幅'])} | {vol} |")


def cmd_overview(args) -> None:
    import pandas as pd

    iso_date, compact_date = parse_date(args.date)
    board_label = {"industry": "行业", "concept": "概念", "region": "地域"}[args.type]

    if iso_date and not is_today(iso_date):
        if args.type == "region":
            raise SystemExit("地域板块暂不支持历史日期查询，请使用 --type industry 或 concept")

        rows = fetch_boards_hist(
            args.type,
            iso_date,
            compact_date,
            with_flow=not args.no_flow,
            workers=args.workers,
        )
        if not rows:
            raise SystemExit(f"{iso_date} 无板块数据，可能为非交易日或数据尚未入库")

        print(f"# A股{board_label}板块概览 ({iso_date})")
        print()

        df = pd.DataFrame(rows).sort_values("涨跌幅", ascending=False, na_position="last")
        gainers = df[df["涨跌幅"] > 0]
        losers = df[df["涨跌幅"] < 0].sort_values("涨跌幅")
        flat = df[df["涨跌幅"] == 0]

        print(f"**统计**：共 {len(df)} 个板块，上涨 {len(gainers)} | 下跌 {len(losers)} | 平盘 {len(flat)}")
        print()

        if args.gainers_only:
            print_overview_table(f"上涨板块（共 {len(gainers)} 个）", gainers, show_flow=not args.no_flow)
        else:
            print_overview_table(f"涨幅前 {args.top}", df.head(args.top), show_flow=not args.no_flow)
            print()
            print_overview_table(f"跌幅前 {args.top}", df.tail(args.top).sort_values("涨跌幅"), show_flow=not args.no_flow)

        if args.no_flow:
            print()
            print("> 已跳过主力流入/流出；去掉 `--no-flow` 可查询资金流（更慢）。")
        else:
            print()
            print("> 主力流入/流出由「主力净流入」拆分；东方财富接口仅提供净值。")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"# A股{board_label}板块概览 ({now})")
    print()

    spot_df = fetch_board_spot(args.type)
    flow_df = fetch_board_fund_flow(args.type, args.period)

    name_col = "名称" if "名称" in flow_df.columns else flow_df.columns[1]
    flow_col = "今日主力净流入-净额" if "今日主力净流入-净额" in flow_df.columns else "主力净流入-净额"
    pct_col = "今日涨跌幅" if "今日涨跌幅" in flow_df.columns else None

    flow_map = dict(zip(flow_df[name_col], flow_df[flow_col]))
    pct_map = (
        dict(zip(flow_df[name_col], flow_df[pct_col])) if pct_col and pct_col in flow_df.columns else {}
    )

    rows = []
    for _, row in spot_df.iterrows():
        name = row["板块名称"]
        change = row.get("涨跌幅")
        if change is None or (isinstance(change, float) and change != change):
            change = pct_map.get(name)
        net = flow_map.get(name)
        item = {
            "板块": name,
            "涨跌幅": change,
            "成交量": None,
            "主力净流入": net,
            "主力流入": None,
            "主力流出": None,
        }
        apply_flow_fields(item, net)
        rows.append(item)

    df = pd.DataFrame(rows)
    df = df.sort_values("涨跌幅", ascending=False, na_position="last")

    if args.gainers_only:
        gainers = df[df["涨跌幅"] > 0]
        print_overview_table(f"上涨板块（共 {len(gainers)} 个）", gainers, show_flow=True)
        print()
        print("> 实时板块列表不含成交量；主力流入/流出由当日主力净流入拆分。")
        return

    gainers = df.head(args.top)
    losers = df.tail(args.top).sort_values("涨跌幅")

    print_overview_table(f"涨幅前 {args.top}", gainers, show_flow=True)
    print()
    print_overview_table(f"跌幅前 {args.top}", losers, show_flow=True)
    print()
    print("> 实时板块列表不含成交量；主力流入/流出由当日主力净流入拆分。")


def print_stock_table(df, *, show_flow: bool, price_label: str = "最新价") -> None:
    import pandas as pd

    if show_flow:
        print(
            f"| 代码 | 名称 | 涨跌幅 | {price_label} | 成交量 | 成交额 | 换手率 | "
            f"主力流入 | 主力流出 |"
        )
        print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    else:
        print(f"| 代码 | 名称 | 涨跌幅 | {price_label} | 成交量 | 成交额 | 换手率 |")
        print("| --- | --- | ---: | ---: | ---: | ---: | ---: |")

    for _, r in df.iterrows():
        turnover = r.get("换手率")
        turnover_str = f"{float(turnover):.2f}%" if pd.notna(turnover) else "-"
        price = r.get("最新价")
        price_str = f"{float(price):.2f}" if pd.notna(price) else "-"
        amount = r.get("成交额")
        amount_str = fmt_money(amount) if pd.notna(amount) else "-"
        line = (
            f"| {r['代码']} | {r['名称']} | {fmt_pct(r['涨跌幅'])} | {price_str} | "
            f"{fmt_volume(r['成交量'])} | {amount_str} | {turnover_str}"
        )
        if show_flow:
            line += f" | {fmt_flow_in(r.get('主力流入'))} | {fmt_flow_out(r.get('主力流出'))} |"
        print(line)


def sort_detail_df(df, sort_key: str):
    sort_cols = {
        "change": "涨跌幅",
        "volume": "成交量",
        "turnover": "换手率",
        "flow": "主力净流入",
        "amount": "成交额",
    }
    col = sort_cols[sort_key]
    return df.sort_values(col, ascending=False, na_position="last")


def cmd_detail(args) -> None:
    import pandas as pd

    iso_date, compact_date = parse_date(args.date)
    boards_df = fetch_board_spot(args.type)
    board_name = resolve_board_name(boards_df, args.name)

    if iso_date and not is_today(iso_date):
        if args.type == "region":
            raise SystemExit("地域板块暂不支持历史日期查询，请使用 --type industry 或 concept")

        rows = fetch_board_stocks_hist(
            args.type,
            board_name,
            iso_date,
            compact_date,
            with_flow=not args.no_flow,
            workers=args.workers,
        )
        if not rows:
            raise SystemExit(f"{iso_date} 无成份股数据，可能为非交易日或板块成分为空")

        print(f"# {board_name} 成份股 ({iso_date})")
        print()
        print("> 历史成份股按当前板块成分回溯，与当日实际成分可能略有差异。")
        print()

        df = pd.DataFrame(rows)
        show_flow = not args.no_flow

        if args.hot:
            gainers = df[df["涨跌幅"] > 0]
            by_gain = sort_detail_df(gainers if args.gainers_only else df, "change").head(args.limit)
            by_amount = sort_detail_df(gainers, "amount").head(args.limit)

            print(f"## 涨幅前列（前 {args.limit}）")
            print_stock_table(by_gain, show_flow=show_flow, price_label="收盘价")
            print()
            print(f"## 资金活跃（上涨股中成交额前 {args.limit}）")
            print_stock_table(by_amount, show_flow=show_flow, price_label="收盘价")
            if args.no_flow:
                print()
                print("> 已跳过主力流入/流出；去掉 `--no-flow` 可查询资金流（更慢）。")
            else:
                print()
                print("> 主力流入/流出由「主力净流入」拆分；东方财富接口仅提供净值。")
            return

        if args.gainers_only:
            df = df[df["涨跌幅"] > 0]

        df = sort_detail_df(df, args.sort)
        if args.limit:
            df = df.head(args.limit)

        sort_label = {
            "change": "涨跌幅",
            "volume": "成交量",
            "turnover": "换手率",
            "flow": "主力净流入",
            "amount": "成交额",
        }[args.sort]
        title = f"## 按{sort_label}排序"
        if args.gainers_only:
            title += "（仅上涨）"
        print(title)
        print_stock_table(df, show_flow=show_flow, price_label="收盘价")
        if args.no_flow:
            print()
            print("> 已跳过主力流入/流出；去掉 `--no-flow` 可查询资金流（更慢）。")
        else:
            print()
            print("> 主力流入/流出由「主力净流入」拆分；东方财富接口仅提供净值。")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"# {board_name} 成份股 ({now})")
    print()

    stocks_df = fetch_board_stocks(args.type, board_name)
    flow_df = fetch_stock_fund_flow(args.period)

    code_col = "代码" if "代码" in flow_df.columns else flow_df.columns[1]
    main_flow_col = None
    for col in flow_df.columns:
        if "主力净流入" in col and "净额" in col:
            main_flow_col = col
            break
    flow_map = dict(zip(flow_df[code_col].astype(str).str.zfill(6), flow_df[main_flow_col])) if main_flow_col else {}

    rows = []
    for _, row in stocks_df.iterrows():
        code = str(row["代码"]).zfill(6)
        net = flow_map.get(code)
        item = {
            "代码": code,
            "名称": row["名称"],
            "涨跌幅": row.get("涨跌幅"),
            "最新价": row.get("最新价"),
            "成交量": row.get("成交量"),
            "成交额": row.get("成交额"),
            "换手率": row.get("换手率"),
            "主力净流入": net,
            "主力流入": None,
            "主力流出": None,
        }
        apply_flow_fields(item, net)
        rows.append(item)

    df = pd.DataFrame(rows)
    if "成交额" not in df.columns or df["成交额"].isna().all():
        df["成交额"] = df["成交量"]
    show_flow = not args.no_flow

    if args.hot:
        gainers = df[df["涨跌幅"] > 0]
        by_gain = sort_detail_df(gainers if args.gainers_only else df, "change").head(args.limit)
        by_amount = sort_detail_df(gainers, "amount").head(args.limit)
        print(f"## 涨幅前列（前 {args.limit}）")
        print_stock_table(by_gain, show_flow=show_flow)
        print()
        print(f"## 资金活跃（上涨股中成交额前 {args.limit}）")
        print_stock_table(by_amount, show_flow=show_flow)
        return

    if args.gainers_only:
        df = df[df["涨跌幅"] > 0]

    df = sort_detail_df(df, args.sort)
    if args.limit:
        df = df.head(args.limit)

    print_stock_table(df, show_flow=show_flow)


def cmd_list(args) -> None:
    ensure_realtime_only(args, "list")
    spot_df = fetch_board_spot(args.type)
    print(f"共 {len(spot_df)} 个板块：")
    for name in spot_df["板块名称"].tolist():
        print(f"  - {name}")


def cmd_fund_flow(args) -> None:
    import pandas as pd

    iso_date, compact_date = parse_date(args.date)
    board_label = {"industry": "行业", "concept": "概念", "region": "地域"}[args.type]

    if iso_date and not is_today(iso_date):
        if args.type == "region":
            raise SystemExit("地域板块暂不支持历史日期查询，请使用 --type industry 或 concept")

        print(f"# A股{board_label}板块资金流 ({iso_date})")
        print()
        rows = fetch_boards_hist(
            args.type,
            iso_date,
            compact_date,
            with_flow=True,
            workers=args.workers,
        )
        if not rows:
            raise SystemExit(f"{iso_date} 无板块数据，可能为非交易日或数据尚未入库")

        df = pd.DataFrame(rows).dropna(subset=["主力净流入"])
        df = df.sort_values("主力净流入", ascending=False)
        inflow = df.head(args.top)
        outflow = df.tail(args.top).sort_values("主力净流入")

        print(f"## 主力净流入前 {args.top}")
        print("| 板块 | 涨跌幅 | 成交量 | 主力流入 | 主力流出 |")
        print("| --- | ---: | ---: | ---: | ---: |")
        for _, r in inflow.iterrows():
            print(
                f"| {r['板块']} | {fmt_pct(r['涨跌幅'])} | {fmt_volume(r.get('成交量'))} | "
                f"{fmt_flow_in(r.get('主力流入'))} | {fmt_flow_out(r.get('主力流出'))} |"
            )

        print()
        print(f"## 主力净流出前 {args.top}")
        print("| 板块 | 涨跌幅 | 成交量 | 主力流入 | 主力流出 |")
        print("| --- | ---: | ---: | ---: | ---: |")
        for _, r in outflow.iterrows():
            print(
                f"| {r['板块']} | {fmt_pct(r['涨跌幅'])} | {fmt_volume(r.get('成交量'))} | "
                f"{fmt_flow_in(r.get('主力流入'))} | {fmt_flow_out(r.get('主力流出'))} |"
            )
        print()
        print("> 主力流入/流出由「主力净流入」拆分；东方财富接口仅提供净值。")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    flow_df = fetch_board_fund_flow(args.type, args.period)

    name_col = "名称" if "名称" in flow_df.columns else flow_df.columns[1]
    flow_col = next((c for c in flow_df.columns if "主力净流入" in c and "净额" in c), None)
    if not flow_col:
        raise SystemExit("无法识别资金流列，接口可能已变更")

    df = flow_df.sort_values(flow_col, ascending=False)
    inflow = df.head(args.top)
    outflow = df.tail(args.top).sort_values(flow_col)

    print(f"# A股{board_label}板块资金流 ({args.period}, {now})")
    print()
    print(f"## 主力净流入前 {args.top}")
    print("| 板块 | 涨跌幅 | 主力流入 | 主力流出 |")
    print("| --- | ---: | ---: | ---: |")
    for _, r in inflow.iterrows():
        net = r[flow_col]
        inf, outf = split_main_flow(net)
        pct = r.get("今日涨跌幅", r.get("涨跌幅"))
        pct_str = fmt_pct(pct) if pct == pct else "-"
        print(
            f"| {r[name_col]} | {pct_str} | {fmt_flow_in(inf)} | {fmt_flow_out(outf)} |"
        )

    print()
    print(f"## 主力净流出前 {args.top}")
    print("| 板块 | 涨跌幅 | 主力流入 | 主力流出 |")
    print("| --- | ---: | ---: | ---: |")
    for _, r in outflow.iterrows():
        net = r[flow_col]
        inf, outf = split_main_flow(net)
        pct = r.get("今日涨跌幅", r.get("涨跌幅"))
        pct_str = fmt_pct(pct) if pct == pct else "-"
        print(
            f"| {r[name_col]} | {pct_str} | {fmt_flow_in(inf)} | {fmt_flow_out(outf)} |"
        )
    print()
    print("> 主力流入/流出由「主力净流入」拆分；东方财富接口仅提供净值。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A股板块行情查询")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--type", choices=["industry", "concept", "region"], default="industry")
    common.add_argument("--period", default="今日", choices=["今日", "3日", "5日", "10日"])
    common.add_argument("--top", type=int, default=10)
    common.add_argument(
        "--date",
        metavar="DATE",
        help="指定查询日期，格式 YYYY-MM-DD 或 YYYYMMDD；省略则查当天实时",
    )
    common.add_argument("--workers", type=int, default=8, help="历史查询并发数（默认 8）")

    p_overview = sub.add_parser("overview", parents=[common], help="板块涨跌概览")
    p_overview.add_argument(
        "--gainers-only",
        action="store_true",
        help="列出全部上涨板块（默认只显示涨幅/跌幅前 N）",
    )
    p_overview.add_argument(
        "--no-flow",
        action="store_true",
        help="跳过主力流入/流出查询（更快）",
    )
    p_overview.set_defaults(func=cmd_overview)

    p_detail = sub.add_parser("detail", parents=[common], help="板块成份股详情")
    p_detail.add_argument("name", help="板块名称")
    p_detail.add_argument("--limit", type=int, default=30)
    p_detail.add_argument(
        "--sort",
        choices=["change", "volume", "turnover", "flow", "amount"],
        default="change",
        help="排序：涨跌幅/成交量/换手率/主力净流入/成交额",
    )
    p_detail.add_argument(
        "--gainers-only",
        action="store_true",
        help="仅显示上涨个股",
    )
    p_detail.add_argument(
        "--hot",
        action="store_true",
        help="同时输出「涨幅前列」与「资金活跃（上涨股成交额靠前）」",
    )
    p_detail.add_argument(
        "--no-flow",
        action="store_true",
        help="跳过主力流入/流出查询（更快）",
    )
    p_detail.set_defaults(func=cmd_detail)

    sub.add_parser("list", parents=[common], help="列出板块").set_defaults(func=cmd_list)
    sub.add_parser("fund-flow", parents=[common], help="板块资金流排行").set_defaults(func=cmd_fund_flow)

    return parser


def main() -> None:
    ensure_akshare()
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as exc:
        print(f"查询失败: {exc}", file=sys.stderr)
        print("提示：请在 A 股交易时段或收盘后重试；非交易日可能无当日数据。", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
