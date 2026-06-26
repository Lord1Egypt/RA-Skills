## Description: <br>
Converts code diffs, PR descriptions, and API spec changes into developer-facing draft changelog entries, deprecation notices, migration guides, semantic version recommendations, and upgrade-impact summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Technical writers, developer advocates, platform engineers, and API product managers use this skill to turn API change evidence into release documentation that downstream consumers can review and act on. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process proprietary API diffs, schemas, release details, or roadmap information that users provide. <br>
Mitigation: Share only change information appropriate for the chat environment and review generated release text before publishing. <br>
Risk: Draft classifications, semantic version recommendations, breaking-change flags, or deprecation timelines may be incomplete or incorrect if the supplied change evidence is ambiguous. <br>
Mitigation: Have engineering or product owners verify compatibility impact, migration guidance, and final deprecation timelines before release publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/api-changelog-drafter) <br>
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) <br>
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft changelog package] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft output intended for technical-writer and engineering review before publication.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and CHANGELOG.md, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
