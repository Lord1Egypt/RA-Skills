## Description: <br>
Searches Ctrip domestic China flights by city, IATA code, or province and returns prices, schedules, route comparisons, and low-price calendar data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hi-yu](https://clawhub.ai/user/hi-yu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Ctrip domestic China flight prices and schedules, compare routes, and find lower-cost options from city, IATA-code, or province inputs. <br>

### Deployment Geography for Use: <br>
Global, for China domestic flight searches where Ctrip is accessible. <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports weakened HTTPS protection because certificate verification is disabled. <br>
Mitigation: Use only on trusted networks and prefer an updated release that restores HTTPS certificate verification. <br>
Risk: The skill sends route/date queries and generated Ctrip identifiers to Ctrip and uses a local cookie cache. <br>
Mitigation: Avoid sensitive queries, review or clear the cookie cache when needed, and prefer a version that documents or limits cached identifiers. <br>
Risk: The security guidance calls out broad triggers and unpinned dependencies. <br>
Mitigation: Review prompts before execution and pin required dependencies such as quickjs in controlled deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hi-yu/ctrip-flights) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown tables by default, or structured JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, quickjs, and the bundled c-sign.js file; accepts departure, arrival, date, optional cabin, and --md or --json flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
