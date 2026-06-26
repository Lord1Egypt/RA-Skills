## Description: <br>
Publish markdown articles to Dev.to via its REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apex-stack-ai](https://clawhub.ai/user/apex-stack-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and writers use this skill to have an agent prepare Dev.to publishing commands and article-formatting guidance for markdown posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to pass a Dev.to API key to a publish_devto.py script that is not included in the release. <br>
Mitigation: Inspect and trust the actual publishing script before use, protect the API key, and prefer draft mode unless public posting is intended. <br>
Risk: Using the publish flag can make an article public immediately. <br>
Mitigation: Omit the publish flag for drafts and review the title, tags, and body before publishing. <br>


## Reference(s): <br>
- [Dev.to API articles endpoint](https://dev.to/api/articles) <br>
- [Dev.to API key settings](https://dev.to/settings/extensions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and publishing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in Dev.to API calls through a user-supplied publishing script and API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
