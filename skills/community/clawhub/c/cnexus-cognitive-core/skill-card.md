## Description: <br>
CNexus 2.0 is a local personal second-brain skill for running a Python standard-library and static UI memory app with a six-step cognitive loop, memory graph, JSON persistence, and one-click clear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plusunm](https://clawhub.ai/user/plusunm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local-first productivity users use this skill to set up and operate a personal memory app that turns conversations and documents into a local, persistent cognitive graph. It supports cognitive conversation, status inspection, memory clearing, REM-style memory organization, and optional code or image ingestion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local app can retain conversations, documents, and ingested material in a JSON state file. <br>
Mitigation: Decide whether that storage model is acceptable before installing, avoid storing secrets, and review local file access controls. <br>
Risk: The one-click clear-memory feature can remove useful local memory state. <br>
Mitigation: Back up important state before using the UI clear action or POST /api/memory/clear endpoint. <br>
Risk: Running the complete upstream app requires executing code from the server-resolved GitHub source. <br>
Mitigation: Review the upstream runtime before running python app_v2.py. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/plusunm/CNexus2.0/tree/main/clawhub/cnexus-cognitive-core) <br>
- [ClawHub skill page](https://clawhub.ai/plusunm/skills/cnexus-cognitive-core) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local endpoint summaries and cautions about persisted memory and clear-memory behavior.] <br>

## Skill Version(s): <br>
1.10.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
