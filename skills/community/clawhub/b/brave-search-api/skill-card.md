## Description: <br>
Brave Search API integration with managed authentication for web, image, news, and video search using a privacy-focused search engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to make Brave Search requests through Maton-managed authentication, including web, image, news, video, local, autosuggest, spellcheck, and summarizer endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, optional location headers, and connection management requests are routed through Maton using the user's API key. <br>
Mitigation: Install only if that routing is acceptable, avoid precise latitude and longitude unless needed, and treat MATON_API_KEY as a sensitive credential. <br>
Risk: Connection creation or deletion can change access to Brave Search accounts. <br>
Mitigation: Review and explicitly approve connection creation or deletion before execution, including the target connection and intended effect. <br>


## Reference(s): <br>
- [Brave Search API Documentation](https://api-dashboard.search.brave.com/documentation) <br>
- [Brave Search API Dashboard](https://api-dashboard.search.brave.com/) <br>
- [Maton Homepage](https://maton.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/brave-search-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, JavaScript, shell command, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Brave Search connection through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
