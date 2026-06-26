// AWP LLM Client for Cloudflare Workers
// Supports Workers AI and OpenAI-compatible APIs.

import type { Env, AgentConfig, ChatMessage } from "./types";

/**
 * Call the LLM for an agent and return the parsed JSON response.
 *
 * Routing:
 * - If agent config has `provider: "workers-ai"`, uses env.AI binding.
 * - Otherwise, uses fetch() against the OpenAI-compatible endpoint.
 */
export async function callLLM(
  env: Env,
  agent: AgentConfig,
  messages: ChatMessage[],
): Promise<Record<string, unknown>> {
  const provider = agent.model.provider ?? "openai-compatible";

  let text: string;

  if (provider === "workers-ai" && env.AI) {
    text = await callWorkersAI(env, agent, messages);
  } else {
    text = await callOpenAICompatible(env, agent, messages);
  }

  return parseJSONResponse(text, agent.identity.id);
}

/** Call Cloudflare Workers AI. */
async function callWorkersAI(
  env: Env,
  agent: AgentConfig,
  messages: ChatMessage[],
): Promise<string> {
  const response = await env.AI!.run(agent.model.name as BaseAiTextGenerationModels, {
    messages: messages.map((m) => ({
      role: m.role,
      content: m.content,
    })),
  });

  if ("response" in response && typeof response.response === "string") {
    return response.response;
  }
  throw new Error(`Workers AI returned unexpected format for agent ${agent.identity.id}`);
}

/** Call an OpenAI-compatible API (OpenRouter, Anthropic, etc.). */
async function callOpenAICompatible(
  env: Env,
  agent: AgentConfig,
  messages: ChatMessage[],
): Promise<string> {
  const baseUrl = env.LLM_BASE_URL || "https://openrouter.ai/api/v1";
  const model = agent.model.name || env.LLM_MODEL;
  const apiKey = env.LLM_API_KEY;

  if (!apiKey) {
    throw new Error("LLM_API_KEY is not set. Use: wrangler secret put LLM_API_KEY");
  }

  const response = await fetch(`${baseUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: agent.model.parameters.temperature ?? 0.2,
      max_tokens: agent.model.parameters.max_tokens,
      response_format: { type: "json_object" },
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(
      `LLM API error (${response.status}) for agent ${agent.identity.id}: ${body}`,
    );
  }

  const data = (await response.json()) as {
    choices: Array<{ message: { content: string } }>;
  };

  return data.choices[0]?.message?.content ?? "";
}

/** Parse an LLM response as JSON, extracting from markdown code blocks if needed. */
function parseJSONResponse(
  text: string,
  agentId: string,
): Record<string, unknown> {
  let jsonStr = text.trim();

  // Extract JSON from markdown code blocks
  const codeBlockMatch = jsonStr.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/);
  if (codeBlockMatch) {
    jsonStr = codeBlockMatch[1].trim();
  }

  try {
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed !== "object" || parsed === null) {
      throw new Error("Response is not a JSON object");
    }
    return parsed as Record<string, unknown>;
  } catch (e) {
    throw new Error(
      `Failed to parse JSON from agent ${agentId}: ${(e as Error).message}\nRaw: ${jsonStr.substring(0, 200)}`,
    );
  }
}
