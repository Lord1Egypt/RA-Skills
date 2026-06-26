#!/usr/bin/env node
import https from "https";

// --- CLI parsing ---
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

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error("\n✗ Token required. Pass via: --token YOUR_TOKEN");
  console.error("  Get yours at: https://www.neta.art/open/");
  process.exit(1);
}

if (!prompt) {
  console.error("\n✗ Prompt required as the first positional argument.");
  console.error('  Example: node bookcovergenerator.js "your prompt" --token YOUR_TOKEN');
  process.exit(1);
}

// --- Size map ---
const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const dims = SIZES[size] || SIZES.portrait;

// --- HTTP helpers ---
function request(method, url, body) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method,
      headers: {
        "x-token": TOKEN,
        "x-platform": "nieta-app/web",
        "content-type": "application/json",
      },
    };
    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data.trim());
        }
      });
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// --- Main ---
async function main() {
  // Build request body
  const body = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width: dims.width,
    height: dims.height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };

  if (refUuid) {
    body.inherit_params = {
      collection_uuid: refUuid,
      picture_uuid: refUuid,
    };
  }

  // Submit job
  const submitRes = await request("POST", "https://api.talesofai.com/v3/make_image", body);

  let taskUuid;
  if (typeof submitRes === "string") {
    taskUuid = submitRes;
  } else if (submitRes && submitRes.task_uuid) {
    taskUuid = submitRes.task_uuid;
  } else {
    console.error("✗ Unexpected response from image API:", JSON.stringify(submitRes));
    process.exit(1);
  }

  // Poll for result
  const MAX_ATTEMPTS = 90;
  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    await sleep(2000);

    const pollRes = await request(
      "GET",
      `https://api.talesofai.com/v1/artifact/task/${taskUuid}`,
      null
    );

    const status = pollRes && pollRes.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      continue;
    }

    // Done — extract URL
    let imageUrl = null;
    if (pollRes.artifacts && pollRes.artifacts[0] && pollRes.artifacts[0].url) {
      imageUrl = pollRes.artifacts[0].url;
    } else if (pollRes.result_image_url) {
      imageUrl = pollRes.result_image_url;
    }

    if (imageUrl) {
      console.log(imageUrl);
      process.exit(0);
    } else {
      console.error("✗ Task finished but no image URL found:", JSON.stringify(pollRes));
      process.exit(1);
    }
  }

  console.error("✗ Timed out waiting for image generation.");
  process.exit(1);
}

main().catch((err) => {
  console.error("✗ Error:", err.message || err);
  process.exit(1);
});
