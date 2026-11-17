# Setup and installation

Requires Node 22+, an installed/authenticated bw CLI and a trusted installed Camofox runtime. No npm dependencies or install step. Existing valid BW_SESSION works on any OS; do not pass it as an argument, invocation JSON or file. A locked vault requires an explicitly configured unlock provider: currently optional macOS Keychain only. Without that provider the helper returns UNLOCK_PROVIDER_MISSING; authenticate/unlock out of band, never send secrets to the agent.

## Local profile (outside skill)

Copy config.example.json to ~/.config/camofox-vault-login/config.json and explicitly set expectedVaultServerUrl and expectedVaultEmail to your intended bw identity. CAMOFOX_VAULT_CONFIG overrides the absolute profile path; otherwise XDG_CONFIG_HOME overrides ~/.config. This profile is trusted, nonsecret and never emitted; never store passwords, seeds or sessions there.

Supported string keys (unknown keys rejected):
- expectedVaultServerUrl, expectedVaultEmail: required; exact comparison with bw status, before unlock or item retrieval. No automatic account trust or account/server switching.
- keychainService, keychainAccount: optional paired keys for an existing macOS generic password. No Keychain writes. Do not configure on other OSes.
- camofoxRuntimePath: optional absolute trusted installed package root; defaults to OPENCLAW_STATE_DIR/extensions/camofox-browser, or ~/.openclaw/extensions/camofox-browser.
- openclawConfigPath: optional absolute existing OpenClaw config; defaults to OPENCLAW_STATE_DIR/openclaw.json, or ~/.openclaw/openclaw.json.

HOME is used instead of fixed machine paths. Runtime/profile settings cannot be supplied through invocation JSON. userId and sessionKey are mandatory per call, not shared profile fields.

## Supported installed contract

Supported build: @askjo/camofox-browser 1.18.1 from jo-inc, not the similarly named redf0x1 repository. The trusted root must contain package.json identifying that exact name/version, mcp/lib/tool-contracts.mjs exporting runTool and lib/config.js exporting loadConfig. Existing OpenClaw plugins.entries.camofox-browser.config supplies url or port; only loopback HTTP(S) endpoints are accepted. Unsupported versions/layouts fail closed (missing files can produce sanitized OPERATION_FAILED). Manifest checks are compatibility gates, not package authenticity verification: installation provenance remains the operator's responsibility. No services/config/plugins are changed.

## Nonsecret invocation examples

Run from any directory (replace SKILL_DIR with installed skill path). Replace caller placeholders with the current context, never a fixed shared identity.


Discovery:

    printf '%s' '{"action":"list","origin":"https://login.example.invalid","userId":"AGENT","sessionKey":"agent:AGENT:CONTEXT"}' | node SKILL_DIR/scripts/cli.mjs

Dry-run after observing actual inputs and choosing the synthetic-placeholder UUID:

    printf '%s' '{"action":"dry-run","origin":"https://login.example.invalid","itemId":"11111111-1111-1111-1111-111111111111","tabId":"OBSERVED_TAB","fields":{"username":"#observed-user","password":"#observed-password"},"userId":"AGENT","sessionKey":"agent:AGENT:CONTEXT"}' | node SKILL_DIR/scripts/cli.mjs

Change action to fill only after validation/review. TOTP uses a separate challenge and fields {"totp":"#observed-otp"}. Never place secret values in commands, selectors, URLs, request JSON or files.

## Canonical shared installation

Install the reviewed camofox-vault-login directory using `openclaw skills install /absolute/path/to/camofox-vault-login --global`; let the installer enforce its current security policy. The shared managed directory (~/.openclaw/skills/camofox-vault-login) is the canonical operational copy. Verify discovery separately in every caller agent; never assume cached discovery updated. Keep the personal profile outside the skill. Archive any older same-named agent-specific instructions only after the shared copy is verified.

Workshop is optional, not required. If its write scanner rejects a required subprocess helper, do not bypass that refusal by direct file copies or encoding. A Workshop-owned copy plus shared symlink is viable only where the supported Workshop approval policy allows every bundled resource.

For a portable export, include only SKILL.md, scripts/ and references/. Exclude installer-generated .openclaw/ provenance, archives, local profiles and repository history; provenance may record private local installation paths.

Standalone: copy this whole directory into your skill manager's supported skill directory; keep relative layout intact and configure the external profile. Do not install the historical repository-root helpers as a second implementation.

Validation: cd SKILL_DIR/scripts && npm run check && npm test. Packaging tests include subprocess stdin and relocation. ClawHub publication requires an explicit publisher request, validation and privacy review. All ClawHub skills use MIT-0: free use, modification and redistribution without attribution. Publish only this sanitized package, never repository history or an installed copy containing private provenance. Release version: 0.1.0.
