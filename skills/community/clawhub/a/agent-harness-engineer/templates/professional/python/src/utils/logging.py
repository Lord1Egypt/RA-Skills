"""
日志模块
规模: Professional
预期行数: ~50行

## ⚠ AI构建提示
根据用户需求生成以下内容:
1. 使用 Python logging 标准库
2. 提供 get_logger(name) 工厂函数
3. 支持从配置文件中读取日志级别和输出目标
4. 格式: "[时间] [级别] [模块名] 消息"

⚠ 仅使用标准库 logging, 不引入第三方日志库
⚠ 默认输出到 stderr, 可选输出到文件
⚠ 支持 LOG_LEVEL 环境变量覆盖
"""

import logging
import sys
from typing import Optional

# TODO: 实现日志配置
# def setup_logging(level: str = "INFO", log_file: Optional[str] = None): ...
# def get_logger(name: str) -> logging.Logger: ...
pass