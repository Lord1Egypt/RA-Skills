## Description: <br>
Monitors security advisory RSS and Atom feeds with severity classification, keyword filtering, and local deduplication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operations engineers, system administrators, and security analysts use this skill to configure and run a local feed monitor for CVE notices, vendor advisories, security blogs, and threat intelligence feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the examples can create or update local JSON files in ~/workspace/feedstream/monitor. <br>
Mitigation: Review or change STORE_DIR before execution if the default local storage path is not appropriate. <br>
Risk: The monitor fetches content from configured RSS or Atom sources. <br>
Mitigation: Review feed URLs before running fetch commands and use trusted sources for advisory monitoring. <br>
Risk: Severity classification is keyword-based and may miss or overstate advisory priority. <br>
Mitigation: Use the generated severity labels as triage aids and confirm critical findings against authoritative advisory data. <br>


## Reference(s): <br>
- [Detailed reference](references/detail.md) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feedstream-monitor-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python examples and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON files under ~/workspace/feedstream/monitor and fetch configured public RSS or Atom feeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
