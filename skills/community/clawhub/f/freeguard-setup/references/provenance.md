# FreeGuard Setup Provenance Notes

Use this reference only when the user, a reviewer, or a registry moderator asks for provenance or security context.

## Official Sources

- Product homepage: `https://freeguardvpn.com`
- Official Homebrew formula: `planetlinkinc/tap/freeguardvpn`
- Homebrew tap repository: `https://github.com/planetlinkinc/homebrew-tap`
- Official binary releases: `https://github.com/planetlinkinc/freeguard-releases/releases`
- Published checksums: each GitHub Release includes `checksums.txt`

## Skill Package Scope

This ClawHub package is instruction-only. It contains no executable installer, shell script, PowerShell script, binary payload, background process, or credential material.

The skill expects the user to install the official `freeguard` CLI through Homebrew, or to manually download a GitHub Release asset and verify it against the release checksum before placing it on PATH.

## Data And Credential Handling

The skill itself does not collect, store, upload, or transmit credentials. Login, subscription, connection, and local storage behavior are handled by the `freeguard` CLI and FreeGuard service endpoints over HTTPS.

Users should enter email verification codes, subscription URLs, and access tokens directly into the CLI or official browser flow whenever possible.

## Review Notes

For ClawHub moderation review, verify that the published skill bundle contains only:

- `SKILL.md`
- `references/provenance.md`

The package intentionally excludes repository documentation, installer scripts, CI workflows, release tooling, and application source code.
