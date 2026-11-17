#E2E CI & Reporting

## CI integration (example)

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
        env:
          CI: true
          BASE_URL: ${{ vars.STAGING_URL }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

Cypress: Fixed `CYPRESS_baseUrl` or `baseUrl` in the configuration file. Failure screenshots/videos are also recommended to upload artifacts.

## E2E report template (Markdown)

The following structure can be used when outputting or archiving test reports to facilitate review:

```markdown
# E2E test report

**Date:** YYYY-MM-DD HH:mm
**Time taken:** X minutes Y seconds
**Result:** Pass/Fail

## Summary

- Total X | Pass Y | Fail Z | Unstable/Skip Description

## Failed use case

### Use case name

- **File:** `tests/e2e/xxx.spec.ts:line number`
- **ERROR:** Brief assertion or timeout information
- **Screenshot/Trace:** path or artifact name
- **Suggested fix:** Executable conclusion

## Product

- HTML report: `playwright-report/index.html`
- Trace / Video / Screenshot: CI artifact or local `test-results/`
```
