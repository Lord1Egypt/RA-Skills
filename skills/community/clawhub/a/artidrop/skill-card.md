## Description: <br>
Publish AI-generated content, including HTML pages, Markdown reports, multi-file sites, dashboards, and visualizations, to a shareable URL using Artidrop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenguo17](https://clawhub.ai/user/wenguo17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and OpenClaw users use this skill to publish generated reports, pages, dashboards, visualizations, or multi-file sites as shareable web links through Artidrop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected content may be uploaded to Artidrop and made accessible through a shareable link. <br>
Mitigation: Review content before publishing, avoid secrets and personal or confidential data unless appropriate visibility and account controls are in place, and use private visibility only with authentication. <br>
Risk: Anonymous publishing has lower rate limits and cannot update, delete, list, claim, or create private artifacts. <br>
Mitigation: Configure ARTIDROP_API_KEY only when authenticated management features, higher rate limits, or private artifacts are needed. <br>


## Reference(s): <br>
- [Artidrop](https://artidrop.ai) <br>
- [Artidrop CLI on npm](https://www.npmjs.com/package/artidrop) <br>
- [Artidrop on ClawHub](https://clawhub.ai/wenguo17/artidrop) <br>
- [Publisher profile](https://clawhub.ai/user/wenguo17) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and returned shareable URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish user-selected content to Artidrop over HTTPS and return a public, unlisted, or private URL depending on CLI options and authentication.] <br>

## Skill Version(s): <br>
1.3.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
