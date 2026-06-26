## Description: <br>
Search and analyze trending GitHub repositories by topics, star count, and creation date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical researchers use this skill to discover popular open-source GitHub projects by topic, stars, creation window, programming language, and sort order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An optional GITHUB_TOKEN may be exposed if stored in shell startup files or granted broad permissions. <br>
Mitigation: Treat the token as a secret, grant only the minimum permissions needed, avoid private-repository or write scopes, and prefer a temporary environment variable or secret manager. <br>
Risk: GitHub API rate limits can interrupt searches or reduce result availability. <br>
Mitigation: Use a minimally scoped token for higher API limits when appropriate, and rerun searches after loosening filters if no results are returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manifoldor/explorer) <br>
- [GitHub Search API reference](references/github_api.md) <br>
- [GitHub REST Search documentation](https://docs.github.com/en/rest/search) <br>
- [GitHub Search Repositories endpoint](https://api.github.com/search/repositories) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text listing matching repositories with names, descriptions, URLs, stars, forks, language, tags, and dates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use an optional GITHUB_TOKEN environment variable to raise GitHub API rate limits.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
