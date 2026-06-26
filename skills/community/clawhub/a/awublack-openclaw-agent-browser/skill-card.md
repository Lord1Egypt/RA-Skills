## Description: <br>
Lets an OpenClaw assistant call a locally installed agent-browser CLI to fetch a URL, extract the page title and Markdown content, and return structured JSON for summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awublack](https://clawhub.ai/user/awublack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw assistant retrieve webpage text through a locally installed browser CLI and summarize the extracted page content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL input can be passed into a shell command unsafely. <br>
Mitigation: Avoid untrusted or unusual URLs until the implementation uses safe argument passing such as spawn or execFile and validates http/https URLs. <br>
Risk: The documentation overstates privacy and safety for a tool that fetches remote webpages through a separate npm package. <br>
Mitigation: Review the maintainer, the agent-browser package, and outbound network behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awublack/awublack-openclaw-agent-browser) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Structured JSON containing the URL, page title, extracted Markdown content, and summary text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Node.js and agent-browser CLI availability; URL handling should be reviewed before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
