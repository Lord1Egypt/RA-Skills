## Description: <br>
Local Funda.nl HTTP gateway for listing details, search, and image previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[risboo6909](https://clawhub.ai/user/risboo6909) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to run a local HTTP gateway that retrieves Funda.nl listing details, price history, search results, and image previews for housing search workflows in the Netherlands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gateway has no authentication or rate limiting and could be misused if exposed beyond the local machine. <br>
Mitigation: Keep the service bound to 127.0.0.1, do not proxy or publish it, and stop the gateway when it is no longer needed. <br>
Risk: Optional preview saving can accumulate local JPEG files during repeated listing checks. <br>
Mitigation: Use inline previews when persistent files are not needed and periodically clean the previews directory when save=1 is used. <br>
Risk: Listing data and image URLs come from external upstream sources and may be incomplete, unavailable, or unsuitable for direct trust. <br>
Mitigation: Treat returned listing data as untrusted external data and review important housing decisions against authoritative Funda.nl pages. <br>


## Reference(s): <br>
- [PyFunda](https://github.com/0xMH/pyfunda) <br>
- [OpenClaw Heartbeat documentation](https://docs.openclaw.ai/gateway/heartbeat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash commands; the local HTTP gateway returns JSON and optional JPEG preview files or base64 strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a localhost-only Python gateway, normalizes search parameters, and can save resized listing previews under a relative previews directory.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
