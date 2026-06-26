"""
配置管理模块

Infrastructure 层的配置加载功能。
环境变量读取属于 I/O 操作，归属于 Infrastructure 层。

架构原则：
- Domain 层不直接导入 settings
- 配置通过 Application 层的 bootstrap 注入到 Domain 层
"""

from .settings import (
    # 配置类
    CheckerConfig,
    # 路径配置
    DEFAULT_DOCUMENT_PATH,
    DEFAULT_OUTPUT_DIR,
    generate_output_path,
    scan_default_documents,
    # OCR 配置
    get_ocr_backend,
    get_aliyun_ocr_credentials,
)
from .secret_ref import (
    # SecretRef 相关
    SecretRef,
    SecretRefResolver,
    SecretRefError,
    parse_secret_ref,
    resolve_secret,
)

__all__ = [
    "CheckerConfig",
    "DEFAULT_DOCUMENT_PATH",
    "DEFAULT_OUTPUT_DIR",
    "generate_output_path",
    "scan_default_documents",
    "get_ocr_backend",
    "get_aliyun_ocr_credentials",
    # SecretRef
    "SecretRef",
    "SecretRefResolver",
    "SecretRefError",
    "parse_secret_ref",
    "resolve_secret",
]
