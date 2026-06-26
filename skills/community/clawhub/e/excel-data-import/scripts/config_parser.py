#!/usr/bin/env python3
from typing import Any
# -*- coding: utf-8 -*-
"""
配置文件解析器

功能：解析和验证 YAML 配置文件
"""

from pathlib import Path

import yaml


def parse_config(config_path) -> Any:
    """解析配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        dict: 配置字典
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 设置默认值
    _set_default_values(config)

    # 解析相对路径为绝对路径（基于配置文件位置）
    config_dir = Path(config_path).parent
    source = config.get("source", {})
    if "file_path" in source and not Path(source["file_path"]).is_absolute():
        source["file_path"] = str(config_dir / source["file_path"])
    if "directory" in source and not Path(source["directory"]).is_absolute():
        source["directory"] = str(config_dir / source["directory"])

    target = config.get("target", {})
    if "file_path" in target and not Path(target["file_path"]).is_absolute():
        target["file_path"] = str(config_dir / target["file_path"])
    if "output_path" in target and not Path(target["output_path"]).is_absolute():
        target["output_path"] = str(config_dir / target["output_path"])

    # 多源模式路径解析
    for src in config.get("sources", []):
        if "file_path" in src and not Path(src["file_path"]).is_absolute():
            src["file_path"] = str(config_dir / src["file_path"])

    return config


def _set_default_values(config) -> None:
    """设置配置的默认值

    Args:
        config: 配置字典（会被修改）
    """
    # 源数据默认值
    # 处理自动检测模式
    if config["source"].get("header_row") == "auto" or config["source"].get("auto_detect_header"):
        # 保持为 "auto"，稍后在主脚本中处理
        pass
    elif "data_start_row" not in config["source"]:
        # 只有在不是 auto 模式时才设置默认值
        if isinstance(config["source"]["header_row"], int):
            config["source"]["data_start_row"] = config["source"]["header_row"] + 1

    # 目标模板默认值
    target = config.get("target", {})
    if target.get("header_row") == "auto" or target.get("auto_detect_header"):
        pass
    elif "data_start_row" not in target:
        if isinstance(target.get("header_row"), int):
            target["data_start_row"] = target["header_row"] + 1

    # 错误处理默认值
    if "error_handling" not in config:
        config["error_handling"] = {}

    error_handling = config["error_handling"]
    if "backup" not in error_handling:
        error_handling["backup"] = True
    if "backup_path" not in error_handling:
        error_handling["backup_path"] = "backup/"
    if "stop_on_error" not in error_handling:
        error_handling["stop_on_error"] = False
    if "log_errors" not in error_handling:
        error_handling["log_errors"] = True
    if "error_log_path" not in error_handling:
        error_handling["error_log_path"] = "logs/import_errors.log"

    # 选项默认值
    if "options" not in config:
        config["options"] = {}

    options = config["options"]
    if "preserve_formatting" not in options:
        options["preserve_formatting"] = True
    if "skip_merged_cells" not in options:
        options["skip_merged_cells"] = False


def validate_config(config) -> None:
    """验证配置文件

    Args:
        config: 配置字典

    Raises:
        ValueError: 如果配置无效
    """
    # 验证必需字段
    required_fields = ["task_name", "source", "target", "field_mappings"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"配置缺少必需字段: {field}")

    # 验证 source 配置（单文件或多源模式）
    if "sources" in config:
        # 多源模式
        for i, src in enumerate(config["sources"]):
            if "file_path" not in src:
                raise ValueError(f"sources[{i}] 配置缺少 file_path")
    elif "source" in config:
        source_required = ["file_path", "header_row", "key_field"]
        is_csv = Path(config["source"].get("file_path", "")).suffix.lower() == ".csv"
        is_dir = config["source"].get("type") == "directory" or "directory" in config["source"]
        for field in source_required:
            if field not in config["source"]:
                if field == "file_path" and is_dir:
                    continue
                raise ValueError(f"source 配置缺少必需字段: {field}")
        # sheet_name 对 CSV 和目录模式可选
        if "sheet_name" not in config["source"] and not is_csv and not is_dir:
            config["source"]["sheet_name"] = "Sheet"

        # 验证源文件存在（单文件模式）
        source_config = config["source"]
        is_dir_mode = source_config.get("type") == "directory" or "directory" in source_config
        if not is_dir_mode:
            source_path = Path(source_config.get("file_path", ""))
            if not source_path.exists():
                raise ValueError(f"源数据文件不存在: {source_path}")

    # 验证 target 配置
    target_required = ["output_path"]
    for field in target_required:
        if field not in config["target"]:
            raise ValueError(f"target 配置缺少必需字段: {field}")

    # 验证文件路径（仅单文件模式）
    source_config = config.get("source", {})
    is_dir_mode = source_config.get("type") == "directory" or "directory" in source_config
    if not is_dir_mode and "file_path" in source_config:
        source_path = Path(source_config["file_path"])
        if not source_path.exists():
            raise ValueError(f"源数据文件不存在: {source_path}")

    # 目标文件可以不存在（将自动创建模板）
    if "file_path" in config["target"]:
        target_path = Path(config["target"]["file_path"])
    else:
        target_path = None

    # 验证字段映射
    if not config["field_mappings"]:
        raise ValueError("field_mappings 不能为空")

    for mapping in config["field_mappings"]:
        if "source" not in mapping or "target" not in mapping:
            raise ValueError("字段映射必须包含 source 和 target 字段")


if __name__ == "__main__":
    # 测试配置解析
    import sys

    if len(sys.argv) < 2:
        print("用法: python config_parser.py <config_path>")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        validate_config(config)
        print("✓ 配置文件验证通过")
        print(f"任务名称: {config['task_name']}")

    except Exception as e:
        print(f"✗ 配置文件验证失败: {str(e)}")
        sys.exit(1)
