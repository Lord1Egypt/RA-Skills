# Baserow access policy

An access policy limits which endpoints Baserow connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/baserow#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Baserow: its 165 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create baserow --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/_health/celery-queue"},
    {"method": "GET", "path": "api/_health/full"},
    {"method": "GET", "path": "api/admin/audit-log"},
    {"method": "GET", "path": "api/admin/audit-log/action-types"},
    {"method": "GET", "path": "api/admin/audit-log/actors"},
    {"method": "GET", "path": "api/admin/dashboard"},
    {"method": "GET", "path": "api/admin/data-scanner/results"},
    {"method": "GET", "path": "api/admin/data-scanner/scans"},
    {"method": "GET", "path": "api/admin/data-scanner/scans/{id}"},
    {"method": "GET", "path": "api/admin/data-scanner/workspace-structure/{id}"},
    {"method": "GET", "path": "api/admin/templates"},
    {"method": "GET", "path": "api/admin/templates/counts"},
    {"method": "GET", "path": "api/admin/users"},
    {"method": "GET", "path": "api/admin/workspaces"},
    {"method": "GET", "path": "api/admin/workspaces/options"},
    {"method": "GET", "path": "api/database/admin/views"},
    {"method": "GET", "path": "api/agent/{id}"},
    {"method": "GET", "path": "api/agent/{id}/configuration"},
    {"method": "GET", "path": "api/agent/{id}/conversations"},
    {"method": "GET", "path": "api/agent/{id}/conversations/{id}/messages"},
    {"method": "GET", "path": "api/agent/{id}/run-as-subjects"},
    {"method": "GET", "path": "api/agent/{id}/triggers"},
    {"method": "GET", "path": "api/agents/workspace/{id}"},
    {"method": "GET", "path": "api/ai-providers"},
    {"method": "GET", "path": "api/ai-providers/features"},
    {"method": "GET", "path": "api/ai-providers/models/discover"},
    {"method": "GET", "path": "api/ai-providers/models/{id}/usage"},
    {"method": "GET", "path": "api/ai-providers/types"},
    {"method": "GET", "path": "api/application/{id}/integrations"},
    {"method": "GET", "path": "api/application/{id}/list-user-source-users"},
    {"method": "GET", "path": "api/application/{id}/user-sources"},
    {"method": "GET", "path": "api/application/{id}/user-sources/roles"},
    {"method": "GET", "path": "api/applications"},
    {"method": "GET", "path": "api/applications/workspace/{id}"},
    {"method": "GET", "path": "api/applications/{id}"},
    {"method": "GET", "path": "assistant/chat"},
    {"method": "GET", "path": "assistant/chat/{id}/messages"},
    {"method": "GET", "path": "api/audit-log"},
    {"method": "GET", "path": "api/audit-log/action-types"},
    {"method": "GET", "path": "api/audit-log/actors"},
    {"method": "GET", "path": "api/auth-provider/login-options"},
    {"method": "GET", "path": "api/automation/node_histories/{id}/result"},
    {"method": "GET", "path": "api/automation/workflow/{id}/nodes"},
    {"method": "GET", "path": "api/automation/workflow_histories/{id}/node_histories"},
    {"method": "GET", "path": "api/automation/workflows/{id}"},
    {"method": "GET", "path": "api/automation/workflows/{id}/history"},
    {"method": "GET", "path": "api/builder/data-source/{id}/record-names"},
    {"method": "GET", "path": "api/builder/domains/aREDACTED-SECRET"},
    {"method": "GET", "path": "api/builder/domains/published/by_id/{id}"},
    {"method": "GET", "path": "api/builder/domains/published/by_name/{id}"},
    {"method": "GET", "path": "api/builder/domains/published/page/{id}/data_sources"},
    {"method": "GET", "path": "api/builder/domains/published/page/{id}/elements"},
    {"method": "GET", "path": "api/builder/domains/published/page/{id}/workflow_actions"},
    {"method": "GET", "path": "api/builder/page/{id}/data-sources"},
    {"method": "GET", "path": "api/builder/page/{id}/elements"},
    {"method": "GET", "path": "api/builder/page/{id}/workflow_actions"},
    {"method": "GET", "path": "api/builder/preview/{id}/custom-code/css"},
    {"method": "GET", "path": "api/builder/preview/{id}/custom-code/js"},
    {"method": "GET", "path": "api/builder/{id}/domains"},
    {"method": "GET", "path": "api/chat-runs/{id}"},
    {"method": "GET", "path": "api/chat-runs/{id}/stream"},
    {"method": "GET", "path": "api/custom_code/{id}/css/public"},
    {"method": "GET", "path": "api/custom_code/{id}/js/public"},
    {"method": "GET", "path": "api/dashboard/public/{id}"},
    {"method": "GET", "path": "api/dashboard/public/{id}/auth"},
    {"method": "GET", "path": "api/dashboard/{id}/data-sources"},
    {"method": "GET", "path": "api/dashboard/{id}/widgets"},
    {"method": "GET", "path": "api/data-sync/{id}/periodic-interval"},
    {"method": "GET", "path": "api/database/data-sync/{id}"},
    {"method": "GET", "path": "api/database/data-sync/{id}/properties"},
    {"method": "GET", "path": "api/database/export/{id}"},
    {"method": "GET", "path": "api/database/field/{id}/workflow_actions"},
    {"method": "GET", "path": "api/field-permissions/{id}"},
    {"method": "GET", "path": "api/field-permissions/{id}/subjects"},
    {"method": "GET", "path": "api/database/field-rules/{id}"},
    {"method": "GET", "path": "api/database/field-rules/{id}/invalid-rows"},
    {"method": "GET", "path": "api/database/fields/table/{id}"},
    {"method": "GET", "path": "api/database/fields/{id}"},
    {"method": "GET", "path": "api/database/fields/{id}/unique_row_values"},
    {"method": "GET", "path": "api/files/{id}"},
    {"method": "POST", "path": "api/database/formula/{id}/type"},
    {"method": "GET", "path": "api/jobs"},
    {"method": "GET", "path": "api/jobs/{id}"},
    {"method": "GET", "path": "api/last-viewed/items"},
    {"method": "GET", "path": "api/licenses"},
    {"method": "GET", "path": "api/licenses/{id}"},
    {"method": "GET", "path": "api/licenses/{id}/lookup-users"},
    {"method": "GET", "path": "api/mcp/oauth/connections"},
    {"method": "GET", "path": "api/mcp/oauth/consent"},
    {"method": "GET", "path": "api/notifications/{id}"},
    {"method": "GET", "path": "api/role/{id}"},
    {"method": "GET", "path": "api/role/{id}/effective-access"},
    {"method": "GET", "path": "api/role/{id}/invitation-links"},
    {"method": "GET", "path": "api/role/{id}/invitations"},
    {"method": "GET", "path": "api/role/{id}/subject-role-assignments"},
    {"method": "GET", "path": "api/row_comments/{id}/{id}"},
    {"method": "GET", "path": "api/database/rows/names"},
    {"method": "GET", "path": "api/database/rows/table/{id}"},
    {"method": "GET", "path": "api/database/rows/table/{id}/{id}"},
    {"method": "GET", "path": "api/database/rows/table/{id}/{id}/adjacent"},
    {"method": "GET", "path": "api/database/rows/table/{id}/{id}/history"},
    {"method": "GET", "path": "api/search/workspace/{id}"},
    {"method": "GET", "path": "api/settings"},
    {"method": "GET", "path": "api/settings/instance-id"},
    {"method": "GET", "path": "api/snapshots/application/{id}"},
    {"method": "GET", "path": "api/sso/saml/login-url"},
    {"method": "GET", "path": "api/subjects"},
    {"method": "GET", "path": "api/database/tables/all-tables"},
    {"method": "GET", "path": "api/database/tables/database/{id}"},
    {"method": "GET", "path": "api/database/tables/{id}"},
    {"method": "GET", "path": "api/teams/workspace/{id}"},
    {"method": "GET", "path": "api/teams/{id}"},
    {"method": "GET", "path": "api/teams/{id}/subjects"},
    {"method": "GET", "path": "api/teams/{id}/subjects/{id}"},
    {"method": "GET", "path": "api/database/tokens/check"},
    {"method": "GET", "path": "api/trash"},
    {"method": "GET", "path": "api/trash/workspace/{id}"},
    {"method": "GET", "path": "api/two-factor-auth/configuration"},
    {"method": "GET", "path": "api/user/dashboard"},
    {"method": "GET", "path": "api/database/view/get-public-view-export/{id}"},
    {"method": "GET", "path": "api/database/views/calendar/{id}"},
    {"method": "GET", "path": "api/database/views/calendar/{id}/public/rows"},
    {"method": "GET", "path": "api/database/views/decoration/{id}"},
    {"method": "GET", "path": "api/database/views/filter-group/{id}"},
    {"method": "GET", "path": "api/database/views/filter/{id}"},
    {"method": "GET", "path": "api/database/views/form/{id}/edit-row/{id}"},
    {"method": "GET", "path": "api/database/views/form/{id}/submit"},
    {"method": "GET", "path": "api/database/views/gallery/{id}"},
    {"method": "GET", "path": "api/database/views/gallery/{id}/public/rows"},
    {"method": "GET", "path": "api/database/views/grid/{id}"},
    {"method": "POST", "path": "api/database/views/grid/{id}"},
    {"method": "GET", "path": "api/database/views/grid/{id}/aggregation/{id}"},
    {"method": "GET", "path": "api/database/views/grid/{id}/aggregations"},
    {"method": "GET", "path": "api/database/views/grid/{id}/group-by-data"},
    {"method": "GET", "path": "api/database/views/grid/{id}/public/aggregations"},
    {"method": "GET", "path": "api/database/views/grid/{id}/public/group-by-data"},
    {"method": "GET", "path": "api/database/views/grid/{id}/public/rows"},
    {"method": "GET", "path": "api/database/views/group_by/{id}"},
    {"method": "GET", "path": "api/database/views/kanban/{id}"},
    {"method": "GET", "path": "api/database/views/kanban/{id}/public/rows"},
    {"method": "GET", "path": "api/database/views/sort/{id}"},
    {"method": "GET", "path": "api/database/views/table/{id}"},
    {"method": "GET", "path": "api/database/views/timeline/{id}"},
    {"method": "GET", "path": "api/database/views/timeline/{id}/public/rows"},
    {"method": "GET", "path": "api/database/views/{id}"},
    {"method": "GET", "path": "api/database/views/{id}/decorations"},
    {"method": "GET", "path": "api/database/views/{id}/field-options"},
    {"method": "GET", "path": "api/database/views/{id}/filters"},
    {"method": "GET", "path": "api/database/views/{id}/group_bys"},
    {"method": "GET", "path": "api/database/views/{id}/link-row-field-lookup/{id}"},
    {"method": "GET", "path": "api/database/views/{id}/public/info"},
    {"method": "GET", "path": "api/database/views/{id}/row/{id}"},
    {"method": "GET", "path": "api/database/views/{id}/sortings"},
    {"method": "GET", "path": "api/database/webhooks/table/{id}"},
    {"method": "GET", "path": "api/database/webhooks/{id}"},
    {"method": "GET", "path": "api/webhooks/{id}"},
    {"method": "GET", "path": "api/workspaces"},
    {"method": "GET", "path": "api/workspaces/invitation-links/slug/{id}"},
    {"method": "GET", "path": "api/workspaces/invitation-links/workspace/{id}"},
    {"method": "GET", "path": "api/workspaces/invitations/token/{id}"},
    {"method": "GET", "path": "api/workspaces/invitations/workspace/{id}"},
    {"method": "GET", "path": "api/workspaces/invitations/{id}"},
    {"method": "GET", "path": "api/workspaces/users/workspace/{id}"},
    {"method": "GET", "path": "api/workspaces/{id}/export"},
    {"method": "GET", "path": "api/workspaces/{id}/permissions"}
  ],
  "deny": []
}
```

## Endpoints

The Baserow endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/_health/celery-queue | read | _health | Health check endpoint to check if the celery, export and/or chat_run queue has exceeded the maximum healthy size. |
| POST | api/_health/email | write | _health | Sends a test email to the provided email address. |
| GET | api/_health/full | read | _health | Runs a full health check testing as many services and systems as possible. |
| POST | api/abuse-reports | write | abuse-reports | Reports a publicly shared resource, like a shared view or form, for abuse. |
| GET | api/admin/audit-log | read | admin | Lists all audit log entries for the given workspace id. |
| GET | api/admin/audit-log/action-types | read | admin | List all distinct action types related to an audit log entry. |
| GET | api/admin/audit-log/actors | read | admin | List users and agents available as audit log actor filters. |
| POST | api/admin/audit-log/export | write | admin | Creates a job to export the filtered audit log to a CSV file. |
| GET | api/admin/auth-provider | write | admin | List all the available authentication providers. Kept out of read: it returns the SSO provider client secret. |
| POST | api/admin/auth-provider | write | admin | Creates a new authentication provider. |
| GET | api/admin/auth-provider/{id} | write | admin | Get an authentication provider. Kept out of read: it returns the SSO provider client secret. |
| PATCH | api/admin/auth-provider/{id} | write | admin | Updates a new authentication provider. |
| DELETE | api/admin/auth-provider/{id} | write | admin | Delete an authentication provider. |
| GET | api/admin/dashboard | read | admin | Returns the new and active users for the last 24 hours, 7 days and 30 days. |
| GET | api/admin/data-scanner/results | read | admin | Lists all data scan results across all scans. |
| POST | api/admin/data-scanner/results/export | write | admin | Creates a job to export data scan results to CSV. |
| DELETE | api/admin/data-scanner/results/{id} | write | admin | Deletes (resolves) a single data scan result, marking it as reviewed. |
| GET | api/admin/data-scanner/scans | read | admin | Lists all data scans configured for this Baserow instance. |
| POST | api/admin/data-scanner/scans | write | admin | Creates a new data scan. |
| GET | api/admin/data-scanner/scans/{id} | read | admin | Returns a single data scan configuration. |
| PATCH | api/admin/data-scanner/scans/{id} | write | admin | Updates a data scan configuration. |
| DELETE | api/admin/data-scanner/scans/{id} | write | admin | Deletes a data scan and all of its results. |
| POST | api/admin/data-scanner/scans/{id}/trigger | write | admin | Triggers an immediate run of the given data scan. |
| GET | api/admin/data-scanner/workspace-structure/{id} | read | admin | Returns the database/table/field structure of a workspace for use in data scan configuration. |
| GET | api/admin/templates | read | admin | Returns the user templates in review, public, rejected or blocked, if the requesting user is staff: the revision under review of a template in review or rejected, the... |
| GET | api/admin/templates/counts | read | admin | Returns how many user templates are in review, public, rejected and blocked, if the requesting user is staff. |
| POST | api/admin/templates/{id}/approve | write | admin | Approves a user template in review or rejected, if the requesting user is staff: the revision they reviewed is listed for everybody on this instance in place of the... |
| POST | api/admin/templates/{id}/block | write | admin | Blocks a user template in any state, if the requesting user is staff. |
| POST | api/admin/templates/{id}/reject | write | admin | Rejects a user template in review, or a listed one, if the requesting user is staff. |
| POST | api/admin/templates/{id}/unblock | write | admin | Lifts the block of a user template, if the requesting user is staff. |
| GET | api/admin/users | read | admin | Returns all users with detailed information on each user, if the requesting user is staff. |
| POST | api/admin/users | write | admin | Creates and returns a new user if the requesting user is staff. |
| POST | api/admin/users/impersonate | write | admin | This endpoint allows staff to impersonate another user by requesting a JWT token and user object. |
| PATCH | api/admin/users/{id} | write | admin | Updates specified user attributes and returns the updated user if the requesting user is staff. |
| DELETE | api/admin/users/{id} | write | admin | Deletes the specified user, if the requesting user has admin permissions. |
| DELETE | api/admin/users/{id}/two-factor-auth | write | admin | Removes the configured two-factor authentication of the specified user, if the requesting user is staff. |
| GET | api/admin/workspaces | read | admin | Returns all workspaces with detailed information on each workspace, if the requesting user is staff. |
| GET | api/admin/workspaces/options | read | admin | Lists all workspaces. |
| DELETE | api/admin/workspaces/{id} | write | admin | Deletes the specified workspace and the applications inside that workspace, if the requesting user is staff. |
| GET | api/database/admin/views | read | admin | Returns all database views in the instance with information about the table, database and workspace they belong to, if the requesting user is staff. |
| PATCH | api/database/admin/views/{id} | write | admin | Updates whether the specified view is publicly shared, if the requesting user is staff. |
| POST | api/database/admin/views/{id}/rotate-slug | write | admin | Rotates the slug of the specified view, permanently invalidating the current public URL, if the requesting user is staff. |
| GET | api/agent/{id} | read | agent | Returns the agent, including its readiness, and records that the user opened it. |
| POST | api/agent/{id} | write | agent | Records that the user opened the agent. |
| GET | api/agent/{id}/configuration | read | agent | Returns the instructions, provider, model, reasoning effort and run-as identity of the agent, with its readiness and the fields that are missing or no longer available. |
| PATCH | api/agent/{id}/configuration | write | agent | Updates the provided fields of the agent configuration and returns the result. |
| GET | api/agent/{id}/conversations | read | agent | Lists the authenticated user's own conversations with the agent and the shared ones its triggers started, pinned first, then most recently active within each group. |
| POST | api/agent/{id}/conversations | write | agent | Starts a private conversation with its first message. |
| PATCH | api/agent/{id}/conversations/{id} | write | agent | Updates the title or pinned state of one of the authenticated user's conversations, without changing its last activity time. |
| DELETE | api/agent/{id}/conversations/{id} | write | agent | Moves one of the authenticated user's conversations to the trash and stops the reply being written in it. |
| POST | api/agent/{id}/conversations/{id}/approvals | write | agent | Approves or rejects tool calls that the waiting reply of one of the authenticated user's conversations, or of a shared conversation a trigger started, holds for approval. |
| GET | api/agent/{id}/conversations/{id}/messages | read | agent | Lists the messages of one of the authenticated user's conversations, newest page first, each page in chronological order. |
| POST | api/agent/{id}/conversations/{id}/messages | write | agent | Adds a message to one of the authenticated user's conversations. |
| GET | api/agent/{id}/run-as-subjects | read | agent | Lists active workspace identities selectable for this Agent. |
| GET | api/agent/{id}/triggers | read | agent | Lists the triggers of the agent with their service, message and the schema of the payload each event provides. |
| POST | api/agent/{id}/triggers | write | agent | Adds a trigger of one of the configuration's available_trigger_types to the agent, with initial values for its service. |
| PATCH | api/agent/{id}/triggers/{id} | write | agent | Updates the provided fields of the trigger: its name, its switch, its message, its overlap rule and the values of its service, whose type is fixed. |
| DELETE | api/agent/{id}/triggers/{id} | write | agent | Moves the trigger to the trash, where it can be restored. |
| GET | api/agents/workspace/{id} | read | agents | Lists the agents in a workspace. |
| POST | api/agents/workspace/{id} | write | agents | Creates a new agent in a workspace. |
| PATCH | api/agents/{id} | write | agents | Updates an existing agent. |
| DELETE | api/agents/{id} | write | agents | Deletes an existing agent. |
| GET | api/ai-providers | read | ai-providers | Pins authenticated realtime recovery reads to the primary database. |
| POST | api/ai-providers | write | ai-providers | Pins authenticated realtime recovery reads to the primary database. |
| GET | api/ai-providers/features | read | ai-providers | Pins authenticated realtime recovery reads to the primary database. |
| PUT | api/ai-providers/features/{id} | write | ai-providers | . |
| GET | api/ai-providers/models/discover | read | ai-providers | . |
| POST | api/ai-providers/models/test | write | ai-providers | . |
| PATCH | api/ai-providers/models/{id} | write | ai-providers | . |
| DELETE | api/ai-providers/models/{id} | write | ai-providers | . |
| GET | api/ai-providers/models/{id}/usage | read | ai-providers | . |
| GET | api/ai-providers/types | read | ai-providers | . |
| PATCH | api/ai-providers/{id} | write | ai-providers | . |
| DELETE | api/ai-providers/{id} | write | ai-providers | . |
| POST | api/ai-providers/{id}/models | write | ai-providers | . |
| GET | api/application/{id}/integrations | read | application | Lists all the integrations of the application related to the provided parameter if the user has access to the related application's workspace. |
| POST | api/application/{id}/integrations | write | application | Creates a new integration. |
| GET | api/application/{id}/list-user-source-users | read | application | List per user sources the first 5 users available. |
| GET | api/application/{id}/user-sources | read | application | Lists all the user_sources of the application related to the provided parameter if the user has access to the related application's workspace. |
| POST | api/application/{id}/user-sources | write | application | Creates a new user_source. |
| GET | api/application/{id}/user-sources/roles | read | application | Lists all the roles of the application related to the provided parameter if the user has access to the related application's workspace. |
| GET | api/applications | read | applications | Lists all the applications that the user has access to. |
| GET | api/applications/workspace/{id} | read | applications | Lists all the applications of the workspace related to the provided workspace_id parameter if the authorized user is in that workspace. |
| POST | api/applications/workspace/{id} | write | applications | Creates a new application based on the provided type. |
| POST | api/applications/workspace/{id}/order | write | applications | Changes the order of the provided application ids to the matching position that the id has in the list. |
| GET | api/applications/{id} | read | applications | Returns the requested application if the authorized user is in the application's workspace. |
| PATCH | api/applications/{id} | write | applications | Updates the existing application related to the provided application_id param if the authorized user is in the application's workspace. |
| DELETE | api/applications/{id} | write | applications | Deletes an application if the authorized user is in the application's workspace. |
| POST | api/applications/{id}/duplicate/async | write | applications | Duplicate an application if the authorized user is in the application's workspace. |
| GET | assistant/chat | read | assistant | List all AI assistant chats for the current user in the specified workspace. |
| GET | assistant/chat/{id}/cancel | write | assistant | List all messages in the specified AI assistant chat. Kept out of read: the path cancels a chat run (spec description is a copy of the messages list). |
| POST | assistant/chat/{id}/cancel | write | assistant | Send a message to the specified AI assistant chat and stream back the response. |
| DELETE | assistant/chat/{id}/cancel | write | assistant | Cancel an ongoing assistant message generation in the specified chat. |
| GET | assistant/chat/{id}/messages | read | assistant | List all messages in the specified AI assistant chat. |
| POST | assistant/chat/{id}/messages | write | assistant | Send a message to the specified AI assistant chat and stream back the response. |
| DELETE | assistant/chat/{id}/messages | write | assistant | Cancel an ongoing assistant message generation in the specified chat. |
| PUT | assistant/messages/{id}/feedback | write | assistant | Provide sentiment and feedback for the given AI assistant chat message. |
| POST | assistant/onboarding/prompt-suggestions | write | assistant | Suggests databases the user could create during the onboarding, based on the industry and team they provided. |
| GET | api/audit-log | read | audit-log | Lists all audit log entries for the given workspace id. |
| GET | api/audit-log/action-types | read | audit-log | List all distinct action types related to an audit log entry. |
| GET | api/audit-log/actors | read | audit-log | List users and agents available as audit log actor filters. |
| POST | api/audit-log/export | write | audit-log | Creates a job to export the filtered audit log to a CSV file. |
| GET | api/auth-provider/login-options | read | auth-provider | Lists the available login options for the configured authentication providers. |
| PATCH | api/automation/node/{id} | write | automation | Updates an existing automation node. |
| DELETE | api/automation/node/{id} | write | automation | Deletes an existing automation node. |
| POST | api/automation/node/{id}/duplicate | write | automation | Duplicate a node of a workflow. |
| POST | api/automation/node/{id}/move | write | automation | Move a node in a workflow to a new position. |
| POST | api/automation/node/{id}/replace | write | automation | Replace a node in a workflow with one of a new type. |
| POST | api/automation/node/{id}/simulate-dispatch | write | automation | Simulate a dispatch for a node. |
| GET | api/automation/node_histories/{id}/result | read | automation | Returns the node history's result JSON. |
| GET | api/automation/workflow/{id}/nodes | read | automation | Lists all the nodes of the workflow related to the provided parameter if the user has access to the related automation's workspace. |
| POST | api/automation/workflow/{id}/nodes | write | automation | Creates a new automation workflow node. |
| POST | api/automation/workflow_histories/{id}/cancel | write | automation | Requests the cancellation of a running workflow. |
| GET | api/automation/workflow_histories/{id}/node_histories | read | automation | Returns all node histories for the given workflow history. |
| GET | api/automation/workflows/{id} | read | automation | Retrieve a single workflow of an automation. |
| PATCH | api/automation/workflows/{id} | write | automation | Updates an existing workflow of an automation. |
| DELETE | api/automation/workflows/{id} | write | automation | Deletes an existing workflow of an automation. |
| POST | api/automation/workflows/{id}/duplicate/async | write | automation | Start a job to duplicate the workflow with the provided workflow_id parameter if the authorized user has access to the automation's workspace. |
| GET | api/automation/workflows/{id}/history | read | automation | Retrieve the history for a workflow. |
| POST | api/automation/workflows/{id}/publish/async | write | automation | This endpoint starts an asynchronous job to publish the automation workflow. |
| POST | api/automation/workflows/{id}/test | write | automation | This endpoint plan the execution of a test run for this workflow. |
| POST | api/automation/{id}/workflows | write | automation | Creates a new Automation Workflow. |
| POST | api/automation/{id}/workflows/order | write | automation | Apply a new order to the workflows of an automation. |
| PATCH | api/builder/data-source/{id} | write | builder | Updates an existing builder data_source. |
| DELETE | api/builder/data-source/{id} | write | builder | Deletes the data_source related by the given id. |
| POST | api/builder/data-source/{id}/dispatch | write | builder | Dispatches the service of the related data_source and returns the result. |
| PATCH | api/builder/data-source/{id}/move | write | builder | Moves the data_source in the page before another data_source or at the end of the page if no before data_source is given. |
| GET | api/builder/data-source/{id}/record-names | read | builder | Find the record names associated with a given list of record ids. |
| POST | api/builder/data-source/{id}/simulate-dispatch | write | builder | Dispatches the service of the related data_source and stores the result as the service's sample data. |
| GET | api/builder/domains/aREDACTED-SECRET | read | builder | This endpoint can be used to check whether a domain exists for SSL certificate purposes. |
| GET | api/builder/domains/published/by_id/{id} | read | builder | Returns the public serialized version of the builder and its pages for the given builder id. |
| GET | api/builder/domains/published/by_name/{id} | read | builder | Returns the public serialized version of the builder for the given domain name and its pages . |
| POST | api/builder/domains/published/data-source/{id}/dispatch | write | builder | Dispatches the service of the related data_source and returns the result. |
| GET | api/builder/domains/published/page/{id}/data_sources | read | builder | Lists all the data_sources of the page related to the provided parameter if the builder is public. |
| POST | api/builder/domains/published/page/{id}/dispatch-data-sources | write | builder | Dispatches the service of the related page data_sources. |
| GET | api/builder/domains/published/page/{id}/elements | read | builder | Lists all the elements of the page related to the provided parameter. |
| GET | api/builder/domains/published/page/{id}/workflow_actions | read | builder | Lists all the workflow actions with their public accessible data. |
| PATCH | api/builder/domains/{id} | write | builder | Updates an existing domain of an application builder. |
| DELETE | api/builder/domains/{id} | write | builder | Deletes an existing domain of an application builder. |
| POST | api/builder/domains/{id}/publish/async | write | builder | This endpoint starts an asynchronous job to publish the builder. |
| PATCH | api/builder/element/{id} | write | builder | Updates an existing builder element. |
| DELETE | api/builder/element/{id} | write | builder | Deletes the element related by the given id. |
| POST | api/builder/element/{id}/duplicate | write | builder | Duplicates an element and all of the elements children and the associated workflow actions as well. |
| PATCH | api/builder/element/{id}/move | write | builder | Moves the element in the page before another element or at the end of the page if no before element is given. |
| GET | api/builder/page/{id}/data-sources | read | builder | Lists all the data_sources of the page related to the provided parameter if the user has access to the related builder's workspace. |
| POST | api/builder/page/{id}/data-sources | write | builder | Creates a new builder data_source. |
| POST | api/builder/page/{id}/dispatch-data-sources | write | builder | Dispatches the service of the related page data_sources. |
| GET | api/builder/page/{id}/elements | read | builder | Lists all the elements of the page related to the provided parameter if the user has access to the related builder's workspace. |
| POST | api/builder/page/{id}/elements | write | builder | Creates a new builder element. |
| GET | api/builder/page/{id}/workflow_actions | read | builder | Lists all the workflow actions of the page related to the provided parameter if the user has access to the related builder's workspace. |
| POST | api/builder/page/{id}/workflow_actions | write | builder | Creates a new builder workflow action. |
| POST | api/builder/page/{id}/workflow_actions/order | write | builder | Apply a new order to the workflow actions of a page. |
| PATCH | api/builder/pages/{id} | write | builder | Updates an existing page of an application builder. |
| DELETE | api/builder/pages/{id} | write | builder | Deletes an existing page of an application builder. |
| POST | api/builder/pages/{id}/duplicate/async | write | builder | Start a job to duplicate the page with the provided page_id parameter if the authorized user has access to the builder's workspace. |
| GET | api/builder/preview/exchange/{id} | write | builder | Consume the preview pass, set a session cookie, and redirect the browser. Kept out of read: consumes a preview pass and sets a session cookie. |
| POST | api/builder/preview/handoff | write | builder | Let the preview Nuxt server consume an opaque one-time handoff code. |
| GET | api/builder/preview/{id}/custom-code/css | read | builder | Returns the css/js for the given builder. |
| GET | api/builder/preview/{id}/custom-code/js | read | builder | Returns the css/js for the given builder. |
| POST | api/builder/preview/{id}/grant | write | builder | Start the preview process for a logged-in editor. |
| PATCH | api/builder/workflow_action/{id} | write | builder | Updates an existing builder workflow action. |
| DELETE | api/builder/workflow_action/{id} | write | builder | Deletes the workflow action related by the given id. |
| POST | api/builder/workflow_action/{id}/dispatch | write | builder | Dispatches the service of the related workflow_action and returns the result. |
| GET | api/builder/{id}/domains | read | builder | Gets all the domains of a builder. |
| POST | api/builder/{id}/domains | write | builder | Creates a new domain for an application builder. |
| POST | api/builder/{id}/domains/order | write | builder | Apply a new order to the domains of a builder. |
| POST | api/builder/{id}/pages | write | builder | Creates a new page for an application builder. |
| POST | api/builder/{id}/pages/order | write | builder | Apply a new order to the pages of a builder. |
| PATCH | api/builder/{id}/theme | write | builder | Updates the theme properties for the provided id. |
| GET | api/chat-runs/{id} | read | chat-runs | Read durable run status and its saved outcome, including after replay expires. |
| POST | api/chat-runs/{id}/cancel | write | chat-runs | Request Stop for this run. |
| GET | api/chat-runs/{id}/stream | read | chat-runs | Follow a run's output as JSON records separated by blank lines, ending with run.finished. |
| GET | api/custom_code/{id}/css/public | read | custom_code | Returns the css/js for the given builder. |
| GET | api/custom_code/{id}/js/public | read | custom_code | Returns the css/js for the given builder. |
| PATCH | api/dashboard/data-sources/{id} | write | dashboard | Updates an existing dashboard data source. |
| POST | api/dashboard/data-sources/{id}/dispatch | write | dashboard | Dispatches the service of the related data source and returns the result. |
| GET | api/dashboard/public/{id} | read | dashboard | Returns the dashboard, its widgets and its data sources of a publicly shared dashboard. |
| GET | api/dashboard/public/{id}/auth | read | dashboard | Returns what the password page of a publicly shared dashboard needs before the password is entered, currently whether the Baserow logo must be shown. |
| POST | api/dashboard/public/{id}/auth | write | dashboard | Returns a valid never-expiring JWT token for this publicly shared dashboard if the password provided matches with the one saved by the dashboard's owner. |
| POST | api/dashboard/public/{id}/data-sources/{id}/dispatch | write | dashboard | Dispatches the service of the related data source of the publicly shared dashboard and returns the result. |
| PATCH | api/dashboard/widgets/{id} | write | dashboard | Updates an existing dashboard widget. |
| DELETE | api/dashboard/widgets/{id} | write | dashboard | Deletes the widget related to the given id. |
| GET | api/dashboard/{id}/data-sources | read | dashboard | Lists all the data sources of the dashboard if the user has access to the related dashboard's workspace. |
| PATCH | api/dashboard/{id}/premium | write | dashboard | Sets dashboard attributes only available for premium users. |
| POST | api/dashboard/{id}/rotate-slug | write | dashboard | Rotates the unique slug of the dashboard by replacing it with a new value. |
| PATCH | api/dashboard/{id}/sharing | write | dashboard | Makes the dashboard publicly accessible via its shared URL, or private again, and sets or removes the password that visitors must enter. |
| GET | api/dashboard/{id}/widgets | read | dashboard | Lists all the widgets of the dashboard related to the provided parameter if the user has access to the related workspace. |
| POST | api/dashboard/{id}/widgets | write | dashboard | Creates a new dashboard widget. |
| PATCH | api/dashboard/{id}/widgets/layout | write | dashboard | Atomically updates and vertically compacts the layout of every dashboard widget visible to the current user. |
| GET | api/data-sync/{id}/periodic-interval | read | data-sync | Responds with the periodic data sync interval data, if the user has the right permissions. |
| PATCH | api/data-sync/{id}/periodic-interval | write | data-sync | Updates the periodic data sync interval, if the user has the right permissions. |
| POST | api/database/data-sync/database/{id} | write | data-sync | Creates a new data sync table with the given data sync type. |
| POST | api/database/data-sync/database/{id}/properties | write | data-sync | Lists all the properties of the provided data sync type given the request data. |
| GET | api/database/data-sync/{id} | read | data-sync | Responds with the data sync, including the data sync type specific properties, if the user has the right permissions. |
| PATCH | api/database/data-sync/{id} | write | data-sync | Updates the properties of the provided data sync, if the user has the right permissions. |
| GET | api/database/data-sync/{id}/properties | read | data-sync | Lists all the available properties of the provided data sync. |
| POST | api/database/data-sync/{id}/sync/async | write | data-sync | Start a job to sync the data sync table with the provided data_sync_id parameter if the authorized user has access to the database's workspace. |
| POST | api/database/export/table/{id} | write | export | Creates and starts a new export job for a table given some exporter options. |
| GET | api/database/export/{id} | read | export | Returns information such as export progress and state or the url of the exported file for the specified export job, only if the requesting user has access. |
| GET | api/database/field/{id}/workflow_actions | read | field | Lists all the workflow actions of the button field related to the provided parameter if the user has access to the related database's workspace. |
| POST | api/database/field/{id}/workflow_actions | write | field | Creates a new database workflow action. |
| POST | api/database/field/{id}/workflow_actions/dispatch | write | field | Runs every workflow action of a button field, in order, for the given row, and returns one result per action. |
| POST | api/database/field/{id}/workflow_actions/order | write | field | Apply a new order to the workflow actions of a button field. |
| GET | api/field-permissions/{id} | read | field-permissions | Retrieve the permissions for writing field values and form visibility of a specific field. |
| PATCH | api/field-permissions/{id} | write | field-permissions | Update permissions for writing field values and form visibility for a specific field. |
| GET | api/field-permissions/{id}/subjects | read | field-permissions | Searches users, agents, and teams that can be selected for a field-specific permission. |
| GET | api/database/field-rules/{id} | read | field-rules | Get a list of field rules for the table. |
| POST | api/database/field-rules/{id} | write | field-rules | Create a field rule for a table. |
| GET | api/database/field-rules/{id}/invalid-rows | read | field-rules | Get a list of invalid rows. |
| PUT | api/database/field-rules/{id}/rule/{id} | write | field-rules | Update a specific field rule. |
| DELETE | api/database/field-rules/{id}/rule/{id} | write | field-rules | Delete a field rule. |
| POST | api/database/fields/password-authentication | write | fields | Checks if the provided password and row matches what is stored in the cell. |
| GET | api/database/fields/table/{id} | read | fields | Lists all the fields of the table related to the provided parameter if the user has access to the related database's workspace. |
| POST | api/database/fields/table/{id} | write | fields | Creates a new field for the table related to the provided table_id parameter if the authorized user has access to the related database's workspace. |
| POST | api/database/fields/table/{id}/change-primary-field | write | fields | Changes the primary field of a table to the one provided in the body payload. |
| POST | api/database/fields/table/{id}/generate-ai-formula | write | fields | This endpoint generates a Baserow formula for the table related to the provided id, based on the human readable input provided in the request body. |
| GET | api/database/fields/{id} | read | fields | Returns the existing field if the authorized user has access to the related database's workspace. |
| PATCH | api/database/fields/{id} | write | fields | Updates the existing field if the authorized user has access to the related database's workspace. |
| DELETE | api/database/fields/{id} | write | fields | Deletes the existing field if the authorized user has access to the related database's workspace. |
| POST | api/database/fields/{id}/duplicate/async | write | fields | Duplicates the table with the provided table_id parameter if the authorized user has access to the database's workspace. |
| POST | api/database/fields/{id}/generate-ai-field-values | write | fields | Endpoint that's used by the AI field to start an sync task that will update the cell value of the provided row IDs based on the dynamically constructed prompt... |
| GET | api/database/fields/{id}/unique_row_values | read | fields | Returns a list of all the unique row values for an existing field, sorted in order of frequency. |
| GET | api/files/{id} | read | files | Downloads a file using the backend and the secure file serve feature. |
| POST | api/database/formula/{id}/type | read | formula | Calculates and returns the type of the specified formula value. |
| POST | api/inbound-email | write | inbound-email | Receives and handles an inbound email webhook request from the inbound mail server. |
| PATCH | api/integration/{id} | write | integration | Updates an existing integration. |
| DELETE | api/integration/{id} | write | integration | Deletes the integration related by the given id. |
| PATCH | api/integration/{id}/move | write | integration | Moves the integration in the application before another integration or at the end of the application if no before integration is given. |
| POST | api/integrations/mcp/oauth/complete | write | integrations | Finishes connecting an account to an MCP server with the code the provider redirected back with. |
| POST | api/integrations/mcp/{id}/oauth/disconnect | write | integrations | Forgets the account connected to an MCP server. |
| POST | api/integrations/mcp/{id}/oauth/start | write | integrations | Starts connecting an account to an MCP server that uses OAuth. |
| POST | api/integrations/mcp/{id}/refresh-tools | write | integrations | Lists the MCP server's tools and stores them. |
| PATCH | api/integrations/mcp/{id}/tools | write | integrations | Turns the given tools on or off and sets whether they change data. |
| GET | api/jobs | read | jobs | List all existing jobs. |
| POST | api/jobs | write | jobs | Creates a new job. |
| GET | api/jobs/{id} | read | jobs | Returns the information related to the provided job id. |
| POST | api/jobs/{id}/cancel | write | jobs | Cancels a job. |
| GET | api/last-viewed/items | read | last-viewed | Lists the views, application pages, dashboards, automation workflows and agents the authenticated user opened most recently, newest first. |
| GET | api/licenses | read | licenses | Lists all the valid licenses that are registered to this instance. |
| POST | api/licenses | write | licenses | Registers a new license. |
| GET | api/licenses/{id} | read | licenses | Responds with detailed information about the license related to the provided parameter. |
| DELETE | api/licenses/{id} | write | licenses | Removes the existing license related to the provided parameter. |
| GET | api/licenses/{id}/check | write | licenses | This endpoint checks with the authority if the license needs to be updated. Kept out of read: contacts the license authority and can update the license. |
| POST | api/licenses/{id}/fill-seats | write | licenses | Fills the remaining empty seats of the license with the first users that are found. |
| GET | api/licenses/{id}/lookup-users | read | licenses | This endpoint can be used to lookup users that can be added to a  license. |
| POST | api/licenses/{id}/remove-all-users | write | licenses | Removes all the users that are on the license. |
| POST | api/licenses/{id}/{id} | write | licenses | Adds the user related to the provided parameter and to the license related to the parameter. |
| DELETE | api/licenses/{id}/{id} | write | licenses | Removes the user related to the provided parameter and to the license related to the parameter. |
| GET | api/mcp/endpoint/{id} | write | mcp | Returns the requested MCP endpoint if the authorized user has access to it. Kept out of read: it returns the MCP endpoint key. |
| PATCH | api/mcp/endpoint/{id} | write | mcp | Updates the name or the tools of the MCP endpoint if the authorized user has access to it. |
| DELETE | api/mcp/endpoint/{id} | write | mcp | Deletes an MCP endpoint if the authorized user has access to it. |
| GET | api/mcp/endpoints | write | mcp | Lists all the MCP (Model Context Protocol) endpoints of a user. Kept out of read: it returns the MCP endpoint key. |
| POST | api/mcp/endpoints | write | mcp | Creates a new MCP endpoint for a given workspace. |
| GET | api/mcp/oauth/connections | read | mcp | Lists the OAuth clients the user granted access to, one per grant. |
| PATCH | api/mcp/oauth/connections/{id} | write | mcp | . |
| DELETE | api/mcp/oauth/connections/{id} | write | mcp | . |
| GET | api/mcp/oauth/consent | read | mcp | . |
| POST | api/mcp/oauth/consent | write | mcp | . |
| GET | api/notifications/{id} | read | notifications | Lists the notifications for the given workspace and the current user. |
| DELETE | api/notifications/{id} | write | notifications | Clear all the notifications for the given workspace and user. |
| POST | api/notifications/{id}/mark-all-as-read | write | notifications | Mark as read all the notifications for the given workspace and user. |
| PATCH | api/notifications/{id}/{id} | write | notifications | Marks a notification as read. |
| PATCH | api/role/invitation-links/{id} | write | role | Changes the name of a permanent invitation link to a scope, or the role people get on the scope when they join through it. |
| DELETE | api/role/invitation-links/{id} | write | role | Deletes a permanent invitation link to a scope, after which it can't be used anymore. |
| PATCH | api/role/invitations/{id} | write | role | Changes the role a pending invitation grants on its scope. |
| DELETE | api/role/invitations/{id} | write | role | Revokes the role a pending invitation grants on its scope. |
| GET | api/role/{id} | read | role | You can list the role assignments within a workspace, optionally filtered downto a specific scope inside of that workspace. |
| POST | api/role/{id} | write | role | You can assign a role to a subject into the given workspace for the given scope with this endpoint. |
| POST | api/role/{id}/batch | write | role | You can assign a role to a multiple subjects into the given workspace for the given scopes with this endpoint. |
| GET | api/role/{id}/effective-access | read | role | Lists the role every user and agent of the workspace effectively holds on the given scope, and the scope it comes from: the given scope itself or one above it, held... |
| GET | api/role/{id}/invitation-links | read | role | Lists the permanent invitation links that give a role on the given scope to everyone who joins through them. |
| POST | api/role/{id}/invitation-links | write | role | Creates a permanent invitation link that gives the chosen role on one scope of the workspace. |
| GET | api/role/{id}/invitations | read | role | Lists the pending invitations that grant a role on the given scope once they are accepted. |
| POST | api/role/{id}/invitations | write | role | Invites an email address to one scope of the workspace. |
| GET | api/role/{id}/subject-role-assignments | read | role | Lists the roles a user, agent or team holds on databases, tables and restricted views of the workspace, limited to the objects whose roles the requesting user may read. |
| PATCH | api/row_comments/{id}/comment/{id} | write | row_comments | Update a row comment. |
| DELETE | api/row_comments/{id}/comment/{id} | write | row_comments | Delete a row comment. |
| GET | api/row_comments/{id}/{id} | read | row_comments | Returns all row comments for the specified table and row. |
| POST | api/row_comments/{id}/{id} | write | row_comments | Creates a comment on the specified row. |
| PUT | api/row_comments/{id}/{id}/notification-mode | write | row_comments | Updates the user's notification preferences for comments made on a specified table row. |
| GET | api/database/rows/names | read | rows | Returns the names of the given row of the given tables. |
| GET | api/database/rows/table/{id} | read | rows | Lists all the rows of the table related to the provided parameter if the user has access to the related database's workspace. |
| POST | api/database/rows/table/{id} | write | rows | Creates a new row in the table if the user has access to the related table's workspace. |
| POST | api/database/rows/table/{id}/batch | write | rows | Creates new rows in the table if the user has access to the related table's workspace. |
| PATCH | api/database/rows/table/{id}/batch | write | rows | Updates existing rows in the table if the user has access to the related table's workspace. |
| POST | api/database/rows/table/{id}/batch-delete | write | rows | Deletes existing rows in the table if the user has access to the table's workspace. |
| GET | api/database/rows/table/{id}/{id} | read | rows | Fetches an existing row from the table if the user has access to the related table's workspace. |
| PATCH | api/database/rows/table/{id}/{id} | write | rows | Updates an existing row in the table if the user has access to the related table's workspace. |
| DELETE | api/database/rows/table/{id}/{id} | write | rows | Deletes an existing row in the table if the user has access to the table's workspace. |
| GET | api/database/rows/table/{id}/{id}/adjacent | read | rows | Fetches the adjacent row to a given row_id in the table with the given table_id. |
| GET | api/database/rows/table/{id}/{id}/history | read | rows | Fetches the row change history of a given row_id in the table with the given table_id. |
| PATCH | api/database/rows/table/{id}/{id}/move | write | rows | Moves the row related to given row_id parameter to another position. |
| GET | api/search/workspace/{id} | read | search | Search across all searchable content within a workspace. |
| GET | api/settings | read | settings | Responds with all the admin configured settings. |
| GET | api/settings/instance-id | read | settings | Responds with the self hosted instance id. |
| PATCH | api/settings/update | write | settings | Updates the admin configured settings if the user has admin permissions. |
| GET | api/snapshots/application/{id} | read | snapshots | Lists snapshots that were created for a given application. |
| POST | api/snapshots/application/{id} | write | snapshots | Creates a new application snapshot. |
| DELETE | api/snapshots/{id} | write | snapshots | Deletes a snapshot. |
| POST | api/snapshots/{id}/restore | write | snapshots | Restores a snapshot. |
| GET | api/sso/oauth2/callback/{id} | write | sso | Processes callback from OAuth2 provider and logs the user in if successful. Kept out of read: completes a login and sets a session. |
| GET | api/sso/oauth2/login/{id} | write | sso | Redirects to the OAuth2 provider's authentication URL based on the provided auth provider's id. Kept out of read: starts an OAuth2 login redirect. |
| POST | api/sso/saml/acs | write | sso | Complete the SAML authentication flow by validating the SAML response. |
| GET | api/sso/saml/login | write | sso | This is the endpoint that is called when the user wants to initiate a SSO SAML login from Baserow (the service provider). Kept out of read: starts a SAML login redirect. |
| GET | api/sso/saml/login-url | read | sso | Return the correct redirect_url to initiate the SSO SAML login. |
| GET | api/subjects | read | subjects | Returns searchable options supplied by registered subject types. |
| GET | api/database/tables/all-tables | read | tables | This endpoint only works in combination with the token authentication. |
| GET | api/database/tables/database/{id} | read | tables | Lists all the tables that are in the database related to the database_id parameter if the user has access to the database's workspace. |
| POST | api/database/tables/database/{id} | write | tables | Creates synchronously a new table for the database related to the provided database_id parameter if the authorized user has access to the database's workspace. |
| POST | api/database/tables/database/{id}/async | write | tables | Creates a job that creates a new table for the database related to the provided database_id parameter if the authorized user has access to the database's workspace. |
| POST | api/database/tables/database/{id}/order | write | tables | Changes the order of the provided table ids to the matching position that the id has in the list. |
| GET | api/database/tables/{id} | read | tables | Returns the requested table if the authorized user has access to the related database's workspace. |
| PATCH | api/database/tables/{id} | write | tables | Updates the existing table if the authorized user has access to the related database's workspace. |
| DELETE | api/database/tables/{id} | write | tables | Deletes the existing table if the authorized user has access to the related database's workspace. |
| POST | api/database/tables/{id}/duplicate/async | write | tables | Start a job to duplicate the table with the provided table_id parameter if the authorized user has access to the database's workspace. |
| POST | api/database/tables/{id}/import/async | write | tables | Import data in the specified table if the authorized user has access to the related database's workspace. |
| GET | api/teams/workspace/{id} | read | teams | Lists all teams in a given workspace. |
| POST | api/teams/workspace/{id} | write | teams | Creates a new team. |
| GET | api/teams/{id} | read | teams | Returns the information related to the provided team id. |
| PUT | api/teams/{id} | write | teams | Updates an existing team with a new name. |
| DELETE | api/teams/{id} | write | teams | Deletes a team if the authorized user is in the team's workspace. |
| GET | api/teams/{id}/subjects | read | teams | Lists all team subjects in a given team. |
| POST | api/teams/{id}/subjects | write | teams | Creates a new team subject. |
| GET | api/teams/{id}/subjects/{id} | read | teams | Returns the information related to the provided subject id. |
| DELETE | api/teams/{id}/subjects/{id} | write | teams | Deletes a subject if the authorized user is in the team's workspace. |
| GET | api/templates | write | templates | Lists the templates. Kept out of read: it returns template private link tokens. |
| POST | api/templates/install/{id}/{id} | write | templates | (Deprecated) Installs the applications of the given template into the given workspace if the user has access to that workspace. |
| POST | api/templates/install/{id}/{id}/async | write | templates | Start an async job to install the applications of the given template into the given workspace if the user has access to that workspace. |
| PATCH | api/templates/{id} | write | templates | Updates a user template owned by the user. |
| DELETE | api/templates/{id} | write | templates | Deletes a user template. |
| POST | api/templates/{id}/download | write | templates | Responds with the URL of the archive of a user template, which imports like a workspace export. |
| POST | api/templates/{id}/rotate-private-link-token | write | templates | Replaces the token of the private link of a user template owned by the user, which takes the access away from everybody who has the old link. |
| GET | api/database/tokens | write | tokens | Lists all the database tokens that belong to the authorized user. Kept out of read: it returns database token keys. |
| POST | api/database/tokens | write | tokens | Creates a new database token for a given workspace and for the authorized user. |
| GET | api/database/tokens/check | read | tokens | This endpoint check be used to check if the provided personal API token is valid. |
| GET | api/database/tokens/{id} | write | tokens | Returns the requested database token if it is owned by the authorized user andif the user has access to the related workspace. Kept out of read: it returns database token keys. |
| PATCH | api/database/tokens/{id} | write | tokens | Updates the existing database token if it is owned by the authorized user and ifthe user has access to the related workspace. |
| DELETE | api/database/tokens/{id} | write | tokens | Deletes the existing database token if it is owned by the authorized user and ifthe user has access to the related workspace. |
| GET | api/trash | read | trash | Responds with the workspaces and applications available for the requesting user to inspect the trash contents of. |
| PATCH | api/trash/restore | write | trash | Restores the specified trashed item back into baserow. |
| GET | api/trash/workspace/{id} | read | trash | Responds with trash contents for a workspace optionally filtered to a specific application. |
| DELETE | api/trash/workspace/{id} | write | trash | Empties the specified workspace and/or application of trash, including the workspace and application themselves if they are trashed also. |
| GET | api/two-factor-auth/configuration | read | two-factor-auth | Returns two-factor auth configuration for the authenticated user. |
| POST | api/two-factor-auth/configuration | write | two-factor-auth | Configures two-factor authentication for the authenticated user. |
| POST | api/two-factor-auth/disable | write | two-factor-auth | Disables two-factor authentication for the authenticated user. |
| POST | api/two-factor-auth/verify | write | two-factor-auth | Verifies TOTP two-factor authentication. |
| POST | api/user | write | user | Creates a new user based on the provided values. |
| PATCH | api/user/account | write | user | Updates the account information of the authenticated user. |
| POST | api/user/change-email | write | user | Changes the email address of a user if the confirmation token is valid. |
| POST | api/user/change-password | write | user | Changes the password of an authenticated user, but only if the old password matches. |
| GET | api/user/dashboard | read | user | Lists all the relevant user information that for example could be shown on a dashboard. |
| PATCH | api/user/preferences | write | user | Changes one or more preferences of the authenticated user, such as the default sort order of a listing page. |
| PATCH | api/user/redo | write | user | Redoes the latest redoable action performed by the user making the request. |
| POST | api/user/reset-password | write | user | Changes the password of a user if the reset token is valid. |
| POST | api/user/schedule-account-deletion | write | user | Schedules the account deletion of the authenticated user. |
| POST | api/user/send-change-email-confirmation | write | user | Sends an email to the new email address containing a confirmation link. |
| POST | api/user/send-reset-password-email | write | user | Sends an email containing the password reset link to the email address of the user. |
| POST | api/user/send-verify-email | write | user | Sends an email to the user with an email verification link if the user's email is not verified yet. |
| POST | api/user/token-auth | write | user | Authenticates an existing user based on their email and their password. |
| POST | api/user/token-blacklist | write | user | Blacklists the provided token. |
| POST | api/user/token-refresh | write | user | Generate a new access_token that can be used to continue operating on Baserow starting from a valid refresh token. |
| POST | api/user/token-verify | write | user | Verifies if the refresh token is valid and can be used to generate a new access_token. |
| PATCH | api/user/undo | write | user | Undoes the latest undoable action performed by the user making the request. |
| POST | api/user/verify-email | write | user | Passing the correct verification token will confirm that the user's email address belongs to the user. |
| POST | api/user-files/upload-file | write | user-files | Uploads a file to Baserow by uploading the file contents directly. |
| POST | api/user-files/upload-via-url | write | user-files | Uploads a file to Baserow by downloading it from the provided URL. |
| POST | api/user-source/sso/saml/acs | write | user-source | Complete the SAML authentication flow by validating the SAML response. |
| PATCH | api/user-source/{id} | write | user-source | Updates an existing user_source. |
| DELETE | api/user-source/{id} | write | user-source | Deletes the user_source related by the given id. |
| POST | api/user-source/{id}/force-token-auth | write | user-source | Force authenticates an existing user based on their ID. |
| PATCH | api/user-source/{id}/move | write | user-source | Moves the user_source in the application before another user_source or at the end of the application if no before user_source is given. |
| GET | api/user-source/{id}/sso/oauth2/openid_connect/callback | write | user-source | Processes callback from OAuth2 provider and logs the user in if successful. Kept out of read: completes a login and sets a session. |
| GET | api/user-source/{id}/sso/oauth2/openid_connect/login | write | user-source | Redirects to the OAuth2 provider's authentication URL based on the provided user source uid and issuer. Kept out of read: starts an OAuth2 login redirect. |
| GET | api/user-source/{id}/sso/saml/login | write | user-source | This is the endpoint that is called when the user wants to initiate a SSO SAML login from Baserow (the service provider). Kept out of read: starts a SAML login redirect. |
| POST | api/user-source/{id}/token-auth | write | user-source | Authenticates an existing user against a user source based on their credentials. |
| POST | api/user-source-auth-refresh | write | user-source-auth-refresh | Generate a new access_token that can be used to continue operating on Baserow with a user source user starting from a valid refresh token. |
| POST | api/user-source-token-blacklist | write | user-source-token-blacklist | Blacklists the provided user source token. |
| GET | api/database/view/get-public-view-export/{id} | read | view | Returns information such as export progress and state or the url of the exported file for the specified export job, only if the requesting user has access. |
| POST | api/database/view/{id}/export-public-view | write | view | Creates and starts a new export job for a publicly shared view  given some exporter options. |
| PATCH | api/database/view/{id}/premium | write | view | Sets view attributes only available for premium users. |
| GET | api/database/views/calendar/{id} | read | views | Responds with serialized rows grouped by date regarding view's date fieldif the user is authenticated and has access to the related workspace. |
| POST | api/database/views/calendar/{id}/ical_slug_rotate | write | views | Rotates the unique slug of the calendar view's ical feed by replacing it with a new value. |
| GET | api/database/views/calendar/{id}/public/rows | read | views | Responds with serialized rows grouped by the view's date field options related to the slug if the calendar view is publicly shared. |
| GET | api/database/views/decoration/{id} | read | views | Returns the existing view decoration if the current user has access to the related database's workspace. |
| PATCH | api/database/views/decoration/{id} | write | views | Updates the existing decoration if the authorized user has access to the related database's workspace. |
| DELETE | api/database/views/decoration/{id} | write | views | Deletes the existing decoration if the authorized user has access to the related database's workspace. |
| GET | api/database/views/filter-group/{id} | read | views | Returns the existing view filter group with the given view_filter_group_id. |
| PATCH | api/database/views/filter-group/{id} | write | views | Updates the existing filter group with the given view_filter_group_id. |
| DELETE | api/database/views/filter-group/{id} | write | views | Deletes the existing filter group with the given view_filter_group_id. |
| GET | api/database/views/filter/{id} | read | views | Returns the existing view filter. |
| PATCH | api/database/views/filter/{id} | write | views | Updates the existing filter. |
| DELETE | api/database/views/filter/{id} | write | views | Deletes the existing filter if the authorized user has access to the related database's workspace. |
| GET | api/database/views/form/{id}/edit-row/{id} | read | views | Returns the current field values of the row identified by the edit token. |
| PATCH | api/database/views/form/{id}/edit-row/{id} | write | views | Updates the row identified by the edit token using the submitted field values. |
| GET | api/database/views/form/{id}/submit | read | views | Returns the metadata related to the form view if the form is publicly shared or if the user has access to the related workspace. |
| POST | api/database/views/form/{id}/submit | write | views | Submits the form if the form is publicly shared or if the user has access to the related workspace. |
| POST | api/database/views/form/{id}/upload-file | write | views | Uploads a file anonymously to Baserow by uploading the file contents directly. |
| GET | api/database/views/gallery/{id} | read | views | Lists the requested rows of the view's table related to the provided view_id if the authorized user has access to the database's workspace. |
| GET | api/database/views/gallery/{id}/public/rows | read | views | Lists the requested rows of the view's table related to the provided slug if the gallery view is public.The response is paginated either by a limit/offset or... |
| GET | api/database/views/grid/{id} | read | views | Lists the requested rows of the view's table related to the provided view_id if the authorized user has access to the database's workspace. |
| POST | api/database/views/grid/{id} | read | views | Lists only the rows and fields that match the request. |
| GET | api/database/views/grid/{id}/aggregation/{id} | read | views | Computes the aggregation of all the values for a specified field from the selected grid view. |
| GET | api/database/views/grid/{id}/aggregations | read | views | Returns all field aggregations values previously defined for this grid view. |
| GET | api/database/views/grid/{id}/group-by-data | read | views | . |
| GET | api/database/views/grid/{id}/public/aggregations | read | views | Returns all field aggregations values previously defined for this grid view. |
| GET | api/database/views/grid/{id}/public/group-by-data | read | views | . |
| GET | api/database/views/grid/{id}/public/rows | read | views | Lists the requested rows of the view's table related to the provided slug if the grid view is public.The response is paginated either by a limit/offset or page/size... |
| GET | api/database/views/group_by/{id} | read | views | Returns the existing view group by if the authorized user has access to the related database's workspace. |
| PATCH | api/database/views/group_by/{id} | write | views | Updates the existing group by if the authorized user has access to the related database's workspace. |
| DELETE | api/database/views/group_by/{id} | write | views | Deletes the existing group by if the authorized user has access to the related database's workspace. |
| GET | api/database/views/kanban/{id} | read | views | Responds with serialized rows grouped by the view's single select field options if the user is authenticated and has access to the related workspace. |
| GET | api/database/views/kanban/{id}/public/rows | read | views | Responds with serialized rows grouped by the view's single select field options related to the slug if the kanban view is publicly shared. |
| GET | api/database/views/sort/{id} | read | views | Returns the existing view sort if the authorized user has access to the related database's workspace. |
| PATCH | api/database/views/sort/{id} | write | views | Updates the existing sort if the authorized user has access to the related database's workspace. |
| DELETE | api/database/views/sort/{id} | write | views | Deletes the existing sort if the authorized user has access to the related database's workspace. |
| GET | api/database/views/table/{id} | read | views | Lists all views of the table related to the provided table_id. |
| POST | api/database/views/table/{id} | write | views | Creates a new view for the table related to the provided table_id parameter. |
| POST | api/database/views/table/{id}/order | write | views | Changes the order of the provided view ids to the matching position that the id has in the list. |
| GET | api/database/views/timeline/{id} | read | views | Lists the requested rows of the view's table related to the provided view_id if the authorized user has access to the database's workspace. |
| GET | api/database/views/timeline/{id}/public/rows | read | views | Lists the requested rows of the view's table related to the provided slug if the timeline view is public.The response is paginated either by a limit/offset or... |
| GET | api/database/views/{id} | read | views | Returns the existing view. |
| PATCH | api/database/views/{id} | write | views | Updates the existing view. |
| DELETE | api/database/views/{id} | write | views | Deletes the existing view. |
| POST | api/database/views/{id}/copy-configuration | write | views | Copies the requested configuration categories, the filters or sorts for example, of another view in the same table into this view, replacing this view's existing... |
| GET | api/database/views/{id}/decorations | read | views | Lists all decorations of the view related to the provided view_id if the user has access to the related database's workspace. |
| POST | api/database/views/{id}/decorations | write | views | Creates a new decoration for the view related to the provided view_id parameter if the authorized user has access to the related database's workspace. |
| PATCH | api/database/views/{id}/default-values | write | views | Updates the default row values for the specified view. |
| POST | api/database/views/{id}/duplicate | write | views | Duplicates an existing view if the user has access to it. |
| GET | api/database/views/{id}/field-options | read | views | Responds with the fields options of the provided view if the authenticated user has access to the related workspace. |
| PATCH | api/database/views/{id}/field-options | write | views | Updates the field options of a view. |
| POST | api/database/views/{id}/filter-groups | write | views | Creates a new filter group for the view related to the provided view_id parameter. |
| GET | api/database/views/{id}/filters | read | views | Lists all filters of the view related to the provided view_id. |
| POST | api/database/views/{id}/filters | write | views | Creates a new filter for the view related to the provided view_id parameter. |
| GET | api/database/views/{id}/group_bys | read | views | Lists all groupings of the view related to the provided view_id if the user has access to the related database's workspace. |
| POST | api/database/views/{id}/group_bys | write | views | Creates a new group by for the view related to the provided view_id parameter if the authorized user has access to the related database's workspace. |
| POST | api/database/views/{id}/group_bys/prioritize | write | views | Updates the priority of the provided view group by ids to the matching position that the id has in the list. |
| GET | api/database/views/{id}/link-row-field-lookup/{id} | read | views | If the view is publicly shared or if an authenticated user has access to the related workspace, then this endpoint can be used to do a value lookup of the link row... |
| POST | api/database/views/{id}/public/auth | write | views | Returns a valid never-expiring JWT token for this public shared view if the password provided matches with the one saved by the view's owner. |
| GET | api/database/views/{id}/public/info | read | views | Returns the required public information to display a single shared view. |
| POST | api/database/views/{id}/rotate-slug | write | views | Rotates the unique slug of the view by replacing it with a new value. |
| GET | api/database/views/{id}/row/{id} | read | views | Returns the data for a specific row in a publicly shared view, identified by the view’s slug and the row’s ID. |
| GET | api/database/views/{id}/sortings | read | views | Lists all sortings of the view related to the provided view_id if the user has access to the related database's workspace. |
| POST | api/database/views/{id}/sortings | write | views | Creates a new sort for the view related to the provided view_id parameter if the authorized user has access to the related database's workspace. |
| POST | api/database/views/{id}/sortings/prioritize | write | views | Updates the priority of the sorts to match the order of the given IDs. |
| GET | api/database/webhooks/table/{id} | read | webhooks | Lists all webhooks of the table related to the provided table_id if the user has access to the related database workspace. |
| POST | api/database/webhooks/table/{id} | write | webhooks | Creates a new webhook for the table related to the provided table_id parameter if the authorized user has access to the related database workspace. |
| POST | api/database/webhooks/table/{id}/test-call | write | webhooks | This endpoint triggers a test call based on the provided data if the user has access to the workspace related to the table. |
| GET | api/database/webhooks/{id} | read | webhooks | Returns the existing webhook if the authorized user has access to the related database workspace. |
| PATCH | api/database/webhooks/{id} | write | webhooks | Updates the existing view if the authorized user has access to the related database workspace. |
| DELETE | api/database/webhooks/{id} | write | webhooks | Deletes the existing webhook if the authorized user has access to the related database's workspace. |
| GET | api/webhooks/{id} | read | webhooks | Receives and handles a webhook request. |
| POST | api/webhooks/{id} | write | webhooks | Receives and handles a webhook request. |
| PUT | api/webhooks/{id} | write | webhooks | Receives and handles a webhook request. |
| PATCH | api/webhooks/{id} | write | webhooks | Receives and handles a webhook request. |
| DELETE | api/webhooks/{id} | write | webhooks | Receives and handles a webhook request. |
| PATCH | api/database/workflow_action/{id} | write | workflow_action | Updates an existing database workflow action. |
| DELETE | api/database/workflow_action/{id} | write | workflow_action | Deletes the workflow action related by the given id. |
| GET | api/workspaces | read | workspaces | Lists all the workspaces of the authorized user. |
| POST | api/workspaces | write | workspaces | Creates a new workspace where only the authorized user has access to. |
| POST | api/workspaces/create-initial-workspace | write | workspaces | Creates an initial workspace. |
| GET | api/workspaces/invitation-links/slug/{id} | read | workspaces | Responds with the workspace and the inviter of the invitation link with the provided slug, so that someone who opens the link knows what they join. |
| POST | api/workspaces/invitation-links/slug/{id}/join | write | workspaces | Adds the authorized user to the workspace of the invitation link with the permissions of the link. |
| GET | api/workspaces/invitation-links/workspace/{id} | read | workspaces | Lists all the invitation links of the workspace related to the provided workspace_id parameter if the authorized user has admin rights to that workspace. |
| POST | api/workspaces/invitation-links/workspace/{id} | write | workspaces | Creates a new permanent invitation link if the authorized user has admin rights to the related workspace. |
| PATCH | api/workspaces/invitation-links/{id} | write | workspaces | Updates the name of the invitation link or the permissions people get when joining through it if the authorized user has admin rights to the related workspace. |
| DELETE | api/workspaces/invitation-links/{id} | write | workspaces | Deletes an invitation link if the authorized user has admin rights to the related workspace. |
| GET | api/workspaces/invitations/token/{id} | read | workspaces | Responds with the serialized workspace invitation if an invitation with the provided token is found. |
| GET | api/workspaces/invitations/workspace/{id} | read | workspaces | Lists all the workspace invitations of the workspace related to the provided workspace_id parameter if the authorized user has admin rights to that workspace. |
| POST | api/workspaces/invitations/workspace/{id} | write | workspaces | Creates a new workspace invitations for an email address if the authorized user has admin rights to the related workspace. |
| GET | api/workspaces/invitations/{id} | read | workspaces | Returns the requested workspace invitation if the authorized user has admin right to the related workspace. |
| PATCH | api/workspaces/invitations/{id} | write | workspaces | Updates the existing workspace invitation related to the provided workspace_invitation_id param if the authorized user has admin rights to the related workspace. |
| DELETE | api/workspaces/invitations/{id} | write | workspaces | Deletes a workspace invitation if the authorized user has admin rights to the related workspace. |
| POST | api/workspaces/invitations/{id}/accept | write | workspaces | Accepts a workspace invitation with the given id if the email address of the user matches that of the invitation. |
| POST | api/workspaces/invitations/{id}/reject | write | workspaces | Rejects a workspace invitation with the given id if the email address of the user matches that of the invitation. |
| POST | api/workspaces/order | write | workspaces | Changes the order of the provided workspace ids to the matching position that the id has in the list. |
| GET | api/workspaces/users/workspace/{id} | read | workspaces | Lists all the users that are in a workspace if the authorized user has admin permissions to the related workspace. |
| PATCH | api/workspaces/users/{id} | write | workspaces | Updates the existing workspace user related to the provided workspace_user_id param if the authorized user has admin rights to the related workspace. |
| DELETE | api/workspaces/users/{id} | write | workspaces | Deletes a workspace user if the authorized user has admin rights to the related workspace. |
| PATCH | api/workspaces/{id} | write | workspaces | Updates the existing workspace related to the provided workspace_id parameter if the authorized user belongs to the workspace. |
| DELETE | api/workspaces/{id} | write | workspaces | Deletes an existing workspace if the authorized user belongs to the workspace. |
| GET | api/workspaces/{id}/export | read | workspaces | Lists exports that were created for given workspace. |
| POST | api/workspaces/{id}/export/async | write | workspaces | Export workspace or set of applications application if the authorized user is in the application's workspace. |
| POST | api/workspaces/{id}/import/async | write | workspaces | Import a set of applications included in a given resource if the authorized user is in the specified workspace. |
| POST | api/workspaces/{id}/import/upload-file | write | workspaces | Uploads an exported workspace or a set of applications if the authorized user is in the workspace. |
| DELETE | api/workspaces/{id}/import/{id} | write | workspaces | Delete a resource. |
| POST | api/workspaces/{id}/leave | write | workspaces | Makes the authenticated user leave the workspace related to the provided workspace_id if the user is in that workspace. |
| GET | api/workspaces/{id}/permissions | read | workspaces | Returns a the permission data necessary to determine the permissions of a specific user over a specific workspace. |
