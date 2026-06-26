from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from app.models.source import Source


class SourceLoader:
    """
    资讯来源配置加载器。
    """

    def __init__(self, file_path: str, sheet_name: str = "sources") -> None:
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name

        if not self.file_path.exists():
            raise FileNotFoundError(f"来源配置文件不存在: {self.file_path}")

    def load(self, enabled_only: bool = True) -> List[Source]:
        """
        读取 Excel 并转换为 Source 列表。
        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        df = df.fillna("")

        sources: List[Source] = []

        for _, row in df.iterrows():
            source_name = self._get_value(row, ["来源名称", "source_name"])
            url = self._get_value(row, ["网址/入口", "网址", "url"])

            if not source_name or not url:
                continue

            source = Source(
                source_name=source_name,
                source_type=self._get_value(row, ["来源类型", "source_type"]) or "other",
                url=url,
                coverage=self._get_value(row, ["覆盖范围", "coverage"]),
                priority=self._parse_int(self._get_value(row, ["优先级", "priority"]), default=5),
                enabled=self._parse_bool(self._get_value(row, ["是否启用", "enabled"]), default=True),
                fetch_method=self._get_value(row, ["抓取方式", "fetch_method"]) or "webpage",
                region_scope=self._get_value(row, ["地区", "region_scope"]),
            )
            sources.append(source)

        if enabled_only:
            sources = [s for s in sources if s.enabled]

        sources.sort(key=lambda x: x.priority)
        return sources

    @staticmethod
    def _get_value(row: pd.Series, candidate_columns: List[str]) -> str:
        for col in candidate_columns:
            if col in row.index:
                value = str(row[col]).strip()
                if value and value.lower() != "nan":
                    return value
        return ""

    @staticmethod
    def _parse_bool(value: str, default: bool = False) -> bool:
        if not value:
            return default

        normalized = value.strip().lower()
        true_values = {"是", "true", "yes", "y", "1"}
        false_values = {"否", "false", "no", "n", "0"}

        if normalized in true_values:
            return True
        if normalized in false_values:
            return False
        return default

    @staticmethod
    def _parse_int(value: str, default: int = 0) -> int:
        try:
            return int(float(str(value).strip()))
        except Exception:
            return default