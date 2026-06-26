/**
 * EMP Skill – role and model configuration.
 *
 * Edit ROLE_MODEL_MAP and ROLE_KEYWORDS here to add, remove, or reassign roles
 * without touching any other module.
 */

/** Maps each employee role to its current OpenRouter model string. */
export const ROLE_MODEL_MAP: Record<string, string> = {
  "Lead Dev": "openrouter/auto",
  "Creative Director": "openrouter/auto",
  "Data Scientist": "openrouter/auto",
  "Legal Counsel": "openrouter/auto",
  "HR/Mediator": "openrouter/auto",
  "Ops Specialist": "openrouter/auto",
  "Security Auditor": "openrouter/auto",
  "Customer Success": "openrouter/auto",
  "NVC Specialist": "openrouter/auto",
};

/** Maps each employee role to its preferred, optimized OpenRouter model. */
export const PREFERRED_MODEL_MAP: Record<string, string> = {
  "Lead Dev": "anthropic/claude-3.5-sonnet",
  "Creative Director": "arcee/trinity-large",
  "Data Scientist": "google/gemini-pro-1.5",
  "Legal Counsel": "openai/gpt-4o",
  "HR/Mediator": "anthropic/claude-3-haiku",
  "Ops Specialist": "meta-llama/llama-3.1-70b-instruct",
  "Security Auditor": "deepseek/deepseek-chat",
  "Customer Success": "google/gemini-1.5-flash",
  "NVC Specialist": "anthropic/claude-3.5-sonnet",
};

/** Fallback model used when the primary model is rate-limited. */
export const FALLBACK_MODEL = "openrouter/free";

/**
 * Keyword sets used by the intent classifier to map tasks to roles.
 * Keys must match the keys in ROLE_MODEL_MAP exactly.
 */
export const ROLE_KEYWORDS: Record<string, string[]> = {
  "Lead Dev": [
    "code", "bug", "refactor", "implement", "function", "class",
    "debug", "test", "develop", "programming", "software", "api",
    "deploy", "build", "architecture", "algorithm",
  ],
  "Creative Director": [
    "design", "creative", "brand", "visual", "art", "aesthetic",
    "campaign", "copy", "content", "story", "narrative", "marketing",
    "logo", "color", "typography", "ux", "ui",
  ],
  "Data Scientist": [
    "data", "analysis", "model", "machine learning", "ml", "statistics",
    "dataset", "predict", "train", "neural", "insight", "metric",
    "chart", "visualize", "regression", "classification",
  ],
  "Legal Counsel": [
    "legal", "contract", "compliance", "regulation", "law", "policy",
    "agreement", "terms", "liability", "copyright", "patent", "gdpr",
    "privacy", "clause", "dispute", "ip",
  ],
  "HR/Mediator": [
    "hr", "hire", "recruit", "onboard", "performance", "review",
    "conflict", "culture", "team", "diversity", "inclusion", "benefit",
    "salary", "employee", "mediat",
  ],
  "Ops Specialist": [
    "ops", "operation", "workflow", "process", "infrastructure",
    "devops", "pipeline", "ci/cd", "monitor", "scale", "automate",
    "cloud", "server", "network", "incident", "sre",
  ],
  "Security Auditor": [
    "security", "vulnerability", "audit", "penetration", "threat",
    "risk", "exploit", "patch", "firewall", "encryption", "access",
    "auth", "credential", "breach", "cve",
  ],
  "Customer Success": [
    "customer", "client", "support", "feedback", "satisfaction",
    "churn", "retention", "onboarding", "success", "account",
    "relationship", "ticket", "issue", "user", "help",
  ],
  "NVC Specialist": [
    "nvc", "empathy", "communication", "feeling", "need", "request",
    "observation", "listen", "compassion", "emotion", "connect",
    "express", "nonviolent", "conflict resolution",
  ],
};

/** OpenRouter API endpoint */
export const OPENROUTER_API_URL =
  "https://openrouter.ai/api/v1/chat/completions";
