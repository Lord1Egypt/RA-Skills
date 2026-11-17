## Description:

Manage Cloudflare DNS records via API. Use when user asks to list, create, update, or delete DNS records, set up DDNS, manage domains on Cloudflare, or check DNS propagation. Supports A, AAAA, CNAME, TXT, MX, and other record types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pushp1997](https://clawhub.ai/user/pushp1997)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and modify Cloudflare DNS records, including zone lookup, record creation, updates, deletion, and DDNS updates through the bundled shell script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, delete, and DDNS-update live Cloudflare DNS records when given an API token.

Mitigation: Use a Cloudflare token restricted to the needed zone and DNS permissions, and require the agent to show the current record plus the exact planned change before any create, update, delete, or DDNS action.

Risk: Cloudflare API tokens could be exposed if copied into prompts, logs, files, or command history.

Mitigation: Store the token in a protected environment variable or secret manager, keep it out of logs and files, and rotate it if exposure is suspected.

Risk: DDNS behavior can create or update an A record based on the public IP returned by external lookup services.

Mitigation: Confirm the target record name and resolved public IP before applying DDNS changes, especially for production hostnames.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pushp1997/skills/cloudflare-dns)
- [Cloudflare API endpoint](https://api.cloudflare.com/client/v4)
- [ipify public IP service](https://api.ipify.org)
- [ifconfig.me public IP service](https://ifconfig.me)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Cloudflare API credentials from environment variables or command flags; the bundled script emits JSON for record operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
