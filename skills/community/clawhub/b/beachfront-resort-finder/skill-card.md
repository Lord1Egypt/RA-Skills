## Description: <br>
Find beach and island resorts, including oceanfront rooms, private beaches, tropical stays with direct beach access, and water activities, powered by Fliggy through the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for beach and island resort options with real-time availability, pricing, and booking links. It is activated for beach, oceanfront, seaside, island resort, and matching Chinese-language resort requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned global flyai CLI package. <br>
Mitigation: Require approval before any npm global install and prefer a pinned, local, or sandboxed CLI installation. <br>
Risk: Travel search details may be sent to the flyai provider. <br>
Mitigation: Install only when users trust the provider and are comfortable sharing the travel details needed for search and booking. <br>
Risk: The skill can store raw travel queries in .flyai-execution-log.json. <br>
Mitigation: Disable, delete, or restrict access to the execution log when local query retention is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/beachfront-resort-finder) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and short guidance with inline shell commands and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results; user-facing results should include booking links and the flyai real-time pricing brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
