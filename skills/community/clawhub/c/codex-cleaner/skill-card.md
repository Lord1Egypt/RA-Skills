## Description: <br>
Monitor and clean invalid Codex auth files from CPA (Codex Provider Agent) by checking quota status, disabling 401 files, and double-verifying before deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geekjair](https://clawhub.ai/user/geekjair) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Codex authentication records in CPA by checking status, disabling records that return 401 responses, and deleting disabled records only after repeated verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CPA administrative access can disable or delete authentication records. <br>
Mitigation: Install and run the skill only in environments where the operator intends to grant CPA administrative access. <br>
Risk: config.json may contain a CPA admin key. <br>
Mitigation: Protect config.json and prefer controlled storage for CPA_URL and CPA_KEY values. <br>
Risk: Cleanup commands can disable or remove auth records after quota checks. <br>
Mitigation: Run status before check, delete, or clean, and rely on the documented double-verification flow before deletion. <br>
Risk: Monitor mode can repeatedly clean auth files without manual review each cycle. <br>
Mitigation: Use monitor mode only when repeated automated cleanup is acceptable for the CPA instance. <br>


## Reference(s): <br>
- [Codex Auth Cleaner on ClawHub](https://clawhub.ai/geekjair/codex-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash command examples; runtime commands may emit JSON or human-readable reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform CPA management API calls when run with a configured CPA URL and admin key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
