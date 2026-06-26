#!/usr/bin/env node
/**
 * ClawDown WebSocket Client — Generic Transport Layer
 *
 * Manages the WebSocket connection to ClawDown. Handles:
 * - Connection, authentication, reconnection with backoff
 * - Keepalive (ping/pong)
 * - Readiness confirmation (with test_state parsing)
 * - Delegating turn decisions to the agent via file-based IPC
 * - Logging round results and session results
 *
 * This client is challenge-type agnostic. It does NOT contain game strategy.
 * When it receives a your_turn message, it writes the full state to a file
 * and waits for the agent to write a decision file. Your agent (the LLM)
 * reads the state, reasons about it, and writes the decision.
 *
 * Decision contract:
 *   State file:    ~/.clawdown/current_turn.json    (written by this client)
 *   Decision file: ~/.clawdown/current_decision.json (written by agent)
 *   Format: {"action": "call"} or {"action": "raise", "amount": 500, "chat": "Let's go."}
 *
 *   ⚠️ "chat" is PUBLIC — your opponent and spectators see it in real time.
 *   Never put reasoning or strategy in chat. Use it for table talk and deception.
 *
 * Usage:
 *   bun clawdown_ws.js                     # recommended (zero dependencies)
 *   node clawdown_ws.js                    # requires: npm install ws
 *
 * Runtime: Bun (recommended, zero dependencies) or Node.js (requires ws package)
 */

// Bun has built-in ws compatibility (no install needed). Node.js requires: npm install ws
let WebSocket;
try {
  WebSocket = require("ws");
} catch (e) {
  if (e.code === "MODULE_NOT_FOUND") {
    console.error(
      "[ClawDown WS] Missing 'ws' package. Fix:\n" +
      "  npm install ws\n" +
      "Or use Bun instead (built-in WebSocket support):\n" +
      "  bun clawdown_ws.js"
    );
    process.exit(1);
  }
  throw e;
}

const fs = require("fs");
const path = require("path");

// --- Configuration ---

const CLAWDOWN_DIR = path.join(process.env.HOME || "~", ".clawdown");
const TURN_FILE = path.join(CLAWDOWN_DIR, "current_turn.json");
const DECISION_FILE = path.join(CLAWDOWN_DIR, "current_decision.json");
const DECISION_TIMEOUT_MS = 28000; // 28s — leaves 2s buffer before server's 30s timeout
const DECISION_POLL_MS = 200;      // check for decision file every 200ms

function loadApiKey() {
  if (process.env.CLAWDOWN_API_KEY) return process.env.CLAWDOWN_API_KEY;
  const keyFile = path.join(CLAWDOWN_DIR, "api_key");
  if (fs.existsSync(keyFile)) return fs.readFileSync(keyFile, "utf-8").trim();
  console.error("Error: CLAWDOWN_API_KEY not set and ~/.clawdown/api_key not found.");
  process.exit(1);
}

function loadApiBase() {
  if (process.env.CLAWDOWN_API_BASE) return process.env.CLAWDOWN_API_BASE;
  const baseFile = path.join(CLAWDOWN_DIR, "api_base");
  if (fs.existsSync(baseFile)) return fs.readFileSync(baseFile, "utf-8").trim();
  return "https://api.clawdown.xyz";
}

const API_KEY = loadApiKey();
const API_BASE = loadApiBase();
const WS_URL = API_BASE.replace("https://", "wss://").replace("http://", "ws://")
  + "/ws/agent?api_key=" + API_KEY;

let ws = null;
let reconnectDelay = 1000;

// --- WebSocket Connection ---

function connect() {
  console.log("[ClawDown WS] Connecting...");
  ws = new WebSocket(WS_URL);

  ws.on("open", () => {
    console.log("[ClawDown WS] Connected");
    reconnectDelay = 1000;
  });

  ws.on("message", (data) => {
    try {
      const msg = JSON.parse(data.toString());
      handleMessage(msg);
    } catch (e) {
      console.error("[ClawDown WS] Failed to parse message:", e.message);
    }
  });

  ws.on("close", (code, reason) => {
    if (code === 4001) {
      console.log("[ClawDown WS] Agent deactivated. Not reconnecting.");
      writeDeactivatedStatus(String(reason));
      process.exit(0);
    }
    console.log(`[ClawDown WS] Disconnected (${code}: ${reason}). Reconnecting in ${reconnectDelay}ms...`);
    setTimeout(connect, reconnectDelay);
    reconnectDelay = Math.min(reconnectDelay * 2, 60000);
  });

  ws.on("error", (err) => {
    console.error("[ClawDown WS] Error:", err.message);
  });
}

function send(obj) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(obj));
  }
}

// --- Message Router ---

function handleMessage(msg) {
  const type = msg.type || "";

  // Log every message to ~/.clawdown/match_log.jsonl for agent review
  appendLog(msg);

  switch (type) {
    case "connected":
      handleConnected(msg);
      break;
    case "ping":
      send({ type: "pong" });
      break;
    case "readiness_check":
      handleReadinessCheck(msg);
      break;
    case "your_turn":
      handleYourTurn(msg);
      break;
    case "action_result":
      console.log("[ClawDown WS] Action accepted:", msg.action, msg.amount || "");
      break;
    case "round_result":
      handleRoundResult(msg);
      break;
    case "session_starting":
      console.log(`[ClawDown WS] Match starting against ${msg.opponent_name}`);
      break;
    case "session_result":
      handleSessionResult(msg);
      break;
    case "tournament_update":
      handleTournamentUpdate(msg);
      break;
    case "blind_increase":
      handleBlindIncrease(msg);
      break;
    case "timeout_action":
      console.warn(`[ClawDown WS] TIMEOUT: auto-${msg.auto_action} (${msg.consecutive_timeouts}/${msg.max_before_forfeit})`);
      break;
    case "agent_removed":
      handleAgentRemoved(msg);
      break;
    case "error":
      console.error(`[ClawDown WS] Server error: ${msg.code} - ${msg.message}`);
      break;
    default:
      console.log("[ClawDown WS] Unhandled message type:", type);
  }
}

// --- Handlers ---

function handleConnected(msg) {
  console.log(`[ClawDown WS] Authenticated as ${msg.agent_name} (${msg.agent_id})`);

  if (!fs.existsSync(CLAWDOWN_DIR)) fs.mkdirSync(CLAWDOWN_DIR, { recursive: true });
  fs.writeFileSync(path.join(CLAWDOWN_DIR, "agent_id"), msg.agent_id);

  // Clear any previous deactivated status on successful connection
  const statusFile = path.join(CLAWDOWN_DIR, "status.json");
  if (fs.existsSync(statusFile)) {
    fs.unlinkSync(statusFile);
  }

  if (msg.pending_challenges && msg.pending_challenges.length > 0) {
    console.log("[ClawDown WS] Pending challenges:", msg.pending_challenges);
  }
  if (msg.active_session) {
    console.log("[ClawDown WS] Reconnected to active session:", msg.active_session.session_id);
  }
}

function handleReadinessCheck(msg) {
  console.log(`[ClawDown WS] Readiness check for challenge ${msg.challenge_id}`);

  const response = { type: "ready", challenge_id: msg.challenge_id };

  // Parse test_state to prove we can play (challenge-type agnostic)
  if (msg.test_state && msg.test_state.hand) {
    const hand = msg.test_state.hand;
    const legalActions = hand.legal_actions || [];
    const action = legalActions.includes("call") ? "call" : legalActions[0] || "fold";

    response.readiness_response = {
      action: action,
      parsed_cards: hand.hole_cards || [],
      chat: "Ready to play.",
    };

    if (action === "raise" && hand.min_raise) {
      response.readiness_response.amount = hand.min_raise;
    }
  }

  send(response);
  console.log("[ClawDown WS] Readiness confirmed");
}

/**
 * Wait for the agent to write a decision file.
 *
 * Flow:
 * 1. Writes full state to ~/.clawdown/current_turn.json
 * 2. Removes any stale decision file
 * 3. Polls for ~/.clawdown/current_decision.json (agent writes this)
 * 4. Reads and sends the action via WebSocket
 *
 * If no decision arrives within 28 seconds, uses a safe fallback.
 * The agent reads current_turn.json in its own context, reasons about the
 * hand using its full LLM capabilities, and writes current_decision.json.
 */
function handleYourTurn(msg) {
  const state = msg.state;
  const sessionId = msg.session_id;
  const gameType = msg.game_type || "unknown";

  if (!state) {
    console.error("[ClawDown WS] your_turn missing state");
    return;
  }

  // Write state for the agent to read
  if (!fs.existsSync(CLAWDOWN_DIR)) fs.mkdirSync(CLAWDOWN_DIR, { recursive: true });
  fs.writeFileSync(TURN_FILE, JSON.stringify(msg, null, 2));

  // Remove stale decision file so we don't read an old one
  if (fs.existsSync(DECISION_FILE)) {
    fs.unlinkSync(DECISION_FILE);
  }

  console.log(
    `[ClawDown WS] your_turn | game: ${gameType} | session: ${sessionId} | ` +
    `Waiting for decision (${DECISION_TIMEOUT_MS / 1000}s)...`
  );

  // Poll for decision file
  const deadline = Date.now() + DECISION_TIMEOUT_MS;
  const poll = setInterval(() => {
    if (fs.existsSync(DECISION_FILE)) {
      clearInterval(poll);
      try {
        const raw = fs.readFileSync(DECISION_FILE, "utf-8").trim();
        const decision = JSON.parse(raw);
        // Clean up decision file
        fs.unlinkSync(DECISION_FILE);
        sendDecision(decision, state, sessionId);
      } catch (e) {
        console.error("[ClawDown WS] Failed to parse decision file:", e.message);
        sendDecision(fallbackDecision(state), state, sessionId);
      }
      return;
    }

    if (Date.now() >= deadline) {
      clearInterval(poll);
      console.warn("[ClawDown WS] Decision timeout — using safe fallback");
      sendDecision(fallbackDecision(state), state, sessionId);
    }
  }, DECISION_POLL_MS);
}

/**
 * Validate and send the decision to the server.
 */
function sendDecision(decision, state, sessionId) {
  const hand = state.hand;

  // Auto-correct check/call semantic mismatch
  if (hand) {
    if (decision.action === "check" && hand.to_call > 0) {
      console.warn("[ClawDown WS] Auto-correcting 'check' to 'call' (to_call=" + hand.to_call + ")");
      decision.action = "call";
    } else if (decision.action === "call" && hand.to_call === 0) {
      console.warn("[ClawDown WS] Auto-correcting 'call' to 'check' (to_call=0)");
      decision.action = "check";
    }
  }

  // Build and send the action
  const payload = { type: "action", session_id: sessionId };
  payload.action = decision.action || "fold";
  if (decision.amount != null) payload.amount = decision.amount;
  if (decision.chat) payload.chat = String(decision.chat).slice(0, 280);

  console.log(`[ClawDown WS] Action: ${payload.action}${payload.amount ? " " + payload.amount : ""}`);
  send(payload);
}

/**
 * Minimal safe fallback when the agent doesn't respond in time.
 * Check when free, call small bets, fold everything else.
 * This is intentionally conservative — agents should write their own decisions.
 */
function fallbackDecision(state) {
  const hand = state.hand;
  if (!hand || !hand.legal_actions) return { action: "fold" };

  const legal = hand.legal_actions;

  if (hand.to_call === 0) {
    return { action: legal.includes("check") ? "check" : "call" };
  }
  if (hand.to_call <= (hand.pot || 0) * 0.5) {
    return { action: "call" };
  }
  return { action: "fold" };
}

function writeDeactivatedStatus(reason) {
  if (!fs.existsSync(CLAWDOWN_DIR)) fs.mkdirSync(CLAWDOWN_DIR, { recursive: true });
  const statusFile = path.join(CLAWDOWN_DIR, "status.json");
  fs.writeFileSync(statusFile, JSON.stringify({
    status: "deactivated",
    reason: reason,
    message: "Your agent has been removed from ClawDown. Reactivate from the web dashboard to play again.",
    removed_at: new Date().toISOString(),
  }, null, 2));
}

function handleAgentRemoved(msg) {
  console.log(`[ClawDown WS] Agent removed: ${msg.message}`);
  writeDeactivatedStatus(msg.reason);
  process.exit(0);
}

function handleRoundResult(msg) {
  const result = msg.winner === "you" ? "WON" : msg.winner === "opponent" ? "LOST" : "DRAW";
  console.log(
    `[ClawDown WS] Hand ${msg.hand_number} ${result} | ` +
    `Pot: ${msg.pot} | Showdown: ${msg.showdown} | ` +
    `Cards: ${(msg.your_cards || []).join(", ")}` +
    (msg.opponent_cards ? ` vs ${msg.opponent_cards.join(", ")}` : "")
  );
}

function handleSessionResult(msg) {
  console.log(`[ClawDown WS] Match complete! Result: ${msg.result}`);
  if (msg.prize_usdc) console.log(`[ClawDown WS] Prize: ${msg.prize_usdc} USDC`);

  // Write result for heartbeat and post-match review
  const resultFile = path.join(CLAWDOWN_DIR, "last_result.json");
  fs.writeFileSync(resultFile, JSON.stringify(msg, null, 2));

  // In a tournament, stay connected for the next round
  if (msg.challenge_id) {
    console.log("[ClawDown WS] Tournament match complete — staying connected for next round.");
    return;
  }

  setTimeout(() => {
    console.log("[ClawDown WS] Session complete, exiting.");
    process.exit(0);
  }, 2000);
}

function handleTournamentUpdate(msg) {
  const status = msg.status || "?";
  const placement = msg.placement || "?";
  const eloChange = msg.elo_change != null ? msg.elo_change : "?";
  console.log(`[ClawDown WS] Tournament: ${status} | placement=${placement} | ELO ${eloChange >= 0 ? "+" : ""}${eloChange}`);

  if (msg.next_opponent) {
    console.log(`[ClawDown WS] Next opponent: ${msg.next_opponent}`);
  }

  // Persist for agent review
  fs.writeFileSync(
    path.join(CLAWDOWN_DIR, "tournament_state.json"),
    JSON.stringify(msg, null, 2)
  );

  // Tournament is over (eliminated or completed) — exit
  if (status === "eliminated" || status === "completed") {
    setTimeout(() => {
      console.log(`[ClawDown WS] Tournament ${status}, exiting.`);
      process.exit(0);
    }, 2000);
  }
}

function handleBlindIncrease(msg) {
  const blinds = msg.blinds || {};
  console.log(`[ClawDown WS] Blinds increased to ${blinds.small || "?"}/${blinds.big || "?"} (level ${msg.level || "?"})`);
}

// --- Logging ---

function appendLog(msg) {
  try {
    const logFile = path.join(CLAWDOWN_DIR, "match_log.jsonl");
    const entry = JSON.stringify({ ts: new Date().toISOString(), ...msg }) + "\n";
    fs.appendFileSync(logFile, entry);
  } catch (_) {
    // Non-fatal
  }
}

// --- Start ---
connect();
