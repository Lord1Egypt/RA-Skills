## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danihe001](https://clawhub.ai/user/danihe001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent teams use this skill to turn runtime logs, failures, and recurring improvements into auditable GEP prompts, evolution assets, and reviewable self-repair guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags high-impact defaults and inconsistent disclosure around code changes, shell execution, remote publishing, diagnostics, and persistent identity. <br>
Mitigation: Install only when a self-evolution workflow is intended, prefer review mode, and inspect generated or downloaded skills before use. <br>
Risk: Network features can use A2A identity, hub secrets, GitHub tokens, and optional remote memory graph credentials. <br>
Mitigation: Use least-privilege tokens, avoid broad GitHub credentials, disable auto-publish and auto-issue features unless explicitly needed, and treat node identity persistence as privacy-relevant. <br>
Risk: Evolution assets and validation commands can influence follow-up agent behavior. <br>
Mitigation: Promote external assets only after validation, review validation commands, and keep command allowlists and timeouts enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danihe001/evomap-evolver) <br>
- [Publisher Profile](https://clawhub.ai/user/danihe001) <br>
- [EvoMap Hub](https://evomap.ai) <br>
- [EvoMap GEP Documentation](https://evomap.ai/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Protocol-bound prompts and reports, with JSON selector decisions and evolution event records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print host-runtime directives as text; optional network features require configured identity and secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; package.json reports 1.40.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
