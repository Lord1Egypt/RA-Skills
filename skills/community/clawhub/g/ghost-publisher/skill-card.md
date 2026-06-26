## Description: <br>
Ghost Publisher lets an agent publish, update, schedule, delete, retrieve, and upload media for Markdown articles on Ghost 5 CMS sites through a standard publisher interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[machinesofdesire](https://clawhub.ai/user/machinesofdesire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and editorial workflow agents can use this skill to automate Ghost CMS publishing tasks while keeping caller code aligned to Publisher Interface v1 rather than Ghost-specific API details. <br>

### Deployment Geography for Use: <br>
Global: Asia-Pacific (APAC), Europe, Middle East, and Africa (EMEA), Latin America (LATAM), and North America (NAM), subject to the user's Ghost site policies and applicable local requirements. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify live posts, delete posts, upload media, and send newsletters when configured with Ghost admin credentials. <br>
Mitigation: Use a dedicated Ghost custom integration key, test against drafts or staging first, and require human approval before publishing, emailing newsletters, or deleting posts. <br>
Risk: Ghost admin credentials are sensitive and could grant broad publishing access if exposed. <br>
Mitigation: Provide credentials through environment variables, keep them out of logs and repositories, and rotate the integration key if exposure is suspected. <br>
Risk: Media uploads from untrusted URLs or files can introduce unsuitable or unexpected content into the CMS media library. <br>
Mitigation: Restrict image inputs to trusted URLs or approved local files before using upload or publish workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/machinesofdesire/ghost-publisher) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/machinesofdesire) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python method calls, CLI commands, JSON-compatible post objects, Ghost CMS post URLs, and command-line text output.] <br>
**Output Parameters:** [1D: Ghost environment variables, optional JSON configuration, standard post objects, post identifiers, Markdown files, publish options, schedule timestamps, and image URLs or local paths.] <br>
**Other Properties Related to Output:** [Outputs may create or change Ghost drafts, published posts, scheduled posts, media assets, and newsletter sends on the configured Ghost site.] <br>

## Skill Version(s): <br>
1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
