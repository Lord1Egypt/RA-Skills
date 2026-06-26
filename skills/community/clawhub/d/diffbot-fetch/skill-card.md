## Description: <br>
Fetch and extract clean article content from any URL using the Diffbot Article API. Returns clean Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flobo3](https://clawhub.ai/user/flobo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch a URL through Diffbot and extract the article title, metadata, and main text without page clutter. It is useful when clean Markdown article content is needed for reading, summarization, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs and the Diffbot API token are sent to Diffbot. <br>
Mitigation: Use only URLs that are acceptable to share with Diffbot, and keep the Diffbot API key scoped and protected. <br>
Risk: Internal, access-controlled, pre-signed, localhost, or otherwise sensitive URLs may expose sensitive request context to Diffbot. <br>
Mitigation: Avoid using this skill with sensitive URLs unless sharing those URLs with Diffbot is acceptable. <br>


## Reference(s): <br>
- [Diffbot Article API endpoint](https://api.diffbot.com/v3/article) <br>
- [ClawHub listing](https://clawhub.ai/flobo3/diffbot-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown article content printed to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIFFBOT_API_KEY and sends the requested URL to Diffbot.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
