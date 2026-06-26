#!/usr/bin/env node
/**
 * Quality Evaluator - 视频质量评估模块
 *
 * 使用 Gemini 2.0 Flash 分析视频质量，按照标准打分。
 * 80分及格，低于80分提供改进建议。
 *
 * Usage:
 *   node quality-evaluator.js <video_url_or_path> [--prompt "原始提示词"]
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// Multi-user config loader
const { loadUserConfig } = require("./config-loader");

// Load config
let config = {};
try {
  const result = loadUserConfig();
  config = result.config;
} catch (e) {
  // Fallback to empty config if USER_ID not set
  config = {};
}
const GEMINI_API_KEY = config.geminiApiKey || process.env.GEMINI_API_KEY;

// 评估标准
const EVALUATION_CRITERIA = {
  singleClip: {
    name: "单片段质量 (Single Clip Level)",
    description: "关注 AI 模型生成的原生画质与物理稳定性",
    metrics: [
      {
        id: "temporal_consistency",
        name: "时空一致性",
        weight: 0.35,
        definition: "主体特征的一致性",
        excellent: "人脸、服装、环境细节在镜头内保持稳定",
        fail: "关键特征突变、衣物颜色变幻",
      },
      {
        id: "dynamics",
        name: "动态动力学",
        weight: 0.3,
        definition: "运动的逻辑与流畅度",
        excellent: "符合物理规律（重力、惯性），无跳帧",
        fail: "肢体畸变、瞬间位移、物体融化",
      },
      {
        id: "visual_clarity",
        name: "视觉纯净度",
        weight: 0.2,
        definition: "画面清晰度与伪影控制",
        excellent: "纹理清晰，无明显 AI 噪点或糊块",
        fail: "出现'恐怖谷'效应、液化",
      },
      {
        id: "lighting",
        name: "光影交互",
        weight: 0.15,
        definition: "动态光影匹配度",
        excellent: "阴影随物体运动同步变化",
        fail: "贴图感强，光源方向不统一",
      },
    ],
  },
  assembly: {
    name: "合成视频质量 (Assembly Level)",
    description: "关注剪辑、逻辑、视听配合与叙事完成度",
    metrics: [
      {
        id: "visual_flow",
        name: "视觉流一致性",
        weight: 0.3,
        definition: "镜头间的色调匹配",
        excellent: "邻近镜头色温、亮度、颗粒感统一",
        fail: "镜头间颜色突跳，风格不统一",
      },
      {
        id: "editing_rhythm",
        name: "剪辑节奏感",
        weight: 0.25,
        definition: "镜头切换的逻辑",
        excellent: "转场自然，剪辑点匹配 BGM 节奏",
        fail: "节奏混乱，出现'黑帧'或无效转场",
      },
      {
        id: "narrative_match",
        name: "叙事匹配度",
        weight: 0.25,
        definition: "脚本还原能力",
        excellent: "准确传达了提示词或脚本的剧情",
        fail: "画面与主题脱节，内容词不达意",
      },
      {
        id: "audio_sync",
        name: "音画同步率",
        weight: 0.2,
        definition: "音效与视觉的契合",
        excellent: "关键动作配有相应音效，BGM 情绪吻合",
        fail: "声音延迟或环境音完全不匹配",
      },
    ],
  },
};

// 构建评估 prompt
function buildEvaluationPrompt(originalPrompt = "") {
  let prompt = `你是一个专业的 AI 生成视频质量评估专家。请根据以下标准对视频进行评分。

## 评估标准

### 维度一：单片段质量 (Single Clip Level)
关注 AI 模型生成的原生画质与物理稳定性。

| 指标 | 权重 | 定义 | 优良标准 (80-100) | 失败表现 (<60) |
|-----|------|------|------------------|---------------|
| 时空一致性 | 35% | 主体特征的一致性 | 人脸、服装、环境细节在镜头内保持稳定 | 关键特征突变、衣物颜色变幻 |
| 动态动力学 | 30% | 运动的逻辑与流畅度 | 符合物理规律（重力、惯性），无跳帧 | 肢体畸变、瞬间位移、物体融化 |
| 视觉纯净度 | 20% | 画面清晰度与伪影控制 | 纹理清晰，无明显 AI 噪点或糊块 | 出现"恐怖谷"效应、液化 |
| 光影交互 | 15% | 动态光影匹配度 | 阴影随物体运动同步变化 | 贴图感强，光源方向不统一 |

### 维度二：合成视频质量 (Assembly Level)
关注剪辑、逻辑、视听配合与叙事完成度。

| 指标 | 权重 | 定义 | 优良标准 (80-100) | 失败表现 (<60) |
|-----|------|------|------------------|---------------|
| 视觉流一致性 | 30% | 镜头间的色调匹配 | 邻近镜头色温、亮度、颗粒感统一 | 镜头间颜色突跳，风格不统一 |
| 剪辑节奏感 | 25% | 镜头切换的逻辑 | 转场自然，剪辑点匹配 BGM 节奏 | 节奏混乱，出现"黑帧"或无效转场 |
| 叙事匹配度 | 25% | 脚本还原能力 | 准确传达了提示词或脚本的剧情 | 画面与主题脱节，内容词不达意 |
| 音画同步率 | 20% | 音效与视觉的契合 | 关键动作配有相应音效，BGM 情绪吻合 | 声音延迟或环境音完全不匹配 |

`;

  if (originalPrompt) {
    prompt += `## 原始提示词/剧本
${originalPrompt}

`;
  }

  prompt += `## 输出要求

请以 JSON 格式输出评估结果：

\`\`\`json
{
  "single_clip": {
    "temporal_consistency": { "score": 0-100, "comment": "评价" },
    "dynamics": { "score": 0-100, "comment": "评价" },
    "visual_clarity": { "score": 0-100, "comment": "评价" },
    "lighting": { "score": 0-100, "comment": "评价" },
    "weighted_score": 0-100
  },
  "assembly": {
    "visual_flow": { "score": 0-100, "comment": "评价" },
    "editing_rhythm": { "score": 0-100, "comment": "评价" },
    "narrative_match": { "score": 0-100, "comment": "评价" },
    "audio_sync": { "score": 0-100, "comment": "评价" },
    "weighted_score": 0-100
  },
  "total_score": 0-100,
  "pass": true/false,
  "issues": ["问题1", "问题2"],
  "suggestions": ["改进建议1", "改进建议2"],
  "prompt_improvements": "如果需要重新生成，建议修改后的提示词"
}
\`\`\`

注意：
- 每个指标打分 0-100
- weighted_score 是该维度的加权总分
- total_score = (single_clip.weighted_score + assembly.weighted_score) / 2
- pass = total_score >= 80
- 如果 pass=false，必须提供 issues、suggestions 和 prompt_improvements

请仔细观看视频后给出评分。`;

  return prompt;
}

// 调用 Gemini API
async function callGemini(videoUrl, prompt) {
  if (!GEMINI_API_KEY) {
    throw new Error(
      "Gemini API key not configured. Set geminiApiKey in config.json or GEMINI_API_KEY env var.",
    );
  }

  const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;

  // 构建请求体
  const requestBody = {
    contents: [
      {
        parts: [
          { text: prompt },
          {
            file_data: {
              mime_type: "video/mp4",
              file_uri: videoUrl,
            },
          },
        ],
      },
    ],
    generationConfig: {
      temperature: 0.1,
      maxOutputTokens: 4096,
    },
  };

  return new Promise((resolve, reject) => {
    const url = new URL(apiUrl);
    const payload = JSON.stringify(requestBody);

    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(payload),
      },
    };

    const req = https.request(options, (res) => {
      let body = "";
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => {
        try {
          const json = JSON.parse(body);
          if (json.error) {
            reject(new Error(json.error.message || "Gemini API error"));
          } else {
            const text = json.candidates?.[0]?.content?.parts?.[0]?.text || "";
            resolve(text);
          }
        } catch (e) {
          reject(new Error(`Parse error: ${body.substring(0, 500)}`));
        }
      });
    });

    req.on("error", reject);
    req.setTimeout(120000, () => {
      req.destroy();
      reject(new Error("Request timeout"));
    });

    req.write(payload);
    req.end();
  });
}

// 解析评估结果
function parseEvaluationResult(text) {
  // 提取 JSON
  const jsonMatch = text.match(/```json\s*([\s\S]*?)\s*```/);
  if (jsonMatch) {
    return JSON.parse(jsonMatch[1]);
  }

  // 尝试直接解析
  const startIdx = text.indexOf("{");
  const endIdx = text.lastIndexOf("}");
  if (startIdx !== -1 && endIdx !== -1) {
    return JSON.parse(text.substring(startIdx, endIdx + 1));
  }

  throw new Error("Could not parse evaluation result");
}

// 计算加权分数
function calculateWeightedScore(dimension, scores) {
  const metrics = EVALUATION_CRITERIA[dimension].metrics;
  let totalScore = 0;

  for (const metric of metrics) {
    const score = scores[metric.id]?.score || 0;
    totalScore += score * metric.weight;
  }

  return Math.round(totalScore);
}

// 主评估函数
async function evaluateVideo(videoUrl, originalPrompt = "") {
  console.log("🔍 Evaluating video quality...");
  console.log(`   Video: ${videoUrl}`);

  const prompt = buildEvaluationPrompt(originalPrompt);
  const response = await callGemini(videoUrl, prompt);
  const result = parseEvaluationResult(response);

  // 验证并补充计算
  if (!result.single_clip?.weighted_score) {
    result.single_clip.weighted_score = calculateWeightedScore("singleClip", result.single_clip);
  }
  if (!result.assembly?.weighted_score) {
    result.assembly.weighted_score = calculateWeightedScore("assembly", result.assembly);
  }
  if (!result.total_score) {
    result.total_score = Math.round(
      (result.single_clip.weighted_score + result.assembly.weighted_score) / 2,
    );
  }
  if (result.pass === undefined) {
    result.pass = result.total_score >= 80;
  }

  return result;
}

// 打印评估报告
function printReport(result) {
  console.log("");
  console.log("═══════════════════════════════════════════════════════════");
  console.log("📊 视频质量评估报告");
  console.log("═══════════════════════════════════════════════════════════");

  console.log("\n📹 单片段质量 (Single Clip Level)");
  console.log("───────────────────────────────────────────────────────────");
  for (const [key, value] of Object.entries(result.single_clip)) {
    if (key === "weighted_score") continue;
    if (typeof value === "object" && value.score !== undefined) {
      const bar =
        "█".repeat(Math.round(value.score / 10)) + "░".repeat(10 - Math.round(value.score / 10));
      console.log(`   ${key}: ${bar} ${value.score}`);
      if (value.comment) console.log(`      → ${value.comment}`);
    }
  }
  console.log(`   加权总分: ${result.single_clip.weighted_score}`);

  console.log("\n🎬 合成视频质量 (Assembly Level)");
  console.log("───────────────────────────────────────────────────────────");
  for (const [key, value] of Object.entries(result.assembly)) {
    if (key === "weighted_score") continue;
    if (typeof value === "object" && value.score !== undefined) {
      const bar =
        "█".repeat(Math.round(value.score / 10)) + "░".repeat(10 - Math.round(value.score / 10));
      console.log(`   ${key}: ${bar} ${value.score}`);
      if (value.comment) console.log(`      → ${value.comment}`);
    }
  }
  console.log(`   加权总分: ${result.assembly.weighted_score}`);

  console.log("\n═══════════════════════════════════════════════════════════");
  console.log(`   总分: ${result.total_score} / 100`);
  console.log(`   结果: ${result.pass ? "✅ 通过" : "❌ 未通过"}`);
  console.log("═══════════════════════════════════════════════════════════");

  if (!result.pass) {
    if (result.issues?.length > 0) {
      console.log("\n⚠️  发现的问题:");
      result.issues.forEach((issue, i) => console.log(`   ${i + 1}. ${issue}`));
    }

    if (result.suggestions?.length > 0) {
      console.log("\n💡 改进建议:");
      result.suggestions.forEach((sug, i) => console.log(`   ${i + 1}. ${sug}`));
    }

    if (result.prompt_improvements) {
      console.log("\n📝 建议修改后的提示词:");
      console.log(`   ${result.prompt_improvements}`);
    }
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log('Usage: node quality-evaluator.js <video_url> [--prompt "原始提示词"]');
    console.log("");
    console.log("Examples:");
    console.log("  node quality-evaluator.js https://example.com/video.mp4");
    console.log(
      '  node quality-evaluator.js https://example.com/video.mp4 --prompt "校园恋爱短剧"',
    );
    console.log("");
    console.log("Config: Set geminiApiKey in config.json or GEMINI_API_KEY env var");
    process.exit(1);
  }

  const videoUrl = args[0];
  let originalPrompt = "";

  // Parse --prompt
  const promptIdx = args.indexOf("--prompt");
  if (promptIdx !== -1 && args[promptIdx + 1]) {
    originalPrompt = args[promptIdx + 1];
  }

  try {
    const result = await evaluateVideo(videoUrl, originalPrompt);
    printReport(result);

    // Output JSON for programmatic use
    if (args.includes("--json")) {
      console.log("\n--- JSON Output ---");
      console.log(JSON.stringify(result, null, 2));
    }

    process.exit(result.pass ? 0 : 1);
  } catch (error) {
    console.error(`\n❌ Evaluation failed: ${error.message}`);
    process.exit(1);
  }
}

// Module exports
module.exports = {
  evaluateVideo,
  EVALUATION_CRITERIA,
  PASSING_SCORE: 80,
  MAX_ITERATIONS: 5,
};

if (require.main === module) {
  main();
}
