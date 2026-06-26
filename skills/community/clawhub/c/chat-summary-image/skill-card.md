## Description: <br>
Turns conversations into polished visual summary cards by extracting key ideas, action items, and next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuminliu026](https://clawhub.ai/user/shuminliu026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to condense conversations into readable visual recap cards with a title, summary, key points, and next steps. It is suited for turning delivered work, open questions, or conversation snapshots into shareable summary images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the user for a Mew.design API key before image generation. <br>
Mitigation: Use a dedicated or revocable Mew.design API key and rotate it if it is pasted somewhere unintended. <br>
Risk: Conversation summary content is sent to Mew.design to generate the image. <br>
Mitigation: Avoid summarizing highly sensitive conversations unless sharing that content with Mew.design is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuminliu026/chat-summary-image) <br>
- [Chat Summary Image Patterns](references/patterns.md) <br>
- [Mew design API endpoint](https://api.mew.design/open/api/design/generate) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown containing an image link and original-image link, with helper-script commands used during generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a visual summary image through the Mew.design API after API-key validation and style selection.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
