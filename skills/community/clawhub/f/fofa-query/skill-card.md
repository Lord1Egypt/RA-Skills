## Description: <br>
Searches FOFA for internet-exposed assets by IP, domain, port, protocol, certificate, geography, time range, and other FOFA query fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, developers, and authorized asset owners use this skill to construct FOFA queries, run searches through the FOFA API, review text, table, or JSON results, and summarize findings for asset discovery or security research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FOFA receives submitted domains, IPs, organizations, and search terms. <br>
Mitigation: Use narrow authorized queries and avoid submitting sensitive targets that should not be disclosed to FOFA. <br>
Risk: FOFA credentials could be exposed through environment variables, command history, logs, or shared configuration. <br>
Mitigation: Keep FOFA_API_KEY private, prefer environment storage, rotate credentials if exposed, and avoid pasting credentials into prompts or logs. <br>
Risk: Broad or unauthorized asset searches can create compliance and misuse concerns. <br>
Mitigation: Use only for authorized asset discovery or security research and follow FOFA and target-site terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Moxin1044/fofa-query) <br>
- [FOFA](https://fofa.info) <br>
- [FOFA API](https://fofa.info/api/v1) <br>
- [FOFA query syntax reference](references/query_syntax.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and text, table, or JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, requests, and FOFA_API_KEY; sends user-provided searches to FOFA.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
