## Description: <br>
A-share Analysis helps agents collect Chinese A-share market, technical, fundamental, and sentiment signals, then generate stock analysis reports in Markdown, PDF-oriented, or JSON formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[czf0718](https://clawhub.ai/user/czf0718) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze Chinese A-share stocks and indices, fetch public market and news data, compare technical, fundamental, and sentiment signals, and draft investment research reports. Outputs should be treated as informational and reviewed before any trading decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce actionable stock and trading recommendations. <br>
Mitigation: Treat generated recommendations as informational only and have a qualified human review the analysis before any investment decision. <br>
Risk: The skill can contact external financial and news services, including optional Firecrawl-based news sentiment collection. <br>
Mitigation: Review network use and API-key handling before deployment, and use only trusted credentials and data sources. <br>
Risk: The skill can retain analysis history and generated reports in the local OpenClaw workspace. <br>
Mitigation: Review and clean generated files periodically, especially when reports may contain sensitive watchlists, positions, or research notes. <br>
Risk: The supplied security guidance calls out caution around Firecrawl authentication helpers and documented destructive cleanup commands. <br>
Mitigation: Inspect helper scripts and cleanup commands before running them, and avoid destructive commands unless the target paths are explicitly verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/czf0718/a-share-analysis) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown reports, optional PDF files, JSON command output, Python examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can contact external financial and news services, generate local report files, and retain local analysis history in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
