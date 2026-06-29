## Description: <br>
Clean HTTP Toolkit lets agents make HTTP requests, download files with checksum verification, extract common web page content, and run small local HTTP test servers using Python standard-library scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to fetch URLs, call HTTP APIs, download files with checksum verification, extract page text or metadata, and run local HTTP test servers without adding third-party Python dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skipping TLS verification can hide certificate or interception problems when using the opt-in insecure mode. <br>
Mitigation: Use the default TLS verification path; reserve insecure mode for controlled testing only. <br>
Risk: Bearer tokens, basic credentials, or mutating HTTP methods can expose secrets or change remote systems. <br>
Mitigation: Use least-privileged credentials, avoid logging secrets, and review target URLs and methods before execution. <br>
Risk: Binding the local server to public interfaces can expose served files or echoed request data. <br>
Mitigation: Keep the default localhost binding unless exposure is intentional, and limit served directories and request counts. <br>


## Reference(s): <br>
- [Clean HTTP Toolkit on ClawHub](https://clawhub.ai/gopendrasharma89-tech/clean-http-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files, shell commands, configuration] <br>
**Output Format:** [Command-line output, JSON summaries, downloaded files, extracted page data, and local HTTP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and uses Python standard-library networking utilities.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
