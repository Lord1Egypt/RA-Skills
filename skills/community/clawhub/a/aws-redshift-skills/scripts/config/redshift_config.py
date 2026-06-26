from __future__ import annotations

"""Unified Redshift Skill configuration management.

This module provides unified configuration loading for AWS Redshift across two
deployment modes and the shared Data API:

- **Redshift Provisioned**: Region, Cluster ID, Database, DB User;
- **Redshift Serverless**: Region, Workgroup Name, Namespace Name;
- **Redshift Data API**: Shared by both modes for SQL execution.

Supports:

- Reading from environment variables;
- Optional loading from a simple local config file (KEY=VALUE format);
- Default values for common settings;
- Clear error messages when configuration is incomplete.

Environment variable conventions:

- ``AWS_REGION``: AWS region, defaults to ``us-east-1``;
- ``REDSHIFT_CLUSTER_ID``: Provisioned cluster identifier;
- ``REDSHIFT_DATABASE``: Database name, defaults to ``dev``;
- ``REDSHIFT_DB_USER``: Database user for provisioned mode;
- ``REDSHIFT_WORKGROUP_NAME``: Serverless workgroup name;
- ``REDSHIFT_NAMESPACE_NAME``: Serverless namespace name;
- ``REDSHIFT_IAM_ROLE_ARN``: IAM role for COPY/UNLOAD;
- ``REDSHIFT_S3_LOG_URI``: S3 path for query results/logs;
- ``REDSHIFT_SECRET_ARN``: Secrets Manager ARN for auth;
- ``REDSHIFT_SKILL_CONFIG``: Optional config file path (KEY=VALUE format).

Note: AWS credentials are handled by boto3's default credential chain (environment
variables, AWS config files, IAM roles, etc.). No explicit access_key/secret_key
fields are needed.
"""

import os
from dataclasses import dataclass
from typing import Dict, Iterable, Optional


class RedshiftSkillConfigError(Exception):
    """Error occurred when loading Redshift Skill configuration."""


@dataclass
class RedshiftSkillConfig:
    """Unified configuration set for Redshift Skill.

    All fields except ``region`` and ``database`` are optional at config load
    time and validated at point of use.

    Attributes:
        region: AWS region, e.g., ``us-east-1``.
        cluster_id: Provisioned cluster identifier (optional).
        database: Database name, defaults to ``dev``.
        db_user: Database user for provisioned mode (optional).
        workgroup_name: Serverless workgroup name (optional).
        namespace_name: Serverless namespace name (optional).
        iam_role_arn: IAM role ARN for COPY/UNLOAD (optional).
        s3_log_uri: S3 path for query results/logs (optional).
        secret_arn: Secrets Manager ARN for auth (optional).
    """

    region: str
    cluster_id: Optional[str] = None
    database: str = "dev"
    db_user: Optional[str] = None
    workgroup_name: Optional[str] = None
    namespace_name: Optional[str] = None
    iam_role_arn: Optional[str] = None
    s3_log_uri: Optional[str] = None
    secret_arn: Optional[str] = None


def _load_simple_kv_file(path: str) -> Dict[str, str]:
    """Load a simple ``KEY=VALUE`` format configuration file.

    Returns an empty dict if the file doesn't exist or fails to read,
    without raising exceptions.
    """
    data: Dict[str, str] = {}
    if not path or not os.path.exists(path):
        return data

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()
    except OSError:
        return {}

    return data


def _get_with_fallback(
    key: str,
    file_cfg: Dict[str, str],
    default: Optional[str] = None,
) -> Optional[str]:
    """Read from environment variable first, then config file, finally use default."""
    return os.getenv(key) or file_cfg.get(key, default)


def _get_any_of(
    keys: Iterable[str],
    file_cfg: Dict[str, str],
    default: Optional[str] = None,
) -> Optional[str]:
    """Select the first valid value from multiple keys in order.

    Priority: environment variable > config file > default value.
    """
    for k in keys:
        val = os.getenv(k) or file_cfg.get(k)
        if val:
            return val
    return default


def load_redshift_skill_config(
    config_file: Optional[str] = None,
) -> RedshiftSkillConfig:
    """Load Redshift Skill configuration from environment variables and optional config file.

    Priority: environment variable > config file > built-in default value.

    All configuration fields are optional at load time (except region which
    defaults to ``us-east-1``). Fields are validated at point of use.

    Args:
        config_file: Optional config file path (KEY=VALUE format). If not
            explicitly provided, will try environment variable
            ``REDSHIFT_SKILL_CONFIG``.

    Returns:
        RedshiftSkillConfig: Parsed configuration object.
    """
    cfg_path = config_file or os.getenv("REDSHIFT_SKILL_CONFIG", "")
    file_cfg = _load_simple_kv_file(cfg_path)

    region = _get_with_fallback("AWS_REGION", file_cfg, "us-east-1")

    return RedshiftSkillConfig(
        region=region,  # type: ignore[arg-type]
        cluster_id=_get_with_fallback("REDSHIFT_CLUSTER_ID", file_cfg),
        database=_get_with_fallback("REDSHIFT_DATABASE", file_cfg, "dev"),  # type: ignore[arg-type]
        db_user=_get_with_fallback("REDSHIFT_DB_USER", file_cfg),
        workgroup_name=_get_with_fallback("REDSHIFT_WORKGROUP_NAME", file_cfg),
        namespace_name=_get_with_fallback("REDSHIFT_NAMESPACE_NAME", file_cfg),
        iam_role_arn=_get_with_fallback("REDSHIFT_IAM_ROLE_ARN", file_cfg),
        s3_log_uri=_get_with_fallback("REDSHIFT_S3_LOG_URI", file_cfg),
        secret_arn=_get_with_fallback("REDSHIFT_SECRET_ARN", file_cfg),
    )
