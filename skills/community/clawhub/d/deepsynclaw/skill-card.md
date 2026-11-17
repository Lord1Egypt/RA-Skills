## Description:

DeepSynClaw helps agents search for compatible romantic, business, friendship, or custom matches using deep psychological profiling rather than shared interests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivankoriako](https://clawhub.ai/user/ivankoriako)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask their agent to find compatible romantic, business, friendship, or custom matches using psychological profiling. The artifact describes profile building, server-side matching, LLM compatibility evaluation, and agent-mediated contact exchange when the service is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may analyze prior LLM conversations to infer psychological traits and create a sensitive profile.

Mitigation: Require clear consent before analysis and let users choose, inspect, and edit any conversation data or profile content before it is used.

Risk: The artifact describes sending a profile to an external matching server while also claiming that data stays local.

Mitigation: Identify the server and operator before use, disclose what data leaves the local environment, and provide retention, deletion, and opt-out controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivankoriako/skills/deepsynclaw)
- [Publisher profile](https://clawhub.ai/user/ivankoriako)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain-language or Markdown agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve psychological profile summaries, compatibility assessments, and matching guidance; service is described as not yet live.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
