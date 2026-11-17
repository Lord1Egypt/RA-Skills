## Description:

Open pages with the real CN or global browser profile on spark and return the live page title plus final URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a task explicitly requires opening a site in a live browser profile and returning the browser-reported page title and final URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can open arbitrary URLs in persistent browser profiles.

Mitigation: Install only in trusted agent environments and prefer isolated or temporary browser profiles for untrusted tasks.

Risk: Browser access can reach local, private, internal, or non-http(s) destinations if not constrained.

Mitigation: Add URL validation and block local, private, internal, and non-http(s) destinations unless explicitly required.

Risk: Fallback page selection can expose metadata from unrelated browser tabs.

Mitigation: Remove the unrelated-tab fallback before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackdark425/skills/aigroup-browser-skill)
- [Project homepage](https://github.com/jackdark425/aigroup-browser-skill)
- [README](README.md)
- [SKILL definition](SKILL.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON object with page status, selected mode, browser port, live page title, and final URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and existing oc-cn, oc-global, and oc-browser commands on the target host.]

## Skill Version(s):

0.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
