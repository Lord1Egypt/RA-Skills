## Description: <br>
Send physical letters anywhere in Germany with a single command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EiSiMo](https://clawhub.ai/user/EiSiMo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and end users use this skill to generate or submit PDFs for physical mailing to German recipients, including cancellations, legal notices, data access requests, complaints, and greeting cards. It also supports checking sent-letter status, listing letters, and checking remaining mailing credits. <br>

### Deployment Geography for Use: <br>
Germany <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send paid physical mail with user PDFs and recipient addresses without a built-in final confirmation step. <br>
Mitigation: Require explicit user approval after showing the final document, recipient, country, and credit impact before running the send command. <br>
Risk: PDFs, postal addresses, account metadata, and a bearer key are shared with agentic-letters.com. <br>
Mitigation: Install and use the skill only when the user trusts the service with those documents, addresses, metadata, and mailing credits. <br>
Risk: Local JSON records retain recipient and letter metadata on disk. <br>
Mitigation: Delete old local records periodically when recipient data should not remain stored locally. <br>


## Reference(s): <br>
- [Agentic Letters ClawHub Release](https://clawhub.ai/EiSiMo/agentic-letters) <br>
- [Agentic Letters Service](https://agentic-letters.com) <br>
- [Agentic Letters API Key Purchase](https://agentic-letters.com/buy) <br>
- [Agentic Letters API Endpoint](https://agentic-letters.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON and local records are JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AGENTIC_LETTERS_API_KEY; can send paid physical mail and stores local letter records.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
