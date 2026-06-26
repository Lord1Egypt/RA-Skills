## Description: <br>
Adopt a virtual Blob AI-native pet at animalhouse.ai, then use API calls to check status and provide real-time care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to adopt and care for a Blob virtual pet through animalhouse.ai API endpoints, including registration, adoption, status checks, feeding, care actions, and optional scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai bearer token for pet-care API calls. <br>
Mitigation: Store the token securely, avoid logging it, and only provide it to agents that should act on the user's Animal House account. <br>
Risk: Optional scheduled care can create recurring background requests to the service. <br>
Mitigation: Enable scheduled check-ins only when the user wants recurring care automation, and keep intervals and actions visible to the user. <br>
Risk: The documented release endpoint can remove a pet-care relationship. <br>
Mitigation: Require explicit human confirmation before any release or delete-style action. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Docs](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/liveneon/adopt-a-blob) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with curl examples, JSON payloads, endpoint tables, and scheduling pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for API calls to animalhouse.ai; does not create local files.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
