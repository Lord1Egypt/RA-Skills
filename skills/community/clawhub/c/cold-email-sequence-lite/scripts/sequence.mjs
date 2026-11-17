#!/usr/bin/env node
// cold-email-sequence-lite — build a 2-touch outreach skeleton (opener +
// breakup) from ICP input. Full version does the 4-touch 0/3/7/14 cadence.
// Input JSON: {product, icp, painPoints[], cta, senderName, company}.
// Output: JSON {sequence[], checks[], warnings[]}. Exit 0 ok, 1 warn/fail, 2 usage.
import fs from "node:fs";

const SPAMMY = /\b(free|guarantee|no risk|act now|limited time|100%|\$\$\$|winner|buy now|click here|offer expires)\b/gi;
const MAX_SUBJ = 60;

const TOUCHES = [
  { n: 1, day: 0, goal: "open a thread — name the pain, ask a low-friction question" },
  { n: 2, day: 7, goal: "breakup — polite close, leave door open, one-line CTA" },
];

function subjectOptions(input, touch) {
  const icp = (input.icp || "").trim();
  const pain = (input.painPoints || [])[0] || "";
  const first = icp.split(/[,\s]/).filter(Boolean)[0] || "there";
  if (touch.n === 1)
    return [
      pain ? `${pain} at {{company}}?` : `quick question, {{firstName}}`,
      `${first} question`,
    ];
  return [`closing the loop`, `last note — {{firstName}}`];
}

export function build(input) {
  const warnings = [];
  const checks = [];
  const c = (id, status, detail) => checks.push({ id, status, detail });

  for (const k of ["product", "icp"]) {
    c(k, input[k] && String(input[k]).trim() ? "pass" : "fail",
      input[k] ? `${k}: "${input[k]}"` : `missing ${k} — required for copy that lands.`);
  }
  const pains = Array.isArray(input.painPoints) ? input.painPoints.filter(Boolean) : [];
  c("pain-points", pains.length ? "pass" : "warn",
    pains.length ? `${pains.length} pain point(s) supplied.` : "No pain points — emails will be generic; ask for 1-3.");
  c("cta", input.cta ? "pass" : "warn",
    input.cta ? `CTA: "${input.cta}"` : "No CTA — default to a yes/no question.");

  const cta = input.cta || "worth a quick look?";
  const sender = input.senderName || "{{senderName}}";
  const company = input.company || "{{company}}";
  const product = input.product || "{{product}}";
  const pain1 = pains[0] || "{{painPoint}}";

  const sequence = TOUCHES.map((t) => ({
    touch: t.n,
    day: t.day,
    goal: t.goal,
    subjectOptions: subjectOptions(input, t),
    skeleton:
      t.n === 1
        ? `Hi {{firstName}} — noticed ${company} ${pain1 !== "{{painPoint}}" ? `deals with ${pain1}` : "might be hitting {{painPoint}}"}. We built ${product} for ${input.icp || "teams like yours"}. ${cta}`
        : `Closing the loop, {{firstName}} — if ${pain1} isn't on the radar right now, no worries. If it is: ${cta} Either way, good luck. — ${sender}`,
  }));

  for (const t of sequence) {
    const long = t.subjectOptions.filter((s) => s.length > MAX_SUBJ);
    if (long.length) warnings.push(`touch ${t.n}: subject(s) over ${MAX_SUBJ} chars — ${long.join(" | ")}`);
    const spam = t.skeleton.match(SPAMMY);
    if (spam) warnings.push(`touch ${t.n}: spam-trigger words in skeleton — ${spam.join(", ")}`);
  }
  if (pains.length === 0) warnings.push("sequence has {{painPoint}} placeholders — supply painPoints to personalize.");
  if (!input.icp) warnings.push("no ICP — touch 1 stays generic.");

  return { input_echo: { icp: input.icp || null, product: input.product || null }, sequence, checks, warnings };
}

if (process.argv[1]?.endsWith("sequence.mjs")) {
  const arg = process.argv[2];
  if (!arg) {
    console.error("usage: node sequence.mjs <brief.json | ->");
    process.exit(2);
  }
  let raw;
  try {
    raw = arg === "-" ? fs.readFileSync(0, "utf8") : fs.readFileSync(arg, "utf8");
  } catch {
    console.error(`cannot read ${arg}`);
    process.exit(2);
  }
  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    console.error("input is not valid JSON — expected {product, icp, painPoints[], cta, senderName, company}");
    process.exit(2);
  }
  const report = build(input);
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.checks.some((x) => x.status === "fail") || report.warnings.length ? 1 : 0);
}
