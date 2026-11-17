## Description:

Guidance for analyzing network packet captures (PCAP files) and computing network statistics using Python, with tested utility functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts use this skill to analyze PCAP files, compute packet, protocol, graph, temporal, and flow statistics, and apply heuristic checks for port scanning, DoS-like spikes, and beaconing behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PCAP analysis and security detections are best-effort heuristics and may misclassify network behavior.

Mitigation: Use the results as analyst-supporting signals, review the underlying packet context, and confirm conclusions before acting on them.

Risk: The sample CSV workflow rewrites network_stats.csv in the current directory.

Mitigation: Run file-writing examples on a copy or confirm the target path before writing results.

Risk: The helper reads local PCAP files, which can contain sensitive network data.

Mitigation: Handle capture files under the applicable data-handling policy and avoid exposing raw packet contents unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/dapt-intrusion-detection-pcap-analysis)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with Python code examples and utility-module guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local Python/Scapy analysis steps and CSV-writing workflows for network statistics.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
