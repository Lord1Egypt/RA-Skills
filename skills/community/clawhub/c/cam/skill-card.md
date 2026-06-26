## Description: <br>
Use when calculating CNC speeds and feeds, selecting cutting tools, referencing G-code commands, looking up material cutting data, or computing machining parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, manufacturing engineers, CNC programmers, and machinists use this skill for quick reference calculations, material cutting guidance, toolpath strategy lookup, and G-code command reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local script execution may be inappropriate in restricted environments. <br>
Mitigation: Install only where running a local bash script that invokes python3 is acceptable, and review the artifact before use. <br>
Risk: Unverified CNC parameters or sample G-code can damage equipment, tooling, material, or create safety hazards. <br>
Mitigation: Verify units, offsets, tooling, workholding, material, coolant, machine limits, controller dialect, and manufacturer recommendations before machining; use simulation, dry-run, or single-block checks. <br>


## Reference(s): <br>
- [Cam Skill Page](https://clawhub.ai/xueyetianya/cam) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-style terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs CNC reference data, calculated RPM and feed values, toolpath guidance, material recommendations, and G-code examples.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
