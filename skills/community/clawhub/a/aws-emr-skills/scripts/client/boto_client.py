"""Boto3 client factory for AWS EMR services.

Provides factory functions for creating boto3 clients using the default
credential chain. Each function accepts an optional ``region`` parameter;
if not provided, the region is loaded from ``EMRSkillConfig``.

No explicit access key / secret key fields are used — authentication is
handled entirely by boto3's default credential chain (environment variables,
AWS config files, IAM roles, etc.).
"""

from __future__ import annotations

from typing import Any, Optional

import boto3

from scripts.config.emr_config import load_emr_skill_config


def _resolve_region(region: Optional[str] = None) -> str:
    """Resolve the AWS region from the argument or config.

    Args:
        region: Explicit region override. If None, loads from config.

    Returns:
        AWS region string.
    """
    if region:
        return region
    config = load_emr_skill_config()
    return config.region


def get_emr_serverless_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for EMR Serverless.

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 EMR Serverless client.
    """
    return boto3.client("emr-serverless", region_name=_resolve_region(region))


def get_emr_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for EMR (On EC2).

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 EMR client.
    """
    return boto3.client("emr", region_name=_resolve_region(region))


def get_emr_containers_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for EMR Containers (On EKS).

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 EMR Containers client.
    """
    return boto3.client("emr-containers", region_name=_resolve_region(region))


def get_s3_client(region: Optional[str] = None) -> Any:
    """Create a boto3 client for Amazon S3.

    Args:
        region: Optional AWS region override. Defaults to config region.

    Returns:
        boto3 S3 client.
    """
    return boto3.client("s3", region_name=_resolve_region(region))
