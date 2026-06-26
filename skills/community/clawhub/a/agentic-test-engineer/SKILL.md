---
name: "Agentic Test Engineer"
description: "AI-powered autonomous test generation and self-healing test maintenance. Generates unit/integration/E2E tests, detects flaky tests, auto-fixes broken selectors, and maintains test coverage. Built for QA engineers and developers. Keywords: AI test automation, self-healing tests, autonomous QA, test generation, Playwright, Selenium, CI/CD testing, flaky test detection, visual AI testing, test coverage, AI-native QA."
version: "1.0.0"
---

# Agentic Test Engineer

## Overview

An AI-powered autonomous testing assistant that revolutionizes QA workflows. It generates comprehensive test suites from user stories and code, self-heals broken selectors using visual AI, detects and diagnoses flaky tests, and continuously maintains test coverage metrics — all with minimal human intervention.

## Triggers

- "generate tests for [feature/code]"
- "write unit tests for [function]"
- "self-heal my broken test"
- "find flaky tests in [project]"
- "check test coverage for [module]"
- "run E2E tests for [workflow]"
- "why is my test failing"
- "智能测试生成"
- "自愈测试修复"
- "测试覆盖率分析"

## Workflow

### Step 1: Detect Context

Identify the testing scenario:
- **Unit tests**: Python, JavaScript, TypeScript, Java, Go functions
- **Integration tests**: API endpoints, database interactions, service meshes
- **E2E tests**: Browser workflows (Playwright, Cypress, Selenium)
- **API tests**: REST/GraphQL endpoints, contract testing
- **Flaky test diagnosis**: Test results history, timing issues, async race conditions
- **Self-healing**: Broken selectors, changed DOM, moved UI elements

### Step 2: Test Generation

For test generation:
1. Analyze code structure, user story, or API spec
2. Select appropriate testing framework:
   - Python: pytest, unittest
   - JavaScript/TypeScript: Jest, Vitest, Playwright, Cypress
   - Java: JUnit, TestNG
   - Go: testing package, testify
3. Generate comprehensive test cases:
   - Happy path scenarios
   - Edge cases and boundary conditions
   - Error handling scenarios
   - Negative test cases
4. Include setup/teardown fixtures
5. Add data-driven test parameters

### Step 3: Self-Healing (When Triggered)

When a test breaks due to UI changes:
1. Capture the failing selector/error message
2. Use visual AI to identify the new element location
3. Generate updated selector using multiple strategies:
   - Text content matching
   - Semantic role/labels
   - Visual proximity to stable elements
   - Shadow DOM traversal
4. Validate the fix across related tests
5. Log the healing action for audit trail

### Step 4: Flaky Test Detection

1. Collect test execution history from CI/CD
2. Analyze failure patterns:
   - Timing issues (race conditions, async waits)
   - Resource contention (DB connections, file locks)
   - Environment instability
   - Test interdependencies
3. Generate diagnosis report with:
   - Probability of flakiness
   - Root cause analysis
   - Recommended fixes (add explicit waits, mock external calls, etc.)

### Step 5: Coverage Analysis

1. Parse code and existing test files
2. Calculate line/branch/function coverage
3. Identify untested code paths
4. Suggest priority test cases for uncovered areas
5. Generate coverage trend report

## Input/Output Examples

### Example 1: Generate Unit Tests

**Input:**
```
Generate unit tests for this Python function:
def calculate_premium(age: int, health_score: float, coverage_amount: float) -> float:
    if age < 18 or age > 70:
        raise ValueError("Age must be between 18 and 70")
    base_rate = coverage_amount * 0.05
    health_factor = 1.0 - (health_score / 100) * 0.3
    return base_rate * health_factor
```

**Output:**
```python
import pytest
from your_module import calculate_premium

class TestCalculatePremium:
    def test_happy_path(self):
        result = calculate_premium(age=30, health_score=80, coverage_amount=100000)
        assert 3000 <= result <= 5000

    def test_age_boundary_18_valid(self):
        result = calculate_premium(age=18, health_score=50, coverage_amount=100000)
        assert result == 100000 * 0.05 * (1.0 - 0.5 * 0.3)

    def test_age_boundary_70_valid(self):
        result = calculate_premium(age=70, health_score=50, coverage_amount=100000)
        assert isinstance(result, float)

    def test_age_too_young(self):
        with pytest.raises(ValueError, match="Age must be between"):
            calculate_premium(age=17, health_score=80, coverage_amount=100000)

    def test_age_too_old(self):
        with pytest.raises(ValueError, match="Age must be between"):
            calculate_premium(age=71, health_score=80, coverage_amount=100000)

    @pytest.mark.parametrize("health_score,expected_factor_range", [
        (0, (0.97, 1.01)),
        (50, (0.82, 0.88)),
        (100, (0.69, 0.71)),
    ])
    def test_health_factor_bounds(self, health_score, expected_factor_range):
        result = calculate_premium(age=30, health_score=health_score, coverage_amount=100000)
        lower, upper = expected_factor_range
        assert lower * 5000 <= result <= upper * 5000
```

### Example 2: Self-Healing a Broken Playwright Test

**Input:**
```
My Playwright test is failing: Selector ".submit-button" not found.
The button text is "提交保单" now.
```

**Output:**
```
🔧 Self-Healing Analysis:
- Original selector: ".submit-button"
- Issue: UI updated, element selector changed
- Healed selector strategy: text-content match

Generated alternatives:
1. await page.getByRole('button', { name: '提交保单' }).click()
2. await page.locator('button[type="submit"]').click()
3. await page.getByText('提交保单').click()

Recommended (most robust): Option 1
- Uses semantic role binding (survives CSS class changes)
- Language-aware (works with i18n updates)
```

### Example 3: Flaky Test Diagnosis

**Input:**
```
Diagnose why this test is flaky:
it('should load user dashboard', async () => {
  const dashboard = await page.locator('.dashboard').waitFor();
  const count = await dashboard.locator('.card').count();
  expect(count).toBeGreaterThan(0);
});
```

**Output:**
```
Flaky Test Report:
- Flakiness probability: 87% (HIGH)
- Root cause: Race condition between page load and element appearance

Recommended fixes:
1. Replace implicit waitFor() with explicit wait:
   await expect(page.locator('.dashboard')).toBeVisible({ timeout: 10000 })

2. Add network idle wait:
   await page.waitForLoadState('networkidle')

3. Use data-testid for stability:
   <div data-testid="user-dashboard" className="dashboard">...</div>

4. Add retry wrapper for truly async cases:
   await expect.poll(async () => {
     return await page.locator('.card').count();
   }, { timeout: 10000 }).toBeGreaterThan(0);
```

## Key Capabilities

| Capability | Description | Supported Frameworks |
|------------|-------------|---------------------|
| Test Generation | Generate tests from code/user stories | pytest, Jest, Vitest, JUnit, Playwright, Cypress |
| Self-Healing | Auto-fix broken selectors | Playwright, Cypress, Selenium |
| Flaky Test Detection | Diagnose intermittent failures | All major frameworks + CI logs |
| Coverage Analysis | Measure and report test coverage | Istanbul, pytest-cov, JaCoCo |
| API Contract Testing | Validate API schemas and responses | OpenAPI, Postman, Pact |

## Best Practices

1. **Always add `data-testid` attributes** to UI elements for stable selectors
2. **Use explicit waits** instead of `sleep()` — AI will recommend optimal wait strategies
3. **Keep tests isolated** — each test should be independent
4. **Parameterize test data** — use data-driven tests for variant coverage
5. **Review self-healed selectors** — AI suggestions should be human-verified before production

## Notes

- This skill generates test code only — it does not execute tests directly
- For CI/CD integration, combine with `ai-test-strategy-architect` skill
- Self-healing suggestions prioritize semantic selectors over CSS class selectors
- Coverage analysis requires access to test execution output files (JSON/XML format)
