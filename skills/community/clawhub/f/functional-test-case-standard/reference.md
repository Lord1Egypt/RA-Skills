# Detailed Scoring Rubrics

## Dimension 1: Naming Convention

Quantitative metric: percentage of cases following unified format.

| Score | Criteria | Evidence |
|-------|----------|----------|
| 10 | >95% follow [Module][Platform] Feature - Condition - Validation Point format; names are concise (30-80 chars); use input condition as description; avoid redundant expected results in name | Benchmark |
| 8-9 | 80-95% follow format; most names include module and functional item; some inconsistency in condition description | Good |
| 6-7 | 50-80% follow format; mixed naming styles within same author; some names lack functional item or condition | Average |
| 4-5 | 20-50% follow format; mostly free-form naming; some names ambiguous | Needs Improvement |
| 2-3 | <20% follow format; naming is inconsistent and unclear; hard to understand test intent from name alone | Poor |
| 0-1 | No format at all; names are random or copy-pasted; completely unclear | Very Poor |

### Naming Quality Indicators

- **Good name (Level 2)**: `[User Management][WEB] User Registration - Username - Length Validation` — includes module, platform, functional item, condition, verification point
- **Good name (Level 2)**: `[Order Processing][WEB] Order Creation - Product Quantity - Boundary Validation` — business scenario with clear condition and verification
- **Bad name**: `Improvement_5_Add_3_Filters_Create_Date_UI_Style` — lacks module tag, platform, and functional item structure
- **Bad name**: `[OMS] Product Category English Name Adjustment` — too short, lacks condition and verification point
- **Bad name**: `Add Location Info Feature Configuration` — no unified format, unclear intent

## Dimension 2: Structural Integrity

Quantitative metric: percentage of cases with substantive content in each required field.

| Score | Precondition | Steps | Expected Result | Overall |
|-------|-------------|-------|-----------------|---------|
| 10 | >95% substantive | >95% substantive | >95% substantive | All three solid |
| 8-9 | >85% substantive | >95% substantive | >85% substantive | Minor gaps |
| 6-7 | 60-85% substantive | 70-95% substantive | 50-85% substantive | Noticeable gaps |
| 4-5 | 30-60% substantive | 50-70% substantive | 30-50% substantive | Many empty fields |
| 2-3 | <30% substantive | 30-50% substantive | <30% substantive | Mostly shells |
| 0-1 | Almost all empty | <30% substantive | Almost all empty | Not usable |

### Substantive Content Definition

- **Precondition**: Not required if none. When filled, must include at least one of: account role, permission info, data state, environment requirement. Writing only "none" without evaluating necessity is acceptable but not preferred.
- **Steps**: Must contain specific operations (click X, input Y, select Z). Writing only "1. " or HTML template is not substantive.
- **Expected Result**: Must contain verifiable outcomes. Writing only "[Expected Result:]" with no content is not substantive.

## Dimension 3: Step Executability

Quantitative metric: average step text length + specificity score.

| Score | Avg Length | Specificity | Example |
|-------|-----------|-------------|---------|
| 10 | >400 chars | Every step names exact buttons, menus, fields | "Product Name: ABC_01; Category: Electronics; Price: $99.99" |
| 8-9 | 250-400 chars | Most steps name specific UI elements | "Navigate to Order Management > Order List, view page" |
| 6-7 | 150-250 chars | Some steps specific, some vague | "Click [Import] button to open Import dialog" |
| 4-5 | 80-150 chars | Mostly vague, few specific elements | "Operation: submit successfully" |
| 2-3 | 40-80 chars | Very vague, minimal detail | HTML template with empty content |
| 0-1 | <40 chars | Empty or meaningless | "[Precondition] none [Steps]" |

### Specificity Indicators

- **High**: Names exact buttons (`[Confirm]`), exact fields (`Product Name`), exact menu paths (`Module > Submodule`)
- **Medium**: Names general areas (`filter box`, `list page`) without exact labels
- **Low**: Uses generic verbs without targets (`operate`, `check`, `verify`)

## Dimension 4: Expected Result Verifiability

Quantitative metric: percentage of expected results that are specific and observable.

| Score | Criteria | Example Good | Example Bad |
|-------|----------|-------------|-------------|
| 10 | Every step has quantifiable/observable result | "Dropdown shows all products containing 'Phone', highlighted match characters" | — |
| 8-9 | Most results specific, some slightly vague | "Page loads with order list displayed" (acceptable if context is clear) | — |
| 6-7 | About half specific, half vague | Mixed: some say exact messages, some say "display correctly" | — |
| 4-5 | Mostly vague generic phrases | "Function normal" / "Page shows correctly" / "Operation successful" | — |
| 2-3 | Expected results exist but are almost all vague | "[Expected Result:]" left empty or with 1-2 words | — |
| 0-1 | Expected results missing entirely | No expected result section or completely empty | — |

### Verifiability Checklist

A good expected result must answer at least one of:
- What exact text/message appears?
- What exact data value is shown?
- What UI state change occurs (enabled/disabled, visible/hidden)?
- What navigation/redirect happens?
- What error message with exact wording?

## Dimension 5: Test Design Method Diversity

Quantitative metric: count of distinct methods used, weighted by coverage.

| Score | Methods Used | Coverage Distribution |
|-------|-------------|----------------------|
| 10 | 5+ methods, each with significant cases (>20 each) | Balanced across methods |
| 8-9 | 4 methods, each with notable cases | Good distribution |
| 6-7 | 3 methods | Some methods dominate |
| 4-5 | 2 methods | Heavy reliance on 1-2 methods |
| 2-3 | 1 method | Almost all cases use same approach |
| 0-1 | No discernible method | Random case generation |

### Method Keywords for Detection

| Method | Keywords in Case Name |
|--------|----------------------|
| Equivalence Class | Valid, Invalid, Correct, Error, Legal, Illegal |
| Boundary Value | Boundary, Max, Min, Limit, Overflow, Upper, Lower, Empty, Null, Zero, 1 char, 50 chars |
| Scenario/Flow | Scenario, Flow, Normal, Exception, Success, Failure, Main Flow |
| Error Guessing | Error, Failure, Interrupt, Timeout, Duplicate, Concurrent, Network Loss |
| Decision Table | Combination, All, Simultaneous, Compatible, Mutually Exclusive, Cover, Multi-select |
| State Transition | State, Change, Switch, Enable, Disable, Activate, Enable to Disable |

## Dimension 6: Positive/Negative Coverage

Quantitative metric: ratio of positive to negative cases.

| Score | Positive | Negative | Ratio | Assessment |
|-------|----------|----------|-------|------------|
| 10 | Balanced | Strong | 1:1 to 2:1 | Excellent exception coverage |
| 8-9 | Dominant | Good | 2:1 to 3:1 | Good exception coverage |
| 6-7 | Dominant | Moderate | 3:1 to 5:1 | Some exception coverage |
| 4-5 | Very dominant | Weak | 5:1 to 10:1 | Limited exceptions |
| 2-3 | Almost all | Minimal | 10:1+ | Rare exceptions |
| 0-1 | 100% | 0% | Infinite | No exception coverage |

### Ideal Ratio

For most functional testing: **2:1 to 4:1** (positive:negative) is ideal. Too many negatives may indicate over-testing edge cases; too few indicates insufficient exception coverage.

## Dimension 7: Priority Rationality

Quantitative metric: distribution across priority levels.

| Score | Distribution | Assessment |
|-------|-------------|------------|
| 10 | Well-balanced: P0 15-25%, P1 35-45%, P2 35-45% | Ideal |
| 8-9 | Reasonable: no level exceeds 60%, P0/P1 cover core features | Good |
| 6-7 | Some imbalance: one level 60-70%, but core features well covered | Acceptable |
| 4-5 | Noticeable imbalance: one level 70-85% | Needs review |
| 2-3 | Severe imbalance: one level 85-95% | Poor differentiation |
| 0-1 | Extreme: one level >95% or all same level | No prioritization |

## Dimension 8: Test Data Specificity

Quantitative metric: percentage of cases with specific input values in steps.

| Score | Criteria | Example |
|-------|----------|---------|
| 10 | >50% cases include exact input values | "Product Name: ABC_01; Category: Electronics; Price: $99.99" |
| 8-9 | 30-50% include specific values | Some fields have exact values, others generic |
| 6-7 | 15-30% include specific values | Mostly generic with occasional specifics |
| 4-5 | 5-15% include specific values | Rare specific data, mostly "input valid data" |
| 2-3 | 1-5% include specific values | Almost no specific data |
| 0-1 | 0% include specific values | All descriptions are generic like "input username" |

## Common Anti-Patterns

### Anti-Pattern 1: Empty Template Shells
**Symptom**: Steps contain only HTML tags or template headers with no content.
**Example**: `<p>[Precondition]</p><p>1.</p><p>[Steps]</p><p>1. </p>`
**Impact**: Score 0-2 on structural integrity and executability.
**Fix**: Fill in actual preconditions, steps, and expected results.

### Anti-Pattern 2: Vague Expected Results
**Symptom**: Expected results say "display correctly", "function normal", "operation successful".
**Example**: `3-1. Page displays correctly`
**Impact**: Score 4-5 on verifiability.
**Fix**: Specify exact display content, data values, or error messages.

### Anti-Pattern 3: Single Priority Distribution
**Symptom**: 90%+ cases assigned to one priority level.
**Example**: 185 High, 1 Medium, 0 Low
**Impact**: Score 0-3 on priority rationality.
**Fix**: Review and re-prioritize based on business impact and frequency.

### Anti-Pattern 4: Missing Preconditions
**Symptom**: Preconditions all say "none" or are empty.
**Example**: `[Precondition] none`
**Impact**: Score 4-5 on structural integrity.
**Fix**: Add account permissions, data states, and environment requirements.

### Anti-Pattern 5: Overly Long Cases
**Symptom**: Single case has 7+ verification points.
**Example**: One case verifies creation, edit, related user management, inbound order, transfer order
**Impact**: Hard to maintain, unclear failure attribution.
**Fix**: Split into 3-5 independent cases.

### Anti-Pattern 6: Test Case Independence Violation
**Symptom**: Cases depend on running order or shared state.
**Example**: Case B expects data created by Case A; Case C modifies data used by Case D.
**Impact**: Unclear failure attribution, difficult to maintain, false positives when run individually.
**Fix**: Each case documents its own prerequisites and expected initial state. Avoid inter-case dependencies in design.

### Anti-Pattern 7: Ignoring Negative Paths
**Symptom**: 90%+ cases are positive; no error handling, validation, or boundary testing.
**Example**: All login cases use valid credentials; no test for wrong password, locked account, expired session.
**Impact**: Production defects in error handling paths.
**Fix**: Apply equivalence class and boundary value methods. Ensure at least 25-30% negative cases.

### Anti-Pattern 8: Testing Implementation Instead of Requirements
**Symptom**: Cases validate internal logic (e.g., specific SQL query, internal flag) rather than user-visible behavior.
**Example**: "Verify database table has 3 rows" instead of "Verify user sees 3 items in list".
**Impact**: Cases break when implementation changes even if behavior is correct.
**Fix**: Test observable behavior. Use black-box approach. Avoid internal implementation details.

### Anti-Pattern 9: Missing Boundary Value Tests
**Symptom**: Only typical values are tested; no min, max, min-1, max+1, or null testing.
**Example**: Age field tested with 25 only; not tested with 0, -1, 999, empty.
**Impact**: Off-by-one errors, overflow bugs, null pointer exceptions in production.
**Fix**: For every numeric or length field, always test: min-1, min, min+1, typical, max-1, max, max+1, null, empty, whitespace.

## Granularity Examples

### Level 1 Granularity Example

**Requirement**: Username restriction: length 6-20, lowercase English letters and digits only.

| Case | Name | Steps | Expected Result |
|------|------|-------|-----------------|
| 1 | [User Management][WEB] Registration - Username Length - Below 6 | Username: "abc" | Prompt: username length must be 6-20 |
| 2 | [User Management][WEB] Registration - Username Length - Above 20 | Username: "abcdefghijklmnopqrstu" | Prompt: username length must be 6-20 |
| 3 | [User Management][WEB] Registration - Username Length - 6-20 | Username: "abcdef" | Registration successful |
| 4 | [User Management][WEB] Registration - Username Length - Empty | Username: "" | Prompt: username cannot be empty |
| 5 | [User Management][WEB] Registration - Username Format - Uppercase | Username: "ABCdef" | Prompt: username must be lowercase |
| 6 | [User Management][WEB] Registration - Username Format - Pure Digits | Username: "123456" | Registration successful |
| 7 | [User Management][WEB] Registration - Username Format - Starts with Number | Username: "1abcdef" | Prompt: username cannot start with number |

**Characteristics**: 7 separate cases, each testing one boundary/rule.

### Level 2 Granularity Example (Default)

| Field | Value |
|-------|-------|
| Name | [User Management][WEB] Registration - Username Length Validation |
| Steps | 1. Username below 6 characters  2. Username above 20 characters |
| Expected | 1. Prompt: length 6-20  2. Prompt: length 6-20 |

| Name | [User Management][WEB] Registration - Username Format Validation |
| Steps | 1. Uppercase letters  2. Pure digits  3. Starts with number |
| Expected | 1. Prompt: lowercase only  2. Success  3. Prompt: cannot start with number |

**Characteristics**: 2 cases, each groups related boundaries.

### Level 3 Granularity Example

| Field | Value |
|-------|-------|
| Name | [User Management][WEB] Registration - Username Restriction Validation |
| Steps | 1. Below 6  2. Above 20  3. Empty  4. Pure digits |
| Expected | 1-3. Prompt rules  4. Success |

**Characteristics**: 1 case covers all username restrictions.

### Granularity Selection Guide

| Scenario | Recommended Level | Reason |
|----------|------------------|--------|
| Regression testing, frequent running | Level 2 | Balanced coverage and efficiency |
| New feature with many boundary conditions | Level 2 or 1 | Level 2 default; Level 1 for critical boundaries |
| Smoke testing | Level 3 or 2 | Quick coverage of main paths |
| New feature rapid verification | Level 1 | Precise isolation of each boundary or rule |
| Large suite maintenance | Level 2 | Best readability and maintainability |

## Test Case Type Detection

| Type | Detection Keywords in Name or Steps |
|------|-------------------------------------|
| Functional Test Case | Specific functional point, boundary, validation |
| Smoke Test Case | P0 priority, main path, critical function |
| Main-Flow Business Case | Flow, process, end-to-end, business scenario, multiple roles |
| Single-API Case | Interface, API, parameter, field validation, required/optional |
| API Business Flow Case | Interface flow, business process via API, end-to-end via interface |

## Automated Analysis Script

Use this Python approach for quantitative analysis:

```python
import pandas as pd
import re

def analyze_test_cases(file_path):
    df = pd.read_excel(file_path, header=1)
    df = df.dropna(subset=['ID', 'Case Name'])

    results = {}
    for creator in df['Creator'].unique():
        subset = df[df['Creator'] == creator]
        names = subset['Case Name'].dropna().astype(str)
        steps = subset['Steps'].dropna().astype(str)

        results[creator] = {
            'total': len(subset),
            'naming_bracket': names.str.contains(r'\[.*?\]').sum(),
            'precondition': steps.str.contains(r'Precondition|Pre').sum(),
            'expected': steps.str.contains(r'Expected Result|Expected').sum(),
            'operations': steps.str.contains(r'Steps|Operation').sum(),
            'avg_step_len': steps.str.len().mean(),
            'avg_name_len': names.str.len().mean(),
            'boundary': names.str.contains(r'Boundary|Max|Min|Limit|Overflow|0|Empty|Null').sum(),
            'equivalence': names.str.contains(r'Valid|Invalid|Correct|Error|Legal|Illegal').sum(),
            'scenario': names.str.contains(r'Scenario|Flow|Normal|Exception|Success|Failure').sum(),
            'error_guess': names.str.contains(r'Error|Failure|Interrupt|Timeout|Duplicate|Concurrent').sum(),
            'state_transition': names.str.contains(r'State|Change|Switch|Enable|Disable|Activate').sum(),
            'positive': names.str.contains(r'Normal|Correct|Success|Valid|Display|Query').sum(),
            'negative': names.str.contains(r'Error|Failure|Invalid|Empty|Null|Overflow|Exceed').sum(),
        }
    return results
```

## Naming Format Detection Regex

For automated analysis of naming convention:

```python
import re

# Level 2 naming format: [Module][Platform] Feature - Condition - Validation Point
def check_naming_format(name):
    pattern = r'\[[^\]]+\]\[[^\]]+\][^\[\]\-]+-[^\[\]\-]+-[^\[\]\-]+'
    return bool(re.search(pattern, name))

# Examples:
# Match: [User Management][WEB] Registration - Username Length Validation
# Match: [Order Processing][WEB] Order Creation - Product Quantity Validation
# No match: [OMS] Product Category Name Adjustment (missing platform and condition)
```

## Layer-Specific Test Case Design Guidelines

### Unit Test Layer
| Aspect | Guidelines |
|--------|-----------|
| Coverage Goal | All branches, boundary conditions, exception paths |
| Input Scope | All equivalence classes and boundary values of function parameters |
| Design Methods | Equivalence class, Boundary value, Path coverage, Property testing |
| Typical Cases | All mathematical boundaries for calculation functions; All valid/invalid state transitions for state machines |

### Integration Test Layer
| Aspect | Guidelines |
|--------|-----------|
| Coverage Goal | Inter-module interface contracts, data flow, transaction consistency |
| Input Scope | Valid and invalid data combinations across modules |
| Design Methods | Scenario-based, State transition, Decision table |
| Typical Cases | Inventory deduction after order creation; Order status change after payment success |

### API Test Layer
| Aspect | Guidelines |
|--------|-----------|
| Coverage Goal | Interface parameter validation, response structure, error codes, authentication |
| Input Scope | All types, lengths, formats, boundaries, combinations for each parameter |
| Design Methods | Equivalence class, Boundary value, Combination testing, Error guessing |
| Typical Cases | Required field empty, Wrong field type, Over-length string, Special characters |

### E2E Test Layer
| Aspect | Guidelines |
|--------|-----------|
| Coverage Goal | Cross-module business flows, user interactions, page navigation, data display |
| Input Scope | Typical business scenarios and key exception scenarios |
| Design Methods | Scenario-based, Business process diagram, Error guessing |
| Typical Cases | Complete order placement flow; Approval workflow; Multi-role collaboration flow |

## Requirement Traceability Matrix

### Traceability Relationship

```
Requirement (User Story) -> Test Case -> Defect -> Fix Verification
```

### Matrix Template

| Requirement ID | Description | Case ID | Case Name | Priority | Status | Related Defect |
|--------|---------|---------|---------|--------|------|---------|
| US-001 | User Registration | reg_001 | [Registration][WEB] Registration - Username Length Validation | P1 | Pass | — |
| US-001 | User Registration | reg_002 | [Registration][WEB] Registration - Username Format Validation | P1 | Fail | BUG-123 |
| US-002 | User Login | login_001 | [Login][WEB] Login - Valid Credentials | P0 | Pass | — |

### Traceability Value
- When requirements change: Quickly identify affected cases
- During regression testing: Only review cases related to changed requirements
- During coverage analysis: Confirm each requirement has corresponding cases
- During defect analysis: Identify requirement coverage gaps

### Maintenance Rules
- New requirements: Must add corresponding cases in same iteration
- Requirement changes: Mark affected cases as "To Update"
- Deprecated requirements: Mark corresponding cases as "Archived" (don't delete, keep traceability)
- End of each iteration: Check uncovered requirements, coverage target ≥95%

## XMind Format Specification

### XMind Structure Guidelines

XMind mindmaps provide a visual representation of test cases, suitable for:
- Stakeholder review meetings
- Requirement coverage analysis
- Quick overview of test scope
- Test planning and estimation

### Review Dimension XMind Structure

Organized by functional hierarchy, focusing on coverage completeness:

```markdown
# Product Requirement Name - Test Cases

## I. Module Name

### 1.1 Sub-feature Name

#### 1.1.1 Function Point
- **Test Point: Condition Verification**
  - [ ] Verification Item 1: Describe what to verify
  - [ ] Verification Item 2: Describe what to verify
  - [ ] Verification Item 3: Describe what to verify

- **Test Point: Business Rule Verification**
  - [ ] Verification Item 1: Rule description and expected behavior
  - [ ] Verification Item 2: Edge case handling

- **Test Point: Exception Scenario Verification**
  - [ ] Network timeout handling
  - [ ] Invalid data format handling
  - [ ] Permission denial handling

### 1.2 Sub-feature Name

#### 1.2.1 Function Point
- **Test Point: Data Validation**
  - [ ] Valid data acceptance
  - [ ] Invalid data rejection with exact error messages
```

**XMind Node Mapping (Review Dimension)**:
- Level 1 (Root): Product Requirement Name
- Level 2 (Main Topic): Module Name (I, II, III...)
- Level 3 (Sub Topic): Sub-feature Name (1.1, 1.2, 2.1...)
- Level 4 (Sub Topic): Function Point (1.1.1, 1.1.2...)
- Level 5 (Sub Topic): Test Point (bold text)
- Level 6 (Floating Topic): Verification Items (checkbox format)

### Execution Dimension XMind Structure

Organized by test case execution flow, focusing on step-by-step guidance:

```markdown
# Product Requirement Name - Test Cases

## I. Module Name

### 1.1 Sub-feature Name

#### TC-001: [Module][Platform] Feature - Condition - Validation
- **Case ID**: order_create_001
- **Priority**: P0
- **Precondition**:
  - User logged in with valid credentials
  - Products available in inventory
- **Test Steps**:
  1. Navigate to Order Management > Create Order
  2. Select product and enter quantity as 1
  3. Click Submit button
- **Expected Result**:
  1. Order creation page loads successfully
  2. Display success message: "Order created successfully"
  3. Redirect to order list page
- **Postcondition**: Order status is "Pending Payment"

#### TC-002: [Module][Platform] Feature - Condition - Validation
- **Case ID**: order_create_002
- **Priority**: P1
- **Precondition**: Same as TC-001
- **Test Steps**:
  1. Navigate to Order Management > Create Order
  2. Select product and enter quantity as 0
  3. Click Submit button
- **Expected Result**:
  1. Display error: "Quantity must be at least 1"
```

**XMind Node Mapping (Execution Dimension)**:
- Level 1 (Root): Product Requirement Name
- Level 2 (Main Topic): Module Name (I, II, III...)
- Level 3 (Sub Topic): Sub-feature Name (1.1, 1.2, 2.1...)
- Level 4 (Sub Topic): Test Case (TC-001, TC-002...)
- Level 5 (Sub Topic): Fields (Case ID, Priority, Precondition, Test Steps, Expected Result, Postcondition)
- Level 6 (Floating Topic): Step details or expected result details

### XMind Format Rules

1. **Title Hierarchy**:
   - `# ` Level 1: Product name (document root)
   - `## ` Level 2: Functional module (use Chinese numerals: I, II, III...)
   - `### ` Level 3: Sub-feature (use numbering: 1.1, 1.2, 2.1...)
   - `#### ` Level 4: Function point or Test case (use numbering: 1.1.1, 1.1.2... or TC-001, TC-002...)

2. **Test Point Format** (Review Dimension):
   - Must use bold: `**Test Point: XXX Verification**`
   - Test point name should be specific and describe verification goal
   - Examples: `**Test Point: Trigger Condition Verification**`, `**Test Point: Network Exception Verification**`

3. **Verification Item Format** (Review Dimension):
   - Must use checkbox format: `- [ ] Verification item content`
   - Use 2-space indentation for hierarchy
   - Each verification item should be specific, executable, and verifiable
   - Avoid vague descriptions: ❌ "Verify function works normally" → ✅ "Verify clicking 'Submit' button successfully sends form data to server"

4. **Test Case Format** (Execution Dimension):
   - Include all required fields: Case ID, Case Name, Priority, Precondition, Test Steps, Expected Result
   - Steps must be numbered: `1. 2. 3.`
   - Expected results must correspond to each step
   - Use exact error messages, not just "error prompt"

5. **Text Processing**:
   - Preserve bold markers `**text**`
   - Support emoji and special characters
   - Do not use checked checkbox `[x]`,统一 use `[ ]`

### XMind Export Workflow

When user requests XMind format:

1. **Generate Markdown file** first with standard structure
2. **Convert to XMind** using one of these methods:
   - Use XMind's Markdown import feature
   - Use Python script with `xmind` library
   - Use online Markdown-to-XMind converters
3. **Apply timestamp** to both files: `{name}-v{MMdd_HHmmss}.md` and `{name}-v{MMdd_HHmmss}.xmind`
4. **Verify structure** matches selected dimension (Review or Execution)

### Dimension Selection Guide

| Scenario | Recommended Dimension | Reason |
|----------|----------------------|--------|
| Requirement review meeting | Review Dimension | Shows coverage completeness, easy to spot gaps |
| Test planning & estimation | Review Dimension | Quick overview of test scope by module |
| Stakeholder sign-off | Review Dimension | Business-focused, non-technical structure |
| Test execution | Execution Dimension | Step-by-step guidance for testers |
| Automation script generation | Execution Dimension | Clear input-output mapping |
| Regression testing | Execution Dimension | Repeatable, traceable test steps |

## Version Management

### Timestamp-Based Versioning System

Every test case generation creates a uniquely versioned file to enable:
- Historical version preservation
- Version comparison and diff analysis
- Traceability of test case evolution
- Rollback capability if needed

### File Naming Convention

**Format**:
```
{requirement-document-name}-v{MMdd_HHmmss}.md
{requirement-document-name}-v{MMdd_HHmmss}.xmind
```

**Timestamp Specification**:
- Format: `MMdd_HHmmss`
- Components: Month (2 digits) + Day (2 digits) + Underscore + Hour (2 digits) + Minute (2 digits) + Second (2 digits)
- Examples:
  - `0318_143052` = March 18, 14:30:52
  - `1205_091230` = December 5, 09:12:30

**Example**:
- Requirement document: "User Registration Enhancement"
- Generated at: March 18, 2026, 14:30:52
- Output files:
  - `user-registration-enhancement-v0318_143052.md`
  - `user-registration-enhancement-v0318_143052.xmind` (if XMind requested)

### Version Directory Structure

Recommended organization:
```
test-cases/
├── user-registration-enhancement/
│   ├── user-registration-enhancement-v0318_143052.md
│   ├── user-registration-enhancement-v0318_143052.xmind
│   ├── user-registration-enhancement-v0319_101530.md
│   ├── user-registration-enhancement-v0319_101530.xmind
│   └── user-registration-enhancement-latest.md  (symlink to latest)
├── order-processing-update/
│   ├── order-processing-update-v0320_153045.md
│   └── order-processing-update-v0320_153045.xmind
```

### Version Comparison

When comparing versions:

1. **List all versions**:
   ```
   Available versions for "User Registration Enhancement":
   - v0318_143052 (March 18, 14:30:52) - Initial generation
   - v0319_101530 (March 19, 10:15:30) - After requirement change
   - v0320_090000 (March 20, 09:00:00) - Added edge cases
   ```

2. **Compare metrics**:
   - Total test case count
   - Coverage by module
   - Priority distribution (P0/P1/P2)
   - Positive/Negative ratio
   - Test design method distribution

3. **Identify changes**:
   - Added test cases (new functionality)
   - Modified test cases (requirement changes)
   - Removed test cases (deprecated features)

### Version Management Best Practices

1. **Always preserve old versions**: Never delete historical versions
2. **Use meaningful requirement names**: Avoid generic names like "test" or "requirement"
3. **Document version changes**: Add brief comment about what changed in each version
4. **Link to requirement version**: If requirements are versioned, note which requirement version the test cases correspond to
5. **Archive old versions**: After 2+ versions with no changes, mark as "Archived" but do not delete

### Automated Version Management Script

Python script example for version management:

```python
import os
from datetime import datetime
import json

def generate_versioned_filename(base_name, output_dir, format='md'):
    """Generate timestamp-based versioned filename"""
    timestamp = datetime.now().strftime('%m%d_%H%M%S')
    filename = f"{base_name}-v{timestamp}.{format}"
    filepath = os.path.join(output_dir, filename)
    return filepath

def list_versions(requirement_name, output_dir):
    """List all versions for a requirement"""
    versions = []
    for file in os.listdir(output_dir):
        if file.startswith(requirement_name) and '-v' in file:
            # Extract timestamp
            parts = file.split('-v')
            if len(parts) == 2:
                timestamp = parts[1].split('.')[0]
                versions.append({
                    'filename': file,
                    'timestamp': timestamp,
                    'format': parts[1].split('.')[1]
                })
    # Sort by timestamp
    versions.sort(key=lambda x: x['timestamp'])
    return versions

def compare_versions(version1, version2):
    """Compare two versions and show differences"""
    # Parse both markdown files
    # Compare: test case count, coverage, priority distribution
    # Return diff report
    pass
```

### Version Control Integration

For teams using Git:

1. **Commit each version**:
   ```bash
   git add test-cases/user-registration-enhancement-v0318_143052.md
   git commit -m "feat: Generate test cases for user registration enhancement v0318_143052"
   ```

2. **Tag important versions**:
   ```bash
   git tag test-cases-v1.0 user-registration-enhancement-v0318_143052.md
   ```

3. **Track changes in Git history**:
   ```bash
   git log --oneline -- test-cases/user-registration-enhancement-*.md
   ```

## Deep Requirement Analysis Examples

### Example 1: Sentence-by-Sentence Analysis

**Requirement Sentence**: "When users click the 'Export' button, if the report contains more than 10,000 records, display a warning message and ask for confirmation before proceeding."

**Analysis**:
- **Condition**: report contains more than 10,000 records
  - Test: exactly 10,000 records (boundary), 9,999 records, 10,001 records
- **Action**: click 'Export' button
  - Test: button click response, disabled state during export
- **State**: display warning message
  - Test: exact message text, message positioning, message styling
- **Data**: ask for confirmation
  - Test: confirm action, cancel action, timeout without action

**Generated Verification Items**:
- [ ] Verify export with exactly 10,000 records: no warning displayed, export proceeds
- [ ] Verify export with 9,999 records: no warning displayed, export proceeds
- [ ] Verify export with 10,001 records: warning message "This report contains 10,001 records. Export may take several minutes. Continue?" is displayed
- [ ] Verify clicking 'Confirm' on warning: export proceeds
- [ ] Verify clicking 'Cancel' on warning: export is cancelled, no file generated
- [ ] Verify closing warning dialog without action: export is cancelled

### Example 2: Business Process Analysis

**Requirement**: "Order lifecycle: User creates order → System validates inventory → Payment processing → Order confirmation → Warehouse shipment → Delivery tracking → Order completion"

**Process Nodes & Test Scenarios**:
1. **Create Order**:
   - Valid products, valid quantity, valid payment method
   - Invalid products (out of stock, discontinued)
   - Invalid quantity (zero, negative, exceeds max)
2. **Validate Inventory**:
   - Sufficient inventory: proceed to payment
   - Insufficient inventory: show error, suggest alternatives
   - Inventory changed during validation: handle race condition
3. **Payment Processing**:
   - Successful payment: generate confirmation
   - Payment failure: show error, allow retry
   - Payment timeout: handle timeout, release inventory
4. **Order Confirmation**:
   - Email sent successfully
   - Email delivery failure: retry mechanism
5. **Warehouse Shipment**:
   - Successful shipment: update tracking number
   - Shipment delay: notify customer
6. **Delivery Tracking**:
   - Tracking API available: show real-time status
   - Tracking API unavailable: show last known status
7. **Order Completion**:
   - Customer confirms receipt: mark as complete
   - Auto-complete after 7 days: verify automatic transition

### Example 3: Data Flow Analysis

**Requirement**: "User registration system with email verification"

**Data Flow**:
1. **Acquisition**: User enters username, email, password on registration form
2. **Processing**:
   - Validate username: 6-20 chars, lowercase + digits only
   - Validate email: format check, domain verification
   - Validate password: 8+ chars, uppercase + lowercase + number + special char
   - Check uniqueness: username and email must be unique
   - Encrypt password: bcrypt hashing
3. **Storage**:
   - Insert into `users` table with status "pending_verification"
   - Generate verification token with 24-hour expiry
   - Store token in `verification_tokens` table
4. **Display**:
   - Show success message: "Registration successful! Please check your email to verify your account."
   - Send verification email with token link
   - After verification: redirect to login page with message "Email verified successfully. You can now log in."

**Verification Points** (each transformation):
- Username validation: 6 test cases (empty, too short, too long, invalid chars, valid, duplicate)
- Email validation: 5 test cases (invalid format, invalid domain, valid, duplicate, disposable email)
- Password validation: 6 test cases (too short, no uppercase, no lowercase, no number, no special char, valid)
- Uniqueness check: 3 test cases (new user, duplicate username, duplicate email)
- Encryption verification: 2 test cases (password stored as hash, cannot be decrypted)
- Token generation: 3 test cases (valid token, expired token, invalid token)

### Example 4: State Transition Analysis

**Requirement**: "Article publishing workflow with review process"

**States**: Draft → Submitted → Under Review → Approved → Published
                        ↓            ↓
                     Rejected    Revision Requested

**Valid Transitions**:
- Draft → Submitted: user clicks "Submit for Review"
- Submitted → Under Review: reviewer accepts review task
- Submitted → Rejected: reviewer rejects without detailed review
- Under Review → Approved: reviewer approves
- Under Review → Revision Requested: reviewer requests changes
- Revision Requested → Submitted: user resubmits after revision
- Approved → Published: system auto-publishes at scheduled time

**Invalid Transitions** (should show error):
- Draft → Published (skip review)
- Rejected → Published (must resubmit first)
- Published → Draft (cannot revert to draft)
- Under Review → Submitted (already submitted)

**Test Cases** (one per transition):
- 7 valid transition test cases with preconditions and expected results
- 4 invalid transition test cases verifying error handling
- 1 self-transition test case: user saves draft multiple times

### Example 5: User Scenario Analysis

**Requirement**: "File upload feature with multiple user roles"

**Role-Scenario Matrix**:

| Role | Normal Scenario | Exception Scenario | Extreme Scenario |
|------|----------------|-------------------|------------------|
| **Admin** | Upload valid file (PDF, 5MB) | Upload wrong format (EXE) | Upload during system maintenance |
| **Manager** | Upload valid file (DOCX, 10MB) | Upload oversized file (100MB) | Upload 50 files simultaneously |
| **User** | Upload valid file (JPG, 2MB) | Upload file with special chars in name | Upload with unstable network |
| **Guest** | Not allowed (permission check) | Attempt to access upload page | Attempt to bypass permission via API |

**Generated Test Cases** (12 total):
- Admin: 3 test cases (valid, invalid format, extreme timing)
- Manager: 3 test cases (valid, oversized, concurrent uploads)
- User: 3 test cases (valid, special chars, network failure)
- Guest: 3 test cases (permission denied, page access denied, API bypass attempt)
