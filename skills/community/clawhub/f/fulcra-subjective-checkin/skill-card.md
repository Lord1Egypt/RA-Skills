## Description: <br>
Runs a short conversational morning check-in that captures mood, energy, social battery, physical state, and daily intention, then saves the result to Fulcra as structured annotations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keng009](https://clawhub.ai/user/keng009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who use Fulcra can ask their agent to run a warm morning check-in, reflect on how they feel, and store the subjective record next to sleep and calendar context for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Fulcra sleep and calendar context and save intimate wellness reflections to Fulcra. <br>
Mitigation: Install only if this data access is acceptable, invoke the skill explicitly, and review dry-run payloads before saving sensitive check-ins. <br>
Risk: The save flow may persist check-in data without a separate final confirmation after the conversation. <br>
Mitigation: Ask the agent to confirm before running the save command or to use dry-run mode when testing the flow. <br>
Risk: Changing FULCRA_API_BASE or FULCRA_CLI_COMMAND can redirect Fulcra access through an untrusted endpoint or command. <br>
Mitigation: Leave those settings unset unless the target endpoint or command is fully trusted. <br>


## Reference(s): <br>
- [Subjective Check-In README](README.md) <br>
- [Fulcra read/write notes](references/fulcra-write-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational text with inline shell commands and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Fulcra annotations for the morning check-in; dry-run mode can preview payloads before saving.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
