## Description: <br>
UUID inspector that parses UUIDs and extracts version, variant, timestamp details for v1 and v7, and MAC address details for v1 without using an LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze, validate, debug, or audit UUIDs, including identifying UUID version and variant and extracting timestamp or node details from time-based UUIDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UUID v1 values can reveal generation time and a device-like node identifier. <br>
Mitigation: Avoid logging or sharing raw v1 timestamp, MAC, or node output unless that detail is needed for the analysis. <br>
Risk: UUID v6, v7, v8, and Microsoft-variant handling is documented as partial, so edge-case results may be incomplete. <br>
Mitigation: Treat the output as inspection guidance and verify edge cases with authoritative UUID tooling before making policy or security decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-uuid-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON analysis with optional Python dictionary output and example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local, deterministic UUID analysis; batch mode accepts one UUID per input line.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
