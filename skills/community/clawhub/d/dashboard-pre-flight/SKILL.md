---
name: pre-flight
version: 1.0.0
tags: [react, dashboard, audit, quality, review, release-checklist, auth-integration-review, onboarding-ux-audit, security-hardening]
description: Universal React dashboard audit — detect hardcoded values, tier bypasses, stale components, and onboarding inconsistencies before users see them.
---

# Dashboard Audit Skill

Detect and fix anomalies in any React dashboard before they reach users.

## When to Use

- Before any release or deployment
- After auth/tier/subscription changes
- When user reports UI inconsistencies
- Before declaring a feature complete
- When onboarding flow changes
- After integrating a new auth provider

## Configuration

Set these at the top of your audit session:

```bash
PROJECT_SRC="./src"                    # Source directory
AUTH_PROVIDER="clerk"                  # clerk, auth0, firebase, etc.
TIER_PROP="userTier"                   # Prop name for subscription tier
MODE_STORAGE_KEY="terminal_mode"       # localStorage key for mode preference
API_CONSTANT="API_URL"                 # Constant exported from api client
PRICING_TIERS="free,pro,team"         # Comma-separated tier names
AUDIT_RUNS=1                           # Number of times to run full audit (1-5)
```

**Note:** Set `AUDIT_RUNS=2` or higher when:
- Fixing issues found in previous run
- First audit of a legacy codebase
- After major auth or tier refactoring
- Before production releases

Each run should produce zero new issues before proceeding.

## Audit Checklist

### 1. Tier Handling Verification
```bash
grep -rn "publicMetadata\|userMetadata\|auth0User" "$PROJECT_SRC/pages/" "$PROJECT_SRC/components/"
```
- [ ] No component reads tier from auth provider metadata directly
- [ ] All components accept tier via prop from root/App
- [ ] Fallback to base tier only in prop default, never in display logic

### 2. Hardcoded Content Scan
```bash
grep -rn "user@example.com\|example.com\|localhost:3001\|placeholder\|TODO\|FIXME\|HACK" \
  --include="*.jsx" --include="*.js" --include="*.tsx" --include="*.ts" "$PROJECT_SRC/"
```
- [ ] No placeholder emails in user-facing output
- [ ] No localhost/dev URLs in production code
- [ ] No TODO/FIXME/HACK comments (move to issues)

### 3. Mode/Preference Consistency
```bash
grep -rn "localStorage.getItem('$MODE_STORAGE_KEY')" "$PROJECT_SRC/"
```
- [ ] Base tier users default to restricted mode
- [ ] Paid tier users default to full mode
- [ ] Preference persists across sessions
- [ ] Propagates to backend for cross-device sync

### 4. Onboarding Flow Verification
```bash
grep -rn "curl -fsSL\|install.sh\|install.ps1\|iwr -useb\|brew install\|npm install -g" \
  "$PROJECT_SRC/pages/Onboarding*" "$PROJECT_SRC/pages/onboarding*"
```
- [ ] No external install commands shown (if integrated)
- [ ] Integrated paths referenced instead of external
- [ ] Safety layers mentioned if required for full mode
- [ ] Example URLs use docs domain, not IP addresses

### 5. API URL Consistency
```bash
grep -rn "192\.168\.\|127\.0\.0\.1\|localhost:" \
  --include="*.jsx" --include="*.js" --include="*.tsx" --include="*.ts" "$PROJECT_SRC/" | \
  grep -v "$API_CONSTANT"
```
- [ ] All API calls use exported constant
- [ ] No hardcoded IPs in components
- [ ] Environment-based API switching configured

### 6. Pricing Consistency
```bash
IFS=',' read -ra TIERS <<< "$PRICING_TIERS"
for tier in "${TIERS[@]}"; do
  grep -rn "\\\$[0-9]*.*$tier\|$tier.*\\\$[0-9]*" "$PROJECT_SRC/pages/"
done
```
- [ ] No hardcoded prices in UI strings
- [ ] Prices fetched from backend or config
- [ ] Currency formatting consistent

### 7. Stale Component Cleanup
```bash
find "$PROJECT_SRC/components" -name "*.jsx" -o -name "*.tsx" | \
  xargs grep -l "debug\|Debug\|wizard\|Wizard\|setup\|Setup" 2>/dev/null | \
  grep -i "debug\|install\|setup\|wizard"
```
- [ ] No debug/login components in production build
- [ ] No deprecated install/setup wizards (if integrated)
- [ ] No mock/demo components in production

### 8. Auth Fallback Chain Verification
```bash
grep -rn "dev-bypass\|test-token\|mock-user\|fake-" \
  --include="*.jsx" --include="*.js" --include="*.tsx" --include="*.ts" "$PROJECT_SRC/"
```
- [ ] No dev bypass tokens in production code
- [ ] Auth fallback chains end at "unauthenticated", not fake data
- [ ] Mock users cannot access real endpoints

## Fixes Applied (Template)

| # | Issue | Location | Fix |
|---|-------|----------|-----|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

## Verification Steps

1. Start dev server: `npm run dev` or `yarn dev`
2. Clear browser storage for fresh user simulation
3. Simulate new user signup with base tier
4. Complete onboarding flow
5. Simulate upgrade to paid tier
6. Execute core workflow in full mode
7. Verify no upgrade prompts for paid users
8. Check all pages render without console errors
9. Verify mobile responsiveness
10. Run Lighthouse audit (target: 90+ all categories)

## Prevention

- Run this audit before every PR merge
- Add CI check for hardcoded values (`grep` patterns above)
- Use constants for all URLs, prices, and tier names
- Never read tier from auth provider metadata in components — pass as prop
- Keep onboarding in sync with actual architecture
- Document auth fallback chain in README

## Adaptation Notes

- **Vue/Svelte:** Change `--include="*.jsx"` to `--include="*.vue"` or `--include="*.svelte"`
- **Next.js:** Add `pages/` and `app/` directories to scan paths
- **React Native:** Add check for Platform-specific code
- **Monorepo:** Run from each package directory separately

## Related Skills

- release-checklist
- auth-integration-review
- onboarding-ux-audit
- security-hardening

## Resources

- **IKKF**: https://ikkf.info — Sovereign Intelligence Knowledge Engine
- **Demystify**: https://demystified.website — Tech explainers and analysis
- **Tooled**: https://tooled.pro — Personal productivity platform
