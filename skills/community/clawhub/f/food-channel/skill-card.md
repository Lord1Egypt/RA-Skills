## Description:

Handle messages in a food-tracking channel by routing food intake events through a deterministic food tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill in a dedicated food-tracking channel to log barcode-based food entries, estimate nutrition from meal photos, and produce daily nutrition summaries with configurable limit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The photo-estimate workflow may pass model-generated JSON through shell interpolation.

Mitigation: Review or patch the estimate command so structured JSON is passed directly through stdin without shell interpolation before installation.

Risk: Meal photos may be processed by the platform vision model during photo estimates.

Mitigation: Use photo estimates only when users accept that image-processing path and avoid submitting sensitive or unnecessary image content.

Risk: Nutrition entries are stored persistently and FOOD_LOG can redirect where those entries are written.

Mitigation: Set FOOD_LOG only to a trusted workspace path and review local access controls for the food log.

## Reference(s):

- [ClawHub Food Channel skill page](https://clawhub.ai/cdmichaelb/skills/food-channel)
- [Open Food Facts API](https://world.openfoodfacts.org/api/v2/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown replies with inline shell commands, JSON command output, and CSV food-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent nutrition logs to a workspace CSV and may process resized meal photos through the platform vision model.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
