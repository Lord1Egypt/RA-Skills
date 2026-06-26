## Description: <br>
Cross-agent context sharing via shared files so agents can write trends, highlights, and signals that other agents read before acting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gum97](https://clawhub.ai/user/Gum97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators running multi-agent OpenClaw setups use this skill to share local trends and highlights between agents through JSON files. It is useful for coordination across agents on the same machine, but not for real-time chat or direct agent-to-agent messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared context may influence posting, engagement, moderation, or business-impacting decisions without enough review. <br>
Mitigation: Validate shared context or require human review before using it for public, moderation, or business-impacting actions. <br>
Risk: Local shared files may expose secrets or private data if untrusted agents can write to them. <br>
Mitigation: Limit write access to trusted agents and avoid storing secrets or private data in shared context files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gum97/agent-shared-context) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local shared JSON files for trends and highlights; no network access, credential use, or hidden behavior is reported by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
