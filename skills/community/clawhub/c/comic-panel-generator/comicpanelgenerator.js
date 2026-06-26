#!/usr/bin/env node
import https from "https";

const args = process.argv.slice(2);

let prompt = null;
let size = "portrait";
let tokenFlag = null;
let refUUID = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--size" && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === "--token" && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === "--ref" && args[i + 1]) {
    refUUID = args[++i];
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
  prompt =
    "comic book panel illustration, bold ink outlines, dynamic composition, manga style, expressive characters, cel shading, dramatic lighting, professional comic art, sequential storytelling panel";
}

const sizes = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const { width, height } = sizes[size] || sizes.portrait;

const HEADERS = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

function request(method, urlStr, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method,
      headers: HEADERS,
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

async function main() {
  const makeBody = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };

  if (refUUID) {
    makeBody.inherit_params = {
      collection_uuid: refUUID,
      picture_uuid: refUUID,
    };
  }

  let makeRes;
  try {
    makeRes = await request(
      "POST",
      "https://api.talesofai.com/v3/make_image",
      makeBody
    );
  } catch (err) {
    console.error("✗ Failed to submit job:", err.message);
    process.exit(1);
  }

  const taskUUID =
    typeof makeRes === "string"
      ? makeRes
      : makeRes.task_uuid || makeRes.taskUUID;

  if (!taskUUID) {
    console.error("✗ No task_uuid in response:", JSON.stringify(makeRes));
    process.exit(1);
  }

  console.error(`Generating... (task: ${taskUUID})`);

  const pollURL = `https://api.talesofai.com/v1/artifact/task/${taskUUID}`;
  const MAX_ATTEMPTS = 90;

  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    await sleep(2000);
    let pollRes;
    try {
      pollRes = await request("GET", pollURL, null);
    } catch (err) {
      console.error("✗ Poll error:", err.message);
      process.exit(1);
    }

    const status = pollRes.task_status;
    if (status === "PENDING" || status === "MODERATION") {
      continue;
    }

    const url =
      pollRes.artifacts?.[0]?.url || pollRes.result_image_url;

    if (!url) {
      console.error("✗ No image URL in response:", JSON.stringify(pollRes));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error("✗ Timed out waiting for image generation.");
  process.exit(1);
}

main();
