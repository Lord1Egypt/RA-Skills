## Description: <br>
Crypto Research Interactive Framework helps AI agents conduct interactive crypto research with human-AI collaboration across project, sector, tokenomics, technical, content, image-prompt, QA, and brainstorming workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kudodefi](https://clawhub.ai/user/kudodefi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and researchers use this skill to structure crypto market, project, tokenomics, technical, and content workflows with checkpoints for human review. It is suited for producing research briefs, comparative analysis, investment-oriented reports, content drafts, image prompts, and QA reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous mode may proceed with less user review and may load relevant workspace documents or prior outputs without asking at each step. <br>
Mitigation: Use collaborative mode for important research, investment decisions, or unfamiliar topics, and review workspace documents before enabling autonomous execution. <br>
Risk: Crypto research can depend on current market, on-chain, and public web data that changes quickly or may be incomplete. <br>
Mitigation: Require dated sources, confidence notes, and primary-source checks before relying on generated analysis. <br>
Risk: Optional MCP data sources can involve API keys when users configure them. <br>
Mitigation: Store MCP API keys in local environment-variable based configuration rather than URL-based examples or framework files. <br>
Risk: The skill writes research outputs and session state under local workspaces. <br>
Mitigation: Monitor and review workspace files, and remove sensitive source materials or outputs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kudodefi/crif) <br>
- [README](README.md) <br>
- [Security and permissions](SECURITY.md) <br>
- [Orchestrator](references/core/orchestrator.md) <br>
- [Core configuration](references/core/core-config.md) <br>
- [MCP servers](references/core/mcp-servers.md) <br>
- [Research methodology](references/guides/research-methodology.md) <br>
- [Collaborative research](references/guides/collaborative-research.md) <br>
- [Output standards](references/guides/output-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown research reports, briefs, content drafts, image prompts, QA notes, and workspace state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source citations, confidence notes, recommendations, checkpoints, and local workspace files depending on workflow.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md framework version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
