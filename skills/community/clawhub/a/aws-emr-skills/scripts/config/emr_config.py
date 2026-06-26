from __future__ import annotations

"""Unified EMR Skill configuration management.

This module provides unified configuration loading for all three AWS EMR deployment modes:

- **EMR Serverless**: Region, Application ID, Execution Role ARN, S3 Log URI;
- **EMR on EC2**: Region, Cluster ID;
- **EMR on EKS**: Region, Virtual Cluster ID, EKS Execution Role ARN.

Supports:

- Reading from environment variables;
- Optional loading from a simple local config file (KEY=VALUE format);
- Default job name prefix for convenience;
- Clear error messages when configuration is incomplete, without exposing sensitive credentials.

Environment variable conventions:

- ``AWS_REGION``: AWS region, defaults to ``us-east-1``;
- ``EMR_SERVERLESS_APP_ID``: EMR Serverless application ID (optional, needed for job submission);
- ``EMR_SERVERLESS_EXEC_ROLE_ARN``: IAM execution role ARN for Serverless job runs;
- ``EMR_SERVERLESS_S3_LOG_URI``: S3 URI for log output, e.g., ``s3://emr-serverless-log/logs/``;
- ``EMR_SERVERLESS_JOB_PREFIX``: Default job name prefix, defaults to ``emr-skill``;
- ``EMR_CLUSTER_ID``: EMR on EC2 cluster ID;
- ``EMR_EKS_VIRTUAL_CLUSTER_ID``: EMR on EKS virtual cluster ID;
- ``EMR_EKS_EXEC_ROLE_ARN``: IAM execution role ARN for EKS job runs;
- ``EMR_SKILL_CONFIG`` or ``EMR_SKILLS_CONFIG``: Optional config file path,
  file format is ``KEY=VALUE``, using the same key names as environment variables.

Note: AWS credentials are handled by boto3's default credential chain (environment variables,
AWS config files, IAM roles, etc.). No explicit access_key/secret_key fields are needed.
"""

import os
from dataclasses import dataclass
from typing import Dict, Iterable, Optional


class EMRSkillConfigError(Exception):
    """Error occurred when loading EMR Skill configuration."""


@dataclass
class EMRSkillConfig:
    """Unified configuration set for all EMR Skill deployment modes.

    All fields are optional at config load time and validated at point of use.

    Attributes:
        region: AWS region, e.g., ``us-east-1``.
        application_id: EMR Serverless application ID (optional).
        execution_role_arn: IAM execution role ARN for Serverless job runs (optional).
        s3_log_uri: S3 URI for log output (optional), e.g., ``s3://emr-serverless-log/logs/``.
        default_job_name_prefix: Default job name prefix, defaults to ``emr-skill``.
        cluster_id: EMR on EC2 cluster ID (optional).
        virtual_cluster_id: EMR on EKS virtual cluster ID (optional).
        eks_execution_role_arn: IAM execution role ARN for EKS job runs (optional).
    """

    region: str
    application_id: Optional[str] = None
    execution_role_arn: Optional[str] = None
    s3_log_uri: Optional[str] = None
    default_job_name_prefix: str = "emr-skill"
    # On EC2
    cluster_id: Optional[str] = None
    # On EKS
    virtual_cluster_id: Optional[str] = None
    eks_execution_role_arn: Optional[str] = None


def _load_simple_kv_file(path: str) -> Dict[str, str]:
    """Load a simple ``KEY=VALUE`` format configuration file.

    Returns an empty dict if the file doesn't exist or fails to read, without raising exceptions.
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
        # Fallback to environment variables only if config file read fails
        return {}

    return data


def _get_with_fallback(
    key: str,
    file_cfg: Dict[str, str],
    default: Optional[str] = None,
) -> Optional[str]:
    """Read from environment variable first, then config file, finally use default value."""

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


def load_emr_skill_config(config_file: Optional[str] = None) -> EMRSkillConfig:
    """Load EMR Skill configuration from environment variables and optional config file.

    Priority: environment variable > config file > built-in default value.

    All configuration fields are optional at load time. Fields like
    ``EMR_SERVERLESS_APP_ID``, ``EMR_CLUSTER_ID``, and ``EMR_EKS_VIRTUAL_CLUSTER_ID``
    are validated at point of use rather than at config load time.

    Args:
        config_file: Optional config file path (KEY=VALUE format). If not explicitly provided,
            will try environment variables ``EMR_SKILL_CONFIG`` and ``EMR_SKILLS_CONFIG`` in order.

    Returns:
        EMRSkillConfig: Parsed configuration object.

    Raises:
        EMRSkillConfigError: Raised when configuration file cannot be parsed.
    """

    file_path = (
        config_file or os.getenv("EMR_SKILL_CONFIG") or os.getenv("EMR_SKILLS_CONFIG")
    )
    file_cfg: Dict[str, str] = _load_simple_kv_file(file_path) if file_path else {}

    region = _get_with_fallback("AWS_REGION", file_cfg, "us-east-1") or "us-east-1"
    application_id = _get_with_fallback("EMR_SERVERLESS_APP_ID", file_cfg)
    execution_role_arn = _get_with_fallback("EMR_SERVERLESS_EXEC_ROLE_ARN", file_cfg)
    s3_log_uri = _get_with_fallback("EMR_SERVERLESS_S3_LOG_URI", file_cfg)
    job_prefix = (
        _get_with_fallback("EMR_SERVERLESS_JOB_PREFIX", file_cfg, "emr-skill")
        or "emr-skill"
    )

    # On EC2
    cluster_id = _get_with_fallback("EMR_CLUSTER_ID", file_cfg)

    # On EKS
    virtual_cluster_id = _get_with_fallback("EMR_EKS_VIRTUAL_CLUSTER_ID", file_cfg)
    eks_execution_role_arn = _get_with_fallback("EMR_EKS_EXEC_ROLE_ARN", file_cfg)

    return EMRSkillConfig(
        region=region,
        application_id=application_id,
        execution_role_arn=execution_role_arn,
        s3_log_uri=s3_log_uri,
        default_job_name_prefix=job_prefix,
        cluster_id=cluster_id,
        virtual_cluster_id=virtual_cluster_id,
        eks_execution_role_arn=eks_execution_role_arn,
    )
