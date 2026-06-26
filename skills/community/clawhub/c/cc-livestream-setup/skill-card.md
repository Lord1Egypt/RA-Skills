## Description: <br>
Creates and configures CC live streaming rooms through the CC HTTP API, including room setup, authentication, and credential handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elberren](https://clawhub.ai/user/elberren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create CC live streaming rooms, choose room templates, configure mobile viewing behavior, and run the room creation API flow with user-supplied CC credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The room creation script uses weak fixed privileged room passwords for publisher and assistant access. <br>
Mitigation: Generate or request strong per-room publisher and assistant passwords before running the script, then verify or rotate room credentials in the CC console after use. <br>
Risk: The script prints request URLs that may contain sensitive request details. <br>
Mitigation: Redact request URLs and avoid logging credentials, hashes, or account identifiers before using the script in a shared terminal, log collector, or support workflow. <br>
Risk: The skill creates resources in the user's CC account. <br>
Mitigation: Review the selected template, authentication settings, and account context before execution, and confirm the created room settings in the CC console afterward. <br>


## Reference(s): <br>
- [CC Live API Documentation Reference](references/api_docs.md) <br>
- [CC Live API Base URL](https://api.csslcloud.net/api/) <br>
- [CC Live Room Creation Endpoint](https://api.csslcloud.net/api/room/create) <br>
- [CC THQS Signature Documentation](https://doc.bokecc.com/live/developer/live_api/Appendix_2.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with command-line script usage and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces room creation status and room identifiers when the CC API call succeeds.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
