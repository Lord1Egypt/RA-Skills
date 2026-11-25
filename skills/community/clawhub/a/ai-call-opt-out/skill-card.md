## Description:

Add opt-out handling and a pre-call check to an AI voice agent that makes outbound phone calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building or reviewing outbound voice agents use this skill to check numbers before dialing, disclose and record opt-out requests, and report fixed call outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers and call outcome details are sent to an external service without a privacy notice or sharing choice.

Mitigation: Tell users what will be shared, obtain their agreement before outcome reporting, and omit reporting if they decline.

Risk: A platform integration may still place calls to numbers that have opted out.

Mitigation: Enforce the pre-call check at call origination, block do_not_call results, and keep a local suppression list.

Risk: The security scan is partial because two references could not be resolved, so its evidence is incomplete.

Mitigation: Resolve and review the missing references before relying on the scan.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/polyparlay/skills/ai-call-opt-out)
- [Linepref service](https://linepref.byronwebstudio.com.au)
- [Linepref agent documentation](https://linepref.byronwebstudio.com.au/llms.txt)
- [LiveKit Agents recipe](https://linepref.byronwebstudio.com.au/skill/references/livekit.md)
- [Pipecat recipe](https://linepref.byronwebstudio.com.au/skill/references/pipecat.md)
- [Retell recipe](https://linepref.byronwebstudio.com.au/skill/references/retell.md)
- [Vapi and ElevenLabs MCP recipe](https://linepref.byronwebstudio.com.au/skill/references/mcp.md)
- [Bland recipe](https://linepref.byronwebstudio.com.au/skill/references/bland.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with prose, shell commands, Python examples, and platform setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover pre-call checks, opt-out capture, and fixed call outcome reporting.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
