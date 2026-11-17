## Description:

Provides real-time searches and verified Geekbench scores for the latest officially released flagship smartphones by brand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingqing404](https://clawhub.ai/user/dingqing404)

### License/Terms of Use:


## Use Case:

Developers and device analysts use this skill to identify current flagship smartphones, fetch Geekbench CPU benchmark records, and produce concise score reports grouped by device and Geekbench version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches Geekbench data from the web, so benchmark availability and device naming can change between runs.

Mitigation: Re-run searches at the time of use and verify results against current Geekbench pages and official device release status.

Risk: The monitor script can send reports through an OpenClaw Feishu messaging setup to an embedded recipient.

Mitigation: Review or disable notification behavior before running the monitor, and make the recipient explicit in the local deployment.

Risk: Reports and archives are written to fixed local paths, and report filenames can be derived from device names.

Mitigation: Configure output directories before use and sanitize device-derived filenames when adapting the scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingqing404/skills/geekbench)
- [Geekbench Browser](https://browser.geekbench.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or plain-text reports with links to Geekbench benchmark records, plus optional JSON data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include device names, Geekbench versions, single-core and multi-core scores, benchmark URLs, local report paths, and monitor summaries.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
