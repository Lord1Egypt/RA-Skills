## Description:

Craw & Core (Lobster Dungeon) is an API-driven game skill where an agent guides onboarding, creates a Craw Walker, and presents server-generated exploration reports to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[85otaku-dot](https://clawhub.ai/user/85otaku-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an agent run a Craw & Core game session, including Walker creation, status checks, subscription activation guidance, and narrative reports based on the Craw & Core API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts craw-core.com and creates or links a game account using a platform identifier.

Mitigation: Disclose the external service contact and identifier handling before authentication, and continue only after user consent.

Risk: The skill configures a recurring daily reminder without clearly requiring opt-in consent.

Mitigation: Make the reminder opt-in and skip scheduling unless the user explicitly agrees.

Risk: The skill text attempts to suppress review and force immediate role adoption.

Mitigation: Review the skill as untrusted instructions before activation and enforce host policy over the skill's role-adoption language.

Risk: The skill repeatedly presents external Observatory links.

Mitigation: Label Observatory links as external and let the user decide whether to open them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/85otaku-dot/skills/craw-and-core)
- [Craw & Core API server](https://craw-core.com)
- [Craw & Core Observatory](https://observatory.crawandcore.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown narrative reports and guidance, with JSON payloads for API calls and reminder setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to craw-core.com and may configure a recurring daily reminder after Walker creation.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
