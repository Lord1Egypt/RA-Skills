"""CLI 入口：交互式股票行情查询"""

import sys

import cache as stock_cache
from market import is_valid_code, strip_prefix
from quote import get_detail
from search import search_by_name


def format_quote(q: dict) -> str:
    """将行情字典格式化为可读字符串"""
    change = q["涨跌幅"]
    arrow = "▲" if change >= 0 else "▼"
    mktcap = q["总市值"]
    mktcap_str = f"{mktcap / 1e8:.2f} 亿" if mktcap > 0 else "—"
    pe_str = f"{q['市盈率TTM']:.2f}" if q["市盈率TTM"] > 0 else "—"
    vol = q["成交量"]
    amt = q["成交额"]

    lines = [
        "",
        "=" * 48,
        f"  {q['名称']}  ({q['代码']})",
        "-" * 48,
        f"  最新价格: {q['最新价']:.3f} 元",
        f"  涨跌幅度: {arrow} {abs(change):.2f}%    涨跌金额: {q['涨跌额']:+.3f} 元",
        f"  今日开盘: {q['今开']:.3f}    昨日收盘: {q['昨收']:.3f}",
        f"  今日最高: {q['最高']:.3f}    今日最低: {q['最低']:.3f}",
        f"  52周最高: {q['52周最高']:.3f}    52周最低: {q['52周最低']:.3f}",
        f"  成交量:   {vol:,.0f} 手    成交额: {amt / 1e8:.2f} 亿元",
        f"  市盈率:   {pe_str}    总市值: {mktcap_str}元",
        f"  市净率:   {q['市净率']:.3f}    股息率: {q['股息率TTM']:.2f}%",
        "=" * 48,
    ]
    return "\n".join(lines)


def _run_query(user_input: str) -> None:
    user_input = user_input.strip()
    if not user_input:
        print("输入不能为空。")
        return

    if is_valid_code(user_input):
        code = strip_prefix(user_input)
        print(f"正在查询 [{code}]（数据来源：雪球）...")
        try:
            print(format_quote(get_detail(code)))
        except Exception as exc:
            print(f"查询失败: {exc}")
        return

    print(f"正在搜索「{user_input}」...")
    matches = search_by_name(user_input)
    if not matches:
        print("未找到匹配的股票，请尝试使用股票代码。")
        return

    if len(matches) == 1:
        try:
            print(format_quote(get_detail(matches[0]["code"])))
        except Exception as exc:
            print(f"查询失败: {exc}")
        return

    print(f"\n找到 {len(matches)} 只匹配的股票：")
    print(f"  {'序号':<4} {'代码':<8} 名称")
    print("-" * 32)
    for i, s in enumerate(matches, 1):
        print(f"  {i:<4} {s['code']:<8} {s['name']}")
    print()

    choice = input("请输入序号查询行情（直接回车取消）: ").strip()
    if not choice:
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(matches):
            print(format_quote(get_detail(matches[idx]["code"])))
        else:
            print("序号超出范围。")
    except ValueError:
        print("无效输入。")


def main() -> None:
    print("=" * 48)
    print("      A股实时行情查询工具（雪球 · AKShare）")
    print("  支持：6位股票代码 / 股票名称关键字")
    print("  输入 q 退出   输入 cache 查看缓存状态")
    print("=" * 48)

    if len(sys.argv) > 1:
        _run_query(" ".join(sys.argv[1:]))
        return

    while True:
        try:
            user_input = input("\n请输入股票代码或名称: ").strip()
            if user_input.lower() in ("q", "exit", "quit", "退出"):
                print("再见！")
                break
            if user_input.lower() == "cache":
                age = stock_cache.cache_age_hours()
                if age is None:
                    print("缓存文件不存在，下次搜索时自动创建。")
                else:
                    ttl = stock_cache.CACHE_TTL / 3600
                    status = "有效" if age <= ttl else f"已过期（超出 {age - ttl:.1f} 小时）"
                    print(f"缓存距今 {age:.1f} 小时，TTL {ttl:.0f} 小时，状态：{status}")
                continue
            _run_query(user_input)
        except KeyboardInterrupt:
            print("\n\n已退出。")
            break


if __name__ == "__main__":
    main()
