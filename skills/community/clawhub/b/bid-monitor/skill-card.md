## Description:

Multi-platform bidding monitor: scan 50+ sites and filter power/electric bidding notices only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powerzzjohn](https://clawhub.ai/user/powerzzjohn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and procurement operators use this skill to scan Chinese bidding and procurement platforms for power and electric industry notices. It supports daily category rotation, targeted category scans, and local summaries for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be stored in plaintext if users add accounts and passwords to references/gx_websites.json.

Mitigation: Use a separate secret manager or runtime-only credentials, protect the configuration file, and keep it out of source control and shared archives.

Risk: The browser-based scanner visits many procurement sites and writes daily results locally.

Mitigation: Run it only in an environment where those network visits and local output files are acceptable, and review the configured site list before scanning.

Risk: The --auth-only mode can print account identifiers in terminal output.

Mitigation: Avoid running --auth-only in logged or shared terminals when account identifiers are sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/powerzzjohn/skills/bid-monitor)
- [Configuration Guide](references/config-guide.md)
- [GX Websites Configuration](references/gx_websites.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text, JSON result files, and optional text notification drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily bidding_results_YYYYMMDD.json and optional wechat_msg_YYYYMMDD.txt under the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
