/* Reliable Bluesky poster for Sugata automation.
   Logs in fresh with an app password each run (app passwords don't expire),
   so there is no token-expiry problem like the saved-session flow.

   Usage:
     BSKY_IDENTIFIER=sugataai.bsky.social BSKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx \
       node sg-post.mjs "Your post text here"

   Or pipe a file:
     BSKY_IDENTIFIER=... BSKY_APP_PASSWORD=... node sg-post.mjs --file post.txt
*/
import { BskyAgent, RichText } from "@atproto/api";
import fs from "fs";

// Load BSKY_* from .env if not already in the environment (so cron/automation works)
try {
  const envText = fs.readFileSync(new URL("./.env", import.meta.url), "utf8");
  for (const line of envText.split("\n")) {
    const m = line.match(/^\s*(BSKY_IDENTIFIER|BSKY_APP_PASSWORD)\s*=\s*(.+)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].trim().replace(/^["']|["']$/g, "");
  }
} catch {}

const id = process.env.BSKY_IDENTIFIER;
const pw = process.env.BSKY_APP_PASSWORD;
if (!id || !pw) {
  console.error("Missing BSKY_IDENTIFIER or BSKY_APP_PASSWORD env vars.");
  process.exit(1);
}

let text;
const args = process.argv.slice(2);
if (args[0] === "--file") text = fs.readFileSync(args[1], "utf8").trim();
else text = args.join(" ").trim();
if (!text) { console.error("No post text provided."); process.exit(1); }

const agent = new BskyAgent({ service: "https://bsky.social" });
await agent.login({ identifier: id, password: pw });

// RichText auto-detects links + hashtags and creates facets so they're clickable.
const rt = new RichText({ text });
await rt.detectFacets(agent);

const res = await agent.post({ text: rt.text, facets: rt.facets, createdAt: new Date().toISOString() });
const rkey = res.uri.split("/").pop();
console.log("Posted: https://bsky.app/profile/" + agent.session.handle + "/post/" + rkey);
