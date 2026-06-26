/**
 * Clawdy Selfie - reference-image edit only
 *
 * Uses fal.ai xAI Grok Imagine EDIT endpoint with a single fixed male reference image.
 * No text-to-image fallback.
 */

import { execFile } from "child_process";
import { promisify } from "util";
import fs from "fs";
import path from "path";

const execFileAsync = promisify(execFile);

interface GrokImagineImage {
  url: string;
  content_type: string;
  file_name?: string;
  width: number;
  height: number;
}

interface GrokImagineResponse {
  images: GrokImagineImage[];
  revised_prompt?: string;
  error?: string;
  detail?: string;
}

type OutputFormat = "jpeg" | "png" | "webp";

action();

async function action() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log("Usage: ts-node clawdy-selfie.ts <prompt> <channel> [caption] [output_format]");
    process.exit(1);
  }

  const [promptRaw, channel, caption = "For you", outputFormat = "jpeg"] = args;
  const falKey = process.env.FAL_KEY;
  if (!falKey) throw new Error("FAL_KEY environment variable not set");

  const skillDir = path.resolve(__dirname, "..");
  const referencePath = path.join(skillDir, "assets", "clawdy.png");
  const referenceBuf = fs.readFileSync(referencePath);
  const dataUrl = `data:image/jpeg;base64,${referenceBuf.toString("base64")}`;

  const mode = /outfit|wearing|jacket|hoodie|suit|mirror|full-body|fashion/i.test(promptRaw)
    ? "mirror"
    : "direct";

  const baseLock = "same exact person as the reference image; preserve the exact same male identity, same face, same eyes, same nose, same eyebrows, same hairstyle, same skin tone, same jawline, same facial structure, same age, same vibe. clearly male. handsome young man. do not change identity. do not feminize. not female. not woman. not a different model. not a different person.";

  const prompt = mode === "mirror"
    ? `Edit this SAME exact person into a mirror selfie. ${baseLock} Requested variation: ${promptRaw}. Keep it realistic and tasteful.`
    : `Edit this SAME exact person into a direct selfie. ${baseLock} Requested variation: ${promptRaw}. Keep it realistic and tasteful.`;

  const response = await fetch("https://fal.run/xai/grok-imagine-image/edit", {
    method: "POST",
    headers: {
      Authorization: `Key ${falKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      image_url: dataUrl,
      prompt,
      num_images: 1,
      output_format: outputFormat,
    }),
  });

  const body = (await response.json()) as GrokImagineResponse;
  if (!response.ok || body.error || body.detail || !body.images?.[0]?.url) {
    throw new Error(`Reference-edit generation failed: ${body.error || body.detail || JSON.stringify(body)}`);
  }

  const imageUrl = body.images[0].url;
  const imgResp = await fetch(imageUrl);
  if (!imgResp.ok) throw new Error(`Failed to download generated image: ${imgResp.status}`);
  const arr = await imgResp.arrayBuffer();
  const ext = outputFormat === "jpeg" ? "jpg" : outputFormat;
  const localFile = path.join(process.env.TMPDIR || "/tmp", `clawdy-selfie-${Date.now()}.${ext}`);
  fs.writeFileSync(localFile, Buffer.from(arr));

  await execFileAsync("openclaw", [
    "message",
    "send",
    "--action",
    "send",
    "--channel",
    channel,
    "--message",
    caption,
    "--filePath",
    localFile,
  ]);

  console.log(JSON.stringify({ success: true, imageUrl, localFile, channel, mode }, null, 2));
}
