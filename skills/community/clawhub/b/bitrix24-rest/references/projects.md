# Projects and Workgroups

Use this file for workgroups, projects, scrum, group membership, and cross-entity queries (tasks in a project, files in a project, project chat).

## Core Methods

List and read:

- `socialnetwork.api.workgroup.list` — list groups with filter and select
- `socialnetwork.api.workgroup.get` — get one group by ID
- `sonet_group.get` — list groups accessible to current user
- `sonet_group.user.groups` — groups of current user

Create and manage:

- `sonet_group.create` — create group (owner = current user)
- `sonet_group.update` — update group
- `sonet_group.delete` — delete group
- `sonet_group.setowner` — change owner

Membership:

- `sonet_group.user.get` — list group members
- `sonet_group.user.add` — add member directly
- `sonet_group.user.invite` — invite member
- `sonet_group.user.delete` — remove member
- `sonet_group.user.update` — change member role
- `sonet_group.user.request` — request to join
- `sonet_group.feature.access` — check user permissions in group

Scrum (for scrum-type projects):

- `tasks.api.scrum.sprint.list` / `tasks.api.scrum.sprint.getFields`
- `tasks.api.scrum.backlog.get`
- `tasks.api.scrum.task.getFields`

## Querying Entities Within a Project

### Tasks in a project

Filter `tasks.task.list` by `GROUP_ID`:

```bash
python3 scripts/bitrix24_call.py tasks.task.list \
  --param 'filter[GROUP_ID]=15' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=STATUS' \
  --param 'select[]=DEADLINE' \
  --json
```

### Files in a project

Projects have their own disk storage. Find it via `disk.storage.getlist` and filter by `ENTITY_TYPE=group`:

```bash
python3 scripts/bitrix24_call.py disk.storage.getlist \
  --param 'filter[ENTITY_TYPE]=group' \
  --param 'filter[ENTITY_ID]=15' \
  --json
```

Then browse with `disk.storage.getchildren` using the storage ID.

### Project chat

Group chats in Bitrix24 use dialog format `sg<GROUP_ID>`:

```bash
python3 scripts/bitrix24_call.py im.dialog.messages.get \
  --param 'DIALOG_ID=sg15' \
  --param 'LIMIT=20' \
  --json
```

## Common Use Cases

### List all my projects

```bash
python3 scripts/bitrix24_call.py sonet_group.user.groups --json
```

### Get project details

```bash
python3 scripts/bitrix24_call.py socialnetwork.api.workgroup.get \
  --param 'id=15' \
  --json
```

### List project members

```bash
python3 scripts/bitrix24_call.py sonet_group.user.get \
  --param 'ID=15' \
  --json
```

### Create a project

```bash
python3 scripts/bitrix24_call.py sonet_group.create \
  --param 'NAME=New Project' \
  --param 'DESCRIPTION=Project description' \
  --param 'VISIBLE=Y' \
  --param 'OPENED=Y' \
  --json
```

### Search groups by filter

```bash
python3 scripts/bitrix24_call.py socialnetwork.api.workgroup.list \
  --param 'filter[%NAME]=marketing' \
  --param 'select[]=ID' \
  --param 'select[]=NAME' \
  --param 'select[]=NUMBER_OF_MEMBERS' \
  --json
```

## Working Rules

- Use `socialnetwork.api.workgroup.list` for filtered queries with `select[]`.
- Use `sonet_group.get` for a quick list of accessible groups.
- Task filtering by project: `tasks.task.list` with `filter[GROUP_ID]`.
- Project files live in a disk storage with `ENTITY_TYPE=group`.
- Project chat is addressable as `sg<GROUP_ID>` in `im.*` methods.

## Good MCP Queries

- `socialnetwork workgroup list get`
- `sonet_group user create`
- `tasks scrum sprint backlog`
