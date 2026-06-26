## Description: <br>
Manage Cloudflare DNS records through the Cloudflare API, including listing, creating, updating, deleting, and DDNS updates for common record types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pushp1997](https://clawhub.ai/user/pushp1997) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site operators, and agents use this skill to inspect and manage Cloudflare DNS records, automate DDNS updates, and prepare DNS maintenance commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloudflare API tokens can grant sensitive DNS permissions if exposed or over-scoped. <br>
Mitigation: Use a least-privilege Cloudflare token, avoid logging or sharing it, and keep credentials in the environment or another secure secret store. <br>
Risk: Incorrect DNS create, update, delete, or DDNS operations can disrupt websites, email, or services. <br>
Mitigation: List and verify target records before changes, review proposed commands before execution, and confirm record IDs before deletion or update. <br>


## Reference(s): <br>
- [Cloudflare DNS skill page](https://clawhub.ai/pushp1997/cloudflare-dns) <br>
- [Cloudflare API v4 endpoint](https://api.cloudflare.com/client/v4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; script execution can return JSON or tabular text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CF_API_TOKEN and may use CF_ZONE_ID; commands can change DNS records.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
