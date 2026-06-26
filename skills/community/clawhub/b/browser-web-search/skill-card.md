## Description: <br>
Browser Web Search gives agents a unified CLI for searching 55 web platforms and returning structured JSON through OpenClaw browser sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to query search, news, social, developer, media, finance, and reference sites through one command interface and consume JSON results. Authenticated adapters should be used only when browser-session access is deliberately authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let a third-party package operate inside logged-in browser sessions. <br>
Mitigation: Keep BWS_PUBLIC_ONLY=1 unless authenticated access is required; use a dedicated OpenClaw browser profile and close unrelated tabs before sensitive calls. <br>
Risk: Sensitive adapters can access account-protected page content through inherited site sessions. <br>
Mitigation: Enable sensitive access only with BWS_ENABLE_SENSITIVE_TIER=1 plus per-call opt-in and per-site consent; run --dry-run first. <br>
Risk: A changed or unaudited browser-web-search package could alter runtime behavior. <br>
Mitigation: Use the pinned browser-web-search@0.4.3 package, verify integrity, install with --ignore-scripts, and re-audit before any package version bump. <br>
Risk: Unexpected sensitive calls may be hard to detect after the fact. <br>
Mitigation: Review ~/.bws/audit.log and ~/.bws/consents.json periodically; sensitive calls emit a transparency block before import. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sipingme/browser-web-search) <br>
- [Browser Web Search Skill Repository](https://github.com/sipingme/browser-web-search-skill) <br>
- [browser-web-search Package Repository](https://github.com/sipingme/browser-web-search) <br>
- [browser-web-search npm Package](https://www.npmjs.com/package/browser-web-search) <br>
- [Pinned Source Audit Reference](https://github.com/sipingme/browser-web-search/blob/v0.4.3/src/index.ts) <br>
- [Artifact Security Model](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON from bws commands, with optional jq-filtered text and stderr transparency records for sensitive calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write metadata-only audit records and consent state under ~/.bws/; sensitive calls require explicit gates and per-site consent.] <br>

## Skill Version(s): <br>
0.4.11 (source: server release evidence; artifact frontmatter reports 0.4.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
