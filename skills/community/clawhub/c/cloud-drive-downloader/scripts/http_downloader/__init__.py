"""http_downloader - 通用 HTTP/HTTPS 直链下载模块（仅限已获授权或公开许可的内容）。

本模块只负责“把一条 http/https 直链下载到本地”。
- 不解析网盘分享链接
- 不绕过登录/验证码/防盗链/会员鉴权
- 不搜索盗版资源
- 保留用户责任确认与合规声明
"""

__version__ = "0.1.0"

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from .downloader import HTTPDownloader, DownloadReport
from .compliance import ComplianceError

__all__ = ["HTTPDownloader", "DownloadReport", "ComplianceError", "__version__"]
