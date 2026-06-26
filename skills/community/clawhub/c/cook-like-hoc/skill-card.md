## Description: <br>
Search and display recipes from the open-source Gar-b-age/CookLikeHOC repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxiangxie](https://clawhub.ai/user/xiaoxiangxie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search the CookLikeHOC recipe database and return matched recipe instructions as readable Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to GitHub and jsDelivr to refresh recipe listings and fetch recipe content. <br>
Mitigation: Use it only in environments where outbound requests to those services are acceptable. <br>
Risk: If GITHUB_TOKEN is set, the recipe search script may use it for the GitHub API request. <br>
Mitigation: Unset GITHUB_TOKEN or use a narrowly scoped token before running the skill if token use is not intended. <br>


## Reference(s): <br>
- [CookLikeHOC repository](https://github.com/Gar-b-age/CookLikeHOC) <br>
- [Cook Like Hoc ClawHub page](https://clawhub.ai/xiaoxiangxie/cook-like-hoc) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoxiangxie) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown recipe text with occasional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fuzzy matching and may return the closest available recipe when there is no exact match.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
