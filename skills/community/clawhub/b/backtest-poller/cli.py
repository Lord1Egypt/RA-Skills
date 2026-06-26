#!/usr/bin/env python3
"""
Backtest Poller CLI — Submit and monitor QuantConnect backtests
===============================================================
A fire-and-forget workflow: submit a backtest, close the terminal, come back
later to check results.

Architecture:
  1. submit:       Submit a backtest -> register in state.json -> start nohup poller
  2. status:       View all backtest progress (reads state.json)
  3. logs:         View poller daemon logs
  4. results:      View completed backtest results and diagnostics
  5. start-poller: Manually start the background poller
  6. stop-poller:  Stop the background poller
  7. clear:        Remove completed backtest records

Environment variables:
  QC_USER_ID       — QuantConnect user ID
  QC_API_TOKEN     — QuantConnect API token
  QC_PROJECT_ID    — Default QC project ID
  STATE_FILE       — Path to state.json (default: ./state.json)
  LOG_FILE         — Path to poller.log (default: ./poller.log)
  RESULTS_DIR      — Directory for downloaded results (default: ./results)

Usage:
  python3 cli.py submit --backtest-id abc123 --name "MyStrategy_v1" --max-dd 0.40
  python3 cli.py status
  python3 cli.py logs --lines 50
  python3 cli.py results --name MyStrategy --full
  python3 cli.py start-poller
  python3 cli.py stop-poller
  python3 cli.py clear
"""
import os
import sys
import argparse
import subprocess
import signal

from dotenv import load_dotenv

load_dotenv()

# Local imports — support both package-style and direct execution
try:
    from .poller import PollerDaemon, BacktestState, STATE_FILE, LOG_FILE
except ImportError:
    from poller import PollerDaemon, BacktestState, STATE_FILE, LOG_FILE


DEFAULT_PROJECT_ID = int(os.environ.get("QC_PROJECT_ID", "0"))


# ================================================================
# Commands
# ================================================================

def cmd_submit(args):
    """Register a backtest for monitoring and start the poller daemon."""
    backtest_id = args.backtest_id
    project_id = args.project_id or DEFAULT_PROJECT_ID
    name = args.name or backtest_id[:12]
    max_dd = args.max_dd or 0

    if not backtest_id:
        print("Error: --backtest-id is required")
        sys.exit(1)

    if project_id == 0:
        print("Error: QC_PROJECT_ID environment variable or --project-id argument is required")
        sys.exit(1)

    print(f"Submitting backtest for monitoring: {name}")
    print(f"  Backtest ID:  {backtest_id}")
    print(f"  Project ID:   {project_id}")
    if max_dd > 0:
        print(f"  DD threshold: {max_dd:.0%}")

    # Register in state.json
    PollerDaemon.add_backtest(
        backtest_id=backtest_id,
        name=name,
        strategy_file=args.strategy_file or "",
        max_dd=max_dd,
        project_id=project_id,
        auto_download=not args.no_download,
        auto_diagnose=not args.no_diagnose,
    )

    # Start the poller if not already running
    _ensure_poller_running()

    print(f"\n{'=' * 50}")
    print("Backtest registered and poller is running!")
    print("You can safely close the terminal now.")
    print("Check progress anytime with:")
    print()
    print("    python3 cli.py status")
    print("    python3 cli.py logs")
    print()
    print("Results will be auto-downloaded when the backtest completes.")
    print(f"{'=' * 50}")


def cmd_status(args):
    """Display status of all tracked backtests."""
    state = PollerDaemon.load_state()

    # Poller daemon status
    poller_running = state.get("poller_running", False)
    poller_pid = state.get("poller_pid")

    # Verify the PID actually exists
    if poller_pid and poller_running:
        try:
            os.kill(poller_pid, 0)  # signal 0 = check existence only
        except OSError:
            poller_running = False

    status_icon = "[ON]" if poller_running else "[OFF]"
    poller_detail = f"running (PID {poller_pid})" if poller_running else "not running"
    print(f"\n{status_icon} Poller daemon: {poller_detail}")

    backtests = state.get("backtests", [])
    if not backtests:
        print("\nNo backtests tracked")
        return

    print(f"\n{'─' * 90}")
    print(
        f"{'Name':<30} {'Status':<15} {'Progress':<12} "
        f"{'Equity':<12} {'Drawdown':<10} {'Elapsed':<10}"
    )
    print(f"{'─' * 90}")

    for bt_data in backtests:
        bt = BacktestState(bt_data)

        # Status label
        status_map = {
            "pending": "Pending",
            "running": "Running",
            "completed": "Completed",
            "error": "Error",
            "early_stop": "Early Stop",
            "timeout": "Timeout",
        }
        status_str = status_map.get(bt.status, bt.status)

        # Progress bar
        bar_len = 8
        filled = int(bar_len * bt.progress)
        bar = "#" * filled + "-" * (bar_len - filled)
        progress_str = f"{bar} {bt.progress * 100:.0f}%"

        # Equity
        eq_str = f"${bt.current_equity:,.0f}" if bt.current_equity > 0 else "-"

        # Drawdown
        dd_str = f"{bt.live_drawdown:.1%}" if bt.live_drawdown > 0.005 else "-"

        # Elapsed time
        elapsed = bt.elapsed_minutes
        if elapsed > 60:
            time_str = f"{elapsed / 60:.1f}h"
        else:
            time_str = f"{elapsed:.0f}min"

        name_short = bt.name[:28] if len(bt.name) > 28 else bt.name
        print(
            f"{name_short:<30} {status_str:<15} {progress_str:<12} "
            f"{eq_str:<12} {dd_str:<10} {time_str:<10}"
        )

        # Show key metrics for completed backtests
        if bt.status == "completed" and bt.stats:
            stats = bt.stats
            net_p = stats.get("Net Profit", "?")
            dd = stats.get("Drawdown", "?")
            sharpe = stats.get("Sharpe Ratio", "?")
            orders = stats.get("Total Orders", "?")
            print(f"  {'':>30} Profit:{net_p} DD:{dd} Sharpe:{sharpe} Orders:{orders}")
            if bt.diagnosis_summary:
                print(f"  {'':>30} Diagnosis: {bt.diagnosis_summary}")

        if bt.status == "error":
            print(f"  {'':>30} Error: {bt.error[:80]}")

        if bt.status == "early_stop":
            print(f"  {'':>30} Early stop: {bt.error[:80]}")

    print(f"{'─' * 90}")

    # Warn if there are active backtests but the poller is not running
    active = [bt for bt in backtests if bt.get("status") in ("pending", "running")]
    if active and not poller_running:
        print(f"\nWARNING: {len(active)} active backtest(s) but poller is not running!")
        print("  Start it with: python3 cli.py start-poller")


def cmd_logs(args):
    """Display recent poller log entries."""
    if not os.path.exists(LOG_FILE):
        print("No log file found")
        return

    n = args.lines
    with open(LOG_FILE) as f:
        lines = f.readlines()

    tail = lines[-n:] if len(lines) > n else lines
    print(f"Poller log (last {len(tail)} lines):\n")
    for line in tail:
        print(line.rstrip())


def cmd_results(args):
    """Display results of completed backtests."""
    state = PollerDaemon.load_state()
    backtests = state.get("backtests", [])

    target = args.name
    found = False

    for bt_data in backtests:
        if target and target.lower() not in bt_data.get("name", "").lower():
            continue
        if bt_data.get("status") != "completed":
            continue

        found = True
        result_dir = bt_data.get("result_dir", "")
        diagnosis = os.path.join(result_dir, "diagnosis.txt") if result_dir else ""

        print(f"\n{bt_data['name']}")
        print(f"  Backtest ID: {bt_data['backtest_id']}")
        print(f"  Result dir:  {result_dir}")

        if bt_data.get("stats"):
            print("  Key metrics:")
            for k in ["Net Profit", "Drawdown", "Sharpe Ratio", "Win Rate", "Total Orders"]:
                if k in bt_data["stats"]:
                    print(f"    {k}: {bt_data['stats'][k]}")

        if diagnosis and os.path.exists(diagnosis):
            print(f"\n  Diagnosis report: {diagnosis}")
            if args.full:
                with open(diagnosis) as f:
                    print(f.read())

    if not found:
        filter_msg = f" matching '{target}'" if target else ""
        print(f"No completed backtests found{filter_msg}")


def cmd_start_poller(args):
    """Manually start the poller daemon."""
    _ensure_poller_running()


def cmd_stop_poller(args):
    """Stop the poller daemon."""
    state = PollerDaemon.load_state()
    pid = state.get("poller_pid")
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Sent stop signal to PID {pid}")
        except ProcessLookupError:
            print(f"PID {pid} not found (already stopped)")
        state["poller_running"] = False
        state["poller_pid"] = None
        PollerDaemon.save_state(state)
    else:
        print("Poller is not running")


def cmd_clear(args):
    """Remove completed/finished backtest records, keeping active ones."""
    state = PollerDaemon.load_state()
    before = len(state.get("backtests", []))
    state["backtests"] = [
        bt for bt in state.get("backtests", [])
        if bt.get("status") in ("pending", "running")
    ]
    after = len(state["backtests"])
    PollerDaemon.save_state(state)
    print(f"Cleared {before - after} completed record(s) ({after} active task(s) retained)")


# ================================================================
# Helpers
# ================================================================

def _ensure_poller_running():
    """Ensure the poller daemon is running, starting it if necessary."""
    state = PollerDaemon.load_state()
    pid = state.get("poller_pid")

    if pid:
        try:
            os.kill(pid, 0)
            print(f"Poller already running (PID {pid})")
            return
        except OSError:
            pass  # stale PID, start a new one

    # Start a new poller daemon
    poller_script = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "poller.py"
    )

    log_fd = open(LOG_FILE, "a")
    process = subprocess.Popen(
        [sys.executable, poller_script],
        stdout=log_fd,
        stderr=log_fd,
        cwd=os.path.dirname(os.path.abspath(__file__)),
        start_new_session=True,  # Detach from terminal session
    )
    log_fd.close()  # Child has inherited the fd; parent no longer needs it

    print(f"Poller daemon started (PID {process.pid})")

    # Update state
    state["poller_pid"] = process.pid
    state["poller_running"] = True
    PollerDaemon.save_state(state)


# ================================================================
# Main entry point
# ================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Backtest Poller CLI — submit and monitor QuantConnect backtests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Register a backtest for monitoring (fire-and-forget)
  python3 cli.py submit --backtest-id abc123 --name "MyStrategy_v1" --max-dd 0.40

  # Check status of all backtests
  python3 cli.py status

  # View poller logs
  python3 cli.py logs --lines 50

  # View completed results
  python3 cli.py results --name MyStrategy --full

  # Start/stop the daemon manually
  python3 cli.py start-poller
  python3 cli.py stop-poller

  # Clean up finished records
  python3 cli.py clear
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # submit
    p_submit = subparsers.add_parser("submit", help="Register a backtest for monitoring")
    p_submit.add_argument("--backtest-id", required=True, help="QC backtest ID to monitor")
    p_submit.add_argument("--project-id", type=int, default=0, help="QC project ID (or set QC_PROJECT_ID env var)")
    p_submit.add_argument("--name", help="Human-readable backtest name")
    p_submit.add_argument("--strategy-file", default="", help="Path to the strategy source file (for reference)")
    p_submit.add_argument("--max-dd", type=float, default=0.50, help="Drawdown early-stop threshold (default: 0.50)")
    p_submit.add_argument("--no-download", action="store_true", help="Disable auto-download on completion")
    p_submit.add_argument("--no-diagnose", action="store_true", help="Disable auto-diagnosis on completion")

    # status
    subparsers.add_parser("status", help="View backtest status")

    # logs
    p_logs = subparsers.add_parser("logs", help="View poller daemon logs")
    p_logs.add_argument("--lines", "-n", type=int, default=30, help="Number of lines to display")

    # results
    p_results = subparsers.add_parser("results", help="View completed results")
    p_results.add_argument("--name", help="Filter by backtest name (substring match)")
    p_results.add_argument("--full", action="store_true", help="Show full diagnosis report")

    # start-poller
    subparsers.add_parser("start-poller", help="Start the poller daemon")

    # stop-poller
    subparsers.add_parser("stop-poller", help="Stop the poller daemon")

    # clear
    subparsers.add_parser("clear", help="Clear completed backtest records")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "submit": cmd_submit,
        "status": cmd_status,
        "logs": cmd_logs,
        "results": cmd_results,
        "start-poller": cmd_start_poller,
        "stop-poller": cmd_stop_poller,
        "clear": cmd_clear,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
