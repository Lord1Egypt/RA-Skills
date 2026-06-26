import {
  buildTemplateVariables,
  renderTemplate
} from "../chunk-7766SIJP.js";

// src/commands/template.ts
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
var VAULT_CONFIG_FILE = ".clawvault.json";
var TEMPLATE_EXTENSION = ".md";
function resolveBuiltinTemplatesDir(override) {
  if (override) {
    const resolved = path.resolve(override);
    return fs.existsSync(resolved) ? resolved : null;
  }
  const moduleDir = path.dirname(fileURLToPath(import.meta.url));
  const candidates = [
    path.resolve(moduleDir, "../templates"),
    path.resolve(moduleDir, "../../templates")
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
      return candidate;
    }
  }
  return null;
}
function findVaultRoot(start) {
  let current = path.resolve(start);
  while (true) {
    if (fs.existsSync(path.join(current, VAULT_CONFIG_FILE))) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) return null;
    current = parent;
  }
}
function resolveVaultPath(options) {
  if (options.vaultPath) {
    return path.resolve(options.vaultPath);
  }
  const envPath = process.env.CLAWVAULT_PATH;
  if (envPath) {
    return path.resolve(envPath);
  }
  const cwd = options.cwd ?? process.cwd();
  return findVaultRoot(cwd);
}
function normalizeTemplateName(name) {
  const base = path.basename(name, path.extname(name));
  return base.trim();
}
function slugify(text) {
  return text.toLowerCase().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-").trim();
}
function listTemplateFiles(dir, ignore) {
  const entries = /* @__PURE__ */ new Map();
  if (!fs.existsSync(dir)) return entries;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isFile() || !entry.name.endsWith(TEMPLATE_EXTENSION)) continue;
    const name = normalizeTemplateName(entry.name);
    if (!name) continue;
    if (ignore?.has(name)) continue;
    entries.set(name, path.join(dir, entry.name));
  }
  return entries;
}
function buildTemplateIndex(options) {
  const index = /* @__PURE__ */ new Map();
  const builtinDir = resolveBuiltinTemplatesDir(options.builtinDir);
  if (builtinDir) {
    const ignore = /* @__PURE__ */ new Set(["daily"]);
    for (const [name, filePath] of listTemplateFiles(builtinDir, ignore)) {
      index.set(name, filePath);
    }
  }
  const vaultPath = resolveVaultPath(options);
  if (vaultPath) {
    const vaultTemplatesDir = path.join(vaultPath, "templates");
    for (const [name, filePath] of listTemplateFiles(vaultTemplatesDir)) {
      index.set(name, filePath);
    }
  }
  return index;
}
function listTemplates(options = {}) {
  const index = buildTemplateIndex(options);
  return [...index.keys()].sort();
}
function createFromTemplate(name, options = {}) {
  const templateName = normalizeTemplateName(name);
  if (!templateName) {
    throw new Error("Template name is required.");
  }
  const index = buildTemplateIndex(options);
  const templatePath = index.get(templateName);
  if (!templatePath) {
    const available = [...index.keys()].sort();
    const hint = available.length > 0 ? ` Available: ${available.join(", ")}` : "";
    throw new Error(`Template not found: ${templateName}.${hint}`);
  }
  const raw = fs.readFileSync(templatePath, "utf-8");
  const now = /* @__PURE__ */ new Date();
  const date = now.toISOString().split("T")[0];
  const type = options.type ?? templateName;
  const title = options.title ?? `${type} ${date}`.trim();
  const variables = buildTemplateVariables({ title, type, date }, now);
  const rendered = renderTemplate(raw, variables);
  const cwd = options.cwd ?? process.cwd();
  const slug = slugify(title) || slugify(templateName) || `template-${date}`;
  const outputPath = path.join(cwd, `${slug}${TEMPLATE_EXTENSION}`);
  if (fs.existsSync(outputPath)) {
    throw new Error(`File already exists: ${outputPath}`);
  }
  fs.writeFileSync(outputPath, rendered);
  return { outputPath, templatePath, variables };
}
function addTemplate(file, options) {
  const name = normalizeTemplateName(options.name);
  if (!name) {
    throw new Error("Template name is required.");
  }
  const vaultPath = resolveVaultPath(options);
  if (!vaultPath) {
    throw new Error("No vault found. Set CLAWVAULT_PATH or use --vault.");
  }
  const cwd = options.cwd ?? process.cwd();
  const sourcePath = path.resolve(cwd, file);
  if (!fs.existsSync(sourcePath) || !fs.statSync(sourcePath).isFile()) {
    throw new Error(`Template file not found: ${sourcePath}`);
  }
  const templatesDir = path.join(vaultPath, "templates");
  fs.mkdirSync(templatesDir, { recursive: true });
  const targetPath = path.join(templatesDir, `${name}${TEMPLATE_EXTENSION}`);
  if (fs.existsSync(targetPath) && !options.overwrite) {
    throw new Error(`Template already exists: ${targetPath}`);
  }
  fs.copyFileSync(sourcePath, targetPath);
  return { templatePath: targetPath, name };
}
export {
  addTemplate,
  createFromTemplate,
  listTemplates
};
