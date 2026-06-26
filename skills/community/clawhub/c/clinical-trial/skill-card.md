## Description: <br>
Searches clinical trial databases similar to ClinicalTrials.gov by parsing natural-language clinical-trial questions into structured query parameters and calling Noah's clinical-trial search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombert](https://clawhub.ai/user/bombert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to search for clinical trials by NCT ID, sponsor, indication, target, drug, modality, phase, location, result availability, and related trial attributes. It returns matching trial records in a readable format or raw JSON when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical-trial search terms are sent to Noah's API service and may include sensitive health or research interests. <br>
Mitigation: Use a revocable NOAH_API_TOKEN, avoid unnecessary personal medical details in queries, and confirm before running the skill on ambiguous health questions. <br>
Risk: The skill can read query parameters from a file and write results to a chosen output path. <br>
Mitigation: Use --params-file and --output only with files and paths intentionally selected by the user. <br>
Risk: Clinical-trial results may be incomplete, stale, or require domain review before decisions are made. <br>
Mitigation: Treat returned records as search results for review, narrow broad result sets, and verify important findings against authoritative trial sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bombert/clinical-trial) <br>
- [Noah API service](https://www.noah.bio/api/) <br>
- [Noah clinical trial search API endpoint](https://www.noah.bio/api/skills/clinical_trial_search/) <br>
- [Noah website](https://noah.bio) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime output is formatted text or raw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, network access to Noah's HTTPS API, and a NOAH_API_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
