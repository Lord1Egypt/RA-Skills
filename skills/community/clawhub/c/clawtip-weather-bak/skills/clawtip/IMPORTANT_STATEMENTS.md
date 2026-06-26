# System Architecture & Security Disclosures

To clarify the scope of the scripts and justify the requested permissions (`credential.read`, `credential.write`, `network.outbound`), the following underlying operations are declared:

1. **Local State Persistence (Credentials):** The `credential.read` and `credential.write` permissions are granted solely to read and write the `u` field inside the local file `configs/config.json`. No environment variables, system keychain entries, or any other credential stores are accessed.

   **Why persist the token?** The `u` (user token) is obtained through a multi-step authorization flow (QR code scan → registration polling → token issuance). Persisting it locally avoids requiring the user to re-authorize on every single payment request, which would be impractical. The token is written once during authorization and read on subsequent payment calls.

   > ⚠️ **Security Advisory — Credential Hardening:**
   >
   > The `u` is stored in local. Operators deploying this skill in security-sensitive environments **must** apply the following protections:
   >
   > 1. **File permissions:** `chmod 600 configs/config.json` — restrict to owner-only read/write.
   > 2. **Directory permissions:** `chmod 700 configs/` — prevent directory listing by other users.
   > 3. **Disk encryption:** On shared or multi-tenant hosts, enable full-disk encryption (e.g., FileVault on macOS, LUKS on Linux).
   >
   > The skill does **not** use OS keychains, environment variables, or any other credential stores — `configs/config.json` is the sole persistence point.

2. **External Network Calls:** The scripts actively call out to external JD endpoints (e.g., `ms.jr.jd.com`) over the network to process transactions, fetch authorization/authentication links, and verify token registration status. This justifies the `network.outbound` permission. No other external domains are contacted.

3. **Bundled Encryption Tooling:** To securely handle payment payloads and credentials, the Python scripts locally invoke a bundled Node.js encryption tool (`scripts/encrypt.js` + `scripts/summer-cryptico-2.0.2.min.js`). **Node.js (`node`) is a required runtime dependency** — it must be present on the host system before the skill is deployed. This requirement is declared in both the `required_binaries` field of the registry metadata above and in this section.

4. **Invocation Policy & Trigger Safeguards:** This skill allows autonomous model invocation (`disable_model_invocation: false`) because it is designed to be called by other skills during payment workflows. To mitigate the risk of mis-triggered payment flows, the following safeguards are enforced:
   - The skill **must only** be triggered when: (a) a third-party skill explicitly initiates a clawtip payment request with valid parameters, (b) the user explicitly requests token creation, (c) the user explicitly requests to view their wallet, or (d) the user explicitly requests a registration status query.
   - The skill **must never** be triggered speculatively, predictively, or based on ambient context without an explicit user or skill request.
   - All payment operations require valid `payTo`, `amount`, and other mandatory parameters — the script will exit with an error if parameters are missing or malformed.
∂