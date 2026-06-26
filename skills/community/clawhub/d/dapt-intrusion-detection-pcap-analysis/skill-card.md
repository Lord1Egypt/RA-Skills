## Description: <br>
Guidance for analyzing network packet captures (PCAP files) and computing network statistics using Python, with tested utility functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and incident-response teams use this skill to compute packet, protocol, graph, temporal, and flow metrics from local PCAP files and interpret port-scan, DoS, beaconing, and benign-traffic indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packet captures and generated CSV outputs can contain private traffic, credentials, payload data, or other sensitive network information. <br>
Mitigation: Keep PCAP inputs and generated outputs in trusted locations, limit sharing, and adjust example file paths for the local environment before use. <br>
Risk: The helper module depends on Scapy and local packet parsing; missing or mismatched dependencies can lead to failed analysis. <br>
Mitigation: Install Scapy in the intended environment and review helper output before relying on analysis results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/dapt-intrusion-detection-pcap-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and helper-module usage instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PCAP analysis guidance and Python helper function usage; no external service calls are described.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
