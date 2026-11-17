## Description:

Generate submission issues for GitHub awesome-lists. Auto-creates formatted Issue content for awesome-indie, awesome-privacy, awesome-cloudflare, and 7 more popular awesome repositories. Highest ROI backlink strategy - permanent, free, high-authority links from starred repos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, founders, and marketing teams use this skill to draft GitHub awesome-list issue or pull-request submissions and to choose relevant repositories for a product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a generated URL-building shell/Python snippet that can run unintended code if hostile product names, titles, or body text are substituted into it.

Mitigation: Review generated commands before use and replace the snippet with an encoder that passes values as arguments rather than interpolating untrusted text into executable code.

Risk: The server security verdict is suspicious because the artifact mostly prints GitHub submission guidance but contains unsafe copy-paste command behavior.

Mitigation: Review this skill before installing or using it, and do not run generated commands with untrusted inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/skills/awesome-submitter-pro)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash and API command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository lists, issue and pull-request templates, submission guidance, formatting rules, and tracking examples.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
