## Description:

Generate and deploy app Privacy Policy and Terms of Service static websites from an app feature document. Use when a user provides app requirements/feature docs and wants production-ready legal pages published via GitHub + Cloudflare Pages, including draft generation, consistency checks, and deployment-ready output URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chentuan7963-afk](https://clawhub.ai/user/chentuan7963-afk)

### License/Terms of Use:


## Use Case:

Developers and app publishers use this skill to turn app feature documentation into reviewable Privacy Policy and Terms of Service static pages, then optionally deploy the approved site to Cloudflare Pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated legal pages may contain incorrect contact, jurisdiction, or data-practice statements if sample values or incomplete inputs are copied unchanged.

Mitigation: Replace all sample contact and jurisdiction values, review the generated Privacy Policy and Terms of Service line by line, and confirm the pages match the app's actual behavior before publication.

Risk: Deployment can publish an approved draft to the wrong Cloudflare Pages project if the project name or production branch is not confirmed.

Mitigation: Confirm the exact Cloudflare project and production branch before deployment, and require explicit user approval after reviewing the generated files.

Risk: Cloudflare credentials could be exposed if pasted into prompts or generated documents.

Mitigation: Configure Cloudflare credentials through environment variables or Wrangler login, and do not paste API tokens into prompts.

## Reference(s):

- [Cloudflare Pages + GitHub Deployment](artifact/references/cloudflare-github-deploy.md)
- [App Legal Pages on ClawHub](https://clawhub.ai/chentuan7963-afk/skills/app-legal-pages)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash commands plus generated HTML and CSS files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a static legal mini-site and can return Cloudflare Pages URLs after user-approved deployment.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
