## Description: <br>
Check domain availability and brainstorm names. Checks .com/.net/.org/.io/.ai/.co/.app/.dev and more. Suggests alternatives when taken. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephflu](https://clawhub.ai/user/josephflu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and product teams use this skill through an AI assistant to check candidate domain availability across common TLDs, see alternatives when names are taken, and optionally brainstorm new domain names from a project description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain availability results are heuristic and can be unknown or stale because they rely on DNS and optional whois checks. <br>
Mitigation: Verify any candidate domain with a registrar before purchasing or making business decisions. <br>
Risk: Brainstorm mode sends the project description to OpenRouter when an API key is configured. <br>
Mitigation: Avoid confidential launch names, internal plans, or sensitive business ideas unless sharing that text with OpenRouter is acceptable. <br>


## Reference(s): <br>
- [Popular TLDs Reference](references/tlds.md) <br>
- [Domain Name Checker Homepage](https://github.com/eagerbots/domain-name-checker) <br>
- [OpenClaw](https://github.com/eagerbots/openclaw) <br>
- [ClawHub Skill Listing](https://clawhub.ai/josephflu/domain-name-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text with domain status tables and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Basic checks perform DNS lookups; brainstorm mode sends the user-provided description to OpenRouter when OPENROUTER_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
