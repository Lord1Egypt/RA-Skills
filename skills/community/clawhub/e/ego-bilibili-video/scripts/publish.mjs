#!/usr/bin/env node
// Entry: parse flags, validate locally, then run post-video.mjs inside ego-browser.
// Without --yes: login-check + plan only, exit 3. With --yes: real submission.
import { existsSync, readFileSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runEgoFile } from "./lib/run-ego.mjs";
import { PUBLISH_CONFIG_PATH, imageDimsFromBuffer, parsePublishArgs, planBody, publishMode, validatePublishInput } from "./lib/pure.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

function coverInfo(p) {
  if (!p) return { exists: false, dims: null };
  const exists = existsSync(p);
  let dims = null;
  if (exists) {
    try {
      dims = imageDimsFromBuffer(readFileSync(p));
    } catch {
      dims = null;
    }
  }
  return { exists, dims };
}

async function main() {
  const parsed = parsePublishArgs(process.argv.slice(2));
  if (parsed.error) {
    console.error(JSON.stringify({ ok: false, error: parsed.error }));
    process.exit(1);
  }
  const a = parsed.args;

  const videoExists = Boolean(a.video) && existsSync(a.video);
  const videoSize = videoExists ? statSync(a.video).size : 0;
  const c43 = coverInfo(a.cover43);
  const c169 = coverInfo(a.cover169);
  if (a.cover43 && !c43.exists) {
    console.error(JSON.stringify({ ok: false, error: `封面不存在: ${a.cover43}` }));
    process.exit(1);
  }
  if (a.cover169 && !c169.exists) {
    console.error(JSON.stringify({ ok: false, error: `封面不存在: ${a.cover169}` }));
    process.exit(1);
  }

  const checked = validatePublishInput({
    video: a.video,
    title: a.title,
    desc: a.desc,
    tags: a.tags,
    cover43: a.cover43,
    cover169: a.cover169,
    cover43Dims: c43.dims,
    cover169Dims: c169.dims,
    videoExists,
    videoSize,
  });
  if (checked.error) {
    console.error(JSON.stringify({ ok: false, error: checked.error }));
    process.exit(1);
  }

  if (publishMode({ yes: a.yes, stopBeforeSubmit: a.stopBeforeSubmit }) === "plan") {
    console.log(JSON.stringify(planBody({
      video: a.video,
      sizeMB: checked.sizeMB,
      title: a.title,
      desc: a.desc,
      tags: a.tags,
      cover43: a.cover43,
      cover169: a.cover169,
      spaceId: a.spaceId || null,
      declare: a.declare,
      type: a.type,
    })));
    process.exit(3);
  }

  writeFileSync(PUBLISH_CONFIG_PATH, JSON.stringify({
    video: a.video,
    title: a.title,
    desc: a.desc,
    tags: checked.tagList,
    cover43: a.cover43,
    cover169: a.cover169,
    type: a.type,
    declare: a.declare,
    keep: a.keep,
    yes: a.yes === true && a.stopBeforeSubmit !== true,
    stopBeforeSubmit: a.stopBeforeSubmit === true,
    spaceId: a.spaceId || 0,
  }));

  const code = await runEgoFile(path.join(here, "post-video.mjs"), { command: "publish" });
  process.exit(code);
}

main().catch((error) => {
  console.error(JSON.stringify({ ok: false, error: String((error && error.message) || error) }));
  process.exit(1);
});
