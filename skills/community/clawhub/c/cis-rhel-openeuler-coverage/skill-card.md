## Description: <br>
Analyzes CIS Red Hat Enterprise Linux Benchmark rules against an OpenEuler security baseline and reports whether each rule is fully covered, partially covered, or not covered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x008](https://clawhub.ai/user/0x008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and compliance reviewers use this skill to compare a CIS RHEL Benchmark PDF with an OpenEuler security baseline Markdown file and produce rule-level coverage reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports are written to local output paths and may overwrite or clutter an existing working directory. <br>
Mitigation: Run the skill with a dedicated report directory and review the output path before executing report-generation commands. <br>
Risk: Fuzzy matches and automatically classified partial coverage can be misleading if used as final compliance evidence without review. <br>
Mitigation: Manually review fuzzy matches, partial coverage entries, and any remarks marked for confirmation before relying on the report. <br>
Risk: Incorrect input paths can cause the analysis to parse unintended PDF or Markdown files. <br>
Mitigation: Provide only the intended CIS Benchmark PDF and OpenEuler baseline Markdown paths for each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x008/cis-rhel-openeuler-coverage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated JSON, CSV, and text report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bilingual Chinese and English CSV coverage reports plus local JSON analysis artifacts and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
