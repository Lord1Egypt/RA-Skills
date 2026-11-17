// Offline harness for oc-usage-badge.js.
// Point HISTORY_JSON at a chat.history payload ({"messages":[...]}) to test.
const path = require("path");
const fs = require("fs");

class FakeWS {
  constructor(url) { this.url = url; this._l = {}; }
  addEventListener(type, fn) { (this._l[type] = this._l[type] || []).push(fn); }
  send() {}
  emit(type, ev) { (this._l[type] || []).forEach((fn) => fn(ev)); }
}
FakeWS.OPEN = 1; FakeWS.CONNECTING = 0; FakeWS.CLOSING = 2; FakeWS.CLOSED = 3;

global.window = { WebSocket: FakeWS };
require(path.join(__dirname, "../assets/oc-usage-badge.js"));

const ws = new window.WebSocket("ws://x");
let got = null;
ws.addEventListener("message", (ev) => { got = ev.data; });

const histPath = process.env.HISTORY_JSON || "/tmp/hist.json";
const hist = JSON.parse(fs.readFileSync(histPath, "utf8"));

function countAnnotated(data) {
  const o = JSON.parse(data);
  let n = 0, sample = "";
  (function walkV(x) {
    if (!x || typeof x !== "object") return;
    if (Array.isArray(x)) return x.forEach(walkV);
    if (x.role === "assistant" && Array.isArray(x.content)) {
      const last = x.content[x.content.length - 1];
      if (last && last.type === "text" && /^\n\n\*\u2191/.test(last.text)) {
        n++; if (!sample) sample = last.text;
      }
    }
    Object.values(x).forEach(walkV);
  })(o);
  return { n, sample };
}

ws.emit("message", { data: JSON.stringify({ type: "res", id: 7, ok: true, result: { messages: hist.messages || hist.items } }) });
console.log("annotated:", got ? countAnnotated(got) : null);

const plain = JSON.stringify({ type: "res", id: 9, ok: true, result: { foo: 1 } });
got = null; ws.emit("message", { data: plain });
console.log("plain frame untouched:", got === plain);
got = null; ws.emit("message", { data: "ping" });
console.log("ping untouched:", got === "ping");
