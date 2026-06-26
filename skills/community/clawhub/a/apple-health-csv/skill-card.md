## Description: <br>
Query Apple Health data exported as CSV files from iOS apps like Simple Health Export or Health Auto Export, covering common health, fitness, sleep, vital, and body metrics locally without cloud services, API keys, or third-party data sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to inspect locally exported Apple Health CSV files, list available health metrics, query recent metric history, and produce daily summaries. It is suited for personal health, fitness trend, and sleep pattern review when the user has intentionally placed exports in the configured data directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apple Health CSV exports can contain private medical, wellness, and fitness information. <br>
Mitigation: Keep the configured data directory scoped to exports the user wants analyzed, and review generated summaries before sharing them. <br>
Risk: The skill can read any Apple Health CSV files placed in its configured data directory. <br>
Mitigation: Place only intended exports in the directory or set HEALTH_DATA_DIR to a narrowly scoped folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/apple-health-csv) <br>
- [Publisher profile](https://clawhub.ai/user/lanyasheng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON query results, with agent-facing guidance typically rendered as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the CSV files available in the configured local health data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
