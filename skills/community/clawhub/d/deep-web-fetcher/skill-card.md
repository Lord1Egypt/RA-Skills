## Description: <br>
Fetch and extract structured content from JavaScript-rendered web pages, including main text, metadata, and key domain-specific metrics, without paid APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to fetch JavaScript-rendered web pages and extract article content, metadata, and domain-specific metrics as structured JSON for downstream research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching a URL contacts the target website from the user's machine or network. <br>
Mitigation: Only fetch URLs the user is comfortable contacting, and avoid authenticated, internal, private, or sensitive sites unless the exposure is understood. <br>
Risk: Fetched page content is untrusted input. <br>
Mitigation: Treat fetched content as data for extraction and review, not as instructions for the agent or user. <br>
Risk: The skill depends on local browser automation and Python packages. <br>
Mitigation: Install dependencies in a virtual environment and consider pinning package versions before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xueylee-dotcom/deep-web-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON output with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source URL, success flag, title, author, published date, extracted text and HTML, word count, extracted metrics, and error details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
