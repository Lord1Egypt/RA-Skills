import { randomUUID } from "node:crypto";
import {
  PROTOCOL_VERSION,
  type Agent,
  type AgentSideConnection,
  type AuthenticateRequest,
  type AuthenticateResponse,
  type CancelNotification,
  type ContentBlock,
  type InitializeRequest,
  type InitializeResponse,
  type NewSessionRequest,
  type NewSessionResponse,
  type PromptRequest,
  type PromptResponse,
} from "@zed-industries/agent-client-protocol";
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { z } from "zod";

export const AGENT_NAME = "Zaphoid";

const SYSTEM_PROMPT = `You are Zaphoid, an ACP (Agent Client Protocol) test agent built on Claude. \
You are being used to validate ACP wiring between this agent and another agent platform. \
If asked who or what you are, identify yourself as Zaphoid.`;

const execFileAsync = promisify(execFile);

/**
 * The only tool Zaphoid gets. Scoped to exactly the one action a reply requires
 * (posting to a Buzz channel) instead of granting general Bash — args are passed
 * as discrete argv entries via execFile (no shell interpolation).
 */
const sendBuzzMessage = tool(
  "send_buzz_message",
  "Post a reply to a Buzz channel. This is the ONLY way to publish a reply.",
  {
    channel: z.string().min(1).max(200).regex(/^[A-Za-z0-9._-]+$/),
    text: z.string().min(1).max(10000),
  },
  async ({ channel, text }) => {
    try {
      const { stdout } = await execFileAsync(
        "buzz",
        ["messages", "send", "--channel", channel, "--content", text],
        { timeout: 15_000 },
      );
      return { content: [{ type: "text", text: stdout || "Message sent." }] };
    } catch (err) {
      return {
        content: [{ type: "text", text: `Failed to send: ${err instanceof Error ? err.message : String(err)}` }],
        isError: true,
      };
    }
  },
);

const buzzMcpServer = createSdkMcpServer({ name: "buzz", version: "1.0.0", tools: [sendBuzzMessage] });

interface SessionState {
  cwd: string;
  systemPrompt: string;
  /** Claude Code CLI session id, used to resume the same conversation across turns. */
  claudeSessionId?: string;
  abortController?: AbortController;
}

function textOf(block: ContentBlock): string | undefined {
  return block.type === "text" ? block.text : undefined;
}

/**
 * A minimal ACP agent that forwards prompts to Claude via the Claude Agent SDK
 * and streams the reply back as `agent_message_chunk` updates. The only tool
 * exposed to the model is `send_buzz_message`, a scoped in-process MCP tool —
 * per buzz-acp's harness contract, that's the only way a reply is ever
 * published; the ACP session/update stream is display-only and never posted.
 */
export class ZaphoidAgent implements Agent {
  private readonly sessions = new Map<string, SessionState>();

  constructor(private readonly conn: AgentSideConnection) {}

  async initialize(_params: InitializeRequest): Promise<InitializeResponse> {
    return {
      protocolVersion: PROTOCOL_VERSION,
      agentCapabilities: {
        loadSession: false,
        promptCapabilities: {
          image: false,
          audio: false,
          embeddedContext: true,
        },
      },
    };
  }

  async authenticate(
    _params: AuthenticateRequest,
  ): Promise<AuthenticateResponse> {
    return {};
  }

  async newSession(params: NewSessionRequest): Promise<NewSessionResponse> {
    const sessionId = randomUUID();
    // `systemPrompt` isn't part of the official ACP schema, but buzz-acp sends it
    // with per-turn operating instructions (how to call send_buzz_message to reply,
    // channel/thread context, etc.) — without it the agent has no way to know it
    // must call that tool to actually post anything.
    const harnessPrompt = (params as { systemPrompt?: string }).systemPrompt;
    const systemPrompt = harnessPrompt
      ? `${SYSTEM_PROMPT}\n\n${harnessPrompt}`
      : SYSTEM_PROMPT;
    this.sessions.set(sessionId, { cwd: params.cwd, systemPrompt });
    return { sessionId };
  }

  async prompt(params: PromptRequest): Promise<PromptResponse> {
    const session = this.sessions.get(params.sessionId);
    if (!session) {
      throw new Error(`Unknown session: ${params.sessionId}`);
    }

    const text = params.prompt
      .map(textOf)
      .filter((t): t is string => Boolean(t))
      .join("\n")
      .trim();

    if (!text) {
      return { stopReason: "end_turn" };
    }

    const abortController = new AbortController();
    session.abortController = abortController;

    const makeStream = (resume: string | undefined) => query({
      prompt: text,
      options: {
        cwd: session.cwd,
        // Zaphoid's own reply is only "sent" when it calls send_buzz_message
        // (see buzz-acp's base_prompt.md) — no built-in tools (Bash included)
        // are granted, so there's nothing else a permission bypass would ever
        // need to cover; allowedTools pre-approves this one MCP tool.
        tools: [],
        mcpServers: { buzz: buzzMcpServer },
        allowedTools: ["mcp__buzz__send_buzz_message"],
        permissionMode: "default",
        systemPrompt: session.systemPrompt,
        resume,
        abortController,
      },
    });

    let stream = makeStream(session.claudeSessionId);
    let stopReason: PromptResponse["stopReason"] = "end_turn";

    try {
      for await (const message of stream) {
        if ("session_id" in message && message.session_id) {
          session.claudeSessionId = message.session_id;
        }

        if (message.type === "assistant") {
          for (const block of message.message.content) {
            if (block.type === "text" && block.text) {
              await this.conn.sessionUpdate({
                sessionId: params.sessionId,
                update: {
                  sessionUpdate: "agent_message_chunk",
                  content: { type: "text", text: block.text },
                },
              });
            }
          }
        }

        if (message.type === "result") {
          switch (message.subtype) {
            case "success":
              stopReason = "end_turn";
              break;
            case "error_max_turns":
              stopReason = "max_turn_requests";
              break;
            case "error_max_budget_usd":
              stopReason = "max_tokens";
              break;
            default:
              stopReason = "refusal";
              break;
          }
        }
      }
    } catch (err) {
      if (abortController.signal.aborted) {
        stopReason = "cancelled";
      } else if (
        session.claudeSessionId &&
        err instanceof Error &&
        err.message.includes("No conversation found with session ID")
      ) {
        // Stale Claude Code session ID (e.g. after a restart) — clear it and
        // retry once from scratch so the conversation continues without error.
        console.error(`[Zaphoid] Stale session ID ${session.claudeSessionId} — retrying fresh`);
        session.claudeSessionId = undefined;
        stream = makeStream(undefined);
        try {
          for await (const message of stream) {
            if ("session_id" in message && message.session_id) {
              session.claudeSessionId = message.session_id;
            }
            if (message.type === "result") {
              stopReason = message.subtype === "success" ? "end_turn" : "refusal";
            }
          }
        } catch (retryErr) {
          throw retryErr;
        }
      } else {
        throw err;
      }
    } finally {
      session.abortController = undefined;
    }

    return { stopReason };
  }

  async cancel(params: CancelNotification): Promise<void> {
    this.sessions.get(params.sessionId)?.abortController?.abort();
  }
}
