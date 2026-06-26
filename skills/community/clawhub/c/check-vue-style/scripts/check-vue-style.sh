#!/usr/bin/env bash
set -euo pipefail

echo "=== Vue .vue 样式规范检查 ==="
echo ""

if ! command -v node >/dev/null 2>&1; then
  echo "❌ 未检测到 Node.js，无法执行检查脚本。"
  exit 2
fi

node - <<'NODE'
const fs = require("fs");
const path = require("path");

const root = process.cwd();

function collectVueFiles(dir, result) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (
        entry.name === "node_modules" ||
        entry.name === ".git" ||
        entry.name === "dist" ||
        entry.name === "build"
      ) {
        continue;
      }
      collectVueFiles(full, result);
      continue;
    }
    if (entry.isFile() && entry.name.endsWith(".vue")) {
      result.push(path.relative(root, full));
    }
  }
}

const files = [];
collectVueFiles(root, files);

if (files.length === 0) {
  console.log("✅ 未找到 .vue 文件，无需检查。");
  process.exit(0);
}

const kebabCase = /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;
let warningCount = 0;

function lineFromIndex(source, index) {
  return source.slice(0, index).split("\n").length;
}

for (const file of files) {
  const abs = path.resolve(file);
  let source = "";
  try {
    source = fs.readFileSync(abs, "utf8");
  } catch (err) {
    console.log(`${file}:1: ⚠️ 读取文件失败：${String(err.message || err)}`);
    warningCount += 1;
    continue;
  }

  const styleRe = /<style\b([^>]*)>([\s\S]*?)<\/style>/gi;
  let styleFound = false;
  let m;

  while ((m = styleRe.exec(source)) !== null) {
    styleFound = true;
    const attrs = m[1] || "";
    const css = m[2] || "";
    const styleStartLine = lineFromIndex(source, m.index);

    if (!/\bscoped\b/i.test(attrs)) {
      console.log(`${file}:${styleStartLine}: ⚠️ 建议使用 <style scoped>，避免样式污染。`);
      warningCount += 1;
    }

    const lines = css.split("\n");
    let depth = 0;
    let depthWarned = false;

    for (let i = 0; i < lines.length; i += 1) {
      const line = lines[i];
      const lineNo = styleStartLine + i + 1;

      if (/!important/.test(line)) {
        console.log(`${file}:${lineNo}: ⚠️ 避免使用 !important，建议通过选择器权重或结构优化解决。`);
        warningCount += 1;
      }

      if (/(^|[\s,{])#[A-Za-z_][\w-]*/.test(line)) {
        console.log(`${file}:${lineNo}: ⚠️ 避免使用 ID 选择器，建议改用 class。`);
        warningCount += 1;
      }

      if (/\/deep\/|>>>|::v-deep/.test(line)) {
        console.log(`${file}:${lineNo}: ⚠️ 检测到深度选择器，建议减少穿透并优化组件样式边界。`);
        warningCount += 1;
      }

      const classRe = /\.([A-Za-z_][\w-]*)/g;
      let clsMatch;
      while ((clsMatch = classRe.exec(line)) !== null) {
        const cls = clsMatch[1];
        if (!kebabCase.test(cls)) {
          console.log(`${file}:${lineNo}: ⚠️ 类名 ".${cls}" 建议使用 kebab-case（示例：user-card-title）。`);
          warningCount += 1;
        }
      }

      // 粗略嵌套层级检查：按大括号深度统计。
      for (const ch of line) {
        if (ch === "{") depth += 1;
        if (ch === "}") depth = Math.max(0, depth - 1);
      }
      if (depth > 3 && !depthWarned) {
        console.log(`${file}:${lineNo}: ⚠️ 样式嵌套超过 3 层，建议拆分选择器降低复杂度。`);
        warningCount += 1;
        depthWarned = true;
      }
    }
  }

  if (!styleFound) {
    console.log(`${file}:1: ⚠️ 未发现 <style> 区块。`);
    warningCount += 1;
  }
}

if (warningCount === 0) {
  console.log("✅ 未发现样式规范问题。");
  process.exit(0);
}

console.log("");
console.log(`检查完成：共发现 ${warningCount} 条样式规范提示。`);
process.exit(1);
NODE
