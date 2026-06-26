# Security notes for local TOTP workflows

Use this reference only when the task needs storage or operational guidance.

## Preferred order

1. OS-provided secure storage
2. Existing local password manager or authenticator with documented local access
3. Encrypted local file with a user-managed key only as an explicit fallback
4. Plaintext storage: avoid

## Minimum operational rules

- Never commit TOTP seeds, otpauth URIs, backup codes, or screenshots.
- Avoid passing seeds through shell history or long-lived environment variables.
- Redact account labels if they would expose sensitive customer or internal system names.
- Keep code generation explicit and scoped to one alias at a time.
- Support deletion and rotation as first-class actions.
- Prefer system vaults such as Keychain, Credential Manager, Secret Service, or KWallet.

## Publication guidance

- Treat this as a private/internal skill unless legal, security, and product review all say otherwise.
- Public positioning should be about secure local TOTP handling for authorized users, not login automation or bypassing restrictions.
