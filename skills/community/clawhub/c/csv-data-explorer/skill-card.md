## Description: <br>
Explore, filter, summarize, and visualize CSV data directly in terminal with interactive queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and engineers use this skill to inspect CSV files, filter rows, select columns, calculate basic statistics, generate simple terminal visualizations, and export results from a command line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads user-specified CSV files that may contain private or business-sensitive data. <br>
Mitigation: Run it only on files you intend to analyze and handle previews, summaries, and generated reports according to the sensitivity of the source data. <br>
Risk: Export commands can write CSV, JSON, or PNG files to user-selected paths. <br>
Mitigation: Choose output paths carefully and avoid overwriting important files. <br>
Risk: Large CSV files may be slow or memory-intensive because processing scales with file size. <br>
Mitigation: Use smaller files or filter data before running broader statistics or visualization workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Derick001/csv-data-explorer) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local CSV, JSON, and PNG files when users run export or matplotlib histogram commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
