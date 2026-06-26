## Description: <br>
Boss Cli helps agents use the BOSS Zhipin CLI to search jobs, manage applications, export results, and contact recruiters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitowerofbabel-lang](https://clawhub.ai/user/aitowerofbabel-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and agents assisting them use this skill to run BOSS Zhipin CLI workflows for job discovery, filtering, application tracking, interviews, history, profile checks, exports, and recruiter greetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rely on browser-cookie login or other account session access. <br>
Mitigation: Install only if the user trusts `kabi-boss-cli`; prefer QR login or a separate browser profile instead of automatic cookie import. <br>
Risk: Greeting and batch-greeting commands can send real messages from the user's recruiting account. <br>
Mitigation: Use dry-run or preview mode before batch greetings and manually confirm message content and recipients before sending. <br>
Risk: Search results, application history, interviews, profile data, and exports may contain private job-search information. <br>
Mitigation: Review CSV or JSON exports and message-related outputs before storing, sharing, or integrating them with other systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aitowerofbabel-lang/boss-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide CSV or JSON exports and dry-run command use where supported by the CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
