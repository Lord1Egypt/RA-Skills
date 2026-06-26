## Description: <br>
获取B站Top20榜单，提取标题、摘要和链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raise7727](https://clawhub.ai/user/raise7727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users invoke this skill to fetch the current Bilibili Top 20 ranking and receive each video's title, short description, and link for quick review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and makes a network request to Bilibili's public API when invoked. <br>
Mitigation: Install and run it only in a trusted Python environment with the expected requests dependency, and review outbound network access before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raise7727/bili-trending) <br>
- [Bilibili ranking API](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Up to 20 Bilibili ranking entries with title, short description, and video link.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
