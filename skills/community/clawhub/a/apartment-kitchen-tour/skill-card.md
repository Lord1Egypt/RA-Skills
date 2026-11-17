## Description:

Turn one kitchen photo the listing already uses into one short clip for the listing page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and hosts use this skill to turn one existing apartment kitchen listing photo into a short listing-page or short-video clip while keeping the photographed room layout, visible text, and amenities grounded in the source image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra device credential can access more than kitchen-video generation.

Mitigation: Treat the credential as account-level Beatra access, keep it in the private credential file only, and revoke or uninstall the connection when it is no longer needed.

Risk: Automatic local code updates are enabled by default.

Mitigation: Disable silent updates with `python3 scripts/mcp_client.py update --auto off` when automatic replacement of package-owned executable files is not acceptable.

Risk: Paid video generation can create unnecessary charges if changed work is retried as the same request or duplicate work is submitted.

Mitigation: Freeze the approved payload, use one opaque `client_request_id` per approved photo, and recover uncertain submissions only with identical arguments.

Risk: Generated motion can misrepresent a property if the model invents appliances, storage contents, text, or fixtures.

Mitigation: Limit the motion vocabulary, require supporting interior photos for opened cabinets or appliances, preserve transcribed text, and review the final clip for drift against the source image.

## Reference(s):

- [Kitchen tour workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/apartment-kitchen-tour)
- [Beatra skill homepage](https://beatra.ai/skills/apartment-kitchen-tour)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, video artifact]

**Output Format:** [Markdown guidance with shell commands, JSON tool payloads, task status, billing details, and returned video artifact references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One kitchen photo produces one clip; the skill requires a live model card and user approval before each paid video generation.]

## Skill Version(s):

0.1.2 (source: release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
