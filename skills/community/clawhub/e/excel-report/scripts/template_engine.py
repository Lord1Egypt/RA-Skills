#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
template_engine.py — 模板引擎
excel-report Skill 核心模块

功能:
- 加载 JSON 模板配置
- 模板验证
- 计算字段求值
- 数据分组和聚合
- KPI 计算
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import json

import pandas as pd
import numpy as np


@dataclass
class TemplateValidationResult:
    """模板验证结果"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class TemplateEngine:
    """模板引擎"""
    
    # 必需的模板字段
    REQUIRED_FIELDS = ["id", "name", "industry", "sheets"]
    
    # 支持的聚合函数
    AGGREGATIONS = {
        "SUM": lambda x: x.sum(),
        "AVG": lambda x: x.mean(),
        "COUNT": lambda x: x.count(),
        "COUNT_DISTINCT": lambda x: x.nunique(),
        "MIN": lambda x: x.min(),
        "MAX": lambda x: x.max(),
        "STD": lambda x: x.std(),
        "VAR": lambda x: x.var(),
        "FIRST": lambda x: x.iloc[0] if len(x) > 0 else None,
        "LAST": lambda x: x.iloc[-1] if len(x) > 0 else None,
        "MODE": lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else None,
    }
    
    def __init__(self, template: Dict[str, Any]):
        self.template = template
        self.validation_result: Optional[TemplateValidationResult] = None
    
    def validate(self) -> TemplateValidationResult:
        """验证模板配置"""
        errors = []
        warnings = []
        
        for field in self.REQUIRED_FIELDS:
            if field not in self.template:
                errors.append(f"缺少必需字段: {field}")
        
        sheets = self.template.get("sheets", [])
        if not sheets:
            errors.append("sheets 列表为空")
        else:
            for idx, sheet in enumerate(sheets):
                sheet_errors = self._validate_sheet(sheet, idx)
                errors.extend(sheet_errors)
        
        self.validation_result = TemplateValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
        return self.validation_result
    
    def _validate_sheet(self, sheet: Dict[str, Any], idx: int) -> List[str]:
        """验证单个 sheet 配置"""
        errors = []
        sheet_name = sheet.get("name", f"Sheet{idx}")
        
        if "type" not in sheet:
            errors.append(f"Sheet '{sheet_name}': 缺少 type 字段")
        
        return errors
    
    def compute_fields(self, df: pd.DataFrame, sheet_config: Dict[str, Any]) -> pd.DataFrame:
        """计算字段"""
        computed_fields = sheet_config.get("computed_fields", [])
        
        for field_config in computed_fields:
            field_name = field_config.get("field")
            formula = field_config.get("formula", "")
            
            if not field_name or not formula:
                continue
            
            try:
                result = self._evaluate_formula(formula, df)
                df[field_name] = result
            except Exception as e:
                print(f"警告: 计算字段 '{field_name}' 失败: {e}")
        
        return df
    
    def _evaluate_formula(self, formula: str, df: pd.DataFrame) -> pd.Series:
        """求值公式"""
        formula = formula.strip()
        
        # 聚合函数
        agg_match = re.match(r"(\w+)\((\w+)\)", formula)
        if agg_match:
            func_name = agg_match.group(1).upper()
            col_name = agg_match.group(2)
            
            if func_name in self.AGGREGATIONS and col_name in df.columns:
                agg_value = self.AGGREGATIONS[func_name](df[col_name])
                return pd.Series([agg_value] * len(df))
        
        # LAG 函数
        if "LAG(" in formula:
            return self._evaluate_lag_formula(formula, df)
        
        # TOTAL 函数
        if "TOTAL(" in formula:
            return self._evaluate_total_formula(formula, df)
        
        # 简单列运算
        expr = formula
        for col in df.columns:
            expr = re.sub(rf"\b{col}\b", f"df['{col}']", expr)
        
        try:
            result = eval(expr)
            if isinstance(result, (int, float)):
                return pd.Series([result] * len(df))
            return result
        except Exception as e:
            # 返回空序列
            return pd.Series([np.nan] * len(df))
    
    def _evaluate_lag_formula(self, formula: str, df: pd.DataFrame) -> pd.Series:
        """求值 LAG 公式"""
        lag_pattern = r"LAG\((\w+),\s*(\d+)\)"
        
        def replace_lag(match):
            col = match.group(1)
            n = int(match.group(2))
            return f"df['{col}'].shift({n})"
        
        expr = re.sub(lag_pattern, replace_lag, formula)
        
        for col in df.columns:
            expr = re.sub(rf"\b{col}\b", f"df['{col}']", expr)
        
        try:
            return eval(expr)
        except:
            return pd.Series([np.nan] * len(df))
    
    def _evaluate_total_formula(self, formula: str, df: pd.DataFrame) -> pd.Series:
        """求值 TOTAL 公式"""
        total_pattern = r"TOTAL\((\w+)\)"
        
        def replace_total(match):
            col = match.group(1)
            return f"df['{col}'].sum()"
        
        expr = re.sub(total_pattern, replace_total, formula)
        
        for col in df.columns:
            expr = re.sub(rf"\b{col}\b", f"df['{col}']", expr)
        
        try:
            result = eval(expr)
            if isinstance(result, (int, float)):
                return pd.Series([result] * len(df))
            return result
        except:
            return pd.Series([np.nan] * len(df))
    
    def aggregate_data(self, df: pd.DataFrame, 
                       sheet_config: Dict[str, Any]) -> pd.DataFrame:
        """数据聚合"""
        group_by = sheet_config.get("group_by", [])
        aggregations = sheet_config.get("aggregations", {})
        
        if not group_by or not aggregations:
            return df
        
        # 确保所有分组列存在
        group_cols = [col for col in group_by if col in df.columns]
        if not group_cols:
            return df
        
        # 构建聚合字典
        agg_dict = {}
        for col, func_name in aggregations.items():
            if col in df.columns and func_name.upper() in self.AGGREGATIONS:
                agg_dict[col] = func_name.lower()
        
        if not agg_dict:
            return df
        
        try:
            return df.groupby(group_cols, as_index=False).agg(agg_dict)
        except Exception as e:
            print(f"聚合失败: {e}")
            return df
    
    def calculate_kpis(self, df: pd.DataFrame, 
                       kpi_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算 KPI 指标"""
        kpis = {}
        
        for kpi_config in kpi_configs:
            kpi_id = kpi_config.get("id", "")
            formula = kpi_config.get("formula", "")
            fmt = kpi_config.get("format", "number")
            
            if not formula:
                continue
            
            try:
                result = self._evaluate_formula(formula, df)
                value = result.iloc[0] if len(result) > 0 else 0
                
                # 格式化
                if fmt == "percent":
                    kpis[kpi_id] = f"{value:.1%}"
                elif fmt == "currency":
                    kpis[kpi_id] = f"¥{value:,.0f}"
                else:
                    kpis[kpi_id] = f"{value:,.0f}"
            except Exception as e:
                kpis[kpi_id] = "N/A"
        
        return kpis
    
    def sort_data(self, df: pd.DataFrame, 
                  sheet_config: Dict[str, Any]) -> pd.DataFrame:
        """数据排序"""
        sort_by = sheet_config.get("sort_by", [])
        
        if isinstance(sort_by, list) and sort_by:
            # 获取存在的列
            sort_cols = [col for col in sort_by if col in df.columns]
            if sort_cols:
                return df.sort_values(by=sort_cols)
        
        elif isinstance(sort_by, dict):
            col = sort_by.get("field")
            order = sort_by.get("order", "asc")
            if col and col in df.columns:
                return df.sort_values(by=col, ascending=(order == "asc"))
        
        return df


def load_template(template_path: Path) -> Dict[str, Any]:
    """加载模板配置文件"""
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python template_engine.py <template.json>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    template = load_template(path)
    
    engine = TemplateEngine(template)
    result = engine.validate()
    
    print(f"模板验证: {'✅ 有效' if result.valid else '❌ 无效'}")
    
    if result.errors:
        print("\n错误:")
        for e in result.errors:
            print(f"  - {e}")
    
    if result.warnings:
        print("\n警告:")
        for w in result.warnings:
            print(f"  - {w}")
