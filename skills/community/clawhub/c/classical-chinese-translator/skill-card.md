## Description: <br>
Converts Classical Chinese texts to modern vernacular Chinese while preserving supported e-book and HTML formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrfengcn](https://clawhub.ai/user/mrfengcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate Classical Chinese source texts into readable modern Chinese and to process full e-book or chapter batches while keeping document structure intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release has inaccurate capability tags for crypto and purchases even though the reviewed code does not perform those actions. <br>
Mitigation: Review the publisher and source before deployment and treat those tags as inaccurate until the release metadata is corrected. <br>
Risk: The translator reads and writes local e-book or HTML files, so incorrect paths or malformed inputs can affect user files. <br>
Mitigation: Run the tool on copies of files inside a scoped working directory and validate output before replacing originals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrfengcn/classical-chinese-translator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mrfengcn) <br>
- [Daoist terminology dictionary](references/daoist_terminology.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and translated UTF-8 text, HTML, XHTML, or e-book files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local input paths and writes translated output files; scanner evidence reports no hidden network, credential, persistence, or destructive behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
