## Description: <br>
Extract and monitor Apple Notes content for workflow integration. Supports bulk extraction, real-time monitoring, and export to various formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianderrington](https://clawhub.ai/user/ianderrington) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and macOS productivity users use this skill to extract, monitor, and export Apple Notes content into local files and workflow tools. It is intended for users who need structured note archives, search indexes, or imports into knowledge-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Apple Notes extraction can copy private or sensitive notes into local exports and downstream workflow tools. <br>
Mitigation: Review output locations and privacy filters before running, prefer selective or simple extraction where possible, and avoid full extraction unless it is needed. <br>
Risk: Full extraction can install and run an unpinned third-party Ruby parser. <br>
Mitigation: Review, trust, and pin the external parser before using full extraction; otherwise use the simpler local AppleScript extraction path. <br>
Risk: Monitoring, webhooks, AI processing, Git, Notion, search, or backup integrations can share extracted notes outside Apple Notes. <br>
Mitigation: Keep monitoring and webhooks disabled unless explicitly needed, and apply filtering, encryption, and access-control review before connecting external systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ianderrington/apple-notes-extractor) <br>
- [Publisher Profile](https://clawhub.ai/user/ianderrington) <br>
- [README](artifact/README.md) <br>
- [Usage Guide](artifact/USAGE.md) <br>
- [Integration Guide](artifact/INTEGRATION.md) <br>
- [Apple Cloud Notes Parser](https://github.com/threeplanetssoftware/apple_cloud_notes_parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, Python code examples, and local note export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports may include JSON, Markdown, SQLite, Obsidian-compatible files, metadata, and attachments depending on configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
