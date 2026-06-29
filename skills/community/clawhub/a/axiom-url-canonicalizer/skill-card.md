## Description: <br>
Normalize URLs for SEO and comparison by lowercasing hosts, sorting query parameters, removing default ports, stripping tracking parameters, and normalizing percent encoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to canonicalize URLs for SEO workflows, cache deduplication, duplicate URL detection, and comparison that ignores tracking noise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL canonicalization can be mistaken for destination safety validation, but the artifact documents no DNS resolution, TLS validation, redirect following, or full scheme support. <br>
Mitigation: Use this skill for normalization and comparison only; apply separate URL safety, redirect, DNS, and TLS checks before trusting or fetching a destination. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code] <br>
**Output Format:** [Plain text or JSON URL canonicalization results, with optional Python function usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic local processing; no network access or credential use indicated by security evidence.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
