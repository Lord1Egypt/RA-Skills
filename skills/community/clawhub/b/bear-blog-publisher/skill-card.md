## Description: <br>
Publish blog posts to Bear Blog platform. Supports user-provided markdown, AI-generated content, and auto-generated diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CatTalk2](https://clawhub.ai/user/CatTalk2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, and teams use this skill to publish user-provided or AI-generated Markdown posts to Bear Blog. It can also generate simple architecture diagrams for technical posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Bear Blog credentials to publish content publicly. <br>
Mitigation: Install only when publishing authority is intended, avoid pasting passwords into chat, and review drafts before publishing. <br>
Risk: Plaintext config is supported for Bear Blog credentials. <br>
Mitigation: Prefer environment variables or runtime secret handling; if config is used, keep the file owner-readable only. <br>
Risk: The security review notes unclear Bear Blog account scoping. <br>
Mitigation: Verify that the configured dashboard URLs and account context match the intended Bear Blog account before publishing. <br>


## Reference(s): <br>
- [Bear Blog](https://bearblog.dev/) <br>
- [Bear Blog Publisher on ClawHub](https://clawhub.ai/CatTalk2/bear-blog-publisher) <br>
- [CatTalk2 Publisher Profile](https://clawhub.ai/user/CatTalk2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like result objects, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a published Bear Blog URL or an error message; optional diagram generation produces a PNG file path before publishing.] <br>

## Skill Version(s): <br>
1.0.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
