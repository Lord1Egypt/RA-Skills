## Description: <br>
Expand a structured brief in `content-production/inbox/` into a reusable long-form markdown article draft, then run a local writer / critic / judge quality loop with a constrained humanization pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and developers use this skill to turn a structured brief with a topic, reader, arguments, and examples into a first-draft long-form article plus reusable writing sidecars for downstream image generation and WeChat formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local brief files and writes generated draft and review files into content-production folders. <br>
Mitigation: Use trusted brief files and review generated article, writing pack, and review trace outputs before downstream publication. <br>
Risk: User-controlled slug values affect generated file paths. <br>
Mitigation: Keep slug values simple and predictable so generated files stay in the intended content-production folders. <br>
Risk: External repository dependencies may affect local execution behavior. <br>
Mitigation: Review dependencies before running the skill in a local article-drafting workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abigale-cyber/case-writer-hybrid) <br>
- [Publisher profile](https://clawhub.ai/user/abigale-cyber) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files] <br>
**Output Format:** [Markdown article draft with Markdown and JSON sidecar files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the article draft, writing pack, review trace, and optional quality-gate notice under content-production paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
