from __future__ import annotations

from io import BytesIO

import pandas as pd

from app.models import ExportFormat


MEDIA_TYPES: dict[ExportFormat, str] = {
    "csv": "text/csv; charset=utf-8",
    "json": "application/json; charset=utf-8",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def export_dataframe(dataframe: pd.DataFrame, file_format: ExportFormat) -> bytes:
    if file_format == "csv":
        return dataframe.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

    if file_format == "json":
        return dataframe.to_json(orient="records", force_ascii=False, date_format="iso").encode(
            "utf-8"
        )

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="AKShare")
    return buffer.getvalue()
