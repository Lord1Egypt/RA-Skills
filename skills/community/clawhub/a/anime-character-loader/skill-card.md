## Description: <br>
Load anime character info from multiple sources and generate validated SOUL.generated.md files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinchen4](https://clawhub.ai/user/colinchen4) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to look up anime character data, disambiguate similar names, and generate SOUL.generated.md character files for agent roleplay configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Character and anime names may be sent to third-party public services during lookup. <br>
Mitigation: Use the skill only when those queries are acceptable, and avoid submitting private or sensitive names as character inputs. <br>
Risk: Generated files can overwrite or merge with existing SOUL.md content. <br>
Mitigation: Review prompts before choosing REPLACE or MERGE and keep backups of important SOUL.md files. <br>
Risk: The documented external-quotes opt-out may not be implemented in the artifact behavior. <br>
Mitigation: Do not rely on that opt-out for privacy-sensitive use unless the publisher implements and verifies it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/colinchen4/anime-character-loader) <br>
- [AniList GraphQL API](https://graphql.anilist.co) <br>
- [Jikan API](https://api.jikan.moe/v4) <br>
- [Baseline v2.4 notes](docs/baseline-v2.4.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown SOUL.generated.md files with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or merge SOUL.md files and cache public character lookup responses locally.] <br>

## Skill Version(s): <br>
2.4.2 (source: server release metadata, SKILL.md frontmatter, setup.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
