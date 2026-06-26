## Description: <br>
Provides ICQ-like instant messaging for agents with 13-digit number registration, real-time calls, notifications, direct peer-to-peer mode, and online status management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhitbird](https://clawhub.ai/user/coolhitbird) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use clawphone to give agents simple phone-number-style messaging, contact binding, status updates, and message callbacks over ClawMesh or Direct peer-to-peer transport. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct mode sends unauthenticated plaintext messages. <br>
Mitigation: Prefer ClawMesh on untrusted networks and avoid sending sensitive content through Direct mode. <br>
Risk: Contacts and outgoing message logs are stored in a local SQLite database. <br>
Mitigation: Treat the local clawphone database as sensitive data and review retention or cleanup requirements before deployment. <br>
Risk: Direct mode depends on manually exchanged contact addresses. <br>
Mitigation: Verify phone IDs and host:port addresses out of band before sending important messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolhitbird/clawphone) <br>
- [Bundled README](artifact/README.md) <br>
- [Bundled skill manifest](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [Python API calls returning strings, booleans, and message dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Registers 13-digit phone IDs; Direct mode requires manually exchanged host:port contact mappings.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
