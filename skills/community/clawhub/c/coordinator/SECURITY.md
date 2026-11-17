# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 1.0.x | Yes |

Only the latest patch release of the 1.0.x line receives security fixes.

## Reporting a vulnerability

Please report vulnerabilities **privately** to `<SECURITY_CONTACT>`.
Do not open a public issue for security problems.

Include in your report:

- A description of the issue and its potential impact
- Step-by-step reproduction instructions
- The affected files or code paths
- Any suggested mitigation

You will receive an acknowledgment within 7 days. Please do not disclose the
issue publicly before a fix is coordinated.

## Disclosure timeline

This project follows coordinated disclosure with a **90-day** window:

1. **Day 0** — you report privately to `<SECURITY_CONTACT>`.
2. **Within 7 days** — the maintainers acknowledge and open a tracking item.
3. **Within 90 days** — a fix or mitigation is released (or a deadline
   extension is agreed with you).
4. **After release** — public disclosure is coordinated with you; if no fix is
   available at day 90, details may be published with mitigations.

## Security baseline of this package

- **Capability ceiling.** The maximum capabilities this skill may exercise are
  declared in the `permissions` block of the `SKILL.md` frontmatter. No code
  path, prompt, or script may exceed those declared permissions. Verify per
  the **Compliance Verification** procedure in
  [Section 5 of `references/method-patterns.md`](references/method-patterns.md).
- **No self-exemption in upgrades.** Self-upgrade proposals must never modify
  `tests/` or the `permissions` block of `SKILL.md`; this invariant is
  asserted by `tests/test-method-patterns.py`.
- **Human-gated tier changes.** `scripts/self-scale.ps1` with
  `-Action evaluate` is read-only. Any tier mutation requires explicit human
  approval and is recorded in `.scaling-state.json`.
- **Zero dynamic code execution.** No `eval` / `exec` on user input and no
  `Invoke-Expression` / `iex` / `DownloadString` in any script or prompt
  (`README-FOR-AI.md` §9.4, P25).
- **Zero hardcoded secrets.** Credentials are read exclusively from
  environment variables; configuration records the variable *name*, never
  the value — not even sample keys (`README-FOR-AI.md` §9.4, P20).
- **Zero sensitive-path access.** The `deny` list in the `permissions`
  block proactively excludes all five sensitive locations
  (`~/.ssh/**`, `~/.aws/**`, `~/.config/**`, `/etc/**`, `{WINDOWS_DIR}/**`)
  and must never be trimmed (`README-FOR-AI.md` §9.4 / §9.1).
