# ClickUp access policy

An access policy limits which endpoints ClickUp connections may call through Maton. ClickUp doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/clickup#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for ClickUp: its 50 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create clickup --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v2/user"},
    {"method": "GET", "path": "api/v2/comment/{id}/reply"},
    {"method": "GET", "path": "api/v2/list/{id}/comment"},
    {"method": "GET", "path": "api/v2/task/{id}/comment"},
    {"method": "GET", "path": "api/v2/view/{id}/comment"},
    {"method": "GET", "path": "api/v2/folder/{id}/field"},
    {"method": "GET", "path": "api/v2/list/{id}/field"},
    {"method": "GET", "path": "api/v2/space/{id}/field"},
    {"method": "GET", "path": "api/v2/team/{id}/field"},
    {"method": "GET", "path": "api/v2/team/{id}/custom_item"},
    {"method": "GET", "path": "api/v2/folder/{id}"},
    {"method": "GET", "path": "api/v2/space/{id}/folder"},
    {"method": "GET", "path": "api/v2/goal/{id}"},
    {"method": "GET", "path": "api/v2/team/{id}/goal"},
    {"method": "GET", "path": "api/v2/team/{id}/guest/{id}"},
    {"method": "GET", "path": "api/v2/folder/{id}/list"},
    {"method": "GET", "path": "api/v2/list/{id}"},
    {"method": "GET", "path": "api/v2/space/{id}/list"},
    {"method": "GET", "path": "api/v2/list/{id}/member"},
    {"method": "GET", "path": "api/v2/task/{id}/member"},
    {"method": "GET", "path": "api/v2/team/{id}/customroles"},
    {"method": "GET", "path": "api/v2/team/{id}/shared"},
    {"method": "GET", "path": "api/v2/space/{id}"},
    {"method": "GET", "path": "api/v2/team/{id}/space"},
    {"method": "GET", "path": "api/v2/space/{id}/tag"},
    {"method": "GET", "path": "api/v2/list/{id}/task"},
    {"method": "GET", "path": "api/v2/task/bulk_time_in_status/task_ids"},
    {"method": "GET", "path": "api/v2/task/{id}"},
    {"method": "GET", "path": "api/v2/task/{id}/time_in_status"},
    {"method": "GET", "path": "api/v2/team/{id}/task"},
    {"method": "GET", "path": "api/v2/team/{id}/folder_template"},
    {"method": "GET", "path": "api/v2/team/{id}/list_template"},
    {"method": "GET", "path": "api/v2/team/{id}/taskTemplate"},
    {"method": "GET", "path": "api/v2/team/{id}/time_entries"},
    {"method": "GET", "path": "api/v2/team/{id}/time_entries/current"},
    {"method": "GET", "path": "api/v2/team/{id}/time_entries/tags"},
    {"method": "GET", "path": "api/v2/team/{id}/time_entries/{id}"},
    {"method": "GET", "path": "api/v2/team/{id}/time_entries/{id}/history"},
    {"method": "GET", "path": "api/v2/task/{id}/time"},
    {"method": "GET", "path": "api/v2/group"},
    {"method": "GET", "path": "api/v2/team/{id}/user/{id}"},
    {"method": "GET", "path": "api/v2/folder/{id}/view"},
    {"method": "GET", "path": "api/v2/list/{id}/view"},
    {"method": "GET", "path": "api/v2/space/{id}/view"},
    {"method": "GET", "path": "api/v2/team/{id}/view"},
    {"method": "GET", "path": "api/v2/view/{id}"},
    {"method": "GET", "path": "api/v2/view/{id}/task"},
    {"method": "GET", "path": "api/v2/team"},
    {"method": "GET", "path": "api/v2/team/{id}/plan"},
    {"method": "GET", "path": "api/v2/team/{id}/seats"}
  ],
  "deny": []
}
```

## Endpoints

The ClickUp endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | api/v2/task/{id}/attachment | write | attachments | Create Task Attachment. |
| POST | api/v2/oauth/token | write | authorization | Get Access Token. |
| GET | api/v2/user | read | authorization | Get Authorized User. |
| PUT | api/v2/comment/{id} | write | comments | Update Comment. |
| DELETE | api/v2/comment/{id} | write | comments | Delete Comment. |
| GET | api/v2/comment/{id}/reply | read | comments | Get Threaded Comments. |
| POST | api/v2/comment/{id}/reply | write | comments | Create Threaded Comment. |
| GET | api/v2/list/{id}/comment | read | comments | Get List Comments. |
| POST | api/v2/list/{id}/comment | write | comments | Create List Comment. |
| GET | api/v2/task/{id}/comment | read | comments | Get Task Comments. |
| POST | api/v2/task/{id}/comment | write | comments | Create Task Comment. |
| GET | api/v2/view/{id}/comment | read | comments | Get Chat View Comments. |
| POST | api/v2/view/{id}/comment | write | comments | Create Chat View Comment. |
| GET | api/v2/folder/{id}/field | read | custom-fields | Get Folder Custom Fields. |
| GET | api/v2/list/{id}/field | read | custom-fields | Get List Custom Fields. |
| GET | api/v2/space/{id}/field | read | custom-fields | Get Space Custom Fields. |
| POST | api/v2/task/{id}/field/{id} | write | custom-fields | Set Custom Field Value. |
| DELETE | api/v2/task/{id}/field/{id} | write | custom-fields | Remove Custom Field Value. |
| GET | api/v2/team/{id}/field | read | custom-fields | Get Workspace Custom Fields. |
| GET | api/v2/team/{id}/custom_item | read | custom-task-types | Get Custom Task Types. |
| GET | api/v2/folder/{id} | read | folders | Get Folder. |
| PUT | api/v2/folder/{id} | write | folders | Update Folder. |
| DELETE | api/v2/folder/{id} | write | folders | Delete Folder. |
| PUT | api/v2/folder/{id}/position | write | folders | Move Folder. |
| GET | api/v2/space/{id}/folder | read | folders | Get Folders. |
| POST | api/v2/space/{id}/folder | write | folders | Create Folder. |
| POST | api/v2/space/{id}/folder_template/{id} | write | folders | Create Folder from template. |
| GET | api/v2/goal/{id} | read | goals | Get Goal. |
| PUT | api/v2/goal/{id} | write | goals | Update Goal. |
| DELETE | api/v2/goal/{id} | write | goals | Delete Goal. |
| POST | api/v2/goal/{id}/key_result | write | goals | Create Key Result. |
| PUT | api/v2/key_result/{id} | write | goals | Edit Key Result. |
| DELETE | api/v2/key_result/{id} | write | goals | Delete Key Result. |
| GET | api/v2/team/{id}/goal | read | goals | Get Goals. |
| POST | api/v2/team/{id}/goal | write | goals | Create Goal. |
| POST | api/v2/folder/{id}/guest/{id} | write | guests | Add Guest To Folder. |
| DELETE | api/v2/folder/{id}/guest/{id} | write | guests | Remove Guest From Folder. |
| POST | api/v2/list/{id}/guest/{id} | write | guests | Add Guest To List. |
| DELETE | api/v2/list/{id}/guest/{id} | write | guests | Remove Guest From List. |
| POST | api/v2/task/{id}/guest/{id} | write | guests | Add Guest To Task. |
| DELETE | api/v2/task/{id}/guest/{id} | write | guests | Remove Guest From Task. |
| POST | api/v2/team/{id}/guest | write | guests | Invite Guest To Workspace. |
| GET | api/v2/team/{id}/guest/{id} | read | guests | Get Guest. |
| PUT | api/v2/team/{id}/guest/{id} | write | guests | Edit Guest On Workspace. |
| DELETE | api/v2/team/{id}/guest/{id} | write | guests | Remove Guest From Workspace. |
| GET | api/v2/folder/{id}/list | read | lists | Get Lists. |
| POST | api/v2/folder/{id}/list | write | lists | Create List. |
| POST | api/v2/folder/{id}/list_template/{id} | write | lists | Create List From Template in Folder. |
| GET | api/v2/list/{id} | read | lists | Get List. |
| PUT | api/v2/list/{id} | write | lists | Update List. |
| DELETE | api/v2/list/{id} | write | lists | Delete List. |
| POST | api/v2/list/{id}/task/{id} | write | lists | Add Task To List. |
| DELETE | api/v2/list/{id}/task/{id} | write | lists | Remove Task From List. |
| GET | api/v2/space/{id}/list | read | lists | Get Folderless Lists. |
| POST | api/v2/space/{id}/list | write | lists | Create Folderless List. |
| POST | api/v2/space/{id}/list_template/{id} | write | lists | Create List From Template in Space. |
| GET | api/v2/list/{id}/member | read | members | Get List Members. |
| GET | api/v2/task/{id}/member | read | members | Get Task Members. |
| GET | api/v2/team/{id}/customroles | read | roles | Get Custom Roles. |
| GET | api/v2/team/{id}/shared | read | shared-hierarchy | Shared Hierarchy. |
| GET | api/v2/space/{id} | read | spaces | Get Space. |
| PUT | api/v2/space/{id} | write | spaces | Update Space. |
| DELETE | api/v2/space/{id} | write | spaces | Delete Space. |
| GET | api/v2/team/{id}/space | read | spaces | Get Spaces. |
| POST | api/v2/team/{id}/space | write | spaces | Create Space. |
| GET | api/v2/space/{id}/tag | read | tags | Get Space Tags. |
| POST | api/v2/space/{id}/tag | write | tags | Create Space Tag. |
| PUT | api/v2/space/{id}/tag/{id} | write | tags | Edit Space Tag. |
| DELETE | api/v2/space/{id}/tag/{id} | write | tags | Delete Space Tag. |
| POST | api/v2/task/{id}/tag/{id} | write | tags | Add Tag To Task. |
| DELETE | api/v2/task/{id}/tag/{id} | write | tags | Remove Tag From Task. |
| PUT | api/v2/checklist/{id} | write | task-checklists | Edit Checklist. |
| DELETE | api/v2/checklist/{id} | write | task-checklists | Delete Checklist. |
| POST | api/v2/checklist/{id}/checklist_item | write | task-checklists | Create Checklist Item. |
| PUT | api/v2/checklist/{id}/checklist_item/{id} | write | task-checklists | Edit Checklist Item. |
| DELETE | api/v2/checklist/{id}/checklist_item/{id} | write | task-checklists | Delete Checklist Item. |
| POST | api/v2/task/{id}/checklist | write | task-checklists | Create Checklist. |
| POST | api/v2/task/{id}/dependency | write | task-relationships | Add Dependency. |
| DELETE | api/v2/task/{id}/dependency | write | task-relationships | Delete Dependency. |
| POST | api/v2/task/{id}/link/{id} | write | task-relationships | Add Task Link. |
| DELETE | api/v2/task/{id}/link/{id} | write | task-relationships | Delete Task Link. |
| GET | api/v2/list/{id}/task | read | tasks | Get Tasks. |
| POST | api/v2/list/{id}/task | write | tasks | Create Task. |
| POST | api/v2/list/{id}/taskTemplate/{id} | write | tasks | Create Task From Template. |
| GET | api/v2/task/bulk_time_in_status/task_ids | read | tasks | Get Bulk Tasks' Time in Status. |
| GET | api/v2/task/{id} | read | tasks | Get Task. |
| PUT | api/v2/task/{id} | write | tasks | Update Task. |
| DELETE | api/v2/task/{id} | write | tasks | Delete Task. |
| POST | api/v2/task/{id}/merge | write | tasks | Merge Tasks. |
| GET | api/v2/task/{id}/time_in_status | read | tasks | Get Task's Time in Status. |
| GET | api/v2/team/{id}/task | read | tasks | Get Filtered Team Tasks. |
| GET | api/v2/team/{id}/folder_template | read | templates | Get Folder Templates. |
| GET | api/v2/team/{id}/list_template | read | templates | Get List Templates. |
| GET | api/v2/team/{id}/taskTemplate | read | templates | Get Task Templates. |
| GET | api/v2/team/{id}/time_entries | read | time-tracking | Get time entries within a date range. |
| POST | api/v2/team/{id}/time_entries | write | time-tracking | Create a time entry. |
| GET | api/v2/team/{id}/time_entries/current | read | time-tracking | Get running time entry. |
| POST | api/v2/team/{id}/time_entries/start | write | time-tracking | Start a time Entry. |
| POST | api/v2/team/{id}/time_entries/stop | write | time-tracking | Stop a time Entry. |
| GET | api/v2/team/{id}/time_entries/tags | read | time-tracking | Get all tags from time entries. |
| POST | api/v2/team/{id}/time_entries/tags | write | time-tracking | Add tags from time entries. |
| PUT | api/v2/team/{id}/time_entries/tags | write | time-tracking | Change tag names from time entries. |
| DELETE | api/v2/team/{id}/time_entries/tags | write | time-tracking | Remove tags from time entries. |
| GET | api/v2/team/{id}/time_entries/{id} | read | time-tracking | Get singular time entry. |
| PUT | api/v2/team/{id}/time_entries/{id} | write | time-tracking | Update a time Entry. |
| DELETE | api/v2/team/{id}/time_entries/{id} | write | time-tracking | Delete a time Entry. |
| GET | api/v2/team/{id}/time_entries/{id}/history | read | time-tracking | Get time entry history. |
| GET | api/v2/task/{id}/time | read | time-tracking-legacy | Get tracked time. |
| POST | api/v2/task/{id}/time | write | time-tracking-legacy | Track time. |
| PUT | api/v2/task/{id}/time/{id} | write | time-tracking-legacy | Edit time tracked. |
| DELETE | api/v2/task/{id}/time/{id} | write | time-tracking-legacy | Delete time tracked. |
| GET | api/v2/group | read | user-groups | Get Groups. |
| PUT | api/v2/group/{id} | write | user-groups | Update Group. |
| DELETE | api/v2/group/{id} | write | user-groups | Delete Group. |
| POST | api/v2/team/{id}/group | write | user-groups | Create Group. |
| POST | api/v2/team/{id}/user | write | users | Invite User To Workspace. |
| GET | api/v2/team/{id}/user/{id} | read | users | Get User. |
| PUT | api/v2/team/{id}/user/{id} | write | users | Edit User On Workspace. |
| DELETE | api/v2/team/{id}/user/{id} | write | users | Remove User From Workspace. |
| GET | api/v2/folder/{id}/view | read | views | Get Folder Views. |
| POST | api/v2/folder/{id}/view | write | views | Create Folder View. |
| GET | api/v2/list/{id}/view | read | views | Get List Views. |
| POST | api/v2/list/{id}/view | write | views | Create List View. |
| GET | api/v2/space/{id}/view | read | views | Get Space Views. |
| POST | api/v2/space/{id}/view | write | views | Create Space View. |
| GET | api/v2/team/{id}/view | read | views | Get Workspace (Everything level) Views. |
| POST | api/v2/team/{id}/view | write | views | Create Workspace (Everything level) View. |
| GET | api/v2/view/{id} | read | views | Get View. |
| PUT | api/v2/view/{id} | write | views | Update View. |
| DELETE | api/v2/view/{id} | write | views | Delete View. |
| GET | api/v2/view/{id}/task | read | views | Get View Tasks. |
| GET | api/v2/team/{id}/webhook | write | webhooks | Get Webhooks. Kept out of read: webhook objects include the signing secret. |
| POST | api/v2/team/{id}/webhook | write | webhooks | Create Webhook. |
| PUT | api/v2/webhook/{id} | write | webhooks | Update Webhook. |
| DELETE | api/v2/webhook/{id} | write | webhooks | Delete Webhook. |
| GET | api/v2/team | read | workspaces | Get Authorized Workspaces. |
| GET | api/v2/team/{id}/plan | read | workspaces | Get Workspace Plan. |
| GET | api/v2/team/{id}/seats | read | workspaces | Get Workspace seats. |
