#!/usr/bin/env node

// --- Argument parsing ---
const args = process.argv.slice(2);
let prompt = null;
let size = "square";
let tokenFlag = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--size" && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === "--token" && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === "--ref" && args[i + 1]) {
    refUuid = args[++i];
  } else if (!args[i].startsWith("--") && prompt === null) {
    prompt = args[i];
  }
}

if (!prompt) {
  prompt =
    "professional album cover art, dramatic lighting, bold composition, music album aesthetic, high contrast, visually striking, suitable for streaming platforms";
}

// --- Token resolution ---
const TOKEN = tokenFlag || process.env.NETA_TOKEN;

if (!TOKEN) {
  console.error(
    '\n✗ Token required. Pass via: --token YOUR_TOKEN'
  );
  process.exit(1);
}

// --- Size mapping ---
const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const { width, height } = SIZES[size] || SIZES.square;

// --- Headers ---
const HEADERS = {
  "x-token": TOKEN,
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
  body.inherit_params = {
    collection_uuid: refUuid,
    picture_uuid: refUuid,
  };
}

// --- Submit job ---
async function makeImage() {
  const res = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`make_image failed (${res.status}): ${text}`);
  }

  const data = await res.json();
  const taskUuid =
    typeof data === "string" ? data : data.task_uuid;

  if (!taskUuid) {
    throw new Error(`No task_uuid in response: ${JSON.stringify(data)}`);
  }

  return taskUuid;
}

// --- Poll for result ---
async function pollTask(taskUuid) {
  const url = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  const MAX_ATTEMPTS = 90;
  const INTERVAL_MS = 2000;

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    await new Promise((r) => setTimeout(r, INTERVAL_MS));

    const res = await fetch(url, { headers: HEADERS });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`poll failed (${res.status}): ${text}`);
    }

    const data = await res.json();
    const status = data.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      continue;
    }

    // Done — extract image URL
    const imageUrl =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (!imageUrl) {
      throw new Error(`No image URL in response: ${JSON.stringify(data)}`);
    }

    return imageUrl;
  }

  throw new Error(`Timed out waiting for task ${taskUuid} after ${MAX_ATTEMPTS} attempts`);
}

// --- Main ---
(async () => {
  try {
    const taskUuid = await makeImage();
    const imageUrl = await pollTask(taskUuid);
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error("Error:", err.message);
    process.exit(1);
  }
})();
