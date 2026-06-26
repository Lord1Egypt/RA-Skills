#!/usr/bin/env node
import fs from "fs/promises";
import path from "path";
import process from "process";

const args = new Map();
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith("--")) {
    const key = a.slice(2);
    const val = process.argv[i + 1] && !process.argv[i + 1].startsWith("--") ? process.argv[++i] : "true";
    args.set(key, val);
  }
}

const root = path.resolve(args.get("root") || process.cwd());
const registryPath = path.resolve(args.get("registry") || path.join(root, "dist", "skills", "registry.json"));
const skillsDir = path.resolve(args.get("skills-dir") || path.join(root, "dist", "skills"));
const playbooksDir = path.resolve(args.get("playbooks-dir") || path.join(root, "dist", "playbooks"));

const requiredSkillFields = [
  "id",
  "name",
  "version",
  "description",
  "allowedTools",
  "input_schema",
  "output_schema",
];

const errors = [];
const warnings = [];

function err(msg) {
  errors.push(msg);
}
function warn(msg) {
  warnings.push(msg);
}

async function readJson(filePath) {
  try {
    const raw = await fs.readFile(filePath, "utf8");
    return JSON.parse(raw);
  } catch (e) {
    err(`JSON 读取失败: ${filePath} (${e.message})`);
    return null;
  }
}

function isNonEmptyString(v) {
  return typeof v === "string" && v.trim().length > 0;
}

function isStringArray(v) {
  return Array.isArray(v) && v.every((x) => typeof x === "string");
}

function validateSchemaLike(schema, fieldName, filePath) {
  if (schema == null || typeof schema !== "object") {
    err(`缺少或无效的 ${fieldName}: ${filePath}`);
    return;
  }
  if (schema.type && schema.type !== "object") {
    warn(`${fieldName}.type 不是 "object": ${filePath}`);
  }
}

async function main() {
  const registry = await readJson(registryPath);
  if (!registry) {
    finish();
    return;
  }

  if (!Array.isArray(registry.skills)) {
    err(`registry.skills 不是数组: ${registryPath}`);
    finish();
    return;
  }

  const registryNames = new Set();
  const registryFiles = new Set();
  for (const entry of registry.skills) {
    if (!entry || typeof entry !== "object") {
      err(`registry.skills 包含非对象条目: ${registryPath}`);
      continue;
    }
    if (!isNonEmptyString(entry.name)) {
      err(`registry 中缺少 name: ${registryPath}`);
    }
    if (!isNonEmptyString(entry.file)) {
      err(`registry 中缺少 file: ${registryPath}`);
    }

    if (entry.name) {
      if (registryNames.has(entry.name)) {
        err(`registry 中 name 重复: ${entry.name}`);
      }
      registryNames.add(entry.name);
    }
    if (entry.file) {
      if (registryFiles.has(entry.file)) {
        err(`registry 中 file 重复: ${entry.file}`);
      }
      registryFiles.add(entry.file);
    }
  }

  const skills = [];
  const skillNames = new Set();
  const skillIds = new Set();

  for (const entry of registry.skills) {
    if (!entry?.file) continue;
    const skillPath = path.join(skillsDir, entry.file);
    try {
      await fs.access(skillPath);
    } catch {
      err(`registry 引用的 skill 文件不存在: ${skillPath}`);
      continue;
    }

    const skill = await readJson(skillPath);
    if (!skill) continue;

    for (const f of requiredSkillFields) {
      if (!(f in skill)) {
        err(`缺少字段 ${f}: ${skillPath}`);
      }
    }

    if (!isNonEmptyString(skill.id)) {
      err(`无效 id: ${skillPath}`);
    } else {
      if (skillIds.has(skill.id)) {
        err(`id 重复: ${skill.id} (${skillPath})`);
      }
      skillIds.add(skill.id);
    }

    if (!isNonEmptyString(skill.name)) {
      err(`无效 name: ${skillPath}`);
    } else {
      if (skillNames.has(skill.name)) {
        err(`name 重复: ${skill.name} (${skillPath})`);
      }
      skillNames.add(skill.name);
    }

    if (entry.name && skill.name && entry.name !== skill.name) {
      err(`registry.name 与 skill.name 不一致: ${entry.name} != ${skill.name} (${skillPath})`);
    }

    if (!isNonEmptyString(skill.version)) {
      err(`无效 version: ${skillPath}`);
    }
    if (!isNonEmptyString(skill.description)) {
      err(`无效 description: ${skillPath}`);
    }
    if (!isStringArray(skill.allowedTools)) {
      err(`allowedTools 必须是字符串数组: ${skillPath}`);
    }

    validateSchemaLike(skill.input_schema, "input_schema", skillPath);
    validateSchemaLike(skill.output_schema, "output_schema", skillPath);

    if (skill.supported_domains && !isStringArray(skill.supported_domains)) {
      warn(`supported_domains 不是字符串数组: ${skillPath}`);
    }
    if (skill.capabilities && !isStringArray(skill.capabilities)) {
      warn(`capabilities 不是字符串数组: ${skillPath}`);
    }

    skills.push(skill);
  }

  try {
    const files = await fs.readdir(skillsDir);
    for (const f of files) {
      if (!f.endsWith(".json")) continue;
      if (f === "registry.json") continue;
      if (!registryFiles.has(f)) {
        warn(`技能文件未被 registry 收录: ${path.join(skillsDir, f)}`);
      }
    }
  } catch {
    warn(`无法读取技能目录: ${skillsDir}`);
  }

  try {
    await fs.access(playbooksDir);
    const playbookFiles = (await fs.readdir(playbooksDir)).filter((f) => f.endsWith(".json"));
    for (const f of playbookFiles) {
      const p = path.join(playbooksDir, f);
      const pb = await readJson(p);
      if (!pb) continue;
      if (Array.isArray(pb.requires_skills)) {
        for (const s of pb.requires_skills) {
          if (!skillNames.has(s)) {
            err(`playbook 引用不存在的 skill: ${s} (${p})`);
          }
        }
      }
    }
  } catch {
  }

  finish();
}

function finish() {
  if (warnings.length) {
    console.warn("WARNINGS:");
    for (const w of warnings) console.warn(`- ${w}`);
  }
  if (errors.length) {
    console.error("ERRORS:");
    for (const e of errors) console.error(`- ${e}`);
    console.error(`\n校验失败: ${errors.length} 个错误`);
    process.exit(1);
  } else {
    console.log("校验通过");
    process.exit(0);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
