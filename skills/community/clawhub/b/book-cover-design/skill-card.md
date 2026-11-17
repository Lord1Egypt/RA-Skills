## Description:

Book Cover Design helps agents create genre-appropriate book cover concepts with sizing guidance, typography rules, thumbnail checks, and AI image generation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

External creators, self-publishing authors, and publishing teams use this skill to plan ebook, print, audiobook, and mockup cover concepts that match genre expectations. It guides prompt generation, layout, typography, sizing, iteration, and print-readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes mutable remote installer and unpinned skill-install commands that can execute code or install unreviewed content.

Mitigation: Review installer contents before execution and use independently verified versions, checksums, or signatures where available.

Risk: Prompts or images sent to external AI services may include confidential manuscript details, unpublished artwork, or sensitive personal images.

Mitigation: Remove confidential or sensitive material from prompts and review external service data handling terms before use.

Risk: AI image models may render book-cover text unreliably.

Mitigation: Generate cover art or backgrounds first, then add title, subtitle, and author typography in a design tool.

## Reference(s):

- [Inference.sh](https://inference.sh)
- [Inference.sh CLI Installer](https://cli.inference.sh)
- [Inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt)
- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/book-cover-design)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and JSON prompt examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-specific image generation prompts, cover sizing recommendations, typography guidance, and review checklists.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
