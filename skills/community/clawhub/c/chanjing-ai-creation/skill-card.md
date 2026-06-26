## Description: <br>
Chanjing AI creation Open API client: submit image and video tasks, poll task status, list and get tasks, and optionally download outputs when the user runs download_result.py. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binkes](https://clawhub.ai/user/binkes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to submit Chanjing AI image or video creation jobs, monitor asynchronous task status, inspect prior tasks, and save generated outputs only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local API credentials and access tokens are stored in credentials.json. <br>
Mitigation: Protect ~/.chanjing/credentials.json from other users, backups, and sync tools, and use a trusted credentials directory. <br>
Risk: Raw JSON payloads and callback URLs can submit arbitrary task parameters to the Chanjing Open API. <br>
Mitigation: Review body-file and body-json content before submitting tasks, especially model parameters, reference URLs, and callbacks. <br>
Risk: Changing the API base URL can send credentials and task data to an unintended endpoint. <br>
Mitigation: Keep CHANJING_OPENAPI_BASE_URL or CHANJING_API_BASE pointed only at a trusted Chanjing Open API endpoint. <br>
Risk: Downloaded result files are fetched from API response URLs and written to local storage. <br>
Mitigation: Run download_result.py only when the user explicitly wants a file saved, and choose an appropriate output path. <br>
Risk: The optional credentials-guard login helper may be used when credentials are missing. <br>
Mitigation: Verify the credentials-guard helper and login flow before relying on browser-assisted credential setup. <br>


## Reference(s): <br>
- [Chanjing AI Creation reference](reference.md) <br>
- [Chanjing AI Creation examples](examples.md) <br>
- [Chanjing Open API documentation](https://doc.chanjing.cc) <br>
- [ClawHub skill page](https://clawhub.ai/binkes/chanjing-ai-creation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/binkes) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, files] <br>
**Output Format:** [Plain text task identifiers and output URLs, JSON task details, command-line configuration, and downloaded image or video files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are returned from Chanjing API tasks; files are written locally only through the explicit download_result.py flow.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
