---
description: AGNTCY Identity Issuer CLI and Node Backend for managing
  verifiable agent identities, metadata, and badges.
homepage: "https://github.com/agntcy/identity"
metadata:
  openclaw:
    emoji: 🪪
    install:
      - id: go
        kind: go
        label: Install via go install
        module: github.com/agntcy/identity/cmd/issuer
    requires:
      anyBins:
        - identity

      # Required/optional environment variables used by examples and typical IdP-backed issuer flows
      env:
        # Base URL of the AGNTCY Identity issuer / node backend (e.g., http://localhost:9090)
        - ISSUER_URL
        # OAuth/OIDC client ID for the configured Identity Provider (IdP) (only needed for IdP-backed issuer flows)
        - CLIENT_ID
        # OAuth/OIDC client secret for the configured Identity Provider (IdP) (only needed for IdP-backed issuer flows)
        - CLIENT_SECRET

      # Local configuration paths this skill instructs users to create/read.
      # The vault may contain private keys and MUST be treated as sensitive.
      config:
        - skills.entries.agntcy-identity.config.vaultPath
name: agntcy-identity
---

# AGNTCY Identity (Issuer CLI + Node Backend)

Use the `identity` CLI to create, manage, issue, and verify
decentralized agent identities and badges within the AGNTCY ecosystem.

This tool enables:

- Identity creation (Agents, MCP Servers, MASs)
- BYOID onboarding (e.g., Okta-based identities)
- Metadata generation
- Badge issuance & publishing
- Verifiable Credential (VC) verification

---

## Requirements

- Docker Desktop OR
  - Docker Engine v27+
  - Docker Compose v2.35+
- Optional for demo:
  - Okta CLI
  - Ollama CLI

---

## Core Commands

### Vault Management

Manage cryptographic vaults and signing keys:

identity vault connect file -f \~/.identity/vault.json -v "My Vault"
identity vault key generate

---

### Issuer Management

Register and manage issuer configurations:

identity issuer register -o "My Organization" -c
"$CLIENT_ID" -s "$CLIENT_SECRET" -u "\$ISSUER_URL"

---

### Metadata Management

Generate and manage identity metadata:

identity metadata generate -c "$CLIENT_ID" -s "$CLIENT_SECRET" -u
"\$ISSUER_URL"

---

### Badge Issuance

Issue and publish badges (Verifiable Credentials):

identity badge issue mcp -u <http://localhost:9090> -n "My MCP Server"
identity badge publish

---

### Verification

Verify published badges:

identity verify -f vcs.json

---

## Running the Node Backend

Start locally using Docker:

git clone <https://github.com/agntcy/identity.git> cd identity
./deployments/scripts/identity/launch_node.sh

Or:

make start_node

---

## Typical Workflow

1. Install CLI
2. Start Node Backend
3. Create vault + keys
4. Register Issuer
5. Generate metadata
6. Issue badge
7. Publish badge
8. Verify badge

## Security notes (read before providing secrets)

- `~/.identity/vault.json` can contain signing key material and should be treated as a **high-value secret**.
  Use a dedicated test vault for evaluation; do not reuse production keys.
- `CLIENT_SECRET` is a **high-value secret**. Only provide it after you have reviewed the code/binaries you
  will run and you are operating in a controlled environment.
- Avoid pasting secrets into chat, logs, tickets, or issue trackers. Prefer secure secret injection.

---

## Notes

- The CLI binary name is `identity`.
- Public issuer keys are exposed via:
  /v1alpha1/issuer/{common_name}/.well-known/jwks.json
- Published VCs are accessible via:
  /v1alpha1/vc/{metadata_id}/.well-known/vcs.json
- Supports Agents, MCP Servers, and MASs.
- Follows decentralized identity standards (e.g., W3C DIDs).
