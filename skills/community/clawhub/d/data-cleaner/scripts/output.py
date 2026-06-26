"""
F6 · Output module.
Exports cleaned data and quality reports to:
  - Excel (.xlsx)
  - CSV
  - Feishu Bitable (multi-dimensional table)
  - Feishu Cloud Document (quality report)

Usage:
    from output import DataExporter

    exporter = DataExporter(df, field_info)
    path = exporter.to_excel("/tmp/cleaned.xlsx")
    path = exporter.to_csv("/tmp/cleaned.csv")
    bitable_url = exporter.to_bitable(table_name="清洗结果")
    doc_url = exporter.to_feishu_doc(report_markdown, title="数据质量报告")
"""

import os
import io
import time
import base64
import tempfile
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import pandas as pd

# ─── Exceptions ─────────────────────────────────────────────────────────────────

class ExportError(Exception):
    pass

# ─── Field type → Bitable field type mapping ───────────────────────────────────

LARK_FIELD_TYPES: Dict[str, int] = {
    "text":       1,
    "number":     2,
    "single_select": 3,
    "multi_select":  4,
    "date":       5,
    "checkbox":   7,
    "person":     11,
    "phone":      13,
    "url":        15,
    "attachment": 17,
    "created_time": 1001,
    "modified_time": 1002,
}

def _infer_bitable_field_type(field_type_str: str) -> int:
    """Map our FieldType label to Feishu Bitable field type ID."""
    mapping: Dict[str, int] = {
        "姓名": 1, "手机号": 13, "邮箱": 1, "地址": 1,
        "金额": 2, "日期": 5, "SKU": 1, "订单号": 1,
        "身份证": 1, "性别": 3, "网址": 15, "IP地址": 1,
        "银行账号": 1, "文本": 1, "数字": 2, "未知": 1,
        "标签": 4,  # tag column → multi-select
    }
    return mapping.get(field_type_str, 1)

# ─── DataExporter ───────────────────────────────────────────────────────────────

class DataExporter:
    """
    Export cleaned DataFrame to various formats.

    Parameters
    ----------
    df         : cleaned DataFrame
    field_info : Dict[col -> FieldInfo] for type hints
    tier       : subscription tier (for feature gating)
    """

    def __init__(
        self,
        df: pd.DataFrame,
        field_info: Optional[Dict] = None,
        tier: str = "free",
    ):
        self.df         = df.copy()
        self.field_info = field_info or {}
        self.tier       = tier

    # ─── Excel ─────────────────────────────────────────────────────────────────

    def to_excel(
        self,
        path: Optional[str] = None,
        sheet_name: str = "清洗结果",
    ) -> str:
        """
        Write DataFrame to .xlsx file.
        Returns the file path.
        """
        if path is None:
            path = tempfile.mktemp(suffix=".xlsx")

        try:
            import openpyxl
        except ImportError:
            raise ExportError(
                "openpyxl 未安装。请运行：pip install openpyxl"
            )

        # Use xlsxwriter if available for better formatting
        try:
            import xlsxwriter  # noqa: F401
            self.df.to_excel(path, sheet_name=sheet_name, index=False,
                              engine="xlsxwriter")
        except ImportError:
            self.df.to_excel(path, sheet_name=sheet_name, index=False,
                              engine="openpyxl")

        return path

    def to_csv(
        self,
        path: Optional[str] = None,
        encoding: str = "utf-8-sig",
    ) -> str:
        """
        Write DataFrame to CSV file.
        Returns the file path.
        """
        if path is None:
            path = tempfile.mktemp(suffix=".csv")

        self.df.to_csv(path, index=False, encoding=encoding)
        return path

    def to_base64_csv(self, encoding: str = "utf-8-sig") -> str:
        """Return CSV as base64-encoded string (for file attachments)."""
        buf = io.StringIO()
        self.df.to_csv(buf, index=False, encoding=encoding)
        return base64.b64encode(buf.getvalue().encode(encoding)).decode()

    def to_base64_excel(self) -> str:
        """Return Excel as base64-encoded string."""
        buf = io.BytesIO()
        self.df.to_excel(buf, index=False, engine="openpyxl")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()

    # ─── Feishu Bitable ────────────────────────────────────────────────────────

    def to_bitable(
        self,
        table_name: str = "清洗结果",
        folder_token: Optional[str] = None,
        open_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a Feishu Bitable app and write data into it.
        Requires Feishu API credentials.

        Returns dict with app_token, table_id, url.

        Raises ExportError if Bitable creation fails.
        """
        # Check tier
        if self.tier not in ("std", "pro"):
            raise ExportError(
                "飞书多维表格导出仅在标准版/专业版可用。"
                "请升级以解锁此功能。"
            )

        # Lazy import feishu tools to avoid hard dependency
        try:
            from feishu_bitable_app import feishu_bitable_app
            from feishu_bitable_app_table import feishu_bitable_app_table
            from feishu_bitable_app_table_record import feishu_bitable_app_table_record
        except ImportError:
            raise ExportError(
                "飞书多维表格模块不可用。"
                "请确认已安装 feishu-bitable skill 并重启服务。"
            )

        # 1. Create the Bitable app
        app_result = feishu_bitable_app(
            action="create",
            name=f"数据清洗_{table_name}",
            folder_token=folder_token or "",
        )
        if not app_result.get("app_token"):
            raise ExportError(f"创建多维表格失败：{app_result}")
        app_token = app_result["app_token"]

        # 2. Define fields
        fields_def = self._build_bitable_fields()

        # 3. Create the table with fields
        table_result = feishu_bitable_app_table(
            action="create",
            app_token=app_token,
            table={"name": table_name, "fields": fields_def},
        )
        table_id = table_result.get("table_id", "")

        # 4. Batch write records (max 500 per call)
        records = self._df_to_records()
        BATCH = 500
        for i in range(0, len(records), BATCH):
            batch = records[i:i + BATCH]
            feishu_bitable_app_table_record(
                action="batch_create",
                app_token=app_token,
                table_id=table_id,
                records=[{"fields": r} for r in batch],
            )

        url = f"https://aiplayer.feishu.cn/bitable/{app_token}"
        return {
            "app_token": app_token,
            "table_id":  table_id,
            "url":       url,
            "rows_written": len(records),
        }

    def _build_bitable_fields(self) -> List[Dict]:
        """Build field definitions for Bitable table creation."""
        fields = []
        for col in self.df.columns:
            type_label = "文本"
            if col in self.field_info:
                type_label = self.field_info[col].label() if hasattr(
                    self.field_info[col], "label"
                ) else str(self.field_info[col])
            elif "标签" in col:
                type_label = "标签"

            # Map to bitable type ID
            bitable_type = _infer_bitable_field_type(type_label)
            field_def: Dict[str, Any] = {
                "field_name": str(col),
                "type": bitable_type,
            }
            # Single-select needs options
            if bitable_type == 3:
                unique_vals = self.df[col].dropna().unique().tolist()[:20]
                field_def["property"] = {
                    "options": [
                        {"name": str(v)[:50]} for v in unique_vals
                    ]
                }
            fields.append(field_def)
        return fields

    def _df_to_records(self) -> List[Dict[str, Any]]:
        """Convert DataFrame rows to Bitable record format."""
        records = []
        for _, row in self.df.iterrows():
            fields: Dict[str, Any] = {}
            for col, val in row.items():
                s = str(val)
                if s in ("", "nan", "NaN", "None", "未知"):
                    fields[str(col)] = None
                elif "标签" in str(col):
                    # Multi-select: split by semicolon
                    tags = [t.strip() for t in s.split(";") if t.strip()]
                    fields[str(col)] = tags
                else:
                    fields[str(col)] = s
            records.append(fields)
        return records

    # ─── Feishu Cloud Document (report) ─────────────────────────────────────────

    def to_feishu_doc(
        self,
        report_markdown: str,
        title: str = "数据质量报告",
        folder_token: Optional[str] = None,
        wiki_space_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a Feishu Cloud Document with the quality report.
        Returns dict with doc_token, url.
        """
        try:
            from feishu_create_doc import feishu_create_doc
        except ImportError:
            raise ExportError(
                "飞书文档模块不可用。"
                "请确认已安装 feishu-create-doc skill 并重启服务。"
            )

        result = feishu_create_doc(
            markdown=report_markdown,
            title=title,
            folder_token=folder_token or "",
            wiki_space=wiki_space_id or "",
        )

        if result.get("task_id"):
            # Async creation — poll
            doc_token = self._poll_doc_task(result["task_id"])
        else:
            doc_token = result.get("document_id", "")

        url = f"https://aiplayer.feishu.cn/docx/{doc_token}"
        return {
            "document_id": doc_token,
            "url":         url,
        }

    def _poll_doc_task(self, task_id: str, timeout: int = 30) -> str:
        """Poll async doc creation task until done."""
        from feishu_create_doc import feishu_create_doc
        start = time.time()
        while time.time() - start < timeout:
            result = feishu_create_doc(task_id=task_id)
            status = result.get("status", "")
            if status == "success" or "document_id" in result:
                return result.get("document_id", result.get("doc_token", ""))
            time.sleep(2)
        raise ExportError("文档创建超时，请稍后重试。")


# ─── Convenience functions ──────────────────────────────────────────────────────

def export_excel(df: pd.DataFrame, path: str) -> str:
    exp = DataExporter(df)
    return exp.to_excel(path)

def export_csv(df: pd.DataFrame, path: str) -> str:
    exp = DataExporter(df)
    return exp.to_csv(path)
