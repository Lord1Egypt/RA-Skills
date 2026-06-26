"""Unit tests for the fund tracker script."""

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check


class FundTrackerTests(unittest.TestCase):
    """Test local fund tracker behavior that does not require network access."""

    def test_detect_changes_handles_status_and_quota_edges(self) -> None:
        """Detect status changes and quota changes from or to missing values."""
        current = pd.DataFrame([
            {
                "基金代码": "000001",
                "基金简称": "Fund A",
                "申购状态": "开放申购",
                "日累计限定金额": 100.0,
            },
            {
                "基金代码": "000002",
                "基金简称": "Fund B",
                "申购状态": "暂停申购",
                "日累计限定金额": float("nan"),
            },
        ])
        history = {
            "000001": {"申购状态": "限大额", "日累计限定金额": None},
            "000002": {"申购状态": "暂停申购", "日累计限定金额": 100.0},
        }

        changes = check.detect_changes(current, history)

        self.assertEqual(changes, ["限大额→开放申购, 限额无→100", "限额100→无"])

    def test_build_current_state_normalizes_nan_values(self) -> None:
        """Convert pandas NaN values to JSON-safe None values."""
        current = pd.DataFrame([
            {
                "基金代码": "000001",
                "基金简称": "Fund A",
                "申购状态": "开放申购",
                "日累计限定金额": float("nan"),
                "手续费": float("nan"),
                "最新净值/万份收益": 1.23,
            },
        ])

        state = check.build_current_state(current)

        self.assertIsNone(state["000001"]["日累计限定金额"])
        self.assertIsNone(state["000001"]["手续费"])
        self.assertEqual(state["000001"]["最新净值"], 1.23)

    def test_run_returns_error_for_missing_preset(self) -> None:
        """Return a non-zero status when the requested preset does not exist."""
        with patch.object(check, "load_presets", return_value={"default": {"funds": []}}):
            with redirect_stdout(StringIO()):
                status = check.run("missing")

        self.assertEqual(status, 1)

    def test_missing_funds_keep_existing_history(self) -> None:
        """Keep previous history for funds missing from the latest data source."""
        current = pd.DataFrame([
            {
                "基金代码": "000001",
                "基金简称": "Fund A",
                "申购状态": "开放申购",
                "日累计限定金额": 100.0,
                "手续费": 0.0,
                "最新净值/万份收益": 1.23,
            },
        ])
        old_missing_state = {
            "基金简称": "Fund B",
            "申购状态": "暂停申购",
            "日累计限定金额": 100.0,
        }
        presets = {"default": {"label": "Default", "funds": ["000001", "000002"]}}
        history = {"000002": old_missing_state}

        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = Path(temp_dir) / "history_default.json"
            with (
                patch.object(check, "load_presets", return_value=presets),
                patch.object(check, "load_history", return_value=history),
                patch.object(check, "fetch_status", return_value=current),
                patch.object(check, "get_history_path", return_value=str(history_path)),
            ):
                with redirect_stdout(StringIO()):
                    status = check.run("default")

            saved = json.loads(history_path.read_text(encoding="utf-8"))

        self.assertEqual(status, 0)
        self.assertEqual(saved["000002"], old_missing_state)


if __name__ == "__main__":
    unittest.main()
