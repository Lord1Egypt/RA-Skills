# ClawScan API Contract v0.1

Use this reference when preparing request payloads or explaining expected response fields.

## Base assumptions

- Base URL example: `https://clawscan.autosec.dev`
- Auth scheme is intentionally unspecified in v0.1; use whatever deployment-specific header or bearer token the operator provides.
- All timestamps should be ISO 8601 UTC when present.
- All hashes should be SHA-256 hex strings.

## Common response envelope

Most routes should follow this shape:

```json
{
  "module": "skills-check",
  "status": "ok",
  "risk_level": "low",
  "summary": "No known malicious skill hash was matched",
  "findings": [],
  "errors": [],
  "meta": {
    "client_id": "uuid-v4",
    "scan_time": "2026-03-06T10:00:00Z",
    "engine_version": "0.1.0"
  }
}
```

## GET /index

Returns service metadata and enabled modules.

Example response:

```json
{
  "service": "ClawScan",
  "service_version": "0.1.0",
  "api_version": "v1",
  "modules": [
    {"name": "vulnerability", "path": "/vulnerability"},
    {"name": "skills-check", "path": "/skills-check"},
    {"name": "port-check", "path": "/port-check"}
  ],
  "register_required": true,
  "latest_skill_version": "0.1.3"
}
```

## POST /register

Request:

```json
{
  "client_id": "uuid-v4",
  "skill_version": "0.1.0",
  "platform": "darwin",
  "openclaw_version": "1.2.3"
}
```

Response:

```json
{
  "status": "ok",
  "registered": true,
  "client_token": "optional"
}
```

## POST /update/check

Request:

```json
{
  "client_id": "uuid-v4",
  "current_skill_version": "0.1.0"
}
```

Response:

```json
{
  "update_available": true,
  "latest_version": "0.1.3",
  "min_supported_version": "0.1.0",
  "download_url": "https://example.invalid/skill.zip",
  "sha256": "abcdef...",
  "release_notes": ["bug fix", "detection update"]
}
```

## POST /vulnerability

Request:

```json
{
  "client_id": "uuid-v4",
  "openclaw_version": "1.2.3",
  "platform": "darwin"
}
```

Response:

```json
{
  "module": "vulnerability",
  "status": "ok",
  "risk_level": "high",
  "summary": "Current OpenClaw version matches known vulnerable versions",
  "findings": [
    {
      "id": "OC-2026-001",
      "title": "Example issue",
      "severity": "high",
      "affected_versions": "<=1.2.3",
      "current_version": "1.2.3",
      "fixed_version": "1.2.4",
      "recommendation": "Upgrade to 1.2.4 or later"
    }
  ]
}
```

## POST /skills-check

Request:

```json
{
  "client_id": "uuid-v4",
  "skills": [
    {
      "skill_name": "foo",
      "files": [
        {"relative_path": "SKILL.md", "sha256": "abc..."},
        {"relative_path": "run.py", "sha256": "def..."}
      ]
    }
  ]
}
```

Response:

```json
{
  "module": "skills-check",
  "status": "ok",
  "risk_level": "medium",
  "summary": "1 suspicious skill found",
  "findings": [
    {
      "skill_name": "foo",
      "risk_level": "high",
      "matched": true,
      "match_type": "exact_hash",
      "matched_files": [
        {
          "relative_path": "run.py",
          "sha256": "def...",
          "threat_name": "KnownMaliciousSkill.A"
        }
      ],
      "recommendation": "Disable and remove this skill immediately"
    }
  ]
}
```

## POST /port-check

Request:

```json
{
  "client_id": "uuid-v4",
  "listeners": [
    {
      "proto": "tcp",
      "ip": "0.0.0.0",
      "port": 3000,
      "process_name": "openclaw",
      "pid": 1234
    }
  ]
}
```

Response:

```json
{
  "module": "port-check",
  "status": "ok",
  "risk_level": "high",
  "summary": "1 externally exposed listener found",
  "findings": [
    {
      "ip": "0.0.0.0",
      "port": 3000,
      "process_name": "openclaw",
      "exposed": true,
      "severity": "high",
      "reason": "Service is listening on all interfaces",
      "recommendation": "Bind to 127.0.0.1 or place behind authenticated reverse proxy"
    }
  ]
}
```

## POST /scan

Optional aggregate route.

Request:

```json
{
  "client_id": "uuid-v4",
  "modules": ["vulnerability", "skills-check", "port-check"],
  "payload": {
    "openclaw_version": "1.2.3",
    "skills": [],
    "listeners": []
  }
}
```

## Local collection notes

### Version discovery

Preferred commands:

```bash
openclaw --version
claw --version
```

### Skills hashing

Run:

```bash
python scripts/collect_skill_hashes.py ~/.openclaw/skills ./skills
```

The script ignores missing roots and emits JSON only for skill directories that exist.

### Listener discovery

Run:

```bash
python scripts/list_listeners.py
```

The script prefers `ss` and falls back to `lsof`.
