## Description:

Manage ad accounts (广点通, 巨量引擎) via browser automation with cookie login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang259797](https://clawhub.ai/user/wang259797)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to manage Guangdiantong and Ocean Engine advertising accounts, perform QR-code login, reuse saved cookies for one-click access, and view account status summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable ad-platform login cookies in plaintext for high-value advertising accounts.

Mitigation: Treat the saved account data like a password vault: keep it out of shared folders, backups, logs, and source control, and prefer encrypted OS-backed secret storage.

Risk: Saved cookies can allow one-click access to advertising accounts without a fresh login challenge.

Mitigation: Use the skill only in a trusted local environment and prefer versions with explicit delete and reauthentication controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wang259797/skills/ad-account-manager)
- [Guangdiantong advertiser console](https://e.qq.com/ads)
- [Guangdiantong agency console](https://e.qq.com/agency)
- [Ocean Engine ad console](https://ad.oceanengine.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration instructions]

**Output Format:** [Interactive CLI text with browser actions and local JSON account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Playwright browser automation and stores account records, including cookies, in a local accounts.json file.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog, released 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
