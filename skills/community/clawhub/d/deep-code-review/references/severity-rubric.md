# Severity Classification Rubric

Every confirmed issue gets exactly one severity level.

## Critical

**Definition**: A bug that causes the system to violate its core security or correctness guarantees, with no workaround.

**Examples**:
- Security boundary bypass that leaks private data
- Feature flag that doesn't actually limit the feature it's named after
- Data corruption that silently destroys user data
- **Over-engineering so severe it makes the codebase unmaintainable** (e.g., 500 lines of new abstraction for a one-line bugfix)

**Litmus test**: Would a reasonable user be shocked to learn this exists in production?

## High

**Definition**: A bug with significant security, correctness, or reliability impact, but with a partial workaround or limited blast radius.

**Examples**:
- SSRF vulnerability that requires attacker-controlled input
- Missing @-mention check in group chats (abuse requires insider knowledge)
- Concurrent race that requires specific timing to trigger

**Litmus test**: Would you fix this before the next release?

## Medium

**Definition**: A bug that degrades user experience, creates operational risk, or has been partially mitigated.

**Examples**:
- Missing backtrack/revisit mechanism in a multi-step workflow
- Error message that doesn't guide the user to the fix
- Flock implemented but with gaps (correct on happy path, missing on edge path)
- Race condition that wastes resources but doesn't corrupt data

**Litmus test**: Would you prioritize fixing this in the next sprint?

## Low

**Definition**: Cosmetic issues, theoretical concerns, or already well-mitigated risks.

**Examples**:
- DNS rebinding theory window with high exploit difficulty
- Token refresh margin that's overly conservative (no harm)
- Function rename needed for code clarity

**Litmus test**: Would you fix this only if you happened to be editing that file anyway?

## Mitigated

**Definition**: The reported concern exists in some form but is defended against by another mechanism.

**Examples**:
- Claimed SSRF vulnerability that's actually handled by a wrapper
- Alleged race condition where an upstream lock serializes access
- Reported missing check that actually happens at a different layer

## False Alarm

**Definition**: The reported concern does not exist in the codebase. No defense is needed because no attack path exists.

**Examples**:
- Reported command injection where no subprocess is used
- Claimed token leak where no logging of sensitive data exists
