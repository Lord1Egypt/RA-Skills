# Akeyless CLI — reference for agents

Canonical docs: [CLI](https://docs.akeyless.io/docs/cli) · [CLI reference](https://docs.akeyless.io/docs/cli-reference) · [Authentication methods](https://docs.akeyless.io/docs/access-and-authentication-methods)

## Install

**macOS (Homebrew)**

```bash
brew install akeylesslabs/tap/akeyless
```

**Linux** — use your distro’s package repo or the official binary download steps from [CLI → Download](https://docs.akeyless.io/docs/cli) (do not guess package names).

Binary name: **`akeyless`**.

## Configure profiles

- Interactive: `akeyless configure`, or first run of any command may prompt setup.
- Profiles directory: `~/.akeyless/profiles/` (TOML per profile). Use `--profile <name>` on commands when needed.
- **API key (example only — user runs with real values outside chat):**

  ```bash
  akeyless configure --profile default \
    --access-id '<Access-ID>' \
    --access-key '<Access-Key>' \
    --access-type access_key
  ```

- Other auth types (`saml`, `oidc`, `azure_ad`, …): see [configure](https://docs.akeyless.io/docs/cli-reference#configure) in the CLI reference.

## SAML authentication (Access ID)

Use the **Access ID** of your SAML **authentication method** in Akeyless (format is often `p-...`). Run **outside** agent chat so IdP login stays in your terminal/browser.

1. **Bind the profile to SAML** (pick profile name, e.g. `default`):

   ```bash
   akeyless configure \
     --profile default \
     --access-id '<YOUR-SAML-ACCESS-ID>' \
     --access-type saml
   ```

2. **Sign in** (opens browser or prints a URL; refreshes CLI temp credentials when JWT expires):

   ```bash
   akeyless auth --access-type saml --access-id '<YOUR-SAML-ACCESS-ID>' --profile default
   ```

3. **Headless / SSH** — use a link on another device:

   ```bash
   akeyless auth --access-type saml --access-id '<YOUR-SAML-ACCESS-ID>' --profile default --use-remote-browser
   ```

4. **Verify:** `akeyless list-items --minimal-view --profile default` (or any read your role allows).

Docs: [Auth with SAML](https://docs.akeyless.io/docs/auth-with-saml) · [CLI reference – Authentication](https://docs.akeyless.io/docs/cli-ref-auth)

## Gateway and SaaS routing

- Default SaaS API host is often **`vault.akeyless.io`**; **EU** and other regions differ—use the tenant URL your org documents.
- To force traffic via an **Akeyless Gateway**:

  ```bash
  export AKEYLESS_GATEWAY_URL='https://Your_GW_HOST:8000/api/v1'
  ```

- Self-signed gateway TLS: **`AKEYLESS_TRUSTED_TLS_CERTIFICATE_FILE`** pointing to a PEM file (see official CLI troubleshooting).

## `list-items` (common read-only check)

```bash
akeyless list-items --minimal-view
akeyless list-items --path '/your/folder' --minimal-view
akeyless list-items --filter 'substring' --minimal-view
akeyless list-items -t static-secret --minimal-view
akeyless list-items --json
```

Flags and types: [list-items](https://docs.akeyless.io/docs/cli-reference#list-items). Use `--auto-pagination=enabled` for large inventories.

Help: `akeyless list-items -h`

## Precedence (highest first)

1. CLI flags  
2. Environment variables  
3. Profile file defaults  

## Safety

- Never commit `~/.akeyless/` or paste profile contents into LLM sessions.
- **Access denied** usually means **role**, **path prefix**, or **wrong gateway/tenant**—not “wrong password” alone.
- When summarizing `--json` output, omit or redact fields that can contain secret material.
