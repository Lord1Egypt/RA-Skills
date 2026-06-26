## Description: <br>
LLM-friendly keyword research CLI for AI agents. Check search volume, CPC, keyword difficulty, and competition via DataForSEO API. Find related keywords, analyze competitor rankings. Outputs TSV by default (optimized for agent context windows). Use when doing SEO research, content planning, or competitive keyword analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexgusevski](https://clawhub.ai/user/alexgusevski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, marketers, and agents use this skill to run DataForSEO keyword research from the command line for SEO research, content planning, and competitive keyword analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DataForSEO credentials are required for API-backed commands and may be exposed through shell history, logs, or shared workspaces if entered directly in commands. <br>
Mitigation: Use dedicated DataForSEO credentials where possible, avoid placing real secrets in commands that may be logged, and review the stored configuration file before sharing the environment. <br>
Risk: Keyword research commands can incur DataForSEO API costs. <br>
Mitigation: Batch volume checks as documented, monitor API usage, and use cache hits when repeated queries are expected. <br>
Risk: Cached keyword research in the local DataForSEO CLI cache may reveal sensitive SEO plans or competitive research. <br>
Mitigation: Clear the local cache when research is sensitive or before handing the workspace to another user. <br>
Risk: Installing a global npm package introduces dependency and package-source risk. <br>
Mitigation: Verify the npm package and linked repository before installation, and use a controlled environment for security-sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexgusevski/dataforseo-cli) <br>
- [Publisher profile](https://clawhub.ai/user/alexgusevski) <br>
- [npm package](https://www.npmjs.com/package/dataforseo-cli) <br>
- [dataforseo-cli GitHub repository](https://github.com/alexgusevski/dataforseo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI results are TSV by default, with optional JSON arrays or human-readable tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keyword metrics can include search volume, CPC, keyword difficulty, competition, ranking URLs, and monthly trends; command options control location, language, result limits, and output format.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence; artifact frontmatter reports 1.0.6 with no file changes detected between 1.0.6 and 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
