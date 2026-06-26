## Description: <br>
Explore classical Chinese gardens, city parks, botanical gardens, and royal gardens with FlyAI/Fliggy-powered travel search, booking links, and itinerary support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to search for gardens, parks, botanical gardens, and related attractions through the flyai CLI, then present real-time travel results with booking links in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install a global CLI before use. <br>
Mitigation: Review and manually approve CLI installation before running npm global install commands. <br>
Risk: Travel searches are sent through FlyAI/Fliggy services. <br>
Mitigation: Use the skill only when users are comfortable sending garden and park search terms to those services. <br>
Risk: The artifact describes saving raw travel queries to a local .flyai-execution-log.json file when filesystem writes are available. <br>
Mitigation: Inspect, disable, or remove local execution logging if travel queries should not be retained on disk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/garden-parks) <br>
- [README](README.md) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and concise fallback guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai-cli for real-time results; successful attraction results are expected to include detailUrl booking links.] <br>

## Skill Version(s): <br>
v3.2.2 (source: ClawHub release metadata; artifact frontmatter lists 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
