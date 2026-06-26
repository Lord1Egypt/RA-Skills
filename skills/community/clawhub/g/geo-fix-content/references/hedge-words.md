# Hedge Language Dictionary

Reference for identifying and replacing hedge words that reduce AI citability.

## Why Hedge Language Matters

Research shows that AI engines prefer confident, authoritative statements when selecting content to cite:
- Hedged language ranks **3x lower** than confident assertions in AI citation (geo-optimizer research)
- Content with statistics increases AI citation probability by **30%** (Aggarwal et al., 2023)
- Direct answers are cited **2x more** than qualified statements

## Hedge Word Categories

### Uncertainty (High Severity)

Words that signal the author is unsure.

| Hedge Word | Replacement Pattern | Example |
|------------|-------------------|---------|
| maybe | [remove or replace with data] | "maybe improves" → "improves by 23%" |
| perhaps | [remove or state condition] | "perhaps useful" → "useful for [specific use case]" |
| possibly | [remove or quantify] | "possibly effective" → "effective in 89% of cases" |
| might | [remove or use present tense] | "might reduce" → "reduces" |
| could | [remove or specify condition] | "could help" → "helps when [condition]" |

### Qualification (Medium Severity)

Words that weaken otherwise strong statements.

| Hedge Word | Replacement Pattern |
|------------|-------------------|
| somewhat | [remove] or quantify the degree |
| relatively | replace with specific comparison |
| fairly | [remove] or use exact measure |
| rather | [remove] |
| quite | [remove] or quantify |

### Approximation (Medium Severity)

Words that avoid precision.

| Hedge Word | Replacement Pattern |
|------------|-------------------|
| about | use exact number or tight range |
| around | use exact number |
| approximately | use exact number or "±X%" |
| roughly | use exact number |
| nearly | use exact number (e.g., "nearly 100" → "97") |

### Distancing (High Severity)

Words that create distance between the author and the claim.

| Hedge Word | Replacement Pattern |
|------------|-------------------|
| seems | "X seems to Y" → "X Y" (direct statement) |
| appears | "appears to be" → "is" |
| tends to | "tends to improve" → "improves" + condition |
| suggests | "data suggests" → "data shows" |
| likely | remove or quantify probability |
| arguably | [remove] — either argue it or don't |

### Generalization (Medium Severity)

Words that avoid committing to specifics.

| Hedge Word | Replacement Pattern |
|------------|-------------------|
| generally | [remove] or specify when it's not true |
| usually | quantify: "in 85% of cases" |
| often | quantify: "in 7 out of 10 deployments" |
| sometimes | specify conditions when it occurs |
| typically | quantify or specify the typical case |
| in most cases | "in 92% of cases" or similar |

### Weakening (High Severity)

Phrases that undermine the statement's authority.

| Hedge Phrase | Replacement |
|-------------|-------------|
| a bit | [remove] or quantify |
| sort of | [remove] |
| kind of | [remove] |
| in some ways | specify which ways |
| to some extent | quantify the extent |
| it could be argued that | [remove] — just state the argument |
| it is worth noting that | [remove] — just state the note |

---

## Hedge Density Calculation

```
Hedge Density = (total hedge word/phrase count) / (total word count) × 100
```

| Range | Rating | Action |
|-------|--------|--------|
| < 0.5% | Excellent | No action needed |
| 0.5-1.0% | Good | Minor cleanup recommended |
| 1.0-2.0% | Needs Work | Systematic rewrite needed |
| > 2.0% | Critical | Fundamental tone issue — full content review |

---

## Before/After Examples

### Example 1: SaaS Product Description

**Before** (Hedge Density: 4.2%):
> Our platform might help companies possibly reduce their operational costs. It seems to work fairly well in generally most enterprise scenarios, and could potentially improve efficiency to some extent.

**After** (Hedge Density: 0%):
> Our platform reduces operational costs by 34% on average across 150 enterprise deployments (2025 data). It achieves a 97% success rate in enterprise scenarios with measurable efficiency gains within 30 days.

**Changes**: Removed 8 hedge words, added 3 specific metrics, added source context.

### Example 2: Technical Blog Post

**Before** (Hedge Density: 3.1%):
> This approach is arguably better than traditional methods. It tends to perform somewhat faster and usually produces relatively more accurate results in most situations.

**After** (Hedge Density: 0%):
> This approach outperforms traditional methods by 2.3x in benchmark tests (IEEE 2025). It processes requests 45% faster and achieves 99.1% accuracy — compared to 94.7% for the baseline.

**Changes**: Removed 6 hedge words, added benchmark source, added specific performance numbers.

### Example 3: Service Page

**Before** (Hedge Density: 2.8%):
> We generally help businesses improve their online presence. Our team has perhaps some of the best expertise in the industry and could likely deliver results for your company.

**After** (Hedge Density: 0%):
> We have improved online visibility for 200+ businesses since 2019, with an average traffic increase of 156%. Our team of 12 certified specialists has delivered measurable results for Fortune 500 companies including [Client A] and [Client B].

**Changes**: Removed 5 hedge words, added client count, added specific metrics, added social proof.
