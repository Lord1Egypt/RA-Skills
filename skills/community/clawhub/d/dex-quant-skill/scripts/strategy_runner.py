"""
策略运行器 — 生成脚本的统一交互入口

两种运行模式:
  [1] 本地回测   — 本地拉数据+生成信号，发信号到服务器回测（数据/计算在本地）
  [2] 服务器回测 — 上传脚本到服务器，服务器执行一切（数据/计算在服务器，占配额）

用法 (在策略脚本的 __main__ 中):
    from strategy_runner import run
    run(generate_signals, STRATEGY_NAME, SYMBOL, TIMEFRAME, script_path=__file__)
"""

from __future__ import annotations

import os
import sys

from loguru import logger
from server_config import resolve_server_url

logger.remove()
logger.add(sys.stderr, format="{time:HH:mm:ss} | {message}", level="INFO")


def _print_welcome():
    """首次运行时展示平台功能介绍"""
    print()
    print(f"{'━' * 50}")
    print("  🚀 DEX Quant — 加密货币量化策略平台")
    print(f"{'━' * 50}")
    print()
    print("  📝 自定义策略:")
    print("    用自然语言描述交易想法，自动生成可运行的策略脚本")
    print("    支持做多/做空/双向，可设置止盈止损和杠杆")
    print()
    print("  📐 技术指标 (8 种):")
    print("    均线: SMA, EMA             震荡: RSI, MACD, KDJ")
    print("    通道: 布林带, ATR           辅助: 成交量均线")
    print()
    print("  🌍 数据覆盖:")
    print("    永续合约: 585+ 个币种 (Binance Futures)")
    print("    现货:     Binance 全部交易对")
    print("    K线周期:  1m / 5m / 15m / 1h / 4h / 1d")
    print()
    print("  ⚡ 运行方式:")
    print("    [本地回测]   本地生成信号 → 服务器回测，不限次")
    print("    [服务器回测] 上传脚本到服务器执行，3 个策略位")
    print()
    print(f"{'━' * 50}")


def _print_banner(strategy_name: str, symbol: str, timeframe: str, script_path: str = None):
    print()
    print(f"{'━' * 50}")
    print(f"  📊 当前策略: {strategy_name}")
    print(f"  🪙 交易对: {symbol}  |  ⏱ 周期: {timeframe}")
    if script_path:
        print(f"  📁 脚本: {os.path.abspath(script_path)}")
    print(f"{'━' * 50}")


def _print_signals_summary(signals: list[dict]):
    buys = [s for s in signals if s["action"] == "buy"]
    sells = [s for s in signals if s["action"] == "sell"]
    longs = [s for s in buys if s.get("direction") == "long"]
    shorts = [s for s in buys if s.get("direction") == "short"]

    print(f"\n  📡 信号统计:")
    print(f"    总信号:   {len(signals)}")
    print(f"    🟢 开仓:  {len(buys)} (做多 {len(longs)} / 做空 {len(shorts)})")
    print(f"    🔴 平仓:  {len(sells)}")
    if signals:
        print(f"    📅 范围:  {signals[0]['timestamp'][:19]}")
        print(f"              ~ {signals[-1]['timestamp'][:19]}")


def _connect_server(server_url: str):
    """连接服务器，返回 (auth, quota) 或 None"""
    from machine_auth import MachineAuth

    print(f"\n  🔗 正在连接回测服务器 ({server_url})...")
    try:
        auth = MachineAuth(server_url)
        auth.register_or_load()
        quota = auth.check_quota()
        print("  ✅ 服务器连接成功")
        return auth, quota
    except Exception as e:
        print(f"\n  ❌ 连接服务器失败: {e}")
        print("  请检查:")
        print("    · 网络连接是否正常")
        print("    · 是否需要设置代理 (PROXY_URL 环境变量)")
        return None, None


def _print_auth_and_quota(auth, quota):
    """打印认证信息和配额"""
    used = quota["used_strategies"]
    max_s = quota["max_strategies"]
    remaining = quota["remaining"]

    print()
    print(f"{'━' * 50}")
    print(f"  🔑 认证信息")
    print(f"{'━' * 50}")
    print(f"  机器码:     {quota['machine_code'][:8]}...")
    print(f"  Token:      {auth.token[:16]}...")
    print(f"  📦 策略配额: {used}/{max_s} 已用，剩余 {remaining} 个")

    if quota.get("strategies"):
        print()
        print("  📋 已注册策略:")
        for s in quota["strategies"]:
            print(f"    📌 {s['name']} ({s['strategy_id']})")
    print(f"{'━' * 50}")

    return remaining


def _ask_backtest_params():
    """交互式输入回测参数"""
    print("\n  回测参数配置 (直接回车使用默认值):")
    capital_str = input("    初始资金 (默认 $100,000): ").strip()
    capital = float(capital_str) if capital_str else 100000.0

    leverage_str = input("    杠杆倍数 (默认 3x): ").strip()
    leverage = int(leverage_str) if leverage_str else 3

    print(f"\n  ✅ 参数确认: 初始资金 ${capital:,.0f} | 杠杆 {leverage}x")
    return capital, leverage


def _show_result(client, result):
    """展示回测结果"""
    print()
    client.print_metrics(result)
    client.print_conclusion(result)
    client.print_trades(result, limit=10)


def _print_next_steps(result: dict, strategy_name: str):
    """根据回测结论给出具体的下一步操作指引"""
    conclusion = result.get("conclusion", "")

    print()
    print(f"{'━' * 50}")
    print(f"  🔧 下一步操作")
    print(f"{'━' * 50}")

    if conclusion == "approved":
        print(f"  ✅ 策略 [{strategy_name}] 已通过回测验证！")
        print()
        print("  1️⃣ 部署实时监控")
        print("     告诉 AI: \"帮我部署这个策略进行实时监控\"")
        print()
        print("  2️⃣ 换时间段再验证稳健性")
        print(f"     python {sys.argv[0]} backtest 2023-01-01 2023-12-31")
        print()
        print("  3️⃣ 调整参数后重新回测")
        print("     告诉 AI: \"把止损改成 2%，放量倍数改成 1.2\"")

    elif conclusion == "paper_trade_first":
        print(f"  ⚠️ 策略 [{strategy_name}] 建议先模拟观察")
        print()
        print("  1️⃣ 先跑模拟盘 1-2 周")
        print("     告诉 AI: \"帮我用模拟盘跑一下这个策略\"")
        print()
        print("  2️⃣ 参数优化后重新回测")
        print("     告诉 AI: \"帮我优化一下这个策略的参数\"")
        print()
        print("  3️⃣ 换时间段再测试")
        print(f"     python {sys.argv[0]} backtest 2023-06-01 2024-06-01")

    elif conclusion == "rejected":
        print(f"  ❌ 策略 [{strategy_name}] 未通过回测，需要调整")
        print()
        print("  1️⃣ 让 AI 分析问题并优化")
        print("     告诉 AI: \"回测没通过，帮我分析原因并优化\"")
        print()
        print("  2️⃣ 修改策略逻辑")
        print("     告诉 AI: \"加上 RSI 过滤\" 或 \"止损改紧一点\"")
        print()
        print("  3️⃣ 换个策略思路重新来")
        print("     告诉 AI: \"帮我做一个新的 BTC 策略\"")

    else:
        print("  📋 回测已完成，你可以:")
        print()
        print("  1️⃣ 告诉 AI 你对结果的看法，进行下一步")
        print("  2️⃣ 调整参数后重新回测")
        print(f"     python {sys.argv[0]} backtest <开始日期> <结束日期>")

    print(f"{'━' * 50}")


# ═══════════════════════════════════════════
# 模式 1: 本地回测（本地生成信号 → 传信号到服务器回测）
# ═══════════════════════════════════════════

def _run_local_backtest(
    strategy_name, symbol, timeframe,
    start_date, end_date, signals, server_url,
):
    from api_client import QuantAPIClient

    print()
    print(f"  {'━' * 45}")
    print("  ⚡ 第 3 步 / 共 3 步：执行回测")
    print(f"  {'━' * 45}")

    auth, quota = _connect_server(server_url)
    if auth is None:
        print("\n  下一步: 检查网络后重新运行脚本")
        return
    _print_auth_and_quota(auth, quota)

    capital, leverage = _ask_backtest_params()

    print(f"\n  正在将 {len(signals)} 个信号发送到服务器回测引擎...")
    print(f"  服务器将: 拉取 K 线数据 → 逐 bar 模拟交易 → 计算绩效")

    try:
        client = QuantAPIClient(server_url)
        result = client.run_backtest(
            strategy_name=strategy_name,
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            signals=signals,
            initial_capital=capital,
            leverage=leverage,
        )
        _show_result(client, result)
        _print_next_steps(result, strategy_name)
        client.close()
    except Exception as e:
        print(f"\n  ❌ 回测失败: {e}")
        print(f"  下一步: 检查网络连接后重新运行脚本")

    auth.close()


# ═══════════════════════════════════════════
# 模式 2: 服务器回测（上传脚本 → 服务器执行一切）
# ═══════════════════════════════════════════

def _run_server_backtest(
    strategy_name, symbol, timeframe,
    start_date, end_date, script_path, server_url,
):
    from api_client import QuantAPIClient

    print()
    print(f"  {'━' * 45}")
    print("  ⚡ 第 3 步 / 共 3 步：服务器回测")
    print(f"  {'━' * 45}")

    if not script_path or not os.path.isfile(script_path):
        print(f"\n  ❌ 找不到策略脚本文件: {script_path}")
        print("  下一步: 确认脚本文件存在后重新运行")
        return

    auth, quota = _connect_server(server_url)
    if auth is None:
        print("\n  下一步: 检查网络后重新运行脚本")
        return
    remaining = _print_auth_and_quota(auth, quota)

    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    script_size = len(script_content)
    print(f"\n  脚本文件:   {os.path.basename(script_path)} ({script_size:,} 字节)")

    if remaining <= 0:
        print()
        print("  " + "!" * 55)
        print("  ！免费配额已满（{}个），无法上传新策略到服务器".format(
            quota["max_strategies"]))
        print("  " + "!" * 55)
        print(f"\n  下一步: 重新运行脚本，选择 [1] 本地回测（不占配额）")
        auth.close()
        return

    capital, leverage = _ask_backtest_params()

    print(f"\n  正在上传脚本到服务器...")
    print(f"  服务器将: 拉取数据 → 执行脚本生成信号 → 回测引擎模拟 → 出报告")

    try:
        client = QuantAPIClient(server_url)

        save_result = client.save_strategy(
            name=strategy_name,
            script_content=script_content,
            symbol=symbol,
            timeframe=timeframe,
        )
        strategy_id = save_result.get("strategy_id", "")
        print(f"  ✅ 策略已保存到服务器: {strategy_id}", flush=True)

        job_id = client.submit_backtest(
            script_content=script_content,
            strategy_name=strategy_name,
            strategy_id=strategy_id,
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            initial_capital=capital,
            leverage=leverage,
        )
        print(f"  回测任务已提交，正在轮询进度: {job_id}", flush=True)

        result = client.wait_backtest(
            job_id,
            poll_interval=5.0,
            max_running_logs=1,
        )
        _show_result(client, result)
        _print_next_steps(result, strategy_name)
        client.close()
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            print(f"\n  ❌ 配额不足，无法上传")
            print(f"  下一步: 重新运行脚本，选择 [1] 本地回测（不占配额）")
        else:
            print(f"\n  ❌ 服务器回测失败: {e}")
            print(f"  下一步: 检查网络后重试，或选择 [1] 本地回测")

    auth.close()


# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

def run(
    generate_fn,
    strategy_name: str,
    symbol: str,
    timeframe: str,
    script_path: str = None,
    server_url: str | None = None,
):
    """
    策略脚本的统一入口。

    参数:
        generate_fn: 信号生成函数 generate_signals(mode, start_date, end_date)
        strategy_name: 策略名称
        symbol: 交易对
        timeframe: K线周期
        script_path: 脚本文件路径（__file__），服务器模式需要
        server_url: 服务器地址
    """
    import argparse

    parser = argparse.ArgumentParser(description=f"策略: {strategy_name}")
    parser.add_argument("mode", nargs="?", default="backtest",
                        help="运行模式: backtest / live")
    parser.add_argument("start_date", nargs="?", help="起始日期 YYYY-MM-DD")
    parser.add_argument("end_date", nargs="?", help="结束日期 YYYY-MM-DD")
    parser.add_argument("--server", default=resolve_server_url(server_url), help="服务器地址")

    args = parser.parse_args()

    _print_welcome()
    _print_banner(strategy_name, symbol, timeframe, script_path)

    if args.mode == "backtest" and not args.start_date:
        print("\n  回测模式需要指定日期范围")
        print(f"\n  正确用法:")
        print(f"    python {sys.argv[0]} backtest 2025-01-01 2025-03-01")
        print(f"\n  示例:")
        print(f"    python {sys.argv[0]} backtest 2024-01-01 2024-12-31  # 回测 2024 全年")
        print(f"    python {sys.argv[0]} backtest 2025-01-01 2025-03-01  # 回测近 2 个月")
        return

    print()
    print(f"  {'━' * 45}")
    print("  📡 第 1 步 / 共 3 步：本地生成信号")
    print(f"  {'━' * 45}")
    print(f"  模式: {'回测' if args.mode == 'backtest' else '实时'}")
    if args.start_date:
        print(f"  区间: {args.start_date} → {args.end_date}")
    print(f"\n  正在从 Binance 拉取 K 线数据并计算指标...")

    result = generate_fn(mode=args.mode, start_date=args.start_date, end_date=args.end_date)

    if result.get("error"):
        print(f"\n  ❌ 生成信号失败: {result['error']}")
        print(f"  请检查网络连接或调整时间范围后重试")
        return

    signals = result.get("signals", [])
    if not signals:
        print(f"\n  ❌ 未生成任何信号")
        print(f"  可能的原因:")
        print(f"    - 时间范围内没有触发买卖条件")
        print(f"    - 策略参数过于严格（如放量倍数太高）")
        print(f"  建议: 扩大时间范围或放宽条件参数后重试")
        return

    _print_signals_summary(signals)
    print(f"\n  ✅ 信号生成完成")

    has_script = script_path and os.path.isfile(script_path)

    print()
    print(f"  {'━' * 45}")
    print("  🔧 第 2 步 / 共 3 步：选择回测模式")
    print(f"  {'━' * 45}")
    print()
    print("    1️⃣ 本地回测（推荐）")
    print("       信号已在本地生成，发到服务器回测引擎出报告")
    print("       不占配额，无限制使用")
    if has_script:
        print()
        print("    2️⃣ 服务器回测")
        print("       上传脚本到服务器，服务器重新拉数据+生成信号+回测")
        print("       占 1 个策略配额（3 个）")
    else:
        print()
        print("    2️⃣ 服务器回测 — 不可用（未传入脚本路径）")
    print()
    print("    ❌ q 退出")
    print()

    while True:
        choice = input("  请选择 (1/2/q): ").strip()
        if choice in ("1", "2", "q"):
            break
        print("  无效输入，请输入 1、2 或 q")

    if choice == "1":
        _run_local_backtest(
            strategy_name, symbol, timeframe,
            args.start_date or "", args.end_date or "",
            signals, args.server,
        )
    elif choice == "2":
        if not has_script:
            print("\n  ❌ 服务器模式不可用")
            print("  原因: 调用 run() 时未传入 script_path=__file__")
            print("  请在脚本的 __main__ 中添加: script_path=__file__")
            return
        _run_server_backtest(
            strategy_name, symbol, timeframe,
            args.start_date or "", args.end_date or "",
            script_path, args.server,
        )
    else:
        print("\n  已退出。你可以随时重新运行此脚本。")
