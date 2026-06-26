## Description: <br>
Guides agents through preserving project context, serializing state, and planning retrieval workflows across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[watermelon11](https://clawhub.ai/user/watermelon11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to capture project state, architectural decisions, and semantic tags so context can be restored or transferred across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may capture broad project knowledge and preserve sensitive information in saved summaries, embeddings, or external stores. <br>
Mitigation: Run it on a narrow project folder, exclude secrets and private files, review saved outputs before storage, and avoid external vector databases or synchronization unless explicitly approved. <br>


## Reference(s): <br>
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline code and structured examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe JSON, Markdown, vector, Protocol Buffers, MessagePack, or YAML storage patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
