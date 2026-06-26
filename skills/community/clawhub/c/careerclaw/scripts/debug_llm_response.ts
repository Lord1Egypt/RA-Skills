/**
 * scripts/debug_llm_response.ts — Shows raw LLM output before parseResponse().
 * Run: npx tsx --env-file=.env scripts/debug_llm_response.ts
 */

import { existsSync, readFileSync } from "node:fs";
import {
  PRO_KEY,
  RESUME_TXT_PATH,
  PROFILE_PATH,
  LLM_OPENAI_KEY,
  LLM_ANTHROPIC_KEY,
  LLM_API_KEY,
  LLM_CHAIN,
  HTTP_TIMEOUT_MS,
} from "../src/config.js";
import { buildResumeIntelligence } from "../src/resume-intel.js";
import { SYSTEM_PROMPT } from "../src/llm-enhance.js";

console.log("\n=== Raw LLM Response Debug ===\n");

type OpenAITransport = "chat" | "responses";

function defaultOpenAITransport(model: string): OpenAITransport {
  const normalized = model.toLowerCase();
  if (normalized.startsWith("gpt-4o")) return "chat";
  return "responses";
}

function extractOpenAIText(data: unknown, transport: OpenAITransport): string {
  if (transport === "chat") {
    const chatData = data as {
      choices?: Array<{
        message?: {
          content?: string | Array<{ type: string; text?: string }>;
        };
      }>;
    };

    const content = chatData.choices?.[0]?.message?.content;

    if (typeof content === "string") {
      return content;
    }

    if (Array.isArray(content)) {
      return content
        .filter((part) => part?.type === "text" && typeof part.text === "string")
        .map((part) => part.text ?? "")
        .join("")
        .trim();
    }

    return "";
  }

  const responsesData = data as {
    output_text?: string;
    output?: Array<{
      content?: Array<{ type?: string; text?: string }>;
    }>;
  };

  if (typeof responsesData.output_text === "string") {
    return responsesData.output_text;
  }

  return (responsesData.output ?? [])
    .flatMap((item) => item.content ?? [])
    .filter((part) => part?.type === "output_text" && typeof part.text === "string")
    .map((part) => part.text ?? "")
    .join("")
    .trim();
}

const profile = JSON.parse(readFileSync(PROFILE_PATH, "utf8"));
const resumeText = existsSync(RESUME_TXT_PATH)
  ? readFileSync(RESUME_TXT_PATH, "utf8")
  : null;

const resumeIntel = buildResumeIntelligence({
  resume_summary: profile.resume_summary ?? "",
  skills: profile.skills ?? [],
  target_roles: profile.target_roles ?? [],
  ...(resumeText ? { resume_text: resumeText } : {}),
});

// Use a real job from the last briefing result for the prompt test
const testJob = {
  title: "Senior Full-Stack Engineer",
  company: "Instinct Science",
  experience_years: null as number | null,
};

const experienceClause = profile.experience_years != null
  ? `${profile.experience_years}+ years`
  : "extensive experience";

const strengths = resumeIntel.impact_signals.slice(0, 12).join(", ") || "software engineering";
const gaps = ["elixir", "postgresql", "emr"].slice(0, 6).join(", ");

const prompt = [
  `Write a cold outreach email from a job candidate to a hiring team.`,
  ``,
  `Role: ${testJob.title}`,
  `Company: ${testJob.company}`,
  `Candidate experience: ${experienceClause}`,
  `Candidate's strongest signals: ${strengths}`,
  `Gap keywords (acknowledge briefly as growth areas — do not apologise, do not skip): ${gaps}`,
  ``,
  `Output format (follow exactly):`,
  `- First line: subject line prefixed with "Subject: "`,
  `- One blank line`,
  `- Email body: maximum 250 words — count before finishing and cut if over`,
  ``,
  `Writing requirements:`,
  `- Opening: "Hi ${testJob.company} team,"`,
  `- Bridge Sentence method: for each strength signal, identify the matching requirement`,
  `  in this role and write one concrete sentence connecting them.`,
  `  Example: "Because I [did X], I can solve your need for [Y] from day one."`,
  `  Every paragraph must contain at least one Bridge Sentence.`,
  `- First paragraph: connect the candidate's strongest 1–2 signals directly to what`,
  `  this specific role needs — make the match feel specific and inevitable`,
  `- Second paragraph: show how the candidate's background maps to a real challenge`,
  `  this company faces — be concrete, not generic`,
  `- If gap keywords are provided, one sentence frames them as active growth, not deficiency`,
  `- Close with a single, low-friction call to action`,
  `- Closing: "Best regards," on its own line, then "[Your Name]" on the next`,
  `- Plain text only — no markdown, no bullet points`,
  `- Do NOT invent specific projects, metrics, or company details`,
  `- Do NOT include any placeholder other than [Your Name]`,
].filter(Boolean).join("\n");

console.log("Prompt sent to LLM:");
console.log("─".repeat(60));
console.log(prompt);
console.log("─".repeat(60));

// Resolve provider
const openaiKey = LLM_OPENAI_KEY ?? LLM_API_KEY;
const anthropicKey = LLM_ANTHROPIC_KEY ?? LLM_API_KEY;

// Parse chain to find first usable candidate
const chain = LLM_CHAIN.split(",").map(e => e.trim()).filter(Boolean);
console.log(`\nLLM_CHAIN: ${LLM_CHAIN}`);

let provider: "anthropic" | "openai" | null = null;
let model = "";
let apiKey = "";

for (const entry of chain) {
  const slash = entry.indexOf("/");
  if (slash === -1) continue;
  const p = entry.slice(0, slash).toLowerCase();
  const m = entry.slice(slash + 1);
  if (p === "anthropic" && anthropicKey) {
    provider = "anthropic"; model = m; apiKey = anthropicKey; break;
  }
  if (p === "openai" && openaiKey) {
    provider = "openai"; model = m; apiKey = openaiKey; break;
  }
}

if (!provider) {
  console.log("❌ No usable provider found in chain.");
  process.exit(1);
}

console.log(`\nUsing: ${provider} / ${model}`);
console.log("Calling LLM…\n");

try {
  let res: Response;
  let openAITransport: OpenAITransport | null = null;

  if (provider === "anthropic") {
    res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model,
        max_tokens: 512,
        system: SYSTEM_PROMPT,
        messages: [{ role: "user", content: prompt }],
      }),
      signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
    });
  } else {
    openAITransport = defaultOpenAITransport(model);

    if (openAITransport === "responses") {
      res = await fetch("https://api.openai.com/v1/responses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model,
          max_output_tokens: 512,
          temperature: 0.7,
          input: [
            {
              role: "system",
              content: [{ type: "input_text", text: SYSTEM_PROMPT }],
            },
            {
              role: "user",
              content: [{ type: "input_text", text: prompt }],
            },
          ],
        }),
        signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
      });
    } else {
      res = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model,
          max_tokens: 512,
          temperature: 0.7,
          messages: [
            { role: "system", content: SYSTEM_PROMPT },
            { role: "user", content: prompt },
          ],
        }),
        signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
      });
    }
  }

  const raw = await res.text();
  console.log(`HTTP status: ${res.status}`);

  if (!res.ok) {
    console.log(`❌ Error response:\n${raw}`);
    process.exit(1);
  }

  const data = JSON.parse(raw);
  const text = provider === "anthropic"
    ? (data.content?.find((b: { type: string }) => b.type === "text")?.text ?? "")
    : extractOpenAIText(data, openAITransport ?? "chat");

  console.log("Raw LLM text output:");
  console.log("─".repeat(60));
  console.log(text);
  console.log("─".repeat(60));

  // Manual parse check
  const lines = text.trim().split(/\r?\n/);
  const subjectIdx = lines.findIndex((l: string) =>
    l.trimStart().toLowerCase().startsWith("subject:")
  );
  console.log(`\nParse check:`);
  console.log(`  Subject line found at index: ${subjectIdx}`);
  if (subjectIdx !== -1) {
    const subject = lines[subjectIdx].replace(/^subject:\s*/i, "").trim();
    console.log(`  Subject: "${subject}"`);
    const company = testJob.company.toLowerCase().slice(0, 6);
    console.log(`  Company check string (first 6): "${company}"`);
    console.log(`  Company appears in body: ${text.toLowerCase().includes(company)}`);
  }

} catch (err) {
  console.log(`❌ Fetch threw: ${String(err)}`);
}
