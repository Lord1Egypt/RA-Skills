"""
CMS Connector Package

Multi-platform CMS connector abstraction layer.
Supports: WordPress, Shopify, Amazon SP-API, Magento, Custom sites.
"""

from .base_connector import (
    BaseCMSConnector,
    CMSCredentials,
    CMSResource,
    CMSOperation,
    CMSPlatform,
    CMSResult,
    CMSResourceType,
    CMSOperationType,
    CMSConnectionStatus,
    RiskLevel,
)

from .wordpress_connector import WordPressConnector
from .shopify_connector import ShopifyConnector
from .amazon_connector import AmazonConnector
from .magento_connector import MagentoConnector

__all__ = [
    "BaseCMSConnector",
    "CMSCredentials",
    "CMSResource",
    "CMSOperation",
    "CMSPlatform",
    "CMSResult",
    "CMSResourceType",
    "CMSOperationType",
    "CMSConnectionStatus",
    "RiskLevel",
    "WordPressConnector",
    "ShopifyConnector",
    "AmazonConnector",
    "MagentoConnector",
]
