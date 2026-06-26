import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import fs from "fs";

const IDLE_RESET_MS = 2 * 60 * 60 * 1000;

let startTime = Date.now();
let lessonDayStart = new Date().toDateString();
let lastMessageTime = Date.now();
let autoReset = false;

function maybeResetTimer() {
  const now = Date.now();
  const todayStr = new Date().toDateString();
  const idleMs = lastMessageTime ? now - lastMessageTime : 0;

  if (lessonDayStart !== todayStr) {
    startTime = now;
    lessonDayStart = todayStr;
    lastMessageTime = now;
    autoReset = true;
  } else if (idleMs > IDLE_RESET_MS) {
    startTime = now;
    lastMessageTime = now;
    autoReset = true;
  }
}

function getPhase(elapsed) {
  if (elapsed < 5) return { phase: "WARM_UP", instruction: "Greet student, ask 1 easy question about day/week. Keep it light." };
  if (elapsed < 25) return { phase: "MAIN_ACTIVITY", instruction: "Lead conversation actively, teach vocab, student should talk 70%." };
  if (elapsed < 30) return { phase: "WRAP_UP", instruction: "Wind down, summarize, assign homework. Write files before goodbye." };
  return { phase: "END", instruction: "Write session summary + transcript to files, then goodbye." };
}

function buildContext() {
  maybeResetTimer();
  const now = Date.now();
  const elapsed = Math.floor((now - startTime) / 60000);
  const { phase, instruction } = getPhase(elapsed);
  const autoResetNote = autoReset ? "\n[Auto-reset: new lesson detected — timer was reset. This is a fresh lesson.]" : "";
  autoReset = false;

  return `[System Context]
Current timestamp: ${new Date().toISOString()}
Session elapsed: ${elapsed} minutes
Current phase: ${phase}
${instruction}
Reminder: You must strictly follow the phase above. Do not skip phases or act out of sequence.${autoResetNote}`;
}

export default definePluginEntry({
  id: "tutor-timing",
  name: "Tutor Timing Injector",
  description: "Injects timing context into english-oral-teacher agent prompts.",

  register(api) {
    api.on("message_received", async () => {
      lastMessageTime = Date.now();
    });

    api.on("before_prompt_build", async () => {
      const ctx = buildContext();
      try { fs.appendFileSync("C:\\Users\\samuel\\.openclaw\\tmp\\hook-log.txt", `before_prompt_build injecting:\n${ctx}\n---\n`); } catch {}
      return { prependContext: ctx };
    });

    api.on("agent_turn_prepare", async () => {
      return { prependContext: buildContext() };
    });

    api.on("before_agent_start", async () => {
      return { prependContext: buildContext() };
    });

    api.on("session_start", async (event) => {
      const reason = event.context?.reason || "unknown";
      if (reason === "new") {
        startTime = Date.now();
        lessonDayStart = new Date().toDateString();
        lastMessageTime = Date.now();
        autoReset = false;
      }
    });
  },
});
