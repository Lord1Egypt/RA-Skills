## Description: <br>
Schedules Feishu meetings by finding shared availability, sending interactive poll cards, and coordinating follow-up through webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lens-lzy](https://clawhub.ai/user/Lens-lzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and teams use this skill to coordinate meetings in Feishu by checking participant availability, proposing time slots, collecting poll responses, and retrying when conflicts appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service can access calendar availability, send messages, create meetings, and track participant responses. <br>
Mitigation: Install only in a controlled Feishu tenant, grant the minimum required app permissions, and review the requested capabilities before deployment. <br>
Risk: The /api/claw routes may be reachable by callers outside the intended agent workflow. <br>
Mitigation: Place an authenticated gateway in front of the /api/claw routes and restrict allowed callers. <br>
Risk: Wake-up callbacks could be sent to unintended destinations if the endpoint is not constrained. <br>
Mitigation: Restrict OPENCLAW_WAKE_ENDPOINT with ALLOWED_WAKE_DOMAINS. <br>
Risk: Availability, poll choices, and response status are processed and temporarily stored during coordination. <br>
Mitigation: Notify users about the processed data and retain session state only as long as needed for scheduling. <br>
Risk: Webhook authenticity is weaker when FEISHU_ENCRYPT_KEY is not configured. <br>
Mitigation: Configure FEISHU_ENCRYPT_KEY and verify Feishu webhook signatures before accepting card actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lens-lzy/easy-meeting) <br>
- [Publisher profile](https://clawhub.ai/user/Lens-lzy) <br>
- [Feishu Open Platform](https://open.feishu.cn/app/) <br>
- [OpenAPI contract](artifact/openapi.yaml) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON API responses with Feishu interactive card messages and webhook-driven status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, a reachable service URL, and webhook configuration; stores meeting session state while coordination is in progress.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact package.json is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
