## Description: <br>
Log, query, import, and chart private local baby-care records, including diapers, feeds, sleep, growth, temperature, medication, illness notes, and CSV exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martinzokov](https://clawhub.ai/user/martinzokov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers and agents use this skill to keep a private local baby-care log, import Huckleberry CSV exports, query recent events, and generate growth or care charts from CSV data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive baby-care, routine, and possible health data in local files. <br>
Mitigation: Protect the data directory, avoid unnecessary raw notes or source text when privacy matters, and periodically review or delete generated records and charts. <br>
Risk: Large imports can add many care records from an external CSV export. <br>
Mitigation: Use the documented dry-run import mode before unusual or large Huckleberry imports. <br>


## Reference(s): <br>
- [Baby Tracker ClawHub listing](https://clawhub.ai/martinzokov/baby-tracker) <br>
- [Schema Reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands and generated CSV, JSON, HTML, or PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CSV and JSON storage, supports idempotent CSV imports, and can generate chart files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
