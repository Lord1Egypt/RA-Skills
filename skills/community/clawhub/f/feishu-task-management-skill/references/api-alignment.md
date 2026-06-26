# API Alignment

Read this file only when updating toolkit request shapes or aligning the default CLI behavior to newer Feishu API samples.

## Contact Endpoints Used In v1

- `GET /contact/v3/scopes`
- `GET /contact/v3/users/find_by_department`

## Task Endpoints Used In v1

- `POST /task/v2/tasks`
- `GET /task/v2/tasks/{task_guid}`
- `GET /task/v2/tasks`
- `PATCH /task/v2/tasks/{task_guid}`
- `DELETE /task/v2/tasks/{task_guid}`
- `POST /task/v2/tasks/{task_guid}/add_members`
- `POST /task/v2/tasks/{task_guid}/remove_members`

## Toolkit Design Choice

The toolkit keeps payload builders centralized in `TaskService` and related helpers so API-shape changes can be made in one place.

The HTTP client now uses mixed auth:

- contact endpoints use `tenant_access_token`
- task endpoints prefer a configured `user_access_token`
- task endpoints fall back to `tenant_access_token` when no user token is configured

OAuth bootstrap is done by exchanging an authorization code through `POST /authen/v2/oauth/token`. Automatic refresh is not implemented yet.

## Escape Hatch

`TaskService.create_task`, `TaskService.update_task`, `TaskService.add_members`, and `TaskService.remove_members` support `raw_body` overrides. Use that only as a temporary alignment mechanism while updating the canonical payload builders.
