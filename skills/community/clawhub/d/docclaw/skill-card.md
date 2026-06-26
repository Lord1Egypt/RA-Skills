## Description: <br>
DocClaw is a documentation skill for OpenClaw that combines live docs search, direct markdown fetch, and offline local-doc fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibecodooor](https://clawhub.ai/user/vibecodooor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use DocClaw to answer OpenClaw documentation questions with canonical links, exact configuration keys, command flags, and local fallback search when live documentation is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes Python scripts that perform network fetches and write local documentation index or cache files. <br>
Mitigation: Review the scripts before use when source provenance matters, run them as a normal user, and allow fetches only to docs.openclaw.ai. <br>
Risk: Fetched documentation may be stale, incomplete, or inconsistent with installed OpenClaw behavior. <br>
Mitigation: Treat fetched docs as reference material and verify behavior with openclaw command help when exact runtime behavior matters. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [DocClaw ClawHub listing](https://clawhub.ai/vibecodooor/docclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with documentation links, concise notes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exact OpenClaw documentation links, fetched markdown references, and local search commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: changelog, released 2026-02-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
