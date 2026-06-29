# Source Notes

Use these notes when refreshing or extending the skill.

## google-labs-code/design.md

- DESIGN.md combines YAML front matter for machine-readable tokens with markdown
  prose for human-readable rationale.
- Tokens carry exact values; prose explains why those values exist and how an
  agent should apply them.
- The spec supports colors, typography, rounded scale, spacing, and component
  tokens.
- The linter checks broken token references, section order, contrast ratios,
  missing typography, missing primary colors, and token usage.
- The CLI can lint, diff, export, and print spec/rules; use lint and rendered
  screenshots together because token validity alone does not prove visual trust.
- For product launch work, treat the design file as a contract between Codex
  agents, not a mood board. Token values, component roles, and do/don't rules
  must be concrete enough to survive later automated edits.
- Source: https://github.com/google-labs-code/design.md

## designdotmd.directory

- Use as a discovery directory for DESIGN.md examples and style-system patterns.
- Treat entries as inspiration, not as normative rules for a product.
- Do not copy an example palette or layout blindly; map it to the product's own
  audience, domain, claims, and reviewer evidence needs.
- Use the directory as a breadth check before reusing a sibling product's visual
  system. A product family can share quality standards without sharing the same
  thumbnail, hero composition, or icon motif.
- Source: https://designdotmd.directory/

## OpenAI Codex Use Cases

- Codex guidance includes building responsive front-end designs, making granular
  UI changes, deploying websites, rendered QA, and saving repeatable
  workflows as skills.
- For release workflows, turn repeated review failures into durable skill gates
  and executable checks instead of relying on memory.
- For Cloudflare Pages or marketplace work, make the repeatable workflow include
  real screenshots, responsive QA, deployment readback, and public-link checks.
- Source: https://developers.openai.com/codex/use-cases

## Generated Image Designer

- Prefer `gpt-image-2-2026-04-21` when model selection is available.
- Generated imagery must have a written art direction and must be visually
  inspected at final rendered size plus thumbnail size.
- Generated imagery can support hero/promo/empty-state trust, but real product
  screenshots remain required for CWS evidence.

## OpenAI Curated Skills

- The public curated skills repository is a useful pattern source for skills
  that keep instructions compact and put reusable details into reference files.
- Figma-oriented curated skills reinforce the same design principle used here:
  inspect the real design/system first, produce structured sections, then verify
  visually instead of relying on prose claims.
- Source: https://github.com/openai/skills/tree/main/skills/.curated

## ClawHub Design And Copy Skills

- `clawhub search` surfaced landing-page, conversion-copywriting, frontend
  design, and design-review skills. Use them as idea sources, not automatic
  dependencies.
- Useful patterns imported into this workflow: five-second clarity checks,
  one-reader/one-offer/one-action copy briefs, proof-before-CTA ordering,
  screenshot-based design review, and anti-pattern checks for generic AI pages.
- Avoid carrying over external CLI dependencies or suspicious skill content
  into this skill. Keep the local workflow based on repo files, screenshots,
  image generation, and explicit gates.
