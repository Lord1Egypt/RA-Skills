# Code Review Focus for AI-Generated Code

## Prioritize (High Signal)

**Invariants and edge cases:**
- What assumptions is this code making about input data?
- What breaks if the assumption is violated?
- Example: If a loop assumes non-empty list, what happens if list is empty?

**Error boundaries:**
- Where can external calls fail? (network, database, API)
- Is the code catching and handling these gracefully?
- Do error paths log enough to debug later?

**Security and auth assumptions:**
- Is user input validated before use?
- Are permissions checked at the right layer?
- Is sensitive data logged or stored insecurely?

**Hidden coupling:**
- Does this change break other modules?
- Are there implicit dependencies on execution order?
- Could this change affect rollout safety (feature flags, canary deploys)?

## De-Prioritize (Low Signal)

**Style disagreements** — automation (formatters, linters, type checkers) handles this. Don't waste review cycles on "I would have named this variable differently."

**Micro-optimization** — unless the change is in a hot path and measurably slow, don't nitpick performance.

**Taste debates** — "I prefer this pattern" vs "this pattern is demonstrably better" are different conversations. Favor consistency with existing codebase.

## Review Questions to Ask

1. **What's the dominant risk in this change?** (If unclear, it needed more decomposition before implementation.)
2. **Can I write an edge-case test that breaks this?** (If yes, it's not done.)
3. **Does this change make rollout harder?** (Feature flags? Backward compatibility? Data migration?)
4. **Is the eval coverage sufficient?** (Did implementation include regression tests for touched domains?)

## Red Flags

- ❌ No regression tests for affected domains
- ❌ Error handling is "try/except: pass"
- ❌ New dependencies on execution order not documented
- ❌ Security-sensitive code with no comments explaining the why
- ❌ Feature flag logic not tested
