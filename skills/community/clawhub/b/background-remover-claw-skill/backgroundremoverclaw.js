#!/usr/bin/env node
import { resolve } from "path";

// --- CLI parsing ---
const args = process.argv.slice(2);
const positional = [];
let size = "square";
let token = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--size" && args[i + 1]) { size = args[++i]; }
  else if (args[i] === "--token" && args[i + 1]) { token = args[++i]; }
  else if (args[i] === "--ref" && args[i + 1]) { refUuid = args[++i]; }
  else if (!args[i].startsWith("--")) { positional.push(args[i]); }
}

const prompt = positional.join(" ").trim() || "remove background, transparent cutout, clean edges";

// --- Token resolution ---
if (!token) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  process.exit(1);
}

// --- Size map ---
const sizeMap = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};
const { width, height } = sizeMap[size] ?? sizeMap.square;

// --- Headers ---
const headers = {
  "x-token": token,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

// --- Build request body ---
const body = {
  storyId: "DO_NOT_USE",
  jobType: "universal",
  rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
  width,
  height,
  meta: { entrance: "PICTURE,VERSE" },
  context_model_series: "8_image_edit",
};

if (refUuid) {
  body.inherit_params = { collection_uuid: refUuid, picture_uuid: refUuid };
}

// --- Submit job ---
async function makeImage() {
  const res = await fetch("https://api.talesofai.cn/v3/make_image", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error(`Error submitting job (${res.status}): ${text}`);
    process.exit(1);
  }

  const raw = await res.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(raw);
    taskUuid = typeof parsed === "string" ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = raw.trim();
  }

  if (!taskUuid) {
    console.error("Error: could not extract task_uuid from response:", raw);
    process.exit(1);
  }

  // --- Poll for result ---
  const maxAttempts = 90;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(`https://api.talesofai.cn/v1/artifact/task/${taskUuid}`, { headers });
    if (!pollRes.ok) {
      console.error(`Poll error (${pollRes.status}): ${await pollRes.text()}`);
      process.exit(1);
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      continue;
    }

    // Done — extract URL
    const url =
      data.artifacts?.[0]?.url ||
      data.result_image_url ||
      null;

    if (!url) {
      console.error("Task finished but no image URL found:", JSON.stringify(data));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error("Timed out waiting for image after 90 attempts (~3 minutes).");
  process.exit(1);
}

makeImage().catch((err) => {
  console.error("Unexpected error:", err);
  process.exit(1);
});
