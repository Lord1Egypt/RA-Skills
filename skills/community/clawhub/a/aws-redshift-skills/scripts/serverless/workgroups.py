from __future__ import annotations

"""Redshift Serverless workgroup management.

Provides :class:`RedshiftWorkgroupManager` for managing Redshift Serverless
workgroups via the ``redshift-serverless`` boto3 client.
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


def _clean_workgroup(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a boto3 Workgroup response dict to snake_case."""
    endpoint = raw.get("endpoint", {}) or {}
    return {
        "workgroup_name": raw.get("workgroupName"),
        "workgroup_arn": raw.get("workgroupArn"),
        "workgroup_id": raw.get("workgroupId"),
        "namespace_name": raw.get("namespaceName"),
        "status": raw.get("status"),
        "base_capacity": raw.get("baseCapacity"),
        "max_capacity": raw.get("maxCapacity"),
        "endpoint": {
            "address": endpoint.get("address"),
            "port": endpoint.get("port"),
        }
        if endpoint
        else None,
        "publicly_accessible": raw.get("publiclyAccessible"),
        "security_group_ids": raw.get("securityGroupIds", []),
        "subnet_ids": raw.get("subnetIds", []),
        "creation_date": str(raw.get("creationDate", "")),
        "enhanced_vpc_routing": raw.get("enhancedVpcRouting"),
    }


class RedshiftWorkgroupManager:
    """Manages Redshift Serverless workgroup operations.

    Attributes:
        config: Redshift skill configuration.
        client: boto3 Redshift Serverless client.
    """

    def __init__(self, config: RedshiftSkillConfig) -> None:
        self.config = config
        self.client = get_redshift_serverless_client(config.region)

    @classmethod
    def from_env(cls) -> "RedshiftWorkgroupManager":
        """Create a manager from environment configuration."""
        from scripts.config.redshift_config import load_redshift_skill_config

        return cls(load_redshift_skill_config())

    def list_workgroups(self) -> List[Dict[str, Any]]:
        """List all Redshift Serverless workgroups.

        Returns:
            List of cleaned workgroup dicts.
        """
        workgroups: List[Dict[str, Any]] = []
        next_token: Optional[str] = None

        try:
            while True:
                kwargs: Dict[str, Any] = {"maxResults": 100}
                if next_token:
                    kwargs["nextToken"] = next_token

                resp = self.client.list_workgroups(**kwargs)
                for wg in resp.get("workgroups", []):
                    workgroups.append(_clean_workgroup(wg))

                next_token = resp.get("nextToken")
                if not next_token:
                    break
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

        return workgroups

    def get_workgroup(
        self, workgroup_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get workgroup details.

        Args:
            workgroup_name: Workgroup name. Defaults to config workgroup_name.

        Returns:
            Cleaned workgroup detail dict.
        """
        wg_name = workgroup_name or self.config.workgroup_name
        if not wg_name:
            raise RuntimeError(
                "Workgroup name required. Set REDSHIFT_WORKGROUP_NAME or pass workgroup_name."
            )

        try:
            resp = self.client.get_workgroup(workgroupName=wg_name)
            return _clean_workgroup(resp.get("workgroup", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def create_workgroup(
        self,
        workgroup_name: str,
        namespace_name: str,
        base_capacity: int = 32,
        max_capacity: Optional[int] = None,
        publicly_accessible: bool = False,
        security_group_ids: Optional[List[str]] = None,
        subnet_ids: Optional[List[str]] = None,
        enhanced_vpc_routing: bool = False,
    ) -> Dict[str, Any]:
        """Create a new Redshift Serverless workgroup.

        Args:
            workgroup_name: Unique name for the workgroup.
            namespace_name: Namespace to associate with.
            base_capacity: Base RPU capacity (8-512, increments of 8).
            max_capacity: Maximum RPU capacity (optional).
            publicly_accessible: Whether the workgroup is publicly accessible.
            security_group_ids: Security group IDs.
            subnet_ids: Subnet IDs.
            enhanced_vpc_routing: Enable enhanced VPC routing.

        Returns:
            Cleaned workgroup dict.
        """
        try:
            kwargs: Dict[str, Any] = {
                "workgroupName": workgroup_name,
                "namespaceName": namespace_name,
                "baseCapacity": base_capacity,
                "publiclyAccessible": publicly_accessible,
                "enhancedVpcRouting": enhanced_vpc_routing,
            }
            if max_capacity is not None:
                kwargs["maxCapacity"] = max_capacity
            if security_group_ids:
                kwargs["securityGroupIds"] = security_group_ids
            if subnet_ids:
                kwargs["subnetIds"] = subnet_ids

            resp = self.client.create_workgroup(**kwargs)
            return _clean_workgroup(resp.get("workgroup", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def update_workgroup(
        self,
        workgroup_name: Optional[str] = None,
        base_capacity: Optional[int] = None,
        max_capacity: Optional[int] = None,
        publicly_accessible: Optional[bool] = None,
        enhanced_vpc_routing: Optional[bool] = None,
        security_group_ids: Optional[List[str]] = None,
        subnet_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update a Redshift Serverless workgroup configuration.

        Args:
            workgroup_name: Workgroup name. Defaults to config workgroup_name.
            base_capacity: New base RPU capacity.
            max_capacity: New maximum RPU capacity.
            publicly_accessible: Update public accessibility.
            enhanced_vpc_routing: Update enhanced VPC routing.
            security_group_ids: Update security group IDs.
            subnet_ids: Update subnet IDs.

        Returns:
            Cleaned workgroup dict.
        """
        wg_name = workgroup_name or self.config.workgroup_name
        if not wg_name:
            raise RuntimeError(
                "Workgroup name required. Set REDSHIFT_WORKGROUP_NAME or pass workgroup_name."
            )

        try:
            kwargs: Dict[str, Any] = {"workgroupName": wg_name}
            if base_capacity is not None:
                kwargs["baseCapacity"] = base_capacity
            if max_capacity is not None:
                kwargs["maxCapacity"] = max_capacity
            if publicly_accessible is not None:
                kwargs["publiclyAccessible"] = publicly_accessible
            if enhanced_vpc_routing is not None:
                kwargs["enhancedVpcRouting"] = enhanced_vpc_routing
            if security_group_ids is not None:
                kwargs["securityGroupIds"] = security_group_ids
            if subnet_ids is not None:
                kwargs["subnetIds"] = subnet_ids

            resp = self.client.update_workgroup(**kwargs)
            return _clean_workgroup(resp.get("workgroup", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def delete_workgroup(
        self, workgroup_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Delete a Redshift Serverless workgroup.

        Args:
            workgroup_name: Workgroup name. Defaults to config workgroup_name.

        Returns:
            Cleaned workgroup dict.
        """
        wg_name = workgroup_name or self.config.workgroup_name
        if not wg_name:
            raise RuntimeError(
                "Workgroup name required. Set REDSHIFT_WORKGROUP_NAME or pass workgroup_name."
            )

        try:
            resp = self.client.delete_workgroup(workgroupName=wg_name)
            return _clean_workgroup(resp.get("workgroup", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc
