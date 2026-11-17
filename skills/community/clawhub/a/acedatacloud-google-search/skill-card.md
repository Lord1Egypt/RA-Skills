## Description:

Searches Google web, image, news, map, place, and video results through AceDataCloud's SERP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to find web pages, images, news, places, maps, and videos with localized, time-filtered, or paginated Google searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed API key can allow unauthorized use of the search service.

Mitigation: Use a scoped key and keep it out of prompts and commits.

Risk: Resubmitting a pending search can incur duplicate charges.

Mitigation: Check the existing task ID until it completes instead of submitting the request again.

Risk: The optional mcp-serp package is a separate dependency.

Mitigation: Review that package separately before installing it.

## Reference(s):

- [ClawHub Google Search skill](https://clawhub.ai/acedatacloud/skills/google-search)
- [AceDataCloud applications and API keys](https://platform.acedata.cloud/console/applications)
- [First run and troubleshooting](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requests can return structured titles, snippets, URLs, and other result details.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
