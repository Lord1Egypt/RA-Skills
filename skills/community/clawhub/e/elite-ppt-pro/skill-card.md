## Description:

Elite PPT Pro helps agents create consulting-style presentation decks using research-first planning, cited data slides, structured slide layouts, PPTX generation, and an HTML preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forrestneo](https://clawhub.ai/user/forrestneo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and presentation-building agents use this skill to prepare strategy decks, investor presentations, market analyses, annual reviews, and business-framework slides from researched source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated slides may include fixed Elite PPT Pro branding without a clear user-controlled opt-out.

Mitigation: Review generated slides before client-facing use and remove or modify hardcoded branding when it is not appropriate.

Risk: The artifact is Chinese-first in examples, slide text, and font guidance, which may not match every desired output language.

Mitigation: Specify the required presentation language and font expectations before generation.

Risk: Research-heavy decks can contain stale or unsupported claims if source gathering is skipped.

Mitigation: Require current source citations for data slides and follow the bundled QA checklist before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forrestneo/skills/elite-ppt-pro)
- [Server-resolved GitHub source](https://github.com/forrestneo/elite-ppt-pro-skill/tree/main/elite-ppt-pro)
- [QA checklist](references/qa-checklist.md)
- [Slide type reference](references/slide-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript pptxgenjs code patterns and optional shell-command instructions for generating PPTX and HTML outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides creation of editable PPTX files and high-fidelity HTML previews, with required source citations on data slides.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
