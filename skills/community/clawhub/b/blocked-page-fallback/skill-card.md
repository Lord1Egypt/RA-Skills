## Description: <br>
Recover when a web page is thin, blocked, JS-heavy, region-limited, or fetch-incompatible by switching to lawful fallback paths instead of stopping early. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and agents use this skill to continue public web research when a normal fetch or search result is blocked, thin, JavaScript-heavy, region-limited, or otherwise fetch-incompatible. It guides lawful fallback discovery while identifying when user-authorized login or a first-party API would be required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback research can drift toward restricted or login-protected content if boundaries are not kept explicit. <br>
Mitigation: Use only lawful public sources unless the user provides explicit authorization for login-protected content or first-party API access. <br>
Risk: Alternate sources such as snippets, mirrors, archives, or secondary databases may be incomplete or stale. <br>
Mitigation: Prefer authoritative sources and converging evidence, and report which fallback path produced the signal. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown with a structured fallback summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports failed primary path, attempted fallback paths, signal-producing fallback, best available answer, and any need for user-authorized login or first-party API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
