## Description: <br>
CueCue Deep Research helps agents run data-driven financial research on markets, industries, companies, policy impacts, competitors, geopolitical risk, sentiment, and regional opportunities through the CueCue CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xfgong](https://clawhub.ai/user/xfgong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and financial professionals use this skill to request structured financial research reports from CueCue for investment decisions, strategy planning, and market insight workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial research prompts are sent to the external CueCue service through the CLI and may contain sensitive client, business, or market information. <br>
Mitigation: Use a dedicated API key and avoid submitting confidential client data or nonpublic business information unless approved. <br>
Risk: Reports are written to user-selected output paths and may persist financial research content locally. <br>
Mitigation: Choose report output paths intentionally and review generated reports before sharing or retaining them. <br>
Risk: Long-running research can run outside close supervision when background execution is used. <br>
Mitigation: Use foreground mode when closer supervision of research progress and results is needed. <br>


## Reference(s): <br>
- [CueCue Homepage](https://cuecue.cn) <br>
- [CueCue Deep Research on ClawHub](https://clawhub.ai/xfgong/cuecue-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown research report saved to an output file, with command-line guidance for invoking the CueCue CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, the cue CLI, CUECUE_API_KEY, and explicit output and channel arguments.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
