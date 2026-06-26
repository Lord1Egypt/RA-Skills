from __future__ import annotations

"""Redshift Data API query execution and metadata management.

Provides :class:`RedshiftQueryManager` for executing SQL queries and retrieving
metadata via the ``redshift-data`` boto3 client. Works with both Redshift
Provisioned and Serverless modes.
"""

import re
import time
from typing import Any, Dict, List, Optional

from botocore.exceptions import ClientError

from scripts.client.boto_client import get_redshift_data_client
from scripts.config.redshift_config import RedshiftSkillConfig


def _mask_secrets(text: str) -> str:
    """Mask potential AWS credentials and secrets in text."""
    text = re.sub(r"(AKIA[0-9A-Z]{16})", "AKIA****MASKED", text)
    text = re.sub(
        r"(?i)(secret[_-]?access[_-]?key\s*[:=]\s*)[^\s,\"']+",
        r"\1****MASKED",
        text,
    )
    text = re.sub(
        r"(?i)(password\s*[:=]\s*)[^\s,\"']+",
        r"\1****MASKED",
        text,
    )
    return text


def _clean_statement(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a boto3 Statement response dict to snake_case."""
    return {
        "id": raw.get("Id"),
        "status": raw.get("Status"),
        "query_string": raw.get("QueryString"),
        "result_rows": raw.get("ResultRows"),
        "result_size": raw.get("ResultSize"),
        "redshift_pid": raw.get("RedshiftPid"),
        "redshift_query_id": raw.get("RedshiftQueryId"),
        "database": raw.get("Database"),
        "db_user": raw.get("DbUser"),
        "cluster_identifier": raw.get("ClusterIdentifier"),
        "workgroup_name": raw.get("WorkgroupName"),
        "secret_arn": raw.get("SecretArn"),
        "created_at": str(raw.get("CreatedAt", "")),
        "updated_at": str(raw.get("UpdatedAt", "")),
        "duration": raw.get("Duration"),
        "error": raw.get("Error"),
        "has_result_set": raw.get("HasResultSet"),
    }


def _clean_statement_summary(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a statement list item to snake_case."""
    return {
        "id": raw.get("Id"),
        "status": raw.get("Status"),
        "query_string": raw.get("QueryString"),
        "created_at": str(raw.get("CreatedAt", "")),
        "updated_at": str(raw.get("UpdatedAt", "")),
        "statement_name": raw.get("StatementName"),
    }


class RedshiftQueryManager:
    """Manages Redshift Data API operations.

    Supports both Provisioned (cluster-identifier + db-user) and
    Serverless (workgroup-name + optional secret-arn) authentication.

    Attributes:
        config: Redshift skill configuration.
        client: boto3 Redshift Data API client.
    """

    def __init__(self, config: RedshiftSkillConfig) -> None:
        self.config = config
        self.client = get_redshift_data_client(config.region)

    @classmethod
    def from_env(cls) -> "RedshiftQueryManager":
        """Create a manager from environment configuration."""
        from scripts.config.redshift_config import load_redshift_skill_config

        return cls(load_redshift_skill_config())

    def _build_auth_params(self) -> Dict[str, Any]:
        """Build authentication parameters for Data API calls.

        Uses workgroup-name if configured, otherwise cluster-identifier + db-user.

        Returns:
            Dict with authentication parameters.
        """
        params: Dict[str, Any] = {"Database": self.config.database}

        if self.config.workgroup_name:
            params["WorkgroupName"] = self.config.workgroup_name
            if self.config.secret_arn:
                params["SecretArn"] = self.config.secret_arn
        elif self.config.cluster_id:
            params["ClusterIdentifier"] = self.config.cluster_id
            if self.config.secret_arn:
                params["SecretArn"] = self.config.secret_arn
            elif self.config.db_user:
                params["DbUser"] = self.config.db_user
        else:
            raise RuntimeError(
                "Either REDSHIFT_WORKGROUP_NAME or REDSHIFT_CLUSTER_ID must be set "
                "for Data API operations."
            )

        return params

    def execute_sql(
        self,
        sql: str,
        statement_name: Optional[str] = None,
        is_sync: bool = False,
        timeout: float = 300.0,
        poll_interval: float = 1.0,
    ) -> Dict[str, Any]:
        """Execute a SQL statement via the Redshift Data API.

        Args:
            sql: SQL statement to execute.
            statement_name: Optional name for the statement.
            is_sync: If True, poll until completion.
            timeout: Maximum wait time in seconds (only when is_sync=True).
            poll_interval: Seconds between status polls (only when is_sync=True).

        Returns:
            Statement info dict.
        """
        try:
            params = self._build_auth_params()
            params["Sql"] = sql
            if statement_name:
                params["StatementName"] = statement_name

            resp = self.client.execute_statement(**params)
            statement_id = resp.get("Id", "")

            if not is_sync:
                return {"id": statement_id, "status": "SUBMITTED"}

            return self._wait_for_statement(statement_id, timeout, poll_interval)
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def batch_execute_sql(
        self,
        sqls: List[str],
        statement_name: Optional[str] = None,
        is_sync: bool = False,
        timeout: float = 600.0,
        poll_interval: float = 2.0,
    ) -> Dict[str, Any]:
        """Execute multiple SQL statements as a batch.

        Args:
            sqls: List of SQL statements.
            statement_name: Optional name for the batch.
            is_sync: If True, poll until completion.
            timeout: Maximum wait time in seconds.
            poll_interval: Seconds between status polls.

        Returns:
            Statement info dict.
        """
        try:
            params = self._build_auth_params()
            params["Sqls"] = sqls
            if statement_name:
                params["StatementName"] = statement_name

            resp = self.client.batch_execute_statement(**params)
            statement_id = resp.get("Id", "")

            if not is_sync:
                return {"id": statement_id, "status": "SUBMITTED"}

            return self._wait_for_statement(statement_id, timeout, poll_interval)
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def _wait_for_statement(
        self, statement_id: str, timeout: float, poll_interval: float
    ) -> Dict[str, Any]:
        """Poll statement status until completion or timeout.

        Args:
            statement_id: Statement ID to poll.
            timeout: Maximum wait time in seconds.
            poll_interval: Seconds between polls.

        Returns:
            Statement info dict.
        """
        start = time.time()
        while time.time() - start < timeout:
            result = self.describe_statement(statement_id)
            status = result.get("status", "")
            if status in ("FINISHED", "FAILED", "ABORTED"):
                return result
            time.sleep(poll_interval)

        return {
            "id": statement_id,
            "status": "TIMEOUT",
            "error": f"Statement did not complete within {timeout}s",
        }

    def describe_statement(self, statement_id: str) -> Dict[str, Any]:
        """Check the status of a SQL statement.

        Args:
            statement_id: Statement ID.

        Returns:
            Cleaned statement info dict.
        """
        try:
            resp = self.client.describe_statement(Id=statement_id)
            return _clean_statement(resp)
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def get_statement_result(
        self, statement_id: str, next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the results of a completed SQL statement.

        Args:
            statement_id: Statement ID.
            next_token: Pagination token for large result sets.

        Returns:
            Dict with columns and rows.
        """
        try:
            kwargs: Dict[str, Any] = {"Id": statement_id}
            if next_token:
                kwargs["NextToken"] = next_token

            resp = self.client.get_statement_result(**kwargs)
            columns = [
                {
                    "name": col.get("name"),
                    "type_name": col.get("typeName"),
                    "label": col.get("label"),
                }
                for col in resp.get("ColumnMetadata", [])
            ]

            rows = []
            for record in resp.get("Records", []):
                row = []
                for field in record:
                    if "stringValue" in field:
                        row.append(field["stringValue"])
                    elif "longValue" in field:
                        row.append(field["longValue"])
                    elif "doubleValue" in field:
                        row.append(field["doubleValue"])
                    elif "booleanValue" in field:
                        row.append(field["booleanValue"])
                    elif "isNull" in field and field["isNull"]:
                        row.append(None)
                    else:
                        row.append(str(field))
                rows.append(row)

            return {
                "columns": columns,
                "rows": rows,
                "total_rows": resp.get("TotalNumRows", len(rows)),
                "next_token": resp.get("NextToken"),
            }
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def list_statements(
        self,
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
        """
        try:
            kwargs: Dict[str, Any] = {"MaxResults": max_results}
            if status:
                kwargs["Status"] = status
            if next_token:
                kwargs["NextToken"] = next_token

            resp = self.client.list_statements(**kwargs)
            statements = [
                _clean_statement_summary(s) for s in resp.get("Statements", [])
            ]
            return {
                "statements": statements,
                "next_token": resp.get("NextToken"),
            }
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def cancel_statement(self, statement_id: str) -> Dict[str, Any]:
        """Cancel a running SQL statement.

        Args:
            statement_id: Statement ID to cancel.

        Returns:
            Dict with cancellation status.
        """
        try:
            resp = self.client.cancel_statement(Id=statement_id)
            return {
                "id": statement_id,
                "status": "cancel_requested",
                "cancelled": resp.get("Status", True),
            }
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def list_databases(self) -> List[str]:
        """List all databases.

        Returns:
            List of database names.
        """
        try:
            params = self._build_auth_params()
            databases: List[str] = []
            next_token: Optional[str] = None

            while True:
                kwargs = {**params}
                if next_token:
                    kwargs["NextToken"] = next_token

                resp = self.client.list_databases(**kwargs)
                databases.extend(resp.get("Databases", []))

                next_token = resp.get("NextToken")
                if not next_token:
                    break

            return databases
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def list_schemas(
        self, database: Optional[str] = None, schema_pattern: Optional[str] = None
    ) -> List[str]:
        """List schemas in a database.

        Args:
            database: Database name. Defaults to config database.
            schema_pattern: LIKE pattern to filter schemas.

        Returns:
            List of schema names.
        """
        try:
            params = self._build_auth_params()
            if database:
                params["Database"] = database

            if schema_pattern:
                params["SchemaPattern"] = schema_pattern

            schemas: List[str] = []
            next_token: Optional[str] = None

            while True:
                kwargs = {**params}
                if next_token:
                    kwargs["NextToken"] = next_token

                resp = self.client.list_schemas(**kwargs)
                schemas.extend(resp.get("Schemas", []))

                next_token = resp.get("NextToken")
                if not next_token:
                    break

            return schemas
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def list_tables(
        self,
        database: Optional[str] = None,
        schema_pattern: Optional[str] = None,
        table_pattern: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List tables in a schema.

        Args:
            database: Database name. Defaults to config database.
            schema_pattern: LIKE pattern to filter schemas.
            table_pattern: LIKE pattern to filter tables.

        Returns:
            List of table dicts.
        """
        try:
            params = self._build_auth_params()
            if database:
                params["Database"] = database
            if schema_pattern:
                params["SchemaPattern"] = schema_pattern
            if table_pattern:
                params["TablePattern"] = table_pattern

            tables: List[Dict[str, Any]] = []
            next_token: Optional[str] = None

            while True:
                kwargs = {**params}
                if next_token:
                    kwargs["NextToken"] = next_token

                resp = self.client.list_tables(**kwargs)
                for t in resp.get("Tables", []):
                    tables.append(
                        {
                            "name": t.get("name"),
                            "schema": t.get("schema"),
                            "type": t.get("type"),
                        }
                    )

                next_token = resp.get("NextToken")
                if not next_token:
                    break

            return tables
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def describe_table(
        self,
        table: str,
        database: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get column metadata for a table.

        Args:
            table: Table name.
            database: Database name. Defaults to config database.
            schema: Schema name.

        Returns:
            List of column dicts with name, type, etc.
        """
        try:
            params = self._build_auth_params()
            params["Table"] = table
            if database:
                params["Database"] = database
            if schema:
                params["Schema"] = schema

            columns: List[Dict[str, Any]] = []
            next_token: Optional[str] = None

            while True:
                kwargs = {**params}
                if next_token:
                    kwargs["NextToken"] = next_token

                resp = self.client.describe_table(**kwargs)
                for col in resp.get("ColumnList", []):
                    columns.append(
                        {
                            "name": col.get("name"),
                            "type_name": col.get("typeName"),
                            "length": col.get("length"),
                            "precision": col.get("precision"),
                            "scale": col.get("scale"),
                            "nullable": col.get("nullable"),
                            "schema_name": col.get("schemaName"),
                            "table_name": col.get("tableName"),
                        }
                    )

                next_token = resp.get("NextToken")
                if not next_token:
                    break

            return columns
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            msg = exc.response["Error"]["Message"]
            raise RuntimeError(f"[{code}] {_mask_secrets(msg)}") from exc

    def execute_copy(
        self,
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
            iam_role_arn: IAM role ARN. Defaults to config iam_role_arn.
            data_format: Data format (CSV, JSON, PARQUET, AVRO, ORC, etc.).
            options: Additional COPY options (e.g., 'IGNOREHEADER 1 DELIMITER ","').
            is_sync: If True, poll until completion.
            timeout: Maximum wait time in seconds.

        Returns:
            Statement info dict.
        """
        role = iam_role_arn or self.config.iam_role_arn
        if not role:
            raise RuntimeError(
                "IAM role ARN required for COPY. Set REDSHIFT_IAM_ROLE_ARN or pass iam_role_arn."
            )

        sql = f"COPY {table} FROM '{s3_path}' IAM_ROLE '{role}' FORMAT AS {data_format}"
        if options:
            sql += f" {options}"
        sql += ";"

        return self.execute_sql(
            sql=sql,
            statement_name=f"copy-{table}",
            is_sync=is_sync,
            timeout=timeout,
        )

    def execute_unload(
        self,
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
            iam_role_arn: IAM role ARN. Defaults to config iam_role_arn.
            data_format: Output format (CSV, JSON, PARQUET).
            options: Additional UNLOAD options (e.g., 'HEADER PARALLEL ON').
            is_sync: If True, poll until completion.
            timeout: Maximum wait time in seconds.

        Returns:
            Statement info dict.
        """
        role = iam_role_arn or self.config.iam_role_arn
        if not role:
            raise RuntimeError(
                "IAM role ARN required for UNLOAD. Set REDSHIFT_IAM_ROLE_ARN or pass iam_role_arn."
            )

        escaped_query = query.replace("'", "''")
        sql = f"UNLOAD ('{escaped_query}') TO '{s3_path}' IAM_ROLE '{role}' FORMAT AS {data_format}"
        if options:
            sql += f" {options}"
        sql += ";"

        return self.execute_sql(
            sql=sql,
            statement_name="unload-query",
            is_sync=is_sync,
            timeout=timeout,
        )
