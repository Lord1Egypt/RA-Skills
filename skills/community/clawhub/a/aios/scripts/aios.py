#!/usr/bin/env python3
"""
AIOS - Aiden Investment Operating System
交易检查工具（支持交互模式和命令行模式）

交互模式：
  python3 aios.py check
  python3 aios.py position
  python3 aios.py init

命令行模式（供 Skill 调用）：
  python3 aios.py position --price 100 --stop-loss 92 --account 1000000
  python3 aios.py init --account 1000000
  python3 aios.py log --type 买入 --ticker AAPL --price 150 --stop-loss 138 --target 180 --reasons "AI趋势" --emotion 1
  python3 aios.py status
  python3 aios.py check --type 买入 --ticker AAPL --price 150 --stop-loss 138 --target 180 --account 1000000
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# ─── 配置 ───────────────────────────────────────────────
AIOS_ROOT = Path(__file__).parent.parent.parent  # skill root
LOG_DIR = Path.cwd() / "logs"
POSITIONS_FILE = LOG_DIR / "positions.json"
TRADE_LOG_FILE = LOG_DIR / "trade_log.json"
CONFIG_FILE = LOG_DIR / "aios_config.json"

DEFAULT_CONFIG = {
    "account_total": 0,
    "max_loss_per_trade_pct": 1,
    "max_monthly_drawdown_pct": 5,
    "max_total_position_pct": 80,
    "max_sector_pct": 30,
    "max_single_stock_pct": 15,
    "min_risk_reward_ratio": 2,
    "consecutive_loss_pause": 3,
    "pause_days": 7,
}


def ensure_log_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            if k not in config:
                config[k] = v
        return config
    return DEFAULT_CONFIG.copy()


def save_config(config):
    ensure_log_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_positions():
    if POSITIONS_FILE.exists():
        with open(POSITIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_positions(positions):
    ensure_log_dir()
    with open(POSITIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(positions, f, ensure_ascii=False, indent=2)


def load_trade_log():
    if TRADE_LOG_FILE.exists():
        with open(TRADE_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_trade_log(log):
    ensure_log_dir()
    with open(TRADE_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def ask_yes_no(question, default=None):
    suffix = " [Y/n]" if default == "y" else " [y/N]" if default == "n" else " [y/n]"
    while True:
        answer = input(f"  {question}{suffix}: ").strip().lower()
        if not answer and default:
            return default == "y"
        if answer in ("y", "yes", "是"):
            return True
        if answer in ("n", "no", "否"):
            return False
        print("  请输入 y 或 n")


def ask_number(question, default=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        answer = input(f"  {question}{suffix}: ").strip()
        if not answer and default is not None:
            return float(default)
        try:
            return float(answer)
        except ValueError:
            print("  请输入有效数字")


def ask_text(question, default=None):
    suffix = f" [{default}]" if default else ""
    answer = input(f"  {question}{suffix}: ").strip()
    return answer if answer else default


def print_header(title):
    print()
    print("=" * 60)
    print(f"  🛡️  AIOS - {title}")
    print("=" * 60)
    print()


def print_section(title):
    print()
    print(f"  ── {title} ──")
    print()


def print_pass(msg):
    print(f"  ✅ {msg}")


def print_fail(msg):
    print(f"  ❌ {msg}")


def print_warn(msg):
    print(f"  ⚠️  {msg}")


def print_info(msg):
    print(f"  ℹ️  {msg}")


# ─── 命令行模式：仓位计算 ───────────────────────────────
def cmd_position_cli(args):
    """命令行仓位计算"""
    config = load_config()
    account = args.account or config["account_total"]

    if account <= 0:
        print(json.dumps({"error": "请提供账户总额 (--account)"}, ensure_ascii=False))
        return

    price = args.price
    stop_loss = args.stop_loss

    if stop_loss >= price:
        print(json.dumps({"error": "止损价必须低于买入价"}, ensure_ascii=False))
        return

    loss_per_share = price - stop_loss
    loss_pct = loss_per_share / price * 100
    max_loss_amount = account * config["max_loss_per_trade_pct"] / 100
    max_shares = int(max_loss_amount / loss_per_share)
    max_amount = max_shares * price
    max_pct = max_amount / account * 100

    # 检查单只股票上限
    capped = False
    if max_pct > config["max_single_stock_pct"]:
        max_amount = account * config["max_single_stock_pct"] / 100
        max_shares = int(max_amount / price)
        max_pct = config["max_single_stock_pct"]
        capped = True

    # 检查总仓位
    positions = load_positions()
    current_total_pct = sum(p.get("pct", 0) for p in positions.values())

    result = {
        "account_total": account,
        "price": price,
        "stop_loss": stop_loss,
        "loss_per_share": round(loss_per_share, 2),
        "loss_pct": round(loss_pct, 2),
        "max_loss_amount": round(max_loss_amount, 2),
        "max_shares": max_shares,
        "max_amount": round(max_amount, 2),
        "max_pct": round(max_pct, 2),
        "capped_by_single_stock_limit": capped,
        "current_total_position_pct": round(current_total_pct, 2),
        "remaining_position_pct": round(config["max_total_position_pct"] - current_total_pct, 2),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


# ─── 命令行模式：快速检查 ───────────────────────────────
def cmd_check_cli(args):
    """命令行快速检查"""
    config = load_config()
    account = args.account or config["account_total"]

    if account <= 0:
        print(json.dumps({"error": "请提供账户总额 (--account)"}, ensure_ascii=False))
        return

    price = args.price
    stop_loss = args.stop_loss
    target = args.target

    checks = []
    all_passed = True

    # 1. 止损检查
    if stop_loss >= price:
        checks.append({"name": "止损价", "passed": False, "detail": f"止损价 {stop_loss} 必须低于买入价 {price}"})
        all_passed = False
    else:
        loss_pct = (price - stop_loss) / price * 100
        checks.append({"name": "止损价", "passed": True, "detail": f"止损幅度 {loss_pct:.1f}%"})

    # 2. 风险回报比检查
    if target and target > price and stop_loss < price:
        gain_pct = (target - price) / price * 100
        loss_pct = (price - stop_loss) / price * 100
        rr_ratio = gain_pct / loss_pct if loss_pct > 0 else 0
        passed = rr_ratio >= config["min_risk_reward_ratio"]
        checks.append({
            "name": "风险回报比",
            "passed": passed,
            "detail": f"1:{rr_ratio:.1f} (最低 1:{config['min_risk_reward_ratio']})"
        })
        if not passed:
            all_passed = False

    # 3. 仓位检查
    loss_per_share = price - stop_loss
    if loss_per_share > 0:
        max_loss_amount = account * config["max_loss_per_trade_pct"] / 100
        max_shares = int(max_loss_amount / loss_per_share)
        max_amount = max_shares * price
        max_pct = max_amount / account * 100

        positions = load_positions()
        current_total_pct = sum(p.get("pct", 0) for p in positions.values())
        remaining = config["max_total_position_pct"] - current_total_pct

        checks.append({
            "name": "仓位建议",
            "passed": True,
            "detail": f"最大 {max_shares} 股 (¥{max_amount:,.0f}, {max_pct:.1f}%)"
        })
        checks.append({
            "name": "剩余仓位空间",
            "passed": remaining > 0,
            "detail": f"{remaining:.1f}%"
        })

    # 4. 止损幅度检查
    if stop_loss < price:
        loss_pct = (price - stop_loss) / price * 100
        if loss_pct > 10:
            checks.append({"name": "止损幅度", "passed": False, "detail": f"止损幅度 {loss_pct:.1f}% > 10%，建议缩小止损距离"})
            all_passed = False

    result = {
        "ticker": args.ticker,
        "price": price,
        "stop_loss": stop_loss,
        "target": target,
        "account": account,
        "checks": checks,
        "all_passed": all_passed
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


# ─── 命令行模式：记录日志 ───────────────────────────────
def cmd_log_cli(args):
    """命令行记录交易日志"""
    entry = {
        "datetime": datetime.now().isoformat(),
        "type": args.type,
        "ticker": args.ticker,
        "price": args.price,
        "stop_loss": args.stop_loss,
        "target_price": args.target,
        "emotion": args.emotion,
        "notes": args.notes or "",
    }

    if args.reasons:
        entry["reasons"] = [r.strip() for r in args.reasons.split(",")]
    else:
        entry["reasons"] = []

    log = load_trade_log()
    log.append(entry)
    save_trade_log(log)

    result = {
        "status": "saved",
        "entry": entry,
        "total_records": len(log)
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ─── 命令行模式：初始化 ─────────────────────────────────
def cmd_init_cli(args):
    """命令行初始化"""
    config = load_config()
    config["account_total"] = args.account
    save_config(config)
    print(json.dumps({"status": "ok", "account_total": args.account}, ensure_ascii=False))


# ─── 命令行模式：查看状态 ───────────────────────────────
def cmd_status_cli(args):
    """命令行查看状态"""
    config = load_config()
    positions = load_positions()
    log = load_trade_log()

    total_pct = sum(p.get("pct", 0) for p in positions.values())

    result = {
        "account_total": config["account_total"],
        "total_position_pct": round(total_pct, 2),
        "max_position_pct": config["max_total_position_pct"],
        "positions": positions,
        "total_trades": len(log),
        "recent_trades": log[-5:] if log else [],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ─── 交互模式：初始化 ───────────────────────────────────
def cmd_init_interactive():
    """交互式初始化"""
    print_header("初始化配置")
    config = load_config()

    if config["account_total"] > 0:
        print_info(f"当前账户总额: ¥{config['account_total']:,.0f}")
        if not ask_yes_no("是否重新配置?", "n"):
            return

    config["account_total"] = ask_number("请输入账户总额（人民币）")
    config["max_loss_per_trade_pct"] = ask_number("单笔最大亏损百分比", config["max_loss_per_trade_pct"])
    save_config(config)
    print_pass("配置保存成功！")


# ─── 交互模式：仓位计算 ─────────────────────────────────
def cmd_position_interactive():
    """交互式仓位计算"""
    print_header("仓位计算器 (Position Sizing)")
    config = load_config()

    if config["account_total"] == 0:
        print_fail("请先运行 init 初始化账户")
        return

    print_info(f"账户总额: ¥{config['account_total']:,.0f}")
    price = ask_number("买入价格")
    stop_loss = ask_number("止损价格")

    if stop_loss >= price:
        print_fail("止损价必须低于买入价")
        return

    loss_per_share = price - stop_loss
    loss_pct = loss_per_share / price * 100
    max_loss_amount = config["account_total"] * config["max_loss_per_trade_pct"] / 100
    max_shares = int(max_loss_amount / loss_per_share)
    max_amount = max_shares * price
    max_pct = max_amount / config["account_total"] * 100

    print_section("计算结果")
    print_info(f"止损距离: ¥{loss_per_share:.2f}/股 ({loss_pct:.1f}%)")
    print_info(f"最大允许亏损: ¥{max_loss_amount:,.0f}")
    print_info(f"建议最大买入: {max_shares:,} 股")
    print_info(f"建议最大金额: ¥{max_amount:,.0f}")
    print_info(f"建议最大占比: {max_pct:.1f}%")

    if max_pct > config["max_single_stock_pct"]:
        max_amount_by_rule = config["account_total"] * config["max_single_stock_pct"] / 100
        max_shares_by_rule = int(max_amount_by_rule / price)
        print_warn(f"超过单只股票仓位上限 {config['max_single_stock_pct']}%")
        print_info(f"按规则上限: {max_shares_by_rule:,} 股 (¥{max_amount_by_rule:,.0f})")


# ─── 交互模式：交易检查 ─────────────────────────────────
def cmd_check_interactive():
    """交互式交易检查"""
    print_header("交易前检查")
    config = load_config()

    if config["account_total"] == 0:
        print_fail("请先运行 init 初始化账户")
        return

    print_section("交易类型")
    print("  1. 买入（新开仓）  2. 加仓  3. 卖出  4. 减仓")
    trade_type = int(ask_number("请选择", 1))
    trade_types = {1: "买入", 2: "加仓", 3: "卖出", 4: "减仓"}
    trade_type_name = trade_types.get(trade_type, "买入")

    ticker = ask_text("标的代码/名称")
    price = ask_number("当前价格")

    if trade_type in (1, 2):
        checks_passed = True

        print_section("一、买入理由（至少 3 条）")
        reasons = []
        for i in range(1, 4):
            reason = ask_text(f"理由 {i}")
            if reason:
                reasons.append(reason)
        if len(reasons) < 3:
            print_fail("需要至少 3 条买入理由")
            checks_passed = False
        else:
            print_pass(f"已提供 {len(reasons)} 条理由")

        print_section("二、失效条件")
        invalidation = ask_text("什么情况下你的判断是错的？")
        if not invalidation:
            print_fail("必须设定失效条件")
            checks_passed = False

        print_section("三、止损价格")
        stop_loss = ask_number("止损价格")
        if stop_loss >= price:
            print_fail(f"止损价 {stop_loss} 必须低于买入价 {price}")
            checks_passed = False
        else:
            loss_pct = (price - stop_loss) / price * 100
            print_pass(f"止损幅度: {loss_pct:.1f}%")

        print_section("四、风险回报比")
        target_price = ask_number("目标价格")
        if target_price > price and stop_loss < price:
            gain_pct = (target_price - price) / price * 100
            loss_pct = (price - stop_loss) / price * 100
            rr_ratio = gain_pct / loss_pct if loss_pct > 0 else 0
            print_info(f"风险回报比: 1:{rr_ratio:.1f}")
            if rr_ratio < config["min_risk_reward_ratio"]:
                print_fail(f"风险回报比不达标")
                checks_passed = False
            else:
                print_pass(f"风险回报比达标")

        print_section("五、仓位")
        loss_per_share = price - stop_loss
        if loss_per_share > 0:
            max_loss_amount = config["account_total"] * config["max_loss_per_trade_pct"] / 100
            max_shares = int(max_loss_amount / loss_per_share)
            max_amount = max_shares * price
            print_info(f"建议最大买入: {max_shares:,} 股 (¥{max_amount:,.0f})")

        # 补仓特殊检查
        if trade_type == 2:
            print_section("六、补仓检查")
            if not ask_yes_no("如果没有持仓，这个价格你会买吗？"):
                print_fail("禁止补仓！")
                checks_passed = False

        # 情绪检查
        print_section("情绪自检")
        print("  1. 冷静理性 ✅  2. 焦虑 ⚠️  3. FOMO ❌  4. 恐慌 ❌  5. 过度自信 ⚠️")
        emotion = int(ask_number("选择", 1))
        if emotion in (3, 4):
            print_fail("情绪不适合交易")
            checks_passed = False

        print()
        print("=" * 60)
        if checks_passed:
            print_pass("🎉 所有检查通过！可以执行交易。")
        else:
            print_fail("🚫 检查未通过，请补充信息后再试。")
    else:
        print_info(f"已确认{trade_type_name}操作")


# ─── 交互模式：交易日志 ─────────────────────────────────
def cmd_log_interactive():
    """交互式记录交易日志"""
    print_header("记录交易日志")
    entry = {
        "datetime": datetime.now().isoformat(),
        "type": ask_text("交易类型（买入/卖出/加仓/减仓）"),
        "ticker": ask_text("标的代码/名称"),
        "price": ask_number("价格"),
        "reasons": [],
    }
    for i in range(1, 4):
        r = ask_text(f"理由 {i}")
        if r:
            entry["reasons"].append(r)

    print("  情绪: 1.冷静 2.焦虑 3.FOMO 4.恐慌 5.过度自信")
    entry["emotion"] = int(ask_number("选择", 1))

    log = load_trade_log()
    log.append(entry)
    save_trade_log(log)
    print_pass("已保存")


# ─── 主入口 ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AIOS - Aiden Investment Operating System")
    subparsers = parser.add_subparsers(dest="command")

    # init
    p_init = subparsers.add_parser("init")
    p_init.add_argument("--account", type=float, help="账户总额")

    # position
    p_pos = subparsers.add_parser("position")
    p_pos.add_argument("--price", type=float, help="买入价格")
    p_pos.add_argument("--stop-loss", type=float, help="止损价格")
    p_pos.add_argument("--account", type=float, help="账户总额")

    # check
    p_check = subparsers.add_parser("check")
    p_check.add_argument("--type", help="交易类型")
    p_check.add_argument("--ticker", help="标的代码")
    p_check.add_argument("--price", type=float, help="价格")
    p_check.add_argument("--stop-loss", type=float, help="止损价格")
    p_check.add_argument("--target", type=float, help="目标价格")
    p_check.add_argument("--account", type=float, help="账户总额")

    # log
    p_log = subparsers.add_parser("log")
    p_log.add_argument("--type", help="交易类型")
    p_log.add_argument("--ticker", help="标的代码")
    p_log.add_argument("--price", type=float, help="价格")
    p_log.add_argument("--stop-loss", type=float, help="止损价")
    p_log.add_argument("--target", type=float, help="目标价")
    p_log.add_argument("--reasons", help="理由（逗号分隔）")
    p_log.add_argument("--emotion", type=int, default=1, help="情绪 1-5")
    p_log.add_argument("--notes", help="备注")

    # status
    subparsers.add_parser("status")

    # review
    subparsers.add_parser("review")

    args, unknown = parser.parse_known_args()

    # 判断是否命令行模式（有参数）还是交互模式
    has_cli_args = len(sys.argv) > 1

    if has_cli_args and args.command:
        if args.command == "init":
            if args.account:
                cmd_init_cli(args)
            else:
                cmd_init_interactive()
        elif args.command == "position":
            if args.price and args.stop_loss:
                cmd_position_cli(args)
            else:
                cmd_position_interactive()
        elif args.command == "check":
            if args.price and args.stop_loss:
                cmd_check_cli(args)
            else:
                cmd_check_interactive()
        elif args.command == "log":
            if args.ticker and args.price:
                cmd_log_cli(args)
            else:
                cmd_log_interactive()
        elif args.command == "status":
            cmd_status_cli(args)
        elif args.command == "review":
            print("请使用交互模式或查看 logs/ 目录中的记录")
        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
