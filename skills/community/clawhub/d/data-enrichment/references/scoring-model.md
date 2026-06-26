# Default Lead Scoring Model

## Scoring Range: 1-100

### Company Fit (0-40 points)

| Factor | Weight | Criteria |
|--------|--------|----------|
| Industry match | 0-15 | Direct match = 15, adjacent = 8, weak = 3 |
| Company size | 0-10 | Within ICP = 10, close = 5, outside = 0 |
| Revenue range | 0-10 | Can afford service = 10, borderline = 5, too small = 0 |
| Location | 0-5 | Target geo = 5, adjacent = 3, outside = 0 |

### Timing & Intent (0-35 points)

| Factor | Weight | Criteria |
|--------|--------|----------|
| Recent funding | 0-10 | Last 6 months = 10, last 12 = 5, none = 0 |
| Hiring signals | 0-10 | Hiring in your area = 10, general hiring = 5, none = 0 |
| Trigger event | 0-10 | Strong trigger = 10, moderate = 5, none = 0 |
| Tech stack fit | 0-5 | Uses complementary tools = 5, neutral = 2, competing = 0 |

### Contact Quality (0-25 points)

| Factor | Weight | Criteria |
|--------|--------|----------|
| Decision maker identified | 0-10 | Direct contact = 10, indirect = 5, none = 0 |
| Seniority level | 0-5 | C-level = 5, VP = 4, Director = 3, Manager = 2 |
| Social activity | 0-5 | Active (posts weekly) = 5, moderate = 3, inactive = 0 |
| Email available | 0-5 | Verified = 5, pattern-based = 3, none = 0 |

## Tag Thresholds

| Score | Tag | Action |
|-------|-----|--------|
| 75-100 | 🔴 Hot | Immediate personalized outreach |
| 50-74 | 🟡 Warm | Include in weekly batch outreach |
| 25-49 | 🔵 Cool | Nurture sequence / newsletter |
| 1-24 | ⚪ Cold | Archive / revisit quarterly |

## Customization

Override default weights by specifying in your prompt:
```
Score these leads with custom weights:
- Industry match: 20 points (we only work with SaaS)
- Company size: 15 points (must be 50-500 employees)
- Funding: 5 points (less important)
- Decision maker: 20 points (critical)
```
