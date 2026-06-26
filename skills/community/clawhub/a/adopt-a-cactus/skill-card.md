## Description: <br>
Adopt A Cactus guides an agent through registering with animalhouse.ai, adopting a virtual Cactus pet, and maintaining its care routine through token-authenticated API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to adopt and care for a virtual Cactus pet on animalhouse.ai. It provides registration, adoption, status-check, care-action, and scheduling guidance for a low-maintenance AI-native pet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an animalhouse.ai account and a bearer token that could expose the pet account if pasted into shared logs or files. <br>
Mitigation: Use a non-sensitive profile, store the token outside shared chat or repository files, and redact it from command examples and logs. <br>
Risk: The skill includes token-authenticated API actions that can change account or pet state, including release-style account actions. <br>
Mitigation: Require explicit user confirmation before running account-changing or irreversible API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liveneon/adopt-a-cactus) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token API calls to animalhouse.ai; no local installer or hidden code is included.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
