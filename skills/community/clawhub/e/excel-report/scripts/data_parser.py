#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
data_parser.py — 数据解析器
excel-report Skill 核心模块

功能:
- 支持 xlsx, csv, json 数据格式导入
- 智能表头映射 (模糊匹配)
- 数据类型推断和转换
- 空值/异常值检测
- 数据诊断报告生成
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

try:
    from rapidfuzz import fuzz, process
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False


@dataclass
class DataParseResult:
    """数据解析结果"""
    dataframe: pd.DataFrame
    column_mapping: Dict[str, str]  # template_field -> actual_column
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)


class DataParser:
    """数据解析器"""
    
    # 数据类型映射
    TYPE_MAPPING = {
        "string": str,
        "number": float,
        "date": "datetime64[ns]",
        "percent": float,
        "currency": float,
    }
    
    def __init__(self, similarity_threshold: int = 60):
        """
        初始化解析器
        
        Args:
            similarity_threshold: 列名匹配相似度阈值 (0-100)
        """
        self.similarity_threshold = similarity_threshold
    
    def parse(self, data_path: Path, template: Dict[str, Any]) -> DataParseResult:
        """
        解析数据文件
        
        Args:
            data_path: 数据文件路径
            template: 模板配置
            
        Returns:
            DataParseResult 解析结果
        """
        errors = []
        warnings = []
        
        # 1. 读取数据
        df = self._read_data(data_path, errors)
        if df is None:
            return DataParseResult(
                dataframe=pd.DataFrame(),
                column_mapping={},
                errors=errors,
                warnings=warnings
            )
        
        # 2. 获取模板列配置
        template_columns = self._get_template_columns(template)
        
        # 3. 智能列名映射
        column_mapping, mapping_warnings = self._map_columns(
            df.columns.tolist(), 
            template_columns
        )
        warnings.extend(mapping_warnings)
        
        # 4. 类型转换
        df = self._convert_types(df, column_mapping, template_columns, warnings)
        
        # 5. 空值和异常值检测
        stats = self._analyze_data(df, column_mapping, template_columns)
        
        # 6. 应用默认值
        df = self._apply_defaults(df, template_columns)
        
        return DataParseResult(
            dataframe=df,
            column_mapping=column_mapping,
            errors=errors,
            warnings=warnings,
            stats=stats
        )
    
    def _read_data(self, path: Path, errors: List[str]) -> Optional[pd.DataFrame]:
        """读取数据文件"""
        suffix = path.suffix.lower()
        
        try:
            if suffix == ".xlsx":
                return pd.read_excel(path, engine="openpyxl")
            elif suffix == ".xls":
                return pd.read_excel(path, engine="xlrd")
            elif suffix == ".csv":
                # 尝试多种编码
                for encoding in ["utf-8", "gbk", "gb2312", "utf-8-sig"]:
                    try:
                        return pd.read_csv(path, encoding=encoding)
                    except UnicodeDecodeError:
                        continue
                errors.append("CSV编码识别失败，尝试: utf-8, gbk, gb2312")
                return None
            elif suffix == ".json":
                return pd.read_json(path)
            else:
                errors.append(f"不支持的文件格式: {suffix}")
                return None
        except Exception as e:
            errors.append(f"读取数据失败: {e}")
            return None
    
    def _get_template_columns(self, template: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取模板列配置"""
        columns = []
        for sheet in template.get("sheets", []):
            if sheet.get("type") == "data_input":
                columns.extend(sheet.get("columns", []))
        return columns
    
    def _map_columns(self, actual_columns: List[str], 
                     template_columns: List[Dict[str, Any]]) -> Tuple[Dict[str, str], List[str]]:
        """
        智能列名映射
        
        Returns:
            (mapping, warnings) mapping: template_field -> actual_column
        """
        mapping = {}
        warnings = []
        
        actual_lower = {col.lower().strip(): col for col in actual_columns}
        
        for tpl_col in template_columns:
            field = tpl_col.get("field")
            label = tpl_col.get("label", field)
            aliases = tpl_col.get("aliases", [label, field])
            required = tpl_col.get("required", False)
            
            matched = None
            
            # 1. 精确匹配 (优先级最高)
            for alias in aliases:
                alias_lower = alias.lower().strip()
                if alias_lower in actual_lower:
                    matched = actual_lower[alias_lower]
                    break
            
            # 2. 模糊匹配
            if not matched and HAS_RAPIDFUZZ and actual_columns:
                for alias in aliases:
                    result = process.extractOne(
                        alias, 
                        actual_columns,
                        scorer=fuzz.ratio
                    )
                    if result and result[1] >= self.similarity_threshold:
                        matched = result[0]
                        warnings.append(
                            f"列名模糊匹配: '{alias}' -> '{matched}' (相似度: {result[1]}%)"
                        )
                        break
            
            if matched:
                mapping[field] = matched
            elif required:
                warnings.append(f"缺少必需列: {label} ({field})")
        
        return mapping, warnings
    
    def _convert_types(self, df: pd.DataFrame, mapping: Dict[str, str],
                       template_columns: List[Dict[str, Any]], 
                       warnings: List[str]) -> pd.DataFrame:
        """类型转换"""
        col_config = {c["field"]: c for c in template_columns}
        
        for field, actual_col in mapping.items():
            if actual_col not in df.columns:
                continue
            
            config = col_config.get(field, {})
            dtype = config.get("type", "string")
            
            try:
                if dtype == "date":
                    df[actual_col] = pd.to_datetime(df[actual_col], errors="coerce")
                elif dtype == "number":
                    df[actual_col] = pd.to_numeric(df[actual_col], errors="coerce")
                elif dtype == "percent":
                    # 百分比可能是小数或字符串 "95%"
                    col_data = df[actual_col]
                    if col_data.dtype == object:
                        # 处理字符串格式百分比
                        df[actual_col] = col_data.astype(str).str.rstrip("%").astype(float) / 100
                    else:
                        df[actual_col] = pd.to_numeric(col_data, errors="coerce")
                elif dtype == "currency":
                    # 移除货币符号
                    if df[actual_col].dtype == object:
                        df[actual_col] = (
                            df[actual_col].astype(str)
                            .str.replace(r"[¥$€,]", "", regex=True)
                        )
                    df[actual_col] = pd.to_numeric(df[actual_col], errors="coerce")
            except Exception as e:
                warnings.append(f"列 '{actual_col}' 类型转换失败: {e}")
        
        return df
    
    def _analyze_data(self, df: pd.DataFrame, mapping: Dict[str, str],
                      template_columns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """数据分析"""
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "null_counts": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
        }
        
        # 数值列统计
        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            stats["numeric_summary"] = df[numeric_cols].describe().to_dict()
        
        return stats
    
    def _apply_defaults(self, df: pd.DataFrame, 
                        template_columns: List[Dict[str, Any]]) -> pd.DataFrame:
        """应用默认值"""
        for col_config in template_columns:
            field = col_config.get("field")
            default = col_config.get("default_values", {}).get(field)
            
            if default is not None and field in df.columns:
                df[field] = df[field].fillna(default)
        
        return df
    
    def generate_diagnostic_report(self, result: DataParseResult) -> str:
        """生成数据诊断报告"""
        lines = []
        lines.append("=" * 50)
        lines.append("📊 数据诊断报告")
        lines.append("=" * 50)
        
        df = result.dataframe
        stats = result.stats
        
        lines.append(f"\n总行数: {stats.get('total_rows', 0)}")
        lines.append(f"总列数: {stats.get('total_columns', 0)}")
        
        # 列映射
        if result.column_mapping:
            lines.append("\n列名映射:")
            for tpl_col, actual_col in result.column_mapping.items():
                lines.append(f"  {tpl_col} <- {actual_col}")
        
        # 空值统计
        null_counts = stats.get("null_counts", {})
        null_cols = {k: v for k, v in null_counts.items() if v > 0}
        if null_cols:
            lines.append("\n空值字段:")
            for col, count in null_cols.items():
                lines.append(f"  {col}: {count} 行")
        
        # 警告
        if result.warnings:
            lines.append("\n⚠️ 警告:")
            for w in result.warnings:
                lines.append(f"  - {w}")
        
        # 错误
        if result.errors:
            lines.append("\n❌ 错误:")
            for e in result.errors:
                lines.append(f"  - {e}")
        
        lines.append("\n" + "=" * 50)
        
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 便捷函数
# ---------------------------------------------------------------------------

def parse_data(data_path: Path, template: Dict[str, Any]) -> DataParseResult:
    """便捷函数: 解析数据"""
    parser = DataParser()
    return parser.parse(data_path, template)


# ---------------------------------------------------------------------------
# CLI 测试
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python data_parser.py <data_file>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    
    # 使用简单模板测试
    test_template = {
        "sheets": [{
            "type": "data_input",
            "columns": [
                {"field": "date", "label": "日期", "type": "date", "required": True},
                {"field": "sales", "label": "销售额", "type": "number"},
            ]
        }]
    }
    
    parser = DataParser()
    result = parser.parse(path, test_template)
    
    print(parser.generate_diagnostic_report(result))
