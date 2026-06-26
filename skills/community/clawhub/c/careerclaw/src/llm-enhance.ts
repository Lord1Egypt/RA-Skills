/**
 * llm-enhance.ts — LLM-powered outreach draft enhancement (Pro tier).
 *
 * `enhanceDraft()` replaces the deterministic baseline draft with a
 * personalised LLM-generated version when a valid Pro key is active.
 *
 * Design principles:
 *   - Silent fallback: any failure returns the original draft unchanged.
 *     The function never throws.
 *   - Privacy-first: only extracted keyword signals are sent to the LLM.
 *     Raw resume text is NEVER included in the prompt.
 *   - Failover chain: providers are tried left-to-right from LLM_CHAIN.
 *     Each candidate is retried up to LLM_MAX_RETRIES times before moving
 *     to the next. A circuit breaker opens after LLM_CIRCUIT_BREAKER_FAILS
 *     consecutive failures across the whole chain.
 *   - Testable: the fetch function is injectable so tests run fully offline.
 */

import type { NormalizedJob, UserProfile, OutreachDraft, ResumeIntelligence } from "./models.js";
import {
  LLM_ANTHROPIC_KEY,
  LLM_OPENAI_KEY,
  LLM_API_KEY,
  LLM_CHAIN,
  LLM_MAX_RETRIES,
  LLM_CIRCUIT_BREAKER_FAILS,
  HTTP_TIMEOUT_MS,
} from "./config.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type OpenAITransport = "chat" | "responses";

export interface ChainCandidate {
  provider: "anthropic" | "openai";
  model: string;
  apiKey: string;
  transport?: OpenAITransport;
}

export interface EnhanceOptions {
  /**
   * Injectable fetch — defaults to global fetch.
   * Pass a stub in tests to avoid live network calls.
   */
  fetchFn?: typeof fetch;
  /**
   * Override the resolved provider chain — for testing only.
   * Bypasses env-var key resolution so tests can run without real credentials.
   */
  _chainOverride?: ChainCandidate[];
  /**
   * Output mode.
   *
   * "draft"        — (default, Free tier) Short outreach email, max 250 words.
   *                  Produced by the deterministic template on Free; LLM-enhanced on Pro.
   * "cover_letter" — (Pro only, future) Tailored cover letter, max 300 words.
   *                  Every sentence connects the candidate to this specific role.
   *                  Zero generic filler. Requires active Pro license.
   *
   * TODO: Phase X — implement cover_letter mode. Stub is in buildPrompt().
   */
  mode?: "draft" | "cover_letter";
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Attempt to replace `draft` with an LLM-enhanced version.
 *
 * @param job          - The job being applied to
 * @param profile      - User profile (experience_years used in prompt)
 * @param resumeIntel  - Section-aware keyword signals (impact_signals used)
 * @param draft        - Deterministic baseline to fall back to on failure
 * @param gapKeywords  - Keywords from the job not present in the profile
 * @param options      - Injectable fetch for testing
 * @returns Enhanced draft with llm_enhanced=true, or original draft on failure
 */
export async function enhanceDraft(
  job: NormalizedJob,
  profile: UserProfile,
  resumeIntel: ResumeIntelligence,
  draft: OutreachDraft,
  gapKeywords: string[] = [],
  options: EnhanceOptions = {}
): Promise<OutreachDraft> {
  const fetchFn = options.fetchFn ?? fetch;
  const mode = options.mode ?? "draft";
  const chain = options._chainOverride ?? buildChain();
  if (chain.length === 0) {
    return draft; // No configured providers — degrade silently
  }

  let consecutiveFails = 0;

  for (const candidate of chain) {
    if (consecutiveFails >= LLM_CIRCUIT_BREAKER_FAILS) {
      break; // Circuit breaker open
    }

    for (let attempt = 0; attempt < LLM_MAX_RETRIES; attempt++) {
      if (consecutiveFails >= LLM_CIRCUIT_BREAKER_FAILS) break;

      try {
        const prompt = buildPrompt(job, profile, resumeIntel, gapKeywords, mode);
        const text = await callProvider(candidate, prompt, fetchFn);
        const parsed = parseResponse(text, job);
        if (parsed) {
          return { ...draft, subject: parsed.subject, body: parsed.body, llm_enhanced: true };
        }
        // Unparseable response counts as a soft failure — try next attempt
        consecutiveFails++;
      } catch {
        consecutiveFails++;
      }
    }
  }

  return draft; // All candidates exhausted or circuit open — fall back
}

// ---------------------------------------------------------------------------
// Chain construction
// ---------------------------------------------------------------------------

/**
 * Parse LLM_CHAIN into candidates with resolved API keys.
 * Candidates without a usable key are silently skipped.
 *
 * Supported chain formats:
 *   "anthropic/claude-haiku-4-5-20251001,openai/gpt-4o-mini"
 *   "openai:chat/gpt-4o-mini,openai:responses/gpt-5.2"
 */
function buildChain(): ChainCandidate[] {
  return LLM_CHAIN.split(",")
    .map((entry) => entry.trim())
    .filter(Boolean)
    .flatMap((entry): ChainCandidate[] => {
      const slash = entry.indexOf("/");
      if (slash === -1) return [];

      const left = entry.slice(0, slash).toLowerCase();
      const model = entry.slice(slash + 1).trim();
      if (!model) return [];

      let provider: "anthropic" | "openai" | null = null;
      let transport: OpenAITransport | undefined;

      if (left === "anthropic") {
        provider = "anthropic";
      } else if (left === "openai") {
        provider = "openai";
      } else if (left === "openai:chat") {
        provider = "openai";
        transport = "chat";
      } else if (left === "openai:responses") {
        provider = "openai";
        transport = "responses";
      } else {
        return [];
      }

      const apiKey = resolveKey(provider);
      if (!apiKey) return []; // No key for this provider — skip

      return [{ provider, model, apiKey, ...(transport !== undefined ? { transport } : {}) }];
    });
}

function resolveKey(provider: "anthropic" | "openai"): string | undefined {
  if (provider === "anthropic") return LLM_ANTHROPIC_KEY ?? LLM_API_KEY;
  if (provider === "openai")    return LLM_OPENAI_KEY    ?? LLM_API_KEY;
}

// ---------------------------------------------------------------------------
// Prompt construction
// ---------------------------------------------------------------------------

/**
 * System prompt — establishes the LLM as a senior career writer.
 * Sent as the `system` field (Anthropic) or system role message (OpenAI).
 */
const SYSTEM_PROMPT = `You are a senior career consultant and professional writer with 15 years of experience placing candidates at top-tier companies. You write outreach emails and cover letters that are specific, compelling, and human — never generic.

Your core method — the Bridge Sentence:
For every strength signal the candidate has, identify the corresponding requirement in the role and connect them with a concrete, specific sentence. Example: "Because I architected the data pipeline at [Company], I can solve your need for reliable real-time ingestion from day one." Every paragraph must contain at least one Bridge Sentence.

Your writing principles:
- Every sentence earns its place. No filler, no padding, no throat-clearing.
- Map the candidate's actual experience to this specific role's needs — not to "the industry."
- When the candidate has a gap, frame it as genuine motivation to grow, not as an apology.
- Write like a thoughtful senior professional, not a cover letter generator.
- Strict word limits: 250 words maximum for outreach emails, 300 words for cover letters.
- Count words before finishing. If over the limit, cut the weakest sentence, not the strongest.
- Output your final word count at the very bottom of the response in brackets.

Banned phrases — never use these under any circumstances:
"I am writing to express my interest", "I am excited to apply", "I would be a great fit", "passion for", "passionate about", "leverage my skills", "leverage my experience", "dynamic team", "fast-paced environment", "detail-oriented", "results-driven", "team player", "go-getter", "hard worker", "strong work ethic", "I am a quick learner", "Enclosed please find", "Please find attached", "I am writing to", "I look forward to hearing from you", "Thank you for your consideration", "I believe I would", "synergy", "proactive", "self-starter".`;

/**
 * Build the LLM prompt for the requested output mode.
 *
 * Only sends keyword signals — never raw resume text.
 * Uses impact_signals (skills + summary section, weight >= 0.8) as the
 * candidate's strength summary, and gap_keywords for strategic gap framing.
 *
 * mode "draft"        — outreach email, max 250 words (Free tier baseline, LLM-enhanced on Pro)
 * mode "cover_letter" — tailored cover letter, max 300 words, zero filler (Pro only, future)
 */
function buildPrompt(
  job: NormalizedJob,
  profile: UserProfile,
  resumeIntel: ResumeIntelligence,
  gapKeywords: string[] = [],
  mode: "draft" | "cover_letter" = "draft"
): string {
  const experienceClause =
    profile.experience_years != null
      ? `${profile.experience_years}+ years`
      : "extensive experience";

  // Cap signal lists to keep token usage low (Haiku: ~0.25¢/1K tokens)
  const strengths = resumeIntel.impact_signals.slice(0, 12).join(", ") || "software engineering";
  const gaps = gapKeywords.slice(0, 6).join(", ");

  const gapsInstruction = gaps
    ? `Gap keywords (acknowledge briefly as growth areas — do not apologise, do not skip): ${gaps}`
    : "";

  if (mode === "cover_letter") {
    // TODO: Phase X — cover_letter mode (Pro only).
    // Spec: under 300 words, zero generic filler, every sentence connects
    // the candidate to this specific role. Paragraph structure:
    //   1. Why this company/role specifically (1–2 sentences)
    //   2. Strongest signal mapped to the role's core need (2–3 sentences)
    //   3. Gap acknowledgement as motivation (1 sentence, only if gaps exist)
    //   4. Clear call to action (1 sentence)
    // For now fall through to draft mode until the feature ships.
  }

  // Draft mode — LLM-enhanced outreach email
  return [
    `Write a cold outreach email from a job candidate to a hiring team.`,
    ``,
    `Role: ${job.title}`,
    `Company: ${job.company}`,
    `Candidate experience: ${experienceClause}`,
    `Candidate's strongest signals: ${strengths}`,
    gapsInstruction,
    ``,
    `Output format (follow exactly):`,
    `- First line: subject line prefixed with "Subject: "`,
    `- One blank line`,
    `- Email body: maximum 250 words — count before finishing and cut if over`,
    ``,
    `Writing requirements:`,
    `- Opening: "Hi ${job.company} team,"`,
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
  ]
    .filter(Boolean)
    .join("\n");
}

// ---------------------------------------------------------------------------
// Provider API calls
// ---------------------------------------------------------------------------

async function callProvider(
  candidate: ChainCandidate,
  prompt: string,
  fetchFn: typeof fetch
): Promise<string> {
  if (candidate.provider === "anthropic") {
    return callAnthropic(candidate.apiKey, candidate.model, prompt, fetchFn);
  }
  return callOpenAI(candidate.apiKey, candidate.model, prompt, fetchFn, candidate.transport);
}

/** Exported for testing — same reference used by both API callers. */
export { SYSTEM_PROMPT };

async function callAnthropic(
  apiKey: string,
  model: string,
  prompt: string,
  fetchFn: typeof fetch
): Promise<string> {
  const res = await fetchFn("https://api.anthropic.com/v1/messages", {
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

  if (!res.ok) {
    const body = await res.text().catch(() => "(no body)");
    throw new Error(`Anthropic HTTP ${res.status}: ${body.slice(0, 200)}`);
  }

  const data = await res.json() as { content: Array<{ type: string; text: string }> };
  const text = data.content?.find((b) => b.type === "text")?.text ?? "";
  if (!text) throw new Error("Anthropic: empty response content");
  return text;
}

function defaultOpenAITransport(model: string): OpenAITransport {
  const normalized = model.toLowerCase();

  if (normalized.startsWith("gpt-4o")) return "chat";
  return "responses";
}

async function callOpenAI(
  apiKey: string,
  model: string,
  prompt: string,
  fetchFn: typeof fetch,
  transport?: OpenAITransport
): Promise<string> {
  const resolvedTransport = transport ?? defaultOpenAITransport(model);

  if (resolvedTransport === "responses") {
    return callOpenAIResponses(apiKey, model, prompt, fetchFn);
  }

  return callOpenAIChat(apiKey, model, prompt, fetchFn);
}

async function callOpenAIChat(
  apiKey: string,
  model: string,
  prompt: string,
  fetchFn: typeof fetch
): Promise<string> {
  const res = await fetchFn("https://api.openai.com/v1/chat/completions", {
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

  if (!res.ok) {
    const body = await res.text().catch(() => "(no body)");
    throw new Error(`OpenAI chat HTTP ${res.status}: ${body.slice(0, 200)}`);
  }

  const data = await res.json() as {
    choices?: Array<{
      message?: {
        content?: string | Array<{ type: string; text?: string }>;
      };
    }>;
  };

  const content = data.choices?.[0]?.message?.content;

  if (typeof content === "string" && content.trim()) {
    return content;
  }

  if (Array.isArray(content)) {
    const text = content
      .filter((part) => part?.type === "text" && typeof part.text === "string")
      .map((part) => part.text ?? "")
      .join("")
      .trim();

    if (text) return text;
  }

  throw new Error("OpenAI chat: empty response content");
}

async function callOpenAIResponses(
  apiKey: string,
  model: string,
  prompt: string,
  fetchFn: typeof fetch
): Promise<string> {
  const res = await fetchFn("https://api.openai.com/v1/responses", {
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

  if (!res.ok) {
    const body = await res.text().catch(() => "(no body)");
    throw new Error(`OpenAI responses HTTP ${res.status}: ${body.slice(0, 200)}`);
  }

  const data = await res.json() as {
    output_text?: string;
    output?: Array<{
      content?: Array<{ type?: string; text?: string }>;
    }>;
  };

  if (typeof data.output_text === "string" && data.output_text.trim()) {
    return data.output_text;
  }

  const text = (data.output ?? [])
    .flatMap((item) => item.content ?? [])
    .filter((part) => part?.type === "output_text" && typeof part.text === "string")
    .map((part) => part.text ?? "")
    .join("")
    .trim();

  if (!text) {
    throw new Error("OpenAI responses: empty response content");
  }

  return text;
}

// ---------------------------------------------------------------------------
// Response parsing
// ---------------------------------------------------------------------------

/**
 * Extract subject and body from raw LLM text.
 *
 * Expected format:
 *   Subject: <subject line>
 *   <blank line>
 *   <body...>
 *
 * Returns null if the response cannot be parsed — caller treats as failure.
 */
function parseResponse(
  text: string,
  job: NormalizedJob
): { subject: string; body: string } | null {
  const lines = text.trim().split(/\r?\n/);

  // Find subject line (must start with "Subject:")
  const subjectIdx = lines.findIndex((l) =>
    l.trimStart().toLowerCase().startsWith("subject:")
  );
  if (subjectIdx === -1) return null;

  const subject = lines[subjectIdx]!
    .replace(/^subject:\s*/i, "")
    .trim();
  if (!subject) return null;

  // Body is everything after the subject (skip blank separator line)
  let bodyStart = subjectIdx + 1;
  while (bodyStart < lines.length && lines[bodyStart]!.trim() === "") {
    bodyStart++;
  }

  const body = lines.slice(bodyStart).join("\n").trim();
  if (!body) return null;

  // Sanity check: body must mention the company (guards against hallucination)
  if (!body.toLowerCase().includes(job.company.toLowerCase().slice(0, 6))) {
    return null;
  }

  return { subject, body };
}