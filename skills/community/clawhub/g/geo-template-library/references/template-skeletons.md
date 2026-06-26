# GEO Template Library – Template Skeletons

This file provides **ready-to-copy markdown skeletons** for the main template families described in
`templates-catalog.md`. Use these as concrete starting points when generating templates.

Comments marked with `<!-- GEO: ... -->` highlight sections that are especially important for
AI citation.

---

## 1. Definition Article (`definition-article`)

```markdown
# [Primary Topic]: Clear, Entity-Focused Title
<!-- GEO: Include the main entity name exactly as you want AI to use it. -->

## Summary
- [1–3 bullet points summarizing what this topic is and why it matters]
<!-- GEO: Make these bullets fact-focused and quotable. -->

## What is [Primary Topic]?
[1–3 concise paragraphs with a clear definition]
<!-- GEO: This is the core definition models will likely cite. -->

## Key Concepts and Components
- [Concept 1]: [Short explanation]
- [Concept 2]: [Short explanation]
- [Concept 3]: [Short explanation]

## Examples
- Example 1: [Short, concrete example]
- Example 2: [Short, concrete example]

## How [Your Brand / Product] Relates
[Explain how your brand/product interacts with or supports this topic]

## FAQ
Q1: [Common question]
A1: [Clear, factual answer]

Q2: [Common question]
A2: [Clear, factual answer]
```

---

## 2. FAQ Page (`faq-page`)

```markdown
# [Topic] FAQ
<!-- GEO: Make the title explicit, e.g. "[Product] Pricing FAQ". -->

## Overview
[1 short paragraph explaining what this FAQ covers and who it is for.]

## Quick Links
- [Section 1 anchor]
- [Section 2 anchor]
- [Contact / support link]

## [Section 1 Label]

Q1: [Question text]
A1: [Clear, factual answer in 2–5 sentences.]
<!-- GEO: Keep answers self-contained so they can be quoted individually. -->

Q2: [Question text]
A2: [Answer]

## [Section 2 Label]

Q3: [Question text]
A3: [Answer]

Q4: [Question text]
A4: [Answer]

## Related Resources
- [Link to deeper guide or docs]
- [Link to pricing / product page]
```

---

## 3. Comparison Guide (`comparison-guide`)

```markdown
# [Product / Approach] vs [Alternative]: Comparison Guide
<!-- GEO: Include exact product/approach names as users search for them. -->

## Who this comparison is for
[1–2 paragraphs on the audience and use case for this comparison.]

## At-a-glance comparison
<!-- GEO: This table is a key citation surface for models. -->
| Criterion          | [Option A]                         | [Option B]                         | Notes                            |
|--------------------|------------------------------------|------------------------------------|----------------------------------|
| Ideal for          | [Ideal user / company profile]     | [Ideal user / company profile]     | [Short explanation]              |
| Pricing model      | [Summary]                          | [Summary]                          | [Key differences]                |
| Key strengths      | [Bullets or short phrases]         | [Bullets or short phrases]         |                                  |
| Key limitations    | [Bullets or short phrases]         | [Bullets or short phrases]         |                                  |

## Detailed comparison by criteria

### [Criterion 1]
- [Option A]: [Explanation]
- [Option B]: [Explanation]

### [Criterion 2]
- [Option A]: [Explanation]
- [Option B]: [Explanation]

## Which option is best for whom?
<!-- GEO: Clear, opinionated but well-justified recommendations. -->
- Choose [Option A] if: [Conditions]
- Choose [Option B] if: [Conditions]

## FAQ
Q1: [Common objection or edge case]
A1: [Answer]

Q2: [Another question]
A2: [Answer]
```

---

## 4. How-to / Tutorial (`howto-guide`)

```markdown
# How to [Achieve Outcome] with [Product / Approach]

## Goal
[One or two sentences describing the final outcome.]

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## Step-by-step instructions

### Step 1 – [Step name]
[Detailed instructions. Include substeps as needed.]

### Step 2 – [Step name]
[Detailed instructions.]

### Step 3 – [Step name]
[Detailed instructions.]

## Tips and common mistakes
- Tip: [Helpful tip]
- Mistake: [Common error and how to avoid it]

## Example scenario
[Short example of a user applying this how-to in a realistic context.]

## Troubleshooting FAQ
Q1: [Common issue]
A1: [Solution or workaround]
```

---

## 5. Statistics Roundup (`stats-roundup`)

```markdown
# [Topic] Statistics for [Year]
<!-- GEO: Clearly specify topic and year so stats are easy to reference. -->

## Overview
[Short paragraph on what this stats page covers and how data was collected (if applicable).]

## Key takeaways
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

## [Theme 1] statistics

### Headline stats
- **[Stat 1 label]** – [Value]  
  Source: [Source name / method], [Year].
- **[Stat 2 label]** – [Value]  
  Source: [Source].

### Additional details
[Context, segment breakdowns, or caveats.]

## [Theme 2] statistics
[Repeat the same pattern as above.]

## Methodology and sources
- [Brief note on methodology]
- [List of main sources with links]
```

---

## 6. Product / Feature Page (`product-page`)

```markdown
# [Product / Feature Name]
<!-- GEO: Use the exact product/feature name as seen in other brand surfaces. -->

## Summary
- [1–3 bullets on what this product/feature is and who it is for]

## What [Product / Feature] does
[1–3 paragraphs describing core capabilities.]

## Key benefits
- Benefit 1: [Short explanation]
- Benefit 2: [Short explanation]
- Benefit 3: [Short explanation]

## Use cases
- Use case 1: [Scenario + outcome]
- Use case 2: [Scenario + outcome]

## Features
- [Feature group 1]
  - [Feature 1]: [Explanation]
  - [Feature 2]: [Explanation]
- [Feature group 2]

## Pricing and plans (high-level)
[High-level view of pricing model or plans. Link to detailed pricing page if needed.]

## FAQ
Q1: [Buying / implementation question]
A1: [Answer]

Q2: [Another question]
A2: [Answer]
```

---

## 7. GEO Blog / Deep-dive (`geo-blog`)

```markdown
# [Article Title]: [Optional subtitle]

## Summary
- [1–3 bullets summarizing the main thesis or key insights]

## Background
[Introduce the topic, context, and why it matters now.]

## Main argument or narrative

### Section 1 – [Key idea]
[Explanation, examples, data points.]

### Section 2 – [Key idea]
[Explanation, examples, data points.]

### Section 3 – [Key idea]
[Explanation, examples, data points.]

## Case studies or examples
- [Example 1]
- [Example 2]

## Key takeaways
- [Takeaway 1]
- [Takeaway 2]

## Optional FAQ
Q1: [Clarifying question]
A1: [Answer]
```

