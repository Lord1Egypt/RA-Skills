## Description: <br>
Chinese mainland calendar service that identifies statutory holidays, weekends, makeup workdays, and supported city vacation periods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manucode2000-max](https://clawhub.ai/user/manucode2000-max) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to check Chinese mainland holiday, weekend, makeup workday, and supported city school vacation status from a local Python CLI or API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Holiday results depend on the third-party chinese-calendar package and its data staying accurate for the target year. <br>
Mitigation: Pin and review the chinese-calendar dependency for managed or production use, and validate important dates against authoritative schedules. <br>
Risk: Server-resolved import provenance is unavailable for this release. <br>
Mitigation: Verify the publisher handle, release metadata, and source provenance before relying on the skill in workflows where supply-chain provenance matters. <br>
Risk: City vacation lookups depend on the regions.json data being located where the script expects it. <br>
Mitigation: Place or package the vacation data at the expected config path, or update the script path before using city vacation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manucode2000-max/china-holiday-calc) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local date lookup output; no hidden data access, persistence, or destructive behavior was reported by server security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
