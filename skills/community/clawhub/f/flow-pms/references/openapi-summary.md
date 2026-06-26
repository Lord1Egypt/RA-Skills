# FlowBoard API summary

Base URL:
- `https://mycivgjuujlnyoycuwrz.supabase.co/functions/v1/api-gateway`

Authentication:
- Header: `Authorization: Bearer <api-key>`
- Token source for this skill: explicit argument or `FLOWBOARD_API_KEY`

## Projects

### GET /projects
List projects.

Query params:
- `limit` integer, default 50, max 200
- `offset` integer, default 0
- `status` one of `briefing | planning | in_progress | review | completed | post_launch | on_hold | continuous_support | archived`

### POST /projects
Create project.

Body:
- required: `name`, `prefix`
- optional: `description`, `color`, `icon`, `status`, `deadline`, `client_name`, `client_email`

### GET /projects/{id}
Get project by UUID.

### PATCH /projects/{id}
Update project.

Allowed fields:
- `name`, `description`, `color`, `icon`, `status`, `deadline`, `client_name`, `client_email`, `client_phone`, `client_website`, `client_address`, `client_notes`

### DELETE /projects/{id}
Delete project permanently.

### POST /projects/{id}/archive
Archive project.

### POST /projects/{id}/unarchive
Unarchive project, restoring it to `on_hold`.

## Cycles

### GET /projects/{projectId}/cycles
List cycles for a project.

Query params:
- `limit` integer, default 50, max 200
- `offset` integer, default 0

### POST /projects/{projectId}/cycles
Create cycle.

Body:
- required: `name`
- optional: `description`, `start_date`, `end_date`, `status`

### GET /cycles/{id}
Get cycle by UUID.

### PATCH /cycles/{id}
Update cycle.

Allowed fields:
- `name`, `description`, `start_date`, `end_date`, `status`

### DELETE /cycles/{id}
Delete cycle.

Cycle statuses:
- `draft`
- `active`
- `completed`
- `cancelled`

Cycle summary fields often useful to surface:
- `progress`
- `scope`
- `completed_scope`
- `cycle_number`
- `start_date`
- `end_date`

## Tasks

### GET /projects/{projectId}/tasks
List tasks for a project.

Query params:
- `limit` integer, default 50, max 200
- `offset` integer, default 0
- `status` one of `backlog | todo | in_progress | in_review | done | cancelled`
- `priority` one of `none | low | medium | high | urgent`
- `cycle_id` UUID
- `assignee_id` UUID

### POST /projects/{projectId}/tasks
Create task.

Body:
- required: `title`
- optional: `description`, `status`, `priority`, `type`, `due_date`, `assignee_id`, `cycle_id`, `estimate`, `parent_id`

### GET /tasks/{id}
Get task by UUID.

### PATCH /tasks/{id}
Update task.

Allowed fields:
- `title`, `description`, `status`, `priority`, `type`, `due_date`, `assignee_id`, `cycle_id`, `estimate`, `parent_id`, `hidden_from_customer`

### DELETE /tasks/{id}
Delete task.

Task statuses:
- `backlog`
- `todo`
- `in_progress`
- `in_review`
- `done`
- `cancelled`

Task priorities:
- `none`
- `low`
- `medium`
- `high`
- `urgent`

Task types:
- `feature`
- `bug`
- `improvement`
- `task`

Useful task fields:
- `id`
- `identifier` like `PRJ-42`
- `title`
- `description`
- `status`
- `priority`
- `type`
- `due_date`
- `assignee_id`
- `cycle_id`
- `estimate`
- `parent_id`
- `hidden_from_customer`

## Common responses

Success list shape:
- `data`: array
- `meta.total`
- `meta.limit`
- `meta.offset`

Success single-resource shape:
- `data`: object

Delete success shape:
- `success: true`

Error shape:
- `error: string`

Common error cases:
- `401` invalid, missing, or revoked API key
- `404` resource not found or outside workspace
- `400` invalid request body
