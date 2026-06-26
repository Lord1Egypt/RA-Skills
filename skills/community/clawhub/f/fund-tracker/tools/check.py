#!/usr/bin/env python3
"""Fund purchase status tracker."""

import json
import sys
from datetime import datetime
from pathlib import Path

import akshare as ak
import pandas as pd

TOOL_DIR = Path(__file__).resolve().parent
SKILL_ROOT = TOOL_DIR.parent
PRESETS_FILE = TOOL_DIR / "presets.json"
RUNTIME_DIR = SKILL_ROOT / "runtime"
DEFAULT_PRESET = "default"

SOURCE_COLUMNS = [
    "基金代码",
    "基金简称",
    "申购状态",
    "日累计限定金额",
    "手续费",
    "最新净值/万份收益",
    "最新净值/万份收益-报告时间",
]


def load_presets() -> dict[str, dict[str, object]]:
    """Load preset definitions."""
    with PRESETS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_history_path(preset_name: str) -> Path:
    """Get history file path for a specific preset."""
    return RUNTIME_DIR / f"history_{preset_name}.json"


def load_history(preset_name: str) -> dict[str, dict[str, object]]:
    """Load previous check results for a preset."""
    path = get_history_path(preset_name)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(preset_name: str, current: dict[str, dict[str, object]]) -> None:
    """Save current results as history for next comparison."""
    path = Path(get_history_path(preset_name))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)


def fetch_status(fund_codes: list[str]) -> pd.DataFrame:
    """Fetch purchase status for specified funds."""
    df = ak.fund_purchase_em()
    missing_columns = [column for column in SOURCE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"AKShare response missing columns: {missing_columns}")

    filtered_df = df[df["基金代码"].isin(fund_codes)][SOURCE_COLUMNS].copy()
    order = {code: index for index, code in enumerate(fund_codes)}
    filtered_df["__order"] = filtered_df["基金代码"].map(order)
    return filtered_df.sort_values("__order").drop(columns=["__order"]).reset_index(drop=True)


def normalize_number(value: object) -> float | None:
    """Convert numeric-like values to float and preserve missing values as None."""
    if value is None or pd.isna(value):
        return None
    return float(value)


def format_change_value(value: object) -> str:
    """Format a change value for compact display."""
    if value is None:
        return "无"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def build_current_state(current_df: pd.DataFrame) -> dict[str, dict[str, object]]:
    """Build normalized history state from current fund rows."""
    current_state = {}
    for _, row in current_df.iterrows():
        code = row["基金代码"]
        current_state[code] = {
            "基金简称": row["基金简称"],
            "申购状态": row["申购状态"],
            "日累计限定金额": normalize_number(row["日累计限定金额"]),
            "手续费": normalize_number(row["手续费"]),
            "最新净值": normalize_number(row["最新净值/万份收益"]),
            "检查时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    return current_state


def detect_changes(current_df: pd.DataFrame, history: dict[str, dict[str, object]]) -> list[str]:
    """Compare current status with history and return change descriptions."""
    changes = []
    for _, row in current_df.iterrows():
        code = row["基金代码"]
        status = row["申购状态"]
        quota = normalize_number(row["日累计限定金额"])
        if code not in history:
            changes.append("NEW")
        else:
            prev = history[code]
            parts = []
            if prev.get("申购状态") != status:
                parts.append(f"{prev.get('申购状态')}→{status}")
            prev_quota = normalize_number(prev.get("日累计限定金额"))
            if quota != prev_quota:
                parts.append(
                    f"限额{format_change_value(prev_quota)}→{format_change_value(quota)}"
                )
            changes.append(", ".join(parts) if parts else "-")
    return changes


def list_presets() -> int:
    """Print available presets as JSON."""
    presets = load_presets()
    output = []
    for name, preset in presets.items():
        funds = preset.get("funds", [])
        output.append({
            "name": name,
            "label": preset.get("label", name),
            "fund_count": len(funds) if isinstance(funds, list) else 0,
        })
    print(json.dumps({"presets": output}, ensure_ascii=False))
    return 0


def run(preset_name: str = DEFAULT_PRESET) -> int:
    """Run a fund status check for one preset."""
    presets = load_presets()
    if preset_name not in presets:
        print(json.dumps({
            "error": f"Preset '{preset_name}' not found",
            "available": list(presets.keys()),
        }, ensure_ascii=False))
        return 1

    preset = presets[preset_name]
    fund_codes = preset.get("funds")
    if not isinstance(fund_codes, list) or not all(isinstance(code, str) for code in fund_codes):
        print(json.dumps({
            "error": f"Preset '{preset_name}' has invalid funds list",
        }, ensure_ascii=False))
        return 1

    history = load_history(preset_name)
    current_df = fetch_status(fund_codes)
    changes = detect_changes(current_df, history)
    found_codes = set(current_df["基金代码"].tolist())
    missing_funds = [code for code in fund_codes if code not in found_codes]

    current_state = build_current_state(current_df)
    for code in missing_funds:
        if code in history:
            current_state[code] = history[code]

    save_history(preset_name, current_state)

    output = []
    for i, (_, row) in enumerate(current_df.iterrows()):
        output.append({
            "基金代码": row["基金代码"],
            "基金简称": row["基金简称"],
            "申购状态": row["申购状态"],
            "日限额": normalize_number(row["日累计限定金额"]),
            "手续费": normalize_number(row["手续费"]),
            "最新净值": normalize_number(row["最新净值/万份收益"]),
            "变化": changes[i],
        })
    print(json.dumps({
        "preset": preset_name,
        "label": preset["label"],
        "missing_funds": missing_funds,
        "data": output,
    }, ensure_ascii=False))
    return 0


def main(args: list[str]) -> int:
    """Parse command-line arguments and execute the requested action."""
    command = args[1] if len(args) > 1 else DEFAULT_PRESET
    try:
        if command == "list":
            return list_presets()
        return run(command)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
