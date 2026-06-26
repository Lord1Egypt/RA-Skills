# Security Notes

This package is intentionally instruction-only.

It does not include:

- Executable scripts
- Package dependencies
- Shell commands
- Remote code loading
- API keys
- Credential handling
- Network calls

The skill asks an AI agent to reason over user-provided ads, landing pages, and campaign context. Users should still avoid pasting private credentials, ad account access tokens, CRM exports, patient data, protected health information, or sensitive customer records into any AI system unless they have an approved data-handling workflow.

For regulated categories such as health, dental, legal, financial, or aesthetic services, the skill instructs agents to flag claims for human review rather than treating generated copy as compliance-approved.
