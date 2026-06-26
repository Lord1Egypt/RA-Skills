## Description: <br>
A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris8265-cl](https://clawhub.ai/user/chris8265-cl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams maintaining agent prompts, logs, and long-running agent loops use this skill to inspect runtime history, generate GEP-guided evolution prompts, and capture reusable Genes, Capsules, and Events for auditable improvement cycles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence describes this as a high-authority self-evolving agent component that can spawn long-running automation and update behavior. <br>
Mitigation: Use review or dry-run modes first, run it in a disposable git worktree, and require human review before applying generated changes in sensitive environments. <br>
Risk: The security evidence says the skill can read broad agent history, memory files, and stable identifiers, and may send data to configured external services. <br>
Mitigation: Limit accessible logs and memory, remove secrets from transcripts, review remote memory and hub settings, and use only the minimum credentials needed. <br>
Risk: The security evidence calls out auto-update, hub networking, task claiming, auto-publish, loop mode, and remote memory settings as controls that need review. <br>
Mitigation: Disable or explicitly review those features before running the skill, especially in shared, production, or credentialed workspaces. <br>
Risk: The artifact supports validation commands and external asset ingestion, which can affect local files or agent behavior if promoted without review. <br>
Mitigation: Validate external assets before promotion, keep command allowlists narrow, and verify generated Genes, Capsules, and Events before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris8265-cl/evolver-bak) <br>
- [EvoMap documentation](https://evomap.ai/wiki) <br>
- [EvoMap](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text prompts with structured JSON-style evolution assets, command snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local GEP assets, reports, and evolution state when the skill is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
