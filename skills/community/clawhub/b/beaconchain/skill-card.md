## Description: <br>
Monitor Ethereum validator dashboard health on beaconcha.in via V2 API, focused on one-check-per-day status and BeaconScore-first triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThisIsJeron](https://clawhub.ai/user/ThisIsJeron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to run concise daily health checks for an Ethereum validator dashboard on Beaconcha.in. It reports healthy, attention-needed, or error status from BeaconScore and missed-duty signals while keeping normal healthy output brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Beaconcha.in API key and dashboard ID to query validator dashboard status. <br>
Mitigation: Provide credentials through environment variables, use the least-privileged or read-only API key available, and avoid exposing command output that may include account or dashboard details. <br>
Risk: Network requests are made to the Beaconcha.in validator performance API and may fail due to authentication, rate limits, endpoint errors, or account permissions. <br>
Mitigation: Check API key validity, dashboard ID, plan permissions, and rate limits when the skill returns an error status. <br>


## Reference(s): <br>
- [Beaconcha.in API Notes](references/api-notes.md) <br>
- [Beaconcha.in](https://beaconcha.in) <br>
- [Beaconcha.in performance-aggregate endpoint](https://beaconcha.in/api/v2/ethereum/validators/performance-aggregate) <br>
- [ClawHub skill page](https://clawhub.ai/ThisIsJeron/beaconchain) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status lines or JSON from the dashboard checker, plus Markdown guidance for setup and triage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, BEACONCHAIN_API_KEY, and BEACONCHAIN_DASHBOARD_ID; supports chain, window, warning-threshold, timeout, and JSON-output options.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
