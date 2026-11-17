## Description:

Fetch car specifications from Chinese automotive websites (dongchedi.com and autohome.com.cn) when the user needs vehicle configuration data such as price, dimensions, battery capacity, range, seating layout, or top speed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and report builders use this skill to collect vehicle specifications from Chinese automotive websites and format the results for comparisons, PPTs, reports, or spreadsheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler makes live web requests and may follow scraped or redirected URLs outside the stated automotive sites.

Mitigation: Run it in a restricted environment, avoid sensitive networks, and review network behavior before operational use.

Risk: The --output option writes crawler results to a user-specified path.

Mitigation: Review the output path before running the command and avoid writing into sensitive or shared locations.

Risk: Missing Python dependencies may be installed ad hoc.

Mitigation: Pin and review requests and lxml versions before installing them in the execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/car-specs-crawler)
- [Dongchedi](https://www.dongchedi.com)
- [Autohome](https://car.autohome.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands; crawler output as JSON or markdown tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write JSON output to a user-specified file path when --output is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
