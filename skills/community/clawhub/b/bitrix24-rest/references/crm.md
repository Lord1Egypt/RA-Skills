# CRM

Use this file for deals, contacts, companies, leads, activities, and modern CRM item APIs.

## Core Methods

Deals:

- `crm.deal.list` / `crm.deal.get` / `crm.deal.add` / `crm.deal.update` / `crm.deal.delete`
- `crm.deal.fields` — field schema
- `crm.deal.contact.add` / `crm.deal.contact.items.get`

Contacts:

- `crm.contact.list` / `crm.contact.get` / `crm.contact.add` / `crm.contact.update` / `crm.contact.delete`
- `crm.contact.fields`

Companies:

- `crm.company.list` / `crm.company.get` / `crm.company.add` / `crm.company.update` / `crm.company.delete`

Leads:

- `crm.lead.list` / `crm.lead.get` / `crm.lead.add` / `crm.lead.update` / `crm.lead.delete`
- `crm.lead.fields`

Activities (classic):

- `crm.activity.list` / `crm.activity.add` / `crm.activity.update` / `crm.activity.delete`

Timeline — Todo (universal activities in deal/lead/contact timeline):

- `crm.activity.todo.add` — create a todo item in timeline
- `crm.activity.todo.update` — update todo
- `crm.activity.todo.updateDeadline` — change deadline only
- `crm.activity.todo.updateDescription` — change description only

Timeline — Comments & Log:

- `crm.timeline.comment.add` — add comment to entity timeline
- `crm.timeline.comment.update` — edit existing comment
- `crm.timeline.logmessage.add` — add log entry to timeline (for recording events)

CRM Feed:

- `crm.livefeedmessage.add` — post message to CRM activity stream

Stage History:

- `crm.stagehistory.list` — history of stage transitions (deals, leads, invoices)

Modern generalized APIs (smart processes, dynamic types):

- `crm.item.list` / `crm.item.add` / `crm.item.update` / `crm.item.delete`
- `crm.item.batchImport`

## Filter Syntax

CRM list methods use prefix operators:

- `>OPPORTUNITY` — greater than
- `>=DATE_CREATE` — on or after
- `=STAGE_ID` — equals (default without prefix)
- `!STATUS_ID` — not equal

Example: `filter[>OPPORTUNITY]=10000` returns deals with opportunity above 10000.

## Common Use Cases

### List deals with filter

```bash
python3 scripts/bitrix24_call.py crm.deal.list \
  --param 'filter[>OPPORTUNITY]=10000' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=OPPORTUNITY' \
  --param 'select[]=STAGE_ID' \
  --json
```

### Create a deal

```bash
python3 scripts/bitrix24_call.py crm.deal.add \
  --param 'fields[TITLE]=New Deal' \
  --param 'fields[OPPORTUNITY]=50000' \
  --param 'fields[CURRENCY_ID]=RUB' \
  --json
```

### Get field schema before writing

```bash
python3 scripts/bitrix24_call.py crm.deal.fields --json
```

### Add activity to a deal

```bash
python3 scripts/bitrix24_call.py crm.activity.add \
  --param 'fields[OWNER_TYPE_ID]=2' \
  --param 'fields[OWNER_ID]=123' \
  --param 'fields[TYPE_ID]=2' \
  --param 'fields[SUBJECT]=Follow-up call' \
  --json
```

### Stuck deals (no activity for 14+ days)

Deals in active pipeline with no recent modification — useful for proactive "💤" warnings:

```bash
python3 scripts/bitrix24_call.py crm.deal.list \
  --param 'filter[ASSIGNED_BY_ID]=1' \
  --param 'filter[STAGE_SEMANTIC_ID]=P' \
  --param 'filter[<DATE_MODIFY]=2026-02-22' \
  --param 'select[]=ID' \
  --param 'select[]=TITLE' \
  --param 'select[]=STAGE_ID' \
  --param 'select[]=DATE_MODIFY' \
  --param 'select[]=OPPORTUNITY' \
  --json
```

`STAGE_SEMANTIC_ID=P` = in progress (active pipeline). `<DATE_MODIFY` = last modified before 14 days ago.

### Add todo to a deal timeline

```bash
python3 scripts/bitrix24_call.py crm.activity.todo.add \
  --param 'ownerTypeId=2' \
  --param 'ownerId=123' \
  --param 'deadline=2026-03-15T15:00:00' \
  --param 'title=Follow up with client' \
  --param 'description=Call to discuss proposal' \
  --param 'responsibleId=5' \
  --json
```

`ownerTypeId`: 1=lead, 2=deal, 3=contact, 4=company.
Optional `pingOffsets` (array of minutes for reminders): `--param 'pingOffsets[]=0' --param 'pingOffsets[]=15'`

### Add comment to deal timeline

```bash
python3 scripts/bitrix24_call.py crm.timeline.comment.add \
  --param 'fields[ENTITY_ID]=123' \
  --param 'fields[ENTITY_TYPE]=deal' \
  --param 'fields[COMMENT]=Client confirmed budget approval' \
  --json
```

`ENTITY_TYPE` values: `deal`, `lead`, `contact`, `company`, `order`, `quote` (string, lowercase).

### Add log entry to timeline

```bash
python3 scripts/bitrix24_call.py crm.timeline.logmessage.add \
  --param 'fields[entityTypeId]=2' \
  --param 'fields[entityId]=123' \
  --param 'fields[title]=Price changed' \
  --param 'fields[text]=Price updated from 100k to 120k after negotiation' \
  --param 'fields[iconCode]=info' \
  --json
```

Note: `crm.timeline.logmessage.add` uses camelCase field names (`entityTypeId`), not UPPER_CASE.

### Post message to CRM feed

```bash
python3 scripts/bitrix24_call.py crm.livefeedmessage.add \
  --param 'fields[POST_TITLE]=Deal update' \
  --param 'fields[MESSAGE]=Contract signed with Company X' \
  --param 'fields[ENTITYTYPEID]=2' \
  --param 'fields[ENTITYID]=123' \
  --json
```

### Get stage history for deals

```bash
python3 scripts/bitrix24_call.py crm.stagehistory.list \
  --param 'entityTypeId=2' \
  --param 'filter[>=CREATED_TIME]=2026-03-01T00:00:00' \
  --param 'select[]=OWNER_ID' \
  --param 'select[]=STAGE_ID' \
  --param 'select[]=CREATED_TIME' \
  --json
```

Returns items with `TYPE_ID`: 1=created, 2=intermediate stage, 3=final stage, 5=pipeline change.
`STAGE_SEMANTIC_ID`: P=in progress, S=won, F=lost.

## Entity Type IDs

| ID | Entity |
|----|--------|
| 1 | Lead |
| 2 | Deal |
| 3 | Contact |
| 4 | Company |
| 5 | Invoice (old) |
| 7 | Quote |
| 31 | Smart Invoice (new) |
| 128+ | Custom smart processes |

## Working Rules

- Read `*.fields` before writing custom or portal-specific fields.
- Do not hardcode stage names across portals — pipelines and categories vary.
- Use classic `crm.deal.*` for built-in entities, `crm.item.*` for smart processes.
- Always use `select[]` to limit response size.
- Pagination: page size is 50, use `start=0`, `start=50`, etc.

## Good MCP Queries

- `crm deal list add update`
- `crm contact company`
- `crm lead fields`
- `crm activity`
- `crm activity todo add`
- `crm timeline comment`
- `crm timeline logmessage`
- `crm livefeedmessage`
- `crm stagehistory`
- `crm item smart process`
