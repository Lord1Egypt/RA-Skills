#!/usr/bin/env node
import https from "https";

const args = process.argv.slice(2);

let prompt = null;
let size = "landscape";
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
    "fantasy world map, hand-drawn cartographic illustration, parchment texture, detailed terrain with mountains forests rivers and oceans, labeled cities and kingdoms, decorative compass rose, ornate borders, medieval fantasy aesthetic, bird's eye view, rich warm tones";
}

const TOKEN = tokenFlag;

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

const { width, height } = SIZES[size] || SIZES.landscape;

const HEADERS = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

function request(method, hostname, path, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const options = {
      hostname,
      path,
      method,
      headers: {
        ...HEADERS,
        ...(data ? { "content-length": Buffer.byteLength(data) } : {}),
      },
    };
    const req = https.request(options, (res) => {
      let raw = "";
      res.on("data", (chunk) => (raw += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(raw));
        } catch {
          resolve(raw.trim());
        }
      });
    });
    req.on("error", reject);
    if (data) req.write(data);
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

  if (refUuid) {
    makeBody.inherit_params = {
      collection_uuid: refUuid,
      picture_uuid: refUuid,
    };
  }

  const makeRes = await request(
    "POST",
    "api.talesofai.com",
    "/v3/make_image",
    makeBody
  );

  let taskUuid;
  if (typeof makeRes === "string") {
    taskUuid = makeRes;
  } else if (makeRes && makeRes.task_uuid) {
    taskUuid = makeRes.task_uuid;
  } else {
    console.error("✗ Failed to get task UUID:", JSON.stringify(makeRes));
    process.exit(1);
  }

  console.error(`Generating image... (task: ${taskUuid})`);

  for (let attempt = 0; attempt < 90; attempt++) {
    await sleep(2000);

    const poll = await request(
      "GET",
      "api.talesofai.com",
      `/v1/artifact/task/${taskUuid}`,
      null
    );

    const status = poll.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      process.stderr.write(".");
      continue;
    }

    process.stderr.write("\n");

    const url =
      poll.artifacts?.[0]?.url || poll.result_image_url;

    if (!url) {
      console.error("✗ No image URL in response:", JSON.stringify(poll));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error("\n✗ Timed out waiting for image generation.");
  process.exit(1);
}

main().catch((err) => {
  console.error("✗ Error:", err.message || err);
  process.exit(1);
});
