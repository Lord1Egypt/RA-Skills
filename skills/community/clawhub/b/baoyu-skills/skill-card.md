## Description:

Baoyu Skills is a Claude Code skill bundle for content generation, conversion, publishing, translation, and image processing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conanwhf](https://clawhub.ai/user/conanwhf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and social media operators use this bundle to generate images and slide decks, convert web and social content to Markdown or HTML, translate articles, format Markdown, compress images, and publish content to social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some workflows use browser automation, authentication cookies, and local session state.

Mitigation: Use a dedicated Chrome profile, avoid reusing a normal signed-in debugging session, and review or delete local cookie and session files after use.

Risk: Some workflows rely on reverse-engineered services or platform posting behavior that can break or affect user accounts.

Mitigation: Use those workflows only after explicit consent and with accounts where automation risk is acceptable.

Risk: Some generation and rendering flows may send prompts, documents, diagrams, or media to external providers.

Mitigation: Avoid private or sensitive content unless the configured provider or rendering server is approved for that data.

Risk: The bundle requires Bun and runs local scripts from the installed package.

Mitigation: Prefer installing Bun directly and review the package and scripts before running workflows with sensitive inputs.

## Reference(s):

- [ClawHub Baoyu Skills page](https://clawhub.ai/conanwhf/skills/baoyu-skills)
- [Publisher profile](https://clawhub.ai/user/conanwhf)
- [Top-level skill manifest](artifact/SKILL.md)
- [README](artifact/README.md)
- [Chrome profile guidance](artifact/docs/chrome-profile.md)
- [Image generation guidance](artifact/docs/image-generation.md)
- [Testing strategy](artifact/docs/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, generated media files, HTML, slide assets, shell commands, and configuration snippets depending on the selected subskill.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Bun; some subskills use API credentials, Chrome/CDP browser automation, consent-gated reverse-engineered services, or platform accounts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
