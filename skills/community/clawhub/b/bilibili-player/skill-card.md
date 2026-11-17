## Description:

Searches Bilibili with Playwright, selects a matching video link, and opens it in the user's current macOS browser for playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e421083458](https://clawhub.ai/user/e421083458)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to search for requested Bilibili videos, music, tutorials, documentaries, movies, or TV content and open the selected result in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens Bilibili search results in the default browser and may use an existing Bilibili login session.

Mitigation: Install only when that browser-opening behavior is acceptable, and review the target URL before relying on an authenticated session.

Risk: The skill depends on Playwright, browser automation, macOS open behavior, and network access.

Mitigation: Install Playwright in an isolated environment with pinned versions when reproducibility matters, and run the skill only on supported macOS systems.

Risk: The security guidance recommends stronger URL validation for opened links.

Mitigation: Harden validation so only HTTPS bilibili.com or approved Bilibili subdomains are opened.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser-opening actions through local scripts; no structured file output is described.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
