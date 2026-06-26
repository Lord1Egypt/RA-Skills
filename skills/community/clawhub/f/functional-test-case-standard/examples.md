# Example Evaluations

## Example 1: Excellent Level 2 Test Case (Benchmark)

### Sample Case

| Field | Value |
|-------|-------|
| Case ID | order_search_014 |
| Case Name | [Order Management][WEB] Order Search - Order ID Filter - Exact Match Support |
| Project | E-Commerce Platform |
| Version | V2.3.0 |
| Module | Order Processing |
| Case Type | Functional Test Case |
| Priority | P1 |
| Precondition | 1. User logged in with Order Manager role  2. System contains multiple orders with different statuses |
| Test Steps | 1. Navigate to Order Management > Order List  2. Enter "ORD-2024-001" in Order ID filter field  3. Click Search button  4. View search results |
| Expected Result | 1. Order list page loads successfully  2. Filter field accepts the input  3. Search executes within 2 seconds  4. Display exactly one order: ORD-2024-001, Customer: John Smith, Status: Shipped |
| Postcondition | None |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 9.5 | Follows [Module][Platform] Feature - Condition - Validation Point format perfectly |
| Structure | 9.0 | All required fields filled; precondition has substance when needed |
| Executability | 9.0 | Steps specific to menu paths and fields with exact button names |
| Verifiability | 9.5 | Expected results are specific with exact order details |
| Method Diversity | 8.0 | Equivalence class (valid/invalid input) and scenario coverage |
| Coverage | 8.5 | Good positive coverage; includes exact match scenario |
| Priority | 8.0 | P1 is reasonable for search functionality |
| Data Specificity | 9.0 | Uses exact order ID "ORD-2024-001" and expected customer name |
| **Composite** | **8.8** | — |

### Strengths
- Naming follows the unified format with module, platform, functional item, condition, and verification point
- Level 2 granularity: focuses on exact match search scenario
- Precondition specifies user role and system data state
- Expected result includes exact display format with order details
- Specific test data with realistic order ID format

### Improvements
- Add a negative case: search with non-existent order ID
- Add edge case: search with partial order ID
- Specify exact error message when no results found

---

## Example 2: Level 2 Granularity with Data-Rich Steps (Benchmark)

### Sample Case

| Field | Value |
|-------|-------|
| Case ID | product_create_001 |
| Case Name | [Product Management][WEB] Product Creation - Product Name Length Validation |
| Project | E-Commerce Platform |
| Version | V1.5.0 |
| Module | Product Catalog |
| Case Type | Functional Test Case |
| Priority | P1 |
| Precondition | 1. User logged in with Product Manager role  2. Navigate to Product Management > Product List page |
| Test Steps | 1. Click [Add Product] button, enter "A" (1 character) in Product Name field, fill other required fields normally, click [Submit]  2. Enter 200-character valid product name, fill other fields normally, click [Submit] |
| Expected Result | 1. Creation fails, display error: "Product name must be between 2-150 characters"  2. Creation succeeds, display success message "Product created successfully", redirect to product list, new product appears in first row |
| Postcondition | None |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 9.0 | Clear format with module, platform, feature, condition, and validation |
| Structure | 9.0 | All fields present and substantive |
| Executability | 9.5 | Extremely detailed with exact field values and constraints |
| Verifiability | 9.5 | Expected results include exact error messages and success states |
| Method Diversity | 8.5 | Boundary value (min and max length) and equivalence class |
| Coverage | 8.0 | Positive and negative cases; could add duplicate name test |
| Priority | 8.0 | P1 reasonable for boundary validation |
| Data Specificity | 9.5 | Exact input values: "A" (1 char), 200 characters |
| **Composite** | **8.9** | — |

### Strengths
- Level 2 granularity: merges min-length and max-length boundary tests into one case
- Exact test data: "1 character", "200 characters"
- Expected results include exact error messages and success messages
- Cross-module verification (creation -> list -> display)

### Improvements
- Add negative case for duplicate product name
- Include P0 case for the main "Add Product" happy path
- Add test case for special characters in product name

---

## Example 3: Needs Improvement

### Sample Case 1 (Empty Steps)

| Field | Value |
|-------|-------|
| Case ID | report_001 |
| Case Name | [Reporting][WEB] Sales Report Export - Export Content - Combined with Filters |
| Project | Analytics Platform |
| Version | V1.0 |
| Module | Report Management |
| Case Type | Functional Test Case |
| Priority | High |
| Precondition | Test path: [WEB] Click Report Management menu, enter Report interface. Role: Sales Manager. |
| Test Steps | (empty) |
| Expected Result | (empty) |
| Postcondition | None |

### Sample Case 2 (Partial Content)

| Field | Value |
|-------|-------|
| Case ID | report_002 |
| Case Name | Improvement_5_Add_3_Filters_Date_Range_UI_Style |
| Project | Analytics Platform |
| Version | V1.0 |
| Module | Report Management |
| Case Type | Functional Test Case |
| Priority | High |
| Precondition | Test path: [WEB] Click Report Management menu. Role: Sales Manager. |
| Test Steps | 1. Operation: single select then export  [Expected Result:]  2. Operation: batch paste product IDs search then export  [Expected Result:] |
| Expected Result | (empty) |
| Postcondition | None |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 4.5 | Case 1 follows format well; Case 2 uses "Improvement_N" prefix, no [ ] format |
| Structure | 4.5 | ~37% steps empty; ~92% preconditions are only test path |
| Executability | 5.0 | Average 169 chars but heavily skewed; filled cases are moderate |
| Verifiability | 4.5 | ~37% expected results empty; filled ones are moderate |
| Method Diversity | 5.5 | Equivalence class coverage is good but others weak |
| Coverage | 5.0 | Positive/negative ratio ~3.7:1, negative coverage insufficient |
| Priority | 3.0 | 99.5% are High; 1 Medium; no differentiation |
| Data Specificity | 4.0 | Only ~5% include specific test data |
| **Composite** | **4.5** | — |

### Critical Issues
- 36.6% of cases have empty steps and expected results — not runnable
- 91.9% preconditions lack substance (only "test path" and "role")
- Priority distribution is severely imbalanced (99.5% High)
- Naming is inconsistent: some follow format, many use "Improvement_N" prefix

### Action Plan
1. Fill all empty steps and expected results immediately
2. Rewrite preconditions with account permissions and data states
3. Re-prioritize: move UI/validation cases to P1/P2
4. Adopt unified [Module][Platform] Feature - Condition - Validation Point naming format
5. Add specific test data values to every case

---

## Example 4: Poor Quality

### Sample Case

| Field | Value |
|-------|-------|
| Case ID | — |
| Case Name | Add Location Information Feature Configuration_Function Setting Add APP obtains user location information configuration item |
| Project | — |
| Version | — |
| Module | — |
| Case Type | Functional Test Case |
| Priority | High |
| Precondition | None |
| Test Steps | (empty) |
| Expected Result | (empty) |
| Postcondition | None |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 4.0 | No [ ] format; unclear intent; overly long |
| Structure | 3.0 | Steps completely empty; preconditions all "none" |
| Executability | 2.0 | Average 39 chars; cases are empty shells |
| Verifiability | 2.0 | Expected results 0% substantive |
| Method Diversity | 3.0 | Extremely limited method diversity |
| Coverage | 4.0 | Some negative cases but overall weak |
| Priority | 5.0 | Priority field present but no context |
| Data Specificity | 2.0 | Almost no specific test data |
| **Composite** | **3.1** | — |

### Critical Issues
- Steps are empty — cases are not runnable
- No expected results at all
- No preconditions beyond "none"
- Naming is inconsistent and unclear
- Missing case ID, project, version, module fields

### Action Plan
- Rewrite all cases following the team standard template
- Reference Example 1 or Example 2 for format and granularity
- Each case must have at least 2-5 specific steps with exact UI elements
- Use unified naming: [Module][Platform] Feature - Condition - Validation Point

---

## Example 5: Level 2 Granularity — Business Flow Case (Main-Flow)

### Sample Case

| Field | Value |
|-------|-------|
| Case ID | order_cancel_001 |
| Case Name | [Order Management][WEB] Order Cancellation - Cancel Active Order - Impact Validation |
| Project | E-Commerce Platform |
| Version | V3.0 |
| Module | Order Processing |
| Case Type | Main-Flow Business Case |
| Priority | P0 |
| Precondition | 1. Order Manager role logged in  2. Existing orders with different statuses: Pending Payment, Processing, Shipped |
| Test Steps | 1. Attempt to cancel Pending Payment order  2. Attempt to cancel Processing order  3. Attempt to cancel Shipped order  4. Verify customer notifications for each cancellation attempt |
| Expected Result | 1. Cancellation successful, order status changed to "Cancelled", refund initiated  2. Cancellation fails, display error: "Order is being processed and cannot be cancelled"  3. Cancellation fails, display error: "Order has been shipped, please initiate return"  4. Cancellation confirmation email sent only for successful cancellations |
| Postcondition | Cancelled orders cannot be reactivated; refund process initiated automatically |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 9.0 | Follows format; includes business scenario and verification point |
| Structure | 9.5 | All fields present; precondition has business state; postcondition covers impact |
| Executability | 8.5 | Steps are clear; could be more specific on UI operations |
| Verifiability | 9.5 | Expected results cover all order statuses with clear outcomes |
| Method Diversity | 7.5 | Scenario-based; covers multiple order states |
| Coverage | 9.0 | Covers all order statuses in the cancellation flow |
| Priority | 9.0 | P0 is correct for core business flow |
| Data Specificity | 8.0 | Describes order states but could include exact order IDs |
| **Composite** | **8.7** | — |

### Strengths
- Level 2 granularity for business flow: groups related order status checks
- Postcondition documents impact scope
- Covers end-to-end business scenario with multiple outcomes
- All order statuses have clear expected outcomes
- Customer notification verification included

---

## Example 6: Level 2 Granularity — Boundary Value Case (Functional)

### Sample Case

| Field | Value |
|-------|-------|
| Case ID | product_import_005 |
| Case Name | [Product Management][WEB] Product Import - Import Template - SKU Required Field Validation |
| Project | E-Commerce Platform |
| Version | V2.1 |
| Module | Product Catalog |
| Case Type | Functional Test Case |
| Priority | P1 |
| Precondition | Product Manager role logged in |
| Test Steps | 1. Import template file with one row where SKU field is empty, other required fields filled with valid content, click Import |
| Expected Result | 1. Import fails, display error: "Row 1: SKU is a required field" with row highlighted in red |
| Postcondition | None |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 9.5 | Perfect format with module, platform, feature, condition, validation |
| Structure | 8.5 | All fields present; precondition could be more detailed |
| Executability | 9.0 | Specific operation with exact field name and action |
| Verifiability | 9.5 | Exact error message provided with row number |
| Method Diversity | 8.5 | Boundary value (empty required field) and error guessing |
| Coverage | 7.0 | Single negative case; could add positive case (filled SKU) |
| Priority | 8.0 | P1 reasonable for field validation |
| Data Specificity | 9.0 | Specific field and exact error message described |
| **Composite** | **8.6** | — |

### Strengths
- Excellent naming following the unified format
- Specific test data: "SKU field is empty"
- Exact expected error message with row number
- Clear single-point verification

---

## Example 7: API Test Case (Single-API)

### Sample Case

| Field | Value |
|-------|-------|
| Case ID | api_user_001 |
| Case Name | [User Management][API] User Creation API - username Parameter - Required Field Validation |
| Project | User Center |
| Version | V2.0 |
| Module | User API |
| Case Type | Single-API Case |
| Priority | P0 |
| Precondition | 1. API base URL accessible  2. Valid authorization token available |
| Test Steps | POST /api/v2/users  Body: {"username": "", "email": "test@example.com", "password": "Pass1234"} |
| Expected Result | 1. HTTP Status: 400 Bad Request  2. Response: {"error": "USERNAME_REQUIRED", "message": "Username is required"}  3. No new user record in database |
| Postcondition | None |

### Data-Driven Extension

| Data Set | username | email | password | Expected HTTP | Expected Error |
|----------|----------|-------|----------|---------------|----------------|
| Empty | "" | valid | valid | 400 | USERNAME_REQUIRED |
| Null | null | valid | valid | 400 | USERNAME_REQUIRED |
| Missing | (omit) | valid | valid | 400 | USERNAME_REQUIRED |
| Too short | "ab" | valid | valid | 400 | USERNAME_TOO_SHORT |
| Too long | 51 chars | valid | valid | 400 | USERNAME_TOO_LONG |
| Invalid chars | "user@name" | valid | valid | 400 | USERNAME_INVALID |
| Valid | "user01" | valid | valid | 201 | — |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 9.0 | Clear format; identifies API and parameter |
| Structure | 9.0 | All fields present; exact request/response |
| Executability | 9.5 | Specific endpoint, method, body, exact response |
| Verifiability | 9.5 | Exact HTTP code, exact error code, DB verification |
| Method Diversity | 8.5 | Equivalence class + Boundary value for parameter |
| Coverage | 8.5 | Positive + multiple negatives; comprehensive validation |
| Priority | 9.0 | P0 correct for core API validation |
| Data Specificity | 9.5 | Exact request body, exact response structure |
| **Composite** | **9.1** | — |

### Strengths
- Data-driven design: one case logic, multiple data sets
- Exact API contract verification (HTTP code, error code, message)
- Database state verification included
- Covers empty, null, missing, length, format validations

---

## Example 8: Data-Driven Test Case

### Sample Case

| Field | Value |
|-------|-------|
| Case ID | calc_discount_001 |
| Case Name | [Promotion Management][API] Discount Calculation - Different Purchase Amounts - Calculation Result Validation |
| Project | E-Commerce Platform |
| Version | V2.5.0 |
| Module | Promotion Engine |
| Case Type | Single-API Case |
| Priority | P0 |
| Precondition | 1. Discount rules: Amount < $100: 5% off, $100-$500: 10% off, > $500: 15% off  2. API endpoint accessible |
| Test Steps | POST /api/v2/calc/discount  Body: {"purchaseAmount": {purchaseAmount}} |
| Expected Result | Response: {"discount": {expectedDiscount}, "rate": {expectedRate}, "finalAmount": {finalAmount}} |
| Postcondition | None |

### Parameter Table

| Case ID | purchaseAmount | expectedRate | expectedDiscount | Description |
|----------|-------------|--------------|---------------|------|
| calc_discount_001a | 0 | 0% | $0 | Boundary - Zero value |
| calc_discount_001b | 99.99 | 5% | $5.00 | Boundary - Below lower limit |
| calc_discount_001c | 100.00 | 10% | $10.00 | Boundary - Lower limit |
| calc_discount_001d | 100.01 | 10% | $10.00 | Boundary - Above lower limit |
| calc_discount_001e | 300.00 | 10% | $30.00 | Typical - Middle tier |
| calc_discount_001f | 499.99 | 10% | $50.00 | Boundary - Below upper limit |
| calc_discount_001g | 500.00 | 15% | $75.00 | Boundary - Upper limit |
| calc_discount_001h | 500.01 | 15% | $75.00 | Boundary - Above upper limit |
| calc_discount_001i | -100 | Error | Error | Invalid - Negative |
| calc_discount_001j | null | Error | Error | Invalid - Null |

### Dimension Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Naming | 9.0 | Clear format; identifies calculation logic |
| Structure | 9.0 | All fields present; parameter table clear |
| Executability | 9.5 | Specific API endpoint with parameterized body |
| Verifiability | 9.5 | Exact expected values for each boundary |
| Method Diversity | 9.5 | Boundary value (all boundaries) + Equivalence class (3 tiers) |
| Coverage | 9.0 | All boundaries + invalid cases comprehensively covered |
| Priority | 9.0 | P0 correct for core calculation logic |
| Data Specificity | 9.5 | Exact input/output pairs for all scenarios |
| **Composite** | **9.2** | — |

### Strengths
- Classic data-driven design: one case logic, 10 data sets
- Covers all boundary values (min-1, min, min+1, max-1, max, max+1)
- Covers invalid inputs (negative, null)
- Exact expected results for verification
- Business rule clearly documented in precondition

### Improvements
- Add decimal precision boundary (e.g., $99.99 vs $100.00)
- Add large number boundary (e.g., $999,999.99)
- Include currency edge cases if multi-currency supported

---

## Evaluation Report Template

When asked to evaluate test cases, produce a report with this structure:

```markdown
# Test Case Quality Evaluation Report

## 1. Overview
- Total cases: N
- Authors: N people
- Evaluation dimensions: 8
- Default granularity: Level 2

## 2. Score Summary

| Author | Count | Naming | Structure | Executable | Verifiable | Methods | Coverage | Priority | Data | Composite |
|--------|-------|--------|-----------|------------|------------|---------|----------|----------|------|-----------|
| Name1  | N     | X.X    | X.X       | X.X        | X.X        | X.X     | X.X      | X.X      | X.X  | X.X       |

## 3. Per-Author Detailed Review

### Author Name - Score X.X
**Strengths:**
1. ...
2. ...

**Improvements:**
1. ...
2. ...

## 4. Team-Wide Common Issues
1. ...
2. ...

## 5. Recommendations
### Immediate (1-2 weeks)
- ...

### Short-term (1 month)
- ...

### Long-term (ongoing)
- ...
```

---

## Example 9: XMind Output - Review Dimension

### Scenario
User requests: "Generate test cases for User Registration feature in both Markdown and XMind formats, using Review dimension for stakeholder review."

### Generated Files
- `user-registration-v0318_143052.md`
- `user-registration-v0318_143052.xmind`

### XMind Content Structure (Review Dimension)

```markdown
# User Registration Enhancement - Test Cases

## I. User Registration Module

### 1.1 Registration Form

#### 1.1.1 Username Field
- **Test Point: Length Validation**
  - [ ] Verify username with exactly 6 characters: accepted
  - [ ] Verify username with exactly 20 characters: accepted
  - [ ] Verify username with 5 characters: rejected with error "Username must be between 6-20 characters"
  - [ ] Verify username with 21 characters: rejected with error "Username must be between 6-20 characters"
  - [ ] Verify empty username: rejected with error "Username is required"

- **Test Point: Format Validation**
  - [ ] Verify username with lowercase letters only ("abcdef"): accepted
  - [ ] Verify username with digits only ("123456"): accepted
  - [ ] Verify username with uppercase letters ("ABCdef"): rejected with error "Username must contain only lowercase letters and digits"
  - [ ] Verify username with special characters ("user@name"): rejected with error "Username must contain only lowercase letters and digits"
  - [ ] Verify username starting with number ("1abcdef"): rejected with error "Username cannot start with a number"

- **Test Point: Uniqueness Validation**
  - [ ] Verify new unique username: accepted
  - [ ] Verify existing username: rejected with error "Username already exists"

#### 1.1.2 Email Field
- **Test Point: Format Validation**
  - [ ] Verify valid email format ("user@example.com"): accepted
  - [ ] Verify missing @ symbol ("userexample.com"): rejected with error "Invalid email format"
  - [ ] Verify missing domain ("user@"): rejected with error "Invalid email format"
  - [ ] Verify missing username ("@example.com"): rejected with error "Invalid email format"
  - [ ] Verify multiple @ symbols ("user@@example.com"): rejected with error "Invalid email format"

- **Test Point: Domain Validation**
  - [ ] Verify valid domain ("user@gmail.com"): accepted
  - [ ] Verify invalid domain ("user@invalid"): rejected with error "Invalid email domain"
  - [ ] Verify disposable email domain: warning displayed "Disposable email addresses are not allowed"

#### 1.1.3 Password Field
- **Test Point: Complexity Validation**
  - [ ] Verify password with 8 characters including uppercase, lowercase, number, special char: accepted
  - [ ] Verify password with 7 characters: rejected with error "Password must be at least 8 characters"
  - [ ] Verify password without uppercase ("password1!"): rejected with error "Password must contain at least one uppercase letter"
  - [ ] Verify password without lowercase ("PASSWORD1!"): rejected with error "Password must contain at least one lowercase letter"
  - [ ] Verify password without number ("Password!"): rejected with error "Password must contain at least one number"
  - [ ] Verify password without special char ("Password1"): rejected with error "Password must contain at least one special character"

### 1.2 Registration Submission

#### 1.2.1 Form Submission
- **Test Point: All Fields Valid**
  - [ ] Verify submission with all valid fields: success message displayed, redirect to verification page
  - [ ] Verify database record created with status "pending_verification"
  - [ ] Verify verification email sent to user's email address

- **Test Point: Partial Fields Missing**
  - [ ] Verify submission with username only: inline errors displayed for email and password
  - [ ] Verify submission with email only: inline errors displayed for username and password
  - [ ] Verify submission with password only: inline errors displayed for username and email
  - [ ] Verify submission with no fields: inline errors displayed for all three fields

- **Test Point: Duplicate Submission Prevention**
  - [ ] Verify double-click submit button: only one request sent, no duplicate records created
  - [ ] Verify submit button disabled after first click: button shows loading state

#### 1.2.2 Email Verification
- **Test Point: Valid Verification Token**
  - [ ] Click verification link within 24 hours: account activated, redirect to login page with success message
  - [ ] Verify account status changed from "pending_verification" to "active"

- **Test Point: Invalid Verification Token**
  - [ ] Click expired verification link (after 24 hours): error message "Verification link expired. Please request a new one."
  - [ ] Click malformed verification link: error message "Invalid verification link"
  - [ ] Click already-used verification link: error message "Account already verified. Please log in."

- **Test Point: Resend Verification Email**
  - [ ] Request new verification email: new token generated, old token invalidated
  - [ ] Verify new email received within 2 minutes
  - [ ] Verify rate limiting: maximum 3 resend requests per hour

## II. Error Handling Module

### 2.1 Network Exceptions

#### 2.1.1 Connection Timeout
- **Test Point: Server Unreachable**
  - [ ] Verify behavior when server is down: user-friendly error message "Service temporarily unavailable. Please try again later."
  - [ ] Verify no partial data saved when request fails

- **Test Point: Slow Network**
  - [ ] Verify loading indicator displayed during submission
  - [ ] Verify timeout after 30 seconds with error message "Request timeout. Please check your connection and try again."

### 2.2 Data Exceptions

#### 2.2.1 SQL Injection Attempts
- **Test Point: Malicious Input**
  - [ ] Verify username with SQL injection ("' OR 1=1 --"): rejected, input sanitized
  - [ ] Verify email with SQL injection ("test@test.com' OR 1=1 --"): rejected, input sanitized
  - [ ] Verify no database errors exposed to user

#### 2.2.2 XSS Attempts
- **Test Point: Script Injection**
  - [ ] Verify username with script tag ("<script>alert('xss')</script>"): rejected or sanitized
  - [ ] Verify input displayed safely in error messages without execution

## III. Edge Cases Module

### 3.1 Boundary Conditions

#### 3.1.1 Concurrent Registrations
- **Test Point: Same Username Concurrent Requests**
  - [ ] Verify two users attempting to register with same username simultaneously: one succeeds, one gets "Username already exists" error

- **Test Point: Same Email Concurrent Requests**
  - [ ] Verify two users attempting to register with same email simultaneously: one succeeds, one gets "Email already exists" error

### 3.2 System Limits

#### 3.2.1 Rate Limiting
- **Test Point: Excessive Registration Attempts**
  - [ ] Verify 10 registration attempts from same IP within 1 minute: block further attempts, display "Too many attempts. Please try again in 5 minutes."
  - [ ] Verify block expires after 5 minutes: registration allowed again
```

### XMind Visual Structure

When imported to XMind, the structure becomes:

```
User Registration Enhancement - Test Cases (Central Topic)
├── I. User Registration Module (Main Topic)
│   ├── 1.1 Registration Form (Sub Topic)
│   │   ├── 1.1.1 Username Field (Sub Topic)
│   │   │   ├── Test Point: Length Validation (Sub Topic, Bold)
│   │   │   │   ├── ☐ Verify username with exactly 6 characters (Floating Topic)
│   │   │   │   ├── ☐ Verify username with exactly 20 characters (Floating Topic)
│   │   │   │   └── ... (more verification items)
│   │   │   ├── Test Point: Format Validation (Sub Topic, Bold)
│   │   │   │   └── ... (verification items)
│   │   │   └── Test Point: Uniqueness Validation (Sub Topic, Bold)
│   │   │       └── ... (verification items)
│   │   ├── 1.1.2 Email Field (Sub Topic)
│   │   │   └── ... (test points and verification items)
│   │   └── 1.1.3 Password Field (Sub Topic)
│   │       └── ... (test points and verification items)
│   └── 1.2 Registration Submission (Sub Topic)
│       └── ... (function points, test points, verification items)
├── II. Error Handling Module (Main Topic)
│   └── ... (network exceptions, data exceptions)
└── III. Edge Cases Module (Main Topic)
    └── ... (boundary conditions, system limits)
```

### Review Dimension Benefits

- ✅ **Stakeholder-friendly**: Non-technical structure, easy to understand test scope
- ✅ **Coverage visibility**: Clear hierarchy shows which areas are covered
- ✅ **Gap identification**: Easy to spot missing test points
- ✅ **Meeting-ready**: Suitable for requirement review presentations
- ✅ **Estimation support**: Quick count of verification items per module for effort estimation

---

## Example 10: XMind Output - Execution Dimension

### Scenario
User requests: "Generate test cases for Order Search feature in both Markdown and XMind formats, using Execution dimension for test execution."

### Generated Files
- `order-search-v0318_150300.md`
- `order-search-v0318_150300.xmind`

### XMind Content Structure (Execution Dimension)

```markdown
# Order Search Feature - Test Cases

## I. Order Search Module

### 1.1 Order ID Search

#### TC-001: [Order Management][WEB] Order Search - Order ID - Exact Match
- **Case ID**: order_search_001
- **Priority**: P0
- **Precondition**:
  - User logged in with Order Manager role
  - System contains order "ORD-2024-001" with status "Shipped"
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Enter "ORD-2024-001" in Order ID filter field
  3. Click Search button
  4. View search results
- **Expected Result**:
  1. Order list page loads successfully
  2. Filter field accepts the input
  3. Search executes within 2 seconds
  4. Display exactly one order: ORD-2024-001, Customer: John Smith, Status: Shipped
- **Postcondition**: None

#### TC-002: [Order Management][WEB] Order Search - Order ID - Non-existent
- **Case ID**: order_search_002
- **Priority**: P1
- **Precondition**: User logged in with Order Manager role
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Enter "ORD-9999-999" in Order ID filter field
  3. Click Search button
  4. View search results
- **Expected Result**:
  1. Order list page loads successfully
  2. Filter field accepts the input
  3. Search executes within 2 seconds
  4. Display message: "No orders found matching your search criteria"
  5. Order list is empty
- **Postcondition**: None

#### TC-003: [Order Management][WEB] Order Search - Order ID - Partial Match
- **Case ID**: order_search_003
- **Priority**: P1
- **Precondition**:
  - User logged in with Order Manager role
  - System contains orders: ORD-2024-001, ORD-2024-002, ORD-2023-001
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Enter "ORD-2024" in Order ID filter field
  3. Click Search button
  4. View search results
- **Expected Result**:
  1. Order list page loads successfully
  2. Search executes within 2 seconds
  3. Display 2 orders: ORD-2024-001 and ORD-2024-002
  4. Order ORD-2023-001 is not displayed
- **Postcondition**: None

### 1.2 Date Range Search

#### TC-004: [Order Management][WEB] Order Search - Date Range - Valid Range
- **Case ID**: order_search_004
- **Priority**: P0
- **Precondition**:
  - User logged in with Order Manager role
  - System contains orders from multiple dates
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Click Date Range filter
  3. Set Start Date: 2024-03-01
  4. Set End Date: 2024-03-31
  5. Click Search button
  6. View search results
- **Expected Result**:
  1. Date range picker opens successfully
  2. Both dates accepted
  3. Search executes within 3 seconds
  4. Display only orders created between 2024-03-01 and 2024-03-31
  5. Each order's creation date is within the specified range
- **Postcondition**: None

#### TC-005: [Order Management][WEB] Order Search - Date Range - Start Date After End Date
- **Case ID**: order_search_005
- **Priority**: P1
- **Precondition**: User logged in with Order Manager role
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Click Date Range filter
  3. Set Start Date: 2024-03-31
  4. Set End Date: 2024-03-01
  5. Click Search button
- **Expected Result**:
  1. Date range picker opens successfully
  2. Both dates accepted
  3. Display error: "Start date cannot be later than end date"
  4. Search is not executed
  5. Order list remains unchanged
- **Postcondition**: None

#### TC-006: [Order Management][WEB] Order Search - Date Range - Future Date
- **Case ID**: order_search_006
- **Priority**: P2
- **Precondition**: User logged in with Order Manager role
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Click Date Range filter
  3. Set Start Date: 2025-01-01
  4. Set End Date: 2025-12-31
  5. Click Search button
- **Expected Result**:
  1. Date range picker opens successfully
  2. Future dates accepted
  3. Search executes successfully
  4. Display message: "No orders found in the specified date range"
  5. Order list is empty
- **Postcondition**: None

### 1.3 Combined Filters

#### TC-007: [Order Management][WEB] Order Search - Multiple Filters - Combined Search
- **Case ID**: order_search_007
- **Priority**: P0
- **Precondition**:
  - User logged in with Order Manager role
  - System contains orders with various statuses and dates
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Enter "ORD-2024" in Order ID filter
  3. Select Status: "Shipped"
  4. Set Date Range: 2024-03-01 to 2024-03-31
  5. Click Search button
  6. View search results
- **Expected Result**:
  1. All filters applied successfully
  2. Search executes within 3 seconds
  3. Display orders matching ALL three criteria:
     - Order ID contains "ORD-2024"
     - Status is "Shipped"
     - Created between 2024-03-01 and 2024-03-31
  4. Non-matching orders are excluded
- **Postcondition**: None

#### TC-008: [Order Management][WEB] Order Search - Clear Filters
- **Case ID**: order_search_008
- **Priority**: P1
- **Precondition**: User has performed a filtered search
- **Test Steps**:
  1. View filtered search results
  2. Click "Clear Filters" button
  3. View search results
- **Expected Result**:
  1. All filter fields are cleared
  2. Order list reloads with all orders (no filters applied)
  3. URL query parameters removed
- **Postcondition**: None

## II. Search Performance Module

### 2.1 Response Time

#### TC-009: [Order Management][WEB] Order Search - Performance - Large Dataset
- **Case ID**: order_search_009
- **Priority**: P1
- **Precondition**: System contains 100,000+ orders
- **Test Steps**:
  1. Navigate to Order Management > Order List
  2. Enter valid search criteria matching ~1,000 orders
  3. Click Search button
  4. Measure search execution time
- **Expected Result**:
  1. Search executes within 5 seconds
  2. Results displayed in paginated format (50 per page)
  3. Page shows "Found 1,000 orders" message
- **Postcondition**: None

### 2.2 Pagination

#### TC-010: [Order Management][WEB] Order Search - Pagination - Navigate Pages
- **Case ID**: order_search_010
- **Priority**: P1
- **Precondition**: Search returned 150 results (3 pages at 50 per page)
- **Test Steps**:
  1. View first page of search results
  2. Verify 50 orders displayed
  3. Click "Next Page" button
  4. Verify second page displays orders 51-100
  5. Click "Page 3" link
  6. Verify third page displays orders 101-150
  7. Click "Previous Page" button
  8. Verify returns to page 2
- **Expected Result**:
  1. Each page displays exactly 50 orders (except last page)
  2. Pagination controls show correct page numbers
  3. Page navigation is smooth, no errors
  4. Search filters remain applied across pages
- **Postcondition**: None
```

### XMind Visual Structure (Execution Dimension)

When imported to XMind, the structure becomes:

```
Order Search Feature - Test Cases (Central Topic)
├── I. Order Search Module (Main Topic)
│   ├── 1.1 Order ID Search (Sub Topic)
│   │   ├── TC-001: [Order Management][WEB] Order Search - Order ID - Exact Match (Sub Topic)
│   │   │   ├── Case ID: order_search_001 (Floating Topic)
│   │   │   ├── Priority: P0 (Floating Topic)
│   │   │   ├── Precondition (Sub Topic)
│   │   │   │   ├── User logged in with Order Manager role (Floating Topic)
│   │   │   │   └── System contains order "ORD-2024-001" (Floating Topic)
│   │   │   ├── Test Steps (Sub Topic)
│   │   │   │   ├── 1. Navigate to Order Management > Order List (Floating Topic)
│   │   │   │   ├── 2. Enter "ORD-2024-001" in Order ID filter (Floating Topic)
│   │   │   │   ├── 3. Click Search button (Floating Topic)
│   │   │   │   └── 4. View search results (Floating Topic)
│   │   │   ├── Expected Result (Sub Topic)
│   │   │   │   ├── 1. Order list page loads successfully (Floating Topic)
│   │   │   │   ├── 2. Filter field accepts the input (Floating Topic)
│   │   │   │   ├── 3. Search executes within 2 seconds (Floating Topic)
│   │   │   │   └── 4. Display exactly one order... (Floating Topic)
│   │   │   └── Postcondition: None (Floating Topic)
│   │   ├── TC-002: [Order Management][WEB] Order Search - Order ID - Non-existent (Sub Topic)
│   │   │   └── ... (all fields)
│   │   └── TC-003: [Order Management][WEB] Order Search - Order ID - Partial Match (Sub Topic)
│   │       └── ... (all fields)
│   ├── 1.2 Date Range Search (Sub Topic)
│   │   └── ... (TC-004, TC-005, TC-006)
│   └── 1.3 Combined Filters (Sub Topic)
│       └── ... (TC-007, TC-008)
└── II. Search Performance Module (Main Topic)
    └── ... (TC-009, TC-010)
```

### Execution Dimension Benefits

- ✅ **Tester-friendly**: Step-by-step guidance, easy to follow during execution
- ✅ **Traceability**: Each step has corresponding expected result
- ✅ **Automation-ready**: Clear input-output mapping for automation scripts
- ✅ **Pass/Fail judgment**: Specific expected results enable unambiguous pass/fail decisions
- ✅ **Regression testing**: Repeatable test cases for regression cycles

---

## Example 11: Version Management Example

### Scenario
User generates test cases for the same requirement three times over a week due to requirement changes.

### Generated Versions

```
Test Case Versions for "User Registration Enhancement":
├── user-registration-enhancement-v0318_143052.md (March 18, 14:30:52)
│   └── Initial generation based on v1.0 requirements
│   └── Test cases: 45
│   └── Modules: User Registration Module, Error Handling Module
│
├── user-registration-enhancement-v0319_101530.md (March 19, 10:15:30)
│   └── Updated after requirement change: added phone number field
│   └── Test cases: 58 (+13 new)
│   └── Modules: User Registration Module, Error Handling Module, Phone Verification Module
│
└── user-registration-enhancement-v0320_090000.md (March 20, 09:00:00)
    └── Updated after requirement change: removed email verification, added social login
    └── Test cases: 72 (+14 new, -5 removed)
    └── Modules: User Registration Module, Error Handling Module, Phone Verification Module, Social Login Module
```

### Version Comparison Report

**Comparing v0318_143052 vs v0320_090000**:

| Metric | v0318_143052 | v0320_090000 | Change |
|--------|--------------|--------------|--------|
| Total Test Cases | 45 | 72 | +27 |
| Modules | 2 | 4 | +2 |
| P0 Cases | 8 | 12 | +4 |
| P1 Cases | 25 | 38 | +13 |
| P2 Cases | 12 | 22 | +10 |
| Positive Cases | 30 | 48 | +18 |
| Negative Cases | 15 | 24 | +9 |
| Coverage | 85% | 96% | +11% |

**Added Modules**:
- Phone Verification Module (13 test cases)
- Social Login Module (19 test cases)

**Removed Test Cases**:
- Email format validation (3 cases) - replaced by phone validation
- Email verification token (2 cases) - no longer required

**Modified Test Cases**:
- Registration form submission: added phone number as required field
- Registration success message: updated to mention phone verification instead of email

### Version Management Benefits Demonstrated

1. **Historical Traceability**: Can see how test cases evolved with requirements
2. **Impact Analysis**: Clear view of what changed between versions
3. **Rollback Capability**: Can revert to v0318_143052 if needed
4. **Audit Trail**: Complete history for compliance and review
5. **Progress Tracking**: Shows testing coverage improvement over time

### How to Access Previous Versions

When user asks: "Show me the previous version of user registration test cases"

**Response**:
```
Available versions for "User Registration Enhancement":

1. v0320_090000 (March 20, 09:00:00) - Latest
   - File: user-registration-enhancement-v0320_090000.md
   - Test cases: 72
   - Changes: Added social login module

2. v0319_101530 (March 19, 10:15:30)
   - File: user-registration-enhancement-v0319_101530.md
   - Test cases: 58
   - Changes: Added phone number field

3. v0318_143052 (March 18, 14:30:52)
   - File: user-registration-enhancement-v0318_143052.md
   - Test cases: 45
   - Changes: Initial version

Which version would you like to view or compare?
```
