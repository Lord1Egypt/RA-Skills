"""EMR On EC2 cluster management via boto3.

Provides a high-level client for managing AWS EMR clusters on EC2:

- list_clusters: List clusters with optional state and date filtering, handles pagination.
- describe_cluster: Retrieve detailed information for a single cluster.
- terminate_clusters: Request termination of one or more clusters.

All methods return clean Python dicts with snake_case keys, not raw boto3 responses.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_emr_client, get_s3_client
from scripts.config.emr_config import EMRSkillConfig, load_emr_skill_config

logger = logging.getLogger(__name__)


def _clean_cluster_summary(cluster: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 cluster summary dict.

    Converts camelCase boto3 keys to snake_case for consistency.
    """
    status = cluster.get("Status", {})
    timeline = status.get("Timeline", {})
    state_change = status.get("StateChangeReason", {})

    return {
        "id": cluster.get("Id", ""),
        "name": cluster.get("Name", ""),
        "state": status.get("State", ""),
        "state_change_reason": state_change.get("Message", ""),
        "created_at": str(timeline.get("CreationDateTime", "")),
        "ready_at": str(timeline.get("ReadyDateTime", "")),
        "ended_at": str(timeline.get("EndDateTime", "")),
        "normalized_instance_hours": cluster.get("NormalizedInstanceHours", 0),
        "cluster_arn": cluster.get("ClusterArn", ""),
    }


def _clean_cluster_detail(cluster: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 describe_cluster response.

    Includes additional detail fields beyond the summary.
    """
    status = cluster.get("Status", {})
    timeline = status.get("Timeline", {})
    state_change = status.get("StateChangeReason", {})

    # Build applications list
    raw_apps = cluster.get("Applications", [])
    applications = [
        {"name": app.get("Name", ""), "version": app.get("Version", "")}
        for app in raw_apps
    ]

    # Build tags list
    raw_tags = cluster.get("Tags", [])
    tags = {tag.get("Key", ""): tag.get("Value", "") for tag in raw_tags}

    # EC2 instance attributes
    ec2_attrs = cluster.get("Ec2InstanceAttributes", {})
    ec2_instance_attributes = {
        "ec2_key_name": ec2_attrs.get("Ec2KeyName", ""),
        "ec2_subnet_id": ec2_attrs.get("Ec2SubnetId", ""),
        "ec2_availability_zone": ec2_attrs.get("Ec2AvailabilityZone", ""),
        "iam_instance_profile": ec2_attrs.get("IamInstanceProfile", ""),
        "emr_managed_master_security_group": ec2_attrs.get(
            "EmrManagedMasterSecurityGroup", ""
        ),
        "emr_managed_slave_security_group": ec2_attrs.get(
            "EmrManagedSlaveSecurityGroup", ""
        ),
    }

    return {
        "id": cluster.get("Id", ""),
        "name": cluster.get("Name", ""),
        "state": status.get("State", ""),
        "state_details": state_change.get("Message", ""),
        "log_uri": cluster.get("LogUri", ""),
        "release_label": cluster.get("ReleaseLabel", ""),
        "applications": applications,
        "service_role": cluster.get("ServiceRole", ""),
        "master_public_dns": cluster.get("MasterPublicDnsName", ""),
        "ec2_instance_attributes": ec2_instance_attributes,
        "step_concurrency_level": cluster.get("StepConcurrencyLevel", 1),
        "auto_terminate": cluster.get("AutoTerminate", False),
        "termination_protected": cluster.get("TerminationProtected", False),
        "cluster_arn": cluster.get("ClusterArn", ""),
        "tags": tags,
        "created_at": str(timeline.get("CreationDateTime", "")),
        "ready_at": str(timeline.get("ReadyDateTime", "")),
        "ended_at": str(timeline.get("EndDateTime", "")),
    }


class EMRClusterManager:
    """High-level client for managing EMR clusters on EC2.

    Uses ``EMRSkillConfig`` for region configuration.
    AWS credentials are resolved via boto3's default credential chain.
    """

    def __init__(self, config: EMRSkillConfig) -> None:
        self._client = get_emr_client(region=config.region)
        self._s3_client = get_s3_client(region=config.region)
        self._config = config

    @classmethod
    def from_env(cls) -> "EMRClusterManager":
        """Create an instance using configuration loaded from environment."""
        return cls(load_emr_skill_config())

    def list_clusters(
        self,
        states: Optional[List[str]] = None,
        created_after: Optional[Union[datetime, str]] = None,
        created_before: Optional[Union[datetime, str]] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """List EMR clusters, with optional state and date filtering.

        Handles pagination automatically to return up to ``max_results`` clusters.

        Args:
            states: Optional list of cluster states to filter by.
                Valid values: STARTING, BOOTSTRAPPING, RUNNING, WAITING,
                TERMINATING, TERMINATED, TERMINATED_WITH_ERRORS.
            created_after: Only return clusters created after this datetime.
            created_before: Only return clusters created before this datetime.
            max_results: Maximum number of clusters to return.

        Returns:
            List of cluster dicts with keys: id, name, state, state_change_reason,
            created_at, ready_at, ended_at, normalized_instance_hours, cluster_arn.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        clusters: List[Dict[str, Any]] = []
        kwargs: Dict[str, Any] = {}
        if states:
            kwargs["ClusterStates"] = states
        if created_after:
            kwargs["CreatedAfter"] = (
                created_after
                if isinstance(created_after, datetime)
                else datetime.fromisoformat(created_after)
            )
        if created_before:
            kwargs["CreatedBefore"] = (
                created_before
                if isinstance(created_before, datetime)
                else datetime.fromisoformat(created_before)
            )

        try:
            while len(clusters) < max_results:
                response = self._client.list_clusters(**kwargs)
                raw_clusters = response.get("Clusters", [])
                clusters.extend(_clean_cluster_summary(c) for c in raw_clusters)

                marker = response.get("Marker")
                if not marker or not raw_clusters:
                    break
                kwargs["Marker"] = marker

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to list EMR clusters: [{error_code}] {error_msg}"
            ) from exc

        return clusters[:max_results]

    def describe_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific EMR cluster.

        Args:
            cluster_id: The EMR cluster ID (e.g., ``j-XXXXXXXXXXXXX``).

        Returns:
            Cluster detail dict with keys: id, name, state, state_details,
            log_uri, release_label, applications, service_role,
            master_public_dns, ec2_instance_attributes, step_concurrency_level,
            auto_terminate, termination_protected, cluster_arn, tags,
            created_at, ready_at, ended_at.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            response = self._client.describe_cluster(ClusterId=cluster_id)
            return _clean_cluster_detail(response["Cluster"])
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to describe cluster '{cluster_id}': [{error_code}] {error_msg}"
            ) from exc

    def terminate_clusters(self, cluster_ids: List[str]) -> Dict[str, Any]:
        """Request termination of one or more EMR clusters.

        Args:
            cluster_ids: List of cluster IDs to terminate.

        Returns:
            Dict with keys: cluster_ids (list), status ('termination_requested').

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            self._client.terminate_job_flows(JobFlowIds=cluster_ids)
            return {
                "cluster_ids": cluster_ids,
                "status": "termination_requested",
            }
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to terminate clusters {cluster_ids}: [{error_code}] {error_msg}"
            ) from exc
