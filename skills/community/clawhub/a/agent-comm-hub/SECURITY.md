# Security Policy

Agent Communication Hub takes security seriously. This document outlines our security mechanisms and how to report vulnerabilities.

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 2.x     | ✅ Active development |
| < 2.0   | ❌ Not supported      |

## Security Features

### Authentication
- **Token-based auth**: API tokens authenticated via SHA-256 hash. Raw tokens never stored in DB.
- **Invite code system**: Time-limited invite codes (24h) for agent registration.
- **Connection-level auth**: SSE (`/events/:agent_id?token=xxx`), WebSocket (`/ws?token=xxx`), and HTTP MCP all require valid tokens.

### Authorization
- **RBAC (4 levels)**: `public` → `member` → `group_admin` → `admin`
- Each MCP tool has an assigned permission level in `TOOL_PERMISSIONS`
- `register_agent` is the only public tool; all others require authentication
- `admin` role required for sensitive operations (token revocation, trust score changes, role assignment)

### Audit Trail
- All sensitive operations logged to `audit_log` table
- **Hash chain**: Each audit record contains `prev_hash` and `record_hash`, forming an immutable chain
- `verifyAuditChain()` validates chain integrity at any time
- DB triggers prevent UPDATE/DELETE on committed audit records

### Transport Security
- **CORS**: Whitelist-only configuration, default deny
- **Security headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Strict-Transport-Security, Content-Security-Policy
- **SSE injection protection**: Message content validated for SSE control sequences (`data:`, `event:`, `id:`, `retry:`)
- **NULL byte detection**: Message content checked for `\x00` bytes
- **Request tracing**: Every request carries a `traceId` for audit correlation

### Rate Limiting
- Per-agent rate limiting: 10 requests/second default window
- Configurable via `RATE_LIMIT_WINDOW` and `RATE_LIMIT_MAX` env vars

### Database
- WAL journal mode for crash safety
- DB split detection + auto-merge (three-layer protection)
- Watchdog cron for periodic DB health checks

### File Upload
- Base64-encoded, 10MB max file size
- Configurable upload directory

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately:

1. **DO NOT** open a public GitHub issue
2. Email the maintainer at the address listed in [package.json](client-sdk/package.json)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Affected version(s)
   - Potential impact

You can expect:
- **Acknowledgment** within 48 hours
- **Status update** within 5 business days
- **Fix timeline** communicated once the issue is triaged

## Responsible Disclosure

We request that you:
- Give us reasonable time to fix the issue before public disclosure
- Do not exploit the vulnerability beyond demonstrating proof of concept
- Share any relevant test cases or fixes you develop

We will:
- Credit you in the release notes (if desired)
- Issue a CVE if applicable
- Notify all supported versions
