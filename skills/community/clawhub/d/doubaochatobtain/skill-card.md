## Description: <br>
DoubaoChatObtain guides an agent through browser automation to extract the full text of a Doubao chat thread and save it as a local text file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenyang-x](https://clawhub.ai/user/zenyang-x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract complete Doubao conversation text for local review or follow-on analysis when normal page reading is limited by virtual scrolling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted Doubao conversation text may contain private or sensitive information. <br>
Mitigation: Review the output path before running the skill, keep generated files local, and delete /tmp/doubao_raw.json and the generated text file when they are no longer needed. <br>
Risk: The workflow depends on agent-browser and a loaded Doubao page, so extraction may fail if the page is not ready or the scroll container is not found. <br>
Mitigation: Open the target Doubao URL with agent-browser, wait for the page to finish loading, scroll when needed, and retry if the extraction returns NOT_FOUND. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zenyang-x/doubaochatobtain) <br>
- [agent-browser package](https://www.npmjs.com/package/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with bash, JavaScript, and Python command examples; extracted Doubao content is saved as a UTF-8 text file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local files, including /tmp/doubao_raw.json and a user-selected text output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
