## Description:

Use when you need thick, durable, washable, insulating floor coverings, doormats, or bed pads made from scrap fabric or old clothing and commercial rugs or mats are unreliable or unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan durable braided rag rugs from old clothing or scrap fabric. The agent helps identify suitable fabrics, calculate material needs, schedule work, track progress, and produce pattern, inventory, and barter templates while the human performs all physical crafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command is not version-pinned.

Mitigation: Use a reviewed or version-pinned ClawHub CLI invocation before installing.

Risk: The skill may store rug photos, inventory details, progress logs, templates, and reminders in local files.

Mitigation: Run it in a low-privilege environment and choose storage locations appropriate for the sensitivity of those files.

Risk: Physical rug-making steps involve sharp tools, repetitive motion, and material failure hazards.

Mitigation: Keep all tearing, cutting, braiding, stitching, and safety decisions under human control, use the stated safety checks, and test small sample coils before larger rugs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/braided-rag-rug-making-basics)
- [ClawHub publisher profile](https://clawhub.ai/user/howtousehumans)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with forms, schedules, checklists, templates, and inline shell command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update user-chosen local files for rug photos, inventory details, progress logs, templates, and reminders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
