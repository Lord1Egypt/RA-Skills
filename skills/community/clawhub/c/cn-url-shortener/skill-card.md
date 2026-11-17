## Description:

Generates shortened URLs from long URLs using a Python script that calls the is.gd shortening service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to turn public long URLs into shorter links for sharing. Reviewers should account for the documented feature mismatch before relying on alias, expiry, statistics, or batch behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input URLs are sent to is.gd without clear disclosure in the skill documentation.

Mitigation: Use only public URLs unless the maintainer adds clear is.gd disclosure and URL handling guidance.

Risk: The documentation advertises alias, expiry, statistics, and batch features that are not implemented by the artifact code.

Mitigation: Validate required behavior before deployment and update or remove unsupported feature claims.

Risk: The script imports requests even though the documentation claims no external dependencies.

Mitigation: Declare the dependency metadata or revise the implementation to use only the Python standard library.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-url-shortener)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [AISoBrand](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script returns a success flag with either a shortened URL or an error string.]

## Skill Version(s):

1.2.5 (source: server release evidence; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
