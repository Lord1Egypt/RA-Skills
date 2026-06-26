## Description: <br>
使用 Everything SDK 快速搜索本地文件，提供文件详情并支持发送选定文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyKungBj](https://clawhub.ai/user/andyKungBj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or individual Windows users use this skill to search local files through Everything, inspect file metadata, and send a selected result to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and return contents of files selected from local search results, and the file export path is broad. <br>
Mitigation: Review searched locations before use and avoid directories containing secrets, credentials, private documents, or work data unless confirmation, path or type allowlists, and clear warnings are added. <br>


## Reference(s): <br>
- [Everything SDK](https://www.voidtools.com/support/everything/sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [JSON response with human-readable status text and optional base64 file payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are limited to the first 10 matches; file sending is capped at 10 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
