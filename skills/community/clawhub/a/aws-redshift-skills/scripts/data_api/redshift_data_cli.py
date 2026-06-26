from __future__ import annotations

"""AWS Redshift Data API Skill tool interface.

Exposes 12 ``@tool``-decorated functions for agent integration, covering:

- Query execution: ``execute_sql``, ``batch_execute_sql``;
- Results: ``get_statement_result``, ``describe_statement``, ``list_statements``;
- Lifecycle: ``cancel_statement``;
- Metadata: ``list_databases``, ``list_schemas``, ``list_tables``, ``describe_table``;
- Data movement: ``execute_copy``, ``execute_unload``.

All functions delegate to :class:`~scripts.data_api.queries.RedshiftQueryManager`.
Works with both Redshift Provisioned and Serverless modes.
"""

from typing import Any, Dict, List, Optional, Tuple

from scripts.config.redshift_config import (
    RedshiftSkillConfig,
    RedshiftSkillConfigError,
    load_redshift_skill_config,
)
from scripts.data_api.queries import RedshiftQueryManager


def tool(func):  # type: ignore[override]
    """Placeholder decorator for agent tool registration."""
    return func


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _build_query_manager() -> Tuple[RedshiftSkillConfig, RedshiftQueryManager]:
    """Load configuration and create a query manager."""
    try:
        config = load_redshift_skill_config()
    except RedshiftSkillConfigError as exc:
        raise RuntimeError(f"Redshift Skill configuration error: {exc}") from exc
    try:
        manager = RedshiftQueryManager(config)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Failed to initialize Redshift query manager: {exc}"
        ) from exc
    return config, manager


def _mask_secrets(text: str) -> str:
    """Mask potential AWS credentials and secrets in text."""
    from scripts.data_api.queries import _mask_secrets as _m

    return _m(text)


# ------------------------------------------------------------------
# Query Execution
# ------------------------------------------------------------------


@tool
def execute_sql(
    sql: str,
    statement_name: Optional[str] = None,
    is_sync: bool = False,
    timeout: float = 300.0,
) -> Dict[str, Any]:
    """Execute a SQL statement via the Redshift Data API.

    Args:
        sql: SQL statement to execute.
        statement_name: Optional name for the statement.
        is_sync: If True, wait for the query to complete before returning.
        timeout: Maximum wait time in seconds (only when is_sync=True).

    Returns:
        Statement info dict with keys: id, status, and (if sync)
        result_rows, duration, error, etc.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.execute_sql(
        sql=sql,
        statement_name=statement_name,
        is_sync=is_sync,
        timeout=timeout,
    )


@tool
def batch_execute_sql(
    sqls: List[str],
    statement_name: Optional[str] = None,
    is_sync: bool = False,
    timeout: float = 600.0,
) -> Dict[str, Any]:
    """Execute multiple SQL statements as a batch.

    Args:
        sqls: List of SQL statements.
        statement_name: Optional name for the batch.
        is_sync: If True, wait for the batch to complete.
        timeout: Maximum wait time in seconds.

    Returns:
        Statement info dict.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.batch_execute_sql(
        sqls=sqls,
        statement_name=statement_name,
        is_sync=is_sync,
        timeout=timeout,
    )


@tool
def get_statement_result(
    statement_id: str,
    next_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the results of a completed SQL statement.

    Args:
        statement_id: Statement ID.
        next_token: Pagination token for large result sets.

    Returns:
        Dict with columns, rows, total_rows, and next_token.

    Raises:
        RuntimeError: If the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.get_statement_result(
        statement_id=statement_id,
        next_token=next_token,
    )


@tool
def describe_statement(statement_id: str) -> Dict[str, Any]:
    """Check the status of a SQL statement.

    Args:
        statement_id: Statement ID.

    Returns:
        Statement detail dict with keys: id, status, query_string,
        result_rows, duration, error, etc.

    Raises:
        RuntimeError: If the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.describe_statement(statement_id=statement_id)


@tool
def list_statements(
    status: Optional[str] = None,
    max_results: int = 100,
    next_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List recent SQL statements.

    Args:
        status: Optional status filter ('SUBMITTED', 'PICKED', 'STARTED',
            'FINISHED', 'ABORTED', 'FAILED').
        max_results: Maximum number of results.
        next_token: Pagination token.

    Returns:
        Dict with statements list and pagination token.

    Raises:
        RuntimeError: If the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.list_statements(
        status=status,
        max_results=max_results,
        next_token=next_token,
    )


@tool
def cancel_statement(statement_id: str) -> Dict[str, Any]:
    """Cancel a running SQL statement.

    Args:
        statement_id: Statement ID to cancel.

    Returns:
        Dict with cancellation status.

    Raises:
        RuntimeError: If the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.cancel_statement(statement_id=statement_id)


# ------------------------------------------------------------------
# Metadata
# ------------------------------------------------------------------


@tool
def list_databases() -> List[str]:
    """List all databases in the Redshift cluster/workgroup.

    Returns:
        List of database names.

    Raises:
        RuntimeError: If configuration is invalid or the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.list_databases()


@tool
def list_schemas(
    database: Optional[str] = None,
    schema_pattern: Optional[str] = None,
) -> List[str]:
    """List schemas in a database.

    Args:
        database: Database name. Defaults to configured database.
        schema_pattern: LIKE pattern to filter schemas (e.g., 'public%').

    Returns:
        List of schema names.

    Raises:
        RuntimeError: If the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.list_schemas(database=database, schema_pattern=schema_pattern)


@tool
def list_tables(
    database: Optional[str] = None,
    schema_pattern: Optional[str] = None,
    table_pattern: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List tables in a schema.

    Args:
        database: Database name. Defaults to configured database.
        schema_pattern: LIKE pattern to filter schemas.
        table_pattern: LIKE pattern to filter tables.

    Returns:
        List of table dicts with name, schema, type.

    Raises:
        RuntimeError: If the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.list_tables(
        database=database,
        schema_pattern=schema_pattern,
        table_pattern=table_pattern,
    )


@tool
def describe_table(
    table: str,
    database: Optional[str] = None,
    schema: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Get column metadata for a table.

    Args:
        table: Table name.
        database: Database name. Defaults to configured database.
        schema: Schema name.

    Returns:
        List of column dicts with name, type_name, length, nullable, etc.

    Raises:
        RuntimeError: If the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.describe_table(table=table, database=database, schema=schema)


# ------------------------------------------------------------------
# Data Movement
# ------------------------------------------------------------------


@tool
def execute_copy(
    table: str,
    s3_path: str,
    iam_role_arn: Optional[str] = None,
    data_format: str = "CSV",
    options: Optional[str] = None,
    is_sync: bool = True,
    timeout: float = 600.0,
) -> Dict[str, Any]:
    """Generate and execute a COPY command to load data from S3.

    Args:
        table: Target table name.
        s3_path: S3 path (e.g., 's3://bucket/prefix/').
        iam_role_arn: IAM role ARN. Defaults to REDSHIFT_IAM_ROLE_ARN env var.
        data_format: Data format (CSV, JSON, PARQUET, AVRO, ORC).
        options: Additional COPY options (e.g., 'IGNOREHEADER 1 DELIMITER ","').
        is_sync: If True, wait for completion.
        timeout: Maximum wait time in seconds.

    Returns:
        Statement info dict.

    Raises:
        RuntimeError: If IAM role is not configured or the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.execute_copy(
        table=table,
        s3_path=s3_path,
        iam_role_arn=iam_role_arn,
        data_format=data_format,
        options=options,
        is_sync=is_sync,
        timeout=timeout,
    )


@tool
def execute_unload(
    query: str,
    s3_path: str,
    iam_role_arn: Optional[str] = None,
    data_format: str = "CSV",
    options: Optional[str] = None,
    is_sync: bool = True,
    timeout: float = 600.0,
) -> Dict[str, Any]:
    """Generate and execute an UNLOAD command to export data to S3.

    Args:
        query: SELECT query to unload.
        s3_path: S3 destination path.
        iam_role_arn: IAM role ARN. Defaults to REDSHIFT_IAM_ROLE_ARN env var.
        data_format: Output format (CSV, JSON, PARQUET).
        options: Additional UNLOAD options (e.g., 'HEADER PARALLEL ON').
        is_sync: If True, wait for completion.
        timeout: Maximum wait time in seconds.

    Returns:
        Statement info dict.

    Raises:
        RuntimeError: If IAM role is not configured or the API call fails.
    """
    _, manager = _build_query_manager()
    return manager.execute_unload(
        query=query,
        s3_path=s3_path,
        iam_role_arn=iam_role_arn,
        data_format=data_format,
        options=options,
        is_sync=is_sync,
        timeout=timeout,
    )
