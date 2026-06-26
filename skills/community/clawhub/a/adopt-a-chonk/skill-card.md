## Description: <br>
Adopt a virtual Chonk AI-native pet at animalhouse.ai, with guidance for registration, adoption, status checks, feeding, care actions, and evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to adopt and care for a virtual Chonk pet through animalhouse.ai API calls, including registration, adoption, status checks, feeding, and scheduled care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai bearer token for protected adoption and care API calls. <br>
Mitigation: Store the token in a secret store, avoid printing it in logs, and do not commit it to files. <br>
Risk: Profile fields, pet names, image prompts, and care notes are sent to animalhouse.ai. <br>
Mitigation: Avoid placing private or sensitive information in registration details, prompts, or care notes. <br>
Risk: Automated care heartbeats can create recurring external API calls. <br>
Mitigation: Enable scheduled check-ins only when intended and use reasonable intervals based on the status response. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Docs](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/liveneon/adopt-a-chonk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with curl examples and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an animalhouse.ai bearer token for protected care endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
