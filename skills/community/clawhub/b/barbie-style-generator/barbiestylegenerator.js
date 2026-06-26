#!/usr/bin/env node
import { parseArgs } from "node:util";

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    token: { type: "string" },
    size: { type: "string", default: "portrait" },
    ref: { type: "string" },
  },
  allowPositionals: true,
});

const PROMPT =
  positionals[0] ||
  "hyper-feminine Barbie doll aesthetic portrait, pastel-saturated pink and blonde fashion editorial look, flawless glamorous makeup, dreamy soft studio lighting, luxury fashion backdrop, ultra-stylized plastic doll beauty, perfect skin, big sparkling eyes";

const TOKEN = values.token;

if (!TOKEN) {
  console.error("\n✗ Token required. Pass via: --token YOUR_TOKEN");
  console.error("  Get yours at: https://www.neta.art/open/");
  process.exit(1);
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const size = SIZES[values.size] || SIZES.portrait;

const headers = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: PROMPT, weight: 1 }],
  width: size.width,
  height: size.height,
  meta: { entrance: "PICTURE,VERSE" },
  context_model_series: "8_image_edit",
};

if (values.ref) {
  body.inherit_params = {
    collection_uuid: values.ref,
    picture_uuid: values.ref,
  };
}

console.error("Generating Barbie-style image...");

const makeRes = await fetch("https://api.talesofai.com/v3/make_image", {
  method: "POST",
  headers,
  body: JSON.stringify(body),
});

if (!makeRes.ok) {
  const text = await makeRes.text();
  console.error(`✗ Request failed (${makeRes.status}): ${text}`);
  process.exit(1);
}

const makeData = await makeRes.json();
const taskUuid =
  typeof makeData === "string" ? makeData : makeData.task_uuid;

if (!taskUuid) {
  console.error("✗ No task_uuid in response:", JSON.stringify(makeData));
  process.exit(1);
}

console.error(`Task ID: ${taskUuid}`);
console.error("Polling for result...");

const MAX_ATTEMPTS = 90;
const POLL_INTERVAL_MS = 2000;

for (let i = 0; i < MAX_ATTEMPTS; i++) {
  await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));

  const pollRes = await fetch(
    `https://api.talesofai.com/v1/artifact/task/${taskUuid}`,
    { headers }
  );

  if (!pollRes.ok) {
    console.error(`Poll ${i + 1}: HTTP ${pollRes.status}, retrying...`);
    continue;
  }

  const pollData = await pollRes.json();
  const status = pollData.task_status;

  if (status === "PENDING" || status === "MODERATION") {
    console.error(`Poll ${i + 1}: ${status}...`);
    continue;
  }

  // Done
  const url =
    pollData?.artifacts?.[0]?.url || pollData?.result_image_url;

  if (!url) {
    console.error("✗ No image URL in response:", JSON.stringify(pollData));
    process.exit(1);
  }

  console.log(url);
  process.exit(0);
}

console.error("✗ Timed out waiting for image generation.");
process.exit(1);
