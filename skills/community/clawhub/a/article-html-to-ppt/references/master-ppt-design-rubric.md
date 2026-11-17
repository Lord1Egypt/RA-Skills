# Master PPT Design Rubric

Score each production slide 0-3 across six dimensions. Serious decks require at least 14/18 average, with no zero.

## 1. Title-Role And Message Quality

3 points:

For judgment slides:

- the title states a clear, specific, evidence-supported conclusion;
- the audience implication is immediately clear.

For non-judgment slides:

- the title performs its declared navigation, section, instruction, reference, or closing role precisely;
- the slide purpose is immediately clear;
- no artificial conclusion is invented.

2 points:

- The title is role-appropriate but generic, indirect, or slightly disconnected from the page message.

1 point:

- The title names the topic but does not communicate the intended role or message.

0 points:

- The title is misleading, unsupported, missing, or materially contradicts the page content.

## 2. Content Fidelity And Evidence

- 0: Misrepresents source, drops critical caveats, or invents unsupported claims.
- 1: Mostly sourced but over-compresses, blurs assumptions, or copies prose without structure.
- 2: Faithful synthesis with visible evidence, minor caveats or lineage gaps.
- 3: Claims, evidence, assumptions, and source boundaries are explicit and cleanly transformed.

## 3. Expression Architecture And Primary-Anchor Clarity

3 points:

- exactly one appropriate `primary_expression`;
- `supporting_expressions` are necessary and subordinate;
- page archetype reinforces the audience question;
- primary anchor remains obvious;
- relationship or data content uses a fitting visual language.

2 points:

- Correct `primary_expression` and one primary anchor, with minor density, grouping, or supporting-expression issues.

1 point:

- Usable primary expression, but weak primary anchor, unclear supporting hierarchy, or poorly matched archetype.

0 points:

- no identifiable primary expression;
- multiple competing primary anchors;
- `hybrid_panel` is used without identifying the true primary expression;
- relationship content is reduced to generic cards with no simplification reason;
- prose/cards/table hide a relationship, trend, or decision logic.

## 4. Page Composition

- 0: Cluttered, cramped, overlapping, or visually confusing.
- 1: Basic alignment exists but hierarchy, spacing, or reading order is weak.
- 2: Clear layout with minor spacing, scale, or balance issues.
- 3: Strong hierarchy, generous whitespace, clear scan path, and professional balance.

## 5. Component Craft And Style Consistency

- 0: Components look like raw wireframes, screenshots, unstyled tables, or tangled connector maps.
- 1: Components are functional but visually uneven, repetitive, or style-inconsistent.
- 2: Components are polished enough, with minor inconsistencies.
- 3: Components feel deliberate, restrained, aligned to the style system, and easy to scan.

## 6. Editability And Delivery Hygiene

- 0: Claimed editable content is rasterized, text clips, media is missing, or render fails.
- 1: Core content partly editable but raster use, object counts, or conversion risks are unclear.
- 2: Core content editable, bounded raster disclosed, minor manual checks remain.
- 3: Message-bearing content editable, raster/SVG use intentional and bounded, render/readback verified.

## Budget Scoring

Exceeding a default node, connector, card, or table budget does not automatically reduce the score.

Score the consequence:

- unclear hierarchy;
- excessive crossings;
- unreadable density;
- competing anchors;
- weak grouping;
- poor presentation-distance legibility.

A slide over a default budget may still score well when the structure is clear, the primary anchor is obvious, and the audience can read it at presentation distance.

## Revision Triggers

Revise before handoff if any condition is true:

- average score below 14/18;
- any dimension scores 0;
- more than 20% of judgment-role slides use generic topic titles;
- any section, navigation, reference, cover, or closing slide invents an unsupported judgment;
- more than 15% of slides have clipping or overlap;
- formal deck pages look like wireframes or spec coverage output;
- key technical diagrams have connector webs or unclear ownership boundaries;
- ordinary card, table, matrix, metric, or simple chart content is rasterized without explicit approval.

## Scoring Evidence

Record formal scores with `schemas/rubric-score.schema.json`. Keep QA hard gates and the 18-point rubric independent: QA `fatal` or `error` issues block production readiness even when the rubric total reaches 14. A total below 14 or any dimension scored 0 also requires revision.

Automatic metrics may inform a dimension, but they do not replace human or configured model judgment. If no scorer is available, the scorecard must say `manual_review_required` instead of inventing final dimension scores.
