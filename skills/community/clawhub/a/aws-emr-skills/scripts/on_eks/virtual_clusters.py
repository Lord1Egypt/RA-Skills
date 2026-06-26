"""EMR on EKS virtual cluster management via boto3.

Provides a high-level client for managing AWS EMR on EKS virtual clusters:

- list_virtual_clusters: List virtual clusters with optional state/provider filtering, handles pagination.
- describe_virtual_cluster: Retrieve detailed information for a single virtual cluster.
- create_virtual_cluster: Create a new virtual cluster linked to an EKS cluster namespace.
- delete_virtual_cluster: Request deletion of a virtual cluster.

All methods return clean Python dicts with snake_case keys, not raw boto3 responses.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_emr_containers_client
from scripts.config.emr_config import EMRSkillConfig, load_emr_skill_config

logger = logging.getLogger(__name__)


def _clean_virtual_cluster_summary(vc: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 virtual cluster dict.

    Converts camelCase boto3 keys to snake_case for consistency.
    """
    container_provider = vc.get("containerProvider", {})
    info = container_provider.get("info", {})
    eks_info = info.get("eksInfo", {})

    return {
        "id": vc.get("id", ""),
        "name": vc.get("name", ""),
        "arn": vc.get("arn", ""),
        "state": vc.get("state", ""),
        "container_provider_type": container_provider.get("type", ""),
        "container_provider_id": container_provider.get("id", ""),
        "namespace": eks_info.get("namespace", ""),
        "created_at": str(vc.get("createdAt", "")),
        "tags": vc.get("tags", {}),
    }


def _clean_virtual_cluster_detail(vc: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 virtual cluster detail dict.

    Includes all summary fields plus any additional detail fields.
    """
    return _clean_virtual_cluster_summary(vc)


class EMRVirtualClusterManager:
    """High-level client for managing EMR on EKS virtual clusters.

    Uses ``EMRSkillConfig`` for region configuration.
    AWS credentials are resolved via boto3's default credential chain.
    """

    def __init__(self, config: EMRSkillConfig) -> None:
        self._client = get_emr_containers_client(region=config.region)
        self._config = config

    @classmethod
    def from_env(cls) -> "EMRVirtualClusterManager":
        """Create an instance using configuration loaded from environment."""
        return cls(load_emr_skill_config())

    def list_virtual_clusters(
        self,
        *,
        states: Optional[List[str]] = None,
        container_provider_id: Optional[str] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """List EMR on EKS virtual clusters, with optional state and provider filtering.

        Handles pagination automatically to return up to ``max_results`` clusters.

        Args:
            states: Optional list of virtual cluster states to filter by.
                Valid values: RUNNING, TERMINATING, TERMINATED, ARRESTED.
            container_provider_id: Optional EKS cluster ID to filter by.
            max_results: Maximum number of virtual clusters to return.

        Returns:
            List of virtual cluster dicts with keys: id, name, arn, state,
            container_provider_type, container_provider_id, namespace,
            created_at, tags.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        clusters: List[Dict[str, Any]] = []
        kwargs: Dict[str, Any] = {}
        if states:
            kwargs["states"] = states
        if container_provider_id:
            kwargs["containerProviderId"] = container_provider_id
            kwargs["containerProviderType"] = "EKS"

        try:
            while len(clusters) < max_results:
                kwargs["maxResults"] = min(50, max_results - len(clusters))
                response = self._client.list_virtual_clusters(**kwargs)
                raw_clusters = response.get("virtualClusters", [])
                clusters.extend(
                    _clean_virtual_cluster_summary(vc) for vc in raw_clusters
                )

                next_token = response.get("nextToken")
                if not next_token or not raw_clusters:
                    break
                kwargs["nextToken"] = next_token

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to list virtual clusters: [{error_code}] {error_msg}"
            ) from exc

        return clusters[:max_results]

    def describe_virtual_cluster(
        self,
        virtual_cluster_id: str,
    ) -> Dict[str, Any]:
        """Get detailed information for a specific EMR on EKS virtual cluster.

        Args:
            virtual_cluster_id: The virtual cluster ID.

        Returns:
            Virtual cluster detail dict with keys: id, name, arn, state,
            container_provider_type, container_provider_id, namespace,
            created_at, tags.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            response = self._client.describe_virtual_cluster(
                id=virtual_cluster_id,
            )
            return _clean_virtual_cluster_detail(response["virtualCluster"])
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to describe virtual cluster '{virtual_cluster_id}': "
                f"[{error_code}] {error_msg}"
            ) from exc

    def create_virtual_cluster(
        self,
        name: str,
        eks_cluster_id: str,
        namespace: str,
        *,
        tags: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Create a new EMR on EKS virtual cluster.

        Links an EKS cluster namespace to EMR for running containerized Spark jobs.

        Args:
            name: Name for the virtual cluster.
            eks_cluster_id: The EKS cluster ID to associate with.
            namespace: The Kubernetes namespace on the EKS cluster.
            tags: Optional tags to attach to the virtual cluster.

        Returns:
            Dict with keys: id, name, arn.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        kwargs: Dict[str, Any] = {
            "name": name,
            "containerProvider": {
                "type": "EKS",
                "id": eks_cluster_id,
                "info": {
                    "eksInfo": {
                        "namespace": namespace,
                    }
                },
            },
        }
        if tags:
            kwargs["tags"] = tags

        try:
            response = self._client.create_virtual_cluster(**kwargs)
            return {
                "id": response.get("id", ""),
                "name": response.get("name", ""),
                "arn": response.get("arn", ""),
            }
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to create virtual cluster '{name}': [{error_code}] {error_msg}"
            ) from exc

    def delete_virtual_cluster(
        self,
        virtual_cluster_id: str,
    ) -> Dict[str, Any]:
        """Request deletion of an EMR on EKS virtual cluster.

        Args:
            virtual_cluster_id: The virtual cluster ID to delete.

        Returns:
            Dict with keys: id, status ('delete_requested').

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            self._client.delete_virtual_cluster(id=virtual_cluster_id)
            return {
                "id": virtual_cluster_id,
                "status": "delete_requested",
            }
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to delete virtual cluster '{virtual_cluster_id}': "
                f"[{error_code}] {error_msg}"
            ) from exc
