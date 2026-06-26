"""
Backtest Poller Daemon
======================
A standalone background process (run via nohup) that monitors QuantConnect
backtests. It does not depend on any terminal session.

Features:
  - Adaptive polling intervals (30s-180s based on progress)
  - Real-time equity tracking and live drawdown calculation
  - Drawdown-based early stop (deletes the backtest when threshold exceeded)
  - Auto-download of results (orders CSV + result JSON) on completion
  - Optional auto-diagnosis via an external forensics module
  - macOS system notifications on completion
  - All state persisted to state.json with file locking

Usage:
    # Start the daemon (typically called by the CLI)
    nohup python3 poller.py &

    # Or run directly for debugging
    python3 poller.py

Environment variables:
    QC_USER_ID       — QuantConnect user ID
    QC_API_TOKEN     — QuantConnect API token
    QC_PROJECT_ID    — Default QC project ID
    STATE_FILE       — Path to state.json (default: ./state.json)
    LOG_FILE         — Path to poller.log (default: ./poller.log)
    RESULTS_DIR      — Directory for downloaded results (default: ./results)
"""
import os
import sys
import csv
import json
import time
import signal
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# Local imports — support both package-style and direct execution
try:
    from .utils import (
        parse_equity, parse_pct, state_file_lock,
        load_state_unlocked, save_state_unlocked,
    )
    from .qc_client import QCClient
except ImportError:
    from utils import (
        parse_equity, parse_pct, state_file_lock,
        load_state_unlocked, save_state_unlocked,
    )
    from qc_client import QCClient


# ====== Configurable paths ======
STATE_FILE = os.environ.get(
    "STATE_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json"),
)
LOG_FILE = os.environ.get(
    "LOG_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "poller.log"),
)
RESULTS_DIR = os.environ.get(
    "RESULTS_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"),
)
DEFAULT_PROJECT_ID = int(os.environ.get("QC_PROJECT_ID", "0"))

# ====== Adaptive polling intervals ======
# Different phases use different frequencies to save API quota.
# A 3-hour backtest: ~360 calls (fixed 30s) -> ~50 calls (adaptive).
POLL_INTERVAL_INITIAL = 30    # Just submitted — confirm it started
POLL_INTERVAL_RUNNING = 120   # Normal running — steady tracking
POLL_INTERVAL_MIDGAME = 180   # 30%-80% progress — low frequency
POLL_INTERVAL_ENDGAME = 60    # >80% progress — nearly done, check often

# ====== Logging — write to file only (stdout may be redirected) ======
logger = logging.getLogger("backtest_poller")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s [POLLER] %(message)s"))
    logger.addHandler(fh)


# =====================================================================
# BacktestState — tracks a single backtest
# =====================================================================
class BacktestState:
    """State tracker for one backtest."""

    def __init__(self, data: dict = None):
        data = data or {}
        self.backtest_id: str = data.get("backtest_id", "")
        self.project_id: int = data.get("project_id", DEFAULT_PROJECT_ID)
        self.name: str = data.get("name", "")
        self.strategy_file: str = data.get("strategy_file", "")
        # Lifecycle: pending -> running -> completed / error / early_stop / timeout
        self.status: str = data.get("status", "pending")
        self.submitted_at: str = data.get("submitted_at", "")
        self.completed_at: str = data.get("completed_at", "")
        self.progress: float = data.get("progress", 0.0)
        self.peak_equity: float = data.get("peak_equity", 0.0)
        self.current_equity: float = data.get("current_equity", 0.0)
        self.live_drawdown: float = data.get("live_drawdown", 0.0)
        self.max_dd_threshold: float = data.get("max_dd_threshold", 0.0)
        self.check_after_progress: float = data.get("check_after_progress", 0.20)
        self.error: str = data.get("error", "")
        self.result_dir: str = data.get("result_dir", "")
        self.stats: dict = data.get("stats", {})
        self.diagnosis_summary: str = data.get("diagnosis_summary", "")
        self.last_checked: str = data.get("last_checked", "")
        self.auto_download: bool = data.get("auto_download", True)
        self.auto_diagnose: bool = data.get("auto_diagnose", True)

    def to_dict(self) -> dict:
        return {
            "backtest_id": self.backtest_id,
            "project_id": self.project_id,
            "name": self.name,
            "strategy_file": self.strategy_file,
            "status": self.status,
            "submitted_at": self.submitted_at,
            "completed_at": self.completed_at,
            "progress": self.progress,
            "peak_equity": self.peak_equity,
            "current_equity": self.current_equity,
            "live_drawdown": self.live_drawdown,
            "max_dd_threshold": self.max_dd_threshold,
            "check_after_progress": self.check_after_progress,
            "error": self.error,
            "result_dir": self.result_dir,
            "stats": self.stats,
            "diagnosis_summary": self.diagnosis_summary,
            "last_checked": self.last_checked,
            "auto_download": self.auto_download,
            "auto_diagnose": self.auto_diagnose,
        }

    @property
    def is_active(self) -> bool:
        return self.status in ("pending", "running")

    @property
    def elapsed_minutes(self) -> float:
        if not self.submitted_at:
            return 0
        try:
            start = datetime.fromisoformat(self.submitted_at)
            return (datetime.now() - start).total_seconds() / 60
        except Exception:
            return 0


# =====================================================================
# PollerDaemon — the main background daemon
# =====================================================================
class PollerDaemon:
    """Background daemon that polls all active backtests."""

    def __init__(self):
        self.client = QCClient()
        self.running = True
        self._last_milestones: dict = {}
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    def _handle_signal(self, signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False

    # ================================================================
    # State file helpers (use file lock to prevent races)
    # ================================================================
    @staticmethod
    def load_state() -> dict:
        """Load state file (no lock — for read-only scenarios)."""
        return load_state_unlocked(STATE_FILE)

    @staticmethod
    def save_state(state: dict):
        """Write state file (no lock — caller must hold lock or be sole writer)."""
        save_state_unlocked(state, STATE_FILE)

    @staticmethod
    def add_backtest(
        backtest_id: str,
        name: str,
        strategy_file: str = "",
        max_dd: float = 0,
        project_id: int = None,
        auto_download: bool = True,
        auto_diagnose: bool = True,
    ):
        """Add a backtest to the tracking queue (with file lock)."""
        with state_file_lock(STATE_FILE):
            state = load_state_unlocked(STATE_FILE)

            bt = BacktestState()
            bt.backtest_id = backtest_id
            bt.project_id = project_id or DEFAULT_PROJECT_ID
            bt.name = name
            bt.strategy_file = strategy_file
            bt.status = "pending"
            bt.submitted_at = datetime.now().isoformat()
            bt.max_dd_threshold = max_dd
            bt.auto_download = auto_download
            bt.auto_diagnose = auto_diagnose

            state["backtests"].append(bt.to_dict())
            save_state_unlocked(state, STATE_FILE)
        logger.info(f"Added backtest: {name} ({backtest_id})")

    @staticmethod
    def get_active_backtests() -> list:
        """Return all active (pending/running) backtests."""
        state = PollerDaemon.load_state()
        return [
            BacktestState(bt)
            for bt in state.get("backtests", [])
            if bt.get("status") in ("pending", "running")
        ]

    @staticmethod
    def get_all_backtests() -> list:
        """Return all backtests (including completed)."""
        state = PollerDaemon.load_state()
        return [BacktestState(bt) for bt in state.get("backtests", [])]

    # ================================================================
    # Core polling logic
    # ================================================================
    def poll_once(self):
        """Execute one round of polling for all active backtests."""
        state = self.load_state()
        backtests = state.get("backtests", [])

        for bt_data in backtests:
            bt = BacktestState(bt_data)
            if not bt.is_active:
                continue

            # Orphan timeout: pending for more than 30 minutes is abnormal
            if bt.status == "pending" and bt.elapsed_minutes > 30:
                logger.warning(
                    f"{bt.name}: pending for over 30 minutes, marking as timeout"
                )
                bt.status = "timeout"
                bt.error = f"Pending for {bt.elapsed_minutes:.0f} minutes without starting"
                bt.completed_at = datetime.now().isoformat()
                self._update_backtest_in_state(bt)
                continue

            try:
                updated_bt = self._poll_single_backtest(bt)
                if updated_bt:
                    self._update_backtest_in_state(updated_bt)
            except Exception as e:
                logger.warning(f"Error checking {bt.name}: {e}")

    def _poll_single_backtest(self, bt: BacktestState) -> Optional[BacktestState]:
        """Poll a single backtest and return the updated state (None if unchanged)."""
        resp = self.client.read_backtest(bt.project_id, bt.backtest_id)
        bt_obj = resp.get("backtest", resp)

        # Update progress
        bt.progress = bt_obj.get("progress", 0)
        bt.status = "running" if bt.progress < 1.0 else "completed"
        bt.last_checked = datetime.now().isoformat()

        # Check for runtime errors
        error = bt_obj.get("error")
        if error:
            bt.status = "error"
            bt.error = str(error)[:500]
            bt.completed_at = datetime.now().isoformat()
            logger.error(f"{bt.name}: runtime error - {bt.error[:100]}")
            return bt

        # Equity tracking
        runtime_stats = bt_obj.get("runtimeStatistics", {})
        eq = parse_equity(runtime_stats.get("Equity"))
        if eq:
            bt.current_equity = eq
            if eq > bt.peak_equity:
                bt.peak_equity = eq

            # Live drawdown
            if bt.peak_equity > 0:
                bt.live_drawdown = (bt.peak_equity - eq) / bt.peak_equity

        # Drawdown early stop
        if (
            bt.max_dd_threshold > 0
            and bt.progress >= bt.check_after_progress
            and bt.live_drawdown > bt.max_dd_threshold
        ):
            logger.warning(
                f"{bt.name}: drawdown {bt.live_drawdown:.1%} exceeds threshold "
                f"{bt.max_dd_threshold:.0%}, triggering early stop!"
            )
            try:
                self.client.delete_backtest(bt.project_id, bt.backtest_id)
                logger.info("  Backtest deleted")
            except Exception as e:
                logger.warning(f"  Failed to delete backtest during early stop: {e}")

            bt.status = "early_stop"
            bt.error = (
                f"Drawdown {bt.live_drawdown:.1%} exceeded "
                f"threshold {bt.max_dd_threshold:.0%}"
            )
            bt.completed_at = datetime.now().isoformat()
            self._send_notification(bt)
            return bt

        # Completion handling
        if bt.progress >= 1.0:
            bt.status = "completed"
            bt.completed_at = datetime.now().isoformat()

            stats = bt_obj.get("statistics", {})
            bt.stats = stats

            elapsed = bt.elapsed_minutes
            logger.info(f"{bt.name}: backtest completed! (elapsed {elapsed:.0f} min)")

            for k in ["Net Profit", "Drawdown", "Sharpe Ratio", "Win Rate", "Total Orders"]:
                if k in stats:
                    logger.info(f"  {k}: {stats[k]}")

            if bt.auto_download:
                self._auto_download(bt)
            if bt.auto_diagnose and bt.result_dir:
                self._auto_diagnose(bt)

            self._send_notification(bt)

        else:
            # In progress — log at 10% milestones only (deduplicated)
            milestone = int(bt.progress * 10) * 10  # 0, 10, 20, ...
            if milestone > self._last_milestones.get(bt.backtest_id, -1):
                self._last_milestones[bt.backtest_id] = milestone
                eq_str = f"${bt.current_equity:,.0f}" if bt.current_equity else "?"
                dd_str = f"DD:{bt.live_drawdown:.1%}" if bt.live_drawdown > 0.01 else ""
                logger.info(
                    f"{bt.name}: {bt.progress * 100:.0f}% | "
                    f"Equity:{eq_str} {dd_str} | "
                    f"elapsed {bt.elapsed_minutes:.0f}min"
                )

        return bt

    def _update_backtest_in_state(self, bt: BacktestState):
        """Update a single backtest entry in state.json (with file lock)."""
        with state_file_lock(STATE_FILE):
            state = load_state_unlocked(STATE_FILE)
            backtests = state.get("backtests", [])
            for i, existing in enumerate(backtests):
                if existing.get("backtest_id") == bt.backtest_id:
                    backtests[i] = bt.to_dict()
                    break
            state["backtests"] = backtests
            save_state_unlocked(state, STATE_FILE)

    # ================================================================
    # Auto-download
    # ================================================================
    def _auto_download(self, bt: BacktestState):
        """Download backtest results (orders CSV + result JSON)."""
        try:
            result_dir = os.path.join(RESULTS_DIR, bt.name or bt.backtest_id[:8])
            os.makedirs(result_dir, exist_ok=True)

            # 1. Save full backtest result as JSON
            resp = self.client.read_backtest(bt.project_id, bt.backtest_id)
            json_path = os.path.join(result_dir, f"{bt.backtest_id}_result.json")
            with open(json_path, "w") as f:
                json.dump(resp, f, indent=2)

            # 2. Download orders in batches
            all_orders = []
            start_idx = 0
            limit = 100
            while True:
                orders_resp = self.client.read_backtest_orders(
                    bt.project_id, bt.backtest_id,
                    start=start_idx, end=start_idx + limit,
                )
                batch = orders_resp.get("orders", [])
                if not batch:
                    break
                all_orders.extend(batch)
                if len(batch) < limit:
                    break
                start_idx += limit

            # 3. Convert orders to CSV
            ORDER_TYPE = {
                0: "Market", 1: "Limit", 2: "StopMarket",
                3: "StopLimit", 4: "MarketOnOpen", 5: "MarketOnClose",
            }
            ORDER_STATUS = {
                0: "New", 1: "Submitted", 2: "PartiallyFilled",
                3: "Filled", 4: "Cancelled", 5: "Invalid",
            }
            DIRECTION = {0: "buy", 1: "sell"}

            csv_path = os.path.join(result_dir, f"{bt.backtest_id}_orders.csv")
            if all_orders:
                with open(csv_path, "w", newline="") as csvfile:
                    fieldnames = [
                        "orderId", "symbol", "type", "direction", "quantity",
                        "fillPrice", "status", "submitTime", "fillTime", "tag",
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for o in all_orders:
                        sym = o.get("symbol", {})
                        sym_str = (
                            sym.get("value", str(sym)) if isinstance(sym, dict)
                            else str(sym)
                        )
                        writer.writerow({
                            "orderId": o.get("id", ""),
                            "symbol": sym_str,
                            "type": ORDER_TYPE.get(o.get("type", ""), str(o.get("type", ""))),
                            "direction": DIRECTION.get(o.get("direction", ""), str(o.get("direction", ""))),
                            "quantity": o.get("quantity", 0),
                            "fillPrice": o.get("price", 0),
                            "status": ORDER_STATUS.get(o.get("status", ""), str(o.get("status", ""))),
                            "submitTime": o.get("time", ""),
                            "fillTime": o.get("lastFillTime", "") or o.get("time", ""),
                            "tag": o.get("tag", ""),
                        })

            bt.result_dir = result_dir
            logger.info(
                f"{bt.name}: results downloaded to {result_dir} "
                f"({len(all_orders)} orders)"
            )
        except Exception as e:
            logger.error(f"{bt.name}: download failed - {e}")

    # ================================================================
    # Auto-diagnose (optional — requires an external forensics module)
    # ================================================================
    def _auto_diagnose(self, bt: BacktestState):
        """Run forensic diagnosis on downloaded results.

        This is optional. If a forensics module is available on the Python path
        (e.g. from the qc-backtest-master skill or a custom module), it will be
        used. Otherwise, diagnosis is skipped gracefully.

        To integrate your own forensics, provide a module importable as:
            from order_forensics import OrderForensics
        with the interface:
            forensics = OrderForensics(orders_csv_path, result_json_path)
            report = forensics.full_diagnosis()
        """
        try:
            # Locate the orders CSV and result JSON
            orders_csv = None
            result_json = None
            for fname in os.listdir(bt.result_dir):
                if fname.endswith("_orders.csv"):
                    orders_csv = os.path.join(bt.result_dir, fname)
                if fname.endswith("_result.json"):
                    result_json = os.path.join(bt.result_dir, fname)

            if not orders_csv:
                logger.info(f"{bt.name}: no order data found, skipping diagnosis")
                return

            # Try to import a forensics module
            OrderForensics = None
            for module_path in [
                "order_forensics",
                "forensics",
            ]:
                try:
                    mod = __import__(module_path, fromlist=["OrderForensics"])
                    OrderForensics = getattr(mod, "OrderForensics", None)
                    if OrderForensics:
                        break
                except ImportError:
                    continue

            if OrderForensics is None:
                logger.info(
                    f"{bt.name}: no forensics module available, skipping diagnosis. "
                    "Install a compatible OrderForensics module to enable auto-diagnosis."
                )
                return

            forensics = OrderForensics(orders_csv, result_json)
            report = forensics.full_diagnosis()

            # Save diagnosis report
            report_path = os.path.join(bt.result_dir, "diagnosis.txt")
            with open(report_path, "w") as f:
                f.write(report)

            # Extract summary if the forensics module supports it
            try:
                tq = forensics.trade_quality()
                roi = forensics.roi_summary()
                bt.diagnosis_summary = (
                    f"Orders:{tq['total_orders']} | "
                    f"Option ROI:{roi['overall_roi']:.1%} | "
                    f"Zero rate:{tq['zero_rate']:.1%} | "
                    f"Big wins >400%:{tq['big_wins_400pct']}"
                )
            except Exception:
                bt.diagnosis_summary = "Diagnosis report generated"

            logger.info(f"{bt.name}: diagnosis complete -> {report_path}")
            if bt.diagnosis_summary:
                logger.info(f"  {bt.diagnosis_summary}")

            # NOTE: If you want an LLM summary (e.g. via OpenAI, Gemini, etc.),
            # add it here. The original implementation used Gemini Flash for a
            # 20-character summary. This has been removed to keep the skill
            # provider-agnostic. You can re-add it by checking for an API key
            # in the environment and calling the appropriate API.

        except Exception as e:
            logger.error(f"{bt.name}: diagnosis failed - {e}")

    # ================================================================
    # Notifications
    # ================================================================
    def _send_notification(self, bt: BacktestState):
        """Send a macOS system notification when a backtest finishes."""
        try:
            title = "Backtest Poller"
            message = f"Backtest {bt.name} finished ({bt.status})"
            os.system(
                f"""osascript -e 'display notification "{message}" with title "{title}"'"""
            )
            logger.info(f"Notification sent: {message}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    # ================================================================
    # Adaptive polling interval
    # ================================================================
    @staticmethod
    def _get_adaptive_interval(backtests: list) -> int:
        """Calculate the polling interval based on active backtest progress.

        Strategy:
          - Just submitted (progress=0, <2min elapsed):  30s  — confirm it started
          - Normal running (0-30%):                      120s — steady tracking
          - Midgame (30%-80%):                           180s — low frequency, save quota
          - Endgame (>80%):                              60s  — nearly done, check often

        A 3-hour backtest uses ~50 API calls instead of ~360.
        """
        if not backtests:
            return POLL_INTERVAL_RUNNING

        # Use the highest progress and lowest elapsed time among active backtests
        max_progress = 0.0
        min_elapsed = float("inf")
        for bt in backtests:
            p = bt.progress if isinstance(bt, BacktestState) else bt.get("progress", 0)
            e = bt.elapsed_minutes if isinstance(bt, BacktestState) else 0
            max_progress = max(max_progress, p)
            min_elapsed = min(min_elapsed, e)

        if max_progress == 0 and min_elapsed < 2:
            return POLL_INTERVAL_INITIAL   # 30s — confirm startup
        elif max_progress > 0.80:
            return POLL_INTERVAL_ENDGAME   # 60s — nearly done
        elif max_progress > 0.30:
            return POLL_INTERVAL_MIDGAME   # 180s — midgame, low frequency
        else:
            return POLL_INTERVAL_RUNNING   # 120s — normal

    # ================================================================
    # Main loop
    # ================================================================
    def run(self):
        """Main loop entry point."""
        logger.info("=" * 50)
        logger.info("Backtest Poller daemon started")
        logger.info(f"  PID: {os.getpid()}")
        logger.info(f"  State file: {STATE_FILE}")
        logger.info(f"  Log file: {LOG_FILE}")
        logger.info(f"  Polling strategy: adaptive (30s-180s)")
        logger.info("=" * 50)

        # Write PID (with lock)
        with state_file_lock(STATE_FILE):
            state = load_state_unlocked(STATE_FILE)
            state["poller_pid"] = os.getpid()
            state["poller_running"] = True
            state["poller_started"] = datetime.now().isoformat()
            save_state_unlocked(state, STATE_FILE)

        try:
            while self.running:
                active = self.get_active_backtests()
                if active:
                    self.poll_once()

                # Check if there are still active tasks
                active = self.get_active_backtests()
                if not active:
                    logger.info("No active backtests remaining, daemon exiting")
                    break

                interval = self._get_adaptive_interval(active)
                logger.debug(f"Next poll in {interval}s")
                time.sleep(interval)

        finally:
            with state_file_lock(STATE_FILE):
                state = load_state_unlocked(STATE_FILE)
                # Only clear PID if it still matches this process
                if state.get("poller_pid") == os.getpid():
                    state["poller_running"] = False
                    state["poller_pid"] = None
                    save_state_unlocked(state, STATE_FILE)
            logger.info("Backtest Poller stopped")


# ================================================================
# Entry point
# ================================================================
if __name__ == "__main__":
    daemon = PollerDaemon()
    daemon.run()
