# ClickUp Operator Configuration

This package treats ClickUp operating behavior as reusable logic plus a thin user-specific config layer.

## Required config

### Workspace defaults

- `workspace_id`
- `workspace_name`
- `default_space_name`

### General list defaults

- `general_todo_list_id`
- `general_todo_list_name`
- `ideas_list_id`
- `ideas_list_name`

### Assignee defaults

- `default_assignee_id`
- `default_assignee_name`

### Read filters

- `active_statuses`
- `include_completed_by_default`

### Policy defaults

- `default_general_todo_due_date`
- `project_items_auto_assign`
- `project_items_auto_due_date`
- `ideas_auto_assign`

## Optional config

- known workspace mappings by plain-English name
- known project-list mappings
- member name or email aliases
- preferred response wording
- list-creation policy for promoting an idea into a project

## Portability boundary

Portable:

- routing logic
- assignment and due-date decision rules
- read filters
- response discipline

User-specific:

- auth path
- workspace IDs
- list IDs
- member IDs
- exact status vocabulary
- naming conventions for project lists

## Packaging recommendation

- Keep human-editable defaults in one config file.
- Avoid hardcoding live IDs in the skill body.
- Reference the config file from the skill and from setup docs.
