from __future__ import annotations

"""Redshift provisioned cluster management.

Provides :class:`RedshiftClusterManager` for managing Redshift provisioned
clusters via the ``redshift`` boto3 client. All operations include error
handling, pagination, and camelCase-to-snake_case response cleaning.
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
    text = re.sub(
        r"(?i)(password\s*[:=]\s*)[^\s,\"']+",
        r"\1****MASKED",
        text,
    )
    return text


def _clean_cluster(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a boto3 Cluster response dict to snake_case."""
    return {
        "cluster_identifier": raw.get("ClusterIdentifier"),
        "node_type": raw.get("NodeType"),
        "cluster_status": raw.get("ClusterStatus"),
        "modify_status": raw.get("ModifyStatus"),
        "master_username": raw.get("MasterUsername"),
        "db_name": raw.get("DBName"),
        "endpoint": {
            "address": raw.get("Endpoint", {}).get("Address"),
            "port": raw.get("Endpoint", {}).get("Port"),
        }
        if raw.get("Endpoint")
        else None,
        "cluster_create_time": str(raw.get("ClusterCreateTime", "")),
        "number_of_nodes": raw.get("NumberOfNodes"),
        "availability_zone": raw.get("AvailabilityZone"),
        "cluster_version": raw.get("ClusterVersion"),
        "encrypted": raw.get("Encrypted"),
        "vpc_id": raw.get("VpcId"),
        "cluster_subnet_group_name": raw.get("ClusterSubnetGroupName"),
        "publicly_accessible": raw.get("PubliclyAccessible"),
        "total_storage_capacity_in_mega_bytes": raw.get(
            "TotalStorageCapacityInMegaBytes"
        ),
        "elastic_resize_number_of_node_options": raw.get(
            "ElasticResizeNumberOfNodeOptions"
        ),
    }


class RedshiftClusterManager:
    """Manages Redshift provisioned cluster operations.

    Wraps the ``redshift`` boto3 client with error handling, pagination,
    and response cleaning.

    Attributes:
        config: Redshift skill configuration.
        client: boto3 Redshift client.
    """

    def __init__(self, config: RedshiftSkillConfig) -> None:
        self.config = config
        self.client = get_redshift_client(config.region)

    @classmethod
    def from_env(cls) -> "RedshiftClusterManager":
        """Create a manager from environment configuration."""
        from scripts.config.redshift_config import load_redshift_skill_config

        return cls(load_redshift_skill_config())

    def list_clusters(
        self, state_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all Redshift provisioned clusters with optional state filter.

        Args:
            state_filter: Optional cluster status to filter by (e.g., 'available',
                'paused', 'creating', 'deleting', 'resuming').

        Returns:
            List of cleaned cluster dicts.
        """
        clusters: List[Dict[str, Any]] = []
        marker: Optional[str] = None

        try:
            while True:
                kwargs: Dict[str, Any] = {"MaxRecords": 100}
                if marker:
                    kwargs["Marker"] = marker

                resp = self.client.describe_clusters(**kwargs)
                for c in resp.get("Clusters", []):
                    cleaned = _clean_cluster(c)
                    if state_filter and cleaned.get("cluster_status") != state_filter:
                        continue
                    clusters.append(cleaned)

                marker = resp.get("Marker")
                if not marker:
                    break
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

        return clusters

    def describe_cluster(self, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed information for a specific Redshift cluster.

        Args:
            cluster_id: Cluster identifier. Defaults to config cluster_id.

        Returns:
            Cleaned cluster detail dict.
        """
        cid = cluster_id or self.config.cluster_id
        if not cid:
            raise RuntimeError(
                "Cluster identifier required. Set REDSHIFT_CLUSTER_ID or pass cluster_id."
            )

        try:
            resp = self.client.describe_clusters(ClusterIdentifier=cid)
            clusters = resp.get("Clusters", [])
            if not clusters:
                raise RuntimeError(f"Cluster '{cid}' not found.")
            return _clean_cluster(clusters[0])
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def create_cluster(
        self,
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
            node_type: Node type (e.g., ra3.xlplus, dc2.large).
            number_of_nodes: Number of compute nodes (min 2 for multi-node).
            master_username: Master database user name.
            master_password: Master database user password.
            db_name: Default database name.
            iam_roles: Optional list of IAM role ARNs to attach.
            publicly_accessible: Whether the cluster is publicly accessible.

        Returns:
            Cleaned cluster dict for the newly created cluster.
        """
        try:
            kwargs: Dict[str, Any] = {
                "ClusterIdentifier": cluster_id,
                "NodeType": node_type,
                "MasterUsername": master_username,
                "MasterUserPassword": master_password,
                "DBName": db_name,
                "PubliclyAccessible": publicly_accessible,
            }
            if number_of_nodes == 1:
                kwargs["ClusterType"] = "single-node"
            else:
                kwargs["ClusterType"] = "multi-node"
                kwargs["NumberOfNodes"] = number_of_nodes

            if iam_roles:
                kwargs["IamRoles"] = iam_roles

            resp = self.client.create_cluster(**kwargs)
            return _clean_cluster(resp.get("Cluster", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def delete_cluster(
        self,
        cluster_id: Optional[str] = None,
        skip_final_snapshot: bool = False,
        final_snapshot_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Delete a Redshift provisioned cluster.

        Args:
            cluster_id: Cluster identifier. Defaults to config cluster_id.
            skip_final_snapshot: If True, skip final snapshot creation.
            final_snapshot_id: Identifier for the final snapshot.

        Returns:
            Cleaned cluster dict for the deleted cluster.
        """
        cid = cluster_id or self.config.cluster_id
        if not cid:
            raise RuntimeError(
                "Cluster identifier required. Set REDSHIFT_CLUSTER_ID or pass cluster_id."
            )

        try:
            kwargs: Dict[str, Any] = {
                "ClusterIdentifier": cid,
                "SkipFinalClusterSnapshot": skip_final_snapshot,
            }
            if not skip_final_snapshot:
                sid = final_snapshot_id or f"{cid}-final-snapshot"
                kwargs["FinalClusterSnapshotIdentifier"] = sid

            resp = self.client.delete_cluster(**kwargs)
            return _clean_cluster(resp.get("Cluster", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def resize_cluster(
        self,
        cluster_id: Optional[str] = None,
        node_type: Optional[str] = None,
        number_of_nodes: Optional[int] = None,
        classic: bool = False,
    ) -> Dict[str, Any]:
        """Resize a Redshift cluster (elastic or classic).

        Args:
            cluster_id: Cluster identifier. Defaults to config cluster_id.
            node_type: New node type (optional).
            number_of_nodes: New number of nodes (optional).
            classic: If True, use classic resize instead of elastic.

        Returns:
            Dict with resize status information.
        """
        cid = cluster_id or self.config.cluster_id
        if not cid:
            raise RuntimeError(
                "Cluster identifier required. Set REDSHIFT_CLUSTER_ID or pass cluster_id."
            )

        try:
            kwargs: Dict[str, Any] = {"ClusterIdentifier": cid, "Classic": classic}
            if node_type:
                kwargs["NodeType"] = node_type
            if number_of_nodes is not None:
                kwargs["NumberOfNodes"] = number_of_nodes

            resp = self.client.resize_cluster(**kwargs)
            return _clean_cluster(resp.get("Cluster", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def pause_cluster(self, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """Pause a Redshift cluster to save costs.

        Args:
            cluster_id: Cluster identifier. Defaults to config cluster_id.

        Returns:
            Cleaned cluster dict.
        """
        cid = cluster_id or self.config.cluster_id
        if not cid:
            raise RuntimeError(
                "Cluster identifier required. Set REDSHIFT_CLUSTER_ID or pass cluster_id."
            )

        try:
            resp = self.client.pause_cluster(ClusterIdentifier=cid)
            return _clean_cluster(resp.get("Cluster", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def resume_cluster(self, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """Resume a paused Redshift cluster.

        Args:
            cluster_id: Cluster identifier. Defaults to config cluster_id.

        Returns:
            Cleaned cluster dict.
        """
        cid = cluster_id or self.config.cluster_id
        if not cid:
            raise RuntimeError(
                "Cluster identifier required. Set REDSHIFT_CLUSTER_ID or pass cluster_id."
            )

        try:
            resp = self.client.resume_cluster(ClusterIdentifier=cid)
            return _clean_cluster(resp.get("Cluster", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def reboot_cluster(self, cluster_id: Optional[str] = None) -> Dict[str, Any]:
        """Reboot a Redshift cluster.

        Args:
            cluster_id: Cluster identifier. Defaults to config cluster_id.

        Returns:
            Cleaned cluster dict.
        """
        cid = cluster_id or self.config.cluster_id
        if not cid:
            raise RuntimeError(
                "Cluster identifier required. Set REDSHIFT_CLUSTER_ID or pass cluster_id."
            )

        try:
            resp = self.client.reboot_cluster(ClusterIdentifier=cid)
            return _clean_cluster(resp.get("Cluster", {}))
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc
