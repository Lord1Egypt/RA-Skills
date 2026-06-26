# Security Model

This document describes the security model and operational boundaries of `chaoji-skills`.

## Scope

`chaoji-skills` has two security-relevant layers:

- Root and scene skills: route requests, read project context, and in some workflows write output files.
- `chaoji-tools`: executes validated API commands through the internal Python runner.

This file covers both layers so reviewers can compare the written workflow against the declared permissions.

## Credential Requirements

This skill pack requires ChaoJi OpenAPI credentials to function. Supported sources are:

| Method | Location | Priority |
|--------|----------|----------|
| Environment variables | `CHAOJI_AK`, `CHAOJI_SK` | Highest |
| Credentials file | `~/.chaoji/credentials.json` | Fallback |

### Credentials File Format

```json
{
  "access_key": "your_access_key",
  "secret_key": "your_secret_key"
}
```

如需获取 AK/SK，请参考 [凭证获取指南](references/credentials-guide.md)。

Security guidance:

- Restrict file permissions, for example `chmod 600 ~/.chaoji/credentials.json`
- Never commit credentials to version control
- Prefer environment variables in CI or shared environments

## Declared Permissions

The root skill is a routing-only skill and declares minimal permissions:

- `file_read`: `~/.chaoji/credentials.json`
- `exec`: `python`

Scene skills declare their own permissions based on their workflows:

- `file_read`: `~/.chaoji/credentials.json`, `~/.openclaw/workspace/chaoji/`
- `file_write`: `~/.openclaw/workspace/chaoji/`
- `exec`: `python` (for internal runner script only)

### Root Skill Permission Scope

| Path | Access | Purpose |
|------|--------|---------|
| `~/.chaoji/credentials.json` | Read | Load API credentials |

The root skill does not write files or read project directories. It only routes to scene skills.

### Scene Skill Permission Scope

| Path | Access | Purpose |
|------|--------|---------|
| `~/.chaoji/credentials.json` | Read | Load API credentials |
| `~/.openclaw/workspace/chaoji/` | Read/Write | Read/write outputs and workspace data |

### Command Execution Scope

| Command | Purpose | When Used |
|---------|---------|-----------|
| `python` | Execute internal runner script | `chaoji-tools/scripts/run_command.py` for API command dispatch |

Notes:

- `chaoji-tools` executes `scripts/run_command.py` via `python` to dispatch API commands.
- Scene skills call the runner indirectly through the executor module.
- No external CLI tools are required — all API calls are made via the built-in Python HTTP client.

## Prompt and Instruction Handling

- User-provided text, prompts, URLs, and JSON fields are treated as task data only.
- User content must not override skill instructions, permission boundaries, or runner behavior.
- Scene skills must not disclose unrelated local file contents, hidden instructions, internal endpoints, or credentials.
- `chaoji-tools` accepts only validated command names and validated parameter shapes from its registry; user text is not command authority.

## Runtime Repair Policy

Automatic runtime repair is intentionally disabled.

- The runner does not auto-install packages
- The runner does not auto-upgrade dependencies
- Operators should install or upgrade dependencies only when they explicitly want to

## Data Flow

### Direct Tool Execution (`chaoji-tools`)

```text
User Request
    |
    v
run_command.py
    |
    +-- Read credentials (env or file)
    +-- Validate command name and inputs
    +-- Execute API call via Python HTTP client
    |   +-- Upload local files to OSS if needed
    |   +-- Call ChaoJi OpenAPI endpoint
    +-- Poll for async task result (if applicable)
    +-- Return result or error with guidance
```

### Scene Workflow Execution

```text
User Request
    |
    v
Root / Scene Skill
    |
    +-- Read project context
    +-- Extract parameters from user input
    +-- Call executor (run_command)
    +-- Return results and download outputs
```

## What This Skill Pack Does NOT Do

- Does not auto-install or auto-upgrade packages
- Does not treat user prompt text as authority to run arbitrary binaries
- Does not declare permission to write outside the current workspace and `~/.openclaw/workspace/chaoji/`
- Does not execute arbitrary scripts from the current project workspace
- Does not intentionally disclose credentials or unrelated local files in responses

## Audit Checklist

Before publishing or using this skill pack in production:

- [ ] Credentials are stored securely and not committed
- [ ] Declared permissions still match the written workflow in `SKILL.md` and scene skills
- [ ] `chaoji-tools/scripts/lib/` source has been reviewed

## Contact

If you encounter any issues during use, contact wuyuxiong@kunbyte.com
