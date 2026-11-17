---
name: coding-net
version: 1.1.0
description: Query and operate on Tencent Coding DevOps platform (e.coding.net) data — iterations, issues (requirements/defects/tasks), and team members — including creating requirements and defects. Triggered when the user's request involves Coding platform operations, such as "list iterations", "query issues", "requirements in the current iteration", "bugs on Coding", "team member list", "assignee", "create a requirement", "create a defect". All APIs require the CODING_TOKEN environment variable.
---

# Coding Open API Skill

## Bootstrap (must run at the start of every conversation)

**Step 1: Collect the token**

Check whether the user's message already includes a token. If not, check the environment variable:
```bash
python3 -c "import os; print('set' if os.environ.get('CODING_TOKEN') else 'not set')"
```
If neither is available, ask the user: "Please provide your Coding personal access token (Bearer Token)."

**Step 2: Validate the token and confirm the team**

```python
import sys; sys.path.insert(0, "path/to/coding-net/scripts")
from core import bootstrap
result = bootstrap(token="<token>")
if result["error"]:
    print("✗", result["error"])
else:
    t = result["team"]
    print(f"✓ Token valid  Team: {t['name']}  ({t['host']})")
```

**Step 3: Confirm the project identifier**

Let the user know the team has been verified, then ask:
"Please provide the project URL or project identifier. The URL format is `https://<team>.coding.net/p/<project-identifier>/`, where the project identifier is the part after `/p/` (e.g. `biaopin-swiftagent`)."

> ⚠️ **Never guess the project name.** Coding.net distinguishes between "display name" and "project identifier" — the API only accepts the identifier.
> The user saying "the project is called swiftagent" does NOT mean the identifier is `swiftagent`; always ask for the URL to confirm.

**Step 4: Validate the project + show the iteration list for the user to choose from**

```python
result = bootstrap("biaopin-swiftagent", token="<token>")
if result["error"]:
    print("✗", result["error"])
else:
    print("Iterations in this project:")
    for it in result["iterations"]:
        print(f"  [{it['code']}] {it['name']}")
```

Show the iteration list to the user and ask: "Which iteration would you like to look at?"

Only after completing these four steps should you proceed with the user's actual query.

---

## Environment configuration (optional — set these to skip passing parameters)

| Variable | Description |
|------|------|
| `CODING_TOKEN` | Bearer Token |
| `CODING_DEFAULT_PROJECT_NAME` | Default project identifier (the part after `/p/` in the URL) |
| `CODING_DEFAULT_ITERATION_CODE` | Default iteration Code (integer) |

## Script layout

```
scripts/
├── core.py        — HTTP client, token resolution, CodingAPIError
├── iterations.py  — Iteration API (depends on core)
├── issues.py      — Issue API (depends on core + iterations)
└── members.py     — Team member API (depends on core)
```

Usage in Python (the scripts already handle sys.path, so just import directly):

```python
import sys
sys.path.insert(0, "path/to/scripts")
from iterations import get_iteration_list_code_and_name
from issues import describe_issue, describe_issue_list, create_issue, describe_defect_types, \
    extract_members_from_issue_list, get_custom_fields_from_issues
from members import get_team_members_id_and_name
```

## Public function reference

### iterations.py

```python
get_iteration_list_code_and_name(project_name=None, *, token=None) -> [{'code': int, 'name': str}]
```
Paginates through and returns the full iteration list. The returned `code` is the value needed by `describe_issue_list(iteration=...)`.

### issues.py

```python
describe_issue_list(
    project_name=None, *,   # falls back to CODING_DEFAULT_PROJECT_NAME if omitted
    issue_type="ALL",       # ALL / REQUIREMENT / DEFECT / MISSION
    limit="2000",
    assignee_ids=None,      # [int] — server-side filter (unreliable; pair with filter_issues for a client-side re-filter)
    iteration=None,         # int  — falls back to CODING_DEFAULT_ITERATION_CODE if omitted; a client-side re-filter is already built in
    status_types=None,      # None→TODO+PROCESSING; []→no filter; ['TODO',...]→specific types
    base_issue_type=None,   # REQUIREMENT / DEFECT / MISSION
    token=None,
) -> dict
# Each entry in Response.IssueList contains:
#   Code, Name, Type, IssueStatusName, IssueStatusType, Priority,
#   Assignees([{"id": int, "name": str}]),  ← array of assignees (not Creator/Handler)
#   IterationCode, IterationName, StartDate, DueDate, CustomFields
```

```python
filter_issues(
    items: list,            # the IssueList returned by describe_issue_list
    *,
    assignee_name=None,     # assignee name (fuzzy match, case-insensitive)
    assignee_id=None,       # assignee ID (exact match)
    iteration_code=None,    # secondary iteration Code filter (use when server-side filtering fails)
) -> list
```

```python
describe_issue(project_name=None, issue_code=0, *, token=None) -> dict
# Returns {Name, Description, IssueStatusName, AssigneeName, CreatorName}
```

```python
create_issue(
    project_name=None, *,
    name: str,                  # title (required)
    issue_type="REQUIREMENT",   # REQUIREMENT / DEFECT / MISSION
    description="",
    priority=2,                 # 0=Low 1=Medium 2=High(default) 3=Urgent (per API docs)
    assignee_id=None,           # int — member ID (see members.py, or look it up from the issue list)
    iteration=None,             # int — falls back to CODING_DEFAULT_ITERATION_CODE if omitted
    start_date=None,            # str 'YYYY-MM-DD' — required in some projects
    due_date=None,              # str 'YYYY-MM-DD' — required in some projects
    label_ids=None,             # [int] — required in some projects; missing value raises issue_project_label_required
    working_hours=None,         # float — estimated hours; required in some projects
    issue_type_id=None,         # int — issue category ID (not the defect subtype)
    defect_type_id=None,        # int — defect subtype ID, from describe_defect_types
    token=None,
) -> dict  # {Code, Name, IssueStatusName, AssigneeName, CreatorName}
```

```python
describe_defect_types(project_name=None, *, token=None) -> [{'id': int, 'name': str}]
# Returns the list of defect subtypes, for use with create_issue(defect_type_id=...)
```

```python
extract_members_from_issue_list(issues_result: dict) -> [{'id': int, 'name': str}]
# Extracts a deduplicated member list from the return value of describe_issue_list — a fallback for
# when the token lacks permission for DescribeTeamMembers
```

```python
get_custom_fields_from_issues(
    project_name=None, *,
    issue_type="REQUIREMENT",   # sample by issue type
    sample=10,                  # number of items to sample
    token=None,
) -> [{'id': int, 'name': str}]
# Infers a project's custom fields by sampling existing issues
# (works around DescribeIssueCustomFieldsBoundToProject, which requires elevated permissions)
# Must be called before creating an issue, so any required fields can be passed to
# create_issue via custom_field_values
```

### members.py

```python
get_team_members_id_and_name(*, token=None) -> [{'id': int, 'name': str}]
```
Paginates through and returns the full team member list. `id` can be used to filter with `describe_issue_list(assignee_ids=[...])`.
**Note**: Some tokens lack the `DescribeTeamMembers` permission, which causes an error — fall back to `extract_members_from_issue_list` in that case.

## Common workflows

**Query a specific assignee's requirements in a given iteration (standard flow):**
```python
import sys; sys.path.insert(0, "path/to/coding-net/scripts")
from issues import describe_issue_list, filter_issues

result = describe_issue_list(project_name, iteration=22904, issue_type="REQUIREMENT", status_types=[])
issues = result["Response"]["IssueList"]

# Filter by assignee client-side (server-side filtering is unreliable)
my_issues = filter_issues(issues, assignee_name="wangyin")
for it in my_issues:
    assignees = ", ".join(a["name"] for a in it["Assignees"])
    print(f"#{it['Code']} [{it['IssueStatusName']}] {it['Name']} — {assignees}")
```

**Extract members from the issue list (fallback when DescribeTeamMembers is not permitted):**
```python
from issues import describe_issue_list, extract_members_from_issue_list

result = describe_issue_list(project_name, iteration=code, status_types=[])
members = extract_members_from_issue_list(result)
# [{'id': 9403993, 'name': 'wangyin'}, ...]
```

**Query the details of a single issue (including description):**
```python
from issues import describe_issue
detail = describe_issue(project_name, issue_code=12345)
```

**Create a requirement (must detect custom fields first):**

> ⚠️ A project may have required custom fields configured (e.g. "test submission date"); creating without
> them raises `issue_custom_field_required`.
> First call `get_custom_fields_from_issues()` to infer the field list, then pass `custom_field_values`.

```python
from issues import create_issue, get_custom_fields_from_issues

# Step 1: Detect the project's custom fields
custom_fields = get_custom_fields_from_issues(project_name, issue_type="REQUIREMENT")
# Example return: [{"id": 38589683, "name": "Test submission date"}, ...]
# Confirm each field's value with the user; required fields must be passed in

# Step 2: Create the requirement
issue = create_issue(
    project_name,
    name="Support feature XX",
    start_date="2026-06-17",
    due_date="2026-06-30",
    custom_field_values=[
        {"Id": 38589683, "Content": "2026-06-30"},  # Test submission date
        # other required custom fields...
    ],
)
print(issue["Code"], issue["Name"])
```

**Create a defect (including project-level required fields):**
```python
from issues import describe_issue_list, extract_members_from_issue_list, describe_defect_types, create_issue, filter_issues

# 1. Look up member ID from the issue list
result = describe_issue_list(project_name, iteration=code, status_types=[])
members = extract_members_from_issue_list(result)
uid = next(m["id"] for m in members if m["name"] == "Zhang San")

# 2. Look up defect subtypes
defect_types = describe_defect_types(project_name)  # [{'id': 36666669, 'name': 'Functional defect'}, ...]

# 3. Create (whether start_date/due_date/label_ids/working_hours are required depends on project config)
issue = create_issue(
    project_name,
    name="Login page returns a 500 error",
    issue_type="DEFECT",
    priority=1,
    assignee_id=uid,
    iteration=code,
    start_date="2026-06-17",
    due_date="2026-06-20",
    label_ids=[123],
    working_hours=2.0,
    defect_type_id=defect_types[0]["id"],
)
```
