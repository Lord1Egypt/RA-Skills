## Description: <br>
Recursively scans image folders, compares configurable visual similarity, and moves likely duplicate images to a recycle folder while preserving higher-quality originals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onealmeng](https://clawhub.ai/user/onealmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to organize photo libraries, media folders, and image asset collections by recursively finding near-duplicates and moving lower-quality copies into a local recycle folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically move many image files inside the folder selected by the user. <br>
Mitigation: Run it first on a narrow folder or backup copy, use a high similarity threshold, and inspect the recycle folder before permanently deleting anything. <br>
Risk: Near-duplicate matching may classify visually similar but intentionally distinct images as duplicates. <br>
Mitigation: Start with a conservative similarity threshold and review moved files before treating the recycle folder as disposable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/onealmeng/deduplicate-images) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/onealmeng) <br>
- [ClawHub Homepage](https://clawhub.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown/text guidance with CLI command examples and terminal status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May move duplicate image files into a recycle folder under the selected root path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
