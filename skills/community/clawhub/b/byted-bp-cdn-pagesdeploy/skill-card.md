## Description:

One-click deployment of static websites to BytePlus / VolcEngine Edge Pages platform, supporting auto project creation, update deployment, custom domain binding, and CDN acceleration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyao00-cloud](https://clawhub.ai/user/fanyao00-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to deploy and manage static websites on BytePlus / VolcEngine Edge Pages, including project creation, update deployment, custom domain binding, and local preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment and management commands can make service-affecting cloud changes, including project creation, updates, offline operations, and deletion.

Mitigation: Verify the exact project name, project ID, domain, and operation before running deploy, offline, or delete commands.

Risk: The setup and deployment scripts may persist BytePlus / VolcEngine credentials through the nest CLI.

Mitigation: Use short-lived or isolated credentials and avoid running the skill on shared machines or CI environments unless credential persistence is acceptable.

Risk: The deployment script can run user-provided build commands before uploading a site.

Mitigation: Use only trusted build commands and review the site project before deployment.

Risk: The scripts may install the @byteplus/nest npm package locally if the CLI is missing.

Mitigation: Review package installation behavior and run the skill in an isolated environment when automatic npm installation is not acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target BytePlus / VolcEngine Edge Pages and may require cloud credentials, a project name, a static site directory, and optional region or domain settings.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
