from __future__ import annotations

"""AWS EMR Serverless Skill tool interface.

Exposes 14 ``@tool``-decorated functions for agent integration, covering:

- Application management: ``list_applications``, ``get_application``,
  ``start_application``, ``stop_application``;
- Job submission: ``submit_spark_sql``, ``submit_spark_jar``, ``submit_pyspark``,
  ``submit_hive_query``;
- Job lifecycle: ``get_job_run``, ``cancel_job_run``, ``list_job_runs``;
- Results: ``get_job_result``;
- Logs: ``get_driver_log``, ``get_stderr_log``.

All functions delegate to :class:`~scripts.on_serverless.applications.EMRApplicationManager`
and :class:`~scripts.on_serverless.jobs.EMRServerlessJobManager`. Configuration is loaded
from environment variables via :func:`~scripts.config.emr_config.load_emr_skill_config`.
"""

from typing import Any, Dict, List, Optional, Tuple

from scripts.config.emr_config import (
    EMRSkillConfig,
    EMRSkillConfigError,
    load_emr_skill_config,
)
from scripts.on_serverless.applications import EMRApplicationManager
from scripts.on_serverless.jobs import EMRServerlessJobManager


def tool(func):  # type: ignore[override]
    """Placeholder decorator for agent tool registration.

    In a real agent environment this is replaced by the framework's ``@tool``.
    """
    return func


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _build_app_manager() -> Tuple[EMRSkillConfig, EMRApplicationManager]:
    """Load configuration and create an application manager.

    Returns:
        Tuple of (config, manager).

    Raises:
        RuntimeError: If configuration loading or client creation fails.
    """
    try:
        config = load_emr_skill_config()
    except EMRSkillConfigError as exc:
        raise RuntimeError(f"EMR Skill configuration error: {exc}") from exc
    try:
        manager = EMRApplicationManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize EMR application manager: {exc}"
        ) from exc
    return config, manager


def _build_job_manager(
    application_id: Optional[str] = None,
) -> Tuple[EMRSkillConfig, EMRServerlessJobManager]:
    """Load configuration and create a job manager.

    Args:
        application_id: Optional application ID override. When provided,
            replaces the config's application_id before manager creation.

    Returns:
        Tuple of (config, manager).

    Raises:
        RuntimeError: If configuration loading or client creation fails.
    """
    try:
        config = load_emr_skill_config()
    except EMRSkillConfigError as exc:
        raise RuntimeError(f"EMR Skill configuration error: {exc}") from exc

    if application_id:
        config.application_id = application_id

    try:
        manager = EMRServerlessJobManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize EMR Serverless job manager: {exc}"
        ) from exc
    return config, manager


def _mask_secrets(text: str) -> str:
    """Mask potential AWS credentials and secrets in text.

    Delegates to :meth:`EMRServerlessJobManager._mask_secrets`.
    """
    return EMRServerlessJobManager._mask_secrets(text)


# ------------------------------------------------------------------
# Application Management
# ------------------------------------------------------------------


@tool
def list_applications(
    states: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """List EMR Serverless applications.

    Args:
        states: Optional list of application states to filter by.
            Valid values: CREATING, CREATED, STARTING, STARTED, STOPPING,
            STOPPED, TERMINATED.

    Returns:
        List of application dicts with keys: id, name, state, type,
        release_label, created_at, updated_at, architecture.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_app_manager()
    return manager.list_applications(states=states)


@tool
def get_application(application_id: str) -> Dict[str, Any]:
    """Get detailed information for a specific EMR Serverless application.

    Args:
        application_id: The EMR Serverless application ID.

    Returns:
        Application detail dict with keys: id, name, state, type,
        release_label, created_at, updated_at, architecture,
        state_details, auto_start_configuration,
        auto_stop_configuration, network_configuration.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_app_manager()
    return manager.get_application(application_id)


@tool
def start_application(application_id: str) -> Dict[str, Any]:
    """Request an EMR Serverless application to start.

    Pre-initializes the application so job submissions start faster.

    Args:
        application_id: The EMR Serverless application ID.

    Returns:
        Dict with keys: application_id, status ('start_requested').

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_app_manager()
    return manager.start_application(application_id)


@tool
def stop_application(application_id: str) -> Dict[str, Any]:
    """Request an EMR Serverless application to stop.

    Releases all resources associated with the application.

    Args:
        application_id: The EMR Serverless application ID.

    Returns:
        Dict with keys: application_id, status ('stop_requested').

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_app_manager()
    return manager.stop_application(application_id)


# ------------------------------------------------------------------
# Job Submission
# ------------------------------------------------------------------


@tool
def submit_spark_sql(
    sql: str,
    task_name: Optional[str] = None,
    application_id: Optional[str] = None,
    conf: Optional[Dict[str, Any]] = None,
    is_sync: bool = True,
    timeout: float = 300.0,
) -> Dict[str, Any]:
    """Submit a Spark SQL query to EMR Serverless.

    The SQL is executed via an embedded PySpark runner script that is
    automatically uploaded to S3. Results can be retrieved with
    :func:`get_job_result`.

    Args:
        sql: SQL query text.
        task_name: Optional job run name.
        application_id: Optional application ID override. Defaults to config.
        conf: Optional Spark configuration overrides.
        is_sync: If True, wait for the job to complete.
        timeout: Maximum wait time in seconds (only when is_sync=True).

    Returns:
        Job run info dict with keys: job_run_id, name, state, application_id, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager(application_id=application_id)
    return manager.submit_spark_sql(
        sql=sql,
        name=task_name,
        conf=conf,
        is_sync=is_sync,
        timeout=timeout,
    )


@tool
def submit_spark_jar(
    jar: str,
    main_class: str,
    main_args: Optional[List[str]] = None,
    task_name: Optional[str] = None,
    application_id: Optional[str] = None,
    conf: Optional[Dict[str, Any]] = None,
    is_sync: bool = True,
    timeout: float = 300.0,
) -> Dict[str, Any]:
    """Submit a Spark JAR job to EMR Serverless.

    Args:
        jar: S3 URI of the JAR file (e.g., ``s3://bucket/path/app.jar``).
        main_class: Fully qualified main class name.
        main_args: Optional list of application arguments.
        task_name: Optional job run name.
        application_id: Optional application ID override. Defaults to config.
        conf: Optional Spark configuration overrides.
        is_sync: If True, wait for the job to complete.
        timeout: Maximum wait time in seconds (only when is_sync=True).

    Returns:
        Job run info dict with keys: job_run_id, name, state, application_id, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager(application_id=application_id)
    return manager.submit_spark_jar(
        jar=jar,
        main_class=main_class,
        args=main_args,
        name=task_name,
        conf=conf,
        is_sync=is_sync,
        timeout=timeout,
    )


@tool
def submit_pyspark(
    script: str,
    args: Optional[List[str]] = None,
    task_name: Optional[str] = None,
    application_id: Optional[str] = None,
    conf: Optional[Dict[str, Any]] = None,
    is_sync: bool = True,
    timeout: float = 300.0,
) -> Dict[str, Any]:
    """Submit a PySpark script job to EMR Serverless.

    Args:
        script: S3 URI of the PySpark script (e.g., ``s3://bucket/scripts/job.py``).
        args: Optional list of script arguments.
        task_name: Optional job run name.
        application_id: Optional application ID override. Defaults to config.
        conf: Optional Spark configuration overrides.
        is_sync: If True, wait for the job to complete.
        timeout: Maximum wait time in seconds (only when is_sync=True).

    Returns:
        Job run info dict with keys: job_run_id, name, state, application_id, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager(application_id=application_id)
    return manager.submit_pyspark(
        script=script,
        args=args,
        name=task_name,
        conf=conf,
        is_sync=is_sync,
        timeout=timeout,
    )


@tool
def submit_hive_query(
    query: str,
    task_name: Optional[str] = None,
    application_id: Optional[str] = None,
    parameters: Optional[str] = None,
    is_sync: bool = True,
    timeout: float = 300.0,
) -> Dict[str, Any]:
    """Submit a Hive query job to EMR Serverless.

    Args:
        query: Hive SQL query text.
        task_name: Optional job run name.
        application_id: Optional application ID override. Defaults to config.
        parameters: Optional Hive parameters string.
        is_sync: If True, wait for the job to complete.
        timeout: Maximum wait time in seconds (only when is_sync=True).

    Returns:
        Job run info dict with keys: job_run_id, name, state, application_id, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager(application_id=application_id)
    return manager.submit_hive_query(
        query=query,
        name=task_name,
        parameters=parameters,
        is_sync=is_sync,
        timeout=timeout,
    )


# ------------------------------------------------------------------
# Job Lifecycle
# ------------------------------------------------------------------


@tool
def get_job_run(
    job_run_id: str,
    application_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Get detailed information for a specific job run.

    Args:
        job_run_id: The job run ID.
        application_id: Optional application ID override. Defaults to config.

    Returns:
        Job run detail dict with keys: job_run_id, name, application_id, arn,
        state, state_details, release_label, created_by, created_at, updated_at,
        started_at, ended_at, execution_role, total_execution_duration_seconds.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager()
    return manager.get_job_run(job_run_id, application_id)


@tool
def cancel_job_run(
    job_run_id: str,
    application_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Cancel a running job.

    Args:
        job_run_id: The job run ID to cancel.
        application_id: Optional application ID override. Defaults to config.

    Returns:
        Dict with keys: job_run_id, cancelled (bool).

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager()
    return manager.cancel_job_run(job_run_id, application_id)


@tool
def list_job_runs(
    application_id: Optional[str] = None,
    states: Optional[List[str]] = None,
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    """List job runs for an EMR Serverless application.

    Args:
        application_id: Optional application ID override. Defaults to config.
        states: Optional list of states to filter by
            (e.g., ``['RUNNING', 'SUCCESS']``).
        max_results: Maximum number of job runs to return.

    Returns:
        List of job run summary dicts with keys: job_run_id, name,
        application_id, arn, state, state_details, release_label,
        created_by, created_at, updated_at, type.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager()
    return manager.list_job_runs(application_id, states, max_results)


# ------------------------------------------------------------------
# Results
# ------------------------------------------------------------------


@tool
def get_job_result(
    job_run_id: str,
    application_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve SQL result JSON from S3 for a completed job run.

    Only available for jobs submitted via :func:`submit_spark_sql` that
    reached the SUCCESS state.

    Args:
        job_run_id: The job run ID.
        application_id: Optional application ID override. Defaults to config.

    Returns:
        Dict with keys: columns, rows, row_count. If the job is not in
        SUCCESS state, returns a dict with an error key instead.

    Raises:
        RuntimeError: If configuration is invalid or S3 access fails.
    """
    _, manager = _build_job_manager()
    return manager.get_job_result(job_run_id, application_id)


# ------------------------------------------------------------------
# Logs
# ------------------------------------------------------------------


@tool
def get_driver_log(
    job_run_id: str,
    application_id: Optional[str] = None,
    max_lines: int = 100,
    mask_secrets: bool = True,
) -> List[str]:
    """Retrieve driver stdout log for a job run.

    Reads the gzip-compressed ``SPARK_DRIVER/stdout.gz`` from S3.

    Args:
        job_run_id: The job run ID.
        application_id: Optional application ID override. Defaults to config.
        max_lines: Maximum number of log lines to return.
        mask_secrets: If True, mask potential AWS credentials in log output.

    Returns:
        List of log line strings.

    Raises:
        RuntimeError: If configuration is invalid or S3 access fails.
    """
    _, manager = _build_job_manager()
    raw_lines = manager.get_driver_log(job_run_id, application_id, max_lines)
    if mask_secrets:
        return [_mask_secrets(line) for line in raw_lines]
    return raw_lines


@tool
def get_stderr_log(
    job_run_id: str,
    application_id: Optional[str] = None,
    max_lines: int = 100,
    mask_secrets: bool = True,
) -> List[str]:
    """Retrieve driver stderr log for a job run.

    Reads the gzip-compressed ``SPARK_DRIVER/stderr.gz`` from S3.

    Args:
        job_run_id: The job run ID.
        application_id: Optional application ID override. Defaults to config.
        max_lines: Maximum number of log lines to return.
        mask_secrets: If True, mask potential AWS credentials in log output.

    Returns:
        List of log line strings.

    Raises:
        RuntimeError: If configuration is invalid or S3 access fails.
    """
    _, manager = _build_job_manager()
    raw_lines = manager.get_stderr_log(job_run_id, application_id, max_lines)
    if mask_secrets:
        return [_mask_secrets(line) for line in raw_lines]
    return raw_lines
