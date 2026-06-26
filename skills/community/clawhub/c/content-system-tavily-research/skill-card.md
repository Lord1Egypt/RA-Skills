## Description: <br>
Conducts AI-powered deep research with the Tavily CLI and returns structured, cited reports for comparisons, market analysis, literature reviews, and topic investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a quick search is insufficient and they need multi-source synthesis with citations, such as comparison reports, market scans, literature reviews, and topic investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to pipe a remote installer script into a shell and start a login flow before use. <br>
Mitigation: Install Tavily CLI only from trusted channels, inspect the installer or use a verified package, and confirm credential storage before running tvly login. <br>
Risk: Research reports grounded in web sources can still contain incomplete, outdated, or misleading synthesis. <br>
Mitigation: Review cited sources and source quality before relying on the report for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abigale-cyber/content-system-tavily-research) <br>
- [Tavily CLI installer](https://cli.tavily.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Tavily CLI output as plain text, Markdown reports, or JSON; optional saved files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stream progress, run asynchronously by request ID, or save output with -o.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
