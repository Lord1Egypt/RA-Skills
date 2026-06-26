## Description: <br>
Curates external-facing changelogs from change logs, commit summaries, or release notes while separating user-facing value from internal changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release managers, and documentation teams use this skill to turn change lists, PR summaries, and release scope notes into reviewable changelog drafts for releases, announcements, and internal updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public changelog wording can be inaccurate, sensitive, or imply unsupported compatibility guarantees if source material is incomplete. <br>
Mitigation: Review release wording, compatibility notes, and sensitive statements before publishing. <br>
Risk: The Python helper reads local input paths and can write to a chosen output path. <br>
Mitigation: Run it only on intended files, use deliberate output paths, and prefer dry-run or review workflows when handling sensitive material. <br>
Risk: Changing bundled configuration could broaden local file inspection behavior. <br>
Mitigation: Do not edit the bundled spec to enable audit modes unless broader local inspection is intentional and reviewed. <br>


## Reference(s): <br>
- [Changelog Curator on ClawHub](https://clawhub.ai/52YuanChangXing/changelog-curator) <br>
- [Publisher profile: 52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown changelog drafts, optional JSON, and local shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include version summary, user-visible changes, internal changes, compatibility notes, upgrade advice, known limitations, confirmation items, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
