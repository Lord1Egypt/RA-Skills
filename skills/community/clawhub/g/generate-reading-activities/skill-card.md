## Description: <br>
根据书名生成读书活动，生成详细介绍、每日打卡计划、问答题库等文档. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lay-white](https://clawhub.ai/user/lay-white) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn a book title into a reading activity package with a book introduction, a 7-day reading check-in plan, and a question bank. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated materials under a configured local output directory and creates a ZIP archive. <br>
Mitigation: Check the destination path before running the skill and avoid using sensitive book titles or sensitive output locations. <br>
Risk: The skill moves the generated working folder to the recycle bin after archiving. <br>
Mitigation: Keep backups or review the generated ZIP before relying on the cleanup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lay-white/generate-reading-activities) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lay-white) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration] <br>
**Output Format:** [Markdown and Excel files collected into a ZIP archive] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a timestamped local output folder for the requested book, then archives the generated materials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
