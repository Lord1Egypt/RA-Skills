# -*- coding: utf-8 -*-
"""
数据加载模块（支持CSV/Excel）
"""

import pandas as pd
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from config import (
    TITLE_ROW_INDEX,
    MIN_LIMIT_ROW_NAME,
    MAX_LIMIT_ROW_NAME,
    RESULT_ROW_NAME
)


@dataclass
class ScatterConfig:
    """散点图配置"""
    item_name: str           # 第1列的Item名称
    column_title: str         # 对应列的列标题
    y_label: str             # Y轴标签（Limit Unit）
    min_limit: Optional[float] = None  # Min Limit值（None表示不存在）
    max_limit: Optional[float] = None  # Max Limit值（None表示不存在）
    result_data: List[float] = None  # Result行数据


class ExcelDataLoader:
    """Excel数据加载器"""

    def __init__(self, file_path: str):
        """
        初始化数据加载器

        Args:
            file_path: 数据文件路径（支持 .xls, .xlsx, .csv）
        """
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None
        self.title_row: Optional[pd.Series] = None
        self.title_dict: Dict[str, int] = {}  # {列标题: 列索引}

    def load(self) -> pd.DataFrame:
        """
        加载数据文件

        Returns:
            DataFrame对象
        """
        # 自动识别文件格式并加载
        file_ext = self.file_path.lower().split('.')[-1]

        if file_ext == 'csv':
            # CSV格式 - 尝试多种编码
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                try:
                    self.df = pd.read_csv(self.file_path, header=None, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                # 最后尝试不带编码
                self.df = pd.read_csv(self.file_path, header=None)
        elif file_ext == 'xlsx':
            self.df = pd.read_excel(self.file_path, header=None, engine='openpyxl')
        elif file_ext == 'xls':
            self.df = pd.read_excel(self.file_path, header=None, engine='xlrd')
        else:
            raise ValueError(f"不支持的文件格式: .{file_ext}，支持的格式: .csv, .xls, .xlsx")

        # 获取第22行标题（索引为21）
        self.title_row = self.df.iloc[TITLE_ROW_INDEX]

        # 构建标题索引字典
        for idx, title in enumerate(self.title_row):
            if pd.notna(title) and str(title).strip():
                self.title_dict[str(title).strip()] = idx

        return self.df

    def get_item_names(self) -> List[str]:
        """
        获取第1列的所有Item名称

        Returns:
            Item名称列表
        """
        if self.df is None:
            raise ValueError("请先调用load()方法加载数据")

        # 第1列（索引为0）的所有非空值
        item_col = self.df.iloc[:, 0]
        items = [str(item).strip() for item in item_col if pd.notna(item) and str(item).strip()]
        return items

    def get_scatter_configs(self) -> List[ScatterConfig]:
        """
        获取所有可用的散点图配置

        Returns:
            ScatterConfig列表
        """
        if self.df is None:
            raise ValueError("请先调用load()方法加载数据")

        configs = []

        # 找到Min Limit、Max Limit和Result行的索引
        min_limit_idx = self._find_row_index_by_name(MIN_LIMIT_ROW_NAME)
        max_limit_idx = self._find_row_index_by_name(MAX_LIMIT_ROW_NAME)
        result_idx = self._find_row_index_by_name(RESULT_ROW_NAME)

        # 打印调试信息
        print(f"      Result行索引: {result_idx}")
        print(f"      Min Limit行索引: {min_limit_idx}")
        print(f"      Max Limit行索引: {max_limit_idx}")

        # 获取第22行的列标题（从第2列开始，跳过Item列）
        column_titles = []
        for idx, title in enumerate(self.title_row):
            if idx == 0:  # 跳过第1列（Item名称列）
                continue
            if pd.notna(title) and str(title).strip():
                column_titles.append((str(title).strip(), idx))

        # 获取第1列的所有Item名称
        item_col = self.df.iloc[:, 0]

        # 为每个Item生成配置
        for item_idx, item_name in enumerate(item_col):
            if pd.isna(item_name) or not str(item_name).strip():
                continue

            item_name = str(item_name).strip()

            # 为该Item的每个列标题生成配置
            for col_title, col_idx in column_titles:
                # 获取Y轴标签（从列标题中提取单位）
                y_label = self._extract_unit_from_title(col_title)

                # 获取Min/Max Limit值
                min_limit = self._get_numeric_value(min_limit_idx, col_idx)
                max_limit = self._get_numeric_value(max_limit_idx, col_idx)

                # 获取Result数据
                result_data = self._get_result_values(result_idx, col_idx)

                # 只在有有效数据时生成配置
                # 条件：有Result数据即可（Limit不存在时只绘制散点图）
                if result_data:
                    configs.append(ScatterConfig(
                        item_name=item_name,
                        column_title=col_title,
                        y_label=y_label,
                        min_limit=min_limit,
                        max_limit=max_limit,
                        result_data=result_data
                    ))

        return configs

    def _find_row_index_by_name(self, row_name: str) -> Optional[int]:
        """根据行名查找行索引"""
        if self.df is None:
            return None

        for idx, row in self.df.iterrows():
            first_cell = str(row.iloc[0]).strip()
            if first_cell == row_name:
                return idx
        return None

    def _get_numeric_value(self, row_idx: Optional[int], col_idx: int) -> Optional[float]:
        """获取指定位置的数值"""
        if row_idx is None or self.df is None:
            return None

        try:
            value = self.df.iloc[row_idx, col_idx]
            if pd.notna(value):
                # 处理带单位的数值（如"5mV" -> 5）
                numeric_value = self._extract_numeric_value(value)
                return numeric_value
        except:
            pass
        return None

    def _get_result_values(self, result_idx: Optional[int], col_idx: int) -> List[float]:
        """获取Result行的所有数值（跳过空值）"""
        if result_idx is None or self.df is None:
            return []

        values = []
        try:
            value = self.df.iloc[result_idx, col_idx]
            if pd.notna(value):
                numeric_value = self._extract_numeric_value(value)
                if numeric_value is not None:
                    values.append(numeric_value)
        except:
            pass
        return values

    def _extract_numeric_value(self, value: Any) -> Optional[float]:
        """从带单位的值中提取数值"""
        if isinstance(value, (int, float)):
            return float(value)

        value_str = str(value).strip()

        # 尝试直接转换为数值
        try:
            return float(value_str)
        except ValueError:
            pass

        # 使用正则表达式提取数值
        match = re.match(r'^([+-]?\d+\.?\d*)', value_str)
        if match:
            return float(match.group(1))

        return None

    def _extract_unit_from_title(self, title: str) -> str:
        """
        从列标题中提取单位

        Args:
            title: 列标题，如 "1 CONT2(V)"

        Returns:
            单位字符串，如 "V"
        """
        # 匹配括号中的单位，如 CONT2(V) -> V
        match = re.search(r'\(([^)]+)\)', title)
        if match:
            return match.group(1)

        # 如果没有括号，返回整个标题
        return title
