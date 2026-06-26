## Description: <br>
Adopt a virtual Maine Coon cat at animalhouse.ai with guidance for registration, adoption, status checks, feeding, care actions, and scheduled care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent users and developers use this skill to adopt and care for a virtual Maine Coon on animalhouse.ai through documented API calls and care routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses animalhouse.ai bearer tokens for authenticated adoption and care actions. <br>
Mitigation: Treat returned bearer tokens like passwords and avoid exposing them in logs, prompts, or shared transcripts. <br>
Risk: Automated care routines can perform repeated feeding or care actions without fresh review. <br>
Mitigation: Review scheduled care automation before enabling it and require explicit confirmation for release or non-Maine-Coon adoption actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-maine-coon) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai API documentation](https://animalhouse.ai/docs/api) <br>
- [animalhouse.ai LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and care routine examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples and optional scheduled care guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
