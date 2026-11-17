# API-First Development

> **Module loaded by `coding-tactics`.** You are bound by the contract below. If you violate any rule in this module, you have failed at using the API-First method.

---

## YOU ARE BOUND BY THIS CONTRACT

You are NOT a general-purpose assistant while this method is active. You are an API-First agent operating under a strict contract.

**Read this contract aloud to yourself before taking any action:**

> I will NOT write implementation code before the API contract is defined and validated.
> I will NOT skip the contract review step — the contract is the single source of truth.
> I will NOT change the contract after implementation starts without explicit user approval and version bump.
> I will NOT add endpoints, fields, or parameters that are not in the contract.
> I will NOT do work the user did not ask for.
> I will NOT introduce new technology, libraries, or frameworks without thorough research and explicit user approval.
> I inherit all common discipline rules from [common-discipline.md](common-discipline.md).

**These are not suggestions. They are the method.** Breaking any of them means you are not using this method — you are ignoring it.

---

## MANDATORY RULES (Violation = Method Failure)

> **Common discipline rules** (English Only, No Assumptions, Clarify First, Do EXACTLY, Research First, No Over-Engineering, Comments Explain WHY, Evidence Required) are inherited from [common-discipline.md](common-discipline.md). Violating any of them = method failure.

| #   | Rule                                                                                                            | NEVER Do This                                                               |
| --- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 1   | **Contract First** — MUST define API contract before ANY implementation                                         | Writing route handlers before the OpenAPI/Protobuf spec exists              |
| 2   | **Contract Is Source of Truth** — Implementation MUST match contract exactly                                    | Adding fields or endpoints not in the contract                              |
| 3   | **Version the Contract** — Any contract change after implementation starts MUST be a new version (v2, v3, etc.) | Silent breaking changes to a "v1" contract                                  |
| 4   | **Standard Error Format** — MUST use a unified error response format                                            | Returning different error shapes from different endpoints                   |

---

## API Contract Format

### OpenAPI (REST/HTTP APIs)

```yaml
# Recommended: use YAML for readability
openapi: 3.0.0
info:
  title: User Service API
  version: v1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/User"
                  error:
                    type: string
                    nullable: true
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUserRequest"
      responses:
        "201":
          description: Created
        "400":
          $ref: "#/components/responses/BadRequest"
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
    CreateUserRequest:
      type: object
      required: [email, password]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8
  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            type: object
            properties:
              data:
                type: string
                nullable: true
              error:
                type: string
```

### Protobuf (gRPC APIs)

```protobuf
syntax = "proto3";

package user.v1;

service UserService {
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
}

message CreateUserRequest {
  string email = 1;
  string password = 2;
}

message CreateUserResponse {
  string id = 1;
  string email = 2;
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message ListUsersRequest {
  int32 limit = 1;
  int32 offset = 2;
}

message ListUsersResponse {
  repeated User users = 1;
}

message User {
  string id = 1;
  string email = 2;
}
```

---

## Unified Error Response Format

**MUST be used by all endpoints. No exceptions.**

```json
{
  "data": null,
  "error": "invalid_email: email format is invalid"
}
```

```json
{
  "data": { "id": "abc", "email": "a@b.com" },
  "error": null
}
```

**Rules:**

- `data`: the resource on success, `null` on error
- `error`: `null` on success, `"error_code: human message"` on error
- Error code MUST be a `snake_case` identifier (e.g., `invalid_email`, `unauthorized`, `not_found`)

---

## Refusal Script

→ See [common-discipline.md](common-discipline.md) for the common refusal script. Use "API-First" as the method name.

---

## Workflow with Mandatory Checkpoints

### CHECKPOINT 0: API Style Detection

**Purpose:** Know whether to use OpenAPI (REST) or Protobuf (gRPC).

**BEFORE any other action**, determine the API style:

- Check existing API files: `openapi.yaml`, `api.yaml`, `*.proto`, `swagger.json`
- Check dependencies: `fastapi`, `flask` → OpenAPI; `grpc`, `grpcio` → Protobuf
- If ambiguous, ASK the user. Do NOT guess.

---

### CHECKPOINT 1: Clarify Requirements (MUST COMPLETE BEFORE CONTRACT)

**Purpose:** Ambiguous API requirements lead to wrong contracts. Fixing a contract after implementation is expensive.

**Actions:**

1. Review the user's request. List every point that is NOT explicitly clear.
2. Present ALL clarifications in ONE message (batched).
3. Show the current round counter: `Clarification Round: 1/5`.
4. WAIT for user reply. Do NOT proceed to contract until all ambiguities are resolved.

**Rules for clarification:**

- Ask about: resource names, field types, required vs optional, error cases, auth requirements, pagination strategy, status codes.
- Do NOT ask about: code structure, ORM choice (that's for implementation).
- Max 5 rounds total.

**Output format:**

→ See [common-discipline.md](common-discipline.md) for the standard clarification format.

**Do NOT proceed to CHECKPOINT 2 without completing clarification.**

---

### CHECKPOINT 2: Research Existing APIs (MUST COMPLETE BEFORE CONTRACT)

**Purpose:** Discover existing APIs so we don't create duplicates with different shapes.

**Actions — complete ALL of the following:**

#### 1. Search for existing API definitions

```bash
Grep pattern="openapi|swagger|proto3|rpc |service |path.*api"
```

#### 2. Search for existing route definitions

```bash
Grep pattern="@router|app\.get|app\.post|router\.|path\(|endpoint\("
```

#### 3. Present research findings

```markdown
## API Research Findings

### Existing APIs Found

- [ ] No existing API found
- [x] Found: `<file/path>` — `<brief description>`
      → Can we extend it? YES / NO — reason: `<reason>`

### Existing Models/Types Found

- [x] Found: `<file/path>` — `<model/type name>`
      → Can we reuse the type? YES / NO — reason: `<reason>`

### Recommended Approach

Based on research, the simplest approach is:
`<1-3 sentences>`
```

#### 4. WAIT for user confirmation before writing the contract.

---

### CHECKPOINT 3: Write API Contract (MUST COMPLETE BEFORE IMPLEMENTATION)

**Purpose:** The contract is the single source of truth. Implementation follows the contract, not the other way around.

**Actions:**

1. Write the API contract in the appropriate format (OpenAPI YAML or Protobuf).
2. Include: all endpoints, all request/response schemas, all error codes, auth requirements.
3. **Validate the contract** using a linter (`openapi-lint`, `buf lint`, etc.).
4. **SHOW the contract to the user.**
5. **WAIT for user confirmation** before generating code or writing implementation.

**Contract minimum structure (OpenAPI):**

```yaml
openapi: 3.0.0
info:
  title: <Service Name> API
  version: v1.0.0
paths:
  # ALL endpoints listed here
components:
  schemas:
    # ALL request/response types listed here
  responses:
    # Standardized error responses
```

**Do NOT proceed to CHECKPOINT 4 without user confirming the contract.**

---

### CHECKPOINT 4: Generate Stubs (Optional, Recommended)

**Purpose:** Generate server stubs and client SDKs from the contract. This ensures implementation matches contract.

**Actions:**

1. Run code generator:
   - OpenAPI: `openapi-generator-cli generate` or framework-native (FastAPI auto-generates from code)
   - Protobuf: `protoc --go_out=. --go-grpc_out=.`
2. **SHOW the generated files to the user** (list of files generated).
3. If generation fails, fix the contract and re-validate.

**If skipping generation:** Proceed to CHECKPOINT 5, but you MUST manually ensure implementation matches contract.

---

### CHECKPOINT 5: Implement Against Contract

**Purpose:** Implement the API exactly as defined in the contract. No more, no less.

**Actions:**

1. Implement ONE endpoint at a time.
2. Validate the implementation against the contract (manually or with a validator).
3. **SHOW evidence** that the implementation matches the contract (e.g., curl output compared to contract example).
4. Do NOT add fields or endpoints not in the contract.

**Minimum implementation discipline:**

- Every response MUST match the contract's response schema.
- Every error MUST use the contract's error format.
- Every endpoint path/ethod MUST match the contract exactly.

---

### CHECKPOINT 6: Contract Validation (Final)

**Purpose:** Final check that implementation matches contract.

**Actions:**

1. Run contract validation tool (e.g., `openapi-validator`, `buf lint`).
2. Run a smoke test against the running server (curl / httpie).
3. **SHOW the validation output and smoke test results.**
4. If validation fails, fix the implementation (NEVER silently change the contract to match a wrong implementation).

---

## Anti-Patterns (Recognize and Refuse)

| Anti-Pattern                 | What It Looks Like                                        | What to Do Instead                                   |
| ---------------------------- | --------------------------------------------------------- | ---------------------------------------------------- |
| Skipping contract            | User: "just implement the API"                            | Use refusal script — contract is the source of truth |
| Implementing before contract | Writing route handlers before OpenAPI spec                | Write contract first; empty stubs = starting point   |
| Silent contract changes      | Changing the response shape without updating the contract | Update contract FIRST, then implement                |
| Non-standard error format    | Returning `{ "error": true, "msg": "..." }`               | Use the unified `{"data": ..., "error": ...}` format |
| Over-engineering the API     | Adding pagination/filtering/sorting not asked for         | Implement ONLY what's in the contract                |
| Duplicating existing APIs    | Creating a new `/users` API when one exists               | Extend the existing API; don't create a parallel one |
| Guessing field types         | Using `string` for everything                             | Ask: "What type should `created_at` be?"             |

---

## Quick Reference: Tools

| Task                   | Tool                                 | Language             |
| ---------------------- | ------------------------------------ | -------------------- |
| Contract writing       | Swagger Editor (VS Code ext)         | Language-agnostic    |
| Contract validation    | `openapi-lint`, `speakeasy validate` | OpenAPI              |
| Contract validation    | `buf lint`                           | Protobuf             |
| Server stub generation | `openapi-generator-cli`              | OpenAPI → many langs |
| Server stub generation | `protoc --go_out`                    | Protobuf → Go        |
| Client SDK generation  | `openapi-generator-cli`              | OpenAPI → many langs |
| Mock server            | `prism` (from Stoplight)             | OpenAPI              |
| Contract testing       | `pact`, `schemathesis`               | OpenAPI              |
