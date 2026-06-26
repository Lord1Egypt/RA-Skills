from __future__ import annotations

"""AWS Redshift Provisioned Skill tool interface.

Exposes 12 ``@tool``-decorated functions for agent integration, covering:

- Cluster management: ``list_clusters``, ``describe_cluster``, ``create_cluster``,
  ``delete_cluster``, ``resize_cluster``, ``pause_cluster``, ``resume_cluster``,
  ``reboot_cluster``;
- Snapshot management: ``create_snapshot``, ``describe_snapshots``,
  ``restore_from_snapshot``, ``delete_snapshot``.

All functions delegate to :class:`~scripts.provisioned.clusters.RedshiftClusterManager`
and :class:`~scripts.provisioned.snapshots.RedshiftSnapshotManager`. Configuration is
loaded from environment variables via
:func:`~scripts.config.redshift_config.load_redshift_skill_config`.
"""

from typing import Any, Dict, List, Optional, Tuple

from scripts.config.redshift_config import (
    RedshiftSkillConfig,
    RedshiftSkillConfigError,
    load_redshift_skill_config,
)
from scripts.provisioned.clusters import RedshiftClusterManager
from scripts.provisioned.snapshots import RedshiftSnapshotManager


def tool(func):  # type: ignore[override]
    """Placeholder decorator for agent tool registration.

    In a real agent environment this is replaced by the framework's ``@tool``.
    """
    return func


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _build_cluster_manager() -> Tuple[RedshiftSkillConfig, RedshiftClusterManager]:
    """Load configuration and create a cluster manager.

    Returns:
        Tuple of (config, manager).

    Raises:
        RuntimeError: If configuration loading or client creation fails.
    """
    try:
        config = load_redshift_skill_config()
    except RedshiftSkillConfigError as exc:
        raise RuntimeError(f"Redshift Skill configuration error: {exc}") from exc
    try:
        manager = RedshiftClusterManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize Redshift cluster manager: {exc}"
        ) from exc
    return config, manager


def _build_snapshot_manager() -> Tuple[RedshiftSkillConfig, RedshiftSnapshotManager]:
    """Load configuration and create a snapshot manager.

    Returns:
        Tuple of (config, manager).

    Raises:
        RuntimeError: If configuration loading or client creation fails.
    """
    try:
        config = load_redshift_skill_config()
    except RedshiftSkillConfigError as exc:
        raise RuntimeError(f"Redshift Skill configuration error: {exc}") from exc
    try:
        manager = RedshiftSnapshotManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize Redshift snapshot manager: {exc}"
        ) from exc
    return config, manager


def _mask_secrets(text: str) -> str:
    """Mask potential AWS credentials and secrets in text."""
    from scripts.provisioned.clusters import _mask_secrets as _m

    return _m(text)


# ------------------------------------------------------------------
# Cluster Management
# ------------------------------------------------------------------


@tool
def list_clusters(
    state_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List all Redshift provisioned clusters with optional state filter.

    Args:
        state_filter: Optional cluster status to filter by (e.g., 'available',
            'paused', 'creating', 'deleting', 'resuming').

    Returns:
        List of cluster dicts with keys: cluster_identifier, node_type,
        cluster_status, endpoint, number_of_nodes, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.list_clusters(state_filter=state_filter)


@tool
def describe_cluster(cluster_id: Optional[str] = None) -> Dict[str, Any]:
    """Get detailed information for a specific Redshift cluster.

    Args:
        cluster_id: Cluster identifier. Defaults to REDSHIFT_CLUSTER_ID env var.

    Returns:
        Cluster detail dict with keys: cluster_identifier, node_type,
        cluster_status, endpoint, number_of_nodes, vpc_id, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.describe_cluster(cluster_id=cluster_id)


@tool
def create_cluster(
    cluster_id: str,
    node_type: str = "ra3.xlplus",
    number_of_nodes: int = 2,
    master_username: str = "admin",
    master_password: str = "CHANGEME",
    db_name: str = "dev",
    iam_roles: Optional[List[str]] = None,
    publicly_accessible: bool = False,
) -> Dict[str, Any]:
    """Create a new Redshift provisioned cluster.

    Args:
        cluster_id: Unique cluster identifier.
        node_type: Node type (ra3.xlplus, ra3.4xlarge, ra3.16xlarge,
            dc2.large, dc2.8xlarge, ds2.xlarge, ds2.8xlarge).
        number_of_nodes: Number of compute nodes (1 for single-node, >=2 for multi).
        master_username: Master database user name.
        master_password: Master database user password.
        db_name: Default database name.
        iam_roles: Optional list of IAM role ARNs to attach.
        publicly_accessible: Whether the cluster is publicly accessible.

    Returns:
        Dict with newly created cluster details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.create_cluster(
        cluster_id=cluster_id,
        node_type=node_type,
        number_of_nodes=number_of_nodes,
        master_username=master_username,
        master_password=master_password,
        db_name=db_name,
        iam_roles=iam_roles,
        publicly_accessible=publicly_accessible,
    )


@tool
def delete_cluster(
    cluster_id: Optional[str] = None,
    skip_final_snapshot: bool = False,
    final_snapshot_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a Redshift provisioned cluster.

    Args:
        cluster_id: Cluster identifier. Defaults to REDSHIFT_CLUSTER_ID env var.
        skip_final_snapshot: If True, skip final snapshot creation.
        final_snapshot_id: Identifier for the final snapshot.

    Returns:
        Dict with deleted cluster details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.delete_cluster(
        cluster_id=cluster_id,
        skip_final_snapshot=skip_final_snapshot,
        final_snapshot_id=final_snapshot_id,
    )


@tool
def resize_cluster(
    cluster_id: Optional[str] = None,
    node_type: Optional[str] = None,
    number_of_nodes: Optional[int] = None,
    classic: bool = False,
) -> Dict[str, Any]:
    """Resize a Redshift cluster (elastic or classic resize).

    Args:
        cluster_id: Cluster identifier. Defaults to REDSHIFT_CLUSTER_ID env var.
        node_type: New node type (e.g., ra3.4xlarge).
        number_of_nodes: New number of nodes.
        classic: If True, use classic resize instead of elastic.

    Returns:
        Dict with resize status information.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.resize_cluster(
        cluster_id=cluster_id,
        node_type=node_type,
        number_of_nodes=number_of_nodes,
        classic=classic,
    )


@tool
def pause_cluster(cluster_id: Optional[str] = None) -> Dict[str, Any]:
    """Pause a Redshift cluster to save costs.

    Args:
        cluster_id: Cluster identifier. Defaults to REDSHIFT_CLUSTER_ID env var.

    Returns:
        Dict with paused cluster details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.pause_cluster(cluster_id=cluster_id)


@tool
def resume_cluster(cluster_id: Optional[str] = None) -> Dict[str, Any]:
    """Resume a paused Redshift cluster.

    Args:
        cluster_id: Cluster identifier. Defaults to REDSHIFT_CLUSTER_ID env var.

    Returns:
        Dict with resumed cluster details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.resume_cluster(cluster_id=cluster_id)


@tool
def reboot_cluster(cluster_id: Optional[str] = None) -> Dict[str, Any]:
    """Reboot a Redshift cluster.

    Args:
        cluster_id: Cluster identifier. Defaults to REDSHIFT_CLUSTER_ID env var.

    Returns:
        Dict with rebooted cluster details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.reboot_cluster(cluster_id=cluster_id)


# ------------------------------------------------------------------
# Snapshot Management
# ------------------------------------------------------------------


@tool
def create_snapshot(
    snapshot_id: str,
    cluster_id: Optional[str] = None,
    retention_period: Optional[int] = None,
) -> Dict[str, Any]:
    """Create a manual snapshot of a Redshift cluster.

    Args:
        snapshot_id: Unique identifier for the snapshot.
        cluster_id: Cluster identifier. Defaults to REDSHIFT_CLUSTER_ID env var.
        retention_period: Number of days to retain the snapshot.

    Returns:
        Dict with snapshot details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_snapshot_manager()
    return manager.create_snapshot(
        snapshot_id=snapshot_id,
        cluster_id=cluster_id,
        retention_period=retention_period,
    )


@tool
def describe_snapshots(
    cluster_id: Optional[str] = None,
    snapshot_id: Optional[str] = None,
    snapshot_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List or describe Redshift snapshots.

    Args:
        cluster_id: Filter by cluster identifier.
        snapshot_id: Filter by specific snapshot identifier.
        snapshot_type: Filter by type ('manual' or 'automated').

    Returns:
        List of snapshot dicts.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_snapshot_manager()
    return manager.describe_snapshots(
        cluster_id=cluster_id,
        snapshot_id=snapshot_id,
        snapshot_type=snapshot_type,
    )


@tool
def restore_from_snapshot(
    cluster_id: str,
    snapshot_id: str,
    node_type: Optional[str] = None,
    number_of_nodes: Optional[int] = None,
    publicly_accessible: bool = False,
) -> Dict[str, Any]:
    """Restore a Redshift cluster from a snapshot.

    Args:
        cluster_id: Identifier for the new restored cluster.
        snapshot_id: Snapshot to restore from.
        node_type: Optional node type override.
        number_of_nodes: Optional number of nodes override.
        publicly_accessible: Whether the restored cluster is publicly accessible.

    Returns:
        Dict with restored cluster details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_snapshot_manager()
    return manager.restore_from_snapshot(
        cluster_id=cluster_id,
        snapshot_id=snapshot_id,
        node_type=node_type,
        number_of_nodes=number_of_nodes,
        publicly_accessible=publicly_accessible,
    )


@tool
def delete_snapshot(snapshot_id: str) -> Dict[str, Any]:
    """Delete a manual Redshift snapshot.

    Args:
        snapshot_id: Snapshot identifier to delete.

    Returns:
        Dict with deleted snapshot details.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_snapshot_manager()
    return manager.delete_snapshot(snapshot_id=snapshot_id)
