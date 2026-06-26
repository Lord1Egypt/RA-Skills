from __future__ import annotations

"""AWS Redshift Serverless Skill tool interface.

Exposes 9 ``@tool``-decorated functions for agent integration, covering:

- Workgroup management: ``list_workgroups``, ``get_workgroup``, ``create_workgroup``,
  ``update_workgroup``, ``delete_workgroup``;
- Namespace management: ``list_namespaces``, ``get_namespace``, ``create_namespace``,
  ``delete_namespace``.

All functions delegate to :class:`~scripts.serverless.workgroups.RedshiftWorkgroupManager`
and :class:`~scripts.serverless.namespaces.RedshiftNamespaceManager`.
"""

from typing import Any, Dict, List, Optional, Tuple

from scripts.config.redshift_config import (
    RedshiftSkillConfig,
    RedshiftSkillConfigError,
    load_redshift_skill_config,
)
from scripts.serverless.workgroups import RedshiftWorkgroupManager
from scripts.serverless.namespaces import RedshiftNamespaceManager


def tool(func):  # type: ignore[override]
    """Placeholder decorator for agent tool registration."""
    return func


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _build_workgroup_manager() -> Tuple[RedshiftSkillConfig, RedshiftWorkgroupManager]:
    """Load configuration and create a workgroup manager."""
    try:
        config = load_redshift_skill_config()
    except RedshiftSkillConfigError as exc:
        raise RuntimeError(f"Redshift Skill configuration error: {exc}") from exc
    try:
        manager = RedshiftWorkgroupManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize Redshift workgroup manager: {exc}"
        ) from exc
    return config, manager


def _build_namespace_manager() -> Tuple[RedshiftSkillConfig, RedshiftNamespaceManager]:
    """Load configuration and create a namespace manager."""
    try:
        config = load_redshift_skill_config()
    except RedshiftSkillConfigError as exc:
        raise RuntimeError(f"Redshift Skill configuration error: {exc}") from exc
    try:
        manager = RedshiftNamespaceManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize Redshift namespace manager: {exc}"
        ) from exc
    return config, manager


# ------------------------------------------------------------------
# Workgroup Management
# ------------------------------------------------------------------


@tool
def list_workgroups() -> List[Dict[str, Any]]:
    """List all Redshift Serverless workgroups.

    Returns:
        List of workgroup dicts with keys: workgroup_name, status,
        base_capacity, endpoint, namespace_name, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_workgroup_manager()
    return manager.list_workgroups()


@tool
def get_workgroup(workgroup_name: Optional[str] = None) -> Dict[str, Any]:
    """Get details for a specific Redshift Serverless workgroup.

    Args:
        workgroup_name: Workgroup name. Defaults to REDSHIFT_WORKGROUP_NAME env var.

    Returns:
        Workgroup detail dict with keys: workgroup_name, status,
        base_capacity, max_capacity, endpoint, namespace_name, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_workgroup_manager()
    return manager.get_workgroup(workgroup_name=workgroup_name)


@tool
def create_workgroup(
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
        max_capacity: Maximum RPU capacity.
        publicly_accessible: Whether the workgroup is publicly accessible.
        security_group_ids: Security group IDs.
        subnet_ids: Subnet IDs.
        enhanced_vpc_routing: Enable enhanced VPC routing.

    Returns:
        Dict with newly created workgroup details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_workgroup_manager()
    return manager.create_workgroup(
        workgroup_name=workgroup_name,
        namespace_name=namespace_name,
        base_capacity=base_capacity,
        max_capacity=max_capacity,
        publicly_accessible=publicly_accessible,
        security_group_ids=security_group_ids,
        subnet_ids=subnet_ids,
        enhanced_vpc_routing=enhanced_vpc_routing,
    )


@tool
def update_workgroup(
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
        workgroup_name: Workgroup name. Defaults to REDSHIFT_WORKGROUP_NAME env var.
        base_capacity: New base RPU capacity.
        max_capacity: New maximum RPU capacity.
        publicly_accessible: Update public accessibility.
        enhanced_vpc_routing: Update enhanced VPC routing.
        security_group_ids: Update security group IDs.
        subnet_ids: Update subnet IDs.

    Returns:
        Dict with updated workgroup details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_workgroup_manager()
    return manager.update_workgroup(
        workgroup_name=workgroup_name,
        base_capacity=base_capacity,
        max_capacity=max_capacity,
        publicly_accessible=publicly_accessible,
        enhanced_vpc_routing=enhanced_vpc_routing,
        security_group_ids=security_group_ids,
        subnet_ids=subnet_ids,
    )


@tool
def delete_workgroup(workgroup_name: Optional[str] = None) -> Dict[str, Any]:
    """Delete a Redshift Serverless workgroup.

    Args:
        workgroup_name: Workgroup name. Defaults to REDSHIFT_WORKGROUP_NAME env var.

    Returns:
        Dict with deleted workgroup details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_workgroup_manager()
    return manager.delete_workgroup(workgroup_name=workgroup_name)


# ------------------------------------------------------------------
# Namespace Management
# ------------------------------------------------------------------


@tool
def list_namespaces() -> List[Dict[str, Any]]:
    """List all Redshift Serverless namespaces.

    Returns:
        List of namespace dicts with keys: namespace_name, status,
        db_name, admin_username, iam_roles, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_namespace_manager()
    return manager.list_namespaces()


@tool
def get_namespace(namespace_name: Optional[str] = None) -> Dict[str, Any]:
    """Get details for a specific Redshift Serverless namespace.

    Args:
        namespace_name: Namespace name. Defaults to REDSHIFT_NAMESPACE_NAME env var.

    Returns:
        Namespace detail dict with keys: namespace_name, status, db_name,
        admin_username, iam_roles, default_iam_role_arn, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_namespace_manager()
    return manager.get_namespace(namespace_name=namespace_name)


@tool
def create_namespace(
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
        Dict with newly created namespace details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_namespace_manager()
    return manager.create_namespace(
        namespace_name=namespace_name,
        db_name=db_name,
        admin_username=admin_username,
        admin_user_password=admin_user_password,
        iam_roles=iam_roles,
        default_iam_role_arn=default_iam_role_arn,
        kms_key_id=kms_key_id,
        log_exports=log_exports,
    )


@tool
def delete_namespace(
    namespace_name: Optional[str] = None,
    final_snapshot_name: Optional[str] = None,
    final_snapshot_retention_period: Optional[int] = None,
) -> Dict[str, Any]:
    """Delete a Redshift Serverless namespace.

    Args:
        namespace_name: Namespace name. Defaults to REDSHIFT_NAMESPACE_NAME env var.
        final_snapshot_name: Optional final snapshot name.
        final_snapshot_retention_period: Retention period for final snapshot (days).

    Returns:
        Dict with deleted namespace details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_namespace_manager()
    return manager.delete_namespace(
        namespace_name=namespace_name,
        final_snapshot_name=final_snapshot_name,
        final_snapshot_retention_period=final_snapshot_retention_period,
    )
