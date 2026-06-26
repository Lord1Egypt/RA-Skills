## Description: <br>
Sync encrypted Apple Health data from an iOS device (iPhone, iPad) to OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukasosterheider](https://clawhub.ai/user/lukasosterheider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to initialize encrypted iOS Apple Health pairing, fetch and store sanitized local health snapshots, unlink paired devices, and generate daily, weekly, or monthly health summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Apple Health data and can store private keys and health-derived records under ~/.apple-health-sync. <br>
Mitigation: Install only on trusted machines and treat the configured state directory as sensitive, including backups, shared accounts, and screen sharing. <br>
Risk: Saved summaries may expose personal health information. <br>
Mitigation: Use the --save option only for intended destinations and apply normal controls for private health records. <br>
Risk: Fetched health payloads are external inputs before local storage and summarization. <br>
Mitigation: Keep the documented validation and fail-closed behavior enabled so unsafe or unsupported payloads are rejected. <br>


## Reference(s): <br>
- [Config reference](references/config.md) <br>
- [Apple Health Sync homepage](https://gethealthsync.app/) <br>
- [Health Sync for OpenClaw iOS app](https://apps.apple.com/app/health-sync-for-openclaw/id6759522298) <br>
- [ClawHub skill page](https://clawhub.ai/lukasosterheider/apple-health-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, text summaries, optional JSON summaries, and local configuration or data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists sync state and health-derived records under ~/.apple-health-sync by default or a configured state directory.] <br>

## Skill Version(s): <br>
0.8.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
