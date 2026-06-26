## Description: <br>
Dual-value learning system that extracts reusable mental models from books, writes individual pattern files with YAML frontmatter, and produces F.A.C.E.T. analysis for user learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kedoupi](https://clawhub.ai/user/kedoupi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, lifelong learners, product teams, founders, investors, and strategists use this skill to select books, extract F.A.C.E.T. mental-model analyses, and build a reusable local decision-framework library for future agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local knowledge-base and reading-history files may contain sensitive book choices, user context, or generated analysis. <br>
Mitigation: Review generated files under memory/knowledge-base and memory/reading-history.json before sharing or syncing them. <br>
Risk: Optional Feishu or Notion export can send analysis records outside the local workspace when credentials are configured. <br>
Mitigation: Keep Feishu and Notion export disabled for confidential material and store tokens in environment variables only. <br>
Risk: Personal details in USER.md can be incorporated into personalized Transfer analysis. <br>
Mitigation: Avoid adding employer, project, or personal details to USER.md unless those details are intended to influence outputs. <br>


## Reference(s): <br>
- [Cognitive Forge on ClawHub](https://clawhub.ai/kedoupi/cognitive-forge) <br>
- [book-scout dependency](https://clawhub.ai/kedoupi/book-scout) <br>
- [mental-model-forge dependency](https://clawhub.ai/kedoupi/mental-model-forge) <br>
- [Book Selection](references/book-selection.md) <br>
- [Example Output](references/example-output.md) <br>
- [Knowledge Classification](references/knowledge-classification.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown briefings, Markdown pattern files with YAML frontmatter, and JSON reading-history updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local knowledge-base files and optionally sync records to Feishu or Notion when configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
