## Description: <br>
Scans A-share market data and documents a workflow for ranking next-day short-term trading candidates using multi-factor signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernelh](https://clawhub.ai/user/kernelh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading workflow builders use this skill to scan China A-share market data, configure signal thresholds, and prepare candidate lists for short-term review. Outputs should be treated as decision support rather than validated financial advice. <br>

### Deployment Geography for Use: <br>
Global; intended market coverage is China A-shares. <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises prediction, reporting, and notification features that are not fully implemented in the submitted artifact. <br>
Mitigation: Review available files and verify commands before deployment; treat the artifact as a scanner-oriented skeleton unless additional implementation is supplied. <br>
Risk: The workflow depends on optional market-data credentials and third-party data packages. <br>
Mitigation: Install dependencies in a virtual environment, review any market-data token before use, and restrict credentials to the minimum needed scope. <br>
Risk: Trading signals can be inaccurate or financially harmful if treated as validated predictions. <br>
Mitigation: Use outputs only as review inputs and require human validation, backtesting, and risk controls before any trading decision. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kernelh/alpha-pulse-1-0-0) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact configuration](artifact/config.yaml) <br>
- [Artifact market scanner](artifact/lib/scanner.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and YAML snippets plus command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe reports, CSVs, charts, and notifications, but the submitted artifact only includes a scanner skeleton and configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
