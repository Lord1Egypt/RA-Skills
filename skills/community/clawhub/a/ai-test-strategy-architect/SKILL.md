---
name: "AI Test Strategy Architect"
description: "AI-powered test strategy and automation assistant — design comprehensive testing frameworks, generate unit/integration/e2e test cases, implement test automation for web/mobile/API, and build CI/CD testing pipelines. Covers Test-Driven Development (TDD), Behavior-Driven Development (BDD), property-based testing, and AI-augmented test generation. Built for QA engineers, software developers, test leads, and DevOps teams shipping reliable software. Keywords: test automation, unit testing, integration testing, e2e testing, TDD, BDD, CI/CD testing, Selenium, Playwright, Pytest, Jest, testing framework, test strategy, quality assurance, 测试自动化, 单元测试, 集成测试, 端到端测试, 测试策略, 质量保障."
version: "1.0.0"
---

# AI Test Strategy Architect

## Overview

Build testing that catches bugs before users do. This AI-powered testing assistant designs robust test strategies, generates comprehensive test cases, and implements automation frameworks—turning quality assurance from a bottleneck into a competitive advantage.

## Triggers

- 中文触发词：`测试策略`、`单元测试`、`集成测试`、`E2E测试`、`自动化测试`、`测试用例`、`TDD`、`BDD`、`Playwright测试`、`Selenium`、`测试覆盖率`
- English triggers: `test strategy`, `unit testing`, `integration testing`, `e2e testing`, `automated testing`, `test cases`, `TDD`, `BDD`, `Playwright`, `Selenium`, `test coverage`, `CI/CD testing`

## Features

### 1. Test Strategy Design
- Assess project requirements and risk profiles
- Design tailored testing pyramids (unit/integration/e2e ratios)
- Select appropriate testing frameworks per use case
- Define test data management strategies
- Create test environment specifications

### 2. Test Case Generation
- Generate unit tests from code functions/methods
- Create integration test scenarios from API specs
- Design end-to-end user journey tests
- Build property-based tests for edge cases
- Generate negative test cases (error handling)

### 3. Test Automation Implementation
- Scaffold test projects with proper structure
- Implement page object models for UI tests
- Set up API test frameworks with data-driven approaches
- Configure test parallelization and distribution
- Implement visual regression testing

### 4. CI/CD Pipeline Integration
- Design testing stages in CI/CD pipelines
- Configure test reporting and dashboards
- Set up automated quality gates
- Implement canary/feature flag testing strategies
- Create performance test thresholds in pipelines

## Workflow

### Comprehensive Test Strategy Workflow

```
Phase 1: Assessment
├── Analyze project architecture
├── Identify critical user flows
├── Assess technical risks
├── Define quality metrics
└── Select testing tools

Phase 2: Design
├── Design test pyramid
├── Define test scope per layer
├── Create test data strategy
├── Document test environment needs
└── Plan test automation approach

Phase 3: Implementation
├── Set up test project structure
├── Implement unit tests
├── Build integration test suite
├── Create e2e test scenarios
└── Configure test runners

Phase 4: Automation
├── Integrate with CI/CD
├── Set up test reporting
├── Configure parallel execution
├── Implement test monitoring
└── Create quality dashboards

Phase 5: Maintenance
├── Review test effectiveness
├── Optimize slow tests
├── Update for new features
└── Archive obsolete tests
```

### Quick Test Generation Workflow

```
1. INPUT: Source code or feature description
   ↓
2. ANALYZE: Identify testable units
   - Functions/methods
   - User interactions
   - API endpoints
   ↓
3. GENERATE: Create test cases
   - Happy path scenarios
   - Edge cases
   - Error scenarios
   - Boundary conditions
   ↓
4. VALIDATE: Run tests, fix failures
   ↓
5. OPTIMIZE: Improve coverage and speed
```

## Input Examples

### Example 1: Function to Unit Test

**Input Code:**
```python
def calculate_discount(price: float, discount_percent: float, is_loyal: bool) -> float:
    """
    Calculate final price after discount.
    
    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)
        is_loyal: Whether customer is a loyalty member
    
    Returns:
        Final price after discount
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    
    discount_multiplier = 1 - (discount_percent / 100)
    
    if is_loyal:
        # Loyalty members get extra 5% off
        final_multiplier = discount_multiplier * 0.95
    else:
        final_multiplier = discount_multiplier
    
    return round(price * final_multiplier, 2)
```

**Generated Test Cases:**
```python
import pytest
from your_module import calculate_discount

class TestCalculateDiscount:
    """Unit tests for calculate_discount function"""
    
    # Happy path tests
    def test_no_discount_returns_original_price(self):
        """No discount should return the original price"""
        assert calculate_discount(100.00, 0, False) == 100.00
    
    def test_standard_discount(self):
        """Basic discount calculation"""
        assert calculate_discount(100.00, 20, False) == 80.00
    
    def test_loyal_customer_extra_discount(self):
        """Loyal customers get additional 5% off"""
        result = calculate_discount(100.00, 20, True)
        expected = round(100 * 0.80 * 0.95, 2)  # 76.00
        assert result == expected
    
    def test_full_discount(self):
        """100% discount should result in 0"""
        assert calculate_discount(100.00, 100, False) == 0.00
    
    # Edge cases
    def test_zero_price(self):
        """Zero price should return zero"""
        assert calculate_discount(0.00, 50, False) == 0.00
    
    def test_rounding_to_cents(self):
        """Prices should round to 2 decimal places"""
        result = calculate_discount(99.99, 33, False)
        assert result == round(99.99 * 0.67, 2)
    
    # Error cases
    def test_negative_price_raises_error(self):
        """Negative price should raise ValueError"""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(-10.00, 10, False)
    
    def test_negative_discount_raises_error(self):
        """Negative discount should raise ValueError"""
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100.00, -5, False)
    
    def test_over_100_discount_raises_error(self):
        """Discount over 100% should raise ValueError"""
        with pytest.raises(ValueError, match="Discount must be between"):
            calculate_discount(100.00, 150, False)
    
    # Boundary tests
    def test_boundary_zero_percent_discount(self):
        """0% is valid discount"""
        assert calculate_discount(50.00, 0, False) == 50.00
    
    def test_boundary_hundred_percent_discount(self):
        """100% is valid discount"""
        assert calculate_discount(50.00, 100, False) == 0.00
```

### Example 2: API Integration Test

**Input:** OpenAPI endpoint definition
```yaml
paths:
  /api/v1/users/{userId}/orders:
    get:
      summary: Get user orders
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, shipped, delivered]
      responses:
        '200':
          description: List of orders
        '401':
          description: Unauthorized
        '404':
          description: User not found
```

**Generated Integration Test:**
```python
import pytest
import requests
from typing import Dict

BASE_URL = "https://api.example.com"
HEADERS = {"Authorization": "Bearer <test_token>"}

class TestUserOrdersAPI:
    """Integration tests for User Orders endpoint"""
    
    @pytest.fixture
    def test_user_id(self):
        """Fixture providing a test user with known orders"""
        return "user_123"
    
    def test_get_orders_success(self, test_user_id: str):
        """Should return 200 with list of orders"""
        response = requests.get(
            f"{BASE_URL}/api/v1/users/{test_user_id}/orders",
            headers=HEADERS
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)
    
    def test_get_orders_with_status_filter(self, test_user_id: str):
        """Should filter orders by status"""
        response = requests.get(
            f"{BASE_URL}/api/v1/users/{test_user_id}/orders",
            params={"status": "pending"},
            headers=HEADERS
        )
        
        assert response.status_code == 200
        orders = response.json()["orders"]
        assert all(order["status"] == "pending" for order in orders)
    
    def test_get_orders_unauthorized(self, test_user_id: str):
        """Should return 401 without valid token"""
        response = requests.get(
            f"{BASE_URL}/api/v1/users/{test_user_id}/orders"
        )
        
        assert response.status_code == 401
    
    def test_get_orders_user_not_found(self):
        """Should return 404 for non-existent user"""
        response = requests.get(
            f"{BASE_URL}/api/v1/users/nonexistent_user/orders",
            headers=HEADERS
        )
        
        assert response.status_code == 404
        assert "error" in response.json()
```

### Example 3: E2E Test with Playwright

**Input:** User journey description
```
User flow: Login -> Add item to cart -> Checkout -> Verify order confirmation
```

**Generated E2E Test:**
```python
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def logged_in_page(page: Page):
    """Fixture that logs in user before each test"""
    page.goto("https://shop.example.com/login")
    page.fill('[name="email"]', "test@example.com")
    page.fill('[name="password"]', "testpassword123")
    page.click('[type="submit"]')
    page.wait_for_url("**/dashboard")
    return page

def test_complete_checkout_flow(logged_in_page: Page):
    """End-to-end test: Login -> Add to cart -> Checkout -> Confirmation"""
    page = logged_in_page
    
    # Step 1: Browse to product
    page.goto("https://shop.example.com/products/widget-pro")
    page.click('[data-testid="add-to-cart"]')
    
    # Step 2: Verify cart
    page.click('[data-testid="cart-icon"]')
    expect(page.locator('[data-testid="cart-item"]')).toHaveCount(1)
    
    # Step 3: Proceed to checkout
    page.click('[data-testid="checkout-button"]')
    page.fill('[name="shipping_address"]', "123 Test Street")
    page.fill('[name="zip_code"]', "12345")
    page.click('[data-testid="continue-payment"]')
    
    # Step 4: Complete payment
    page.fill('[name="card_number"]', "4242424242424242")
    page.fill('[name="expiry"]', "12/28")
    page.fill('[name="cvv"]', "123")
    page.click('[data-testid="place-order"]')
    
    # Step 5: Verify confirmation
    expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible()
    expect(page.locator('[data-testid="order-number"]')).not_toBeEmpty()
```

## Output Templates

### Template: Test Strategy Document
```markdown
# Test Strategy Document

## Project Overview
- Project Name: [Name]
- Version: [Version]
- Test Scope: [What's in/out]

## Quality Objectives
| Metric | Target | Measurement |
|--------|--------|-------------|
| Code Coverage | >80% | Codecov |
| Bug Escape Rate | <5% | Bug Tracker |
| Test Execution Time | <10 min | CI Pipeline |

## Test Pyramid

        ╱╲
       ╱  ╲
      ╱ E2E╲         [Few - 10%]
     ╱──────╲
    ╱Integration╲     [Some - 30%]
   ╱────────────╲
  ╱  Unit Tests  ╲   [Many - 60%]
 ╱────────────────╲

## Testing Tools

| Layer | Tool | Language |
|-------|------|----------|
| Unit | Pytest | Python |
| Integration | pytest | Python |
| E2E | Playwright | TypeScript |
| API | REST Assured | Java |

## Test Environments
- Dev: https://dev.example.com
- Staging: https://staging.example.com
- Production: https://example.com

## Test Data Strategy
- [Strategy details]

## Release Criteria
- [ ] All critical tests pass
- [ ] Coverage meets target
- [ ] No P0 bugs open
```

## Best Practices

### For Test Design
1. **Follow FIRST principles:** Fast, Independent, Repeatable, Self-validating, Timely
2. **Name tests descriptively:** `test_user_cannot_login_with_invalid_password`
3. **Test one thing per test:** Easier debugging and maintenance
4. **Use data-driven tests:** Reduce duplication with parameterized tests
5. **Test edge cases:** Empty inputs, null values, maximum limits

### For Test Automation
1. **Prioritize stability:** Flaky tests are worse than no tests
2. **Keep tests fast:** Slow tests don't run often
3. **Use page objects:** Encapsulate UI structure changes
4. **Isolate tests:** No shared state between tests
5. **Clean up after yourself:** Reset what you change

### For CI/CD Integration
1. **Fail fast:** Run fastest tests first
2. **Parallelize:** Split tests across workers
3. **Report properly:** Generate actionable reports
4. **Set quality gates:** Block releases below thresholds
5. **Monitor trends:** Track flakiness over time

## Testing Framework Comparison

| Framework | Best For | Languages |
|-----------|----------|-----------|
| Pytest | Python APIs, unit tests | Python |
| Jest | JavaScript/TypeScript | JS/TS |
| JUnit 5 | Java applications | Java |
| Playwright | Web E2E testing | TS, Python |
| Cypress | Web E2E testing | JS/TS |
| Selenium | Legacy browser testing | Multi |
| REST Assured | API testing | Java, Groovy |
| SuperTest | Node.js API testing | JavaScript |

## Version History

- **1.0.0** (2026-05-15): Initial release
  - Test strategy design framework
  - Unit test generation
  - Integration test scaffolding
  - E2E test patterns (Playwright)
  - CI/CD integration guidance
