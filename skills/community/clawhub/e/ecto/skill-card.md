## Description: <br>
Ghost.io Admin API CLI for managing blog posts, pages, tags, and content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visionik](https://clawhub.ai/user/visionik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site operators, and agents use Ecto to manage Ghost blog content, configuration, publishing workflows, and read-only site data through the Ghost Admin API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ghost Admin API keys grant site-admin access and may be stored in the local Ecto configuration. <br>
Mitigation: Install from a trusted pinned version, protect the local configuration file, and rotate the key if it is exposed. <br>
Risk: Publishing, deleting, scheduling, bulk operations, image uploads, and webhook creation can materially change a Ghost site. <br>
Mitigation: Require explicit confirmation for these actions and verify the target Ghost site before commands run. <br>


## Reference(s): <br>
- [Ecto on ClawHub](https://clawhub.ai/visionik/ecto) <br>
- [Ghost Admin API](https://ghost.io) <br>
- [libecto library](https://github.com/visionik/libecto) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create, edit, publish, schedule, delete, upload, or query Ghost Admin API resources.] <br>

## Skill Version(s): <br>
0.1.0 (source: changelog, released 2026-01-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
