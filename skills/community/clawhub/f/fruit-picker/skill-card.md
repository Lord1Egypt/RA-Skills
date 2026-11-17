## Description:

Helps Chinese-speaking users evaluate supported fruit photos and user-provided details for ripeness, quality risks, variety confidence, and buying recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezra-y](https://clawhub.ai/user/ezra-y)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to decide whether to buy, avoid, or compare supported fruits from photos and targeted follow-up details. It covers Monthong durian, selected non-Monthong durians, mango, avocado, and watermelon within documented confidence limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photo-based fruit guidance can be mistaken for guarantees about sweetness, Brix, hollow core, or hidden internal quality.

Mitigation: Keep conclusions within the documented fruit-specific scope, include confidence limits, and avoid claims the references say are not supported.

Risk: Running helper scripts may install Pillow from the configured Python package source.

Mitigation: Run scripts in a restricted environment or preinstall reviewed dependencies when dependency supply-chain controls matter.

Risk: If bundled anchor images are missing, the workflow may fetch replacement images from GitHub.

Mitigation: Use the bundled images or disable network access when remote fetching is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ezra-y/skills/fruit-picker)
- [Skill definition](artifact/SKILL.md)
- [Common photo and confidence protocol](artifact/references/common.md)
- [Output guide](artifact/references/output-guide.md)
- [Monthong durian guide](artifact/references/fruits/durian-monthong.md)
- [Non-Monthong durian guide](artifact/references/fruits/durian-non-monthong.md)
- [Mango guide](artifact/references/fruits/mango.md)
- [Avocado guide](artifact/references/fruits/avocado.md)
- [Watermelon guide](artifact/references/fruits/watermelon.md)
- [Anchor image notes](artifact/references/anchors/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Chinese-language Markdown or plain text; helper scripts can emit JSON analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses high, medium, or low confidence labels and avoids unsupported sweetness, Brix, hollow-core, or internal-quality guarantees.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
