## Description: <br>
Driftling Buddy adds a compact, non-human companion that reacts to a user's real work, renders bilingual terminal cards, tracks local progress, and grows a collection over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taojinkai](https://clawhub.ai/user/taojinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to add a lightweight companion layer to normal agent sessions, including progress-aware terminal cards, collection mechanics, bilingual flavor, and local continuity across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buddy progress and activity-derived notes can be saved locally, which may expose sensitive personal, client, or secret information if those details are placed in buddy context. <br>
Mitigation: Review or redirect BUDDY_STATE_FILE before use and avoid placing sensitive information in buddy context. <br>
Risk: The companion layer can add whimsical status text around serious work, which may distract from warnings, failures, or uncertainty. <br>
Mitigation: Keep the buddy output compact, reduce whimsy for urgent or high-stakes tasks, and never let buddy text hide warnings or unresolved risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taojinkai/driftling-buddy) <br>
- [Publisher profile](https://clawhub.ai/user/taojinkai) <br>
- [README](artifact/README.md) <br>
- [Skill source](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with terminal-card text and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON state for buddy collection and growth; supports Chinese, English, and mixed-language output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
