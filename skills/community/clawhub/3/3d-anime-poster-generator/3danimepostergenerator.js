#!/usr/bin/env node

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = "portrait";
let token = null;
let ref = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--token" && i + 1 < args.length) {
    token = args[++i];
  } else if (args[i] === "--size" && i + 1 < args.length) {
    size = args[++i];
  } else if (args[i] === "--ref" && i + 1 < args.length) {
    ref = args[++i];
  } else if (!prompt && !args[i].startsWith("--")) {
    prompt = args[i];
  }
}

const TOKEN = token;

if (!TOKEN) {
  console.error("\n\u2717 Token required. Pass via: --token YOUR_TOKEN");
  console.error("  Get yours at: https://www.neta.art/open/");
  process.exit(1);
}

if (!prompt) {
  prompt =
    "3D anime poster, volumetric lighting, cinematic depth of field, vibrant colors, dynamic composition, detailed character art, cyberpunk-infused atmosphere, dramatic scene layout, high detail rendering";
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const chosen = SIZES[size] || SIZES.portrait;

const HEADERS = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

async function createImage() {
  const body = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width: chosen.width,
    height: chosen.height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };

  if (ref) {
    body.inherit_params = {
      collection_uuid: ref,
      picture_uuid: ref,
    };
  }

  console.error(`Creating 3D anime poster (${size} ${chosen.width}x${chosen.height})...`);
  console.error(`Prompt: ${prompt}`);

  const res = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error(`\u2717 Image creation failed (${res.status}): ${text}`);
    process.exit(1);
  }

  const data = await res.json();
  const taskUuid = typeof data === "string" ? data : data.task_uuid;

  if (!taskUuid) {
    console.error("\u2717 No task_uuid returned from API");
    console.error(JSON.stringify(data));
    process.exit(1);
  }

  console.error(`Task UUID: ${taskUuid}`);
  console.error("Polling for result...");

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(
      `https://api.talesofai.com/v1/artifact/task/${taskUuid}`,
      { headers: HEADERS }
    );

    if (!pollRes.ok) {
      console.error(`Poll error (${pollRes.status}), retrying...`);
      continue;
    }

    const pollData = await pollRes.json();
    const status = pollData.task_status;

    if (status === "PENDING" || status === "MODERATION") {
      console.error(`  Status: ${status} (attempt ${attempt + 1}/90)`);
      continue;
    }

    const imageUrl =
      (pollData.artifacts && pollData.artifacts[0] && pollData.artifacts[0].url) ||
      pollData.result_image_url;

    if (imageUrl) {
      console.log(imageUrl);
      process.exit(0);
    } else {
      console.error("\u2717 Task completed but no image URL found");
      console.error(JSON.stringify(pollData));
      process.exit(1);
    }
  }

  console.error("\u2717 Timed out waiting for image (180s)");
  process.exit(1);
}

createImage();
