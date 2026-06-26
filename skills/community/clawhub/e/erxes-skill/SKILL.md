---
name: erxes
emoji: 🔌
description: >
  Manage contacts, companies, products, tags, documents, brands, automations,
  team members, organization data, block plugin records, and operation plugin
  records on an erxes instance. Use when the user wants to view, create,
  update, or remove erxes data through GraphQL.
requires:
  - env: ERXES_BASE_URL
    description: "erxes gateway URL, for example https://your-subdomain.next.erxes.io/gateway or http://localhost:4000"
---

# erxes– Чадварууд

## Login

Use `scripts/login.sh` for authentication.

```bash
ERXES_BASE_URL=<url> ERXES_CLIENT_ID=${ERXES_CLIENT_ID:-erxes-local} bash scripts/login.sh
```

- `ERXES_BASE_URL` is required.
- `ERXES_CLIENT_ID` is optional. Default to `erxes-local`.
- Accept the URL in whatever form the user gives and normalize it to `ERXES_BASE_URL=<url>`.
- Do not explain OAuth internals unless the user asks.
- Do not ask the user to copy tokens manually.
- Do not store tokens in project files.
- The script opens the browser, waits for approval, and prints a session JSON payload to stdout.

Read [erxes-app-token-auth.md](./erxes-app-token-auth.md) only when you need the quick login reference.

## API calls

After login, use the returned session payload directly.

- Read `accessToken` from the login JSON response.
- Send `Authorization: Bearer <accessToken>` and `erxes-subdomain: <subdomain>` headers on GraphQL calls.
- If the access token expires during the current task, use the in-memory `refreshToken` to get a new access token.
- Do not write tokens to `.auth.json` or any other project file.
- Read [erxes-graphql-api.md](./erxes-graphql-api.md) only when you need query or mutation examples.
- Assume OpenClaw is operating as the erxes owner unless the live API proves otherwise.
- Do not stop a normal workflow just because the backend source defines permission names. Treat those as implementation detail, not a user-facing blocker.

---

## Safe Action Rules

- Read, list, search, filter, group, and summarize can run directly.
- If the user asks to group results, fetch the matching list first and group the returned records in the response.
- For create or update, if the target record or required fields are unclear, summarize the planned change and ask only for the missing information.
- For delete, remove, deactivate, publish, unpublish, end, transfer, or convert actions, always identify the exact record and ask for explicit confirmation before sending the mutation.
- Never print `accessToken`, `refreshToken`, raw session JSON, or auth headers.
- Keep the auth session in memory only for the current task.
- Assume owner-mode access for discovered workflows. Only mention access problems if the live API actually rejects the request.

## Follow-Up Rules

- If the user gives a name but not an `_id`, search first, show the likely matches, then ask which record should be used.
- If the workflow depends on team, project, status, milestone, cycle, building, zoning, or unit IDs, fetch the choices first instead of guessing.
- Ask only for fields that are still missing.
- Warn before risky mutations:
- `blockDeleteBuilding` fails if the building still has zonings.
- `blockDeleteBuildingZoning` fails if the zoning still has units.
- `blockUpdateUnit` can fail if the unit already has a signed contract.
- `blockOpptyConvertToContract` needs both a target unit and a payment plan.
- `operationConvertTriageToTask` may need a valid team-specific status type.

## Харилцагч

- Бүх харилцагчийн жагсаалт харах
- Нэр, имэйл, утсаар хайх
- Харилцагчийн дэлгэрэнгүй мэдээлэл харах
- Төрлөөр нь бүлэглэх (үйлчлүүлэгч / боломжит / зочин)
- Шинэ харилцагч нэмэх
- Харилцагчийн мэдээлэл засах
- Харилцагч устгах
- Давхардсан харилцагчийг нэгтгэх

## Бүтээгдэхүүн

- Бүтээгдэхүүний жагсаалт харах
- Нэг бүтээгдэхүүний дэлгэрэнгүй харах
- Шинэ бүтээгдэхүүн нэмэх
- Бүтээгдэхүүн засах, устгах, нэгтгэх
- Ангилал болон хэмжих нэгж удирдах

## Шошго

- Бүх шошго харах
- Шошго нэмэх, засах, устгах
- Харилцагч эсвэл бүтээгдэхүүнд шошго хавсаргах

## Баримт бичиг

- Баримт бичгийн жагсаалт харах
- Баримт бичиг нэмэх, засах, устгах

## Брэнд

- Брэндийн жагсаалт харах
- Брэнд нэмэх, засах, устгах

## Автоматжуулалт

- Бүх автоматжуулалтын жагсаалт харах
- Автоматжуулалт нэмэх, засах, идэвхжүүлэх, устгах

## Байгууллагын бүтэц

- Хэлтэс, салбар, нэгж, албан тушаалын бүтэц харах
- Хэлтэс, салбар, нэгж, тушаал нэмэх, засах, устгах

## Багийн гишүүд

- Гишүүдийн жагсаалт харах
- Шинэ гишүүн урих
- Гишүүний мэдээлэл засах
- Гишүүнийг идэвхгүй болгох

## Block Plugin

- Use [block-api.md](./block-api.md) when the user wants help with block-side SaaS workflows such as projects, buildings, floor zonings, units, unit types, opportunities, statuses, payment plans, contracts, offers, invoices, documents, attachments, notes, or the developer profile.
- Natural language examples:
- "Show me all blocks grouped by status"
- "Create a new block with these details"
- "Find all units in this building"
- "Move this opportunity to another status"
- "Create a payment plan for this project"
- Read and list actions can run directly.
- Create and update actions should summarize the planned write first when important fields are ambiguous.
- Delete, publish, unpublish, transfer, and convert actions must always ask for confirmation first.

## Operation Plugin

- Use [operation-api.md](./operation-api.md) when the user wants help with operation-side SaaS workflows such as projects, tasks, triage, teams, statuses, cycles, milestones, notes, activities, and templates.
- Natural language examples:
- "Show me active projects"
- "Find tasks with no assignee"
- "Create a triage item for this team"
- "Convert this triage item to a task"
- "Summarize milestone progress"
- Read and list actions can run directly.
- Create and update actions should summarize the planned write first when important fields are ambiguous.
- Delete, end-cycle, remove-member, and status-removal actions must always ask for confirmation first.

## References
- scripts/login.sh — Browser login helper
- erxes-app-token-auth.md — Quick login reference
- erxes-graphql-api.md — Үйлдлүүдийн техникийн лавлах
- block-api.md — block_api SaaS workflow болон exact GraphQL ops
- operation-api.md — operation_api SaaS workflow болон exact GraphQL ops
