# ClawHub Publishing Research Notes

Derived from recent public version history samples using `scripts/analyze_history.py`.

## Observed patterns

### 1. Many releases are not pure bugfixes
High-version skills often spend many releases on:
- description/title/opening copy
- onboarding/setup clarity
- documentation and reference expansion
- metadata corrections

Implication: a publishing assistant should not only validate syntax. It should also help authors improve trigger clarity and operator comprehension.

### 2. Metadata drift is common
Recent histories such as `baidu-search` and `minimax-vision-search` show repeated metadata-related edits.

Implication: declaration drift between SKILL.md, scripts, and scan expectations is a core failure mode.

### 3. Repeated release loops can mean process failure, not product momentum
When many versions land in a short period, likely causes include:
- validator/frontmatter mistakes
- unclear publish path
- metadata mismatch after scan
- post-publish verification confusion
- docs/examples still misleading users

Implication: the skill should diagnose why repeated publishes are happening before encouraging another upload.

### 4. Trigger copy matters a lot
Several mature skills repeatedly adjusted title/description/opening wording.

Implication: `clawhub-publisher` should eventually review the description as product copy, not just metadata.

## Suggested failure-mode buckets
- `frontmatter-invalid`
- `metadata-drift`
- `publish-path-wrong`
- `package-validation-failed`
- `latest-not-updated`
- `scan-pending`
- `scan-suspicious-real`
- `docs-trigger-iteration`
- `feature-iteration`
