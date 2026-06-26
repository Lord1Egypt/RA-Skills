---
name: cold-start-path
description: Choose the best first growth path for a new product, new shop, or weak early-stage offer based on product shape, margin room, content readiness, and channel constraints. Use when the user asks what to do first instead of trying search, creators, ads, live, and content all at once.
---

# Cold Start Path

Choose the first path before the team wastes time spreading effort everywhere.

## Skill Card

- **Category:** Growth Planning
- **Core problem:** What should we try first for cold start?
- **Best for:** New products, new stores, and stalled early-stage launches
- **Expected input:** Product info + margin room + asset readiness + channel constraints
- **Expected output:** First-path recommendation + why now + what to delay
- **Creatop handoff:** Feed decision into first-week content, creator, and ad execution

## Before you run

Ask the user to clarify:
- product category
- average selling price
- margin room
- whether the item is standard or non-standard
- whether they have content assets already
- whether they have creator access
- whether they have ad budget
- which channels are already live

If key facts are missing, ask for them before recommending a path.

## Optional tools / APIs

Useful but not required:
- store export
- ad spend export
- product sheet
- search trend export
- Google Sheets / CSV

If no tools are connected, continue with user-provided constraints and label the result as rule-based guidance.

## Workflow

1. Confirm cold-start scope.
2. Classify the product by margin, complexity, and content-friendliness.
3. Check readiness across five paths:
   - search
   - merchant content
   - creator content
   - paid ads
   - live selling
4. Recommend the best first path.
5. Name the second path to add later.
6. Explicitly say what not to do yet.

## Output format

Return in this order:
1. Executive summary
2. Best first path
3. Why this path fits now
4. What to delay
5. First 7-day move list

## Fallback mode

If the user only gives a rough product description:
- infer the most likely first path from product type, margin, and asset readiness
- mark assumptions clearly
- avoid fake certainty

## Quality rules

- Do not recommend five paths at once.
- Favor sequencing over complexity.
- Match the path to actual constraints, not ideal conditions.
- Say “not enough info” when the path depends on missing economics.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
