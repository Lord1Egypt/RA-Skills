const REMINDER_CONTENT = `
## Contact Discovery Reminder

Use contact discovery when a task needs:
- a public email for a person or company,
- a support, press, team, or contact page,
- a company email-format clue,
- a public contact path before outreach.

Workflow:
- preflight: confirm \`PRISMFY_API_KEY\` is available
- resolve identity first
- use \`bash contact-find.sh --person "Name" --company "Company" --query-family all\` or \`bash contact-find.sh --company "Company" --query-family company\`
- return a short verdict in chat first
- never guess a private email from a pattern clue

Guardrails:
- only treat an email as found if it appears in public evidence
- do not claim deliverability
- treat pattern pages and third-party bio pages as pattern clues or ambiguous unless they show an explicit public contact method
- if evidence is weak, prefer \`company_email_pattern_found\`, \`not_found\`, or \`ambiguous\`
`.trim();

const handler = async (event) => {
  if (!event || typeof event !== "object") return;
  if (event.type !== "agent" || event.action !== "bootstrap") return;
  if (!event.context || typeof event.context !== "object") return;

  if (!Array.isArray(event.context.bootstrapFiles)) event.context.bootstrapFiles = [];
  event.context.bootstrapFiles.push({
    path: "CONTACT_DISCOVERY_REMINDER.md",
    content: REMINDER_CONTENT,
    virtual: true,
  });
};

module.exports = handler;
module.exports.default = handler;
