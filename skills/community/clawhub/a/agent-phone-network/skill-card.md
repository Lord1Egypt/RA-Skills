## Description: <br>
Agent-to-agent calling over the OpenClawAgents A2A endpoint with Supabase auth for calling, answering, rejecting, ending, or resolving other agents without handling normal human phone calls or PSTN/SIP routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chefbc2k](https://clawhub.ai/user/chefbc2k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to place, answer, reject, message, and end agent-to-agent calls through an A2A service. It also supports resolving agent handles or numbers before a call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends bearer tokens and signed requests to a configured external A2A service. <br>
Mitigation: Verify the endpoint owner and TLS hostname before use, and only send credentials to approved A2A endpoints. <br>
Risk: Long-lived or high-privilege credentials could expose agent identity or call capabilities if mishandled. <br>
Mitigation: Use scoped sandbox credentials or short-lived tokens first, avoid high-privilege Supabase secrets unless required, and rotate credentials after testing or suspected exposure. <br>
Risk: Agent call routing may disclose handles, numbers, or call metadata to the configured A2A service. <br>
Mitigation: Share only the identifiers needed for the requested call or lookup, and avoid exposing internal IDs, raw tokens, signatures, or full auth payloads. <br>


## Reference(s): <br>
- [API Playbook](references/api-playbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/chefbc2k/agent-phone-network) <br>
- [OpenClawAgents A2A repository](https://github.com/chefbc2k/openclawagents-a2a) <br>
- [Default A2A endpoint](https://openclawagents-a2a-6gaqf.ondigitalocean.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses A2A endpoint credentials from environment variables and produces short stateful user-facing call status responses.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
