# Actions

Read this file for CI workflows, workflow runs, jobs, logs, artifacts, and runners.

## Core Tools

| Goal | Canonical method |
| --- | --- |
| List workflows | `atomgit_get_repository_actions_workflows` |
| Validate workflow YAML | `atomgit_validate_repository_actions_workflow` |
| Manually run a workflow | `atomgit_dispatch_repository_actions_workflow` |
| List workflow runs | `atomgit_get_repository_actions_runs` |
| Inspect one run | `atomgit_get_repository_actions_run` |
| Rerun a workflow run | `atomgit_rerun_repository_actions_run` |
| Retry failed jobs only | `atomgit_retry_repository_actions_run` |
| Stop a running workflow | `atomgit_stop_repository_actions_run` |
| List jobs of a run | `atomgit_get_repository_actions_run_jobs` |
| Inspect one job | `atomgit_get_repository_actions_run_job` |
| Download a job log | `atomgit_download_repository_actions_run_job_log` |
| Query step-level logs | `atomgit_query_repository_actions_job_step_logs` |
| List artifacts | `atomgit_get_repository_actions_artifacts` |
| Inspect one artifact | `atomgit_get_repository_actions_artifact` |
| List artifacts of a run | `atomgit_get_repository_actions_run_artifacts` |
| Download an artifact | `atomgit_download_repository_actions_artifact` |
| Delete an artifact | `atomgit_delete_repository_actions_artifact` |
| List repo host runners | `atomgit_get_repository_actions_runners` |
| List repo K8S runners | `atomgit_get_repository_actions_runner_sets` |
| List shared host runners | `atomgit_get_repository_actions_shared_runners` |
| List shared K8S runners | `atomgit_get_repository_actions_shared_runner_sets` |
| List org runner groups | `atomgit_get_organization_actions_runner_groups` |
| Inspect one runner group | `atomgit_get_organization_actions_runner_group` |
| List host runners of a group | `atomgit_get_organization_actions_runner_group_runners` |
| List K8S runners of a group | `atomgit_get_organization_actions_runner_group_runner_sets` |
| List namespaces allowed to use a group | `atomgit_get_organization_actions_runner_group_shared_namespaces` |
| Query runner job history | `atomgit_get_organization_actions_job_history` |

## Debug Flow

1. Find the target run with `atomgit_get_repository_actions_runs`, filtering by branch, event, status, or pull request number.
2. Inspect the run with `atomgit_get_repository_actions_run`.
3. Drill into jobs with `atomgit_get_repository_actions_run_jobs`, then one job with `atomgit_get_repository_actions_run_job`.
4. Read logs with `atomgit_query_repository_actions_job_step_logs`; pass a step id from the job's steps array to narrow to one step.
5. Rerun the whole run or retry only the failed jobs after confirming intent.

## Notes

- AtomGit workflow YAML dialect: every step must have a `name` field, and `on` must be structured (e.g. `on.push.branches`); a bare `on: push` fails validation. Run `atomgit_validate_repository_actions_workflow` before dispatching edited YAML.
- `atomgit_dispatch_repository_actions_workflow` only works when the workflow declares a `workflow_dispatch` trigger; pass an empty object for `inputs` when there are none.
- Start/end time filters on run queries are Unix timestamps in milliseconds.
- Runner tooling is read-only: host runners, K8S runner sets, org runner groups, and job history. Treat `stop`, `rerun`, `retry`, and artifact `delete` as write operations that need explicit confirmation.
