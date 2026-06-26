## Description: <br>
Helps users analyze which URLs AI engines cite for a query, whether a domain is cited, how citation rates change over time, and how coverage compares with competitors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketers, SEO teams, and site owners use this skill to inspect AI citation coverage across queries, domains, engines, competitors, and historical trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The paired server may make external API calls for citation checks. <br>
Mitigation: Provide API keys only for providers the user intends to query and review provider terms before use. <br>
Risk: Citation history may rely on local cache data. <br>
Mitigation: Treat cached history as local working data and manage retention according to the user's privacy and compliance needs. <br>
Risk: A third-party npm package is required for the paired server. <br>
Mitigation: Verify trust in the AutomateLab npm package before installation or deployment. <br>


## Reference(s): <br>
- [Citation Intelligence homepage](https://github.com/AutomateLab-tech/citation-intelligence) <br>
- [Citation Intelligence configuration](https://github.com/AutomateLab-tech/citation-intelligence#configuration) <br>
- [ClawHub release page](https://clawhub.ai/automatelab/automatelab-citation-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include citation matrices, per-engine breakdowns, snippets, trend summaries, competitor comparisons, setup guidance, and configuration examples.] <br>

## Skill Version(s): <br>
0.10.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
