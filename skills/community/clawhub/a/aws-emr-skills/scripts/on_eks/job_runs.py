"""EMR on EKS job run management via boto3.

Provides a high-level client for managing AWS EMR on EKS job runs:

- submit_spark_job: Submit Spark jobs via sparkSubmitJobDriver.
- submit_spark_sql: Submit Spark SQL jobs via sparkSqlJobDriver.
- describe_job_run: Retrieve detailed information for a single job run.
- list_job_runs: List job runs with optional state filtering, handles pagination.
- cancel_job_run: Cancel a running job.
- get_job_log: Retrieve compressed driver logs from S3.

All methods return clean Python dicts with snake_case keys, not raw boto3 responses.
AWS credentials are resolved via boto3's default credential chain.
"""

from __future__ import annotations

import gzip
import io
import logging
import re
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_emr_containers_client, get_s3_client
from scripts.config.emr_config import EMRSkillConfig, load_emr_skill_config

logger = logging.getLogger(__name__)

# Terminal states for EMR on EKS job runs.
_TERMINAL_STATES = {"COMPLETED", "FAILED", "CANCELLED"}


def _clean_job_run(job_run: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 job run detail dict.

    Converts camelCase boto3 keys to snake_case for consistency.
    """
    return {
        "id": job_run.get("id", ""),
        "name": job_run.get("name", ""),
        "arn": job_run.get("arn", ""),
        "virtual_cluster_id": job_run.get("virtualClusterId", ""),
        "state": job_run.get("state", ""),
        "state_details": job_run.get("stateDetails", ""),
        "created_at": str(job_run.get("createdAt", "")),
        "finished_at": str(job_run.get("finishedAt", "")),
        "execution_role_arn": job_run.get("executionRoleArn", ""),
        "release_label": job_run.get("releaseLabel", ""),
    }


def _clean_job_run_summary(job_run: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 job run summary dict (list results)."""
    return {
        "id": job_run.get("id", ""),
        "name": job_run.get("name", ""),
        "arn": job_run.get("arn", ""),
        "virtual_cluster_id": job_run.get("virtualClusterId", ""),
        "state": job_run.get("state", ""),
        "state_details": job_run.get("stateDetails", ""),
        "created_at": str(job_run.get("createdAt", "")),
        "finished_at": str(job_run.get("finishedAt", "")),
        "execution_role_arn": job_run.get("executionRoleArn", ""),
        "release_label": job_run.get("releaseLabel", ""),
    }


class EMRContainersJobRunManager:
    """High-level client for managing EMR on EKS job runs.

    Uses ``EMRSkillConfig`` for region, virtual cluster ID, execution role,
    and S3 log URI. AWS credentials are resolved via boto3's default
    credential chain.

    Typical usage::

        from scripts.on_eks.job_runs import EMRContainersJobRunManager

        mgr = EMRContainersJobRunManager.from_env()
        result = mgr.submit_spark_job("vc-123", "s3://bucket/script.py")
        print(result)
    """

    def __init__(self, config: EMRSkillConfig) -> None:
        self._emr_client = get_emr_containers_client(region=config.region)
        self._s3_client = get_s3_client(region=config.region)
        self._config = config

    @classmethod
    def from_env(cls) -> "EMRContainersJobRunManager":
        """Create an instance using configuration loaded from environment."""
        return cls(load_emr_skill_config())

    # ------------------------------------------------------------------
    # Job submission methods
    # ------------------------------------------------------------------

    def submit_spark_job(
        self,
        virtual_cluster_id: Optional[str],
        entry_point: str,
        *,
        name: Optional[str] = None,
        execution_role_arn: Optional[str] = None,
        release_label: str = "emr-7.1.0-latest",
        entry_point_args: Optional[List[str]] = None,
        spark_submit_params: Optional[str] = None,
        conf: Optional[Dict[str, str]] = None,
        s3_log_uri: Optional[str] = None,
        cloudwatch_log_group: Optional[str] = None,
        is_sync: bool = False,
        timeout: float = 600,
        polling_interval: float = 30,
    ) -> Dict[str, Any]:
        """Submit a Spark job to EMR on EKS using sparkSubmitJobDriver.

        Args:
            virtual_cluster_id: The virtual cluster ID. Falls back to config.
            entry_point: S3 URI of the Spark script or JAR entry point.
            name: Optional job run name.
            execution_role_arn: IAM execution role ARN. Falls back to config.
            release_label: EMR release label (default: ``emr-7.1.0-latest``).
            entry_point_args: Optional list of entry point arguments.
            spark_submit_params: Optional spark-submit parameters string.
            conf: Optional Spark configuration overrides as key-value pairs.
            s3_log_uri: Optional S3 URI for log output. Falls back to config.
            cloudwatch_log_group: Optional CloudWatch log group name.
            is_sync: If True, wait for the job to reach a terminal state.
            timeout: Maximum wait time in seconds (only when is_sync=True).
            polling_interval: Seconds between status polls (only when is_sync=True).

        Returns:
            Job run info dict with keys: id, name, arn, virtual_cluster_id,
            state, state_details, created_at, finished_at, execution_role_arn,
            release_label.

        Raises:
            RuntimeError: If the API call fails or required config is missing.
        """
        vc_id = virtual_cluster_id or self._config.virtual_cluster_id
        if not vc_id:
            raise RuntimeError(
                "Virtual cluster ID is not configured. "
                "Provide virtual_cluster_id or set EMR_EKS_VIRTUAL_CLUSTER_ID."
            )

        role_arn = execution_role_arn or self._config.eks_execution_role_arn
        if not role_arn:
            raise RuntimeError(
                "EKS execution role ARN is not configured. "
                "Provide execution_role_arn or set EMR_EKS_EXEC_ROLE_ARN."
            )

        job_name = (
            name or f"{self._config.default_job_name_prefix}-{uuid.uuid4().hex[:8]}"
        )

        # Build sparkSubmitJobDriver
        spark_submit_driver: Dict[str, Any] = {
            "entryPoint": entry_point,
        }
        if entry_point_args:
            spark_submit_driver["entryPointArguments"] = entry_point_args

        # Merge conf into spark_submit_params
        submit_params = self._build_spark_params(spark_submit_params, conf)
        if submit_params:
            spark_submit_driver["sparkSubmitParameters"] = submit_params

        job_driver: Dict[str, Any] = {
            "sparkSubmitJobDriver": spark_submit_driver,
        }

        # Build monitoring configuration
        log_uri = s3_log_uri or self._config.s3_log_uri
        monitoring = self._build_monitoring_config(log_uri, cloudwatch_log_group)

        kwargs: Dict[str, Any] = {
            "virtualClusterId": vc_id,
            "name": job_name,
            "executionRoleArn": role_arn,
            "releaseLabel": release_label,
            "jobDriver": job_driver,
        }
        if monitoring:
            kwargs["configurationOverrides"] = {
                "monitoringConfiguration": monitoring,
            }

        try:
            response = self._emr_client.start_job_run(**kwargs)
            job_run_id = response["id"]
            logger.info("Job run started: %s (name=%s)", job_run_id, job_name)
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to start job run: [{error_code}] {error_msg}"
            ) from exc

        if is_sync:
            return self._wait_for_job(job_run_id, vc_id, timeout, polling_interval)

        return {
            "id": job_run_id,
            "name": job_name,
            "arn": response.get("arn", ""),
            "virtual_cluster_id": vc_id,
            "state": "PENDING",
            "state_details": "",
            "created_at": "",
            "finished_at": "",
            "execution_role_arn": role_arn,
            "release_label": release_label,
        }

    def submit_spark_sql(
        self,
        virtual_cluster_id: Optional[str],
        sql_entry_point: str,
        *,
        name: Optional[str] = None,
        execution_role_arn: Optional[str] = None,
        release_label: str = "emr-7.1.0-latest",
        spark_sql_params: Optional[str] = None,
        s3_log_uri: Optional[str] = None,
        is_sync: bool = False,
        timeout: float = 600,
        polling_interval: float = 30,
    ) -> Dict[str, Any]:
        """Submit a Spark SQL job to EMR on EKS using sparkSqlJobDriver.

        Args:
            virtual_cluster_id: The virtual cluster ID. Falls back to config.
            sql_entry_point: S3 URI of the SQL script file.
            name: Optional job run name.
            execution_role_arn: IAM execution role ARN. Falls back to config.
            release_label: EMR release label (default: ``emr-7.1.0-latest``).
            spark_sql_params: Optional Spark SQL parameters string.
            s3_log_uri: Optional S3 URI for log output. Falls back to config.
            is_sync: If True, wait for the job to reach a terminal state.
            timeout: Maximum wait time in seconds (only when is_sync=True).
            polling_interval: Seconds between status polls (only when is_sync=True).

        Returns:
            Job run info dict with keys: id, name, arn, virtual_cluster_id,
            state, state_details, created_at, finished_at, execution_role_arn,
            release_label.

        Raises:
            RuntimeError: If the API call fails or required config is missing.
        """
        vc_id = virtual_cluster_id or self._config.virtual_cluster_id
        if not vc_id:
            raise RuntimeError(
                "Virtual cluster ID is not configured. "
                "Provide virtual_cluster_id or set EMR_EKS_VIRTUAL_CLUSTER_ID."
            )

        role_arn = execution_role_arn or self._config.eks_execution_role_arn
        if not role_arn:
            raise RuntimeError(
                "EKS execution role ARN is not configured. "
                "Provide execution_role_arn or set EMR_EKS_EXEC_ROLE_ARN."
            )

        job_name = (
            name or f"{self._config.default_job_name_prefix}-{uuid.uuid4().hex[:8]}"
        )

        # Build sparkSqlJobDriver
        spark_sql_driver: Dict[str, Any] = {
            "entryPoint": sql_entry_point,
        }
        if spark_sql_params:
            spark_sql_driver["sparkSqlParameters"] = spark_sql_params

        job_driver: Dict[str, Any] = {
            "sparkSqlJobDriver": spark_sql_driver,
        }

        # Build monitoring configuration
        log_uri = s3_log_uri or self._config.s3_log_uri
        monitoring = self._build_monitoring_config(log_uri)

        kwargs: Dict[str, Any] = {
            "virtualClusterId": vc_id,
            "name": job_name,
            "executionRoleArn": role_arn,
            "releaseLabel": release_label,
            "jobDriver": job_driver,
        }
        if monitoring:
            kwargs["configurationOverrides"] = {
                "monitoringConfiguration": monitoring,
            }

        try:
            response = self._emr_client.start_job_run(**kwargs)
            job_run_id = response["id"]
            logger.info("Spark SQL job run started: %s (name=%s)", job_run_id, job_name)
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to start Spark SQL job run: [{error_code}] {error_msg}"
            ) from exc

        if is_sync:
            return self._wait_for_job(job_run_id, vc_id, timeout, polling_interval)

        return {
            "id": job_run_id,
            "name": job_name,
            "arn": response.get("arn", ""),
            "virtual_cluster_id": vc_id,
            "state": "PENDING",
            "state_details": "",
            "created_at": "",
            "finished_at": "",
            "execution_role_arn": role_arn,
            "release_label": release_label,
        }

    # ------------------------------------------------------------------
    # Job lifecycle methods
    # ------------------------------------------------------------------

    def describe_job_run(
        self,
        job_run_id: str,
        virtual_cluster_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get detailed information for a specific EMR on EKS job run.

        Args:
            job_run_id: The job run ID.
            virtual_cluster_id: Optional virtual cluster ID override. Falls back to config.

        Returns:
            Job run detail dict with keys: id, name, arn, virtual_cluster_id,
            state, state_details, created_at, finished_at, execution_role_arn,
            release_label.

        Raises:
            RuntimeError: If the API call fails.
        """
        vc_id = virtual_cluster_id or self._config.virtual_cluster_id
        if not vc_id:
            raise RuntimeError(
                "Virtual cluster ID is not configured. "
                "Provide virtual_cluster_id or set EMR_EKS_VIRTUAL_CLUSTER_ID."
            )

        try:
            response = self._emr_client.describe_job_run(
                virtualClusterId=vc_id,
                id=job_run_id,
            )
            return _clean_job_run(response["jobRun"])
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to describe job run '{job_run_id}': [{error_code}] {error_msg}"
            ) from exc

    def list_job_runs(
        self,
        virtual_cluster_id: Optional[str] = None,
        *,
        states: Optional[List[str]] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """List job runs for an EMR on EKS virtual cluster.

        Handles pagination automatically to return up to ``max_results`` job runs.

        Args:
            virtual_cluster_id: Optional virtual cluster ID override. Falls back to config.
            states: Optional list of states to filter by.
                Valid values: PENDING, SUBMITTED, RUNNING, COMPLETED, FAILED,
                CANCELLED, CANCEL_PENDING.
            max_results: Maximum number of job runs to return.

        Returns:
            List of job run summary dicts with snake_case keys.

        Raises:
            RuntimeError: If the API call fails.
        """
        vc_id = virtual_cluster_id or self._config.virtual_cluster_id
        if not vc_id:
            raise RuntimeError(
                "Virtual cluster ID is not configured. "
                "Provide virtual_cluster_id or set EMR_EKS_VIRTUAL_CLUSTER_ID."
            )

        job_runs: List[Dict[str, Any]] = []
        kwargs: Dict[str, Any] = {"virtualClusterId": vc_id}
        if states:
            kwargs["states"] = states

        try:
            while len(job_runs) < max_results:
                kwargs["maxResults"] = min(50, max_results - len(job_runs))
                response = self._emr_client.list_job_runs(**kwargs)
                raw_runs = response.get("jobRuns", [])
                job_runs.extend(_clean_job_run_summary(r) for r in raw_runs)

                next_token = response.get("nextToken")
                if not next_token or not raw_runs:
                    break
                kwargs["nextToken"] = next_token

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to list job runs: [{error_code}] {error_msg}"
            ) from exc

        return job_runs[:max_results]

    def cancel_job_run(
        self,
        job_run_id: str,
        virtual_cluster_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Cancel a running EMR on EKS job.

        Args:
            job_run_id: The job run ID to cancel.
            virtual_cluster_id: Optional virtual cluster ID override. Falls back to config.

        Returns:
            Dict with keys: id, virtual_cluster_id, status ('cancel_requested').

        Raises:
            RuntimeError: If the API call fails.
        """
        vc_id = virtual_cluster_id or self._config.virtual_cluster_id
        if not vc_id:
            raise RuntimeError(
                "Virtual cluster ID is not configured. "
                "Provide virtual_cluster_id or set EMR_EKS_VIRTUAL_CLUSTER_ID."
            )

        try:
            self._emr_client.cancel_job_run(
                virtualClusterId=vc_id,
                id=job_run_id,
            )
            return {
                "id": job_run_id,
                "virtual_cluster_id": vc_id,
                "status": "cancel_requested",
            }
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to cancel job run '{job_run_id}': [{error_code}] {error_msg}"
            ) from exc

    # ------------------------------------------------------------------
    # Log retrieval
    # ------------------------------------------------------------------

    def get_job_log(
        self,
        job_run_id: str,
        virtual_cluster_id: Optional[str] = None,
        *,
        log_type: str = "stderr",
        max_lines: int = 200,
    ) -> List[str]:
        """Retrieve driver log from S3 for an EMR on EKS job run.

        Attempts to locate and download the gzip-compressed driver log from S3.
        The exact log path is unpredictable (container names vary), so this method
        uses ``list_objects_v2`` to discover the driver log file.

        Log path pattern:
            ``{s3_log_uri}/{virtual_cluster_id}/jobs/{job_run_id}/containers/spark-*/spark-*-driver/{log_type}.gz``

        Args:
            job_run_id: The job run ID.
            virtual_cluster_id: Optional virtual cluster ID override. Falls back to config.
            log_type: Type of log to retrieve (``stderr`` or ``stdout``).
            max_lines: Maximum number of log lines to return.

        Returns:
            List of log line strings.

        Raises:
            RuntimeError: If S3 access fails unexpectedly.
        """
        vc_id = virtual_cluster_id or self._config.virtual_cluster_id
        if not vc_id:
            return ["[Error] Virtual cluster ID is not configured."]

        s3_log_uri = (self._config.s3_log_uri or "").rstrip("/")
        if not s3_log_uri:
            return ["[Error] S3 log URI not configured, cannot retrieve logs."]

        # Build the prefix to search for driver logs
        log_prefix = f"{vc_id}/jobs/{job_run_id}/containers/"
        bucket, base_prefix = self._parse_s3_uri(s3_log_uri)
        search_prefix = f"{base_prefix}/{log_prefix}" if base_prefix else log_prefix

        log_filename = f"{log_type}.gz"

        try:
            # List objects to find the driver log file
            response = self._s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=search_prefix,
                MaxKeys=500,
            )
            contents = response.get("Contents", [])

            # Find the driver log matching the pattern: .../spark-*-driver/{log_type}.gz
            driver_log_key = None
            for obj in contents:
                key = obj["Key"]
                if key.endswith(f"-driver/{log_filename}"):
                    driver_log_key = key
                    break

            if not driver_log_key:
                return [
                    f"[Log not found] No driver {log_type} log found for "
                    f"job run '{job_run_id}' under s3://{bucket}/{search_prefix}"
                ]

            return self._read_s3_gzip_log(bucket, driver_log_key, max_lines)

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            if error_code in ("NoSuchKey", "404", "NoSuchBucket"):
                return [
                    f"[Log not found] s3://{bucket}/{search_prefix} "
                    f"- [{error_code}] {error_msg}"
                ]
            raise RuntimeError(
                f"Failed to list log objects from S3: [{error_code}] {error_msg}"
            ) from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _wait_for_job(
        self,
        job_run_id: str,
        virtual_cluster_id: str,
        timeout: float,
        polling_interval: float,
    ) -> Dict[str, Any]:
        """Poll job run status until it reaches a terminal state or times out.

        Terminal states: COMPLETED, FAILED, CANCELLED.

        Args:
            job_run_id: The job run ID to monitor.
            virtual_cluster_id: The virtual cluster ID.
            timeout: Maximum wait time in seconds.
            polling_interval: Seconds between status polls.

        Returns:
            Final job run info dict.

        Raises:
            RuntimeError: If the job times out or API calls fail.
        """
        start_time = time.monotonic()
        last_state = ""

        while True:
            elapsed = time.monotonic() - start_time
            if elapsed > timeout:
                raise RuntimeError(
                    f"Job run '{job_run_id}' timed out after {timeout}s. "
                    f"Last state: {last_state}"
                )

            try:
                response = self._emr_client.describe_job_run(
                    virtualClusterId=virtual_cluster_id,
                    id=job_run_id,
                )
                job_run = response["jobRun"]
                current_state = job_run.get("state", "")
                last_state = current_state

                if current_state in _TERMINAL_STATES:
                    logger.info(
                        "Job run %s reached terminal state: %s",
                        job_run_id,
                        current_state,
                    )
                    return _clean_job_run(job_run)

                logger.debug(
                    "Job run %s state: %s (%.1fs elapsed)",
                    job_run_id,
                    current_state,
                    elapsed,
                )

            except ClientError as exc:
                error_code = exc.response["Error"]["Code"]
                error_msg = exc.response["Error"]["Message"]
                logger.warning(
                    "Error polling job run %s: [%s] %s",
                    job_run_id,
                    error_code,
                    error_msg,
                )

            time.sleep(polling_interval)

    @staticmethod
    def _parse_s3_uri(uri: str) -> Tuple[str, str]:
        """Parse an S3 URI into (bucket, key).

        Args:
            uri: S3 URI in the form ``s3://bucket/key/path``.

        Returns:
            Tuple of (bucket_name, object_key).

        Raises:
            ValueError: If the URI is not a valid S3 URI.
        """
        if not uri.startswith("s3://"):
            raise ValueError(f"Invalid S3 URI (must start with 's3://'): {uri}")
        path = uri[5:]  # Remove 's3://' prefix
        parts = path.split("/", 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ""
        return bucket, key

    def _read_s3_gzip_log(
        self,
        bucket: str,
        key: str,
        max_lines: int,
    ) -> List[str]:
        """Download and decompress a gzip log file from S3.

        Args:
            bucket: S3 bucket name.
            key: S3 object key.
            max_lines: Maximum number of lines to return.

        Returns:
            List of log line strings.
        """
        try:
            response = self._s3_client.get_object(Bucket=bucket, Key=key)
            compressed_data = response["Body"].read()

            with gzip.GzipFile(fileobj=io.BytesIO(compressed_data)) as gz:
                text = gz.read().decode("utf-8", errors="replace")

            lines = text.splitlines()
            if max_lines and len(lines) > max_lines:
                lines = lines[:max_lines]
            return lines

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            if error_code in ("NoSuchKey", "404"):
                return [f"[Log not found] s3://{bucket}/{key}"]
            raise RuntimeError(
                f"Failed to read log from S3: [{error_code}] {error_msg}"
            ) from exc
        except (OSError, UnicodeDecodeError) as exc:
            return [f"[Error reading log] {exc}"]

    @staticmethod
    def _build_spark_params(
        spark_submit_params: Optional[str] = None,
        conf: Optional[Dict[str, str]] = None,
    ) -> str:
        """Build a combined spark-submit parameters string.

        Merges explicit parameters with ``--conf`` entries from the conf dict.

        Args:
            spark_submit_params: Optional base spark-submit parameters string.
            conf: Optional dict of Spark configuration key-value pairs.

        Returns:
            Combined parameters string, or empty string.
        """
        parts: List[str] = []
        if spark_submit_params:
            parts.append(spark_submit_params)
        if conf:
            conf_parts = [f"--conf {k}={v}" for k, v in conf.items()]
            parts.extend(conf_parts)
        return " ".join(parts)

    @staticmethod
    def _build_monitoring_config(
        s3_log_uri: Optional[str] = None,
        cloudwatch_log_group: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build the monitoring configuration for job runs.

        Args:
            s3_log_uri: Optional S3 URI for log output.
            cloudwatch_log_group: Optional CloudWatch log group name.

        Returns:
            Monitoring configuration dict, or empty dict if no config is set.
        """
        config: Dict[str, Any] = {}
        if s3_log_uri:
            config["s3MonitoringConfiguration"] = {
                "logUri": s3_log_uri,
            }
        if cloudwatch_log_group:
            config["cloudWatchMonitoringConfiguration"] = {
                "logGroupName": cloudwatch_log_group,
            }
        return config

    @staticmethod
    def _mask_secrets(text: str) -> str:
        """Mask potential AWS credentials and secrets in log text.

        Replaces long alphanumeric strings (likely access keys or secret keys)
        with a masked version showing only the first and last 3 characters.

        Args:
            text: Input text that may contain secrets.

        Returns:
            Text with secrets masked.
        """

        def _repl(m: re.Match[str]) -> str:
            s = m.group(0)
            if len(s) <= 6:
                return s
            return s[:3] + "***" + s[-3:]

        pattern = re.compile(
            r"(?i)(?<![A-Za-z0-9_])[A-Za-z0-9_\-+=]{20,}(?![A-Za-z0-9_])"
        )
        return pattern.sub(_repl, text)
