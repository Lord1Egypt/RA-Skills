from __future__ import annotations

"""Redshift snapshot management.

Provides :class:`RedshiftSnapshotManager` for managing Redshift manual snapshots
via the ``redshift`` boto3 client.
"""

import re
from typing import Any, Dict, List, Optional

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_redshift_client
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


def _clean_snapshot(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a boto3 Snapshot response dict to snake_case."""
    return {
        "snapshot_identifier": raw.get("SnapshotIdentifier"),
        "cluster_identifier": raw.get("ClusterIdentifier"),
        "snapshot_create_time": str(raw.get("SnapshotCreateTime", "")),
        "status": raw.get("Status"),
        "port": raw.get("Port"),
        "availability_zone": raw.get("AvailabilityZone"),
        "cluster_create_time": str(raw.get("ClusterCreateTime", "")),
        "master_username": raw.get("MasterUsername"),
        "cluster_version": raw.get("ClusterVersion"),
        "engine_full_version": raw.get("EngineFullVersion"),
        "snapshot_type": raw.get("SnapshotType"),
        "node_type": raw.get("NodeType"),
        "number_of_nodes": raw.get("NumberOfNodes"),
        "db_name": raw.get("DBName"),
        "encrypted": raw.get("Encrypted"),
        "total_backup_size_in_mega_bytes": raw.get("TotalBackupSizeInMegaBytes"),
        "actual_incremental_backup_size_in_mega_bytes": raw.get(
            "ActualIncrementalBackupSizeInMegaBytes"
        ),
    }


class RedshiftSnapshotManager:
    """Manages Redshift snapshot operations.

    Attributes:
        config: Redshift skill configuration.
        client: boto3 Redshift client.
    """

    def __init__(self, config: RedshiftSkillConfig) -> None:
        self.config = config
        self.client = get_redshift_client(config.region)

    @classmethod
    def from_env(cls) -> "RedshiftSnapshotManager":
        """Create a manager from environment configuration."""
        from scripts.config.redshift_config import load_redshift_skill_config

        return cls(load_redshift_skill_config())

    def create_snapshot(
        self,
        snapshot_id: str,
        cluster_id: Optional[str] = None,
        retention_period: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a manual snapshot of a Redshift cluster.

        Args:
            snapshot_id: Unique identifier for the snapshot.
            cluster_id: Cluster identifier. Defaults to config cluster_id.
            retention_period: Number of days to retain the snapshot.

        Returns:
            Cleaned snapshot dict.
        """
        cid = cluster_id or self.config.cluster_id
        if not cid:
            raise RuntimeError(
                "Cluster identifier required. Set REDSHIFT_CLUSTER_ID or pass cluster_id."
            )

        try:
            kwargs: Dict[str, Any] = {
                "SnapshotIdentifier": snapshot_id,
                "ClusterIdentifier": cid,
            }
            if retention_period is not None:
                kwargs["ManualSnapshotRetentionPeriod"] = retention_period

            resp = self.client.create_cluster_snapshot(**kwargs)
            return _clean_snapshot(resp.get("Snapshot", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def describe_snapshots(
        self,
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
            List of cleaned snapshot dicts.
        """
        snapshots: List[Dict[str, Any]] = []
        marker: Optional[str] = None

        try:
            while True:
                kwargs: Dict[str, Any] = {"MaxRecords": 100}
                if marker:
                    kwargs["Marker"] = marker
                if cluster_id:
                    kwargs["ClusterIdentifier"] = cluster_id
                if snapshot_id:
                    kwargs["SnapshotIdentifier"] = snapshot_id
                if snapshot_type:
                    kwargs["SnapshotType"] = snapshot_type

                resp = self.client.describe_cluster_snapshots(**kwargs)
                for s in resp.get("Snapshots", []):
                    snapshots.append(_clean_snapshot(s))

                marker = resp.get("Marker")
                if not marker:
                    break
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

        return snapshots

    def restore_from_snapshot(
        self,
        cluster_id: str,
        snapshot_id: str,
        node_type: Optional[str] = None,
        number_of_nodes: Optional[int] = None,
        publicly_accessible: bool = False,
    ) -> Dict[str, Any]:
        """Restore a Redshift cluster from a snapshot.

        Args:
            cluster_id: Identifier for the new cluster.
            snapshot_id: Snapshot to restore from.
            node_type: Optional node type override.
            number_of_nodes: Optional number of nodes override.
            publicly_accessible: Whether the restored cluster is publicly accessible.

        Returns:
            Cleaned cluster dict for the restored cluster.
        """
        try:
            kwargs: Dict[str, Any] = {
                "ClusterIdentifier": cluster_id,
                "SnapshotIdentifier": snapshot_id,
                "PubliclyAccessible": publicly_accessible,
            }
            if node_type:
                kwargs["NodeType"] = node_type
            if number_of_nodes is not None:
                kwargs["NumberOfNodes"] = number_of_nodes

            resp = self.client.restore_from_cluster_snapshot(**kwargs)
            raw = resp.get("Cluster", {})
            return {
                "cluster_identifier": raw.get("ClusterIdentifier"),
                "cluster_status": raw.get("ClusterStatus"),
                "node_type": raw.get("NodeType"),
                "number_of_nodes": raw.get("NumberOfNodes"),
                "db_name": raw.get("DBName"),
                "master_username": raw.get("MasterUsername"),
            }
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def delete_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """Delete a manual Redshift snapshot.

        Args:
            snapshot_id: Snapshot identifier to delete.

        Returns:
            Cleaned snapshot dict for the deleted snapshot.
        """
        try:
            resp = self.client.delete_cluster_snapshot(
                SnapshotIdentifier=snapshot_id
            )
            return _clean_snapshot(resp.get("Snapshot", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc
