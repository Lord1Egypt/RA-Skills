# M&A Agreement Review Example

## Prompt

```
Review this acquisition agreement. I'm the seller.
```

## Example Output

```markdown
# Contract Review: Asset Purchase Agreement

**Document Type:** Asset Purchase Agreement
**Your Position:** Seller
**Counterparty:** Acquirer Inc.
**Risk Level:** 🔴 High

## Executive Summary

$15M acquisition with 30% earnout, 18-month escrow, and 3-year rep survival.
Significant seller exposure post-closing. Earnout mechanics need protection.

---

## Key Terms

| Term | Value | Location |
|------|-------|----------|
| Base Purchase Price | $10,500,000 cash at closing | Section 2.1(a) |
| Earnout | Up to $4,500,000 (Y1-Y2 revenue) | Section 2.1(b) |
| Escrow | $1,575,000 (15%) for 18 months | Section 2.1(c) |
| Indemnification Cap | $3,000,000 (20% of total) | Section 10.4 |
| Rep Survival | 36 months | Section 10.2 |
| Non-Compete | 5 years, nationwide | Section 7.8 |

---

## Risk Analysis

### 🔴 Critical

**Earnout Mechanics** (Section 2.1(b), Exhibit C)
> "Earnout shall be calculated based on Revenue as determined by Buyer in its sole discretion"

- **Issue:** No objective standard; buyer controls calculation; no audit rights
- **Risk:** Buyer can manipulate to minimize earnout
- **Redline:** Add:
  - "Revenue calculated per GAAP, consistent with historical practices"
  - "Seller audit rights within 30 days of each calculation"
  - "Buyer shall operate business consistent with past practice"
  - "Earnout accelerates in full upon change of control"

---

### 🔴 Critical

**Rep & Warranty Survival** (Section 10.2)
> "All representations and warranties shall survive for 36 months"

- **Issue:** 3-year survival is longer than market (12-18 months typical)
- **Redline:** Change to "18 months for general reps; 36 months only for fundamental reps (title, authority, cap)"
- **Fallback:** Accept 24 months

---

### 🔴 Critical

**Non-Compete** (Section 7.8)
> "Seller shall not engage in any competitive business for 5 years anywhere in the United States"

- **Issue:** 5-year nationwide non-compete may be unenforceable; exceeds market (2-3 years)
- **Redline:**
  - Duration: "five (5) years" → "three (3) years"
  - Geography: "United States" → "states where Business operates"
  - Add clear definition of "competitive"

---

### 🟡 Important

**Sandbagging** (Section 10.5)
> "Buyer's right to indemnification shall not be affected by any investigation or knowledge"

- **Issue:** Pro-sandbagging lets buyer claim for issues known pre-close
- **Redline:** Add anti-sandbagging: "Buyer may not seek indemnification for matters actually known to Buyer prior to Closing"

---

### 🟡 Important

**Basket Structure** (Section 10.4)
> "First dollar basket of $150,000"

- **Issue:** First-dollar (tipping) basket means once threshold met, buyer recovers from dollar one
- **Redline:** Convert to true deductible: "Seller liable only for amounts exceeding $150,000"

---

## Reviewed & Acceptable

| Category | Status | Notes |
|----------|--------|-------|
| Escrow Amount | ✓ | 15% is within market range |
| Escrow Duration | ✓ | 18 months is standard |
| Indemnification Cap | ✓ | 20% is reasonable |
| Governing Law | ✓ | Delaware |

---

## Missing Provisions

| Provision | Priority | Suggested Language |
|-----------|----------|-------------------|
| Earnout Operating Covenants | Critical | "Buyer shall operate Business consistent with past practice and not take actions primarily intended to reduce Earnout" |
| R&W Insurance Acknowledgment | Important | "Buyer shall first seek recovery under R&W insurance before asserting claims against Seller" |
| Earnout Acceleration | Important | "Upon change of control of Buyer, unpaid Earnout accelerates at target amount" |

---

*This review is for informational purposes only. M&A transactions require qualified legal and tax counsel.*
```

## Seller Protection Checklist

1. **Maximize cash at close** — earnouts, escrows, holdbacks reduce certainty
2. **Earnout protections** — operating covenants, audit rights, acceleration
3. **Short rep survival** — 12-18 months general, longer only for fundamental
4. **True deductible basket** — not first-dollar/tipping
5. **Reasonable indemnification cap** — 10-15% excluding fraud
6. **Anti-sandbagging** — buyer can't claim for known issues
7. **Reasonable non-compete** — 2-3 years, limited geography
8. **Partial escrow release** — at 12 months if no claims
9. **D&O tail** — buyer to purchase or fund
