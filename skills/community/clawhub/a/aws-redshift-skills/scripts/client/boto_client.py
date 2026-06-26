"""Boto3 client factory for AWS Redshift services.

Provides factory functions for creating boto3 clients using the default
credential chain. Each function accepts an optional ``region`` parameter;
if not provided, the region is loaded from ``RedshiftSkillConfig``.

No explicit access key / secret key fields are used — authentication is
handled entirely by boto3's default credential chain (environment variables,
AWS config files, IAM roles, etc.).
"""

from __future__ import annotations

from typing import Any, Optional

import boto3

from scripts.config.redshift_config import load_redshift_skill_config


def _resolve_region(region: Optional[str] = None) -> str:
    """Resolve the AWS region from the argument or config.

    Args:
        region: Explicit region override. If None, loads from config.

    Returns:
        AWS region string.
    """
    if region:
        return region
    config = load_redshift_skill_config()
    return config.region


def get_redshift_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for Redshift (provisioned cluster management).

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 Redshift client.
    """
    return boto3.client("redshift", region_name=_resolve_region(region))


def get_redshift_serverless_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for Redshift Serverless.

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 Redshift Serverless client.
    """
    return boto3.client("redshift-serverless", region_name=_resolve_region(region))


def get_redshift_data_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for Redshift Data API.

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 Redshift Data API client.
    """
    return boto3.client("redshift-data", region_name=_resolve_region(region))


def get_s3_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for Amazon S3.

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 S3 client.
    """
    return boto3.client("s3", region_name=_resolve_region(region))
