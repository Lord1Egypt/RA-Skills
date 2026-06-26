## Description: <br>
Encode an agent personality into a diploid genome with 27 cognitive primitives, compare against a library of agent personalities, simulate compatibility, and generate phenotype cards or self-knowledge reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohmhm1](https://clawhub.ai/user/mohmhm1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to encode SOUL.md personality files as genome JSON, compare agent genomes, browse a personality library, and generate structured summaries for agent self-knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package is incomplete and directs the agent to run helper Python files that are not included. <br>
Mitigation: Install or run it only in a trusted directory that contains the expected encoder.py, visualize.py, agent_report.py, and library files. <br>
Risk: Encoding may send SOUL.md content to a Claude API call. <br>
Mitigation: Use the mock option when source personality content should not leave the local environment. <br>
Risk: Bundled HTML reports can contact Google Fonts when opened. <br>
Mitigation: Open reports in a network-restricted environment or block external font requests when offline behavior is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mohmhm1/ai-genome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, text summaries, and JSON phenotype card outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encoding may call a Claude API unless the mock option is used; local comparison and reporting depend on trusted helper files and genome library files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
