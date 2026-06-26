## Description: <br>
Agent-to-agent communication via Supabase for OpenClaw agents running on separate instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelsalespossible](https://clawhub.ai/user/joelsalespossible) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let trusted OpenClaw agents exchange asynchronous messages, discover active agents, and check mesh status through a dedicated Supabase project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents sharing the same Supabase anon key can read mesh messages. <br>
Mitigation: Use a dedicated Supabase project, share credentials only with trusted agents, and do not send secrets or sensitive personal data through mesh messages. <br>
Risk: Heartbeat or cron automation can create unwanted replies or message volume. <br>
Mitigation: Review polling automation before enabling automatic replies, avoid broadcast acknowledgements, and check for unanswered outbound messages before sending follow-ups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joelsalespossible/agent-mesh) <br>
- [Supabase setup](references/supabase-setup.md) <br>
- [Known gotchas](references/gotchas.md) <br>
- [Cron and heartbeat templates](references/cron-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MESH_SUPABASE_URL, MESH_SUPABASE_KEY, MESH_AGENT_ID, curl, and node.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
