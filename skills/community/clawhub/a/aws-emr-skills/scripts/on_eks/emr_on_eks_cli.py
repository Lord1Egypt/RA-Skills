from __future__ import annotations

"""AWS EMR on EKS Skill tool interface.

Exposes 10 ``@tool``-decorated functions for agent integration, covering:

- Virtual cluster management: ``list_eks_virtual_clusters``,
  ``describe_eks_virtual_cluster``, ``create_eks_virtual_cluster``,
  ``delete_eks_virtual_cluster``;
- Job submission: ``submit_eks_spark_job``, ``submit_eks_spark_sql``;
- Job lifecycle: ``describe_eks_job_run``, ``list_eks_job_runs``,
  ``cancel_eks_job_run``;
- Logs: ``get_eks_job_log``.

All functions delegate to :class:`~scripts.on_eks.virtual_clusters.EMRVirtualClusterManager`
and :class:`~scripts.on_eks.job_runs.EMRContainersJobRunManager`. Configuration is loaded
from environment variables via :func:`~scripts.config.emr_config.load_emr_skill_config`.
"""

from typing import Any, Dict, List, Optional, Tuple

from scripts.config.emr_config import (
    EMRSkillConfig,
    EMRSkillConfigError,
    load_emr_skill_config,
)
from scripts.on_eks.job_runs import EMRContainersJobRunManager
from scripts.on_eks.virtual_clusters import EMRVirtualClusterManager


def tool(func):  # type: ignore[override]
    """Placeholder decorator for agent tool registration.

    In a real agent environment this is replaced by the framework's ``@tool``.
    """
    return func


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _build_vc_manager() -> Tuple[EMRSkillConfig, EMRVirtualClusterManager]:
    """Load configuration and create a virtual cluster manager.

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
        manager = EMRVirtualClusterManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize EMR virtual cluster manager: {exc}"
        ) from exc
    return config, manager


def _build_job_manager(
    virtual_cluster_id: Optional[str] = None,
) -> Tuple[EMRSkillConfig, EMRContainersJobRunManager]:
    """Load configuration and create a job run manager.

    Args:
        virtual_cluster_id: Optional virtual cluster ID override. When provided,
            replaces the config's virtual_cluster_id before manager creation.

    Returns:
        Tuple of (config, manager).

    Raises:
        RuntimeError: If configuration loading or client creation fails.
    """
    try:
        config = load_emr_skill_config()
    except EMRSkillConfigError as exc:
        raise RuntimeError(f"EMR Skill configuration error: {exc}") from exc

    if virtual_cluster_id:
        config.virtual_cluster_id = virtual_cluster_id

    try:
        manager = EMRContainersJobRunManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize EMR Containers job run manager: {exc}"
        ) from exc
    return config, manager


def _mask_secrets(text: str) -> str:
    """Mask potential AWS credentials and secrets in text.

    Delegates to :meth:`EMRContainersJobRunManager._mask_secrets`.
    """
    return EMRContainersJobRunManager._mask_secrets(text)


# ------------------------------------------------------------------
# Virtual Cluster Management
# ------------------------------------------------------------------


@tool
def list_eks_virtual_clusters(
    states: Optional[List[str]] = None,
    container_provider_id: Optional[str] = None,
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    """List EMR on EKS virtual clusters.

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
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_vc_manager()
    return manager.list_virtual_clusters(
        states=states,
        container_provider_id=container_provider_id,
        max_results=max_results,
    )


@tool
def describe_eks_virtual_cluster(
    virtual_cluster_id: str,
) -> Dict[str, Any]:
    """Get detailed info for an EMR on EKS virtual cluster.

    Args:
        virtual_cluster_id: The virtual cluster ID.

    Returns:
        Virtual cluster detail dict with keys: id, name, arn, state,
        container_provider_type, container_provider_id, namespace,
        created_at, tags.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_vc_manager()
    return manager.describe_virtual_cluster(virtual_cluster_id)


@tool
def create_eks_virtual_cluster(
    name: str,
    eks_cluster_id: str,
    namespace: str,
    tags: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Create an EMR on EKS virtual cluster.

    Links an EKS cluster namespace to EMR for running containerized Spark jobs.

    Args:
        name: Name for the virtual cluster.
        eks_cluster_id: The EKS cluster ID to associate with.
        namespace: The Kubernetes namespace on the EKS cluster.
        tags: Optional tags to attach to the virtual cluster.

    Returns:
        Dict with keys: id, name, arn.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_vc_manager()
    return manager.create_virtual_cluster(
        name=name,
        eks_cluster_id=eks_cluster_id,
        namespace=namespace,
        tags=tags,
    )


@tool
def delete_eks_virtual_cluster(
    virtual_cluster_id: str,
) -> Dict[str, Any]:
    """Delete an EMR on EKS virtual cluster.

    Args:
        virtual_cluster_id: The virtual cluster ID to delete.

    Returns:
        Dict with keys: id, status ('delete_requested').

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_vc_manager()
    return manager.delete_virtual_cluster(virtual_cluster_id)


# ------------------------------------------------------------------
# Job Submission
# ------------------------------------------------------------------


@tool
def submit_eks_spark_job(
    entry_point: str,
    virtual_cluster_id: Optional[str] = None,
    name: Optional[str] = None,
    execution_role_arn: Optional[str] = None,
    release_label: str = "emr-7.1.0-latest",
    entry_point_args: Optional[List[str]] = None,
    spark_submit_params: Optional[str] = None,
    conf: Optional[Dict[str, str]] = None,
    s3_log_uri: Optional[str] = None,
    is_sync: bool = False,
    timeout: float = 600,
) -> Dict[str, Any]:
    """Submit a Spark job to EMR on EKS.

    Args:
        entry_point: S3 URI of the Spark script or JAR entry point.
        virtual_cluster_id: Optional virtual cluster ID. Falls back to config.
        name: Optional job run name.
        execution_role_arn: IAM execution role ARN. Falls back to config.
        release_label: EMR release label (default: ``emr-7.1.0-latest``).
        entry_point_args: Optional list of entry point arguments.
        spark_submit_params: Optional spark-submit parameters string.
        conf: Optional Spark configuration overrides.
        s3_log_uri: Optional S3 URI for log output. Falls back to config.
        is_sync: If True, wait for the job to complete.
        timeout: Maximum wait time in seconds (only when is_sync=True).

    Returns:
        Job run info dict with keys: id, name, arn, virtual_cluster_id,
        state, state_details, created_at, finished_at, execution_role_arn,
        release_label.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager(virtual_cluster_id=virtual_cluster_id)
    return manager.submit_spark_job(
        virtual_cluster_id=virtual_cluster_id,
        entry_point=entry_point,
        name=name,
        execution_role_arn=execution_role_arn,
        release_label=release_label,
        entry_point_args=entry_point_args,
        spark_submit_params=spark_submit_params,
        conf=conf,
        s3_log_uri=s3_log_uri,
        is_sync=is_sync,
        timeout=timeout,
    )


@tool
def submit_eks_spark_sql(
    sql_entry_point: str,
    virtual_cluster_id: Optional[str] = None,
    name: Optional[str] = None,
    execution_role_arn: Optional[str] = None,
    release_label: str = "emr-7.1.0-latest",
    spark_sql_params: Optional[str] = None,
    s3_log_uri: Optional[str] = None,
    is_sync: bool = False,
    timeout: float = 600,
) -> Dict[str, Any]:
    """Submit a Spark SQL job to EMR on EKS.

    Args:
        sql_entry_point: S3 URI of the SQL script file.
        virtual_cluster_id: Optional virtual cluster ID. Falls back to config.
        name: Optional job run name.
        execution_role_arn: IAM execution role ARN. Falls back to config.
        release_label: EMR release label (default: ``emr-7.1.0-latest``).
        spark_sql_params: Optional Spark SQL parameters string.
        s3_log_uri: Optional S3 URI for log output. Falls back to config.
        is_sync: If True, wait for the job to complete.
        timeout: Maximum wait time in seconds (only when is_sync=True).

    Returns:
        Job run info dict with keys: id, name, arn, virtual_cluster_id,
        state, state_details, created_at, finished_at, execution_role_arn,
        release_label.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager(virtual_cluster_id=virtual_cluster_id)
    return manager.submit_spark_sql(
        virtual_cluster_id=virtual_cluster_id,
        sql_entry_point=sql_entry_point,
        name=name,
        execution_role_arn=execution_role_arn,
        release_label=release_label,
        spark_sql_params=spark_sql_params,
        s3_log_uri=s3_log_uri,
        is_sync=is_sync,
        timeout=timeout,
    )


# ------------------------------------------------------------------
# Job Lifecycle
# ------------------------------------------------------------------


@tool
def describe_eks_job_run(
    job_run_id: str,
    virtual_cluster_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Get detailed info for an EMR on EKS job run.

    Args:
        job_run_id: The job run ID.
        virtual_cluster_id: Optional virtual cluster ID. Falls back to config.

    Returns:
        Job run detail dict with keys: id, name, arn, virtual_cluster_id,
        state, state_details, created_at, finished_at, execution_role_arn,
        release_label.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager()
    return manager.describe_job_run(job_run_id, virtual_cluster_id)


@tool
def list_eks_job_runs(
    virtual_cluster_id: Optional[str] = None,
    states: Optional[List[str]] = None,
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    """List job runs for an EMR on EKS virtual cluster.

    Args:
        virtual_cluster_id: Optional virtual cluster ID. Falls back to config.
        states: Optional list of states to filter by.
            Valid values: PENDING, SUBMITTED, RUNNING, COMPLETED, FAILED,
            CANCELLED, CANCEL_PENDING.
        max_results: Maximum number of job runs to return.

    Returns:
        List of job run summary dicts with snake_case keys.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager()
    return manager.list_job_runs(
        virtual_cluster_id=virtual_cluster_id,
        states=states,
        max_results=max_results,
    )


@tool
def cancel_eks_job_run(
    job_run_id: str,
    virtual_cluster_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Cancel an EMR on EKS job run.

    Args:
        job_run_id: The job run ID to cancel.
        virtual_cluster_id: Optional virtual cluster ID. Falls back to config.

    Returns:
        Dict with keys: id, virtual_cluster_id, status ('cancel_requested').

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_job_manager()
    return manager.cancel_job_run(job_run_id, virtual_cluster_id)


# ------------------------------------------------------------------
# Logs
# ------------------------------------------------------------------


@tool
def get_eks_job_log(
    job_run_id: str,
    virtual_cluster_id: Optional[str] = None,
    log_type: str = "stderr",
    max_lines: int = 200,
    mask_secrets: bool = True,
) -> List[str]:
    """Get job run log from S3 for EMR on EKS.

    Retrieves the gzip-compressed driver log from S3. The exact log path
    is auto-discovered via S3 listing since container names are unpredictable.

    Args:
        job_run_id: The job run ID.
        virtual_cluster_id: Optional virtual cluster ID. Falls back to config.
        log_type: Type of log to retrieve (``stderr`` or ``stdout``).
        max_lines: Maximum number of log lines to return.
        mask_secrets: If True, mask potential AWS credentials in log output.

    Returns:
        List of log line strings.

    Raises:
        RuntimeError: If configuration is invalid or S3 access fails.
    """
    _, manager = _build_job_manager()
    raw_lines = manager.get_job_log(
        job_run_id,
        virtual_cluster_id,
        log_type=log_type,
        max_lines=max_lines,
    )
    if mask_secrets:
        return [_mask_secrets(line) for line in raw_lines]
    return raw_lines
