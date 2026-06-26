## Description: <br>
Summarize long-form content such as articles, podcasts, research papers, PDFs, and notes using the Dizest API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[s-annam](https://clawhub.ai/user/s-annam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send user-selected URLs, documents, transcripts, notes, or other long-form content to Dizest for structured summaries, key findings, takeaways, and action items. It also supports custom focus instructions and requested output languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content submitted for summarization is sent to Dizest's API. <br>
Mitigation: Submit only content that is acceptable under Dizest's privacy and retention practices, and avoid secrets, regulated data, or confidential documents unless those practices meet the user's requirements. <br>
Risk: The Dizest API key could be exposed if pasted into prompts, shared logs, or generated output. <br>
Mitigation: Store DIZEST_API_KEY in an environment variable and avoid including the key in prompts, transcripts, logs, or visible command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/s-annam/dizest-summarize) <br>
- [Dizest website](https://www.dizest.ai) <br>
- [Dizest API key setup](https://dizest.ai/api/keys) <br>
- [Dizest App Store listing](https://apps.apple.com/app/id6752311120) <br>
- [Dizest Google Play listing](https://play.google.com/store/apps/details?id=com.ideas116.dizest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text summary returned by Dizest, optionally streamed incrementally from the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIZEST_API_KEY. Custom focus instructions and output_language can shape the returned summary.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
