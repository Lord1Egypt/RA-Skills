# Workflow Example: Bug Fix with Ockham Agent

Complete workflow for fixing bugs using Ockham Agent via SpeakMCP.

---

## Scenario

You have a Python service with a `NullPointerException` (actually `AttributeError` in Python) that occurs intermittently when fetching user data.

### Error Log
```
File "services/user_service.py", line 45, in get_user_profile
  return user.profile.to_dict()
AttributeError: 'NoneType' object has no attribute 'profile'
```

---

## Step 1: Capture Context

**Collect:**
- Stacktrace (from logs above)
- Issue description
- Repository path

---

## Step 2: Voice Command

**Hold `Ctrl+Alt` in SpeakMCP and say:**

```
Use Ockham Agent to fix the bug in user_service.py line 45.
The error is AttributeError NoneType has no attribute profile.
The repository is at C:\projects\myapp.
Language is Python.
```

**Or type (Ctrl+T):**

```
Use ockham_fix_bug to solve this issue:

Issue: AttributeError when fetching user profile
File: services/user_service.py
Line: 45
Stacktrace:
File "services/user_service.py", line 45, in get_user_profile
  return user.profile.to_dict()
AttributeError: 'NoneType' object has no attribute 'profile'

Repo: C:\projects\myapp
Language: python
```

---

## Step 3: Agent Processing

**What Ockham Agent does:**

1. **Context Building**
   - Extracts relevant files from stacktrace
   - Reads `services/user_service.py`
   - Finds related test files
   - Identifies error type: `AttributeError`

2. **Hypothesis Generation**
   - Generates 3 patch variants:

     **Patch 1 (Tiny Guard):**
     ```python
     def get_user_profile(user_id):
         user = User.query.get(user_id)
         if user is None or user.profile is None:
             return {}
         return user.profile.to_dict()
     ```

     **Patch 2 (Small Logic):**
     ```python
     def get_user_profile(user_id):
         user = User.query.get(user_id)
         if user is None:
             raise UserNotFoundError(f"User {user_id} not found")
         if user.profile is None:
             return {"user_id": user_id, "profile": None}
         return user.profile.to_dict()
     ```

     **Patch 3 (Fallback):**
     ```python
     def get_user_profile(user_id):
         try:
             user = User.query.get(user_id)
             return user.profile.to_dict() if user and user.profile else {}
         except AttributeError:
             logger.warning(f"Profile not found for user {user_id}")
             return {}
     ```

3. **Evaluation**
   - Applies each patch in isolated environment
   - Runs pytest tests
   - Checks with ruff linter
   - Runs mypy type checker
   - Scans with bandit (security)

4. **Scoring**
   ```
   Patch 1: Score 0.92 (2 LoC, 0 complexity increase, tests pass)
   Patch 2: Score 0.75 (5 LoC, +2 complexity, tests pass)
   Patch 3: Score 0.68 (4 LoC, +3 complexity, tests pass)
   ```

5. **Selection**
   - **Winner: Patch 1** (highest score, minimal change)

---

## Step 4: Review Results

**SpeakMCP displays:**

```
✅ Ockham Agent Fix Complete

Best Patch (Score: 0.92):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Strategy: tiny-guard
Description: Add null checks for user and profile

Patch:
───────────────────────────────
--- a/services/user_service.py
+++ b/services/user_service.py
@@ -42,6 +42,8 @@ def get_user_profile(user_id):
 def get_user_profile(user_id):
     user = User.query.get(user_id)
+    if user is None or user.profile is None:
+        return {}
     return user.profile.to_dict()
───────────────────────────────

Evaluation:
  ✓ Tests: 15/15 passed
  ✓ Lint: No issues
  ✓ Type Check: OK
  ✓ Security: No new issues

Complexity:
  Lines changed: 2
  Files touched: 1
  Cyclomatic delta: +1
  New dependencies: 0

Rationale:
Minimal guard clause prevents AttributeError when user
or profile is None. Returns empty dict for missing data,
maintaining API contract. Tests confirm fix without breaking
existing functionality.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5: Apply the Patch

**Review checklist:**
- ✅ Logic makes sense
- ✅ Tests pass
- ✅ No security issues
- ✅ Minimal complexity
- ✅ Matches project patterns

**Apply manually:**

```powershell
# Create feature branch
cd C:\projects\myapp
git checkout -b fix/user-profile-null-check

# Copy patch to file
# (SpeakMCP copied patch to clipboard)

# Apply patch
git apply patch.diff

# Or edit manually based on shown diff
```

**Test locally:**

```powershell
pytest tests/test_user_service.py
python -m mypy services/
```

**Commit:**

```powershell
git add services/user_service.py
git commit -m "fix: Add null check for user profile

Prevents AttributeError when user.profile is None.
Returns empty dict to maintain API contract.

Fixes #123

🤖 Generated with Ockham Agent
```

---

## Step 6: Verify

**Run full test suite:**

```powershell
pytest
```

**Check in production-like environment:**

```powershell
# Test with missing profile
curl http://localhost:8000/api/users/999/profile
# Should return {} instead of 500 error
```

---

## Alternative Scenarios

### If Patch Doesn't Pass Tests

Ockham Agent will:
1. Try next patch variant (Patch 2)
2. If all fail, relax complexity constraints
3. Generate new patches with slightly larger scope
4. Report if no solution found

**You then:**
- Review why patches failed (check test output)
- Provide more context to Ockham
- Or fix manually with Ockham's insights

### If Multiple Patches Score Similarly

Review all high-scoring patches:
```
Use ockham_evaluate_patch on each variant
Compare trade-offs
Choose based on project preferences
```

---

## Tips

1. **Provide good context:** More info = better patches
2. **Check test output:** Understand why solutions work
3. **Verify security:** Always review security scan results
4. **Incremental fixes:** One issue at a time
5. **Learn patterns:** Ockham reveals simple solutions you can reuse

---

## Metrics to Track

After using Ockham for bugs:
- **Time saved:** ~10-15 min per bug
- **Code quality:** Lower complexity than manual fixes
- **Test coverage:** Ensures tests pass
- **Consistency:** Similar patterns across codebase

---

**Next:** Try [workflow_feature.md](workflow_feature.md) for adding features!
