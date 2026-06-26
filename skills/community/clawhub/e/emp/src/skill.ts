/**
 * EMP Skill for OpenClaw.
 *
 * Dynamically routes tasks to one of nine specialised employee roles, calls the
 * corresponding OpenRouter model, and returns the response wrapped in an NVC
 * structure.  Rate-limit errors trigger automatic failover to FALLBACK_MODEL.
 */

import { classifyRole } from "./classifier.js";
import { FALLBACK_MODEL, OPENROUTER_API_URL, ROLE_MODEL_MAP } from "./config.js";
import { type NVCResponse, wrapNvc } from "./nvc.js";

// ---------------------------------------------------------------------------
// Skill decorator (OpenClaw convention)
// ---------------------------------------------------------------------------

const skillRegistry = new Map<string, EMPSkill>();

/**
 * Register a class instance as a named OpenClaw skill.
 *
 * ```ts
 * \@skill("emp")
 * class EMPSkill { ... }
 * ```
 */
export function skill(name: string) {
  return function <T extends new (...args: unknown[]) => EMPSkill>(
    constructor: T,
  ): T {
    const instance = new constructor();
    skillRegistry.set(name, instance);
    (constructor as Record<string, unknown>)._skillName = name;
    return constructor;
  };
}

/** Retrieve a registered skill instance by name. */
export function getSkill(name: string): EMPSkill {
  const instance = skillRegistry.get(name);
  if (!instance) throw new Error(`No skill registered under the name '${name}'.`);
  return instance;
}

// ---------------------------------------------------------------------------
// Execute options
// ---------------------------------------------------------------------------

export interface ExecuteOptions {
  /** Optionally override automatic role selection. */
  role?: string;
  /** Additional HTTP headers forwarded to OpenRouter (e.g. HTTP-Referer). */
  extraHeaders?: Record<string, string>;
}

// ---------------------------------------------------------------------------
// Core skill
// ---------------------------------------------------------------------------

/**
 * OpenClaw skill that routes tasks to specialised employee roles.
 *
 * The `OPENROUTER_API_KEY` environment variable must be set before calling
 * {@link execute}.
 */
@skill("emp")
export class EMPSkill {
  private readonly apiKey: string;

  constructor() {
    this.apiKey = process.env["OPENROUTER_API_KEY"] ?? "";
  }

  /**
   * Route {@link prompt} to the appropriate employee role and return an NVC
   * response.
   *
   * @throws {Error} When both the primary and fallback models fail.
   */
  async execute(prompt: string, options: ExecuteOptions = {}): Promise<NVCResponse> {
    const selectedRole = options.role ?? classifyRole(prompt);
    const primaryModel = ROLE_MODEL_MAP[selectedRole];
    if (!primaryModel) {
      throw new Error(`Unknown role: '${selectedRole}'`);
    }

    let raw = await this.callModel(primaryModel, prompt, options.extraHeaders);
    let usedModel: string;

    if (raw !== null) {
      usedModel = primaryModel;
    } else {
      raw = await this.callModel(FALLBACK_MODEL, prompt, options.extraHeaders);
      if (raw === null) {
        throw new Error(
          `Both primary model '${primaryModel}' and fallback model '${FALLBACK_MODEL}' failed for role '${selectedRole}'.`,
        );
      }
      usedModel = FALLBACK_MODEL;
    }

    return { ...wrapNvc(raw, selectedRole, usedModel), model: usedModel };
  }

  // ------------------------------------------------------------------
  // Internal helpers
  // ------------------------------------------------------------------

  /**
   * Call {@link model} via the OpenRouter API.
   *
   * @returns The assistant message text on success, or `null` on a
   *   rate-limit (HTTP 429) or any other non-2xx response.
   */
  private async callModel(
    model: string,
    prompt: string,
    extraHeaders?: Record<string, string>,
  ): Promise<string | null> {
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.apiKey}`,
      "Content-Type": "application/json",
      ...extraHeaders,
    };

    let response: Response;
    try {
      response = await fetch(OPENROUTER_API_URL, {
        method: "POST",
        headers,
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: prompt }],
        }),
      });
    } catch {
      return null;
    }

    if (response.status === 429 || !response.ok) return null;

    try {
      const data = (await response.json()) as {
        choices?: { message?: { content?: string } }[];
      };
      return data.choices?.[0]?.message?.content ?? null;
    } catch {
      return null;
    }
  }
}
