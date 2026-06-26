import { runCommand } from "./utils.js";

const ENV_RULES = [
  {
    host: "claude-code",
    confidence: "env-var",
    matches: [
      "CLAUDE_CODE",
      "CLAUDECODE",
      "CLAUDE_PROJECT_DIR",
      "ANTHROPIC_API_KEY"
    ]
  },
  {
    host: "codex",
    confidence: "env-var",
    matches: [
      "CODEX_THREAD_ID",
      "CODEX_CI",
      "CODEX_SHELL",
      "CODEX_INTERNAL_ORIGINATOR_OVERRIDE",
      "OPENAI_CODE_INTERPRETER",
      "OPENAI_API_KEY"
    ]
  },
  {
    host: "openclaw",
    confidence: "env-var",
    matches: [
      "OPENCLAW",
      "OPENCLAW_ENV",
      "OPENCLAW_SESSION",
      "OPENCLAW_HOME"
    ]
  }
];

async function detectParentProcess() {
  try {
    const parentPid = String(process.ppid);
    const { stdout } = await runCommand("ps", ["-o", "comm=", "-p", parentPid]);
    return stdout || null;
  } catch {
    return null;
  }
}

function matchEnvironment(env) {
  for (const rule of ENV_RULES) {
    const matchedKeys = rule.matches.filter((key) => Boolean(env[key]));

    if (matchedKeys.length > 0) {
      return {
        host: rule.host,
        confidence: rule.confidence,
        matched_signals: matchedKeys,
        term_program: env.TERM_PROGRAM ?? null
      };
    }
  }

  return null;
}

function matchHeuristics(env, parentProcess) {
  const parent = parentProcess?.toLowerCase() ?? "";
  const originator = env.CODEX_INTERNAL_ORIGINATOR_OVERRIDE?.toLowerCase() ?? "";

  if (originator.includes("codex") || parent.includes("codex")) {
    return {
      host: "codex",
      confidence: "heuristic",
      matched_signals: [originator ? "CODEX_INTERNAL_ORIGINATOR_OVERRIDE" : "parent-process"],
      term_program: env.TERM_PROGRAM ?? null
    };
  }

  if (parent.includes("claude")) {
    return {
      host: "claude-code",
      confidence: "heuristic",
      matched_signals: ["parent-process"],
      term_program: env.TERM_PROGRAM ?? null
    };
  }

  if (parent.includes("openclaw")) {
    return {
      host: "openclaw",
      confidence: "heuristic",
      matched_signals: ["parent-process"],
      term_program: env.TERM_PROGRAM ?? null
    };
  }

  return null;
}

export async function detectHost(env = process.env) {
  const envMatch = matchEnvironment(env);
  if (envMatch) {
    return envMatch;
  }

  const parentProcess = await detectParentProcess();
  const heuristicMatch = matchHeuristics(env, parentProcess);
  if (heuristicMatch) {
    return {
      ...heuristicMatch,
      parent_process: parentProcess
    };
  }

  return {
    host: "unknown",
    confidence: "none",
    matched_signals: [],
    term_program: env.TERM_PROGRAM ?? null,
    parent_process: parentProcess
  };
}
