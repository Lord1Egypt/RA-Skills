#!/usr/bin/env python3
from typing import Any
# -*- coding: utf-8 -*-
"""
验证引擎

功能：验证导入数据的完整性和正确性
"""

import re


class ValidationReport:
    """验证报告"""

    def __init__(self) -> None:
        self.total = 0
        self.successful = 0
        self.failed = 0
        self.warnings = []


def validate_data(data, validations) -> Any:
    """验证数据

    Args:
        data: 待验证的数据字典
        validations: 验证规则列表

    Returns:
        tuple: (is_valid, errors)
    """
    errors = []

    for validation in validations:
        field = validation["field"]
        rules = validation.get("rules", [])

        for rule in rules:
            rule_type = rule.get("type")
            error = None

            if rule_type == "required":
                error = _validate_required(field, data)
            elif rule_type == "format":
                pattern = rule.get("pattern")
                error = _validate_format(field, data, pattern)
            elif rule_type == "unique":
                validation_result = _validate_unique(
                    field, data
                )  # pylint: disable=assignment-from-none
                if validation_result is not None:
                    error = validation_result

            if error:
                errors.append(error)

    return len(errors) == 0, errors


def _validate_required(field, data) -> Any:
    """验证必填字段"""
    if field not in data or not data[field]:
        return f"必填字段 '{field}' 为空"
    return None


def _validate_format(field, data, pattern) -> Any:
    """验证字段格式"""
    if field in data and data[field]:
        value = str(data[field])
        if not re.match(pattern, value):
            return f"字段 '{field}' 格式错误: {value}"
    return None


def _validate_unique(field, data) -> Any:
    """验证字段唯一性（需要在更高层次处理）"""
    # 这里只返回 None，实际唯一性验证需要在数据导入时进行
    return None
