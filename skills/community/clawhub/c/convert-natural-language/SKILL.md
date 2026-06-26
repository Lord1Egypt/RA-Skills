---
name: convert-natural-language
description: >
  Use when (1) user provides a natural language description and asks to convert it to a structured format (SQL query, JSON object, API request, search query, regex pattern). (2) user wants to take a plain-language instruction and produce a machine-readable command or data schema. (3) user asks to parse or normalize a messy text input into a clean structured format.
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

## Core Position

This skill converts **natural language input into structured machine-readable formats**: SQL queries, JSON objects, API request specifications, search queries, regular expressions, and formal grammar productions. It does NOT just find-replace — it understands intent, extracts entities, resolves ambiguity, and produces semantically equivalent structured output.

Key responsibilities:
- Parse natural language to identify intent (what the user wants to do), entities (objects being referenced), and constraints (filters, conditions, limits)
- Map ambiguous conversational terms to precise structured syntax (e.g., "last week" → `date >= NOW() - 7 days`)
- Validate that the generated output is structurally correct (SQL parses, JSON is valid, regex compiles)
- Handle incomplete or ambiguous input by asking clarifying questions before generating wrong output

## Modes

### `/convert-natural-language --sql`
**Natural language → SQL query.** Converts a plain-language description into a syntactically valid SQL statement (SELECT, INSERT, UPDATE, DELETE). Supports PostgreSQL, MySQL, SQLite, and MongoDB query syntax.

Example: `"show me all users who signed up in the last 30 days and have never made a purchase"` → `SELECT * FROM users WHERE created_at >= NOW() - INTERVAL '30 days' AND id NOT IN (SELECT user_id FROM purchases);`

### `/convert-natural-language --json`
**Natural language → JSON object.** Converts a description into a structured JSON document. Use when the user describes a data structure or configuration in plain terms.

Example: `"a user with name John, email john@example.com, age 30, and optional phone number"` → `{"name": "John", "email": "john@example.com", "age": 30, "phone": null}`

### `/convert-natural-language --api`
**Natural language → API request specification.** Converts a description into an HTTP API call: method, URL path, query parameters, headers, body.

Example: `"get the profile of user ID 123 from the /users endpoint"` → `GET /users/123` (with auth header)

### `/convert-natural-language --search`
**Natural language → search query.** Converts a conversational search request into a precise query string for a specific search engine or database full-text search.

Example: `"find articles about AI from 2023 that mention GPT and were published in Nature or Science"` → `AI GPT 2023 site:nature.com OR site:science.com` (or `WHERE ...` for DB)

### `/convert-natural-language --regex`
**Natural language → Regular expression.** Converts a description of a text pattern into a regex pattern with named capture groups.

Example: `"a date in the format YYYY-MM-DD, like 2024-01-15"` → `(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})`

### `/convert-natural-language --schema`
**Natural language → JSON Schema or TypeScript interface.** Converts a description of a data structure into a formal schema definition.

Example: `"an array of order objects, each with order_id (string), amount (number), status (enum: pending/paid/refunded), and optional notes"` → TypeScript interface or JSON Schema.

### `/convert-natural-language --command`
**Natural language → shell command or CLI command.** Converts a description into a valid shell command (bash, zsh) or CLI tool invocation (git, docker, kubectl, etc.).

Example: `"show me all docker containers that are stopped"` → `docker ps -a --filter "status=exited"`

## Execution Steps

### Step 1: Identify target format and intent

**Detect target format** from user input:
- Contains "SQL", "query", "database" → `--sql`
- Contains "JSON", "data structure", "object", "schema" → `--json` or `--schema`
- Contains "API", "endpoint", "GET", "POST", "request", "call" → `--api`
- Contains "search", "find articles", "google", "look for" → `--search`
- Contains "regex", "pattern", "match", "validate format" → `--regex`
- Contains "command", "terminal", "run", "execute", "docker", "kubectl", "git" → `--command`

If format is still ambiguous, ask: "Should this be converted to SQL, JSON, an API call, a search query, or another format?"

**Identify intent components** from the input:
1. **Action**: what to do (SELECT, CREATE, SEARCH, VALIDATE, etc.)
2. **Subject**: the primary entity (users, orders, articles)
3. **Conditions**: filters, constraints (date ranges, status values, IDs)
4. **Fields**: what to return or include (columns, properties)
5. **Modifiers**:排序 (order by), limit, group by

### Step 2: Extract entities and map to structured syntax

**Entity extraction patterns:**

| Natural language | SQL | JSON | API | Regex |
|---|---|---|---|---|
| "all", "every", "everything" | `SELECT *` | no filter | no query param | `.*` |
| "last N days/weeks/months" | `WHERE ts >= NOW() - INTERVAL 'N days'` | `{"gte": "2024-01-01"}` | `&after=2024-01-01` | `\d{4}-\d{2}-\d{2}` |
| "never", "no", "without" | `WHERE id NOT IN (...)` or `WHERE field IS NULL` | `{"exists": false}` | `&has_field=false` | negative lookahead |
| "contains", "includes" | `WHERE col LIKE '%text%'` | `{"contains": "text"}` | `&q=text` | `.*text.*` |
| "or more", "at least" | `WHERE amount >= N` | `{"gte": N}` | `&min=N` | `\d+` |
| "optional", "may have" | `field = NULL allowed` | `{"type": "null"}` | `omitempty` in schema | quantifier `?` |
| "one of", "either A or B" | `WHERE status IN ('A', 'B')` | `{"enum": ["A", "B"]}` | `&status=A,B` | `(A|B)` |
| "sorted by", "order by" | `ORDER BY field ASC|DESC` | (not applicable) | `&sort=field` | (not applicable) |

### Step 3: Handle ambiguous or incomplete input

**Ambiguous time references:**
- "yesterday" → if today is 2024-01-16: `DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY)` (2024-01-15)
- "last week" → 7 days ago (or Monday to Sunday of last week — clarify)
- "recently" → ask for specific date range or use last 30 days as default

**Ambiguous entity references:**
- "the user", "they", "him" → ask for ID or use most recent if referentially clear
- "that order" → confirm which order if multiple candidates in context

**Incomplete conditions:**
- "show orders over $100" → infer `ORDER BY amount DESC` or ask for limit
- "users in California" → infer `SELECT *` but ask what fields to return

If critical information is missing and guessing would produce wrong output, ask before generating:
```
Cannot generate SQL: "users who bought something" — what table contains purchase records?
Please specify: (a) purchase/orders table name, (b) the link between users and orders tables (e.g., user_id foreign key).
```

### Step 4: Generate structured output

**For SQL mode:**
1. Determine SELECT columns (use `*` if not specified, or list specific columns)
2. Determine FROM table (infer from context or ask)
3. Determine WHERE conditions (map from natural language)
4. Add ORDER BY, LIMIT, GROUP BY if specified
5. Validate: parse with SQL grammar checker if available

**For JSON mode:**
1. Identify required fields from description
2. Map natural language to JSON types: string, number, boolean, array, object, null
3. Apply format constraints: email format, date format, enum values
4. Validate: `json.loads()` to confirm valid JSON

**For API mode:**
1. Determine HTTP method from action (get → GET, create → POST, update → PUT/PATCH, delete → DELETE)
2. Build URL path with path parameters (/users/{id})
3. Add query parameters for filters
4. Add headers (auth: Bearer token from env)
5. Validate: URL is well-formed, method is appropriate for resource

**For Regex mode:**
1. Identify required segments and their formats
2. Add named capture groups for each extracted entity
3. Add anchors (`^` at start, `$` at end) if pattern represents a complete match
4. Validate: compile with `re.compile()` — if fails, report syntax error with position

### Step 5: Validate output

**SQL validation:**
```python
# Use sqlparse (if available) to check syntax
import sqlparse
parsed = sqlparse.parse(output)
if not parsed:
    report_error("Invalid SQL syntax at character {pos}")
# Check for dangerous operations (DROP, DELETE without WHERE — warn but don't block)
```

**JSON validation:**
```python
import json
try:
    json.loads(output)
except json.JSONDecodeError as e:
    report_error(f"Invalid JSON: {e.msg} at position {e.pos}")
```

**Regex validation:**
```python
import re
try:
    re.compile(output)
except re.error as e:
    report_error(f"Invalid regex: {e.msg} at position {e.pos}")
```

**API validation:**
- Method + URL must match (e.g., GET with body → warn)
- Path parameters must be present in URL
- Auth header must be included (or document required header)

### Step 6: Return with explanation

For every conversion, return:
1. **The structured output** (the SQL, JSON, etc.)
2. **A mapping explanation** — how each NL phrase was interpreted:
   ```
   "last 30 days" → WHERE created_at >= NOW() - INTERVAL '30 days'
   "never made a purchase" → AND id NOT IN (SELECT user_id FROM purchases)
   ```
3. **Confidence** — how confident the conversion is:
   - `high`: intent clear, entities unambiguous, conditions complete
   - `medium`: some ambiguity resolved by reasonable default
   - `low`: significant assumptions made — flag for user review

```json
{
  "output": "SELECT * FROM users WHERE created_at >= NOW() - INTERVAL '30 days' AND id NOT IN (SELECT user_id FROM purchases);",
  "format": "sql",
  "dialect": "postgresql",
  "confidence": "high",
  "explanation": {
    "last 30 days": "WHERE created_at >= NOW() - INTERVAL '30 days'",
    "never made a purchase": "AND id NOT IN (SELECT user_id FROM purchases)",
    "all users": "SELECT * FROM users"
  },
  "warnings": [],
  "assumptions": []
}
```

## Mandatory Rules

### Do not

- Do not generate SQL INSERT/UPDATE/DELETE from natural language without explicitly confirming — destructive operations require `--confirm-dml` flag
- Do not guess table names or column names when they're absent from the description — ask instead of assuming
- Do not produce SQL that performs a full table scan without at least warning the user (e.g., `SELECT * FROM huge_table` without WHERE)
- Do not generate regex that matches extremely broad patterns (e.g., `.*`) without flagging as too permissive
- Do not convert natural language to shell commands that contain `rm -rf` or other destructive operations without explicit confirmation
- Do not assume a specific database dialect when the user didn't specify — default to the most common (PostgreSQL) but flag in output

### Do

- Show the mapping between natural language phrases and generated syntax (Step 6 explanation)
- Flag low-confidence conversions and explain why: "Assumed 'orders' table exists — verify table name matches your schema"
- Handle time zone references: "today" means current date in the user's configured timezone (default UTC)
- Handle plurals and mass nouns: "users" → `users` table, "order items" → `order_items` table (snake_case plural)
- Preserve case sensitivity when the user specifies it: "userID" different from "user_id"
- For SQL, always include a semicolon at end of statement

## Quality Bar

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Syntax validity | Output passes format parser (SQL parses, JSON valid, regex compiles) | Output passes strict schema validation |
| Semantic equivalence | Intent preserved — action, subject, conditions all captured | Intent preserved + nuanced details (ordering, limits, grouping) |
| Entity resolution | Ambiguous references resolved or flagged | All references resolved with context |
| Handling ambiguity | Flagged with specific question to user | Multiple interpretations offered with pros/cons |
| Time reference handling | Current date in UTC for "today", relative dates calculated | Timezone-aware, user-preferred timezone used |
| Edge case coverage | Handles null/empty/missing fields gracefully | Documents every assumption made |

A good output is syntactically valid, semantically equivalent to the input natural language, includes a clear explanation of how each phrase was interpreted, and flags any areas of ambiguity that required assumptions.

## Good vs. Bad Examples

| Scenario | Bad | Good |
|---------|-----|------|
| Missing table name | Assumes "users" table exists, generates SQL | Reports "Cannot determine which table contains user data — please specify table name (e.g., customers, accounts)" |
| Ambiguous time | Converts "recently" to last 7 days without flagging | Reports "Converted 'recently' to last 7 days — please specify exact date range if this is incorrect" |
| Destructive SQL | Generates DELETE FROM users without WHERE from "delete all users" | Generates DELETE with WHERE from "delete users who never logged in" with confirmation |
| No validation | Returns SQL that fails sqlparse | Validates SQL syntax, reports "Invalid SQL: unexpected token at line 1, position 15" |
| Incomplete NL | Returns partial output without noting what's missing | Reports "Could not generate complete query: missing (a) what to select, (b) which table" |
| Regex too broad | Generates `.*` for "any characters" (matches everything) | Generates `.*?` (non-greedy) or more specific pattern with explanation |
| Case sensitivity | Ignores case differences in field names | Preserves case: "UserID" → `user_id` (snake_case) vs `UserID` (exact) |
| API method | Converts "get data" to POST without confirming | Infers GET from "get/fetch/retrieve", POST from "create/submit", asks if ambiguous |