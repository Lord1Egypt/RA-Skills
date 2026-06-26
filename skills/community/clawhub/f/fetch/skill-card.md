## Description: <br>
Public web retrieval and clean extraction engine for public URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public web pages, extract readable text and links, save raw and cleaned copies locally, and inspect previous fetch jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches URLs supplied by the user or agent, which can unintentionally include internal, private, or credential-bearing URLs. <br>
Mitigation: Use it only with deliberate public http/https URLs and avoid URLs that contain credentials or point to internal systems. <br>
Risk: Fetched pages are saved locally and may retain sensitive content if sensitive pages are fetched by mistake. <br>
Mitigation: Periodically review or clear the saved history and page files under ~/.openclaw/workspace/memory/fetch. <br>


## Reference(s): <br>
- [Fetch Philosophy](references/philosophy.md) <br>
- [Fetch ClawHub Listing](https://clawhub.ai/AGIstack/fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Command-line text output and local raw HTML or clean text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores fetched page content and job history under ~/.openclaw/workspace/memory/fetch.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
