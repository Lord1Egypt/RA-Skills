## Description:

☤CaduceusMail lets your OpenClaw automate an enterprise-level communications stack with one domain/mailbox combo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmtlssss](https://clawhub.ai/user/lmtlssss)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to automate Microsoft 365 mailbox, alias, Exchange, and Cloudflare DNS setup for enterprise outreach or support mail flows. It helps bootstrap, verify, provision, and retire mail lanes while preserving reply continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses high-value Microsoft 365, Exchange, and Cloudflare credentials for mail and DNS automation.

Mitigation: Use a dedicated least-privilege Entra service principal and a Cloudflare token limited to the target zone's DNS permissions.

Risk: The security scan notes that installation depends on the exact vendored CaduceusMail CLI being present and audited against the manifest.

Mitigation: Install only when the vendored release artifact is included and its integrity matches artifact/vendor/caduceusmail-release.json.

Risk: Environment forwarding can expose secrets placed under OPENCLAW_*, CADUCEUSMAIL_*, or EMAIL_ALIAS_FABRIC_* variables.

Mitigation: Keep unrelated secrets out of those environment variable namespaces and prefer explicit OpenClaw skill environment injection.

Risk: The wrapped operations can mutate Exchange accepted domains, service-principal roles, and Cloudflare DNS records.

Mitigation: Review planned bootstrap, provision, verify, and retire commands before execution and test against a non-critical domain or lane first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lmtlssss/skills/caduceusmail)
- [Declared CaduceusMail homepage](https://github.com/lmtlssss/caduceusmail)
- [Declared skill adapter repository](https://github.com/lmtlssss/caduceusmail-skill)
- [Vendored release manifest](artifact/vendor/caduceusmail-release.json)
- [OpenClaw configuration example](artifact/examples/openclaw.config.json5)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapped tool may generate machine-readable state artifacts under its configured CaduceusMail state directory.]

## Skill Version(s):

3.6.7 (source: release evidence, package.json, vendored release manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
