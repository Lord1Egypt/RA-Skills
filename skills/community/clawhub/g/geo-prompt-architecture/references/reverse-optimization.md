# Reverse Optimization

Use this reference when the user has AI visibility monitoring results and wants to improve the prompt system or the client’s content and assets.

## 1. The loop

Use this loop:

`Prompt monitoring -> answer analysis -> loss-reason tagging -> asset recommendation -> prompt-set evolution`

Do not stop at visibility reporting. Translate misses into actions.

## 2. What to inspect for each prompt

At minimum, inspect:

- brand mention: yes / no
- mention type: recommendation, list inclusion, comparison, weak mention
- relative position: early, middle, late, absent
- brands shown instead
- cited source types
- answer framing

## 3. Loss-reason tags

Default loss reasons:

- `No Brand Mention`
- `Wrong Category Mapping`
- `Weak Comparison Presence`
- `Weak Commercial Fit`
- `Weak Evidence Support`
- `Weak Brand Entity`
- `Weak Product-Line Mapping`
- `Weak Channel Presence`

Use one primary tag and optional secondary tags.

## 4. Action buckets

Map every loss reason to one or more action buckets:

### Content actions

Examples:

- educational article
- comparison page
- buying guide
- FAQ
- scenario guide
- style guide

### Page / asset actions

Examples:

- category page
- product page rewrite
- use-case page
- sizing page
- returns / shipping page
- marketplace listing rewrite

### Evidence / entity actions

Examples:

- reviews
- third-party mentions
- case studies
- structured product facts
- clearer product-line entities
- stronger competitive framing

### Prompt-set actions

Examples:

- delete low-value prompts
- split broad prompts into scenario prompts
- add competitor prompts
- add brand-defense prompts
- add channel prompts
- rebalance the layer mix

## 5. Recommended output format

Use a table when possible:

| Prompt | Result | Loss Reason | Recommended Action | Prompt Update |
|---|---|---|---|---|
| Prompt A | Brand absent | Weak Product-Line Mapping | Build a stronger use-case page | Add a more specific scenario prompt |

## 6. Prompt-pool evolution rules

Improve the monitoring set over time:

- remove prompts with low business and low monitoring value
- merge prompts that produce the same answer pattern
- add prompts that expose competitor substitution clearly
- add prompts that reflect missing scenarios or channels
- keep a stable benchmark set for trend comparison

The goal is not just to have more prompts. The goal is to have a prompt library that reveals why the brand wins or loses in AI answers.
