## Description: <br>
Brightdata Research helps an agent batch-search candidates, verify public web evidence, deduplicate results, assign risk tiers, and organize findings into Feishu or Lark documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[16miku](https://clawhub.ai/user/16miku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research operators use this skill to run repeatable public-web candidate research pipelines, collect evidence, deduplicate against current or historical Feishu/Lark documents, and produce structured findings with risk tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger global npm installs and add external skills during environment setup. <br>
Mitigation: Require explicit user approval before global installs or external skill additions, and review the exact commands before execution. <br>
Risk: The skill may read or write Feishu/Lark documents using the user's authorization. <br>
Mitigation: Confirm the target document and operation type before writes, prefer append over replace, and use Markdown-only output when document mutation is not intended. <br>
Risk: The skill can initialize or commit to a local git repository to enable subagent workflows. <br>
Mitigation: Require approval before git init, git add, or git commit, and fall back to serial execution when repository changes are not acceptable. <br>
Risk: Search summaries or scraped pages may be incomplete or misleading if treated as verified facts. <br>
Mitigation: Keep source links with each candidate, prefer official pages for capability evidence, and label low-confidence findings clearly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/16miku/brightdata-research) <br>
- [BrightData MCP setup](references/brightdata-mcp-setup.md) <br>
- [Environment checklist](references/environment-checklist.md) <br>
- [Feishu setup and write rules](references/feishu-setup.md) <br>
- [Known failures and fallbacks](references/known-failures-and-fallbacks.md) <br>
- [lark-cli install and auth](references/lark-cli-install-and-auth.md) <br>
- [Smoke tests](references/smoke-tests.md) <br>
- [Subagent and git prerequisites](references/subagent-git-prerequisites.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured research fields and inline shell commands when environment setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or append Feishu/Lark documents when the user provides authorization and a target document; otherwise returns Markdown in chat.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
