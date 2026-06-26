## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mifashion](https://clawhub.ai/user/mifashion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to drive browser workflows through deterministic snapshots, ref-based interaction commands, isolated sessions, and state persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents powerful access to logged-in browser sessions and workflows that submit or change data. <br>
Mitigation: Use it only on sites and accounts where automation is authorized, and supervise actions that submit, modify, or expose data. <br>
Risk: Saved state files, cookies, storage values, screenshots, PDFs, and network captures may contain credentials or private data. <br>
Mitigation: Treat generated browser artifacts as sensitive, restrict access to them, and delete or rotate them when they are no longer needed. <br>
Risk: The release relies on an unpinned external CLI with unclear server-resolved provenance metadata. <br>
Mitigation: Confirm the intended agent-browser package and upstream source before installation, and pin a trusted version when deploying. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mifashion/agent-dyxc) <br>
- [Publisher profile](https://clawhub.ai/user/mifashion) <br>
- [ClawHub metadata homepage](https://www.sztv.com.cn/ysz/zx/zw/80706997.shtml) <br>
- [Referenced agent-browser CLI](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON output examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser state files, screenshots, PDFs, cookies, storage values, and network captures through the referenced CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
