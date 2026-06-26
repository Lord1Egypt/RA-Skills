import { soulConfig } from "./persistence.ts";
async function postWebhook(type, message) {
  const url = soulConfig.notify_webhook;
  if (!url) return;
  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type, message, ts: Date.now() })
    });
  } catch (e) {
    console.error(`[cc-soul][webhook] ${e.message}`);
  }
}
async function notifySoulActivity(message) {
  if (message.includes("\u68C0\u6D4B\u5230") && message.includes("\u8FDB\u7A0B") && (message.includes("\u5E76\u53D1\u8FD0\u884C") || message.includes("\u5B9E\u4F8B"))) {
    return;
  }
  console.log(`[cc-soul][notify] ${message}`);
  postWebhook("activity", message);
}
async function notifyOwnerDM(message) {
  if (message.includes("\u68C0\u6D4B\u5230") && message.includes("\u8FDB\u7A0B") && (message.includes("\u5E76\u53D1\u8FD0\u884C") || message.includes("\u5B9E\u4F8B"))) {
    return;
  }
  console.log(`[cc-soul][owner] ${message}`);
  postWebhook("owner", message);
}
async function sendRawDM(message) {
  console.log(`[cc-soul][raw] ${message}`);
  postWebhook("raw", message);
}
async function replySender(to, text, _cfg) {
  console.log(`[cc-soul][reply] \u2192 ${to}: ${text.slice(0, 120)}`);
  postWebhook("reply", text);
}
export {
  notifyOwnerDM,
  notifySoulActivity,
  replySender,
  sendRawDM
};
