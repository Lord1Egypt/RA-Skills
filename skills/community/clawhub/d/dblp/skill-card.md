## Description: <br>
Dblp provides MCP-based access to DBLP literature search, citation generation, and BibTeX formatting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to search DBLP publications, retrieve author and venue information, calculate publication statistics, and collect or export BibTeX entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends API keys and literature queries to the third-party Xiaobenyang MCP service. <br>
Mitigation: Install only where that service is trusted for the intended data, and avoid submitting sensitive literature queries unless approved. <br>
Risk: The artifact can store XBY_APIKEY in a local .env file. <br>
Mitigation: Prefer providing XBY_APIKEY through an environment variable or managed secret store instead of persisting it in the workspace. <br>
Risk: Some artifact wording references stale Gaokao/search_schools behavior that does not match the DBLP release purpose. <br>
Mitigation: Review the tool descriptions and generated outputs before relying on results in production workflows. <br>


## Reference(s): <br>
- [ClawHub Dblp skill page](https://clawhub.ai/cainingnk/dblp) <br>
- [Xiaobenyang API key and service site](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, BibTeX files, configuration guidance] <br>
**Output Format:** [Markdown summaries with structured tool results and optional .bib file exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Xiaobenyang API key; search results depend on the third-party MCP service and DBLP data returned by that service.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
