## Description:

Adsbrain Trace Error Locator helps agents diagnose AdsBrain and Codewiz Langfuse/XRay traces by locating the failing observation, step, tool, or model behavior, explaining responsibility, and suggesting fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizejia668-code](https://clawhub.ai/user/lizejia668-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate incorrect AdsBrain or Codewiz agent behavior from Langfuse/XRay trace links, trace IDs, screenshots, timestamps, or expected-versus-actual examples. The skill produces a concise root-cause report that identifies the faulty observation or responsibility boundary, cites key trace evidence, and recommends fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a local trace-analysis script with user-controlled trace_id and project_id values, and the release security summary says safe argument handling is not clear.

Mitigation: Use the skill only in trusted environments; validate trace_id and project_id strictly, reject shell metacharacters and whitespace, and call the trace-analysis tool through a reviewed package-controlled path or structured argument API.

Risk: The artifact references a user-specific absolute path for the trace-analysis dependency.

Mitigation: Replace the user-specific path with an approved, versioned dependency path before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizejia668-code/skills/adsbrain-trace-error-locator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown root-cause report with trace/session links, key evidence, and fix suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report is concise; detailed timelines and full evidence chains are produced only when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
