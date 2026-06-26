/**
 * Clinical Tempo / ClawHub — OpenClaw bootstrap hook
 * Injects a reminder to load llm-full.txt + CLAWHUB.md before deep work.
 */

const REMINDER_CONTENT = `
## Clinical Tempo context (ClawHub skill)

**Published skill:** https://clawhub.ai/arunnadarasa/clinicaltempo

**OpenClaw (optional):** \`openclaw plugins install @anyway-sh/anyway-openclaw\`

**Full repo bundle:** \`public/llm-full.txt\` — regenerate: \`npm run build:llm\` (also runs before \`npm run build\`). Running app: **\`/llm-full.txt\`**.

**Tribal debugging:** \`CLAWHUB.md\` (successes, failures, MPP, port **8787**, purl, AgentMail).

**MPPScan discovery:** \`GET /openapi.json\` — validate: \`npm run discovery\` (server on 8787).

**API smoke (Express on 8787):** \`GET /api/dance-extras/live\` → JSON with \`flowKeys\`. If HTML/404 → wrong server or stale \`node\` process.

**Hub routes:** \`src/hubRoutes.ts\` · **Server:** \`server/index.js\`

**EVVM (optional depth):** \`docs/EVVM_TEMPO.md\` · upstream **\`https://www.evvm.info/llms-full.txt\`** (large; attach when needed).

**Secrets:** never paste real \`.env\` values — use \`.env.example\` names only.

After non-obvious fixes, consider a short line under **Successes** or **Failures** in \`CLAWHUB.md\`.
`.trim();

/** @param {unknown} event */
const handler = async (event) => {
  if (!event || typeof event !== 'object') {
    return;
  }

  const e = /** @type {{ type?: string; action?: string; sessionKey?: string; context?: { bootstrapFiles?: unknown } }} */ (
    event
  );

  if (e.type !== 'agent' || e.action !== 'bootstrap') {
    return;
  }

  const sessionKey = e.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  const ctx = e.context;
  if (!ctx || typeof ctx !== 'object') {
    return;
  }

  const files = ctx.bootstrapFiles;
  if (Array.isArray(files)) {
    files.push({
      path: 'CLINICAL_TEMPO_CONTEXT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
