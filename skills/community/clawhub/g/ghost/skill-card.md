## Description: <br>
Manage Ghost CMS blog posts through the Ghost Admin API, including creating, updating, deleting, listing, uploading images, and setting feature images using a user-provided JSON credential config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to let an agent manage Ghost blog content through authenticated Admin API calls. It supports draft or published post workflows, tag updates, image uploads, and listing existing posts for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user-provided Ghost Admin API key can allow live blog publishing, updates, image uploads, and deletion. <br>
Mitigation: Keep the JSON config file private, use credentials only for Ghost sites you control, and rotate the Admin API key if the config is exposed. <br>
Risk: Create, update, publish, and delete operations can change public content. <br>
Mitigation: Require explicit confirmation before publishing or deleting live content, and review post IDs, titles, statuses, and target site configuration before write operations. <br>
Risk: Image upload and feature-image workflows can use local files or remote URLs. <br>
Mitigation: Use trusted local image files or trusted URLs and verify the resulting image URL before associating it with a post. <br>


## Reference(s): <br>
- [Ghost Admin API Reference](references/api.md) <br>
- [Ghost Official Admin API Docs](https://ghost.org/docs/admin-api/) <br>
- [ClawHub Skill Page](https://clawhub.ai/manifoldor/ghost) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell examples, plus Ghost Admin API responses and command-line status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JSON config file containing api_url and admin_api_key; operations may create, publish, update, delete, list, or upload content on the configured Ghost site.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
