# anime-asset-pipeline

A pipeline for generating anime/2D character art with an AI image model, where the **same character has to stay recognisable across hundreds of images**.

Most AI art skills tell the agent what good taste looks like. This one tells it **which specific things will go wrong, and how to catch them before spending the render.**

---

## The problem

You are producing a character across many images — a sprite set, a key visual series, MV frames. Three things reliably go wrong, and none of them are taste problems:

1. **Identity drifts.** Text-to-image cannot hold a character across images. Every generation is a slightly different person.
2. **Defects hide in specific regions.** Hands, local hair colour, frame-to-frame transitions. Nobody finds them by glancing at the result.
3. **Renders get wasted on changes that cannot be seen.** Parameters get tuned, criteria go green, and the finished piece looks identical to the last one.

## What this skill actually enforces

| Rule | Why it is here |
|---|---|
| Fix the picture layer, not the parameter layer | Look problems are composition/lighting/grading problems. Tuning constants is not a fix. |
| Criteria prove correctness, never quality | A green checklist does not mean it looks good. Stop presenting it as if it does. |
| One A/B frame before any full re-render | Full re-renders to validate a small change are the largest source of wasted spend. |
| Stay inside the marked region | Scope creep on a fix is a defect, not a bonus. |
| Reuse is free; sameness is a treatment problem | Monotony comes from varying every section the same way, not from reusing an image. |
| Probe the channel every session | Tool definitions can be present while the channel is not mounted. Yesterday's result does not apply. |

## The 8-bit budget

This is the part nobody else has, because it costs renders to find out.

On 8-bit material the quantisation step is `1 / base`:

| base | step |
|---|---|
| 200 | 0.005 |
| 220 | 0.0045 |
| 240 | 0.00417 |

Measured consequences:

- decay constant **6 → 5** moves the output about **one level** — indistinguishable
- peak **1.03 → 1.06** moves it **one or two levels** — also not visible

**Micro-tuning parameters on 8-bit source cannot produce a visible difference.** If the only justification for a change is that the numbers moved, the change did not happen.

## Identity locking

Text-to-image does not hold identity. The working mechanism:

1. Establish **anchor images** — canonical views of the character.
2. Derive every image **image-to-image from an anchor**. The prompt guides pose and framing; the anchor supplies identity.
3. Verify **feature by feature** against real reference images. Not "it looks like her."

Known failure: a model that holds the character overall can still fail on a **local** colour feature. Three attempts at the same local feature is enough evidence — change the approach, don't retry.

## Install

```
npx skills add CatsMansion/anime-asset-pipeline
```

Or clone into your skills directory:

```
git clone https://github.com/CatsMansion/anime-asset-pipeline.git
```

Works with any agent that reads `SKILL.md` — Claude Code, Codex, Cursor, Gemini CLI, Copilot, Windsurf, and the rest.

### Frontmatter is spec-clean

All four fields used here sit within the six the standard allows (`name`, `description`, `license`, `metadata`), and `version` is nested under `metadata` rather than sitting at the top level.

That detail matters. A **top-level `version` key** is the most common reason a skill fails to upload to claude.ai or the Skills API, with a hard `Unexpected key(s) in SKILL.md frontmatter` error — not a warning, an error. As of October 2026 an audit of 158 catalogued skills with frontmatter found 12 using fields outside the spec. This one is not among them.

## Structure

```
anime-asset-pipeline/
├── SKILL.md                          # pipeline + the four iron rules
├── references/
│   ├── identity-lock.md              # anchors, feature-by-feature verification
│   ├── 8bit-budget.md                # quantisation arithmetic + decision rule
│   ├── defect-checklist.md           # per-region checks, animation metrics
│   └── channel-preflight.md          # availability probing, balance checks
└── assets/
    └── review-report-template.md     # failures-first report format
```

## Where this comes from

Distilled from two productions: a desktop-pet project with **1372 sprite assets**, and an anime music video. Every rule in here corresponds to a real failure that cost real renders — including a full re-render cycle spent proving that two parameter values one quantisation level apart look the same.

The thresholds in `references/defect-checklist.md` are recorded measurements from that project. They are given as examples of what a measured value looks like, **not as universal pass/fail targets**. Measure a known-good asset in your own project and set your own.

## Scope

Process discipline for 2D character art production. Not a prompt-syntax guide, and deliberately not tied to any specific model provider — those change, and this discipline does not.

## License

MIT
