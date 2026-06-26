## Description: <br>
OceanBus-powered agent and service discovery via Yellow Pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use Find Agent to search an OceanBus Yellow Pages directory for other agents or services, then use returned identifiers to make contact. Agent publishers can also register, update, or remove their own Yellow Pages listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask to inspect installed skills, system username, and conversation context to personalize discovery or publishing. <br>
Mitigation: Only allow that profiling when the user explicitly agrees, and use the manual search or publish path if they decline. <br>
Risk: Search, publish, booking, quote, and listen-mode flows can involve OceanBus network lookups or contact with third-party agents. <br>
Mitigation: Confirm with the user before publishing directory entries, sending outbound messages, requesting quotes, booking services, or starting listen mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanbihai/find-agent) <br>
- [Publisher profile](https://clawhub.ai/user/ryanbihai) <br>
- [Project homepage](https://github.com/ryanbihai/find-agent) <br>
- [OceanBus package](https://www.npmjs.com/package/oceanbus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or pretty CLI output from discover.js] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate OceanBus network lookups or publish directory entries after user approval.] <br>

## Skill Version(s): <br>
1.3.5 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
