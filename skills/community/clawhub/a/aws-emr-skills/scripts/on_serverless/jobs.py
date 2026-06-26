"""EMR Serverless job management via boto3.

Provides a high-level client for managing AWS EMR Serverless job runs:

- submit_spark_sql: Submit SQL queries via an embedded PySpark runner script.
- submit_spark_jar: Submit Spark JAR jobs with a main class.
- submit_pyspark: Submit PySpark script jobs.
- submit_hive_query: Submit Hive queries.
- get_job_run / cancel_job_run / list_job_runs: Job lifecycle management.
- get_job_result: Retrieve SQL result JSON from S3.
- get_driver_log / get_stderr_log: Retrieve compressed driver logs from S3.

All methods return clean Python dicts with snake_case keys, not raw boto3 responses.
AWS credentials are resolved via boto3's default credential chain.
"""

from __future__ import annotations

import gzip
import io
import json
import logging
import re
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_emr_serverless_client, get_s3_client
from scripts.config.emr_config import EMRSkillConfig, load_emr_skill_config

logger = logging.getLogger(__name__)

# Terminal states for EMR Serverless job runs.
_TERMINAL_STATES = {"SUCCESS", "FAILED", "CANCELLED"}


def _clean_job_run(job_run: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 job run dict.

    Converts camelCase boto3 keys to snake_case for consistency.
    """
    return {
        "job_run_id": job_run.get("jobRunId", ""),
        "name": job_run.get("name", ""),
        "application_id": job_run.get("applicationId", ""),
        "arn": job_run.get("arn", ""),
        "state": job_run.get("state", ""),
        "state_details": job_run.get("stateDetails", ""),
        "release_label": job_run.get("releaseLabel", ""),
        "created_by": job_run.get("createdBy", ""),
        "created_at": str(job_run.get("createdAt", "")),
        "updated_at": str(job_run.get("updatedAt", "")),
        "started_at": str(job_run.get("startedAt", "")),
        "ended_at": str(job_run.get("endedAt", "")),
        "execution_role": job_run.get("executionRole", ""),
        "total_execution_duration_seconds": job_run.get(
            "totalExecutionDurationSeconds"
        ),
    }


def _clean_job_run_summary(job_run: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 job run summary dict (list results)."""
    return {
        "job_run_id": job_run.get("id", ""),
        "name": job_run.get("name", ""),
        "application_id": job_run.get("applicationId", ""),
        "arn": job_run.get("arn", ""),
        "state": job_run.get("state", ""),
        "state_details": job_run.get("stateDetails", ""),
        "release_label": job_run.get("releaseLabel", ""),
        "created_by": job_run.get("createdBy", ""),
        "created_at": str(job_run.get("createdAt", "")),
        "updated_at": str(job_run.get("updatedAt", "")),
        "type": job_run.get("type", ""),
    }


class EMRServerlessJobManager:
    """High-level client for managing EMR Serverless job runs.

    Uses ``EMRSkillConfig`` for region, application ID, execution role, and S3 log URI.
    AWS credentials are resolved via boto3's default credential chain.

    Typical usage::

        from scripts.on_serverless.jobs import EMRServerlessJobManager

        mgr = EMRServerlessJobManager.from_env()
        result = mgr.submit_spark_sql("SELECT 1 AS test_col")
        print(result)
    """

    # Embedded PySpark script for running SQL queries.
    # This script is uploaded to S3 on first use and reused thereafter.
    _SQL_RUNNER_CODE = """
import sys
import json
from pyspark.sql import SparkSession

spark = SparkSession.builder.enableHiveSupport().getOrCreate()
sql = sys.argv[1]
result_path = sys.argv[2] if len(sys.argv) > 2 else None
df = spark.sql(sql)
df.show(100, truncate=False)
if result_path:
    rows = [row.asDict() for row in df.collect()]
    columns = df.columns
    result_json = json.dumps({"columns": columns, "rows": rows, "row_count": len(rows)})
    # Write to S3 via Hadoop filesystem
    sc = spark.sparkContext
    rdd = sc.parallelize([result_json])
    rdd.saveAsTextFile(result_path)
spark.stop()
"""

    def __init__(self, config: EMRSkillConfig) -> None:
        self._emr_client = get_emr_serverless_client(region=config.region)
        self._s3_client = get_s3_client(region=config.region)
        self._config = config

    @classmethod
    def from_env(cls) -> "EMRServerlessJobManager":
        """Create an instance using configuration loaded from environment."""
        return cls(load_emr_skill_config())

    # ------------------------------------------------------------------
    # Job submission methods
    # ------------------------------------------------------------------

    def submit_spark_sql(
        self,
        sql: str,
        *,
        name: Optional[str] = None,
        conf: Optional[Dict[str, Any]] = None,
        is_sync: bool = True,
        timeout: float = 300,
        polling_interval: float = 5,
    ) -> Dict[str, Any]:
        """Submit a Spark SQL query via an embedded PySpark runner script.

        The SQL runner script is automatically uploaded to S3 on first use.
        Query results are written to S3 as JSON and can be retrieved with
        :meth:`get_job_result`.

        Args:
            sql: SQL query text.
            name: Optional job run name.
            conf: Optional Spark configuration overrides as key-value pairs.
            is_sync: If True, wait for the job to reach a terminal state.
            timeout: Maximum wait time in seconds (only when is_sync=True).
            polling_interval: Seconds between status polls (only when is_sync=True).

        Returns:
            Job run info dict with snake_case keys.

        Raises:
            RuntimeError: If S3 upload or API call fails.
        """
        runner_s3_path = self._ensure_sql_runner_uploaded()

        # Build a unique S3 path for storing SQL results.
        result_id = uuid.uuid4().hex[:12]
        s3_log_uri = (self._config.s3_log_uri or "").rstrip("/")
        result_s3_path = f"{s3_log_uri}/skill-results/{result_id}/result.json"

        spark_submit: Dict[str, Any] = {
            "entryPoint": runner_s3_path,
            "entryPointArguments": [sql, result_s3_path],
        }
        spark_params = self._build_spark_params(conf)
        if spark_params:
            spark_submit["sparkSubmitParameters"] = spark_params
        job_driver: Dict[str, Any] = {"sparkSubmit": spark_submit}

        return self._submit_job(
            name=name,
            job_driver=job_driver,
            is_sync=is_sync,
            timeout=timeout,
            polling_interval=polling_interval,
        )

    def submit_spark_jar(
        self,
        *,
        jar: str,
        main_class: str,
        args: Optional[List[str]] = None,
        name: Optional[str] = None,
        conf: Optional[Dict[str, Any]] = None,
        is_sync: bool = True,
        timeout: float = 300,
        polling_interval: float = 5,
    ) -> Dict[str, Any]:
        """Submit a Spark JAR job.

        Args:
            jar: S3 URI of the JAR file (e.g., ``s3://bucket/path/app.jar``).
            main_class: Fully qualified main class name.
            args: Optional list of application arguments.
            name: Optional job run name.
            conf: Optional Spark configuration overrides.
            is_sync: If True, wait for the job to reach a terminal state.
            timeout: Maximum wait time in seconds.
            polling_interval: Seconds between status polls.

        Returns:
            Job run info dict with snake_case keys.

        Raises:
            RuntimeError: If the API call fails.
        """
        spark_params = self._build_spark_params(conf)
        submit_params = f"--class {main_class}"
        if spark_params:
            submit_params = f"{submit_params} {spark_params}"

        spark_submit: Dict[str, Any] = {
            "entryPoint": jar,
            "entryPointArguments": args or [],
        }
        if submit_params:
            spark_submit["sparkSubmitParameters"] = submit_params
        job_driver: Dict[str, Any] = {"sparkSubmit": spark_submit}

        return self._submit_job(
            name=name,
            job_driver=job_driver,
            is_sync=is_sync,
            timeout=timeout,
            polling_interval=polling_interval,
        )

    def submit_pyspark(
        self,
        *,
        script: str,
        args: Optional[List[str]] = None,
        name: Optional[str] = None,
        conf: Optional[Dict[str, Any]] = None,
        is_sync: bool = True,
        timeout: float = 300,
        polling_interval: float = 5,
    ) -> Dict[str, Any]:
        """Submit a PySpark script job.

        Args:
            script: S3 URI of the PySpark script (e.g., ``s3://bucket/scripts/job.py``).
            args: Optional list of script arguments.
            name: Optional job run name.
            conf: Optional Spark configuration overrides.
            is_sync: If True, wait for the job to reach a terminal state.
            timeout: Maximum wait time in seconds.
            polling_interval: Seconds between status polls.

        Returns:
            Job run info dict with snake_case keys.

        Raises:
            RuntimeError: If the API call fails.
        """
        spark_submit: Dict[str, Any] = {
            "entryPoint": script,
            "entryPointArguments": args or [],
        }
        spark_params = self._build_spark_params(conf)
        if spark_params:
            spark_submit["sparkSubmitParameters"] = spark_params
        job_driver: Dict[str, Any] = {"sparkSubmit": spark_submit}

        return self._submit_job(
            name=name,
            job_driver=job_driver,
            is_sync=is_sync,
            timeout=timeout,
            polling_interval=polling_interval,
        )

    def submit_hive_query(
        self,
        *,
        query: str,
        name: Optional[str] = None,
        parameters: Optional[str] = None,
        init_query_file: Optional[str] = None,
        is_sync: bool = True,
        timeout: float = 300,
        polling_interval: float = 5,
    ) -> Dict[str, Any]:
        """Submit a Hive query job.

        Args:
            query: Hive SQL query text.
            name: Optional job run name.
            parameters: Optional Hive parameters string.
            init_query_file: Optional S3 URI of an initialization query file.
            is_sync: If True, wait for the job to reach a terminal state.
            timeout: Maximum wait time in seconds.
            polling_interval: Seconds between status polls.

        Returns:
            Job run info dict with snake_case keys.

        Raises:
            RuntimeError: If the API call fails.
        """
        hive_config: Dict[str, Any] = {"query": query}
        if init_query_file:
            hive_config["initQueryFile"] = init_query_file
        if parameters:
            hive_config["parameters"] = parameters

        job_driver: Dict[str, Any] = {"hive": hive_config}

        return self._submit_job(
            name=name,
            job_driver=job_driver,
            is_sync=is_sync,
            timeout=timeout,
            polling_interval=polling_interval,
        )

    # ------------------------------------------------------------------
    # Job lifecycle methods
    # ------------------------------------------------------------------

    def get_job_run(
        self,
        job_run_id: str,
        application_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get detailed information for a specific job run.

        Args:
            job_run_id: The job run ID.
            application_id: Optional application ID override. Defaults to config.

        Returns:
            Job run detail dict with snake_case keys.

        Raises:
            RuntimeError: If the API call fails.
        """
        app_id = application_id or self._config.application_id
        try:
            response = self._emr_client.get_job_run(
                applicationId=app_id,
                jobRunId=job_run_id,
            )
            return _clean_job_run(response["jobRun"])
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to get job run '{job_run_id}': [{error_code}] {error_msg}"
            ) from exc

    def cancel_job_run(
        self,
        job_run_id: str,
        application_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Cancel a running job.

        Args:
            job_run_id: The job run ID to cancel.
            application_id: Optional application ID override. Defaults to config.

        Returns:
            Dict with job_run_id and cancelled status.

        Raises:
            RuntimeError: If the API call fails.
        """
        app_id = application_id or self._config.application_id
        try:
            self._emr_client.cancel_job_run(
                applicationId=app_id,
                jobRunId=job_run_id,
            )
            return {"job_run_id": job_run_id, "cancelled": True}
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to cancel job run '{job_run_id}': [{error_code}] {error_msg}"
            ) from exc

    def list_job_runs(
        self,
        application_id: Optional[str] = None,
        states: Optional[List[str]] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """List job runs for an application.

        Handles pagination automatically to return up to ``max_results`` job runs.

        Args:
            application_id: Optional application ID override. Defaults to config.
            states: Optional list of states to filter by (e.g., ``['RUNNING', 'SUCCESS']``).
            max_results: Maximum number of job runs to return.

        Returns:
            List of job run summary dicts with snake_case keys.

        Raises:
            RuntimeError: If the API call fails.
        """
        app_id = application_id or self._config.application_id
        job_runs: List[Dict[str, Any]] = []
        kwargs: Dict[str, Any] = {"applicationId": app_id}
        if states:
            kwargs["states"] = states

        try:
            while len(job_runs) < max_results:
                # Request up to remaining count per page.
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

    # ------------------------------------------------------------------
    # Result and log retrieval
    # ------------------------------------------------------------------

    def get_job_result(
        self,
        job_run_id: str,
        application_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve SQL result JSON from S3 for a completed SQL job run.

        The result is written by the embedded SQL runner script to a known S3 path.
        This method reads the result from S3, looking under the ``skill-results/``
        prefix for any result file associated with the job.

        Args:
            job_run_id: The job run ID.
            application_id: Optional application ID override.

        Returns:
            Dict with ``columns``, ``rows``, and ``row_count`` keys.

        Raises:
            RuntimeError: If reading from S3 fails or result is not found.
        """
        app_id = application_id or self._config.application_id

        # First get the job run to confirm it exists and is completed.
        job_info = self.get_job_run(job_run_id, app_id)
        if job_info.get("state") != "SUCCESS":
            return {
                "error": f"Job run is in state '{job_info.get('state')}', "
                "results are only available for SUCCESS state.",
                "job_run_id": job_run_id,
                "state": job_info.get("state", ""),
            }

        # Try reading the result from the skill-results directory.
        # The SQL runner writes to: {s3_log_uri}/skill-results/{uuid}/result.json/part-00000
        s3_log_uri = (self._config.s3_log_uri or "").rstrip("/")
        if not s3_log_uri:
            return {"error": "S3 log URI not configured, cannot retrieve results."}

        bucket, prefix = self._parse_s3_uri(s3_log_uri)
        results_prefix = f"{prefix}/skill-results/"

        try:
            # List objects under the skill-results prefix to find the result file.
            response = self._s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=results_prefix,
                MaxKeys=200,
            )
            contents = response.get("Contents", [])

            # Find the most recently modified part-00000 file.
            result_key = None
            latest_modified = None
            for obj in contents:
                key = obj["Key"]
                if key.endswith("/part-00000"):
                    modified = obj.get("LastModified")
                    if latest_modified is None or (
                        modified and modified > latest_modified
                    ):
                        latest_modified = modified
                        result_key = key

            if not result_key:
                return {
                    "error": "No result file found in S3 for this job run.",
                    "job_run_id": job_run_id,
                }

            # Read the result JSON.
            obj_response = self._s3_client.get_object(Bucket=bucket, Key=result_key)
            raw_text = obj_response["Body"].read().decode("utf-8").strip()
            return json.loads(raw_text)

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to read job result from S3: [{error_code}] {error_msg}"
            ) from exc
        except (json.JSONDecodeError, KeyError) as exc:
            raise RuntimeError(f"Failed to parse job result JSON: {exc}") from exc

    def get_driver_log(
        self,
        job_run_id: str,
        application_id: Optional[str] = None,
        max_lines: int = 100,
    ) -> List[str]:
        """Retrieve driver stdout log for a job run.

        Reads the gzip-compressed ``SPARK_DRIVER/stdout.gz`` from S3.

        Args:
            job_run_id: The job run ID.
            application_id: Optional application ID override.
            max_lines: Maximum number of log lines to return.

        Returns:
            List of log line strings.

        Raises:
            RuntimeError: If reading from S3 fails.
        """
        app_id = application_id or self._config.application_id or ""
        return self._read_spark_driver_log(app_id, job_run_id, "stdout.gz", max_lines)

    def get_stderr_log(
        self,
        job_run_id: str,
        application_id: Optional[str] = None,
        max_lines: int = 100,
    ) -> List[str]:
        """Retrieve driver stderr log for a job run.

        Reads the gzip-compressed ``SPARK_DRIVER/stderr.gz`` from S3.

        Args:
            job_run_id: The job run ID.
            application_id: Optional application ID override.
            max_lines: Maximum number of log lines to return.

        Returns:
            List of log line strings.

        Raises:
            RuntimeError: If reading from S3 fails.
        """
        app_id = application_id or self._config.application_id or ""
        return self._read_spark_driver_log(app_id, job_run_id, "stderr.gz", max_lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _submit_job(
        self,
        name: Optional[str],
        job_driver: Dict[str, Any],
        is_sync: bool,
        timeout: float,
        polling_interval: float,
    ) -> Dict[str, Any]:
        """Shared job submission logic.

        Calls ``start_job_run``, optionally waits for a terminal state.

        Args:
            name: Optional job run name.
            job_driver: The jobDriver parameter for the API call.
            is_sync: Whether to wait for completion.
            timeout: Maximum wait time in seconds.
            polling_interval: Seconds between status polls.

        Returns:
            Job run info dict.

        Raises:
            RuntimeError: If the API call fails.
        """
        app_id = self._config.application_id
        if not app_id:
            raise RuntimeError(
                "EMR Serverless application ID is not configured. "
                "Set EMR_SERVERLESS_APP_ID environment variable."
            )

        execution_role = self._config.execution_role_arn
        if not execution_role:
            raise RuntimeError(
                "EMR Serverless execution role ARN is not configured. "
                "Set EMR_SERVERLESS_EXEC_ROLE_ARN environment variable."
            )

        job_name = (
            name or f"{self._config.default_job_name_prefix}-{uuid.uuid4().hex[:8]}"
        )

        kwargs: Dict[str, Any] = {
            "applicationId": app_id,
            "executionRoleArn": execution_role,
            "jobDriver": job_driver,
            "name": job_name,
        }

        # Add S3 monitoring configuration if log URI is set.
        monitoring_config = self._build_monitoring_config()
        if monitoring_config:
            kwargs["configurationOverrides"] = {
                "monitoringConfiguration": monitoring_config
            }

        try:
            response = self._emr_client.start_job_run(**kwargs)
            job_run_id = response["jobRunId"]
            logger.info("Job run started: %s (name=%s)", job_run_id, job_name)
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to start job run: [{error_code}] {error_msg}"
            ) from exc

        if is_sync:
            return self._wait_for_job(job_run_id, app_id, timeout, polling_interval)

        # For async mode, return the initial submission info.
        return {
            "job_run_id": job_run_id,
            "application_id": app_id,
            "name": job_name,
            "state": "SUBMITTED",
            "arn": response.get("arn", ""),
        }

    def _wait_for_job(
        self,
        job_run_id: str,
        app_id: str,
        timeout: float,
        polling_interval: float,
    ) -> Dict[str, Any]:
        """Poll job run status until it reaches a terminal state or times out.

        Terminal states: SUCCESS, FAILED, CANCELLED.

        Args:
            job_run_id: The job run ID to monitor.
            app_id: The application ID.
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
                response = self._emr_client.get_job_run(
                    applicationId=app_id,
                    jobRunId=job_run_id,
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

    def _ensure_sql_runner_uploaded(self) -> str:
        """Ensure the SQL runner PySpark script exists in S3.

        Uploads the embedded script if it does not already exist.

        Returns:
            S3 URI of the SQL runner script.

        Raises:
            RuntimeError: If the S3 log URI is not configured or upload fails.
        """
        s3_log_uri = (self._config.s3_log_uri or "").rstrip("/")
        if not s3_log_uri:
            raise RuntimeError(
                "S3 log URI is not configured. Cannot upload SQL runner script. "
                "Set EMR_SERVERLESS_S3_LOG_URI environment variable."
            )

        runner_s3_uri = f"{s3_log_uri}/skill-assets/sql_runner.py"
        bucket, key = self._parse_s3_uri(runner_s3_uri)

        # Check if the script already exists in S3.
        try:
            self._s3_client.head_object(Bucket=bucket, Key=key)
            logger.debug("SQL runner script already exists at %s", runner_s3_uri)
            return runner_s3_uri
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            if error_code not in ("404", "NoSuchKey"):
                raise RuntimeError(
                    f"Failed to check SQL runner script in S3: [{error_code}] "
                    f"{exc.response['Error']['Message']}"
                ) from exc

        # Upload the script.
        try:
            self._s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=self._SQL_RUNNER_CODE.encode("utf-8"),
                ContentType="text/x-python",
            )
            logger.info("Uploaded SQL runner script to %s", runner_s3_uri)
            return runner_s3_uri
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to upload SQL runner script to S3: [{error_code}] {error_msg}"
            ) from exc

    def _read_spark_driver_log(
        self,
        app_id: str,
        job_run_id: str,
        log_filename: str,
        max_lines: int,
    ) -> List[str]:
        """Read a gzip-compressed Spark driver log file from S3.

        Log path pattern:
            ``{s3_log_uri}/applications/{app_id}/jobs/{job_run_id}/SPARK_DRIVER/{log_filename}``

        Args:
            app_id: Application ID.
            job_run_id: Job run ID.
            log_filename: Log filename (e.g., ``stdout.gz``, ``stderr.gz``).
            max_lines: Maximum number of lines to return.

        Returns:
            List of log line strings.

        Raises:
            RuntimeError: If reading from S3 fails.
        """
        s3_log_uri = (self._config.s3_log_uri or "").rstrip("/")
        if not s3_log_uri:
            return ["[Error] S3 log URI not configured, cannot retrieve logs."]

        log_s3_uri = (
            f"{s3_log_uri}/applications/{app_id}/jobs/{job_run_id}"
            f"/SPARK_DRIVER/{log_filename}"
        )
        bucket, key = self._parse_s3_uri(log_s3_uri)

        return self._read_s3_gzip_log(bucket, key, max_lines)

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

    def _build_monitoring_config(self) -> Dict[str, Any]:
        """Build the S3 monitoring configuration for job runs.

        Returns:
            Monitoring configuration dict, or empty dict if no S3 log URI is set.
        """
        s3_log_uri = self._config.s3_log_uri
        if not s3_log_uri:
            return {}
        return {
            "s3MonitoringConfiguration": {
                "logUri": s3_log_uri,
            }
        }

    @staticmethod
    def _build_spark_params(conf: Optional[Dict[str, Any]] = None) -> str:
        """Build a ``--conf k=v`` parameters string from a configuration dict.

        Args:
            conf: Optional dict of Spark configuration key-value pairs.

        Returns:
            Space-separated ``--conf key=value`` string, or empty string.
        """
        if not conf:
            return ""
        parts = [f"--conf {k}={v}" for k, v in conf.items()]
        return " ".join(parts)

    @staticmethod
    def _job_run_to_dict(job_run: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a raw boto3 job run dict to a clean snake_case dict.

        This is an alias for the module-level ``_clean_job_run`` for use
        by external callers who hold a reference to the class.
        """
        return _clean_job_run(job_run)

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
