## Description: <br>
Schedule and coordinate asynchronous group meetings with 2-50 participants via email across timezones, with status checks, pauses, resumes, and cancellations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DheerG](https://clawhub.ai/user/DheerG) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and external-facing teams use this skill to create, monitor, pause, resume, and cancel asynchronous meeting requests for internal or external participants. Developers and agents can use it to call SkipUp's API for email-based scheduling without direct calendar access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting requests can contact participants or alter live scheduling coordination. <br>
Mitigation: Ask for explicit user confirmation before creating, cancelling, pausing, or resuming a meeting request. <br>
Risk: Meeting metadata, participant email addresses, and workspace-member information are sent to SkipUp. <br>
Mitigation: Install and use the skill only when the user trusts SkipUp with that data and has configured an appropriate SKIPUP_API_KEY. <br>
Risk: Duplicate meeting requests may be created if retries are not handled carefully. <br>
Mitigation: Use an Idempotency-Key header when creating meeting requests. <br>
Risk: Organizer emails that are not active workspace members can cause request failures. <br>
Mitigation: Verify the organizer with the workspace members endpoint before creating a meeting request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DheerG/ai-meeting-scheduling) <br>
- [Publisher Profile](https://clawhub.ai/user/DheerG) <br>
- [SkipUp Homepage](https://skipup.ai) <br>
- [API Reference](references/api-reference.md) <br>
- [Natural Language Examples](references/examples.md) <br>
- [Meeting Scheduling API Reference](https://support.skipup.ai/api/meeting-requests/) <br>
- [OpenClaw Integration Guide](https://support.skipup.ai/integrations/openclaw/) <br>
- [API Authentication and Scopes](https://support.skipup.ai/api/authentication/) <br>
- [SkipUp llms.txt](https://skipup.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce SkipUp API request payloads and concise user-facing status summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
