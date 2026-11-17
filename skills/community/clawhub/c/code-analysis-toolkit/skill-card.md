## Description: <br>
Code Analysis Toolkit helps agents run consent-aware Git history and code quality analysis across one or more repositories, producing retrospectives, audit reports, trend comparisons, and anonymized outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze Git history, code quality, repository trends, and team retrospectives with explicit consent controls and optional anonymized reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository history and author metadata can be sensitive, and the release has conflicting local-only and LLM/API data-flow claims. <br>
Mitigation: Confirm whether repository history may be sent to an agent or LLM provider before use, and avoid scanning repositories that contain data outside the intended analysis scope. <br>
Risk: Generated retrospectives, reports, consent logs, and baselines may expose team activity or author metadata. <br>
Mitigation: Use explicit consent controls, anonymize team reports when appropriate, and protect or delete `.code-analysis` logs and reports when they are no longer needed. <br>
Risk: The workflow asks an agent to execute Python and shell commands against local repositories. <br>
Mitigation: Verify the actual `src.main` code and run scans only in controlled workspaces with the minimum repository access needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-analysis-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Project homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON result objects, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .code-analysis logs, baselines, reports, and consent records in the analyzed workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
