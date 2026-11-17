# Test scenario design

Turn each acceptance criterion (AC) in the PRD into an executable test scenario for direct use by R&D/testing to avoid "the acceptance criteria are written but cannot be tested".

---

## 1. Test scenario template

```
Test scenario: [scenario name]

Test goal: [What to verify]

Initial conditions:
- [System status]
- [Required data]
- [User Settings]

Test steps:
1. [Action 1] → [Expected Result 1]
2. [Action 2] → [Expected Result 2]
3. [Action 3] → [Expected Result 3]

Expected results:
- [Observable 1]
- [Observable 2]
```

Correspondence: one AC → at least one test scenarios; the scene name can directly reference the AC number, such as "test scenarios (corresponding toAC-2)".

---

## 2. Example

**Test scenario**: View recently viewed products on the product details page

**Test goal**: Verify that the "Recently Viewed" area is displayed correctly and exclude the current product

**Initial conditions**:

- User is logged in
- The user has viewed at least 2 items in this session

**Test steps**:

1. Enter any product details page → the "Recently Viewed" area should appear
2. Scroll to the bottom of the page → Verify product card display
3. Check the current product → not in the recently viewed list
4. Click on the product card → jump to the corresponding details page
