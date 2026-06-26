# MCP Workflow

Use MCP as the source of truth for Bitrix24 docs.

## Connection Facts

- Endpoint: `https://mcp-dev.bitrix24.tech/mcp`
- This is a streamable MCP endpoint, not a regular documentation page
- Without `Accept: text/event-stream`, the endpoint rejected requests with `406 Not Acceptable`
- `initialize` reported:
  - protocol version `2025-03-26`
  - server `b24-dev-mcp`
  - version `0.2.0`

## Recommended Order

1. Search.
2. Resolve the exact method, event, or article title.
3. Fetch details.
4. Only then make the REST call or write the example.

## Search Tool

Use `bitrix-search` first.

Helpful arguments:

- `query`: natural-language search text
- `limit`: cap the number of matches
- `doc_type`: narrow the result space

Supported `doc_type` values confirmed from MCP:

- `method`
- `event`
- `other`
- `app_development_docs`

## Detail Tools

- `bitrix-method-details`: exact REST method name only
- `bitrix-event-details`: exact event name only
- `bitrix-article-details`: exact non-method article title
- `bitrix-app-development-doc-details`: exact app-development title

## Practical Search Patterns

Use queries close to the user task:

- `crm deal add`
- `task checklist`
- `task comment`
- `im message chat`
- `calendar event section`
- `disk storage folder file`
- `user department structure`
- `oauth install callback`

Then pass the exact name from search into the appropriate details tool.

## Patterns Confirmed During Analysis

The current MCP server returned strong matches for these families:

- CRM: `crm.deal.*`, `crm.contact.*`, `crm.company.*`, `crm.lead.*`, `crm.activity.*`, `crm.item.*`
- Tasks: `tasks.task.*`, `task.checklistitem.*`, `task.commentitem.*`, `task.planner.getlist`
- Chat: `im.message.*`, `im.chat.*`, `im.dialog.*`, `im.recent.*`, `im.notify.*`, `imbot.*`
- Calendar: `calendar.event.*`, `calendar.section.*`, `calendar.accessibility.get`
- Drive: `disk.storage.*`, `disk.folder.*`, `disk.file.*`, `im.disk.file.commit`
- Users and org structure: `user.*`, `department.*`, `im.department.*`, `im.search.*`

## Avoid Stale Memory

Do not trust memory alone when:

- a method family is large
- a scenario is scope-sensitive
- a method may be deprecated
- an example mixes `im.*` and `imbot.*`
- a field name is portal-specific

Re-run `bitrix-method-details` in those cases.
