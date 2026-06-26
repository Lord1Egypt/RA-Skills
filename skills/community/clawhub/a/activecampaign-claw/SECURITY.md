# Security policy

## Reporting a vulnerability

If you discover a security issue in this skill — including credential handling,
markdown injection from API data, command-injection vectors in scripts, or
unsafe defaults — please report it privately rather than opening a public issue.

**Preferred channel:** Open a [GitHub Security Advisory](https://github.com/ji282h7/activecampaign-claw/security/advisories/new)
on the repository. Advisories are private until you and a maintainer agree to disclose.

If you cannot use Security Advisories, contact the author via the email listed
on their GitHub profile.

Please include:

- A clear description of the issue and its impact
- Reproduction steps (a minimal script or commit reference is ideal)
- Your AC plan tier and the affected endpoint(s) if relevant
- Whether the issue is exploitable in the OpenClaw agent harness, the standalone
  CLI, or both

## Response expectations

- **Acknowledgement** within 5 business days
- **Triage + initial assessment** within 14 days
- **Fix or mitigation** for critical issues within 30 days, lower-severity within 90
- **Credit in the changelog** unless you ask to remain anonymous

## Scope

In scope:

- All Python scripts in `scripts/`
- `_ac_client.py` and its handling of `AC_API_URL` / `AC_API_TOKEN`
- Markdown rendering of API response data (`sanitize()` in `_ac_client.py`)
- The state file at `~/.activecampaign-skill/state.json` and the history JSONL
- Default file permissions and storage of credentials

Out of scope:

- Vulnerabilities in ActiveCampaign's own API or infrastructure (report to AC)
- OpenClaw gateway / harness vulnerabilities (report to OpenClaw)
- Issues that require already having privileged access to the user's machine
- Social engineering of the user

## Design philosophy and scope of operation

This skill is built around a single, important constraint: **it operates only against the AC account whose token you provide**, and it does so on your behalf as the legitimate account holder.

A few specific consequences of that constraint are worth calling out because automated security scanners sometimes misread the patterns:

1. **The data you see is your own.** Reports include contact emails, names, deal values, and similar information *because that information lives in your AC account, which you own and operate*. Displaying it back to you is not a privacy leak — it is the entire point of a reporting tool. The skill does not share data with the skill author, the marketplace, or any other third party. All output is written to local files on your machine or printed in your terminal session.

2. **Exports are backups, not exfiltration.** Scripts like `snapshot.py`, `account_archive.py`, and `contact_data_export.py` write your data to a local JSON file. This is the same right you have through AC's own dashboard export. The data does not travel anywhere it doesn't already have access to — you are the data controller.

3. **Per-contact data export is a feature, not a risk.** `contact_data_export.py` exists to help account holders fulfill their legal obligation when a customer requests their data. This is a compliance feature, not a way to extract data that someone shouldn't have. The output is written locally so the operator can forward it through whatever legally-required channel applies.

4. **Webhook audit is not SSRF.** `webhook_audit.py` probes the webhook URLs *you have already configured in your AC account*. It cannot be redirected to arbitrary third-party targets and offers a `--skip-probe` flag if you prefer not to make the outbound check. This is "verify your own configuration" — not "make my server fetch arbitrary URLs."

5. **CSV validation is read-only.** `import_validator.py` validates a CSV against deliverability rules. It does not push the CSV to AC, and it does not call any AC write endpoint. Bulk-import to AC is performed in AC's own UI, by the user, after they review the validator's report.

6. **Write operations exist and are explicitly declared.** A subset of scripts modify records in your AC account when you ask them to. The "Operating model" section of SKILL.md enumerates these and the multi-layer safeguards around them (least-privileged token, `AC_READ_ONLY=1` env var, `AC_MAX_WRITES` per-process cap, audit log, dry-run defaults on destructive helpers, explicit user confirmation before every POST/PUT/DELETE).

## Hardening notes for users

- Use a dedicated AC integration user with the minimum permissions needed.
- AC tokens are scoped to the user that created them — rotate the token
  whenever the integration user changes.
- Tokens are stored at `~/.openclaw/openclaw.json` (mode 0600). Anyone with
  shell access to that user account can read them. Enable full-disk security
  on the device.
- The skill never sends data to third-party services — only to your own AC
  account via your own token.
- For pure-analysis use, set `AC_READ_ONLY=1` in your shell environment before
  invoking any script. This refuses every write at the HTTP layer before any
  request goes out.
- Treat any exported file (suppression list, local export, snapshot) as you
  would any other customer-data export: store it securely, share only with
  people who need it for a legitimate business reason, and delete it when
  the need has passed.

## Credit / coordinated disclosure

We follow standard coordinated disclosure. If a fix lands in a public release,
we'll mention the reporter in the CHANGELOG entry unless they ask otherwise.
