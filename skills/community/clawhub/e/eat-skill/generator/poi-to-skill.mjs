#!/usr/bin/env node

/**
 * 干饭.skill — POI → 餐馆 Skill 转换器
 *
 * 把高德 API 返回的 POI 数据转换成标准的餐馆 SKILL.md。
 * 不自己调 API —— API 调用交给 amap-lbs-skill。
 *
 * 用法：
 *   # 从 amap-lbs-skill 的搜索结果转换
 *   node scripts/poi-search.js --keywords="饺子" --city="北京" | node poi-to-skill.mjs --outdir ../restaurants/
 *
 *   # 从 JSON 文件转换
 *   node poi-to-skill.mjs --input pois.json --outdir ../restaurants/
 *
 *   # 从 stdin 读取单个 POI JSON
 *   echo '{"name":"老王烤串","address":"望京SOHO","type":"烧烤"}' | node poi-to-skill.mjs
 */

import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { parseArgs } from "util";

const __dirname = dirname(fileURLToPath(import.meta.url));

const { values: args } = parseArgs({
  options: {
    input: { type: "string", short: "i" },
    outdir: { type: "string", short: "d" },
    output: { type: "string", short: "o" },
    help: { type: "boolean", short: "h" },
  },
});

if (args.help) {
  console.log(`
🍜 POI → 餐馆 Skill 转换器

把高德 POI 数据转成标准的餐馆 SKILL.md，不自己调 API。

用法：
  node poi-to-skill.mjs --input <pois.json> [--outdir restaurants/]
  cat pois.json | node poi-to-skill.mjs --outdir restaurants/

参数：
  -i, --input   POI JSON 文件（数组或单个对象）
  -d, --outdir  输出目录（自动创建 {slug}/SKILL.md）
  -o, --output  输出单个文件路径
  -h, --help    显示帮助

输入格式（高德 v5 POI 或简化格式均可）：
  {"name":"店名","address":"地址","type":"品类","tel":"电话",...}
  `);
  process.exit(0);
}

function makeSlug(name) {
  const ascii = name
    .toLowerCase()
    .replace(/[^a-zA-Z0-9]/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
  if (ascii && ascii !== "-") return ascii;
  return `restaurant-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
}

function parsePoi(poi) {
  return {
    name: poi.name || "",
    slug: poi.slug || makeSlug(poi.name || "unknown"),
    address: poi.address || poi.pname + poi.cityname + poi.adname || "",
    city: poi.cityname || poi.city || "",
    district: poi.adname || poi.district || "",
    category: (poi.type || poi.category || "").split(";").pop().split("/").pop(),
    phone: poi.tel || poi.phone || "",
    location: poi.location || "",
    rating: poi.biz_ext?.rating || poi.rating || "",
    price: poi.biz_ext?.cost || poi.price_per_person || poi.price || "",
    hours: poi.biz_ext?.open_time || poi.hours || "",
    distance: poi.distance || "",
    business_area: poi.business_area || "",
  };
}

function generateYaml(r) {
  return `name: "${r.name}"
slug: "${r.slug}"
category: "${r.category}"
city: "${r.city}"
district: "${r.district}"
address: "${r.address}"
hours: "${r.hours || "待确认"}"
${r.phone ? `phone: "${r.phone}"` : "# phone: 待补充"}
${r.price ? `price_per_person: "${r.price}"` : "# price_per_person: 待补充"}
${r.rating ? `# amap_rating: ${r.rating}` : ""}
${r.distance ? `# distance: ${r.distance}m` : ""}

signature_dishes:
  - name: "待补充"
    description: "欢迎补充推荐菜！"

tags:
  - "${r.category}"
  - "${r.district || r.city}"

contributor:
  name: "eat-skill"
  note: "由高德 POI 自动生成，推荐菜待社区补充"
`;
}

function generateSkillMd(r) {
  const today = new Date().toISOString().split("T")[0];
  const keywords = [r.name, r.category, r.city, r.district, "吃什么", "吃饭", "美食"].filter(Boolean);

  let md = `---
name: ${r.slug}
description: ${r.name}信息查询。地址、营业时间、人均消费等。
version: 0.1.0
alwaysApply: false
keywords:
${keywords.map((k) => `  - ${k}`).join("\n")}
---

# ${r.name} · Skill

> 🟡 骨架版 — 基础信息来自高德 API，推荐菜和氛围待社区补充

## 基本信息

| 项目 | 内容 |
|------|------|
| 餐厅名称 | ${r.name} |
| 品类 | ${r.category} |
| 地址 | ${r.address} |`;

  if (r.city) md += `\n| 城市 | ${r.city}${r.district ? " · " + r.district : ""} |`;
  if (r.hours) md += `\n| 营业时间 | ${r.hours} |`;
  if (r.phone) md += `\n| 电话 | ${r.phone} |`;
  if (r.price) md += `\n| 人均 | ¥${r.price} |`;
  if (r.rating) md += `\n| 评分 | ${r.rating} |`;

  md += `

## 推荐菜

> 📝 还没人补充推荐菜，来当第一个？
> 编辑这个文件或[提个 PR](https://github.com/funAgent/eat-skill/blob/main/CONTRIBUTING.md)

## 怎么去

${r.address}${r.business_area ? "（" + r.business_area + "附近）" : ""}
${r.location ? `\n📍 坐标：${r.location}（可用 amap-lbs-skill 导航）` : ""}

## 能力边界

这个 Skill 由高德 POI 自动生成（${today}），基础信息可靠，以下需补充：

- 🔴 推荐菜 / 菜单
- 🔴 氛围和适合场景
- 🟡 营业时间可能变动
- 🟡 人均价格仅供参考

---

> 由 [干饭.skill](https://github.com/funAgent/eat-skill) 自动生成
> 数据来源：高德地图 | ${today}
`;

  return md;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf-8");
}

async function main() {
  let raw;

  if (args.input) {
    raw = readFileSync(resolve(args.input), "utf-8");
  } else if (!process.stdin.isTTY) {
    raw = await readStdin();
  } else {
    console.error('❌ 需要输入数据。用 --input 指定文件，或从 stdin 管道输入。\n   node poi-to-skill.mjs --help');
    process.exit(1);
  }

  let pois;
  try {
    const parsed = JSON.parse(raw);
    if (parsed.pois) {
      pois = parsed.pois;
    } else if (Array.isArray(parsed)) {
      pois = parsed;
    } else {
      pois = [parsed];
    }
  } catch {
    console.error("❌ JSON 解析失败。确保输入是有效的 JSON。");
    process.exit(1);
  }

  const restaurants = pois.map(parsePoi);
  console.log(`📋 共 ${restaurants.length} 个 POI\n`);

  for (const r of restaurants) {
    const skillMd = generateSkillMd(r);
    const yamlData = generateYaml(r);

    if (args.outdir) {
      const dir = resolve(args.outdir, r.slug);
      mkdirSync(dir, { recursive: true });
      writeFileSync(resolve(dir, "SKILL.md"), skillMd, "utf-8");
      writeFileSync(resolve(dir, "restaurant-info.yaml"), yamlData, "utf-8");
      console.log(`   ✅ ${r.name} → ${r.slug}/`);
    } else if (args.output) {
      writeFileSync(resolve(args.output), skillMd, "utf-8");
      console.log(`   ✅ ${r.name} → ${args.output}`);
    } else {
      process.stdout.write(skillMd);
    }
  }

  if (args.outdir) {
    console.log(`\n🎉 已生成 ${restaurants.length} 个餐馆 Skill（骨架版）`);
    console.log("   推荐菜和氛围需要手动补充，或者让社区来贡献！");
  }
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});
