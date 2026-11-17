# userstory

As a supplementary form of expression to the function point table in PRD §4: the function point table prefers "research and development can be compared and implemented", and the user story prefers "telling clearly why and to whom it is valuable." For functional points that are complex or require value alignment across teams, it is recommended to write both.

---

## 1. User story template

```
Title: [function name]

Description: As [User Role], I want [Action] for [Benefit].

Design: [Design File Link]

Acceptance criteria:
1. [Clear, testable standards]
2. [observable behavior]
3. [System correct verification]
4. [Border case handling]
```

After the acceptance criteria are written, they can be moved directly to the "Acceptance Criteria (AC)" table in the PRD, or used as an expanded description of a certain AC.

---

## 2. INVEST standard

| Standard | Description |
|------|------|
| **I**ndependent | Independent, not dependent on other stories |
| **N**egotiable | Negotiable, non-fixed specifications |
| **V**aluable | Valuable to users |
| **E**stimable | Estimated workload |
| **S**mall | Moderate size |
| **T**estable | Testable and Acceptable |

---

## 3. Example

**Title**: Recently viewed area

**Description**: As an online shopper, I would like to see a "Recently Viewed" area on product detail pages so I can easily review items I have considered.

**Acceptance Criteria**:

1. For users who have viewed at least 1 product, the "Recently Viewed" area is displayed at the bottom of the product details page
2. For users who access the first item in this session, this area will not be displayed.
3. The current product is excluded from the display list
4. Area displays product pictures, titles and prices
5. Each card is marked with the viewing time (such as "5 minutes ago")
6. Click on the card to jump to the corresponding product details page
