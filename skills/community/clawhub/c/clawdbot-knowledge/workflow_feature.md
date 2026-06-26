# Workflow Example: Feature Addition with Ockham Agent

Complete workflow for adding small features using Ockham Agent via SpeakMCP.

---

## Scenario

You want to add email validation to a user registration form in a TypeScript/React application.

### Current Code
```typescript
// src/components/RegisterForm.tsx
export function RegisterForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    // TODO: Add email validation
    await registerUser({ email });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      {error && <span className="error">{error}</span>}
      <button type="submit">Register</button>
    </form>
  );
}
```

---

## Step 1: Voice Command

**Hold `Ctrl+Alt` and say:**

```
Use Ockham Agent to add email validation to the RegisterForm component
in src/components/RegisterForm.tsx. The repository is at
C:\projects\webapp. Language is TypeScript.
```

**Or type:**

```
Use ockham_add_feature:

Feature: Add email validation to user registration
File: src/components/RegisterForm.tsx
Requirements:
  - Validate email format before submission
  - Show error message for invalid emails
  - Use existing error state
  - Follow project patterns

Repo: C:\projects\webapp
Language: typescript
```

---

## Step 2: Agent Processing

**Ockham Agent:**

1. **Context Analysis**
   - Reads `RegisterForm.tsx`
   - Finds existing error handling pattern
   - Checks for validation utilities in project
   - Identifies React/TypeScript patterns

2. **Patch Generation**

   **Patch 1 (Tiny - Regex Validation):**
   ```typescript
   const handleSubmit = async () => {
     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
     if (!emailRegex.test(email)) {
       setError('Invalid email address');
       return;
     }
     setError('');
     await registerUser({ email });
   };
   ```

   **Patch 2 (Small - Extracted Function):**
   ```typescript
   const validateEmail = (email: string): boolean => {
     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
     return emailRegex.test(email);
   };

   const handleSubmit = async () => {
     if (!validateEmail(email)) {
       setError('Please enter a valid email address');
       return;
     }
     setError('');
     await registerUser({ email });
   };
   ```

   **Patch 3 (Fallback - Use Library):**
   ```typescript
   import validator from 'validator';  // New dependency

   const handleSubmit = async () => {
     if (!validator.isEmail(email)) {
       setError('Please enter a valid email address');
       return;
     }
     setError('');
     await registerUser({ email });
   };
   ```

3. **Evaluation**
   - Applies patches to worktree
   - Runs: `npm test`
   - Checks: `npx eslint`
   - Checks: `npx tsc --noEmit`
   - Scans: `npm audit`

4. **Scoring**
   ```
   Patch 1: Score 0.88 (3 LoC, inline, no deps)
   Patch 2: Score 0.82 (7 LoC, extracted function)
   Patch 3: Score 0.45 (4 LoC, NEW DEPENDENCY penalty)
   ```

5. **Selection: Patch 1** (simplest, no new dependencies)

---

## Step 3: Review Results

**SpeakMCP shows:**

```
✅ Ockham Agent Feature Added

Best Patch (Score: 0.88):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Strategy: tiny-guard
Description: Add inline email validation with regex

Patch:
───────────────────────────────
--- a/src/components/RegisterForm.tsx
+++ b/src/components/RegisterForm.tsx
@@ -8,6 +8,11 @@ export function RegisterForm() {
   const handleSubmit = async () => {
-    // TODO: Add email validation
+    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
+    if (!emailRegex.test(email)) {
+      setError('Invalid email address');
+      return;
+    }
+    setError('');
     await registerUser({ email });
   };
───────────────────────────────

Evaluation:
  ✓ Tests: 8/8 passed
  ✓ ESLint: No issues
  ✓ TypeScript: No errors
  ✓ Security: No issues

Complexity:
  Lines changed: 5
  Files touched: 1
  Dependencies added: 0
  API changes: 0

Rationale:
Simple regex validation using standard email pattern.
Reuses existing error state. No new dependencies or
external validation libraries needed. Inline approach
keeps logic localized and easy to understand.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 4: Enhance (Optional)

**If you want the extracted function version:**

```
Use ockham_evaluate_patch on Patch 2

Review:
  - More maintainable (function can be reused)
  - Slightly more complex (+4 LoC)
  - Better for multiple validation points

Decision: Use Patch 2 if you'll validate emails elsewhere
```

---

## Step 5: Apply & Test

**Apply patch:**

```powershell
cd C:\projects\webapp
git checkout -b feature/email-validation

# Apply from clipboard
git apply patch.diff
```

**Add tests:**

```typescript
// src/components/__tests__/RegisterForm.test.tsx
describe('RegisterForm', () => {
  it('validates email format', () => {
    render(<RegisterForm />);

    const input = screen.getByRole('textbox');
    const button = screen.getByText('Register');

    // Invalid email
    fireEvent.change(input, { target: { value: 'invalid' } });
    fireEvent.click(button);
    expect(screen.getByText('Invalid email address')).toBeInTheDocument();

    // Valid email
    fireEvent.change(input, { target: { value: 'user@example.com' } });
    fireEvent.click(button);
    expect(screen.queryByText('Invalid email address')).not.toBeInTheDocument();
  });
});
```

**Run tests:**

```powershell
npm test -- RegisterForm.test.tsx
```

**Manual test:**

```powershell
npm start

# Test in browser:
# 1. Enter "notanemail" -> See error
# 2. Enter "user@example.com" -> No error, registers
```

---

## Step 6: Commit

```powershell
git add src/components/RegisterForm.tsx src/components/__tests__/RegisterForm.test.tsx
git commit -m "feat: Add email validation to registration form

- Validates email format before submission
- Shows error message for invalid emails
- Uses regex pattern for validation
- No new dependencies added

🤖 Generated with Ockham Agent"

git push origin feature/email-validation
```

---

## Alternative: More Robust Validation

**If Patch 1 is too simple, request enhancement:**

**Say:**
```
Ockham, enhance the email validation with more robust checking
including domain validation
```

**Or use Patch 2/3** if:
- You need validation elsewhere (extract function)
- You want library-quality validation (use validator.js)

---

## Extending the Feature

### Add More Validations

**Say:**
```
Use Ockham Agent to add password strength validation
to the RegisterForm, following the same pattern as email
```

### Add Loading State

**Say:**
```
Use Ockham to add a loading indicator during registration,
using existing patterns from the codebase
```

---

## Tips

1. **Specify patterns:** "Follow existing error handling"
2. **Avoid over-engineering:** Let Ockham keep it simple
3. **Incremental features:** Add one validation at a time
4. **Reuse patterns:** Ockham finds and follows project conventions

---

## Comparison: Manual vs Ockham

### Manual Implementation
```
Time: 15-20 minutes
- Write validation code
- Check existing patterns
- Test manually
- Maybe add dependency
- Write tests
- Code review concerns
```

### With Ockham Agent
```
Time: 5-7 minutes
- Voice command (30 sec)
- Review patch (2 min)
- Apply & test (3 min)
- Automatic pattern matching
- Minimal complexity
- Tests already passed
```

**Benefit:**
- ⏱️  10+ min saved
- 📉  Lower complexity
- ✅  Tests guaranteed
- 🎯  Consistent patterns

---

## Metrics

Track after using Ockham for features:
- **Features added:** Count
- **Time per feature:** Average
- **Dependencies avoided:** Count (should be high!)
- **Complexity trend:** Should stay flat/low

---

## Next Steps

**Similar workflows:**
- [workflow_refactor.md](workflow_refactor.md) - Refactoring patterns
- [workflow_bugfix.md](workflow_bugfix.md) - Bug fixes

**Advanced:**
- Chain features: "Add validation, then add loading state"
- Batch similar: "Add validation to all forms"

---

**Ockham Agent: Simple features, simply! 🚀**
