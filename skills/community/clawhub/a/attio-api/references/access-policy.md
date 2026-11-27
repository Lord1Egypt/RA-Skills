# Attio access policy

An access policy limits which endpoints Attio connections may call through Maton. Attio doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/attio#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Attio: its 47 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create attio --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v2/activities"},
    {"method": "GET", "path": "v2/activities/{id}"},
    {"method": "POST", "path": "v2/activities/{id}/records/query"},
    {"method": "GET", "path": "v2/activities/{id}/records/{id}"},
    {"method": "GET", "path": "v2/{id}/{id}/attributes"},
    {"method": "GET", "path": "v2/{id}/{id}/attributes/{id}"},
    {"method": "GET", "path": "v2/{id}/{id}/attributes/{id}/options"},
    {"method": "GET", "path": "v2/{id}/{id}/attributes/{id}/statuses"},
    {"method": "GET", "path": "v2/meetings/{id}/call_recordings"},
    {"method": "GET", "path": "v2/meetings/{id}/call_recordings/{id}"},
    {"method": "GET", "path": "v2/comments/{id}"},
    {"method": "GET", "path": "v2/emails"},
    {"method": "POST", "path": "v2/lists/{id}/entries/query"},
    {"method": "GET", "path": "v2/lists/{id}/entries/{id}"},
    {"method": "GET", "path": "v2/lists/{id}/entries/{id}/attributes/{id}/values"},
    {"method": "GET", "path": "v2/files"},
    {"method": "GET", "path": "v2/files/{id}"},
    {"method": "GET", "path": "v2/files/{id}/download"},
    {"method": "GET", "path": "v2/lists"},
    {"method": "GET", "path": "v2/lists/{id}"},
    {"method": "GET", "path": "v2/meetings"},
    {"method": "GET", "path": "v2/meetings/{id}"},
    {"method": "GET", "path": "v2/self"},
    {"method": "GET", "path": "v2/notes"},
    {"method": "GET", "path": "v2/notes/{id}"},
    {"method": "GET", "path": "v2/objects"},
    {"method": "GET", "path": "v2/objects/{id}"},
    {"method": "POST", "path": "v2/objects/records/search"},
    {"method": "POST", "path": "v2/objects/{id}/records/query"},
    {"method": "GET", "path": "v2/objects/{id}/records/{id}"},
    {"method": "GET", "path": "v2/objects/{id}/records/{id}/attributes/{id}/values"},
    {"method": "GET", "path": "v2/objects/{id}/records/{id}/entries"},
    {"method": "POST", "path": "v2/sql"},
    {"method": "GET", "path": "v2/tasks"},
    {"method": "GET", "path": "v2/tasks/{id}"},
    {"method": "GET", "path": "v2/threads"},
    {"method": "GET", "path": "v2/threads/{id}"},
    {"method": "GET", "path": "v2/meetings/{id}/call_recordings/{id}/transcript"},
    {"method": "GET", "path": "v2/lists/{id}/views"},
    {"method": "GET", "path": "v2/lists/{id}/views/{id}"},
    {"method": "GET", "path": "v2/objects/{id}/views"},
    {"method": "GET", "path": "v2/objects/{id}/views/{id}"},
    {"method": "GET", "path": "v2/webhooks"},
    {"method": "GET", "path": "v2/webhooks/{id}"},
    {"method": "GET", "path": "v2/workspace_blocklist_addresses"},
    {"method": "GET", "path": "v2/workspace_members"},
    {"method": "GET", "path": "v2/workspace_members/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Attio endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v2/activities | read | activities | List activities. |
| POST | v2/activities | write | activities | Create an activity. |
| GET | v2/activities/{id} | read | activities | Get an activity. |
| PATCH | v2/activities/{id} | write | activities | Update an activity. |
| DELETE | v2/activities/{id} | write | activities | Delete an activity. |
| POST | v2/activities/{id}/records | write | activity records | Create an activity record. |
| PUT | v2/activities/{id}/records | write | activity records | Upsert an activity record. |
| POST | v2/activities/{id}/records/query | read | activity records | List activity records. |
| GET | v2/activities/{id}/records/{id} | read | activity records | Get an activity record. |
| PUT | v2/activities/{id}/records/{id} | write | activity records | Update an activity record (overwrite multiselect values). |
| PATCH | v2/activities/{id}/records/{id} | write | activity records | Update an activity record (append multiselect values). |
| DELETE | v2/activities/{id}/records/{id} | write | activity records | Delete an activity record. |
| GET | v2/{id}/{id}/attributes | read | attributes | List attributes. |
| POST | v2/{id}/{id}/attributes | write | attributes | Create an attribute. |
| GET | v2/{id}/{id}/attributes/{id} | read | attributes | Get an attribute. |
| PATCH | v2/{id}/{id}/attributes/{id} | write | attributes | Update an attribute. |
| GET | v2/{id}/{id}/attributes/{id}/options | read | attributes | List select options. |
| POST | v2/{id}/{id}/attributes/{id}/options | write | attributes | Create a select option. |
| PATCH | v2/{id}/{id}/attributes/{id}/options/{id} | write | attributes | Update a select option. |
| GET | v2/{id}/{id}/attributes/{id}/statuses | read | attributes | List statuses. |
| POST | v2/{id}/{id}/attributes/{id}/statuses | write | attributes | Create a status. |
| PATCH | v2/{id}/{id}/attributes/{id}/statuses/{id} | write | attributes | Update a status. |
| GET | v2/meetings/{id}/call_recordings | read | call recordings | List call recordings. |
| POST | v2/meetings/{id}/call_recordings | write | call recordings | Create call recording. |
| GET | v2/meetings/{id}/call_recordings/{id} | read | call recordings | Get call recording. |
| DELETE | v2/meetings/{id}/call_recordings/{id} | write | call recordings | Delete call recording. |
| POST | v2/comments | write | comments | Create a comment. |
| GET | v2/comments/{id} | read | comments | Get a comment. |
| DELETE | v2/comments/{id} | write | comments | Delete a comment. |
| GET | v2/emails | read | emails | List emails. |
| POST | v2/lists/{id}/entries | write | entries | Create an entry (add record to list). |
| PUT | v2/lists/{id}/entries | write | entries | Upsert a list entry by parent. |
| POST | v2/lists/{id}/entries/query | read | entries | List entries. |
| GET | v2/lists/{id}/entries/{id} | read | entries | Get a list entry. |
| PUT | v2/lists/{id}/entries/{id} | write | entries | Update a list entry (overwrite multiselect values). |
| PATCH | v2/lists/{id}/entries/{id} | write | entries | Update a list entry (append multiselect values). |
| DELETE | v2/lists/{id}/entries/{id} | write | entries | Delete a list entry. |
| GET | v2/lists/{id}/entries/{id}/attributes/{id}/values | read | entries | List attribute values for a list entry. |
| PUT | v2/lists/{id}/entries/{id}/attributes/{id}/values | write | entries | Write list entry attribute values. |
| GET | v2/files | read | files | List files. |
| POST | v2/files | write | files | Create a folder. |
| POST | v2/files/upload | write | files | Upload a file. |
| GET | v2/files/{id} | read | files | Get a file. |
| DELETE | v2/files/{id} | write | files | Delete a file. |
| GET | v2/files/{id}/download | read | files | Download a file. |
| GET | v2/lists | read | lists | List all lists. |
| POST | v2/lists | write | lists | Create a list. |
| GET | v2/lists/{id} | read | lists | Get a list. |
| PATCH | v2/lists/{id} | write | lists | Update a list. |
| GET | v2/meetings | read | meetings | List meetings. |
| POST | v2/meetings | write | meetings | Create a meeting. |
| GET | v2/meetings/{id} | read | meetings | Get a meeting. |
| PUT | v2/meetings/{id} | write | meetings | Update a meeting (overwrite linked records). |
| PATCH | v2/meetings/{id} | write | meetings | Update a meeting (append linked records). |
| DELETE | v2/meetings/{id} | write | meetings | Delete a meeting. |
| GET | v2/self | read | meta | Identify. |
| GET | v2/notes | read | notes | List notes. |
| POST | v2/notes | write | notes | Create a note. |
| GET | v2/notes/{id} | read | notes | Get a note. |
| PATCH | v2/notes/{id} | write | notes | Update a note. |
| DELETE | v2/notes/{id} | write | notes | Delete a note. |
| GET | v2/objects | read | objects | List objects. |
| POST | v2/objects | write | objects | Create an object. |
| GET | v2/objects/{id} | read | objects | Get an object. |
| PATCH | v2/objects/{id} | write | objects | Update an object. |
| DELETE | v2/objects/{id} | write | objects | Delete an object. |
| POST | v2/objects/records/search | read | records | Search records. |
| POST | v2/objects/{id}/records | write | records | Create a record. |
| PUT | v2/objects/{id}/records | write | records | Upsert a record. |
| POST | v2/objects/{id}/records/merge | write | records | Merge two records. |
| POST | v2/objects/{id}/records/query | read | records | List records. |
| GET | v2/objects/{id}/records/{id} | read | records | Get a record. |
| PUT | v2/objects/{id}/records/{id} | write | records | Update a record (overwrite multiselect values). |
| PATCH | v2/objects/{id}/records/{id} | write | records | Update a record (append multiselect values). |
| DELETE | v2/objects/{id}/records/{id} | write | records | Delete a record. |
| GET | v2/objects/{id}/records/{id}/attributes/{id}/values | read | records | List record attribute values. |
| PUT | v2/objects/{id}/records/{id}/attributes/{id}/values | write | records | Write record attribute values. |
| GET | v2/objects/{id}/records/{id}/entries | read | records | List record entries. |
| POST | v2/sequences/unsubscribed_emails | write | sequences | Add emails to the unsubscribe list. |
| POST | v2/sql | read | sql | Query SQL. |
| GET | v2/tasks | read | tasks | List tasks. |
| POST | v2/tasks | write | tasks | Create a task. |
| GET | v2/tasks/{id} | read | tasks | Get a task. |
| PATCH | v2/tasks/{id} | write | tasks | Update a task. |
| DELETE | v2/tasks/{id} | write | tasks | Delete a task. |
| GET | v2/threads | read | threads | List threads. |
| GET | v2/threads/{id} | read | threads | Get a thread and its comments. |
| GET | v2/meetings/{id}/call_recordings/{id}/transcript | read | transcripts | Deprecated: Get call transcript. |
| GET | v2/lists/{id}/views | read | views | List views for list. |
| POST | v2/lists/{id}/views | write | views | Create a list view. |
| GET | v2/lists/{id}/views/{id} | read | views | Get a list view. |
| PATCH | v2/lists/{id}/views/{id} | write | views | Update a list view. |
| DELETE | v2/lists/{id}/views/{id} | write | views | Delete a list view. |
| GET | v2/objects/{id}/views | read | views | List views for object. |
| POST | v2/objects/{id}/views | write | views | Create an object view. |
| GET | v2/objects/{id}/views/{id} | read | views | Get an object view. |
| PATCH | v2/objects/{id}/views/{id} | write | views | Update an object view. |
| DELETE | v2/objects/{id}/views/{id} | write | views | Delete an object view. |
| GET | v2/webhooks | read | webhooks | List webhooks. |
| POST | v2/webhooks | write | webhooks | Create a webhook. |
| GET | v2/webhooks/{id} | read | webhooks | Get a webhook. |
| PATCH | v2/webhooks/{id} | write | webhooks | Update a webhook. |
| DELETE | v2/webhooks/{id} | write | webhooks | Delete a webhook. |
| GET | v2/workspace_blocklist_addresses | read | workspace blocklist | List workspace blocklist addresses. |
| PUT | v2/workspace_blocklist_addresses | write | workspace blocklist | Add or update workspace blocklist addresses. |
| DELETE | v2/workspace_blocklist_addresses/{id} | write | workspace blocklist | Delete a workspace blocklist address. |
| GET | v2/workspace_members | read | workspace members | List workspace members. |
| GET | v2/workspace_members/{id} | read | workspace members | Get a workspace member. |
