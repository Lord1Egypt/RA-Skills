"""
Futu API skill - A wrapper for Futu OpenAPI trading and query.

This skill provides a convenient client for querying stock positions,
account info, placing orders, and more using Futu OpenAPI.
Requires FutuOpenD to be running on the local machine (127.0.0.1:11111).
"""

__version__ = "1.0.0"

from futu_client.client import FutuClient

__all__ = ["FutuClient"]
