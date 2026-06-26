## Description: <br>
Automates agent self-audit by gathering evidence, summarizing runs, proposing minimal patches, and requesting human approval for safe incremental evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adragon0707](https://clawhub.ai/user/adragon0707) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Audit Evolution after agent runs, failures, benchmarks, handoffs, or user feedback to convert evidence into a structured audit, memory ledger, minimal patch proposal, and next-run bootstrap. It is intended to preserve useful learning while keeping edits, external actions, and benchmark runs behind human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist automatic agent-routing behavior through installed guidance and hooks. <br>
Mitigation: Review the AGENTS.md block and .audit-evolution hooks before enabling them, and install only in workspaces where a persistent self-audit loop is desired. <br>
Risk: A short command can lead to local patch proposals and, after approval, modifications to skills, configs, or memory files. <br>
Mitigation: Require explicit file-by-file diff approval before allowing the "进化" flow to modify local files, and avoid --force unless overwriting an existing audit-evolution skill directory is intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adragon0707/audit-evolution) <br>
- [README](README.md) <br>
- [Adapter Guide](ADAPTERS_ZH.md) <br>
- [Quickstart](QUICKSTART_60S_ZH.md) <br>
- [Closed Loop Example](examples/closed_loop_case_zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown sections with YAML or text blocks and optional shell-command or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a seven-part audit bundle plus a short-command menu; patch proposals require human approval before application.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
