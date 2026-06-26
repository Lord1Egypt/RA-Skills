#!/usr/bin/env python3
"""
法大大电子签 Python SDK (FASC API 5.0)

一键式电子合同签署解决方案
"""

from .client import FaDaDaClient
from .signer import Signer
from .exceptions import FaDaDaError, FaDaDaAuthError, FaDaDaAPIError

__version__ = "2.0.0"
__all__ = ["FaDaDaClient", "Signer", "FaDaDaError", "FaDaDaAuthError", "FaDaDaAPIError"]
