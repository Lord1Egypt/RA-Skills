## Description: <br>
Local CSV, TSV, and JSONL inspection and cleanup toolkit for profiling, validating, deduplicating, diffing, previewing, filtering, sorting, joining, pivoting, transforming, and converting tabular data without third-party dependencies or remote calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, data analysts, and agents use this skill to inspect, clean, validate, reshape, compare, and convert local tabular datasets before passing them into reports, CI checks, or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can read sensitive local data supplied by the user. <br>
Mitigation: Run the tools only on intended files and avoid passing credentials or sensitive datasets unless that processing is required. <br>
Risk: Commands can write or overwrite output files at user-specified paths. <br>
Mitigation: Review output paths before execution and write to a working directory or version-controlled branch when preserving originals matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples; generated data can be CSV, TSV, JSON, JSONL, or Markdown tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure Python 3 standard library tools; local file reads and writes are limited to caller-provided paths.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
