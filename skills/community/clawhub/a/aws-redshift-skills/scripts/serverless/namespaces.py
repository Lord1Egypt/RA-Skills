from __future__ import annotations

"""Redshift Serverless namespace management.

Provides :class:`RedshiftNamespaceManager` for managing Redshift Serverless
namespaces via the ``redshift-serverless`` boto3 client.
"""

import re
from typing import Any, Dict, List, Optional

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_redshift_serverless_client
from scripts.config.redshift_config import RedshiftSkillConfig


def _mask_secrets(text: str) -> str:
    """Mask potential AWS credentials and secrets in text."""
    text = re.sub(r"(AKIA[0-9A-Z]{16})", "AKIA****MASKED", text)
    text = re.sub(
        r"(?i)(secret[_-]?access[_-]?key\s*[:=]\s*)[^\s,\"']+",
        r"\1****MASKED",
        text,
    )
    return text


def _clean_namespace(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a boto3 Namespace response dict to snake_case."""
    return {
        "namespace_name": raw.get("namespaceName"),
        "namespace_arn": raw.get("namespaceArn"),
        "namespace_id": raw.get("namespaceId"),
        "status": raw.get("status"),
        "db_name": raw.get("dbName"),
        "admin_username": raw.get("adminUsername"),
        "creation_date": str(raw.get("creationDate", "")),
        "iam_roles": raw.get("iamRoles", []),
        "default_iam_role_arn": raw.get("defaultIamRoleArn"),
        "kms_key_id": raw.get("kmsKeyId"),
        "log_exports": raw.get("logExports", []),
    }


class RedshiftNamespaceManager:
    """Manages Redshift Serverless namespace operations.

    Attributes:
        config: Redshift skill configuration.
        client: boto3 Redshift Serverless client.
    """

    def __init__(self, config: RedshiftSkillConfig) -> None:
        self.config = config
        self.client = get_redshift_serverless_client(config.region)

    @classmethod
    def from_env(cls) -> "RedshiftNamespaceManager":
        """Create a manager from environment configuration."""
        from scripts.config.redshift_config import load_redshift_skill_config

        return cls(load_redshift_skill_config())

    def list_namespaces(self) -> List[Dict[str, Any]]:
        """List all Redshift Serverless namespaces.

        Returns:
            List of cleaned namespace dicts.
        """
        namespaces: List[Dict[str, Any]] = []
        next_token: Optional[str] = None

        try:
            while True:
                kwargs: Dict[str, Any] = {"maxResults": 100}
                if next_token:
                    kwargs["nextToken"] = next_token

                resp = self.client.list_namespaces(**kwargs)
                for ns in resp.get("namespaces", []):
                    namespaces.append(_clean_namespace(ns))

                next_token = resp.get("nextToken")
                if not next_token:
                    break
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

        return namespaces

    def get_namespace(
        self, namespace_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get namespace details.

        Args:
            namespace_name: Namespace name. Defaults to config namespace_name.

        Returns:
            Cleaned namespace detail dict.
        """
        ns_name = namespace_name or self.config.namespace_name
        if not ns_name:
            raise RuntimeError(
                "Namespace name required. Set REDSHIFT_NAMESPACE_NAME or pass namespace_name."
            )

        try:
            resp = self.client.get_namespace(namespaceName=ns_name)
            return _clean_namespace(resp.get("namespace", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def create_namespace(
        self,
        namespace_name: str,
        db_name: str = "dev",
        admin_username: Optional[str] = None,
        admin_user_password: Optional[str] = None,
        iam_roles: Optional[List[str]] = None,
        default_iam_role_arn: Optional[str] = None,
        kms_key_id: Optional[str] = None,
        log_exports: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new Redshift Serverless namespace.

        Args:
            namespace_name: Unique name for the namespace.
            db_name: Default database name.
            admin_username: Admin user name.
            admin_user_password: Admin user password.
            iam_roles: List of IAM role ARNs.
            default_iam_role_arn: Default IAM role ARN.
            kms_key_id: KMS key for encryption.
            log_exports: Log types to export ('useractivitylog', 'userlog', 'connectionlog').

        Returns:
            Cleaned namespace dict.
        """
        try:
            kwargs: Dict[str, Any] = {
                "namespaceName": namespace_name,
                "dbName": db_name,
            }
            if admin_username:
                kwargs["adminUsername"] = admin_username
            if admin_user_password:
                kwargs["adminUserPassword"] = admin_user_password
            if iam_roles:
                kwargs["iamRoles"] = iam_roles
            if default_iam_role_arn:
                kwargs["defaultIamRoleArn"] = default_iam_role_arn
            if kms_key_id:
                kwargs["kmsKeyId"] = kms_key_id
            if log_exports:
                kwargs["logExports"] = log_exports

            resp = self.client.create_namespace(**kwargs)
            return _clean_namespace(resp.get("namespace", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def delete_namespace(
        self,
        namespace_name: Optional[str] = None,
        final_snapshot_name: Optional[str] = None,
        final_snapshot_retention_period: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete a Redshift Serverless namespace.

        Args:
            namespace_name: Namespace name. Defaults to config namespace_name.
            final_snapshot_name: Optional final snapshot name.
            final_snapshot_retention_period: Retention period for final snapshot (days).

        Returns:
            Cleaned namespace dict.
        """
        ns_name = namespace_name or self.config.namespace_name
        if not ns_name:
            raise RuntimeError(
                "Namespace name required. Set REDSHIFT_NAMESPACE_NAME or pass namespace_name."
            )

        try:
            kwargs: Dict[str, Any] = {"namespaceName": ns_name}
            if final_snapshot_name:
                kwargs["finalSnapshotName"] = final_snapshot_name
            if final_snapshot_retention_period is not None:
                kwargs["finalSnapshotRetentionPeriod"] = final_snapshot_retention_period

            resp = self.client.delete_namespace(**kwargs)
            return _clean_namespace(resp.get("namespace", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc
