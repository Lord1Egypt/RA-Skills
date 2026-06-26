#!/usr/bin/env node

// --- Argument parsing ---
const args = process.argv.slice(2);
let prompt = null;
let size = "portrait";
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
    "3D action figure of a person sealed inside a retail blister pack toy box, collectible figurine packaging, accessories included, product name label on box, hyperrealistic 3D render, studio product photography lighting, toy store shelf aesthetic";
}

// --- Token resolution ---
const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error(
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

const { width, height } = SIZES[size] || SIZES.portrait;

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
async function main() {
  const makeRes = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!makeRes.ok) {
    const text = await makeRes.text();
    console.error(`Error submitting job (${makeRes.status}): ${text}`);
    process.exit(1);
  }

  const makeData = await makeRes.json();
  const taskUuid =
    typeof makeData === "string" ? makeData : makeData.task_uuid;

  if (!taskUuid) {
    console.error("Error: No task_uuid in response:", JSON.stringify(makeData));
    process.exit(1);
  }

  // --- Poll for result ---
  const MAX_ATTEMPTS = 90;
  const POLL_INTERVAL_MS = 2000;

  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));

    const pollRes = await fetch(
      `https://api.talesofai.com/v1/artifact/task/${taskUuid}`,
      { headers: HEADERS }
    );

    if (!pollRes.ok) {
      const text = await pollRes.text();
      console.error(`Error polling task (${pollRes.status}): ${text}`);
      process.exit(1);
    }

    const pollData = await pollRes.json();
    const status = pollData.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      continue;
    }

    // Done — extract image URL
    const url =
      pollData.artifacts?.[0]?.url || pollData.result_image_url;

    if (!url) {
      console.error("Error: No image URL in response:", JSON.stringify(pollData));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error("Error: Timed out waiting for image generation.");
  process.exit(1);
}

main().catch((err) => {
  console.error("Unexpected error:", err);
  process.exit(1);
});
