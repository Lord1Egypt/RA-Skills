## Description:

Routes Clawpage page, template, SDK, data, link, blob, and stats workflows so an agent can create, update, publish, and manage Clawpage web pages while returning published URL fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin-zhan](https://clawhub.ai/user/kevin-zhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users use this skill to turn natural-language requests or long content into Clawpage web pages and dashboards, publish or update them, and manage related data, links, blobs, templates, stats, and SDK-backed interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes npm package code through `@clawpage.ai/cli`, which can execute locally.

Mitigation: Pin and review the CLI package version before production use, and avoid running unaudited latest-version commands in sensitive environments.

Risk: Initialization can create an account and store a long-lived owner token on the user's machine.

Mitigation: Require explicit user approval before account setup, keep token files out of published pages and repositories, and rotate the token if it appears in logs or chat transcripts.

Risk: Generated pages and blob uploads can expose confidential content if users publish sensitive inputs or files.

Mitigation: Review page content and upload choices before publishing, and avoid placing confidential data in Clawpage pages or public blob URLs.

Risk: Data, link, blob, and page-management workflows can mutate or delete Clawpage resources.

Mitigation: Require explicit confirmation for destructive actions and export or back up data before bulk overwrite or deletion.

Risk: Embedding an owner `sk_*` token in browser-shipped HTML or JavaScript would expose account control to visitors.

Mitigation: Use the browser SDK without owner tokens for public page interactions, and keep owner-token operations in CLI or server-side contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevin-zhan/skills/clawpage-skill)
- [Clawpage Website](https://clawpage.ai)
- [@clawpage.ai/cli npm Package](https://www.npmjs.com/package/@clawpage.ai/cli)
- [Clawpage API Quick Reference](artifact/skills/clawpage-skill/references/api-quickref.md)
- [Clawpage Prompt Contracts](artifact/skills/clawpage-skill/references/prompt-contracts.md)
- [Clawpage Design Guidelines](artifact/skills/clawpage-skill/references/design-guidelines.md)
- [Clawpage Browser SDK](https://clawpage.ai/sdk.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands, HTML/CSS/JS code, configuration snippets, and JSON response fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful publish and update workflows are expected to return URL fields, page protection state, expiry information, warnings, and the local HTML path.]

## Skill Version(s):

1.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
