## Description: <br>
Open Apple News, read Apple News links, and run local News workflows on macOS using deterministic CLI commands and shortcut-based search fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers on macOS use this skill to open Apple News, read specific Apple News articles or feeds, and run repeatable local News workflows with explicit confirmation before multi-link or shortcut actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opening multiple Apple News links can disrupt the user's reading context or expose sensitive topics in opened URLs. <br>
Mitigation: Preview links, keep confirmations enabled, and require explicit confirmation before opening more than one link. <br>
Risk: User-owned Shortcuts may trigger additional local or network actions outside the base skill behavior. <br>
Mitigation: Review the Shortcut name and expected behavior before running it, and keep confirmation enabled for shortcut execution. <br>
Risk: Local preferences and operation notes in ~/apple-news/ may retain reading workflow details. <br>
Mitigation: Periodically review ~/apple-news/ and remove retained preferences or notes that should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/apple-news) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill homepage](https://clawic.com/skills/apple-news) <br>
- [Apple News endpoint](https://apple.news) <br>
- [Setup](artifact/setup.md) <br>
- [Command Paths](artifact/command-paths.md) <br>
- [Operation Patterns](artifact/operation-patterns.md) <br>
- [Safety Checklist](artifact/safety-checklist.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-first macOS workflow guidance with confirmation guardrails for multiple links and Shortcuts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
