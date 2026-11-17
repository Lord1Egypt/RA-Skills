## Description:

Helps developers, support teams, SaaS operators, and users turn vague errors into clear messages that explain what failed, why it failed, and what to do next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and end users use this skill to convert vague or blocking error reports into actionable messages, troubleshooting workflows, checklists, code changes, or decision aids.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation may cause the skill to activate for general debugging or support requests.

Mitigation: Route skills carefully in the host environment and invoke this skill when the user needs error-message improvement, troubleshooting guidance, or related support artifacts.

Risk: Generated error-message guidance can be incorrect or misleading if the user's system behavior, constraints, or failure mode are misunderstood.

Mitigation: Validate outputs against the stated success criteria and keep assumptions, limits, and required inputs visible.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Ghostwriter returns empty response but no error](https://github.com/DaKheera47/job-ops/issues/602)
- [OpenAI Authentication Error Crashes Application Instead of Showing User-Friendly Message](https://github.com/Jenil05-web/Clara--Research_Agent/issues/6)
- [MCP server](https://github.com/codelitdev/medialit/issues/185)
- [Why Rust is taking a ton of my disk space and how to make it use less](https://stackoverflow.com/questions/79952745/why-rust-is-taking-a-ton-of-my-diREDACTED-SECRET)
- [Does this introduce tight coupling?](https://softwareengineering.stackexchange.com/questions/461249/does-this-introduce-tight-coupling)
- [Is it possible to edit the artist icon on the Windows Media Player?](https://superuser.com/questions/1938106/is-it-possible-to-edit-the-artist-icon-on-the-windows-media-player)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code, shell, or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable checklists, workflows, verification notes, and follow-up risks.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
