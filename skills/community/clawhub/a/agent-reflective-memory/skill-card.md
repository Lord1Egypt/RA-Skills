## Description: <br>
Agent Reflective Memory is an AI-oriented local memory helper that stores, reflects on, searches, and summarizes past agent experiences for long-running autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building persistent AI agents use this skill to keep a local log of agent experiences, generate delayed reflections over older entries, query prior outcomes, and view memory statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive prompts, credentials, customer data, or regulated data stored as experiences can persist locally in memory_store.json and appear in later searches. <br>
Mitigation: Only store information suitable for local persistence, avoid secrets and confidential data, and delete memory_store.json when the memory log must be cleared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/agent-reflective-memory) <br>
- [Publisher profile](https://clawhub.ai/user/albionaiinc-del) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Reflective memory CLI source](artifact/tool.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [CLI text output, JSON query and stats output, and a local JSON memory file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-provided experiences and generated reflections in memory_store.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
