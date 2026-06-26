#!/usr/bin/env node

const args = process.argv.slice(2);
if (args.length < 2 || args[0] === "-h" || args[0] === "--help") {
  console.error('Usage: generate.mjs <api-key> "prompt"');
  process.exit(2);
}

const apiKey = args[0].trim();
if (!apiKey) {
  console.error("Missing API key. Get one at https://www.skillboss.co");
  process.exit(1);
}

const resp = await fetch("https://api.heybossai.com/v1/run", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ api_key: apiKey, model: "mm/img", inputs: { prompt: args[1] } }),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`API failed (${resp.status}): ${text}`);
}

const data = await resp.json();
const url = data.image_url || data.url || data.data?.[0] || null;
if (url) {
  console.log(url);
} else {
  console.log(JSON.stringify(data, null, 2));
}
