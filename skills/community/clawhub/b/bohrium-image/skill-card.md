## Description: <br>
Manage Bohrium container images via the bohr CLI or Bohrium image APIs, including listing, pulling, creating, deleting, and finding public images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Bohrium container images and find public or custom images for Bohrium container workloads. It is not intended for node management, job submission, or project management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an ACCESS_KEY to upload Dockerfiles and create, share, unshare, or delete remote Bohrium images. <br>
Mitigation: Install only for trusted Bohrium project or account contexts, verify image IDs before changes, and require explicit user confirmation before build, delete, share, or unshare actions. <br>
Risk: Dockerfile builds may upload secrets, proprietary source, or other sensitive content to Bohrium. <br>
Mitigation: Inspect Dockerfiles before any build and remove credentials, private assets, or proprietary content that should not leave the local environment. <br>


## Reference(s): <br>
- [Bohrium Image Management on ClawHub](https://clawhub.ai/sorrymaker0624/bohrium-image) <br>
- [Bohrium public image API](https://open.bohrium.com/openapi/v2/image/public) <br>
- [Bohrium public image version search API](https://open.bohrium.com/openapi/v2/image/public/version/search) <br>
- [Bohrium private image API](https://open.bohrium.com/openapi/v2/image/private) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose credentialed Bohrium CLI or API actions that should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
