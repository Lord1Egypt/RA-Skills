## Description: <br>
A Xiaohongshu hot-post fetching and human-style rewrite prompt helper that stores results as local JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaojie66](https://clawhub.ai/user/Shaojie66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to gather Xiaohongshu-style hot post data, generate rewrite prompts that sound less AI-written, and save the resulting prompt package locally for later review or editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched content and generated rewrite prompts remain in local output JSON files until removed. <br>
Mitigation: Delete generated output files when they are no longer needed and avoid storing sensitive content in fetched or rewritten material. <br>
Risk: Real fetching may depend on an external Xiaohongshu MCP tool supplied by the agent environment. <br>
Mitigation: Review the MCP tool's permissions and network behavior in the target agent environment before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Shaojie66/auto-redbook-content) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON files containing source note fields, metadata, and rewrite prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local files under output/; XHS_MAX_RESULTS controls the requested note count.] <br>

## Skill Version(s): <br>
2.5.2 (source: frontmatter, package.json, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
