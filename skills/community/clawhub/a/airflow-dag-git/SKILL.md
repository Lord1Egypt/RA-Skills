# airflow-dag-git

## Purpose

Operate Airflow DAG files through GitHub PR workflow only.

## Available tools

- `airflow_dag_git_read_file`
- `airflow_dag_git_open_pr`

## Guardrails

- Use allowlisted `owner`, `repo`, and DAG paths only.
- Target must be a single `.py` file.
- No path traversal, absolute paths, delete, rename, or multi-file operations.
- No CI workflow changes.
- `open_pr` requires DAG-like content (`DAG(` or `@dag`) and rejects dangerous patterns.

## Expected workflow

1. Read existing DAG with `airflow_dag_git_read_file`.
2. Prepare updated DAG content.
3. Submit update through `airflow_dag_git_open_pr`.
4. Human reviews PR and decides merge.

## Rollback

- Close PR if not merged.
- Delete created branch.
- Revert merge commit if already merged.