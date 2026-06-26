# Engineering Design & Implementation Plan — Master Template

This is the engineer's primary deliverable after SRS sign-off. It is the single source of truth for all development work. Every dev agent works from their section of this document.

## Document Structure

The Implementation Plan follows this structure exactly. Each major section has its own reference file with detailed templates — this file defines the overall structure and cross-cutting concerns.

---

## Section 1: Project Overview

```
Project: [Project Name]
SRS Version: [version number and date]
Engineer: Project Engineer
Date: [date produced]
Last Updated: [date of most recent update]
Status: Draft | Under PM Review | Approved | In Development
```

### 1.1 Scope Summary

2-3 paragraphs summarizing what is being built or modified, drawn from the SRS. Reference the SRS by version number.

### 1.2 Architecture Overview

Describe how all the pieces connect:
- System components and their relationships
- Data flow from user action to database and back
- Third-party integrations and their touch points
- Infrastructure/deployment context (if relevant)

For greenfield projects, include a reference to the Architecture Decision Record (ADR).

### 1.3 Technology Stack

```
Frontend: [framework, version, key libraries]
Backend: [language, framework, version, key libraries]
Database: [engine, version]
Infrastructure: [hosting, CI/CD, etc. — if known]
Third-Party: [APIs, services, payment processors, etc.]
```

### 1.4 Repository Information

```
Repo(s): [URL(s)]
Primary Branch: main
Branch Convention: feature/[ticket-id]-[slug], fix/[ticket-id]-[slug]
```

---

## Section 2: Frontend Specification

**Audience:** FE Developer (this section must stand alone — the FE dev should not need to read any other section to do their work)

See `references/frontend_spec.md` for the complete template. Produce the full FE spec using that template and insert it here.

---

## Section 3: Backend Specification

**Audience:** BE Developer (standalone section)

See `references/backend_spec.md` for the complete template. Produce the full BE spec and insert it here.

---

## Section 4: Database Schema Specification

**Audience:** BE Developer / DB (standalone section)

See `references/db_schema_spec.md` for the complete template. Produce the full DB spec and insert it here.

---

## Section 5: Cross-Cutting Concerns

These apply across all sections and all dev roles.

### 5.1 Authentication & Authorization

```
Auth Method: [JWT, session, OAuth, etc.]
Token Storage: [where tokens are stored on the client]
Auth Flow: [login → token issuance → token refresh → logout]
Permission Model: [role-based, attribute-based, etc.]
Roles: [list each role and what it can access]
```

Map each API endpoint to its required permission level.

### 5.2 Error Handling Strategy

```
Frontend:
  - API error display pattern (toast, inline, modal)
  - Network failure handling
  - Validation error display
  - Unexpected error fallback

Backend:
  - Error response format: { "error": { "code": "string", "message": "string", "details": {} } }
  - HTTP status code usage (400 for validation, 401 for auth, 403 for permission, 404 for not found, 500 for server)
  - Logging requirements for errors
  - Never expose stack traces or internal details to the client
```

### 5.3 Logging & Monitoring

Define what gets logged and at what level:
- **Info:** Successful operations, state changes
- **Warn:** Recoverable issues, deprecated usage
- **Error:** Failed operations, caught exceptions
- **Critical:** System-level failures, data integrity issues

### 5.4 Performance Considerations

- Expected data volumes and query patterns
- Caching strategy (if applicable)
- Pagination approach for list endpoints
- File upload size limits (if applicable)
- Any known performance-sensitive areas

### 5.5 Environment & Configuration

- Environment variables required (name and purpose, never values)
- Feature flags (if applicable)
- Configuration that varies by environment (dev/staging/prod)

---

## Section 6: QA Coverage Plan

**Audience:** QA Engineer (standalone section)

See `references/qa_spec.md` for the complete template. Produce the full QA plan and insert it here.

---

## Section 7: Task Breakdown & Dependency Map

**Audience:** PM (for Asana board setup)

See `references/asana_task_guide.md` for the Task Manifest format. Produce the full task breakdown and insert it here.

### 7.1 Dependency Diagram

Show task dependencies visually or as a structured list:

```
DB-001 (Create users table) → BE-001 (User CRUD endpoints) → FE-001 (User management UI)
DB-002 (Create orders table) → BE-003 (Order endpoints) → FE-004 (Order form)
BE-001 → BE-002 (Auth middleware) → FE-002 (Login flow)
```

### 7.2 Recommended Build Order

List the recommended sequence of development, noting what can be parallelized:

```
Phase A (can parallel):
  - DB: All schema migrations (DB-001 through DB-004)
  - FE: Static components, routing, state management setup (FE-001, FE-002 scaffolding)

Phase B (after Phase A):
  - BE: Core CRUD endpoints (BE-001 through BE-004)
  - FE: Wire up API calls as BE endpoints become available

Phase C (after Phase B):
  - BE: Business logic, edge cases (BE-005 through BE-008)
  - FE: Complex interactions, error states (FE-003 through FE-006)
  - QA: Begin testing completed features

Phase D:
  - Integration testing
  - QA full regression
  - Bug fixes
```

---

## Section 8: Change Log

Track all updates to the Implementation Plan after initial approval:

```
[Date] — [SRS ID or description] — [what changed] — [reason]
```

The engineer updates this log whenever the plan is modified, whether due to PM gap review, dev escalation findings, or scope changes.

---

## Completeness Checklist

Before submitting to the PM for review, verify:

- [ ] Every SRS requirement has corresponding spec coverage (trace each SRS ID)
- [ ] FE spec is self-contained (FE dev needs nothing else)
- [ ] BE spec is self-contained (BE dev needs nothing else)
- [ ] DB spec covers all new/altered tables with migration guidance
- [ ] Every endpoint has defined request/response shapes and error codes
- [ ] Every UI component has defined behavior for: loading, empty, error, and success states
- [ ] QA plan has test scenarios for every requirement (happy path + edge cases)
- [ ] Task breakdown covers all roles with effort estimates and dependencies
- [ ] Security checklist is completed in the BE spec
- [ ] Cross-cutting concerns are defined (auth, errors, logging)
- [ ] Dependency order is explicit and buildable
