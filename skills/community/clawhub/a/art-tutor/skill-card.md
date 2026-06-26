## Description: <br>
A private art-learning tutor that recommends resources from a local art knowledge base, builds staged learning paths, and answers technique questions based on the user's goals, level, and preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingxiahotmail](https://clawhub.ai/user/qingxiahotmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as an art study coach for watercolor, sketching, art history, digital art, illustration, photography, and related topics. It helps diagnose learning needs, scan a configured local art-library folder, recommend specific resources, and turn those resources into practical study plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can list filenames and sizes inside the configured local art-library folder. <br>
Mitigation: Set knowledge_base_path to a dedicated art-books directory rather than a broad personal or system folder, and review scan output before sharing it. <br>
Risk: Recommendations may be inaccurate if the configured folder does not match the documented art knowledge-base structure. <br>
Mitigation: Verify the configured path and the returned file paths before relying on the study plan or resource recommendations. <br>


## Reference(s): <br>
- [Art Knowledge Base Collection List](references/corpus.md) <br>
- [Art Learning Paths Recommendation Guide](references/learning_paths.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with resource paths, staged study plans, practice suggestions, and optional PowerShell file-scanning commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-configured knowledge_base_path and may list filenames and file sizes from that directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
