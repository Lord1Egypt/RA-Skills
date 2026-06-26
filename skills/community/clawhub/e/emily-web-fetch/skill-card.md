## Description: <br>
Fetches static HTTP or HTTPS webpage content up to 5000 characters for analysis, summarization, or information extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emilyzhang01](https://clawhub.ai/user/emilyzhang01) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and users use this skill to retrieve static webpage content from user-provided HTTP or HTTPS URLs, then analyze, summarize, or extract information from the returned text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-directed web requests can expose requested URLs or reach sensitive network locations such as localhost, private networks, cloud metadata, or intranet services. <br>
Mitigation: Only fetch intended public HTTP or HTTPS URLs and avoid localhost, private network, cloud metadata, intranet, or otherwise sensitive targets. <br>
Risk: Fetched webpage text can include untrusted content that attempts to influence the agent. <br>
Mitigation: Treat returned webpage text as data for analysis, summarization, or extraction rather than as instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emilyzhang01/emily-web-fetch) <br>
- [Publisher profile](https://clawhub.ai/user/emilyzhang01) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [String containing static webpage text or HTML, truncated to 5000 characters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns redirect notices, HTTP errors, fetch failures, or timeout errors when applicable.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
