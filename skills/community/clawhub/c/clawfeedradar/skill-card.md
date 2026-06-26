## Description: <br>
Personal "news radar" skill built on top of a clawsqlite knowledge base and its interest clusters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ernestyu](https://clawhub.ai/user/ernestyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run personalized news-radar jobs against a clawsqlite knowledge base, score new feed items against existing interest clusters, and generate RSS/XML plus JSON outputs for review or subscription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON sidecars and feeds can reveal reading interests, article fulltext, summaries, scores, and cluster matches. <br>
Mitigation: Keep output directories private by default and review JSON sidecars before publishing or sharing generated feeds. <br>
Risk: Configured embedding, LLM, scraping, and git services may receive URLs, article text, summaries, or publishing credentials during normal operation. <br>
Mitigation: Use intentionally scoped service credentials, restrict source configuration, and enable git publishing only for repositories meant to host these feeds. <br>
Risk: The bootstrap step installs the upstream clawfeedradar Python package and the runtime executes that package's CLI. <br>
Mitigation: Install from trusted package sources and review or pin the upstream package version according to local deployment policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ernestyu/clawfeedradar) <br>
- [Project Homepage](https://github.com/ernestyu/clawfeedradar) <br>
- [Upstream Documentation](https://github.com/ernestyu/clawfeedradar/tree/main/docs) <br>
- [clawsqlite Project](https://github.com/ernestyu/clawsqlite) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Guidance] <br>
**Output Format:** [JSON responses with generated RSS XML feeds and JSON sidecar files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include NEXT guidance, output paths, warnings, scores, cluster matches, and error classification.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence, SKILL.md frontmatter, manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
