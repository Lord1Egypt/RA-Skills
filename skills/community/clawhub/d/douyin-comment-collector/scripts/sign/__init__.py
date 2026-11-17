# -*- coding: utf-8 -*-
"""抖音 a_bogus 纯 Python 签名子包。

对外仅暴露 ``ABogusPureSigner``；``sm3`` / ``fingerprint`` 为内部依赖。
"""

from .ab_pure import ABogusPureSigner

__all__ = ["ABogusPureSigner"]
