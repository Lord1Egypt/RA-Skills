# Mistakes to Avoid

## Critical (Block Immediately)
1. **Force pushing main** - Never allowed
2. **Committing without tests** - Blocks CI/CD
3. **Direct database writes** - Bypasses validation
4. **Hardcoded secrets** - Security violation
5. **Ignoring TypeScript errors** - Breaks type safety

## High Severity (Require Confirmation)
1. **Large refactors without tests** - High risk of regression
2. **Adding new dependencies** - Increases bundle size
3. **Changing API contracts** - Breaks client compatibility
4. **Removing deprecated code** - May break integrations

## Common Corrections (Auto-promote after 3 occurrences)
1. **Forgetting to update documentation** - Add pre-commit hook
2. **Inconsistent naming** - Add ESLint rule
3. **Missing error boundaries** - Add React error boundary
4. **Hardcoded URLs** - Move to environment variables

## Resolved Mistakes
- ~~Using `var` instead of `const/let`~~ (ESLint rule added)
- ~~Not handling promise rejections~~ (global handler added)
- ~~Inline styles instead of CSS modules~~ (lint rule added)

## Correction History
- **2026-04-05**: Corrected force push attempt → added pre-push hook
- **2026-04-04**: Fixed missing test for new component → added test requirement
- **2026-04-03**: Caught hardcoded API URL → moved to env vars

## Auto-Promotion Rules
After 3 corrections of the same type:
1. Add to "Critical" or "High Severity" list
2. Create automated guard (pre-commit hook, lint rule)
3. Update documentation
4. Notify team