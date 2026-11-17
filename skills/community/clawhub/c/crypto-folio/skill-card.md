## Description:

Asset Management helps agents record and manage crypto holdings, trades, yield products, transfers, accounts, and export portfolio reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christinafanxy](https://clawhub.ai/user/christinafanxy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage cryptocurrency portfolios through natural-language entries, local or optional Cloudflare-backed storage, visual review, and CSV-style exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial portfolio data in local files, browser storage, and optional Cloudflare KV.

Mitigation: Use only data the user is comfortable storing in those locations and review the skill carefully before installing.

Risk: The security summary flags unsafe local/cloud APIs and persistent browser-stored credentials.

Mitigation: Avoid enabling cloud sync until the local API is authenticated and loopback-only, browser rendering is XSS-safe, and stored credentials are handled appropriately.

Risk: The security guidance warns about hardcoded Worker tokens and third-party AI processing of financial context.

Mitigation: Use Worker secrets instead of hardcoded tokens, rotate any token or AI key already used with this version, and warn before sending financial documents or portfolio context to third parties.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christinafanxy/skills/crypto-folio)
- [Project homepage](https://github.com/ChristinaFanxy/CryptoFolio-Skill)
- [CryptoFolio README](artifact/readme.md)
- [Cloudflare Worker deployment guide](artifact/cloudflare-worker/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Chinese conversational confirmations, shell commands, JSON state, and CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores portfolio data in local files and browser storage, with optional Cloudflare KV synchronization.]

## Skill Version(s):

1.0.0 (source: release metadata, skill frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
