---
name: "AI Test Strategy Architect"
description: "AI-powered test strategy and automation assistant — design comprehensive testing frameworks, generate unit/integration/e2e test cases, implement test automation for web/mobile/API, and build CI/CD testing pipelines. Covers Test-Driven Development (TDD), Behavior-Driven Development (BDD), property-based testing, and AI-augmented test generation. Built for QA engineers, software developers, test leads, and DevOps teams shipping reliable software. Keywords: test automation, unit testing, integration testing, e2e testing, TDD, BDD, CI/CD testing, Selenium, Playwright, Pytest, Jest, testing framework, test strategy, quality assurance, 测试自动化, 单元测试, 集成测试, 端到端测试, 测试策略, 质量保障."
version: "1.0.4"
---

# AI Test Strategy Architect

## Overview

Build testing that catches bugs before users do. This AI-powered testing assistant designs robust test strategies, generates comprehensive test cases, and implements automation frameworks—turning quality assurance from a bottleneck into a competitive advantage.

## Language Policy（语言策略 / SQP-3）

本技能同时提供中英双语触发词与内容，语言使用规则如下，避免输出语言飘移：

| 项目 | 规则 |
|---|---|
| 默认语言 | 跟随提问语言：中文提问用中文回答，英文提问用英文回答 |
| 术语 | 保留英文原词（`property-based testing`、`page object`、`flaky`），首次出现时括注中文 |
| 代码与配置 | 一律原样保留，不翻译标识符、字符串与注释语言之外的部分 |
| 混合提问 | 以正文主体语言为准；若仍不明确，直接询问一次，不要自行猜测 |
| 表格与模板 | 同一份产物内保持单一语言，不要中英混排 |
| 切换 | 用户任何时候说“用英文/用中文回答”，立即切换，不影响技术内容 |



## Triggers

- 中文触发词：`测试策略`、`单元测试`、`集成测试`、`E2E测试`、`自动化测试`、`测试用例`、`TDD`、`BDD`、`Playwright测试`、`Selenium`、`测试覆盖率`
- English triggers: `test strategy`, `unit testing`, `integration testing`, `e2e testing`, `automated testing`, `test cases`, `TDD`, `BDD`, `Playwright`, `Selenium`, `test coverage`, `CI/CD testing`

**Required context（至少满足一条才激活）**
1. 需要设计或改进一套测试策略、分层比例或门禁；或
2. 需要为具体代码/接口/流程设计用例；或
3. 需要把测试接入 CI/CD 并设定质量门禁；或
4. 需要诊断测试体系本身的健康问题（覆盖率虚高、flaky、断言强度不足）。

**Non-triggers（不激活）**

| 请求 | 为什么不归本技能 | 应转向 |
|---|---|---|
| “帮我修这个 bug” | 缺陷修复，不是测试设计 | 通用调试 |
| “这个接口返回 500，帮我看看” | 生产问题排查 | 运维/日志排查 |
| “压测一下能扛多少 QPS” | 性能工程，目标与方法都不同 | 性能测试工具（k6/Locust） |
| “做一次安全渗透测试” | 安全测试需专门授权与方法 | 安全测试流程 |
| “把这份需求文档总结一下” | 文档处理，无测试对象 | 文档摘要 |
| “安装 Playwright 环境” | 环境搭建操作 | 官方安装文档 |

**执行边界声明**：本技能输出测试代码、配置形态与策略文档，供你在自己的环境中
审阅后运行。它不执行测试、不写入你的仓库、不访问你的 CI。文中代码仅作参考材料。

## Features

### 1. Test Strategy Design
- Assess project requirements and risk profiles
- Design tailored testing pyramids (unit/integration/e2e ratios)
- Select appropriate testing frameworks per use case
- Define test data management strategies
- Create test environment specifications


**Worked example — risk-based scope for a payments-style service**

| Module | 失效影响 | 发生概率 | 风险分 | 测试投入 | 具体手段 | 门禁归属 |
|---|---|---|---|---|---|---|
| 保费计算 | 资金错误，监管风险 | 中 | 9 | 最高 | 属性测试 + 黄金样本回归 + 变更检测 | PR 阻断 + nightly 变异测试 |
| 投保校验 | 单用户受阻 | 高 | 6 | 高 | 边界表 + 参数化 | PR 阻断 |
| 支付回调 | 重复扣款 | 低 | 6 | 高 | 幂等性专项 + 故障注入 | PR 阻断 + nightly 故障注入 |
| 报表导出 | 内部使用 | 中 | 3 | 中 | 快照测试 | nightly 快照比对 |
| 邮件通知 | 体验问题 | 中 | 2 | 低 | 冒烟 + 手动抽查 | 不设门禁，仅冒烟 |
| 管理后台筛选 | 内部低效 | 低 | 1 | 最低 | 冒烟即可 | 不设门禁 |

评分方式：影响（1–5）× 概率（1–2），≥8 必须有属性测试与变更检测，
≤3 只做冒烟。这样把预算集中在真正会出钱的地方，而不是平均撒。

**测试环境规格清单（常被忽略的 5 项）**
1. 数据种子能否一键重建（不能就要先解决这个，否则一切自动化都是脆弱的）
2. 第三方依赖是否有稳定的测试替身（沙箱/契约/Mock 三选一）
3. 环境之间配置差异是否有单一来源（配置漂移是"本地能跑线上挂"的主因）
4. 测试数据是否含脱敏后的真实分布（用全是合法值的假数据测不出边界）
5. 每个环境的重置成本与时限（重置超过 10 分钟的流水线会被绕过）


### 2. Test Case Generation
- Generate unit tests from code functions/methods
- Create integration test scenarios from API specs
- Design end-to-end user journey tests
- Build property-based tests for edge cases
- Generate negative test cases (error handling)


**Worked example — 一个参数的完整用例矩阵（参数化而非堆砌）**

以 `calculate_discount(price, discount_percent, is_loyal)` 为例，不要写 12 个
独立函数，用一张表驱动：

| price | discount_percent | is_loyal | 期望 | 覆盖的意图 |
|---|---|---|---|---|
| 100.00 | 0 | False | 100.00 | 恒等 |
| 100.00 | 20 | False | 80.00 | 基本路径 |
| 100.00 | 20 | True | 76.00 | 忠诚用户叠加 |
| 100.00 | 100 | False | 0.00 | 上边界 |
| 0.00 | 50 | False | 0.00 | 零值 |
| 99.99 | 33 | False | 66.99 | 舍入 |
| -10.00 | 10 | False | ValueError | 负价 |
| 100.00 | -5 | False | ValueError | 下越界 |
| 100.00 | 150 | False | ValueError | 上越界 |

对应的参数化写法要点：把"期望异常"也放进同一张表，用哨兵值标记，
不要在参数化之外再补一批独立的异常测试——那会让两套用例逐渐分叉。

**属性测试该测什么（property-based，不是随机测试）**

对同一个函数，属性测试关心的是不变量，例如：
- 对任意合法输入，`0 <= result <= price`
- 对任意合法输入，`discount_percent` 单调不减时，`result` 单调不增
- 对任意合法输入，`result == round(result, 2)`
- 对任意合法输入，同样参数调用两次结果相同（纯函数性）

最小可运行的 Hypothesis 形态：

```python
from hypothesis import given, strategies as st

@given(
    price=st.floats(min_value=0, max_value=1e6, allow_nan=False),
    pct=st.floats(min_value=0, max_value=100, allow_nan=False),
    loyal=st.booleans,
)
def test_result_within_bounds(price, pct, loyal):
    r = calculate_discount(price, pct, loyal)
    assert 0 <= r <= price
    assert r == round(r, 2)
```

注意：这段代码是给你在自己环境运行的参考材料，本技能不代为执行。


### 3. Test Automation Implementation
- Scaffold test projects with proper structure
- Implement page object models for UI tests
- Set up API test frameworks with data-driven approaches
- Configure test parallelization and distribution
- Implement visual regression testing


**Worked example — page object 的正确粒度**

反例（把业务流程塞进 page object，导致一改就全崩）：

```python
class CheckoutPage:
    def buy_whole_flow(self, card):   # 不要这样
        ...
```

正例（page object 只暴露页面能力，流程留在测试里）：

```python
class ProductPage:
    def __init__(self, page): self.page = page
    def add_to_cart(self):
        self.page.get_by_test_id("add-to-cart").click
    def cart_count(self) -> int:
        return self.page.get_by_test_id("cart-item").count

class CheckoutPage:
    def __init__(self, page): self.page = page
    def pay_with(self, card: str, expiry: str, cvv: str):
        self.page.get_by_label("card number").fill(card)
        self.page.get_by_label("expiry").fill(expiry)
        self.page.get_by_label("cvv").fill(cvv)
        self.page.get_by_test_id("place-order").click
    def order_number(self) -> str:
        return self.page.get_by_test_id("order-number").inner_text
```

判据：page object 里不应出现断言（`assert` 属于测试），也不应出现跨页面跳转。
跳转留在测试用例里，页面对象只负责"这一页能做什么"。

**并行化的三条硬约束**
1. 数据隔离：并行 worker 不能共用同一条测试数据，用 worker id 生成唯一前缀。
2. 端口与临时目录：并行时端口冲突是最常见的"随机失败"，必须动态分配。
3. 共享服务：若必须共用一个外部服务（如支付沙箱），要么串行，要么限流——
   否则你会得到一批看起来像 flaky 的资源竞争失败。


### 4. CI/CD Pipeline Integration
- Design testing stages in CI/CD pipelines
- Configure test reporting and dashboards
- Set up automated quality gates
- Implement canary/feature flag testing strategies
- Create performance test thresholds in pipelines


**Worked example — 四阶段流水线与门禁**

| 阶段 | 运行内容 | 时限 | 失败处理 | 门禁指标 |
|---|---|---|---|---|
| commit (pre-push) | lint + 单元测试(受影响模块) | ≤ 60 s | 阻断提交 | 0 失败 |
| PR | 全量单元 + 集成 + 契约 | ≤ 8 min | 阻断合并 | 覆盖率不低于基线 |
| merge (main) | 全量 + E2E 冒烟 | ≤ 20 min | 阻断发布流水线 | 冒烟 100% 通过 |
| nightly | 全量 E2E + 性能 + 变异测试 | ≤ 2 h | 次日处理，不阻断 | 变异分趋势不下降 |

关键设计：把慢的、不稳定的放 nightly，把快的、确定的放 PR。
如果 PR 阶段超过 8 分钟，工程师会开始绕过它——这是流水线失效的真实起点。

**质量门禁配置示例（概念形态，按你的 CI 语法调整）**

```yaml
quality_gates:
  coverage:
    metric: line
    floor: 72            # 当前实际值 + 2，不要一上来写 90
    ratchet: true        # 只允许上升，不允许回落
    exclude: ["generated/*", "migrations/*"]
  flakiness:
    quarantine_threshold: 0.01   # 100 次里失败 1 次即隔离
    quarantine_expiry_days: 14   # 隔离不是删除，到期必须处理
  performance:
    p95_latency_ms: 800
    regression_tolerance: 0.10   # 允许 10% 波动，超过即失败
  blocking:
    - name: critical_path_e2e
      on_failure: stop_pipeline
    - name: visual_diff
      on_failure: require_human_approval   # 视觉差异必须人看
```

注意：以上为配置形态示例，需在用户自己的 CI 环境中运行与调整。


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

## Pyramid Ratios by Project Type

The classic 60/30/10 split is a starting point, not a law. Use this instead:

| 项目类型 | Unit | Integration | E2E | 额外层 | 理由 | 常见误判 |
|---|---|---|---|---|---|---|
| 纯前端 Web 应用 | 50% | 20%（组件/契约） | 30% | 视觉回归 | UI 是主要风险面，E2E 占比自然更高 | 把视觉回归当成 E2E 的替代品 |
| 后端 API 服务 | 60% | 35% | 5% | 契约测试 | 逻辑在服务端，E2E 只需关键链路 | 用 E2E 去覆盖所有业务分支 |
| 数据/ETL 管道 | 45% | 25% | 5% | 25% 数据质量测试 | 行数、空值率、分布漂移比功能更重要 | 只测转换函数，忽略数据质量层 |
| 移动端 | 55% | 20% | 25% | 设备矩阵冒烟 | 设备与系统版本碎片化推高 UI 层 | 只在一台真机上跑冒烟就算设备覆盖 |
| 金融/保险核心 | 65% | 25% | 10% | 属性测试 + 审计测试 | 计算正确性优先，且需可追溯 | 只靠单元测试，缺审计留痕测试 |
| 内部工具 | 40% | 30% | 30% | 探索式测试 | 用户少、变更快，重自动化反而拖慢 | 照搬 60/30/10 做全套自动化 |

**如何判断比例是否合适**
- E2E 占比高且经常红 → 逻辑下沉不足，把验证前移到集成层
- 单元覆盖高但线上仍有事故 → 断言太弱，引入变异测试检验"断言强度"
- 集成层几乎为零 → 多半是"只能整体起来才能测"，这是架构问题不是测试问题

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
        data = response.json
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
        orders = response.json["orders"]
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
        assert "error" in response.json
```

### Example 3: E2E Test with Playwright

**API 风格提醒（Python 与 JS 不同名，混用会静默失效）**

Playwright 的 Python 绑定用 snake_case，JavaScript/TypeScript 用 camelCase。
同一个断言在两种语言里名字不同：

| 意图 | Python | JS / TS |
|---|---|---|
| 可见 | `expect(loc).to_be_visible` | `expect(loc).toBeVisible` |
| 数量 | `expect(loc).to_have_count(1)` | `expect(loc).toHaveCount(1)` |
| 文本 | `expect(loc).to_have_text("ok")` | `expect(loc).toHaveText("ok")` |
| 非空 | `expect(loc).not_to_be_empty` | `expect(loc).not.toBeEmpty` |

Python 里写 `toBeVisible` 不会报语法错误，但会抛 `AttributeError`；更糟的情况是
被 IDE 自动补全"修正"成一个存在但语义不同的方法。**复制示例时先确认语言绑定。**
下方示例统一使用 Python（snake_case）风格。

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
    expect(page.locator('[data-testid="cart-item"]')).to_have_count(1)
    
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
    expect(page.locator('[data-testid="order-confirmation"]')).to_be_visible
    expect(page.locator('[data-testid="order-number"]')).not_to_be_empty
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

### Example 4: 数据管道（ETL）的测试策略

**Input:**
```
我们有一个每日跑批：从业务库抽数 → 清洗 → 计算保费指标 → 写入报表库。
目前没有测试，每次出问题都要人工对数。怎么设计测试？
```

**Output:**
```
ETL 的测试重点不是"函数对不对"，而是"数据对不对"。分四层：

第 1 层：转换逻辑单元测试（占比 40%）
  把清洗与计算函数抽成纯函数（输入 DataFrame → 输出 DataFrame），
  用小型固定样本断言。关键是让转换逻辑不依赖 IO。

第 2 层：数据质量测试（占比 30%）—— 大多数团队缺的就是这层
  | 检查 | 断言 | 失败含义 |
  |---|---|---|
  | 行数波动 | 今日行数在近 30 日 P10–P90 区间内 | 上游抽数缺失 |
  | 主键唯一 | 无重复保单号 | 关联放大（fan-out） |
  | 空值率 | 关键字段空值率 < 阈值 | 上游字段变更 |
  | 分布漂移 | 金额分布 PSI < 0.2 | 口径或业务突变 |
  | 汇总对账 | 明细合计 == 汇总表 | 口径不一致 |
  | 时间完整性 | 每个分区都有数据 | 跑批漏跑 |

第 3 层：端到端小样本回归（占比 20%）
  用 100 条脱敏真实数据跑完整管道，与上一次的黄金结果文件比对。
  黄金文件需要有明确的更新流程，否则会变成"永远批准"。

第 4 层：生产监控（占比 10%）
  把第 2 层的检查搬到生产，作为数据契约告警。

三个最常见的坑：
1. 用"全是合法值"的假数据 —— 测不出脏数据路径，务必混入脏样本
2. 没有幂等性测试 —— 同一天重跑两次结果必须一致
3. 把测试写在对生产库的直连上 —— 必须有独立的可重置环境
```

### Example 5: 从"覆盖率 85% 但仍在出事故"说起

**Input:**
```
我们覆盖率 85%，质量门禁也过了，但线上还是出低级事故。测试策略哪里有问题？
```

**Output:**
```
覆盖率衡量的是"代码被执行过"，不是"结论被验证过"。85% 且仍出事故，
通常是以下四种情况之一：

1. 断言太弱（最常见）
   症状：测试只写 assert result is not None
   检验：跑一次变异测试（mutmut / Stryker / PIT），变异分低于 40% 即确认
   修复：对每个分支断言具体值或具体不变量

2. 测试写成了实现镜像
   症状：改实现时测试必须同步改，且改完仍然绿
   检验：故意引入一个业务错误，看测试是否变红
   修复：从需求/规格推导期望值，不从当前实现推导

3. 关键路径没有端到端覆盖
   症状：单元全绿，但串起来就错
   检验：列出"出钱/出合规风险"的 3 条链路，看是否有跨层测试
   修复：这 3 条链路各补一个端到端用例，其余不必追求

4. 覆盖率数字被稀释
   症状：DTO、generated、migrations 计入分母
   修复：排除这些目录后重算，通常真实覆盖率会显著下降

两周可落地的改进顺序：
- 第 1 天：排除 generated/migrations，重算真实基线
- 第 2–3 天：对核心模块跑一次变异测试，拿到变异分
- 第 4–8 天：给 3 条关键链路各补 1 个端到端用例
- 第 9–10 天：把覆盖率门禁从"绝对值"改为"棘轮"（只升不降）

判断改进是否有效的唯一标准：变异分上升，而不是覆盖率上升。
```

### Example 6: 门禁设在哪里才不会被绕过

**Input:**
```
我们把覆盖率门禁设成 85%，结果工程师开始写"只为覆盖率"的测试。
门禁是不是设错了？
```

**Output:**
```
问题不在阈值，在门禁挂错了指标，也挂错了阶段。

三个常见错误与修正：

1. 门禁挂在"绝对值"上 → 改为棘轮（ratchet）
   绝对值会让团队围绕数字优化。棘轮只要求"不比上一次低"，
   把激励从"刷数字"改成"别变差"。

2. 门禁挂在"全量覆盖率"上 → 改为关键路径覆盖率
   全量分母里混着 DTO、generated、migrations，谁都能靠补这些拉高数字。
   只统计"出钱/出合规风险"的模块，数字会下降但可信度上升。

3. 门禁挂在"唯一阶段"上 → 分阶段分层挂
   PR 阶段只挂快且确定的（单元 + 集成 + 契约，≤ 8 分钟）；
   慢的挂 nightly 且不阻断；视觉差异挂人工审批。
   PR 阶段超过 8 分钟，工程师就会开始绕过它。

再补一条反刷分规则：新增代码的行覆盖率单独统计，
不允许用存量代码的高覆盖率去掩盖新增代码的低覆盖。

验证门禁是否健康的可观测信号：
- 门禁失败后，有多少次是"改了测试"而不是"改了代码"？前者占比过高即为刷分
- 变异分是否随覆盖率一起上升？不上升说明新增测试没有断言强度
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

## Ecosystem Status (as of 2026-11-17 / 截至 2026-11-17)

Tool versions and best practice shift quickly. Verify against official release
notes before committing to a stack.

| 关注点 | 需要确认什么 | 影响 |
|---|---|---|
| 浏览器自动化版本 | Playwright / Cypress / Selenium 当前主版本 | 等待机制与选择器 API 差异 |
| 变异测试工具链 | 与你的语言和测试框架是否兼容 | 决定能否把变异分纳入门禁 |
| CI 运行成本 | 并行 worker 的计费与上限 | 决定金字塔各层能跑多频繁 |
| 视觉回归方案 | SaaS 还是自托管 | 涉及截图是否出网（受监管行业敏感） |
| AI 生成测试的合入政策 | 本单位对生成代码的评审要求 | 决定人工检查点设在哪里 |

**最近动态（截至 2026-11-17，以官方发布为准）**
1. 变异测试与"断言强度"指标正从学术研究走向工程实践，部分团队已用它替代
   单纯的覆盖率门禁。
2. 视觉回归的自托管方案受关注度上升，主要驱动是数据驻留与合规要求。
3. AI 生成测试用例已成常见能力，行业关注点转向"生成用例的评审与可追溯"，
   而非生成数量。
4. 质量门禁的口径正在从"覆盖率绝对值"转向"棘轮 + 关键路径覆盖率 + 变异分"
   的组合，单纯提高覆盖率阈值被普遍认为会产生反向激励。
5. AI 生成测试用例的评审成为落地瓶颈：多数团队反馈瓶颈不在生成速度，而在
   "生成用例是否与需求一致、是否可追溯"，评审环节的人工成本被低估。
6. 以上为趋势描述，具体工具版本与能力请以官方最新发布为准。

## Testing Framework Comparison

| Framework | Best For | Languages | 学习曲线 | 并行能力 | 调试体验 | 适合团队规模 | 主要坑 | 何时不要用 | 多语言 API 差异风险 |
|---|---|---|---|---|---|---|---|---|---|
| Pytest | Python APIs, unit tests | Python | 低 | 中（pytest-xdist） | 好（--pdb、丰富报错） | 1–20 | fixture 作用域误用导致状态泄漏 | 需要浏览器级交互时 | 无（纯 Python） |
| Jest | JS/TS 单元与组件测试 | JS/TS | 低 | 好（内置） | 好 | 1–20 | mock 过深，测到 mock 而非实现 | 需要真实浏览器行为时 | 无（纯 JS/TS） |
| Vitest | Vite 生态单元测试 | JS/TS | 低 | 好 | 好 | 1–15 | 与 Jest 的 mock API 差异 | 非 ESM/老构建体系 | 无（纯 JS/TS） |
| JUnit 5 | Java 应用 | Java | 中 | 中 | 中 | 5–50 | 扩展模型复杂，配置易失控 | 快速原型阶段 | 无（纯 Java） |
| Playwright | Web E2E | TS, Python, Java | 中 | 好（内置分片） | 很好（trace viewer） | 2–30 | 自动等待让人误解为"不需要断言状态" | 需测极老浏览器 | 高：Python snake_case 与 JS camelCase 断言不同名 |
| Cypress | Web E2E（开发体验优先） | JS/TS | 低 | 需付费/自建 | 很好（时间旅行） | 1–15 | 多标签、多域限制 | 跨域/多窗口场景 | 无（仅 JS/TS） |
| Selenium | 遗留浏览器与网格 | 多语言 | 高 | 好（Grid） | 差（报错不直观） | 10+ | 等待与驱动版本地狱 | 新项目（有更好选择） | 中：多语言绑定的命名并不总是一致 |
| REST Assured | API 测试 | Java, Groovy | 中 | 好 | 中 | 5–30 | DSL 冗长，维护成本高 | 团队不以 Java 为主 | 无（Java/Groovy） |
| SuperTest | Node API 测试 | JavaScript | 低 | 好 | 好 | 1–10 | 只覆盖 HTTP 层，无契约能力 | 需要跨语言契约时 | 无（JavaScript） |
| Pact | 消费者驱动契约测试 | 多语言 | 中高 | 好 | 中 | 5–30 | Broker 运维被低估 | 单体应用、调用方单一 | 中：各语言 DSL 差异较大 |
| Hypothesis | 属性/不变量测试 | Python | 中 | 好 | 中（反例收缩优秀） | 2–20 | 策略写不好等于随机测试 | 纯 CRUD、无计算逻辑 | 无（仅 Python） |
| k6 / Locust | 性能与负载 | JS / Python | 中 | 好 | 中 | 2–20 | 把负载测试当功能测试跑 | 只需要单次基准时 | 中：k6 用 JS，Locust 用 Python，脚本不可互换 |

**选型判据（比"哪个更流行"更可靠）**：团队已有语言 > 调试体验 > 并行能力 >
生态插件。调试体验决定日常成本，流行度不决定。

## Version History

- **1.0.1** (2026-09-10)
  - Added worked examples to all four feature groups (risk-based scope table and
    environment checklist; parameterised case matrix and property-based invariants;
    page-object granularity and parallelism constraints; four-stage pipeline with
    quality-gate config)
  - Added "Pyramid Ratios by Project Type" (6 project types, 6 columns) and a
    self-check for whether your ratio is right
  - Expanded framework comparison from 3 to 10 columns and 8 to 12 rows
    (learning curve, parallelism, debugging, team size, main pitfall, when not to use)
  - Added Example 4 (ETL/data-pipeline strategy incl. data-quality checks) and
    Example 5 (high coverage but still shipping incidents)
  - Added "Ecosystem Status (as of 2026-09-10)"
  - Corrected Python Playwright assertions (`to_have_count`, `not_to_be_empty`)
- **1.0.2** (2026-09-28)
  - Fixed a real code defect in the Playwright example: `toBeVisible` (JS/TS
    camelCase) inside a Python snippet corrected to `to_be_visible`, and added a
    Python vs JS/TS assertion-name table explaining why the mix-up fails silently
    (SDI-4)
  - Added a Language Policy section covering default-language, terminology, code,
    mixed-language and switching rules (SQP-3)
  - Narrowed triggers with a required-context rule, a six-row non-trigger table and
    an explicit execution-boundary statement (SQP-1)
  - Added a 门禁归属 column to the risk-based scope table, a 常见误判 column to the
    pyramid-ratio table and a 多语言 API 差异风险 column to the framework comparison
  - Added Example 6 on where to place quality gates so they are not bypassed
  - Ecosystem status updated to 2026-09-28 with two added dynamics
- **1.0.0** (2026-05-15): Initial release
  - Test strategy design framework
  - Unit test generation
  - Integration test scaffolding
  - E2E test patterns (Playwright)
  - CI/CD integration guidance

**Last Updated**: 2026-11-17

## 本轮增量（2026-11-13）：复核维度与举例补充

> 本节为 2026-11-13 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Release Criteria**：

- 准出条件把「阻断级缺陷数」「关键路径用例通过率」「回滚方案演练结果」三项并列，任一不达标即不放行，避免用整体通过率掩盖关键路径失败。
- 对灰度发布单列「观测窗口时长与回滚触发阈值」，写明触发后由谁在多久内决策，避免准出通过但无人负责回滚。

**Test Pyramid / 分层策略**：

- 金字塔配比先按「变更频率 × 失效影响」给模块分级，高频高影响模块增加契约层与集成层投入，而非全系统统一比例。
- 对外部依赖不可控的接口，单列「契约测试 + 故障注入」两层，并在策略文档写明降级与超时假设，避免把不可控依赖全部压到端到端层。

### 新增复核维度表（2026-11-13）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 准出三项并列核验 | 测试负责人 + 发布经理 | 缺陷清单 + 关键路径报告 + 演练记录 | 三项是否逐条留痕、是否单独判定 | 高 | 仅作策略草稿，放行须授权人员确认 |
| 分层投入依据 | 测试负责人 | 变更频率与失效影响分级表 | 分级依据、外部依赖假设是否写明 | 中 | 需结合项目实际复核，不直接套用 |

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于测试策略与发布准出设计的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的、客户或案件的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送、系统登记）不适用本技能，应转由相应业务系统与授权人员处理。

**数据最小化**：仅处理完成当前任务所必需的最小数据集；对可识别个人、账户、持仓、健康、保单或未公开经营信息，优先脱敏、聚合或以标识符替代。不复制、不留存、不外传原始敏感数据；任何外部数据或服务的使用须以用户明确授权为前提，并保留可追溯的取数与复核留痕。

### 时效性说明

- 本期时效性核查：**截至 2026-11-13**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-17）：复核维度与举例补充

> 本节为 2026-11-17 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Pyramid Ratios by Project Type**：

- 分层配比表补「成本与反馈」两列：每层标注相对成本量级与反馈时效描述，草稿只记录口径，不代入具体金额或时长。
- 配比说明新增「倒置风险」占位：把确定性基础占比过低时可能出现的问题分栏描述，纸面标注需人工复核，不给出调整结论。

**Release Criteria**：

- 准出清单补「统计口径」一列：每条准出项标注是基于均值、通过率还是硬失败项，草稿只记录口径类型，不设定具体阈值。
- 回归对照新增「基线留痕」占位：当前观察与上一版本基线分栏，基线缺失的条目标注不可比较，需人工确认。

### 新增复核维度表（2026-11-17）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 分层成本与反馈 | 测试架构师 + 复核人 | 分层配比表 / 草稿 | 每层相对成本量级与反馈时效是否标注 | 中 | 纸面对照，结论须人工确认 |
| 准出统计口径 | 测试架构师 | 准出清单 | 每条准出项是否标注口径类型、基线是否留痕 | 中 | 文档记录，不构成放行结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于测试策略方法论参考的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及生产发布、准出放行与正式质量结论的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-17）

> 参考公开测试策略框架中「评测金字塔按不确定性分层、确定性基础承担主要信号」「金标准样本集自真实失败样本构建」「准出采用统计型闸门并保留回归基线」的思路，在准出章节补一个纸面小节：把确定性检查、录制回放、语义评测、人工抽检四类证据分层列明，并提示样本集齐备前不宜讨论优化、阈值须由具备资质的人员结合业务设定。

### 时效性说明

- 本期时效性核查：**截至 2026-11-17**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
