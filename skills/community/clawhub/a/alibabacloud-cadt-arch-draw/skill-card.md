## Description: <br>
Draw cloud architecture diagrams via CADT AI agent from a product or resource description and return a Markdown summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud architects use this skill to request Alibaba Cloud CADT architecture diagrams through the Aliyun CLI, iterate on existing CADT sessions, and relay the backend-generated Markdown summary to users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer guidance includes a curl-to-bash Aliyun CLI setup path and automatic plugin installation. <br>
Mitigation: Prefer a package-manager install or checksum/signature-verified CLI package, and disable automatic plugin installation unless it is required. <br>
Risk: The permissions reference recommends PowerUserAccess as the pragmatic default for architecture drawing. <br>
Mitigation: Use the listed per-product read-only RAM policies whenever possible for a lower-privilege drawing workflow. <br>
Risk: The CADT backend may return clarifying questions for invalid products, regions, or incomplete architecture requests instead of a completed diagram. <br>
Mitigation: Relay backend responses faithfully, reuse the same sessionId for follow-ups, and do not fabricate a successful architecture result. <br>


## Reference(s): <br>
- [RAM Policies](references/ram-policies.md) <br>
- [CLI Command Reference](references/related-commands.md) <br>
- [CADT Console](https://bpstudio.console.aliyun.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with inline Aliyun CLI commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Relays backend-generated CADT architecture content; does not create local diagram files.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
