## Description: <br>
CSV Processor Free helps agents inspect, clean, merge, split, type-convert, and export CSV files while detecting encodings and delimiters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers, analysts, and developers use this skill to preprocess local CSV exports before downstream analysis or reporting. It is intended for explicit CSV tasks such as encoding detection, delimiter detection, cleanup, merging, splitting, type conversion, and CSV export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests local read, write, and exec authority for CSV workflows. <br>
Mitigation: Use it only for explicit CSV preprocessing tasks, review file paths before export or split operations, and confirm generated shell or Python commands before execution. <br>
Risk: The security summary notes routing toward generic analytics tasks beyond CSV processing. <br>
Mitigation: Avoid invoking the skill for general analytics, visualization, or reporting requests unless CSV preprocessing is the required task. <br>
Risk: Generated split or export operations can create or overwrite local files. <br>
Mitigation: Choose a dedicated output directory and inspect proposed filenames before allowing write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/csv-processor-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Text] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus structured JSON-style result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose reading and writing local CSV files and running Python or pip commands for CSV preprocessing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
