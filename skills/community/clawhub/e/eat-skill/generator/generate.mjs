#!/usr/bin/env node

/**
 * 干饭.skill — 餐馆 Skill 生成器
 *
 * 用法：
 *   node generate.mjs --input restaurant.yaml --output SKILL.md
 *   node generate.mjs --input restaurant.yaml --outdir ../restaurants/my-restaurant/
 *   node generate.mjs --input restaurant.json
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { resolve, dirname, extname, basename } from "path";
import { fileURLToPath } from "url";
import { parseArgs } from "util";

const __dirname = dirname(fileURLToPath(import.meta.url));

const { values: args } = parseArgs({
  options: {
    input: { type: "string", short: "i" },
    output: { type: "string", short: "o" },
    outdir: { type: "string", short: "d" },
    help: { type: "boolean", short: "h" },
  },
});

if (args.help || !args.input) {
  console.log(`
🍜 干饭.skill — 餐馆 Skill 生成器

用法：
  node generate.mjs --input <restaurant.yaml|.json> [--output SKILL.md] [--outdir dir/]

参数：
  -i, --input   餐馆信息文件路径（YAML 或 JSON）
  -o, --output  输出文件路径（默认 stdout）
  -d, --outdir  输出目录（自动创建 {slug}/SKILL.md）
  -h, --help    显示帮助

示例：
  node generate.mjs -i my-restaurant.yaml -o SKILL.md
  node generate.mjs -i data.json -d ../restaurants/
  `);
  process.exit(0);
}

function parseYaml(text) {
  const result = {};
  let currentKey = null;
  let currentList = null;
  let currentObj = null;
  let inMultiline = false;
  let multilineKey = null;
  let multilineText = "";

  for (const rawLine of text.split("\n")) {
    if (rawLine.trim().startsWith("#") || rawLine.trim() === "") {
      if (inMultiline && rawLine.trim() === "") {
        multilineText += "\n";
      }
      continue;
    }

    if (inMultiline) {
      if (rawLine.startsWith("  ") || rawLine.startsWith("\t")) {
        multilineText += rawLine.trimStart() + "\n";
        continue;
      } else {
        result[multilineKey] = multilineText.trim();
        inMultiline = false;
        multilineKey = null;
        multilineText = "";
      }
    }

    const kvMatch = rawLine.match(/^(\w[\w_]*)\s*:\s*(.*)$/);
    if (kvMatch) {
      const [, key, rawVal] = kvMatch;
      const val = rawVal.replace(/^["']|["']$/g, "").trim();

      if (val === "|") {
        inMultiline = true;
        multilineKey = key;
        multilineText = "";
        currentKey = null;
        currentList = null;
        continue;
      }

      if (val === "" || val === undefined) {
        currentKey = key;
        currentList = null;
        currentObj = null;
        if (!result[key]) result[key] = [];
        continue;
      }

      result[key] = val === "true" ? true : val === "false" ? false : val;
      currentKey = null;
      currentList = null;
      continue;
    }

    const listItemMatch = rawLine.match(/^\s+-\s+(.*)/);
    if (listItemMatch && currentKey) {
      const val = listItemMatch[1].replace(/^["']|["']$/g, "").trim();
      if (!Array.isArray(result[currentKey])) result[currentKey] = [];

      const nestedKv = val.match(/^(\w+)\s*:\s*(.+)$/);
      if (nestedKv) {
        const [, nKey, nVal] = nestedKv;
        const obj = {};
        obj[nKey] = nVal.replace(/^["']|["']$/g, "").trim();
        currentObj = obj;
        result[currentKey].push(obj);
      } else {
        result[currentKey].push(val);
        currentObj = null;
      }
      continue;
    }

    // Handle nested key: value under a parent key (non-list, e.g., wifi.name)
    const nestedKvMatch = rawLine.match(/^\s+(\w[\w_]*)\s*:\s*(.*)$/);
    if (nestedKvMatch) {
      const [, nKey, nRawVal] = nestedKvMatch;
      const nVal = nRawVal.replace(/^["']|["']$/g, "").trim();

      if (currentObj) {
        currentObj[nKey] =
          nVal === "true" ? true : nVal === "false" ? false : nVal;
      } else if (currentKey && !Array.isArray(result[currentKey])) {
        if (typeof result[currentKey] !== "object") result[currentKey] = {};
        result[currentKey][nKey] =
          nVal === "true" ? true : nVal === "false" ? false : nVal;
      } else if (currentKey && Array.isArray(result[currentKey]) && result[currentKey].length === 0) {
        result[currentKey] = {};
        result[currentKey][nKey] =
          nVal === "true" ? true : nVal === "false" ? false : nVal;
      }
    }
  }

  if (inMultiline && multilineKey) {
    result[multilineKey] = multilineText.trim();
  }

  return result;
}

function loadInput(filePath) {
  const content = readFileSync(filePath, "utf-8");
  const ext = extname(filePath).toLowerCase();

  if (ext === ".json") {
    return JSON.parse(content);
  }
  return parseYaml(content);
}

function buildKeywords(data) {
  const kw = new Set();
  if (data.name) kw.add(data.name);
  if (data.slug) kw.add(data.slug);
  if (data.category) kw.add(data.category);
  if (data.city) kw.add(data.city);
  if (data.district) kw.add(data.district);

  kw.add("吃什么");
  kw.add("吃饭");
  kw.add("美食");

  if (data.tags && Array.isArray(data.tags)) {
    data.tags.forEach((t) => kw.add(t));
  }
  if (data.nearby_landmarks) kw.add(data.nearby_landmarks);

  return [...kw];
}

function renderSignatureDishes(dishes) {
  if (!dishes || !Array.isArray(dishes) || dishes.length === 0) return "";
  return dishes
    .map((d) => {
      let line = `- **${d.name}**`;
      if (d.price) line += ` ¥${d.price}`;
      if (d.description) line += ` — ${d.description}`;
      return line;
    })
    .join("\n");
}

function generateSkill(data) {
  const keywords = buildKeywords(data);

  let md = `---
name: ${data.slug || data.name}
description: ${data.name}信息查询。获取地址、营业时间、菜单、推荐菜、人均消费等。用户询问"${data.name}在哪"、"${data.name}怎么样"、"${data.name}吃什么"时使用。
version: 0.1.0
alwaysApply: false
keywords:
${keywords.map((k) => `  - ${k}`).join("\n")}
---

# ${data.name} · Skill

## 基本信息

| 项目 | 内容 |
|------|------|
| 餐厅名称 | ${data.name} |
| 品类 | ${data.category || "-"} |
| 营业时间 | ${data.hours || "-"} |
| 地址 | ${data.address || "-"} |`;

  if (data.phone) md += `\n| 电话 | ${data.phone} |`;
  if (data.price_per_person) md += `\n| 人均 | ¥${data.price_per_person} |`;
  if (data.city) md += `\n| 城市 | ${data.city} · ${data.district || ""} |`;

  if (data.location_tips || data.transit || data.parking) {
    md += `\n\n## 怎么去\n`;
    if (data.location_tips) md += `\n${data.location_tips}`;
    if (data.nearby_landmarks)
      md += `\n\n附近地标：${data.nearby_landmarks}`;
    if (data.transit) md += `\n\n公共交通：${data.transit}`;
    if (data.parking) md += `\n\n停车：${data.parking}`;
  }

  if (
    data.signature_dishes &&
    Array.isArray(data.signature_dishes) &&
    data.signature_dishes.length > 0
  ) {
    md += `\n\n## 推荐菜\n\n${renderSignatureDishes(data.signature_dishes)}`;
  }

  if (data.delivery) {
    md += `\n\n## 外卖\n`;
    if (typeof data.delivery === "object") {
      const platforms = data.delivery.platforms;
      if (platforms && Array.isArray(platforms) && platforms.length > 0) {
        md += `\n可以点外卖：${platforms.join("、")}`;
      } else {
        md += `\n支持外卖。`;
      }
      if (data.delivery.range) md += `\n\n配送范围：${data.delivery.range}`;
    } else {
      md += `\n${typeof data.delivery === "string" ? data.delivery : "支持外卖"}`;
    }
  }

  if (data.booking) {
    md += `\n\n## 排队 / 预约\n`;
    if (typeof data.booking === "object") {
      if (data.booking.required === true || data.booking.required === "true") {
        md += `\n建议提前预约。`;
      } else {
        md += `\n不用预约，直接去。`;
      }
      if (data.booking.method) md += `排队方式：${data.booking.method}`;
    } else {
      md += `\n${data.booking}`;
    }
  }

  if (data.wifi) {
    md += `\n\n## Wi-Fi\n`;
    if (typeof data.wifi === "object") {
      if (data.wifi.name) md += `\nWi-Fi 名称：\`${data.wifi.name}\``;
      if (data.wifi.password) md += `\n密码：\`${data.wifi.password}\``;
    }
  }

  if (data.vibe) {
    md += `\n\n## 氛围\n\n${data.vibe}`;
  }

  if (
    data.suitable_for &&
    Array.isArray(data.suitable_for) &&
    data.suitable_for.length > 0
  ) {
    md += `\n\n适合：${data.suitable_for.join("、")}`;
  }

  if (data.special_notes) {
    md += `\n\n## 特别说明\n\n${data.special_notes}`;
  }

  const dishNames =
    data.signature_dishes && Array.isArray(data.signature_dishes)
      ? data.signature_dishes.map((d) => d.name).join("、")
      : "招牌菜";

  md += `

## 使用示例

### 用户问地址

> 用户：${data.name}在哪儿？

> ${data.name}在${data.address || "（地址）"}。${data.location_tips || ""}

### 用户问推荐

> 用户：${data.name}吃什么好？

> 推荐：${dishNames}，都不错。

### 用户问营业时间

> 用户：${data.name}几点关门？

> 营业时间是 ${data.hours || "（营业时间）"}。

## 能力边界

这个 Skill 只包含 ${data.name} 的基本信息。以下情况请引导用户自行确认：

- 实时排队人数、等位时间
- 临时歇业、节假日调整
- 菜品价格如有变动以店内为准
- 优惠活动、团购券信息

遇到不确定的问题，诚实说不知道，建议用户到店或搜大众点评确认。

---

> 由 [干饭.skill](https://github.com/funAgent/eat-skill) 生成`;

  if (data.contributor) {
    let cName, cNote;
    if (typeof data.contributor === "object") {
      cName = data.contributor.name;
      cNote = data.contributor.note;
    } else {
      cName = String(data.contributor);
    }
    if (cName) {
      md += `\n> 贡献者：${cName}`;
      if (cNote) md += `（${cNote}）`;
    }
  }

  md += "\n";
  return md;
}

const inputPath = resolve(args.input);
if (!existsSync(inputPath)) {
  console.error(`错误：文件不存在 ${inputPath}`);
  process.exit(1);
}

const data = loadInput(inputPath);
const skillMd = generateSkill(data);

if (args.outdir) {
  const slug = data.slug || data.name.toLowerCase().replace(/\s+/g, "-");
  const outDir = resolve(args.outdir, slug);
  mkdirSync(outDir, { recursive: true });
  const outPath = resolve(outDir, "SKILL.md");
  writeFileSync(outPath, skillMd, "utf-8");
  console.log(`✅ 已生成：${outPath}`);
} else if (args.output) {
  const outPath = resolve(args.output);
  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, skillMd, "utf-8");
  console.log(`✅ 已生成：${outPath}`);
} else {
  process.stdout.write(skillMd);
}
