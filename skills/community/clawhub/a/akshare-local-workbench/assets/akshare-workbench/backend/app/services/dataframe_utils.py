from __future__ import annotations

from typing import Any

import pandas as pd


def normalize_dataframe(value: Any) -> pd.DataFrame:
    if isinstance(value, pd.DataFrame):
        dataframe = value.copy()
    elif isinstance(value, pd.Series):
        dataframe = value.to_frame().reset_index()
    elif isinstance(value, list):
        dataframe = pd.DataFrame(value)
    elif isinstance(value, dict):
        dataframe = pd.DataFrame([value])
    else:
        dataframe = pd.DataFrame([{"value": value}])

    dataframe = dataframe.replace({pd.NA: None})
    dataframe = dataframe.where(pd.notnull(dataframe), None)
    return dataframe


# Column-name hints used to detect a date/time column for sorting.
_DATE_NAME_HINTS = ("日期", "date", "时间", "datetime", "交易日", "月份", "报告期", "年月")


def _find_date_column(dataframe: pd.DataFrame) -> tuple[str | None, "pd.Series | None"]:
    """Return (column_name, parsed_datetime_series) for the best date column, if any."""
    # 1) A real datetime dtype column wins.
    for column in dataframe.columns:
        if pd.api.types.is_datetime64_any_dtype(dataframe[column]):
            return column, dataframe[column]

    # 2) Otherwise look for a date-like column name that parses cleanly.
    for column in dataframe.columns:
        name = str(column).lower()
        if any(hint in name for hint in _DATE_NAME_HINTS):
            parsed = pd.to_datetime(dataframe[column], errors="coerce")
            if len(parsed) and parsed.notna().mean() >= 0.7:
                return column, parsed
    return None, None


def dataframe_preview(dataframe: pd.DataFrame, limit: int = 100) -> list[dict[str, Any]]:
    frame = dataframe
    # If the data is keyed by date, show the most recent rows first.
    date_column, parsed = _find_date_column(dataframe)
    if date_column is not None and parsed is not None:
        try:
            order = parsed.sort_values(ascending=False, kind="stable").index
            frame = dataframe.loc[order]
        except Exception:
            frame = dataframe

    preview_frame = frame.head(limit).copy()
    for column in preview_frame.columns:
        if pd.api.types.is_datetime64_any_dtype(preview_frame[column]):
            preview_frame[column] = preview_frame[column].astype(str)
    return preview_frame.to_dict(orient="records")
