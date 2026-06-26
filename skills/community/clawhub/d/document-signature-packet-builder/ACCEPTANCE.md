# Acceptance Checks: Document Signature Packet Builder

## Metadata

- `skill.json` has version `1.0.0`.
- `skill.json` has license `MIT-0`.
- `skill.json` has language `en`.
- `skill.json` has `hasExecutableCode: false`.
- The skill directory contains exactly `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.

## Functional Checks

- Produces a sign-here and logistics checklist for a document packet.
- Tracks signatures, dates, initials, witnesses, notarization, attachments, copies, identity items, deadlines, and submission method.
- Groups checklist items by document and signer when applicable.
- Builds a clear list of questions to confirm with the issuer.
- Includes a packet assembly order for signing, copying, attaching, and submitting.

## Boundary Checks

- Does not provide legal interpretation or advice.
- Does not tell the user whether to sign.
- Does not state that a packet is legally valid or acceptable.
- Does not invent issuer requirements, deadlines, witness rules, notary rules, or accepted formats.
- Directs the user to confirm rules with the issuer or a qualified professional.
- Does not require external services, credentials, scripts, package files, or executable code.

## Example Pass Scenario

User has a benefits form, an authorization form, and a notarized affidavit due next week. The skill returns a packet summary, per-document sign-here checklist, logistics checklist, issuer-confirmation questions, assembly order, and boundary note without interpreting the forms.

## Install-First Success Path

- **Input:** User says "I have an employee benefits enrollment packet with 4 forms: health insurance election, dependent verification, beneficiary designation, and direct deposit authorization. The HR deadline is Friday. Some need witness signatures and one needs notarization. Walk me through a sign-here checklist."
- **Steps:** Skill inventories every document in the packet → identifies each visible signature, date, initial, witness, notary, attachment, copy, payment, and submission requirement from provided instructions → groups actions by signer and by document → adds logistics items (identification, appointment timing, copies, delivery method, deadline, proof of submission) → creates a confirmation list for unclear or issuer-specific rules → provides a final packet assembly order → appends a boundary note stating this is a sign-here checklist only, not legal interpretation.
- **Output:** A document signature packet builder with packet summary, per-document sign-here checklist, logistics checklist, issuer-confirmation questions, packet assembly order, and boundary note — all logistics-focused without legal interpretation.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — does not interpret legal meaning, rights, obligations, penalties, waivers, or enforceability; does not advise whether to sign; does not infer hidden requirements; marks uncertain items as "confirm with issuer"; respects privacy by avoiding full identity numbers or sensitive document contents.
