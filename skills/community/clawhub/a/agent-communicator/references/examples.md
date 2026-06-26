# Agent Communicator — Code Examples

## Example 1

```markdown
## Review Request Flow

**Initiator:** /python-pro
**Reviewer:** /security-auditor

### Step 1: Request
📨 /python-pro → /security-auditor

Subject: Security review needed for auth module
Context: Implemented JWT authentication
Content: Please review auth.py for security issues
Files: src/auth/auth.py, src/auth/jwt_handler.py
Deadline: Before merge

### Step 2: Acknowledgment
📩 /security-auditor → /python-pro

Status: Review started
ETA: 30 minutes

### Step 3: Review Complete
📩 /security-auditor → /python-pro

Subject: Security review complete
Findings:
- 🔴 Critical: Token expiry not enforced (line 45)
- 🟡 Medium: Consider rate limiting (line 78)
- 🟢 Good: Proper password hashing

Action Required: Fix critical issue before merge

### Step 4: Resolution
📨 /python-pro → /security-auditor

Subject: Issues addressed
Content: Fixed token expiry, added rate limiting
Request: Re-review please

### Step 5: Approval
📩 /security-auditor → /python-pro

Subject: ✅ Approved
Content: All issues resolved, ready for merge
```

## Example 2

```markdown
## Handoff Flow

**From:** /backend-architect
**To:** /frontend-specialist

### Handoff Message
🤝 /backend-architect → /frontend-specialist

Subject: API ready for frontend integration
Context: User management API complete

**Deliverables:**
- OpenAPI spec: docs/api/users.yaml
- Base URL: /api/v1/users
- Auth: Bearer token required

**Endpoints:**
| Method | Path | Purpose |
|--------|------|---------|
| GET | /users | List users |
| GET | /users/:id | Get user |
| POST | /users | Create user |
| PUT | /users/:id | Update user |
| DELETE | /users/:id | Delete user |

**Notes:**
- Rate limit: 100 req/min
- Pagination: offset/limit params
- Error format: { error: string, code: number }

**Your tasks:**
1. Implement user list page
2. Implement user detail page
3. Implement user forms (create/edit)

**Questions?** Reply to this thread

### Acknowledgment
📩 /frontend-specialist → /backend-architect

Subject: Handoff received
Status: Starting implementation
Questions:
- Is there a search endpoint?
- What's the max page size?

### Clarification
📨 /backend-architect → /frontend-specialist

Answers:
- Search: GET /users?search=query
- Max page size: 100 items

Updated docs attached.
```

## Example 3

```markdown
## Feedback Loop Flow

**Designer:** /ux-designer
**Implementer:** /react-pro
**Reviewer:** /code-reviewer

### Initial Implementation
📢 /react-pro → [broadcast]

Subject: Dashboard component ready for review
Status: First implementation complete
Preview: localhost:3000/dashboard

### Design Feedback
💬 /ux-designer → /react-pro

Subject: Design feedback
Feedback:
- ✅ Layout matches wireframes
- ⚠️ Spacing inconsistent (use 8px grid)
- ⚠️ Colors slightly off (use design tokens)
- 💡 Consider adding loading skeleton

### Code Feedback
💬 /code-reviewer → /react-pro

Subject: Code review feedback
Feedback:
- ✅ Component structure good
- ⚠️ Extract repeated styles to shared components
- ⚠️ Add error boundary
- 💡 Consider React.memo for performance

### Iteration
📨 /react-pro → /ux-designer, /code-reviewer

Subject: Feedback addressed
Changes:
- Fixed spacing to 8px grid
- Applied design tokens
- Extracted shared styles
- Added error boundary
- Added loading skeleton

Request: Final review please

### Approval
💬 /ux-designer → /react-pro
Subject: ✅ Design approved

💬 /code-reviewer → /react-pro
Subject: ✅ Code approved

Ready for merge!
```

## Example 4

```markdown
## Collaborative Discussion

**Participants:** /backend-architect, /frontend-specialist, /security-auditor
**Topic:** Real-time updates implementation

### Discussion Thread

📨 /backend-architect [Thread Start]
Subject: How should we implement real-time updates?

Options:
1. WebSockets - bidirectional, complex
2. SSE - simpler, one-way
3. Polling - simplest, more load

My take: WebSockets for flexibility

---

💬 /frontend-specialist
Re: Real-time updates

Prefer SSE for our use case:
- We only need server → client
- Simpler to implement
- Better browser support
- Auto-reconnect built-in

---

💬 /security-auditor
Re: Real-time updates

Security considerations:
- WebSockets: Need to secure the upgrade
- SSE: Uses existing auth, easier
- Both: Rate limiting required

Recommendation: SSE is safer for our team's experience level

---

📨 /backend-architect
Subject: Decision: Using SSE

Based on feedback:
- SSE chosen for simplicity and security
- Will implement with auth token validation
- Rate limit: 1 connection per user

@/frontend-specialist - Can you handle SSE client?
@/security-auditor - Please review implementation

---

📩 /frontend-specialist
Confirmed: Will implement EventSource client

📩 /security-auditor
Confirmed: Will review when ready
```
