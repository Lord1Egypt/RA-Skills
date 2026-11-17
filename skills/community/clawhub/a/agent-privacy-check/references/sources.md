# Source Notes

This Skill translates public OWASP guidance into a smaller, user-facing
workflow. It does not reproduce OWASP's taxonomy, assign OWASP scores, or
claim certification.

## OWASP references

- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
  informs the checks for least privilege, untrusted input, data exfiltration,
  memory and context security, human approval, output validation, monitoring,
  data protection, and adversarial testing.
- [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
  informs the checks for malicious or compromised Skills, supply-chain
  provenance, over-privilege, insecure metadata, external instructions, weak
  isolation, update drift, scanning, governance, and cross-platform reuse.
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
  is a related agent-level reference for goal hijacking, identity and
  privilege abuse, code execution, excessive autonomy, and observability.
  Use the current OWASP page or linked publication when a user asks for a
  broader agentic-application mapping.

As checked on 2026-09-09, the official Agentic Skills Top 10 project page
describes its v1 material as Public review (v1). Treat it as evolving guidance, not
a stable standard or certification, and recheck the live page before making a
version-specific claim.

## Adaptation notes

The Secret Source, External Sink, and Untrusted Content wording is a deliberate
plain-language data-flow model for this Skill. It is inspired by the combined
risk of private-data access, untrusted instructions, and external
communication, but it is not an OWASP category or a substitute for a
platform-specific threat model.

The Low, Medium, High, and Critical rubric is also local to this Skill. It
prioritizes a user's next safe action; it does not replace formal risk
assessment, incident response, privacy law analysis, or a vendor's security
documentation.

Prefer the live OWASP pages above over copied excerpts. Record the date and
version when a report relies on a specific publication, and say when an OWASP
mapping is an interpretation.
