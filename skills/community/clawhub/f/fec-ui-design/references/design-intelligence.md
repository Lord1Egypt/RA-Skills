#DesignSmartReference

This reference is used to turn obscure UI requests into an executable design system. Start by identifying the product category, then combine style archetypes, color roles, font moods, motion rhythms, graphic tasks, and UX risks.

## Decision-making process

1. Extract keywords: product type, users, scenarios, main tasks, content density, brand tone, technology stack.
2. Write out the design reads: page type, audience, primary mission, brand constraints, and sources of trustworthiness.
3. Match product rules: Select the closest category from `data/product-rules.json` and record the recommended structure, risks and anti-patterns.
4. Select style archetypes: Select 1 main style and up to 1 auxiliary style from `data/style-archetypes.json` to avoid style collage.
5. Set the design dial: visual tension, motion intensity, information density, media authenticity, and content persuasiveness are all expressed on a scale of 1-10, and vary with the page type.
6. Establish token direction: define the semantic roles of main color, accent color, background, foreground, border, dangerous color and focus ring.
7. Choose font mood: Don’t just choose a “good-looking font”, explain the tone and readability of the title and body text respectively.
8. Judgment of data expression: Use polylines/areas for trends, columns for comparisons, donut charts to form a small number of categories, funnels/steps for processes, and tables must be retained for details.
9. Output anti-patterns and quality gates: Every design suggestion must be accompanied by a “what not to do” and supplemented with above-the-fold, CTAs, media authenticity, section changes, and state integrity checks based on page type.

## Direction Advisor

When the user only says "looks better", "give me some directions", "I don't know what style" and there is no authoritative design draft, don't continue to ask general questions about taste. First, give 3 directions with obvious differences so that users can judge the choice.

Each direction must contain:

- Applicable scenarios: Why it is suitable for the current product, audience and task.
- Visual anchors: information structure, real media, data form, material, font character, spatial organization or interaction rhythm.
- Key tokens: main color, accent color, background, font mood, rounded corners/border/shadow tendency.
- What to avoid: This is the easiest templating error to slip into.

The three directions should come from different design logics, such as:

- Information architecture type: high-density, rational, data-first, suitable for B2B, operations, finance, and engineering tools.
- Editorial narrative type: layout, white space, strong text hierarchy, suitable for brand stories, content products, and portfolios.
- Product demonstration type: real screenshots, objects, status, and process evidence are given priority, suitable for SaaS, hardware, and developer tools.
- Experimental expression: strong motion effect, sense of space, generative vision, suitable for release pages, event pages, and art/creative projects.
- Warm and humanistic: low-offensive colors, approachable illustrations or real characters, suitable for education, health, and lifestyle.

After the user chooses the direction, then implement it into the design system and page structure; do not collage the 3 directions into a mixed system.

## Real assets take priority

Brand or product related UI recognition comes from real assets, not color guesswork. Priority:

1. Logo, product pictures, real UI screenshots, physical photos, and brand application pictures.
2. The project already has icons, components, data status, charts and screenshots.
3. Special assets generated for the current task.
4. Clearly marked structured placeholder.

Don’t use CSS outlines, generic illustrations, fake screenshots, or remote placeholder images to replace the subject that users need to identify. When there is a lack of key assets, first mark the asset gap and provide an alternative route; if the logo or main product is the core of first-screen recognition, confirmation should be suspended or changed to a structural plan that does not rely on brand recognition.

## v0 calibration

When the visual risk is high, the direction is unclear, or the page has a large impact, deliver a viewable v0 first instead of doing the entire page at once.

v0 should contain:

- Core layout, first screen hierarchy, main token and a key module.
- Clarify placeholder and asset gaps.
- 1-2 alternative direction points such as density, color temperature or media strategy.
- Does not include the full state matrix, all content details, or production-grade animations.

After v0 is passed, components, states, responsiveness and interactive effects will be completed.

## Design Critique

When users request to "review the UI", "whether it looks good or not", "more advanced" or a self-inspection is required before delivery, output specific questions in 5 dimensions instead of just giving subjective descriptions:

- Directional consistency: Whether the visual choice serves the design read and product mission.
- Hierarchy and scanning: Whether the first screen, title, CTA, data, and status are clearly prioritized.
- Workmanship quality: spacing, alignment, number of colors, text wrapping, rounded corners/borders/shadows are stable.
- Function completeness: whether loading, empty, error, disabled, hover, focus, and selected are covered.
- Originality and recognition: whether to get rid of universal gradients, three cards, fake screenshots, and bodyless heroes.

The output should give executable fixes by severity, without judging the designers themselves.

## When to run the generator

Generate design system recommendations using the following command:

```bash
node skills/fec-ui-design/scripts/design-system.mjs "beauty spa booking" --project "Serenity Spa"
```

Output Markdown is suitable for pasting into plans or PR descriptions; output JSON is suitable for testing or tool consumption:

```bash
node skills/fec-ui-design/scripts/design-system.mjs "fintech analytics dashboard" --format json --stack next
```

## Output must answer

- What is the main task of this interface?
- What are the design reads and the five design dials?
- What page structure or workspace structure is recommended?
- What is a visual anchor and why does it fit the business?
- What goals do the main style, font, color, and animation serve respectively?
- How to deal with charts and data density?
- What anti-patterns must be avoided?
- What is the minimum QA checklist before going live?
