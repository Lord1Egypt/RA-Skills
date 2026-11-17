## Description:

Publishes HTML frontend projects to the PushWebly publishing platform, manages public or private project visibility, lists published projects, and can package published HTML projects as Android APKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[publisher-skill](https://clawhub.ai/user/publisher-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish local zipped HTML frontend projects to PushWebly, obtain shareable project URLs, change visibility, list existing projects, and request Android APK builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist plaintext account credentials in ~/.publisher/config.json.

Mitigation: Use a low-impact password, store credentials only after explicit consent, restrict the local config file to the user, and review or delete the config after use.

Risk: Conflicting visibility rules could publish a project publicly when the user expected private access.

Mitigation: Require an explicit public or private visibility choice before publishing and do not rely on default visibility behavior.

Risk: Project zip files are uploaded to the PushWebly remote publishing service.

Mitigation: Review zip contents for secrets, private data, and unintended assets before upload.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/publisher-skill/skills/ai-game-publisher)
- [Publisher Profile](https://clawhub.ai/user/publisher-skill)
- [Server-Resolved GitHub Provenance](https://github.com/publisher-skill/ai-game-publisher)
- [PushWebly Platform](https://pushwebly.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project URLs, visibility status, access-password handling guidance, and APK download URLs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
