#!/usr/bin/env npx tsx
/**
 * FlowSearch — Deep Web Research
 *
 * Uses Claude CLI for powerful web searches with synthesis.
 * Works locally or in CI/agent environments.
 *
 * Usage:
 *   npx tsx search.ts "query"           # Quick search
 *   npx tsx search.ts --deep "topic"    # Deep research
 *
 * Requirements:
 *   CLAUDE_CODE_OAUTH_TOKEN env var (from `claude auth login`)
 */

import { spawn } from "child_process";
import { existsSync } from "fs";

// Find Claude CLI path
function findClaudePath(): string {
  const paths = [
    "/data/claude-cli/node_modules/.bin/claude", // Railway / CI
    "/usr/local/bin/claude",                      // Global install
    `${process.env.HOME}/.claude/bin/claude`,     // User install
    "claude",                                     // In PATH
  ];
  for (const p of paths) {
    if (p === "claude" || existsSync(p)) return p;
  }
  return "claude";
}

export interface SearchResult {
  success: boolean;
  query: string;
  answer: string;
  error?: string;
  durationMs: number;
}

/**
 * Execute a Claude CLI web search
 */
export async function claudeSearch(
  query: string,
  options?: { deep?: boolean; timeout?: number }
): Promise<SearchResult> {
  const startTime = Date.now();
  const deep = options?.deep ?? false;
  const timeout = options?.timeout ?? (deep ? 180_000 : 120_000);

  const prompt = deep
    ? `Conduct deep research on: "${query}"

Instructions:
1. Search multiple sources for comprehensive coverage
2. Prioritize recent information (2025–2026)
3. Synthesize into a well-structured report
4. Include specific facts, numbers, and comparisons
5. Cite all sources with URLs

Format:
## Summary
(2–3 sentence overview)

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Details
(Detailed analysis)

## Sources
- [Title](URL)`
    : `Search the web and answer: "${query}"

Instructions:
1. Search for current, accurate information
2. Provide a clear, direct answer
3. Include specific facts and numbers when available
4. Cite sources with URLs at the end`;

  const claudePath = findClaudePath();
  const isRoot = process.getuid?.() === 0;
  const args = ["--print", ...(isRoot ? [] : ["--dangerously-skip-permissions"]), "-p", prompt];

  return new Promise((resolve) => {
    let output = "";
    let errorOutput = "";

    const proc = spawn(claudePath, args, {
      timeout,
      env: { ...process.env },
      stdio: ["pipe", "pipe", "pipe"],
    });

    proc.stdout.on("data", (d) => { output += d.toString(); });
    proc.stderr.on("data", (d) => { errorOutput += d.toString(); });

    proc.on("close", (code) => {
      const durationMs = Date.now() - startTime;
      if (code === 0 && output.trim()) {
        resolve({ success: true, query, answer: output.trim(), durationMs });
      } else {
        resolve({
          success: false, query, answer: "",
          error: errorOutput || `Claude CLI exited with code ${code}`,
          durationMs,
        });
      }
    });

    proc.on("error", (err) => {
      resolve({ success: false, query, answer: "", error: err.message, durationMs: Date.now() - startTime });
    });
  });
}

/**
 * Deep research on a topic with optional guiding questions
 */
export async function claudeResearch(
  topic: string,
  questions?: string[]
): Promise<SearchResult> {
  const query = questions?.length
    ? `${topic}\n\nSpecific questions to answer:\n${questions.map((q, i) => `${i + 1}. ${q}`).join("\n")}`
    : topic;
  return claudeSearch(query, { deep: true });
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === "--help" || args[0] === "-h") {
    console.log(`
FlowSearch — Deep Web Research via Claude CLI
Uses Claude's native search for powerful research synthesis.

Usage:
  npx tsx search.ts <query>              Quick search
  npx tsx search.ts --deep <topic>       Deep research

Environment:
  CLAUDE_CODE_OAUTH_TOKEN    Auth token from \`claude auth login\`

Examples:
  npx tsx search.ts "Kling AI pricing 2026"
  npx tsx search.ts --deep "AI video generation market analysis"
`);
    process.exit(0);
  }

  const isDeep = args[0] === "--deep" || args[0] === "-d";
  const query = isDeep ? args.slice(1).join(" ") : args.join(" ");

  if (!query) {
    console.error("Error: No query provided");
    process.exit(1);
  }

  console.log(`🔍 ${isDeep ? "Researching" : "Searching"}: "${query}"\n`);

  claudeSearch(query, { deep: isDeep })
    .then((result) => {
      if (result.success) {
        console.log(result.answer);
        console.log(`\n⏱️  ${result.durationMs}ms`);
      } else {
        console.error(`❌ Search failed: ${result.error}`);
        process.exit(1);
      }
    })
    .catch((err) => {
      console.error(`❌ Error: ${err.message}`);
      process.exit(1);
    });
}
