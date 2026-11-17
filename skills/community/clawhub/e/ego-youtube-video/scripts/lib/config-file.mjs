import fs from "node:fs";
import path from "node:path";
import { PUBLISH_CONFIG_PATH, parsePublishArgs, validatePublishInput } from "./pure.mjs";

function writeJson(file, data, io) {
  io.mkdirSync(path.dirname(file), { recursive: true });
  io.writeFileSync(file, `${JSON.stringify(data)}\n`);
}

export function writePublishConfigSync(argv, deps = {}) {
  const parsed = parsePublishArgs(argv);
  const pathMod = deps.path || path;
  const video = pathMod.resolve(parsed.video);
  const thumbnail = parsed.thumbnail ? pathMod.resolve(parsed.thumbnail) : "";
  const io = deps.fs || fs;
  const exists = deps.exists ? deps.exists(video) : io.existsSync(video);
  const thumbExists = !thumbnail || (deps.thumbExists ? deps.thumbExists(thumbnail) : io.existsSync(thumbnail));
  let sizeBytes = 0;
  if (exists) sizeBytes = deps.sizeBytes != null ? deps.sizeBytes : io.statSync(video).size;
  const checked = validatePublishInput({
    video,
    title: parsed.title,
    description: parsed.description,
    tags: parsed.tags,
    visibility: parsed.visibility,
    thumbnail,
    madeForKids: parsed.madeForKids,
    exists,
    thumbExists,
    sizeBytes,
  });
  if (!checked.ok) {
    const error = new Error(checked.error);
    error.exitCode = 1;
    throw error;
  }
  const file = deps.file || PUBLISH_CONFIG_PATH;
  const config = {
    video,
    title: parsed.title.trim(),
    description: parsed.description || "",
    tags: checked.tags,
    visibility: checked.visibility,
    thumbnail,
    madeForKids: checked.madeForKids,
    spaceId: parsed.spaceId,
    keep: parsed.keep,
  };
  writeJson(file, config, io);
  return { file, config, sizeMB: checked.sizeMB };
}

export function readConfigSync(file, io = fs) {
  return JSON.parse(io.readFileSync(file, "utf8"));
}
