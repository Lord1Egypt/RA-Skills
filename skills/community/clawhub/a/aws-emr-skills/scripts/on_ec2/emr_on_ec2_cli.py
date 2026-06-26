from __future__ import annotations

"""AWS EMR On EC2 Skill tool interface.

Exposes 10 ``@tool``-decorated functions for agent integration, covering:

- Cluster management: ``list_emr_clusters``, ``describe_emr_cluster``,
  ``terminate_emr_clusters``;
- Step submission: ``add_spark_step``, ``add_pyspark_step``, ``add_hive_step``;
- Step lifecycle: ``list_emr_steps``, ``describe_emr_step``, ``cancel_emr_steps``;
- Logs: ``get_emr_step_log``.

All functions delegate to :class:`~scripts.on_ec2.clusters.EMRClusterManager`
and :class:`~scripts.on_ec2.steps.EMRStepManager`. Configuration is loaded
from environment variables via :func:`~scripts.config.emr_config.load_emr_skill_config`.
"""

from typing import Any, Dict, List, Optional, Tuple

from scripts.config.emr_config import (
    EMRSkillConfig,
    EMRSkillConfigError,
    load_emr_skill_config,
)
from scripts.on_ec2.clusters import EMRClusterManager
from scripts.on_ec2.steps import EMRStepManager


def tool(func):  # type: ignore[override]
    """Placeholder decorator for agent tool registration.

    In a real agent environment this is replaced by the framework's ``@tool``.
    """
    return func


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _build_cluster_manager() -> Tuple[EMRSkillConfig, EMRClusterManager]:
    """Load configuration and create a cluster manager.

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
        manager = EMRClusterManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to initialize EMR cluster manager: {exc}") from exc
    return config, manager


def _build_step_manager() -> Tuple[EMRSkillConfig, EMRStepManager]:
    """Load configuration and create a step manager.

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
        manager = EMRStepManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to initialize EMR step manager: {exc}") from exc
    return config, manager


def _mask_secrets(text: str) -> str:
    """Mask potential AWS credentials and secrets in text.

    Delegates to :meth:`EMRStepManager._mask_secrets`.
    """
    return EMRStepManager._mask_secrets(text)


# ------------------------------------------------------------------
# Cluster Management
# ------------------------------------------------------------------


@tool
def list_emr_clusters(
    states: Optional[List[str]] = None,
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    """List EMR clusters on EC2.

    Args:
        states: Optional list of cluster states to filter by.
            Valid values: STARTING, BOOTSTRAPPING, RUNNING, WAITING,
            TERMINATING, TERMINATED, TERMINATED_WITH_ERRORS.
        max_results: Maximum number of clusters to return.

    Returns:
        List of cluster dicts with keys: id, name, state, state_change_reason,
        created_at, ready_at, ended_at, normalized_instance_hours, cluster_arn.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.list_clusters(states=states, max_results=max_results)


@tool
def describe_emr_cluster(cluster_id: str) -> Dict[str, Any]:
    """Get detailed info for an EMR cluster.

    Args:
        cluster_id: The EMR cluster ID (e.g., ``j-XXXXXXXXXXXXX``).

    Returns:
        Cluster detail dict with keys: id, name, state, state_details,
        log_uri, release_label, applications, service_role,
        master_public_dns, ec2_instance_attributes, step_concurrency_level,
        auto_terminate, termination_protected, cluster_arn, tags.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.describe_cluster(cluster_id)


@tool
def terminate_emr_clusters(cluster_ids: List[str]) -> Dict[str, Any]:
    """Terminate EMR clusters.

    Args:
        cluster_ids: List of cluster IDs to terminate.

    Returns:
        Dict with keys: cluster_ids (list), status ('termination_requested').

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_cluster_manager()
    return manager.terminate_clusters(cluster_ids)


# ------------------------------------------------------------------
# Step Submission
# ------------------------------------------------------------------


@tool
def add_spark_step(
    cluster_id: str,
    entry_point: str,
    main_class: Optional[str] = None,
    args: Optional[List[str]] = None,
    name: Optional[str] = None,
    conf: Optional[Dict[str, str]] = None,
    deploy_mode: str = "cluster",
    action_on_failure: str = "CONTINUE",
) -> Dict[str, Any]:
    """Add a Spark submit step to an EMR cluster.

    Args:
        cluster_id: The EMR cluster ID.
        entry_point: S3 URI of the JAR or script to submit.
        main_class: Fully qualified main class (for JAR submissions).
        args: Optional list of application arguments.
        name: Optional step name.
        conf: Optional Spark configuration overrides.
        deploy_mode: Spark deploy mode (``cluster`` or ``client``).
        action_on_failure: Action when step fails.
            Valid values: TERMINATE_CLUSTER, CANCEL_AND_WAIT, CONTINUE.

    Returns:
        Dict with keys: step_id, cluster_id, name.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_step_manager()
    return manager.add_spark_submit_step(
        cluster_id,
        entry_point,
        name=name,
        deploy_mode=deploy_mode,
        main_class=main_class,
        args=args,
        conf=conf,
        action_on_failure=action_on_failure,
    )


@tool
def add_pyspark_step(
    cluster_id: str,
    script: str,
    args: Optional[List[str]] = None,
    name: Optional[str] = None,
    py_files: Optional[List[str]] = None,
    conf: Optional[Dict[str, str]] = None,
    action_on_failure: str = "CONTINUE",
) -> Dict[str, Any]:
    """Add a PySpark step to an EMR cluster.

    Args:
        cluster_id: The EMR cluster ID.
        script: S3 URI of the PySpark script.
        args: Optional list of script arguments.
        name: Optional step name.
        py_files: Optional list of additional Python files/archives.
        conf: Optional Spark configuration overrides.
        action_on_failure: Action when step fails.

    Returns:
        Dict with keys: step_id, cluster_id, name.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_step_manager()
    return manager.add_pyspark_step(
        cluster_id,
        script,
        name=name,
        args=args,
        py_files=py_files,
        conf=conf,
        action_on_failure=action_on_failure,
    )


@tool
def add_hive_step(
    cluster_id: str,
    script_s3_uri: Optional[str] = None,
    query: Optional[str] = None,
    name: Optional[str] = None,
    args: Optional[List[str]] = None,
    action_on_failure: str = "CONTINUE",
) -> Dict[str, Any]:
    """Add a Hive step to an EMR cluster.

    Either ``script_s3_uri`` or ``query`` must be provided. If ``query``
    is provided, it is uploaded to a temporary S3 path.

    Args:
        cluster_id: The EMR cluster ID.
        script_s3_uri: S3 URI of a Hive script file.
        query: Inline Hive query text.
        name: Optional step name.
        args: Optional additional Hive arguments.
        action_on_failure: Action when step fails.

    Returns:
        Dict with keys: step_id, cluster_id, name.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_step_manager()
    return manager.add_hive_step(
        cluster_id,
        script_s3_uri=script_s3_uri,
        query=query,
        name=name,
        args=args,
        action_on_failure=action_on_failure,
    )


# ------------------------------------------------------------------
# Step Lifecycle
# ------------------------------------------------------------------


@tool
def list_emr_steps(
    cluster_id: str,
    states: Optional[List[str]] = None,
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    """List steps for an EMR cluster.

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
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_step_manager()
    return manager.list_steps(cluster_id, states=states, max_results=max_results)


@tool
def describe_emr_step(
    cluster_id: str,
    step_id: str,
) -> Dict[str, Any]:
    """Get detailed info for an EMR step.

    Args:
        cluster_id: The EMR cluster ID.
        step_id: The step ID (e.g., ``s-XXXXXXXXXXXXX``).

    Returns:
        Step detail dict with keys: id, name, state, action_on_failure,
        jar, args, created_at, started_at, ended_at, failure_reason,
        failure_message, failure_log_file.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_step_manager()
    return manager.describe_step(cluster_id, step_id)


@tool
def cancel_emr_steps(
    cluster_id: str,
    step_ids: List[str],
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
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_step_manager()
    return manager.cancel_steps(cluster_id, step_ids, cancel_option=cancel_option)


# ------------------------------------------------------------------
# Logs
# ------------------------------------------------------------------


@tool
def get_emr_step_log(
    cluster_id: str,
    step_id: str,
    log_type: str = "stderr",
    max_lines: int = 200,
    mask_secrets: bool = True,
) -> List[str]:
    """Get step log from S3.

    Reads the gzip-compressed log file from the cluster's configured log URI.

    Args:
        cluster_id: The EMR cluster ID.
        step_id: The step ID.
        log_type: Log type to retrieve (e.g., ``stderr``, ``stdout``,
            ``controller``, ``syslog``).
        max_lines: Maximum number of log lines to return.
        mask_secrets: If True, mask potential AWS credentials in log output.

    Returns:
        List of log line strings.

    Raises:
        RuntimeError: If configuration is invalid or S3 access fails.
    """
    _, manager = _build_step_manager()
    raw_lines = manager.get_step_log(
        cluster_id, step_id, log_type=log_type, max_lines=max_lines
    )
    if mask_secrets:
        return [_mask_secrets(line) for line in raw_lines]
    return raw_lines
