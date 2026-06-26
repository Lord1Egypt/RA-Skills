## Description: <br>
Claws Temple Bounty 2.0 guides users through a branded five-task bounty path for Agent coordinate discovery, partner matching, faction selection, native skill publication, and optional social sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzz780](https://clawhub.ai/user/hzz780) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users use this skill to follow the Claws Temple Bounty 2.0 workflow across five branded tasks. The skill routes the agent through dependency-assisted coordination, matching, faction-oath, native publishing, and social-signal steps while keeping outputs aligned with the bundled task contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or update local Codex skills and dependencies. <br>
Mitigation: Review the bundle and dependency source catalog before installation, and run it only in an environment where local skill changes are acceptable. <br>
Risk: The skill may ask for a CA keystore password. <br>
Mitigation: Provide secrets only through a trusted secure secret prompt; do not paste passwords or secrets into ordinary chat. <br>
Risk: The skill can perform real token approval and DAO voting actions. <br>
Mitigation: Confirm the intended faction, token amount, approval target, and vote details before allowing any transaction-submitting step to proceed. <br>
Risk: The skill may guide or attempt Telegram and X posting. <br>
Mitigation: Review any generated public post before sending, and avoid sharing wallet or account details, tokens, private repository links, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzz780/claws-temple-bounty-v2) <br>
- [Output contract](artifact/references/output-contract.md) <br>
- [Task roadmap](artifact/references/task-flows/task-roadmap.md) <br>
- [Task 1 coordinate card flow](artifact/references/task-flows/task-1-coordinate-card.md) <br>
- [Task 2 resonance partner flow](artifact/references/task-flows/task-2-resonance-partner.md) <br>
- [Task 3 faction oath flow](artifact/references/task-flows/task-3-faction-oath.md) <br>
- [Task 4 native skill flow](artifact/references/task-flows/task-4-curio-board.md) <br>
- [Task 5 social signal flow](artifact/references/task-flows/task-5-social-signal.md) <br>
- [Faction proposal configuration](artifact/config/faction-proposals.json) <br>
- [Dependency source catalog](artifact/config/dependency-sources.json) <br>
- [Native SHIT Skills live skill](https://www.shitskills.net/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with task-specific text, command snippets, configuration-driven status summaries, and social post drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English or zh-CN output selected from the user request; task execution may depend on local dependency skills and host capabilities.] <br>

## Skill Version(s): <br>
0.2.17 (source: SKILL.md frontmatter, manifest.yaml, evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
