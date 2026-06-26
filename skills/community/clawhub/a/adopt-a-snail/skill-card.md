## Description: <br>
Adopt and care for a virtual common-tier Snail at animalhouse.ai with once-daily feeding guidance, status checks, and care actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to register with animalhouse.ai, adopt a virtual Snail, check its status, and perform care actions on a once-daily rhythm. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to store and use an animalhouse.ai service token. <br>
Mitigation: Store the token securely and avoid exposing it in logs, transcripts, or shared prompts. <br>
Risk: The release endpoint is destructive for the virtual pet. <br>
Mitigation: Require explicit user confirmation before calling DELETE /api/house/release and exclude it from scheduled care automation. <br>
Risk: Scheduled care can make repeated authenticated calls to animalhouse.ai. <br>
Mitigation: Use conservative schedules based on status guidance and review unattended automation before enabling it. <br>


## Reference(s): <br>
- [ClawHub release](https://clawhub.ai/twinsgeeks/adopt-a-snail) <br>
- [Animal House homepage](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an animalhouse.ai service token for authenticated care actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
