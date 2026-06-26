"""EMR Serverless application management via boto3.

Provides a high-level client for managing AWS EMR Serverless applications:

- list_applications: List applications with optional state filtering, handles pagination.
- get_application: Retrieve detailed information for a single application.
- start_application: Request an application to start (pre-initialize capacity).
- stop_application: Request an application to stop and release resources.

All methods return clean Python dicts with snake_case keys, not raw boto3 responses.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_emr_serverless_client
from scripts.config.emr_config import EMRSkillConfig, load_emr_skill_config

logger = logging.getLogger(__name__)


def _clean_application_summary(app: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 application summary dict.

    Converts camelCase boto3 keys to snake_case for consistency.
    """
    return {
        "id": app.get("id", ""),
        "name": app.get("name", ""),
        "state": app.get("state", ""),
        "type": app.get("type", ""),
        "release_label": app.get("releaseLabel", ""),
        "created_at": app.get("createdAt", ""),
        "updated_at": app.get("updatedAt", ""),
        "architecture": app.get("architecture", ""),
    }


def _clean_application_detail(app: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 application detail dict.

    Includes additional detail fields beyond the summary.
    """
    result = _clean_application_summary(app)
    result.update(
        {
            "state_details": app.get("stateDetails", ""),
            "auto_start_configuration": app.get("autoStartConfiguration", {}),
            "auto_stop_configuration": app.get("autoStopConfiguration", {}),
            "network_configuration": app.get("networkConfiguration", {}),
        }
    )
    return result


class EMRApplicationManager:
    """High-level client for managing EMR Serverless applications.

    Uses ``EMRSkillConfig`` for region configuration.
    AWS credentials are resolved via boto3's default credential chain.
    """

    def __init__(self, config: EMRSkillConfig) -> None:
        self._client = get_emr_serverless_client(region=config.region)
        self._config = config

    @classmethod
    def from_env(cls) -> "EMRApplicationManager":
        """Create an instance using configuration loaded from environment."""
        return cls(load_emr_skill_config())

    def list_applications(
        self,
        states: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """List EMR Serverless applications, with optional state filtering.

        Handles pagination automatically to return all matching applications.

        Args:
            states: Optional list of application states to filter by.
                Valid values: CREATING, CREATED, STARTING, STARTED, STOPPING,
                STOPPED, TERMINATED.

        Returns:
            List of application dicts with keys: id, name, state, type,
            release_label, created_at, updated_at, architecture.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        applications: List[Dict[str, Any]] = []
        kwargs: Dict[str, Any] = {}
        if states:
            kwargs["states"] = states

        try:
            while True:
                response = self._client.list_applications(**kwargs)
                raw_apps = response.get("applications", [])
                applications.extend(_clean_application_summary(app) for app in raw_apps)

                next_token = response.get("nextToken")
                if not next_token:
                    break
                kwargs["nextToken"] = next_token

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to list EMR Serverless applications: [{error_code}] {error_msg}"
            ) from exc

        return applications

    def get_application(self, application_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific EMR Serverless application.

        Args:
            application_id: The EMR Serverless application ID.

        Returns:
            Application detail dict with keys: id, name, state, type,
            release_label, created_at, updated_at, architecture,
            state_details, auto_start_configuration,
            auto_stop_configuration, network_configuration.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            response = self._client.get_application(applicationId=application_id)
            return _clean_application_detail(response["application"])
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to get application '{application_id}': [{error_code}] {error_msg}"
            ) from exc

    def start_application(self, application_id: str) -> Dict[str, Any]:
        """Request an EMR Serverless application to start.

        Pre-initializes the application so job submissions start faster.

        Args:
            application_id: The EMR Serverless application ID.

        Returns:
            Dict with keys: application_id, status ('start_requested').

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            self._client.start_application(applicationId=application_id)
            return {
                "application_id": application_id,
                "status": "start_requested",
            }
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to start application '{application_id}': [{error_code}] {error_msg}"
            ) from exc

    def stop_application(self, application_id: str) -> Dict[str, Any]:
        """Request an EMR Serverless application to stop.

        Releases all resources associated with the application.

        Args:
            application_id: The EMR Serverless application ID.

        Returns:
            Dict with keys: application_id, status ('stop_requested').

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            self._client.stop_application(applicationId=application_id)
            return {
                "application_id": application_id,
                "status": "stop_requested",
            }
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to stop application '{application_id}': [{error_code}] {error_msg}"
            ) from exc
