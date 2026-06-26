# Provider Coverage - Apple Mail (MacOS)

This skill operates on accounts already connected in Mail.app.

## Supported Provider Profiles

| Provider | Typical Mail.app Support | Notes |
|----------|--------------------------|-------|
| Gmail | Full via Mail OAuth | Folder and label mapping can differ from Gmail web view |
| Outlook and Microsoft 365 | Full via Mail OAuth | Shared mailbox and policy setups can vary by tenant |
| iCloud Mail | Full native support | Usually the most predictable folder behavior |
| Yahoo Mail | Full via Mail OAuth | Folder names and spam handling can vary by locale |
| Fastmail | IMAP and SMTP standard | Ensure app password and folder mapping are confirmed |
| Proton Mail | Via Proton Mail Bridge only | Bridge must be installed, running, and unlocked |

## Provider-Specific Safety Notes

- Gmail: Verify target mailbox name before move actions because label semantics differ from strict folder semantics.
- Outlook: Confirm sender identity for shared mailboxes before send.
- Proton via Bridge: If bridge state is uncertain, block send and ask user to verify bridge health first.

## Coverage Rule

Only claim a provider path as operational after a successful read probe and one verified write-safe dry-run.
