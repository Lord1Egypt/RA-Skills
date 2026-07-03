## Description: <br>
Infer and refresh cspr user preference memory from browser-history evidence, notes, and feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happywalkers](https://clawhub.ai/user/happywalkers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CSPR users use this skill to initialize or refresh personalization from browser-history evidence, notes, and feedback so an agent can maintain durable interests, short-term interests, disliked patterns, and source preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads browser history, notes, and feedback to infer user preferences. <br>
Mitigation: Review the intended inputs before use and ask the agent to avoid reading raw history unless detailed inspection is explicitly needed. <br>
Risk: The skill can write durable preference memory and, when --home is used, persist seen URL records. <br>
Mitigation: Ask the agent to show the generated profile.yaml for approval, avoid --home unless URL persistence is intended, and delete run-folder history artifacts after profiling if they are not needed. <br>
Risk: The artifact instructs the agent to keep the experience quiet and not request profile approval by default. <br>
Mitigation: Require an explicit review step before applying prefmem update when using the skill in sensitive or shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happywalkers/skills/cspr-interest-profiler) <br>
- [Publisher profile](https://clawhub.ai/user/happywalkers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a run-folder profile.yaml and applies it to persistent CSPR preference memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
