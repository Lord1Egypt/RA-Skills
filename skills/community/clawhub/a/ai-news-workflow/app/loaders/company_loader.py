from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from app.models.company import Company


class CompanyLoader:
    """
    企业名单加载器。
    """

    def __init__(self, file_path: str, sheet_name: str = "company_list") -> None:
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name

        if not self.file_path.exists():
            raise FileNotFoundError(f"企业名单文件不存在: {self.file_path}")

    def load(self) -> List[Company]:
        """
        读取 Excel 并转换为 Company 列表。
        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        df = df.fillna("")

        companies: List[Company] = []

        for _, row in df.iterrows():
            company_cn = self._get_value(row, ["企业中文名", "公司中文名", "中文名"])
            if not company_cn:
                continue

            company = Company(
                company_cn=company_cn,
                company_en=self._get_value(row, ["企业英文名", "公司英文名", "英文名"]),
                short_name=self._get_value(row, ["企业简称", "简称"]),
                aliases=self._parse_aliases(self._get_value(row, ["常见别名", "别名"])),
                parent_company=self._get_value(row, ["母公司"]),
                country_region=self._get_value(row, ["国家/地区", "国家地区"]),
                is_key=self._parse_bool(self._get_value(row, ["重点关注", "是否重点关注"])),
                remarks=self._get_value(row, ["备注"]),
            )
            companies.append(company)

        return companies

    @staticmethod
    def _get_value(row: pd.Series, candidate_columns: List[str]) -> str:
        """
        按候选列名依次读取。
        """
        for col in candidate_columns:
            if col in row.index:
                value = str(row[col]).strip()
                if value and value.lower() != "nan":
                    return value
        return ""

    @staticmethod
    def _parse_aliases(alias_text: str) -> List[str]:
        """
        将别名字段解析为列表。
        支持分隔符：; ； , ， / |
        """
        if not alias_text:
            return []

        separators = [";", "；", ",", "，", "/", "|"]
        text = alias_text
        for sep in separators[1:]:
            text = text.replace(sep, separators[0])

        aliases = [item.strip() for item in text.split(separators[0]) if item.strip()]
        return aliases

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """
        将重点关注字段转为布尔值。
        """
        if not value:
            return False

        normalized = value.strip().lower()
        true_values = {"是", "true", "yes", "y", "1"}
        return normalized in true_values