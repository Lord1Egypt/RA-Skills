---
name: functional-test-case-standard
description: Generate and evaluate functional test cases following standardized quality dimensions. Use when creating test cases, reviewing test case documents, analyzing test case quality, scoring test cases, or when the user mentions test case templates, test case evaluation, test case standards, or test case quality assessment. Supports Markdown and XMind mindmap output formats with version management.
---

# Functional Test Case Standard

## Overview

This skill provides standardized guidelines for writing high-quality functional test cases and an 8-dimension evaluation framework for assessing test case quality.

**Core Features**:
- ✅ Standardized test case design with 15+ design methods
- ✅ 8-dimension quality evaluation framework with scoring
- ✅ Deep requirement analysis using 5 analysis methods
- ✅ Dual output formats: Markdown (default) and XMind mindmap
- ✅ Two export modes: Review dimension and Execution dimension
- ✅ Timestamp-based version management for traceability

## Requirement Analysis Methodology

Before designing test cases, perform deep requirement analysis using these 5 methods to extract all test details:

### 1. Sentence-by-Sentence Analysis Method
Analyze each sentence in the requirement document to identify:
- **Condition words**: if, when, unless, only if, etc.
- **Action words**: click, input, select, submit, delete, etc.
- **State words**: display, hide, enable, disable, active, inactive, etc.
- **Data words**: create, read, update, delete, calculate, validate, etc.

**Output**: Each identified element becomes a verification item.

**Example**:
- Requirement: "When user clicks Submit button, if all required fields are filled, display success message and redirect to order list."
- Extracted verifications:
  - Condition: all required fields filled → test with valid/invalid combinations
  - Action: click Submit button → verify button is clickable and responsive
  - State: display success message → verify exact message text
  - Data: redirect to order list → verify correct page navigation

### 2. Business Process Analysis Method
Identify the complete business flow from start to end:
- **Process nodes**: Each step in the workflow
- **Decision branches**: All if-else or switch conditions
- **Exception exits**: Error handling, timeout, cancel, rollback
- **Parallel flows**: Concurrent processes or independent branches

**Output**: Each node and branch becomes a test scenario.

**Example** (Order Flow):
- Node 1: Create order → test with valid/invalid products
- Node 2: Payment → test successful payment, payment failure, timeout
- Node 3: Ship → test shipping with/without inventory
- Branch: Payment failure → test retry, cancel, refund flows

### 3. Data Flow Analysis Method
Trace data through its complete lifecycle:
- **Data acquisition**: Where does data come from? (user input, API, database, third-party)
- **Data processing**: How is data transformed? (calculation, validation, formatting)
- **Data storage**: Where is data saved? (database, cache, file, session)
- **Data display**: How is data presented? (UI, report, export, notification)

**Output**: Each data transformation point becomes a verification item.

**Example** (User Registration):
- Acquisition: user enters username, email, password
- Processing: validate format, encrypt password, check uniqueness
- Storage: insert into users table, send to CRM system
- Display: show success message, send confirmation email

### 4. State Transition Analysis Method
Model the system as a finite state machine:
- **Identify all states**: Draft, Pending, Approved, Rejected, Completed, Cancelled, etc.
- **Identify transition conditions**: What triggers state changes?
- **Identify valid transitions**: Allowed state changes
- **Identify invalid transitions**: Disallowed state changes (should show error)
- **Identify self-transitions**: Staying in the same state after action

**Output**: Each valid and invalid transition becomes a test case.

**Example** (Order Status):
- Valid: Draft → Pending (submit), Pending → Approved (approve), Approved → Shipped (ship)
- Invalid: Draft → Shipped (skip states), Shipped → Pending (reverse), Rejected → Approved (without revision)

### 5. User Scenario Analysis Method
Analyze from different user perspectives:
- **Different roles**: Admin, Manager, Regular User, Guest, etc.
- **Normal scenarios**: Happy path, typical usage
- **Exception scenarios**: Error handling, edge cases, abnormal conditions
- **Extreme scenarios**: High concurrency, large data volume, network failure, system timeout

**Output**: Each role-scenario combination becomes a test case.

**Example** (File Upload):
- Admin + Normal: upload valid file within size limit
- User + Exception: upload oversized file, wrong format
- Guest + Extreme: upload during network timeout, concurrent uploads

### Requirement Analysis Workflow

1. **Read requirement document** thoroughly (do not skip any section)
2. **Apply all 5 analysis methods** to extract test details
3. **Organize results** into:
   - Functional module inventory
   - Business rule inventory
   - Exception scenario inventory
   - Test data inventory
4. **Map to test cases** using design methods from Test Design Methodology section

## Output Format Selection

This skill supports two output formats with user-selectable options:

### Format Mode

| Format | Trigger | Description |
|--------|---------|-------------|
| **Markdown** (default) | User does not specify format | Generate standard Markdown test case document |
| **XMind Mindmap** | User explicitly requests "mindmap format", "XMind format", or "both md and xmind" | Additionally generate XMind mindmap file for visual review |

### Export Dimension

| Dimension | Use Case | Structure | When to Use |
|-----------|----------|-----------|-------------|
| **Review Dimension** (default) | Quality evaluation, peer review, requirement coverage analysis | Organized by: Module → Feature → Test Point → Verification Items (focus on completeness and coverage) | When stakeholders need to review test case coverage, during requirement review meetings, for quality audits |
| **Execution Dimension** | Test execution, automation, step-by-step testing | Organized by: Module → Test Case → Steps → Expected Results (focus on executability and traceability) | When testers execute test cases, for automation script generation, during test execution phase |

### User Selection Guide

**Ask user before generation**:
1. "Which output format do you prefer? (Markdown only / Markdown + XMind mindmap)"
2. "Which export dimension? (Review dimension for coverage analysis / Execution dimension for test execution)"

**Default behavior**: If user does not specify, generate Markdown format with Review dimension.

### XMind Mindmap Structure

**Review Dimension Structure**:
```
Product Requirement Name
├── I. Module Name
│   ├── 1.1 Sub-feature Name
│   │   ├── 1.1.1 Function Point
│   │   │   ├── Test Point: Condition Verification
│   │   │   │   ├── [ ] Verification Item 1
│   │   │   │   ├── [ ] Verification Item 2
│   │   │   │   └── [ ] Verification Item 3
│   │   │   └── Test Point: Business Rule Verification
│   │   │       ├── [ ] Verification Item 1
│   │   │       └── [ ] Verification Item 2
```

**Execution Dimension Structure**:
```
Product Requirement Name
├── I. Module Name
│   ├── 1.1 Sub-feature Name
│   │   ├── TC-001: [Module][Platform] Feature - Condition - Validation
│   │   │   ├── Precondition: ...
│   │   │   ├── Steps
│   │   │   │   ├── 1. ...
│   │   │   │   ├── 2. ...
│   │   │   │   └── 3. ...
│   │   │   ├── Expected Result
│   │   │   │   ├── 1. ...
│   │   │   │   ├── 2. ...
│   │   │   │   └── 3. ...
│   │   │   └── Priority: P0/P1/P2
```

## Version Management

### Timestamp-Based Versioning

Every test case generation creates a versioned file to enable traceability and historical comparison.

**File Naming Convention**:
```
{requirement-name}-v{MMdd_HHmmss}.md
{requirement-name}-v{MMdd_HHmmss}.xmind
```

**Timestamp Format**:
- Format: `MMdd_HHmmss` (MonthDay_HourMinuteSecond)
- Example: `0318_143052` means March 18, 14:30:52

**Example**:
- Requirement: "User Registration Enhancement"
- Generated files:
  - `user-registration-enhancement-v0318_143052.md`
  - `user-registration-enhancement-v0318_143052.xmind` (if XMind requested)

**Version Management Benefits**:
- ✅ All historical versions are preserved
- ✅ Easy comparison between different generations
- ✅ Trace test case evolution over time
- ✅ Support rollback to previous versions if needed

**Version Comparison**:
When user requests comparison between versions:
1. List all available versions with timestamps
2. Show differences in: test case count, coverage changes, priority adjustments
3. Highlight added/modified/removed test cases

## Design Principles

### Functional Item as Unit
Design test cases by functional item. Group related functional points by business or operation type into "functional items" — each item contains one or more similar functional points. For a given functional item, input a specific set of data or operation sequence, and verify the unique output result for each functional point within that item.

### Core Principles
1. **Operation Granularity**: Each case focuses on one group of similar functional items. Steps must be clear and the target explicit.
2. **Input-Output One-to-One Mapping**: Define a unique input set for the functional item, and strictly verify the corresponding output result. Ensure both test coverage and result judgment are unambiguous.
3. **Clear Boundaries**: Functional item boundaries are well-defined. Do not cross-item test. Avoid redundancy and duplicate operations.
4. **Case Independence**: Design each case to be self-contained with no inter-case dependencies. Clear boundaries between functional items minimize redundancy and maximize maintainability.

## Layered Testing Strategy (Test Pyramid)

Understand test layering to avoid over-reliance on a single test type. The pyramid guides resource allocation and test design focus for functional testing.

```
        /\
       /  \     E2E Tests (fewer, slower, high maintenance)
      /----\    ————————————————————————————————————————
     /      \   API / Integration Tests (moderate count, faster)
    /--------\  ————————————————————————————————————————
   /          \ Unit / Component Tests (most, fastest, cheapest)
  /------------\
```

| Layer | Scope | Speed | Maintenance | When to Design Cases Here |
|-------|-------|-------|------------|---------------------------|
| **Unit** | Single function/class | <100ms | Low | Complex business logic, calculation rules, state machines |
| **Integration** | Module interactions | <1s | Medium | Database operations, message queues, third-party service calls |
| **API** | Interface contracts | <1s | Medium | Parameter validation, response structure, error codes, auth |
| **E2E** | Full user workflow | Seconds~minutes | High | Cross-module business flows, user-facing critical paths |

**Guidelines**:
- Push tests as low in the pyramid as possible.
- E2E cases should cover only cross-module critical paths and user journeys.
- API cases should validate all parameter combinations and error responses.
- Unit tests should cover all branches and boundary conditions of business logic.

## Test Case Granularity

Default adoption: **Level 2 granularity**.

| Level | Definition | Characteristics | When to Use |
|-------|-----------|-----------------|-------------|
| **Level 1** | Validates a single, independent, indivisible functional point. The smallest functional verification unit with clear input and expected output. | Finest granularity; each case tests one boundary or rule. | When boundary values and independent rules need precise isolation. |
| **Level 2 (Default)** | Groups and merges multiple Level-1 points of the same type or related functional points into a small category. | Integrates similar points for systematic organization; easier management and maintenance. | **Default choice** for functional test cases. Balances coverage and maintainability. |
| **Level 3** | Further integrates Level-2 cases of the same type or business relation into a large category. | Broader business scenario focus; higher-level test perspective; lower maintenance cost. | When a high-level overview of module coverage is needed. |

### Level 2 Granularity Example

**Requirement**: Username restriction: length 6-20, lowercase English letters and digits only.

**Level 2 case**:
- **Name**: [User Management][WEB] User Registration - Username Length Validation
- **Steps**:
  1. Enter username with length below 6 characters
  2. Enter username with length above 20 characters
- **Expected Results**:
  1. Display error: "Username must be between 6-20 characters"
  2. Display error: "Username must be between 6-20 characters"

For detailed granularity examples, see [reference.md](reference.md).

## Naming Convention

**Unified format**: **[Module][Platform] Feature - Condition - Validation Point**

- **Module**: The business module name (e.g., User Management, Order Processing)
- **Platform**: WEB / APP / H5 / API
- **Feature**: The functional item under test
- **Condition**: The specific input condition or rule
- **Validation Point**: The verification point or operation being tested

**Naming principles**:
- Use the functional item's input condition as the naming description. Keep it concise.
- Specific inputs should be included; expected results are optional to avoid overly long names.
- Avoid vague words like "verify" or "test".

**Examples**:
- `[Feedback][APP] Feedback Creation - Content - Length Validation`
- `[Promotion][WEB] Red Packet Campaign - Manual Stop - Impact Validation`
- `[OOH Management][WEB] OOH File Import - Template - Sales Region3 Required Field`

## Case ID

**Format**: `primary_module_secondary_module_sequence_number`

- Example: `user_reg_001`, `order_create_014`, `product_import_005`
- Must be unique within the project
- Should reflect module hierarchy for easy location

## Required Fields

| Field | Required | Description |
|-------|----------|-------------|
| Case Name | Yes | Follow naming convention; concise input-condition-based description |
| Case ID | Yes | `primary_module_secondary_module_sequence_number` |
| Precondition | No | Prerequisites, specific inputs, and materials needed for the test |
| Test Steps | Yes | Clear, executable operation steps with specific UI elements |
| Expected Result | Yes | Unique, clear output result for the functional item, including state changes |
| Case Type | Yes | Functional / Smoke / Main-Flow / Single-API / API-Flow |
| Priority | Yes | P0(blocking/high) / P1(core/medium) / P2(normal/low) |
| Project | Yes | The project this case belongs to |
| Version | Yes | The version this case belongs to |
| Module | Yes | The module this case belongs to |
| Postcondition | No | Impact scope; fill when requirements change |

## Case Type Definitions

| Type | Description |
|------|-------------|
| **Functional Test Case** | Precisely designed for specific functional points with clear input and output. Example: verify username length limits, covering max, min, and empty boundary cases. |
| **Smoke Test Case** | Selected P0 cases from the test suite. Quickly validates whether critical main functions are available to determine if deeper testing can proceed. |
| **Main-Flow Business Case** | Designed according to business processes, covering the full lifecycle from start to end. Example: User A creates an order -> B processes it -> C approves -> D completes payment. |
| **Single-API Case** | Validates interface input parameters: required fields, empty values, wrong types, length overflow, etc. |
| **API Business Flow Case** | Uses interface operations to flow through the entire business process from start to end, validating business process integrity. |

## Test Design Methodology

Design methods are categorized into 5 groups. Select methods based on the functional item's characteristics.

### 1. Input Domain Methods
- **Equivalence Class Partitioning**: Divide input domain into valid and invalid equivalence classes. Test one representative from each class.
- **Boundary Value Analysis**: Test values at boundaries (min, max, min-1, max+1, typical values, empty/null).

**Best for**: Form fields, numeric ranges, length limits, date ranges, enum values.

### 2. Combination Methods
- **Decision Table**: Use when multiple conditions interact to produce different actions. List all condition combinations.
- **Cause-Effect Graphing**: Map causes to effects with constraint relationships (AND, OR, NOT, M, O, R, I).
- **Orthogonal Testing**: Use orthogonal arrays to reduce N-dimensional combination explosion to representative subsets.
- **Pairwise Testing**: Test all possible pairs of parameter values (Pairwise / n-wise).

**Best for**: Multi-field forms, configuration combinations, filter combinations, permission matrices.

### 3. Flow & State Methods
- **Scenario-Based Testing**: Design test scenarios based on business processes (normal flow, alternative flows, exception flows).
- **State Transition Testing**: Model system as a finite state machine. Test all valid transitions, invalid transitions, and self-transitions.
- **Business Process Diagram Method**: Derive test paths from business process diagrams (BPMN).

**Best for**: Approval workflows, order lifecycles, stateful entities, multi-step operations.

### 4. Experience-Based Methods
- **Error Guessing**: Based on past defect data and experience, predict likely failure points and design targeted test cases.

**Best for**: Complex legacy systems, areas with high historical defect density, regression testing of fixed defects.

### 5. Modern Methods
- **Risk-Based Testing**: Assign risk score = Impact × Probability. Prioritize test effort by risk. Use FMEA for systematic analysis.
- **Data-Driven Testing**: Separate test logic from test data. Store data in CSV/Excel/DB. Same case runs with multiple data sets.
- **Keyword-Driven Testing**: Abstract operations as reusable keywords (e.g., "Login", "Search", "Verify").
- **Model-Based Testing**: Generate tests from state machines, decision trees, or AI models.
- **Fuzzing**: Design test cases using random, malformed, or unexpected inputs as test data to cover edge cases.
- **Property-Based Testing**: Design invariant properties (e.g., "sorting output must be ordered") and generate test data to verify them.

**Best for**: Regression test case design, complex stateful system test design.

### Method Selection Guide

| Functional Item Characteristic | Recommended Methods |
|-------------------------------|--------------------|
| Input forms with multiple fields | Equivalence class + Boundary value + Decision table |
| Business workflows with approvals | Scenario + State transition + Error guessing |
| Configuration / permission matrix | Pairwise + Decision table |
| API parameter validation | Boundary value + Equivalence class + Error guessing |
| Complex calculation logic | Equivalence class + Boundary value + Property testing |
| Unknown / new features | Risk-based testing + Error guessing |

## Field Rules

### Precondition
- Not required if none. Only fill when prerequisites are necessary.
- Must include: account role, permissions, system data state, or specific test data.
- If the case cannot execute without certain conditions, they must be documented.

### Test Steps
- Number sequentially: `1. 2. 3.`
- Be specific to button names, menu paths, field names.
- Input data must specify exact values.
- For Level 2 granularity: each step tests one boundary/condition within the same functional item.
- Keep 2-5 steps per case; split if exceeding 7 steps.

### Expected Result
- Must be specific, observable, and verifiable.
- Each step has a corresponding expected result.
- Include state changes during the operation.
- Avoid vague phrases like "display correctly" or "function normally".
- For errors: include exact error message text.
- Must be independently judgeable as pass/fail.

### Priority Assignment
- **P0 / High**: Core business paths, blocking issues, main workflows
- **P1 / Medium**: Important features, frequently used functions
- **P2 / Low**: General features, secondary functions, edge scenarios
- Never assign all cases to a single priority level

## Test Data Strategy

### Data-Driven Testing
Separate test logic from test data. Store data in external files (CSV, Excel, JSON, DB). The same test case executes with multiple data sets.

**When to use**: Login with multiple account types, form submission with various valid/invalid inputs, bulk import with different file formats.

**Template**:
```
| Data Set | Input | Expected Result |
|----------|-------|-----------------|
| Valid-1  | "user01" | Success |
| Valid-2  | "user123456" | Success |
| Invalid-1| "" | Error: username required |
| Invalid-2| "ab" | Error: min length 6 |
```

### Parameterization Design
For cases that differ only in input values, design one case with parameters:
- Use placeholders like `{username}`, `{password}`, `{amount}`
- Record parameter constraints in the "Test Data" field
- Specify value ranges and boundary values

### Mock / Stub Strategy
When dependencies are unavailable or unstable during test design:
- Document which external systems are mocked
- Specify mock response data for positive and negative scenarios

## Case Lifecycle

```
Create -> Review -> Maintain -> Archive
```

| Stage | Key Activities | Decision Criteria |
|-------|---------------|-------------------|
| **Create** | Write case following standard; self-review before submission | Completeness of fields, design rationale clear |
| **Review** | Peer review or group review; focus on coverage gaps and design clarity | Coverage ≥ 90% of requirements; no empty fields; steps clear and specific |
| **Maintain** | Update case when requirements change; add cases for new defects | Review within 1 sprint of requirement change |
| **Archive** | Archive obsolete cases; do not delete (for audit trace) | Case no longer applicable for 2+ versions |

### Maintenance Triggers
- Requirement changes (functional or UI)
- Defect found in production not covered by existing cases
- Test data or environment changes
- Process optimization (merge/split cases)

## Common Word Constraints

Use consistent terminology across the team:

| Preferred | Alternatives to Avoid |
|-----------|----------------------|
| Create | Add, New, Insert |
| Query | Filter, Search |
| Edit | Modify, Update |
| Delete | Remove, Clear |
| Submit | Save, Confirm |
| Import | Upload (file scenarios only) |
| Export | Download (file scenarios only) |

## 8-Dimension Quality Evaluation Framework

Evaluate each test case author across these 8 dimensions (0-10 scale):

### 1. Naming Convention
- 9-10: >90% follow [Module][Platform] Feature - Condition - Validation Point format
- 7-8: 60-90% follow format, some inconsistency
- 5-6: 30-60% follow format, mixed styles
- 3-4: <30% follow format, mostly free-form
- 0-2: No format consistency, names unclear

### 2. Structural Integrity
- 9-10: All cases have steps + expected result with substance; preconditions filled when needed
- 7-8: >80% complete, minor omissions
- 5-6: 50-80% complete, noticeable gaps
- 3-4: <50% complete, many empty fields
- 0-2: Mostly template shells without content

### 3. Step Executability
- 9-10: Steps specific to buttons/fields/menus, directly executable by anyone
- 7-8: Mostly specific, some vague descriptions
- 5-6: Mix of specific and vague steps
- 3-4: Mostly vague, hard to execute consistently
- 0-2: Steps are empty or meaningless

### 4. Expected Result Verifiability
- 9-10: Each step has specific, quantifiable, observable expected result
- 7-8: Most have substance, some are vague
- 5-6: About half are specific, half vague or empty
- 3-4: Mostly vague like "display correctly"
- 0-2: Expected results empty or missing

### 5. Test Design Method Diversity
- 9-10: Uses 4+ methods from the 5 categories above
- 7-8: Uses 3 methods with good coverage
- 5-6: Uses 2 methods
- 3-4: Uses 1 method primarily
- 0-2: No discernible design method

### 6. Positive/Negative Coverage
- 9-10: Balanced ratio (1:1 to 3:1), good exception coverage
- 7-8: Ratio 3:1 to 5:1, some exception coverage
- 5-6: Ratio 5:1 to 10:1, limited exceptions
- 3-4: Mostly positive cases, rare negatives
- 0-2: Almost exclusively positive cases

### 7. Priority Rationality
- 9-10: Well-distributed across P0/P1/P2 or High/Medium/Low
- 7-8: Mostly reasonable, minor imbalances
- 5-6: Noticeable imbalance (e.g., 70%+ in one level)
- 3-4: Severe imbalance (e.g., 90%+ in one level)
- 0-2: All cases same priority, no differentiation

### 8. Test Data Specificity
- 9-10: >50% cases include specific input values
- 7-8: 30-50% include specific values
- 5-6: 10-30% include specific values
- 3-4: <10% include specific values
- 0-2: No specific test data, all vague descriptions

## Scoring Formula

**Composite Score** = round(average of 8 dimensions, 1)

**Grade Mapping**:
- 8.0-10.0: Excellent (Benchmark)
- 6.0-7.9: Good
- 4.0-5.9: Needs Improvement
- 0-3.9: Poor

## Generation Workflow

When generating test cases from requirements:

1. **Ask User Preferences**:
   - Output format: Markdown or Markdown + XMind?
   - Export dimension: Review or Execution?
   
2. **Perform Requirement Analysis**:
   - Apply all 5 analysis methods (Sentence-by-Sentence, Business Process, Data Flow, State Transition, User Scenario)
   - Extract: functional modules, business rules, exception scenarios, test data
   
3. **Design Test Cases**:
   - Select appropriate design methods from Test Design Methodology section
   - Follow Level 2 granularity by default
   - Apply naming convention and field rules
   
4. **Generate Output Files**:
   - Create timestamp-based filename: `{name}-v{MMdd_HHmmss}.md`
   - If XMind requested: also generate `{name}-v{MMdd_HHmmss}.xmind`
   - Structure according to selected dimension (Review or Execution)
   
5. **Self-Review**:
   - Run through Writing Checklist
   - Verify 8-dimension quality criteria
   - Ensure requirement coverage ≥ 95%

## Evaluation Workflow

When evaluating test cases:

1. **Read** the test case file and identify all authors
2. **Analyze** per author across the 8 dimensions using quantitative metrics
3. **Score** each dimension 0-10 with evidence
4. **Calculate** composite score
5. **Write** evaluation report with:
   - Score table per author
   - Strengths per author
   - Improvement suggestions per author
   - Team-wide common issues
   - Actionable recommendations

## Case Template

```
| Field | Value |
|-------|-------|
| Case ID | order_create_014 |
| Case Name | [Order Management][WEB] Order Creation - Product Quantity - Boundary Validation |
| Project | E-Commerce Platform |
| Version | V2.3.0 |
| Module | Order Processing |
| Case Type | Functional Test Case |
| Priority | P1 |
| Precondition | 1. User logged in with valid credentials<br>2. Products available in inventory |
| Test Steps | 1. Navigate to Order Management > Create Order<br>2. Select product and enter quantity as 0<br>3. Click Submit button<br>4. Enter quantity as 999<br>5. Click Submit button |
| Expected Result | 1. Order creation page loads successfully<br>2. Display error: "Quantity must be at least 1"<br>3. Display error: "Maximum order quantity is 100" |
| Postcondition | None |
```

## Writing Checklist

Before submitting test cases, verify:

### Pre-Generation Questions
- [ ] Confirm output format with user: Markdown only or Markdown + XMind?
- [ ] Confirm export dimension: Review dimension or Execution dimension?
- [ ] Apply all 5 requirement analysis methods before designing cases

### Basic Completeness
- [ ] Naming follows [Module][Platform] Feature - Condition - Validation Point format
- [ ] Case ID follows primary_module_secondary_module_sequence_number format
- [ ] Precondition filled as needed (don't blindly write "None")
- [ ] Each step specifies button/field/menu names
- [ ] Each step has a corresponding expected result
- [ ] Expected results are specific and verifiable (no "correctly"/"normally")
- [ ] Priority distribution is reasonable (not all same level)
- [ ] Both positive and negative cases are covered
- [ ] Specific test data values are provided
- [ ] Cases are independent (running order does not affect results)
- [ ] Default Level 2 granularity (2-5 steps per case)
- [ ] Use consistent terminology (Create/Query/Edit/Delete/Submit)

### Design Quality
- [ ] At least one design method is consciously applied (equivalence, boundary, scenario, etc.)
- [ ] Input-output mapping is one-to-one (no ambiguous expected results)
- [ ] Boundary values are covered for numeric/length/date fields
- [ ] Empty/null/whitespace inputs are tested for text fields
- [ ] Cross-field validation is covered (e.g., start date > end date)
- [ ] Error messages include exact text, not just "error prompt"
- [ ] State changes are documented (before/after states)
- [ ] Data persistence is verified (create -> query -> update -> delete cycle)

### Layering & Types
- [ ] Test pyramid is considered during design (not all cases are E2E-level design)
- [ ] API cases cover all parameter combinations and error codes
- [ ] UI cases cover only cross-module critical paths
- [ ] Smoke cases are marked as P0 and cover main workflows

### Maintainability
- [ ] Case is traceable to a requirement ID
- [ ] Postcondition records impact scope when applicable
- [ ] Test data can be reproduced (not dependent on random production data)
- [ ] Case does not contain hard-coded values that change per environment

## Review Checklist (For Peer Review)

Reviewers use this checklist to verify case quality:

```
Review Item                              Pass  Fail  Notes
─────────────────────────────────────────────────────────
Naming follows standard format            □    □
ID is unique and reflects module hierarchy □    □
Preconditions adequately described        □    □
Steps executable (specific to UI elements) □    □
Expected results verifiable (specific)     □    □
Priority reasonably assigned               □    □
Granularity appropriate (Level 2 default)  □    □
Positive/negative coverage balanced        □    □
Test data specific                         □    □
Design method identifiable                 □    □
Traceable to requirements                  □    □
─────────────────────────────────────────────────────────
Review Conclusion: Pass / Needs Revision / Fail
Reviewer: __________  Date: __________
```

## Additional Resources

- For detailed scoring rubrics per dimension, see [reference.md](reference.md)
- For example evaluations of real test cases, see [examples.md](examples.md)
- For XMind format specifications and version management guidelines, see [reference.md](reference.md) sections: XMind Format Specification, Version Management
- For requirement analysis examples, see [reference.md](reference.md) section: Deep Requirement Analysis Examples
