# Consistency Checklist Reference

## Dimension definitions

### Numbers

Every figure must be identical across materials unless a specific rounding rule applies to a platform.

Check: amount, percentage, ratio, date, time window, score, rank.

Examples from documented incidents:

| Issue | Material A | Material B | Root cause |
|---|---|---|---|
| "GPU利用率达到100%" | "接近100%" | Absolute vs safe wording |
| 3人4小时→1人15分钟 | same | ✅ consistent |
| Morgan Stanley 4400x + IDC 92% | mixed in one sentence | Source conflation |

### Product names

Every product must use its official full name on first mention in every material. Abbreviations are acceptable after the first full-name introduction.

Check: formal name, abbreviation consistency, ownership (which product delivers which feature).

### Fact wording

The same underlying fact must be expressed with the same wording when the audience and platform are the same. When platforms differ, the core fact must still be preserved.

Check: published/accepted/included wording, milestones, legal status descriptions.

Examples:

| Issue | Material A | Material B |
|---|---|---|
| "论文已被VLDB接收" | "技术成果入选VLDB 2025" |
| "A、B、C、D等一线基金" | investment roles differ by round |

### Terminology

A technical term must mean the same thing in all materials. Cross-material mixing creates confusion.

Check: technical terms, framework names, category labels, positioning language.

### Source attribution

When the same figure is cited in multiple materials, the source mark must match. When different figures come from different sources, each must be independently tagged.

Check: source type, publication date, scope note.

### Structural promises

Material A stating "the next section will cover X" creates a reader expectation. If Material B (a companion piece) does not cover X, the inconsistency must be flagged.

Check: cross-references, section previews, series promises.

### Cross-platform drift

Multi-platform (WeChat, LinkedIn, Substack) versions of the same article must share core facts and judgments. Expression may differ by audience, but fact wording and source attribution must be examined.

Check: same fact, same source, same judgment across platforms.

## Severity rules

- P0: number or product-name error, legal-status wording drift, figure-caption mismatch.
- P1: source-attribution difference, cross-platform judgment rewording, terminology mixing.
- P2: non-critical rhetoric, platform-depth mismatch, structural promise not fulfilled.
