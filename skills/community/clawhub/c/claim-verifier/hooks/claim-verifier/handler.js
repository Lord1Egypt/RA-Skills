/**
 * Claim Verifier Hook for OpenClaw
 *
 * Injects a lightweight reminder during agent bootstrap for fact-checking drafts
 * that contain external claims.
 */

const REMINDER_CONTENT = `
## Claim Verifier Reminder

Use claim verification when a draft contains external factual statements and the
text is being prepared for publication or sending.

Workflow:
- extract factual claims from the draft
- verify each claim with reliable sources
- assign status: verified | weak | conflicting | not_found
- reply in chat with a short verdict first
- list only the claims that need correction or caution
- produce claim_verification_report.json only if the user asked for a file or a structured export is clearly useful

Guardrails:
- do not mark verified without evidence
- do not fabricate citations
- if evidence conflicts, keep non-verified status and explain why
`.trim();

const handler = async (event) => {
  if (!event || typeof event !== "object") return;
  if (event.type !== "agent" || event.action !== "bootstrap") return;
  if (!event.context || typeof event.context !== "object") return;

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: "CLAIM_VERIFIER_REMINDER.md",
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
