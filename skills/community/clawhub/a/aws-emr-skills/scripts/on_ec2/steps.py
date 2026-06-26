"""EMR On EC2 step management via boto3.

Provides a high-level client for managing AWS EMR steps on EC2 clusters:

- add_spark_submit_step: Add a generic Spark submit step.
- add_pyspark_step: Add a PySpark script step.
- add_hive_step: Add a Hive script or query step.
- list_steps: List steps for a cluster with optional state filtering.
- describe_step: Retrieve detailed information for a single step.
- cancel_steps: Cancel running steps on a cluster.
- get_step_log: Retrieve step log from S3.

All methods return clean Python dicts with snake_case keys, not raw boto3 responses.
AWS credentials are resolved via boto3's default credential chain.
"""

from __future__ import annotations

import gzip
import io
import logging
import re
import uuid
from typing import Any, Dict, List, Optional, Tuple

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_emr_client, get_s3_client
from scripts.config.emr_config import EMRSkillConfig, load_emr_skill_config

logger = logging.getLogger(__name__)


def _clean_step_summary(step: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 step summary dict.

    Converts camelCase boto3 keys to snake_case for consistency.
    """
    status = step.get("Status", {})
    timeline = status.get("Timeline", {})
    failure = status.get("FailureDetails", {})
    config = step.get("Config", {})

    return {
        "id": step.get("Id", ""),
        "name": step.get("Name", ""),
        "state": status.get("State", ""),
        "action_on_failure": step.get("ActionOnFailure", ""),
        "jar": config.get("Jar", ""),
        "args": config.get("Args", []),
        "created_at": str(timeline.get("CreationDateTime", "")),
        "started_at": str(timeline.get("StartDateTime", "")),
        "ended_at": str(timeline.get("EndDateTime", "")),
        "failure_reason": failure.get("Reason", ""),
        "failure_message": failure.get("Message", ""),
        "failure_log_file": failure.get("LogFile", ""),
    }


def _clean_step_detail(step: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields from a boto3 describe_step response.

    Same structure as summary — describe_step returns the same fields.
    """
    return _clean_step_summary(step)


class EMRStepManager:
    """High-level client for managing EMR steps on EC2 clusters.

    Uses ``EMRSkillConfig`` for region configuration.
    AWS credentials are resolved via boto3's default credential chain.

    Typical usage::

        from scripts.on_ec2.steps import EMRStepManager

        mgr = EMRStepManager.from_env()
        result = mgr.add_pyspark_step("j-XXXXX", "s3://bucket/script.py")
        print(result)
    """

    def __init__(self, config: EMRSkillConfig) -> None:
        self._client = get_emr_client(region=config.region)
        self._s3_client = get_s3_client(region=config.region)
        self._config = config

    @classmethod
    def from_env(cls) -> "EMRStepManager":
        """Create an instance using configuration loaded from environment."""
        return cls(load_emr_skill_config())

    # ------------------------------------------------------------------
    # Step submission methods
    # ------------------------------------------------------------------

    def add_spark_submit_step(
        self,
        cluster_id: str,
        entry_point: str,
        *,
        name: Optional[str] = None,
        deploy_mode: str = "cluster",
        main_class: Optional[str] = None,
        args: Optional[List[str]] = None,
        conf: Optional[Dict[str, str]] = None,
        action_on_failure: str = "CONTINUE",
    ) -> Dict[str, Any]:
        """Add a Spark submit step to an EMR cluster.

        Builds a HadoopJarStep using ``command-runner.jar`` with ``spark-submit``.

        Args:
            cluster_id: The EMR cluster ID (e.g., ``j-XXXXXXXXXXXXX``).
            entry_point: S3 URI of the JAR or script to submit.
            name: Optional step name. Auto-generated if not provided.
            deploy_mode: Spark deploy mode (``cluster`` or ``client``).
            main_class: Fully qualified main class (for JAR submissions).
            args: Optional list of application arguments.
            conf: Optional dict of Spark configuration key-value pairs.
            action_on_failure: Action when step fails. Valid values:
                TERMINATE_CLUSTER, CANCEL_AND_WAIT, CONTINUE.

        Returns:
            Dict with keys: step_id, cluster_id, name.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        step_name = name or f"spark-submit-{uuid.uuid4().hex[:8]}"
        spark_args = self._build_spark_submit_args(
            entry_point, deploy_mode, main_class, args, conf
        )

        step_config = {
            "Name": step_name,
            "ActionOnFailure": action_on_failure,
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": ["spark-submit"] + spark_args,
            },
        }

        return self._add_step(cluster_id, step_config, step_name)

    def add_pyspark_step(
        self,
        cluster_id: str,
        script: str,
        *,
        name: Optional[str] = None,
        args: Optional[List[str]] = None,
        py_files: Optional[List[str]] = None,
        conf: Optional[Dict[str, str]] = None,
        action_on_failure: str = "CONTINUE",
    ) -> Dict[str, Any]:
        """Add a PySpark step to an EMR cluster.

        Builds a HadoopJarStep using ``command-runner.jar`` with ``spark-submit``
        for a PySpark script.

        Args:
            cluster_id: The EMR cluster ID.
            script: S3 URI of the PySpark script (e.g., ``s3://bucket/script.py``).
            name: Optional step name. Auto-generated if not provided.
            args: Optional list of script arguments.
            py_files: Optional list of additional Python files/archives.
            conf: Optional dict of Spark configuration key-value pairs.
            action_on_failure: Action when step fails.

        Returns:
            Dict with keys: step_id, cluster_id, name.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        step_name = name or f"pyspark-{uuid.uuid4().hex[:8]}"

        spark_args: List[str] = ["spark-submit", "--deploy-mode", "cluster"]

        if py_files:
            spark_args.extend(["--py-files", ",".join(py_files)])

        if conf:
            for k, v in conf.items():
                spark_args.extend(["--conf", f"{k}={v}"])

        spark_args.append(script)

        if args:
            spark_args.extend(args)

        step_config = {
            "Name": step_name,
            "ActionOnFailure": action_on_failure,
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": spark_args,
            },
        }

        return self._add_step(cluster_id, step_config, step_name)

    def add_hive_step(
        self,
        cluster_id: str,
        script_s3_uri: Optional[str] = None,
        *,
        query: Optional[str] = None,
        name: Optional[str] = None,
        args: Optional[List[str]] = None,
        action_on_failure: str = "CONTINUE",
    ) -> Dict[str, Any]:
        """Add a Hive step to an EMR cluster.

        Either ``script_s3_uri`` or ``query`` must be provided. If ``query``
        is provided, it is uploaded to a temporary S3 path first.

        Uses ``command-runner.jar`` with ``hive-script`` to run the query.

        Args:
            cluster_id: The EMR cluster ID.
            script_s3_uri: S3 URI of a Hive script file.
            query: Inline Hive query text. Uploaded to S3 if provided.
            name: Optional step name. Auto-generated if not provided.
            args: Optional additional Hive arguments (e.g., ``['-d', 'KEY=VAL']``).
            action_on_failure: Action when step fails.

        Returns:
            Dict with keys: step_id, cluster_id, name.

        Raises:
            ValueError: If neither script_s3_uri nor query is provided.
            RuntimeError: If the AWS API call fails or S3 upload fails.
        """
        if not script_s3_uri and not query:
            raise ValueError(
                "Either 'script_s3_uri' or 'query' must be provided for a Hive step."
            )

        step_name = name or f"hive-{uuid.uuid4().hex[:8]}"

        # If inline query is provided, upload to S3 first.
        if query and not script_s3_uri:
            script_s3_uri = self._upload_hive_query(cluster_id, query)

        hive_args: List[str] = [
            "hive-script",
            "--run-hive-script",
            "--args",
            "-f",
            script_s3_uri or "",
        ]

        if args:
            hive_args.extend(args)

        step_config = {
            "Name": step_name,
            "ActionOnFailure": action_on_failure,
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": hive_args,
            },
        }

        return self._add_step(cluster_id, step_config, step_name)

    # ------------------------------------------------------------------
    # Step lifecycle methods
    # ------------------------------------------------------------------

    def list_steps(
        self,
        cluster_id: str,
        *,
        states: Optional[List[str]] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """List steps for an EMR cluster.

        Handles pagination automatically to return up to ``max_results`` steps.

        Args:
            cluster_id: The EMR cluster ID.
            states: Optional list of step states to filter by.
                Valid values: PENDING, CANCEL_PENDING, RUNNING, COMPLETED,
                CANCELLED, FAILED, INTERRUPTED.
            max_results: Maximum number of steps to return.

        Returns:
            List of step dicts with keys: id, name, state, action_on_failure,
            jar, args, created_at, started_at, ended_at, failure_reason,
            failure_message, failure_log_file.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        steps: List[Dict[str, Any]] = []
        kwargs: Dict[str, Any] = {"ClusterId": cluster_id}
        if states:
            kwargs["StepStates"] = states

        try:
            while len(steps) < max_results:
                response = self._client.list_steps(**kwargs)
                raw_steps = response.get("Steps", [])
                steps.extend(_clean_step_summary(s) for s in raw_steps)

                marker = response.get("Marker")
                if not marker or not raw_steps:
                    break
                kwargs["Marker"] = marker

        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to list steps for cluster '{cluster_id}': "
                f"[{error_code}] {error_msg}"
            ) from exc

        return steps[:max_results]

    def describe_step(
        self,
        cluster_id: str,
        step_id: str,
    ) -> Dict[str, Any]:
        """Get detailed information for a specific EMR step.

        Args:
            cluster_id: The EMR cluster ID.
            step_id: The step ID (e.g., ``s-XXXXXXXXXXXXX``).

        Returns:
            Step detail dict with keys: id, name, state, action_on_failure,
            jar, args, created_at, started_at, ended_at, failure_reason,
            failure_message, failure_log_file.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            response = self._client.describe_step(
                ClusterId=cluster_id,
                StepId=step_id,
            )
            return _clean_step_detail(response["Step"])
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to describe step '{step_id}' on cluster '{cluster_id}': "
                f"[{error_code}] {error_msg}"
            ) from exc

    def cancel_steps(
        self,
        cluster_id: str,
        step_ids: List[str],
        *,
        cancel_option: str = "SEND_INTERRUPT",
    ) -> List[Dict[str, Any]]:
        """Cancel running EMR steps.

        Args:
            cluster_id: The EMR cluster ID.
            step_ids: List of step IDs to cancel.
            cancel_option: Cancellation option. Valid values:
                SEND_INTERRUPT, TERMINATE_PROCESS.

        Returns:
            List of dicts with keys: step_id, status, reason.

        Raises:
            RuntimeError: If the AWS API call fails.
        """
        try:
            response = self._client.cancel_steps(
                ClusterId=cluster_id,
                StepIds=step_ids,
                StepCancellationOption=cancel_option,
            )
            raw_results = response.get("CancelStepsInfoList", [])
            return [
                {
                    "step_id": r.get("StepId", ""),
                    "status": r.get("Status", ""),
                    "reason": r.get("Reason", ""),
                }
                for r in raw_results
            ]
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to cancel steps on cluster '{cluster_id}': "
                f"[{error_code}] {error_msg}"
            ) from exc

    # ------------------------------------------------------------------
    # Log retrieval
    # ------------------------------------------------------------------

    def get_step_log(
        self,
        cluster_id: str,
        step_id: str,
        *,
        log_type: str = "stderr",
        max_lines: int = 200,
    ) -> List[str]:
        """Retrieve step log from S3.

        Reads the gzip-compressed log file from the cluster's log URI:
        ``{log_uri}/{cluster_id}/steps/{step_id}/{log_type}.gz``

        Args:
            cluster_id: The EMR cluster ID.
            step_id: The step ID.
            log_type: Log type to retrieve (e.g., ``stderr``, ``stdout``,
                ``controller``, ``syslog``).
            max_lines: Maximum number of log lines to return.

        Returns:
            List of log line strings. Returns a descriptive message if
            the log is not found.
        """
        # Get log_uri from cluster description.
        try:
            cluster_info = self.describe_cluster_for_log(cluster_id)
            log_uri = cluster_info.get("log_uri", "")
        except RuntimeError:
            return [
                f"[Log not found] Could not describe cluster '{cluster_id}' "
                "to determine log URI."
            ]

        if not log_uri:
            return [
                f"[Log not found] Cluster '{cluster_id}' does not have a log URI configured."
            ]

        # Build S3 path: {log_uri}/{cluster_id}/steps/{step_id}/{log_type}.gz
        log_uri = log_uri.rstrip("/")
        log_s3_uri = f"{log_uri}/{cluster_id}/steps/{step_id}/{log_type}.gz"
        bucket, key = self._parse_s3_uri(log_s3_uri)

        return self._read_s3_gzip_log(bucket, key, max_lines)

    def describe_cluster_for_log(self, cluster_id: str) -> Dict[str, Any]:
        """Get cluster description for log retrieval (minimal wrapper).

        Args:
            cluster_id: The EMR cluster ID.

        Returns:
            Dict with log_uri key.

        Raises:
            RuntimeError: If the API call fails.
        """
        try:
            response = self._client.describe_cluster(ClusterId=cluster_id)
            cluster = response["Cluster"]
            return {"log_uri": cluster.get("LogUri", "")}
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to describe cluster '{cluster_id}': [{error_code}] {error_msg}"
            ) from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _add_step(
        self,
        cluster_id: str,
        step_config: Dict[str, Any],
        step_name: str,
    ) -> Dict[str, Any]:
        """Shared step submission logic.

        Calls ``add_job_flow_steps`` and returns a clean result dict.

        Args:
            cluster_id: The EMR cluster ID.
            step_config: The step configuration dict for the API call.
            step_name: The step name for the response.

        Returns:
            Dict with keys: step_id, cluster_id, name.

        Raises:
            RuntimeError: If the API call fails.
        """
        try:
            response = self._client.add_job_flow_steps(
                JobFlowId=cluster_id,
                Steps=[step_config],
            )
            step_ids = response.get("StepIds", [])
            step_id = step_ids[0] if step_ids else ""
            logger.info(
                "Step added: %s (name=%s) to cluster %s",
                step_id,
                step_name,
                cluster_id,
            )
            return {
                "step_id": step_id,
                "cluster_id": cluster_id,
                "name": step_name,
            }
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to add step to cluster '{cluster_id}': "
                f"[{error_code}] {error_msg}"
            ) from exc

    def _upload_hive_query(self, cluster_id: str, query: str) -> str:
        """Upload an inline Hive query to a temporary S3 path.

        Uses the cluster's log URI as a base path for the temporary script.

        Args:
            cluster_id: The EMR cluster ID (for log URI lookup).
            query: Hive SQL query text.

        Returns:
            S3 URI of the uploaded query script.

        Raises:
            RuntimeError: If S3 upload fails or log URI is not available.
        """
        # Get log_uri from cluster to determine S3 base path.
        try:
            cluster_info = self.describe_cluster_for_log(cluster_id)
            log_uri = cluster_info.get("log_uri", "")
        except RuntimeError as exc:
            raise RuntimeError(
                f"Cannot upload Hive query: failed to get log URI for cluster "
                f"'{cluster_id}': {exc}"
            ) from exc

        if not log_uri:
            raise RuntimeError(
                f"Cannot upload Hive query: cluster '{cluster_id}' has no log URI. "
                "Provide a 'script_s3_uri' instead."
            )

        log_uri = log_uri.rstrip("/")
        query_id = uuid.uuid4().hex[:12]
        script_s3_uri = f"{log_uri}/skill-scripts/hive-{query_id}.sql"
        bucket, key = self._parse_s3_uri(script_s3_uri)

        try:
            self._s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=query.encode("utf-8"),
                ContentType="text/x-sql",
            )
            logger.info("Uploaded Hive query to %s", script_s3_uri)
            return script_s3_uri
        except ClientError as exc:
            error_code = exc.response["Error"]["Code"]
            error_msg = exc.response["Error"]["Message"]
            raise RuntimeError(
                f"Failed to upload Hive query to S3: [{error_code}] {error_msg}"
            ) from exc

    @staticmethod
    def _build_spark_submit_args(
        entry_point: str,
        deploy_mode: str,
        main_class: Optional[str],
        args: Optional[List[str]],
        conf: Optional[Dict[str, str]],
    ) -> List[str]:
        """Build the args list for spark-submit via command-runner.jar.

        Args:
            entry_point: S3 URI of the JAR or script.
            deploy_mode: Spark deploy mode.
            main_class: Optional main class for JAR submissions.
            args: Optional application arguments.
            conf: Optional Spark configuration key-value pairs.

        Returns:
            List of spark-submit argument strings.
        """
        spark_args: List[str] = ["--deploy-mode", deploy_mode]

        if main_class:
            spark_args.extend(["--class", main_class])

        if conf:
            for k, v in conf.items():
                spark_args.extend(["--conf", f"{k}={v}"])

        spark_args.append(entry_point)

        if args:
            spark_args.extend(args)

        return spark_args

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
