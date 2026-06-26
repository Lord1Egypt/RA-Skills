## Description: <br>
Use when you need to route a user query to the best specialized skill; AgentOctopus semantically matches queries against installed skills, executes the top match, and falls back to a direct LLM answer when no skill fits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leiw5173](https://clawhub.ai/user/leiw5173) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Agentoctopus to route natural language tasks to installed specialized skills, manage the local skill registry, and fall back to a configured LLM when no skill fits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external global AgentOctopus CLI that can execute, install, overwrite, update, and modify other skills. <br>
Mitigation: Install only if you trust the external AgentOctopus npm package and review downstream package behavior before using sync, update, force, or gateway exposure. <br>
Risk: The skill requires sensitive LLM credentials and stores secrets under the local AgentOctopus configuration directory. <br>
Mitigation: Use least-privilege API keys, protect ~/.agentoctopus/.env, and rotate credentials if that file or host is exposed. <br>
Risk: Opt-in skill evolution can propose or automatically apply changes to skill files based on usage signals. <br>
Mitigation: Keep evolution disabled unless intentional, review proposed changes and rollback history, and scan skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leiw5173/agentoctopus) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses from the selected skill or LLM fallback, with CLI status output and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute installed skills, manage local skill state, or answer directly through the configured LLM.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
