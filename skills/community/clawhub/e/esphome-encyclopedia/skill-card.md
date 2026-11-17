## Description:

ESPHome Encyclopedia guides agents through official-doc-first ESPHome configuration help, YAML authoring and review, component selection, troubleshooting, local documentation caching, and operational notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when working on ESPHome nodes and configurations, especially when they need current component documentation, YAML guidance, config review, troubleshooting, or cautious live node maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation cache helper may fetch and persist off-domain or oversized content when redirects and response sizes are not bounded.

Mitigation: Use the cache helper only after validating redirects on every hop, bounding content type and response size, and keeping cached source URLs auditable.

Risk: Workspace notes and inventories can accidentally capture sensitive ESPHome operational details.

Mitigation: Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia cache, notes, or inventory files.

Risk: Cached pages and local observations can become stale or be mistaken for authoritative ESPHome behavior.

Mitigation: Treat cached pages as reference material, distinguish official documentation from local observations, and recheck current ESPHome docs before device-impacting configuration or OTA work.

## Reference(s):

- [ESPHome Components Documentation](https://esphome.io/components/)
- [ESPHome Encyclopedia Workflow Notes](references/workflow.md)
- [.ESPHome-Encyclopedia Cache Layout](references/cache-layout.md)
- [ESPHome Topic Map](references/topic-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with ESPHome YAML, code snippets, and shell commands when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses workspace-local ESPHome documentation cache and notes when available]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
