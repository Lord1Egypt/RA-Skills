---
name: feishu-master
description: AI Tool Extension for Feishu API - A progressively extensible skill that enables AI tools (OpenClaw, Claude Code, etc.) to leverage Feishu capabilities on-demand. Only implements APIs when needed, avoiding premature development.
---

# Feishu Skill - AI Tool Extension for Feishu API

A progressively extensible skill designed for AI tools to leverage Feishu capabilities. The core philosophy is **implement only what you need, when you need it**.

## ⚠️ CRITICAL: After Creating New Scripts

**You MUST update `scripts/script_index.json` immediately after creating any new script.**

Failure to update the index will cause:
- Future AI lookup cannot find the newly created script
- Duplicate implementation of the same functionality
- Confusion for other AI tools using this skill

**Action required:** Add an entry to `scripts/script_index.json` with fields: `name`, `description`, `usage_hint`, `added_date`, `tags`

## Design Philosophy

This skill is **designed specifically for AI tools**, not for human manual use.

When an AI tool receives a task involving Feishu:

1. **Check existing scripts first** - Search `scripts/script_index.json` for already-implemented APIs
2. **Implement only if needed** - If no match exists, use Context7 to query Feishu OpenAPI documentation
3. **Add to index** - Once implemented, update the index to avoid future re-implementation

This approach ensures:
- **No wasted effort** - Only implement APIs when actually needed
- **Progressive expansion** - The skill grows based on real usage patterns
- **Efficient lookup** - AI tools can quickly find what's already available

## Quick Start

This skill works out of the box once authentication is configured:

```bash
# Configure authentication (one-time setup)
cd scripts/env
echo '{"app_id": "your_app_id", "app_secret": "your_app_secret"}' > app.json
```

## AI Workflow

### Decision Logic

When AI encounters a Feishu-related task, follow this decision tree:

**Step 1: Check index file**
```
Read scripts/script_index.json
Search by: description, tags
```

**If match found:**
- Run `python3 script.py --help` to understand parameters
- Execute the script
- Return result

**If NO match found:**
- Use Context7 to query Feishu API documentation:
  ```
  Library: open.feishu.cn / larksuite
  Query: "[specific requirement, e.g., 如何获取群组成员列表]"
  ```
- Implement new Python script based on documentation
- Execute and test
- **IMPORTANT:** Update `scripts/script_index.json` to add the new script

**If execution fails:**
- Check API error messages
- Use Context7 or `references/doc_urls.txt` to consult documentation
- Fix the script
- Re-test

### Critical Decision Points

When deciding between "use existing" vs "implement new", consider:

- **Is there a semantic match?** Even if parameter names differ, if the functionality is equivalent, use existing script
- **What's the cost of implementing?** Simple single-call APIs → implement immediately. Complex multi-call workflows → consider reusing existing scripts
- **Can this compose from existing scripts?** Sometimes new features can be achieved by combining multiple existing scripts

## Technical Reference

### Script Index Format

`scripts/script_index.json` structure:

```json
{
  "version": "1.0",
  "last_updated": "2026-02-12T12:00:00Z",
  "scripts": [
    {
      "name": "get_group_members",
      "description": "获取指定群组的人员列表",
      "usage_hint": "python3 get_group_members.py <open_chat_id>",
      "added_date": "2026-02-12",
      "tags": ["group", "member", "user"]
    }
  ]
}
```

**Key fields for AI search:**
- `description`: Human-readable explanation of functionality
- `tags`: Array of keywords for matching (prioritize these for fuzzy matching)

### Authentication

**Configuration file:** `scripts/env/app.json`

```json
{
  "app_id": "cli_xxxxxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

To obtain credentials:
1. Login to [Feishu Open Platform](https://open.feishu.cn/)
2. Create or select an application
3. Get App ID and App Secret from application details

**Token management:** `get_token.py` handles token lifecycle:
- Automatic caching during validity period
- Auto-refresh 5 minutes before expiration
- Cache file: `scripts/env/token_cache.json`

### Script Template

When implementing new APIs, use this template:

```python
#!/usr/bin/env python3
"""
[Complete functional description]

Usage:
    python3 script.py <param1> <param2> [options]

Parameters:
    param1: Parameter description
    param2: Parameter description

Options:
    --page-size: Page size (default: 20)
    --page-token: Pagination token

Output:
    JSON format output:
    {
      "code": 0,
      "msg": "success",
      "data": { ... }
    }

References:
    Feishu API: https://open.feishu.cn/document/...
"""

import sys
import json
import subprocess
from pathlib import Path
import requests

# Configuration
TOKEN_SCRIPT = Path(__file__).parent / "get_token.py"
BASE_URL = "https://open.feishu.cn"

def get_token():
    """Get Feishu access token"""
    result = subprocess.run(
        [sys.executable, str(TOKEN_SCRIPT)],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def api_function(param1, param2, token, **kwargs):
    """API call function"""
    headers = {"Authorization": f"Bearer {token}"}
    # ... implement API call
    pass

def main():
    # Handle --help
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return

    # Parse required parameters
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    param1 = sys.argv[1]
    param2 = sys.argv[2]
    kwargs = {}

    # Parse optional parameters
    for i in range(3, len(sys.argv)):
        if sys.argv[i].startswith("--"):
            key = sys.argv[i][2:].replace("-", "_")
            i += 1
            if i < len(sys.argv):
                kwargs[key] = sys.argv[i]

    # Get token
    token = get_token()

    # Call API
    result = api_function(param1, param2, token, **kwargs)

    # Output JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

**Development standards:**
1. **⚠️ CRITICAL:** After creating any new script, you MUST update `scripts/script_index.json` immediately
2. Complete docstring with Usage, Parameters, Options, Output sections
3. Support `--help` parameter
4. Use `get_token.py` for authentication
5. Output standard JSON format
6. Proper error handling with friendly messages

### 📋 New Script Creation Checklist

When implementing a new API, you MUST complete ALL steps:

- [ ] Query Context7 for API documentation
- [ ] Create the Python script following the template
- [ ] Test the script execution (verify it returns correct JSON)
- [ ] **⚠️ UPDATE `scripts/script_index.json`** ← Don't forget this!
- [ ] Save the API documentation URL to `references/doc_urls.txt`

### Using Context7 for Feishu API

When implementing new APIs, query Feishu documentation via Context7:

```
Library ID: open.feishu.cn / larksuite
Query examples:
- "如何获取群组成员列表"
- "发送消息到飞书群组的 API 使用方法"
- "飞书文档操作的 OpenAPI"
```

**Why Context7?**
- Provides up-to-date API documentation
- Includes code examples and parameters
- Faster than searching the web manually
- Reduces trial-and-error

## Examples

### AI Task Example 1: Get Group Members

**User request:** "Get the member list for group oc_xxxxxxxxxxxxx"

**AI decision process:**
1. Search `scripts/script_index.json` → Found match: `get_group_members`
2. Execute: `python3 scripts/get_group_members.py oc_xxxxxxxxxxxxx`
3. Return result

### AI Task Example 2: Add New API Capability

**User request:** "Delete a message from the group"

**AI decision process:**
1. Search `scripts/script_index.json` → No match
2. Context7 query: "飞书删除消息 API"
3. Get documentation showing `message/delete` endpoint
4. Implement `delete_message.py` script
5. Test execution
6. **⛔ CRITICAL STEP: Update `scripts/script_index.json` with new entry** - DO NOT skip this!
7. Return result

**Why step 6 is critical:**
- If you skip it, next AI will NOT find `delete_message.py` in the index
- This causes duplicate work: same functionality will be re-implemented
- The progressive expansion philosophy breaks down

## References

- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu API Documentation](https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/AI-assistant-code-generation-guide)
- DEVELOPMENT.md - Detailed development guidelines
