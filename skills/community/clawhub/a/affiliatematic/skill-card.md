## Description:

Affiliatematic guides agents through integrating AI-powered Amazon affiliate product recommendation widgets into websites using affiliatematic.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dowands](https://clawhub.ai/user/dowands)

### License/Terms of Use:


## Use Case:

Website owners, affiliate marketers, and developers use this skill to add Affiliatematic widgets, configure Amazon affiliate tags, whitelist domains, and place product recommendations on monetized content pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration embeds an unpinned third-party script that can run on visitor pages and change without site-owner review.

Mitigation: Before broad deployment, request version-pinned script URLs, SRI hashes, CSP guidance, or a sandboxed or self-hosted option.

Risk: The widget may inspect page content to generate product recommendations, which can be inappropriate for sensitive or private pages.

Mitigation: Use only on public, non-sensitive pages unless Affiliatematic's data handling, retention, and compliance posture has been verified.

## Reference(s):

- [Affiliatematic documentation](https://affiliatematic.com/docs)
- [Affiliatematic dashboard](https://affiliatematic.com/user/dashboard)
- [Affiliatematic revenue calculator](https://affiliatematic.com/calculator)
- [Amazon Associates](https://affiliate-program.amazon.com)
- [ClawHub skill page](https://clawhub.ai/dowands/skills/affiliatematic)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTML snippets, configuration steps, placement guidance, and troubleshooting notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party service URLs and widget embed examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
