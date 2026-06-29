## Description: <br>
Downloads Baidu image-search results by keyword to a local folder using Baidu's acjson endpoint and a zero-dependency Node.js command-line script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lfp1979](https://clawhub.ai/user/lfp1979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run a Node.js CLI that downloads Baidu image-search results by keyword into a local folder, with options for count, image source, delay, and output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to Baidu while collecting image results. <br>
Mitigation: Avoid sensitive or confidential search terms when using the skill. <br>
Risk: Image downloads from Baidu or third-party origin hosts can create local clutter or consume disk space. <br>
Mitigation: Use a dedicated output folder, keep requested counts reasonable, and review downloaded files before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lfp1979/baidu-img-download) <br>
- [Baidu image acjson endpoint](https://image.baidu.com/search/acjson) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [Downloaded image files with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes images under download/<keyword>/ by default, or to a user-specified output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
