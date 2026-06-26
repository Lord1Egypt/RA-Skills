#!/usr/bin/env node
"use strict";

const fs = require("fs");

const DEFAULT_PLATFORMS = [
  "xiaohongshu",
  "douyin",
  "moments",
  "zhihu",
  "marketplace",
  "ads"
];

const PLATFORM_NAMES = {
  xiaohongshu: "小红书",
  douyin: "抖音",
  live: "直播",
  moments: "朋友圈",
  zhihu: "知乎",
  marketplace: "电商详情页",
  ads: "广告"
};

const CATEGORY_HASHTAGS = {
  "美妆": ["#美妆测评", "#护肤分享", "#好物分享", "#通勤护肤"],
  "数码": ["#数码好物", "#开箱测评", "#效率工具", "#科技生活"],
  "家居": ["#家居好物", "#生活方式", "#提升幸福感", "#收纳灵感"],
  "食品": ["#零食分享", "#办公室零食", "#囤货清单", "#真实测评"],
  "服装": ["#穿搭分享", "#通勤穿搭", "#质感单品", "#ootd"]
};

const REQUIRED_FIELDS = ["name", "category", "audience", "benefits"];
const RISK_PATTERNS = [
  { pattern: /(治愈|根治|治疗|抗炎|止痛|减肥|瘦身)/i, note: "medical or body-effect claim" },
  { pattern: /(100%|百分百|绝对|保证|永久|零风险|无风险)/i, note: "absolute or guaranteed claim" },
  { pattern: /(第一|最强|最好|全网最低|行业领先)/i, note: "comparative superiority claim" },
  { pattern: /(官方认证|独家授权|专利|临床证明)/i, note: "official, patent, or clinical claim" },
  { pattern: /(仅限今天|最后一批|库存告急|错过再等一年)/i, note: "scarcity claim" }
];

function asArray(value) {
  if (Array.isArray(value)) return value.filter(Boolean);
  if (value === undefined || value === null || value === "") return [];
  return [String(value)];
}

function first(value, fallback) {
  const arr = asArray(value);
  return arr.length ? arr[0] : fallback;
}

function normalizeProduct(input) {
  const product = { ...input };
  product.name = String(product.name || product.product || "Unnamed Product").trim();
  product.category = String(product.category || "通用").trim();
  product.price = product.price === undefined || product.price === null ? "待补充" : String(product.price);
  product.audience = String(product.audience || product.targetAudience || "目标用户待补充").trim();
  product.scenario = String(product.scenario || product.useCase || "使用场景待补充").trim();
  product.goal = String(product.goal || "帮助用户判断是否值得了解或购买").trim();
  product.tone = String(product.tone || product.brandVoice || "真实、克制、有帮助").trim();
  product.benefits = asArray(product.benefits || product.highlights);
  product.evidence = asArray(product.evidence || product.proofPoints);
  product.limitations = asArray(product.limitations || product.cons);
  product.differentiators = asArray(product.differentiators || product.pros);
  product.offer = product.offer ? String(product.offer) : "";
  product.platforms = asArray(product.platforms).length ? asArray(product.platforms) : DEFAULT_PLATFORMS;
  product.prohibitedClaims = asArray(product.prohibitedClaims);
  return product;
}

function validateProduct(product) {
  const missingFields = REQUIRED_FIELDS.filter((field) => {
    if (field === "benefits") return product.benefits.length === 0;
    return !product[field] || String(product[field]).includes("待补充");
  });

  const joined = [
    product.name,
    product.category,
    product.audience,
    product.scenario,
    product.goal,
    product.tone,
    ...product.benefits,
    ...product.evidence,
    ...product.limitations,
    ...product.differentiators,
    ...product.prohibitedClaims
  ].join(" ");

  const riskyClaims = RISK_PATTERNS
    .filter((entry) => entry.pattern.test(joined))
    .map((entry) => entry.note);

  return {
    missingFields,
    riskyClaims: [...new Set(riskyClaims)],
    evidenceStatus: product.evidence.length ? "provided" : "missing",
    assumptions: buildAssumptions(product, missingFields)
  };
}

function buildAssumptions(product, missingFields) {
  const assumptions = [];
  if (missingFields.includes("audience")) assumptions.push("Audience is inferred and should be confirmed.");
  if (missingFields.includes("benefits")) assumptions.push("Benefits are placeholder-level until concrete proof is supplied.");
  if (!product.evidence.length) assumptions.push("Performance and experience claims are phrased conservatively because evidence is missing.");
  if (!product.price || product.price === "待补充") assumptions.push("Price-sensitive advice should be revised after price is confirmed.");
  return assumptions;
}

function proofLine(product) {
  return product.evidence.length
    ? product.evidence.map((item) => `证据：${item}`).join("；")
    : "证据：待补充证据，不建议使用强效果承诺。";
}

function benefitLines(product, prefix = "- ") {
  const benefits = product.benefits.length ? product.benefits : ["核心卖点待补充"];
  return benefits.map((item) => `${prefix}${item}`).join("\n");
}

function limitationLine(product) {
  return product.limitations.length
    ? product.limitations.join("；")
    : "暂无明确限制，建议补充不适合人群或使用边界。";
}

function hashtags(product) {
  const base = CATEGORY_HASHTAGS[product.category] || ["#好物分享", "#真实测评", "#购物决策"];
  const scenario = product.scenario && !product.scenario.includes("待补充")
    ? `#${product.scenario.replace(/\s+/g, "")}`
    : "";
  return [...base, scenario].filter(Boolean).join(" ");
}

function generateXiaohongshu(product) {
  const primaryBenefit = first(product.benefits, "这个细节值得看");
  return {
    platform: "xiaohongshu",
    titleOptions: [
      `${product.audience}可以看看：${product.name}真实体验`,
      `${product.category}别急着买，先看${product.name}适不适合你`,
      `用了${product.name}之后，我会重点看这${Math.max(product.benefits.length, 3)}点`,
      `${product.price}元的${product.name}，适合谁不适合谁？`
    ],
    body: [
      `最近在${product.scenario}里反复用到${product.name}，这篇只讲真实感受和购买判断。`,
      `适合人群：${product.audience}`,
      `我最在意的一点：${primaryBenefit}`,
      "核心体验：\n" + benefitLines(product),
      proofLine(product),
      `需要注意：${limitationLine(product)}`,
      `购买建议：如果你主要想解决“${primaryBenefit}”，可以加入候选；如果你更在意长期效果或极致性价比，建议先对比同类产品或等更多反馈。`,
      hashtags(product)
    ].join("\n\n")
  };
}

function generateDouyin(product) {
  const primaryBenefit = first(product.benefits, "体验点待补充");
  return {
    platform: "douyin",
    hookOptions: [
      `${product.audience}，买${product.category}前先看这一点。`,
      `${product.name}我会怎么判断值不值得买？`,
      `别只看种草，${product.name}真正要看的是这里。`
    ],
    spokenScript: [
      `如果你正在${product.scenario}，${product.name}可以先这样判断。`,
      `第一，看它是不是解决你的核心需求：${primaryBenefit}。`,
      `第二，看证据。${proofLine(product)}`,
      `第三，看边界。${limitationLine(product)}`,
      `我的建议是：适合${product.audience}先加入对比清单，别因为一句“闭眼入”就直接下单。`
    ],
    caption: `${product.name}购买前先看证据和适用人群。${hashtags(product)}`,
    cta: "想要我按你的预算做对比，可以把价格和候选产品发来。"
  };
}

function generateLive(product) {
  const primaryBenefit = first(product.benefits, "核心卖点待补充");
  return {
    platform: "live",
    opening: `今天讲${product.name}，不只报价格，重点帮${product.audience}判断适不适合。`,
    demoFlow: [
      `场景：${product.scenario}`,
      `卖点展示：${primaryBenefit}`,
      `证据说明：${proofLine(product)}`,
      `边界提醒：${limitationLine(product)}`
    ],
    objections: [
      {
        question: "是不是所有人都适合？",
        answer: `不是。更适合${product.audience}，其他人建议先看需求是否匹配。`
      },
      {
        question: "为什么现在看它？",
        answer: product.offer || `如果你正在比较${product.category}，它可以作为候选项之一。`
      }
    ],
    close: "需要的先收藏参数和适用人群，再决定是否下单。"
  };
}

function generateMoments(product) {
  const primaryBenefit = first(product.benefits, "有一个点比较实用");
  return {
    platform: "moments",
    short: `最近在看${product.name}，适合${product.audience}。我比较认可的是：${primaryBenefit}。不急着冲，建议先看自己场景是否匹配。`,
    medium: `试着整理一下${product.name}：\n适合：${product.audience}\n场景：${product.scenario}\n亮点：${primaryBenefit}\n注意：${limitationLine(product)}\n有同类需求的可以先放进候选清单。`
  };
}

function generateZhihu(product) {
  const primaryBenefit = first(product.benefits, "核心卖点待补充");
  return {
    platform: "zhihu",
    title: `如何评价${product.name}？是否值得买？`,
    answer: [
      `先说结论：如果你是${product.audience}，并且核心需求是“${primaryBenefit}”，${product.name}可以进入候选；但不建议只凭种草内容直接购买。`,
      `## 判断标准`,
      `1. 需求是否匹配：${product.scenario}`,
      `2. 卖点是否有证据：${proofLine(product)}`,
      `3. 缺点或边界是否能接受：${limitationLine(product)}`,
      `## 适合谁`,
      `${product.audience}`,
      `## 不适合谁`,
      product.limitations.length ? product.limitations.map((item) => `- ${item}`).join("\n") : "- 对价格非常敏感，且需要长期效果数据的人。",
      `## 购买建议`,
      `把它和2-3个同类产品按价格、证据、售后、真实评价做表格对比，再决定。`
    ].join("\n\n")
  };
}

function generateMarketplace(product) {
  const benefits = product.benefits.length ? product.benefits : ["核心卖点待补充"];
  return {
    platform: "marketplace",
    title: `${product.name} ${product.category} ${first(benefits, "")}`.trim(),
    bullets: benefits.slice(0, 5).map((benefit) => `${benefit}：面向${product.audience}的${product.scenario}需求。`),
    detailSections: {
      scenario: `适用场景：${product.scenario}`,
      proof: proofLine(product),
      fit: `适合人群：${product.audience}`,
      caution: `购买前注意：${limitationLine(product)}`
    }
  };
}

function generateAds(product) {
  const primaryBenefit = first(product.benefits, "核心卖点待补充");
  const evidence = product.evidence.length ? product.evidence[0] : "待补充证据";
  return {
    platform: "ads",
    variants: [
      {
        angle: "pain-point",
        headline: `${product.audience}，别再盲选${product.category}`,
        body: `${product.name}围绕${primaryBenefit}展开，适合${product.scenario}。`,
        cta: "查看是否适合我"
      },
      {
        angle: "proof",
        headline: `先看证据，再决定要不要买`,
        body: `${product.name}当前证据：${evidence}。`,
        cta: "查看详细对比"
      },
      {
        angle: "fit",
        headline: `${product.name}适合谁？`,
        body: `更适合${product.audience}，购买前也要确认：${limitationLine(product)}`,
        cta: "获取购买建议"
      }
    ]
  };
}

function generatePlatform(platform, product) {
  const generators = {
    xiaohongshu: generateXiaohongshu,
    douyin: generateDouyin,
    live: generateLive,
    moments: generateMoments,
    zhihu: generateZhihu,
    marketplace: generateMarketplace,
    ads: generateAds
  };
  const generator = generators[platform];
  if (!generator) {
    return {
      platform,
      warning: `Unsupported platform '${platform}'. Supported platforms: ${Object.keys(generators).join(", ")}.`
    };
  }
  return generator(product);
}

function generateContentPack(input) {
  const product = normalizeProduct(input);
  const quality = validateProduct(product);
  const platformOutputs = {};
  product.platforms.forEach((platform) => {
    platformOutputs[platform] = generatePlatform(platform, product);
  });

  return {
    brief: {
      name: product.name,
      category: product.category,
      price: product.price,
      audience: product.audience,
      scenario: product.scenario,
      goal: product.goal,
      tone: product.tone
    },
    platforms: platformOutputs,
    qualityNotes: {
      evidenceStatus: quality.evidenceStatus,
      missingFields: quality.missingFields,
      riskyClaims: quality.riskyClaims,
      assumptions: quality.assumptions,
      nextIteration: suggestNextIteration(product, quality)
    }
  };
}

function suggestNextIteration(product, quality) {
  const suggestions = [];
  if (quality.missingFields.length) suggestions.push(`补充字段：${quality.missingFields.join(", ")}`);
  if (!product.evidence.length) suggestions.push("补充真实证据，例如用户反馈、参数、测试条件、价格截图或售后政策。");
  if (!product.limitations.length) suggestions.push("补充不适合人群或使用边界，让内容更可信。");
  suggestions.push("为下载/安装表现好的平台保留一组A/B标题，下一轮按点击或转化反馈迭代。");
  return suggestions;
}

function renderValue(value, indent = "") {
  if (Array.isArray(value)) {
    return value.map((item) => {
      if (typeof item === "object" && item !== null) {
        return `${indent}- ${renderValue(item, `${indent}  `).trimStart()}`;
      }
      return `${indent}- ${item}`;
    }).join("\n");
  }
  if (typeof value === "object" && value !== null) {
    return Object.entries(value)
      .map(([key, nested]) => `${indent}${key}:\n${renderValue(nested, `${indent}  `)}`)
      .join("\n");
  }
  return `${indent}${value}`;
}

function renderMarkdown(pack) {
  const lines = [];
  lines.push(`# ${pack.brief.name} Content Pack`);
  lines.push("");
  lines.push("## Brief");
  Object.entries(pack.brief).forEach(([key, value]) => {
    lines.push(`- ${key}: ${value}`);
  });
  lines.push("");
  lines.push("## Platform Drafts");
  Object.entries(pack.platforms).forEach(([platform, output]) => {
    lines.push("");
    lines.push(`### ${PLATFORM_NAMES[platform] || platform}`);
    Object.entries(output)
      .filter(([key]) => key !== "platform")
      .forEach(([key, value]) => {
        lines.push(`#### ${key}`);
        lines.push(renderValue(value));
        lines.push("");
      });
  });
  lines.push("## Quality Notes");
  Object.entries(pack.qualityNotes).forEach(([key, value]) => {
    lines.push(`### ${key}`);
    lines.push(renderValue(value) || "- none");
    lines.push("");
  });
  return lines.join("\n").trim() + "\n";
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    }
  }
  return args;
}

function readInput(path) {
  if (!path || path === "-") return fs.readFileSync(0, "utf8");
  return fs.readFileSync(path, "utf8");
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.input) {
    process.stdout.write([
      "Usage: node scripts/generate_content_pack.js --input product.json [--platforms xiaohongshu,douyin] [--format json|markdown]",
      "",
      "Input must be JSON. Use --input - to read from stdin."
    ].join("\n") + "\n");
    process.exit(args.help ? 0 : 1);
  }

  const input = JSON.parse(readInput(args.input));
  if (args.platforms) {
    input.platforms = String(args.platforms).split(",").map((item) => item.trim()).filter(Boolean);
  }
  const pack = generateContentPack(input);
  const format = args.format || "json";
  process.stdout.write(format === "markdown" ? renderMarkdown(pack) : `${JSON.stringify(pack, null, 2)}\n`);
}

if (require.main === module) {
  main();
}

module.exports = {
  DEFAULT_PLATFORMS,
  PLATFORM_NAMES,
  generateContentPack,
  normalizeProduct,
  renderMarkdown,
  validateProduct
};
