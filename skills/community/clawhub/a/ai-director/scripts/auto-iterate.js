#!/usr/bin/env node
/**
 * Auto-Iterate - 自动评估和迭代生成
 *
 * 生成视频 → 评估质量 → 如果低于80分则改进提示词重新生成
 * 最多迭代5次
 *
 * Usage:
 *   node auto-iterate.js <prompt> [options]
 *
 * Options:
 *   --duration 60|120|180|300    视频时长（默认 120）
 *   --style "风格名称"           风格
 *   --ratio 9:16|16:9            比例（默认 9:16）
 *   --max-iterations 5           最大迭代次数（默认 5）
 *   --threshold 80               及格分数（默认 80）
 *   --json                       JSON 输出模式
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// Import modules
const qualityEvaluator = require("./quality-evaluator.js");
const accountManager = require("./ad-account-manager.js");
const { loadUserConfig } = require("./config-loader");

// Configuration
const DEFAULT_MAX_ITERATIONS = 5;
const DEFAULT_THRESHOLD = 80;

function loadConfig() {
  try {
    const result = loadUserConfig();
    return result.config;
  } catch (e) {
    return {};
  }
}

// Parse arguments
function parseArgs() {
  const args = process.argv.slice(2);

  if (args.length < 1 || args[0].startsWith("--")) {
    console.log('Usage: node auto-iterate.js "<prompt>" [options]');
    console.log("");
    console.log("Options:");
    console.log("  --duration 60|120|180|300    视频时长（默认 120）");
    console.log('  --style "风格名称"           风格');
    console.log("  --ratio 9:16|16:9            比例（默认 9:16）");
    console.log("  --max-iterations 5           最大迭代次数（默认 5）");
    console.log("  --threshold 80               及格分数（默认 80）");
    console.log("  --json                       JSON 输出模式");
    console.log("");
    console.log("Example:");
    console.log('  node auto-iterate.js "吉卜力风格的校园恋爱短剧" --duration 60 --style "吉卜力"');
    process.exit(1);
  }

  const config = {
    prompt: args[0],
    duration: "120",
    style: null,
    ratio: "9:16",
    maxIterations: DEFAULT_MAX_ITERATIONS,
    threshold: DEFAULT_THRESHOLD,
    jsonMode: false,
  };

  for (let i = 1; i < args.length; i++) {
    switch (args[i]) {
      case "--duration":
        config.duration = args[++i];
        break;
      case "--style":
        config.style = args[++i];
        break;
      case "--ratio":
        config.ratio = args[++i];
        break;
      case "--max-iterations":
        config.maxIterations = parseInt(args[++i]);
        break;
      case "--threshold":
        config.threshold = parseInt(args[++i]);
        break;
      case "--json":
        config.jsonMode = true;
        break;
    }
  }

  return config;
}

// Log helper
function log(message, config) {
  if (!config.jsonMode) {
    console.log(message);
  }
}

// Execute ad-producer command
function runProducer(command, silent = false) {
  try {
    const output = execSync(`node ${path.join(__dirname, "ad-producer.js")} ${command}`, {
      encoding: "utf8",
      stdio: silent ? "pipe" : "inherit",
      cwd: __dirname,
    });
    return { success: true, output };
  } catch (err) {
    return { success: false, error: err.message, output: err.stdout };
  }
}

// Main iteration loop
async function autoIterate(config) {
  const startTime = Date.now();
  const history = [];
  let currentPrompt = config.prompt;
  let projectId = null;
  let videoUrl = null;
  let finalResult = null;

  log("", config);
  log("═══════════════════════════════════════════════════════════", config);
  log("🔄 Auto-Iterate: 自动评估和迭代生成", config);
  log("═══════════════════════════════════════════════════════════", config);
  log(`   原始提示词: ${config.prompt.substring(0, 50)}...`, config);
  log(`   时长: ${config.duration}s`, config);
  log(`   及格线: ${config.threshold}分`, config);
  log(`   最大迭代: ${config.maxIterations}次`, config);
  log("", config);

  for (let iteration = 1; iteration <= config.maxIterations; iteration++) {
    log(`\n🔁 迭代 ${iteration}/${config.maxIterations}`, config);
    log("───────────────────────────────────────────────────────────", config);

    const iterationData = {
      iteration,
      prompt: currentPrompt,
      projectId: null,
      videoUrl: null,
      score: null,
      pass: false,
      issues: [],
      suggestions: [],
    };

    try {
      // Step 1: Generate script
      log("📝 生成剧本...", config);
      let cmdOpts = `"${currentPrompt}" --duration ${config.duration} --ratio ${config.ratio} --wait`;
      if (config.style) cmdOpts += ` --style "${config.style}"`;

      const scriptResult = runProducer(`generate-script ${cmdOpts}`, true);
      if (!scriptResult.success) {
        throw new Error(`Script generation failed: ${scriptResult.error}`);
      }

      // Extract project ID
      const pidMatch = scriptResult.output.match(/Project ID: ([a-f0-9-]+)/);
      if (!pidMatch) {
        throw new Error("Could not extract project ID");
      }
      projectId = pidMatch[1];
      iterationData.projectId = projectId;
      log(`   Project ID: ${projectId}`, config);

      // Step 2: Produce video
      log("🎬 生成视频...", config);
      const videoResult = runProducer(`produce-video ${projectId} 1 --wait`, true);
      if (!videoResult.success) {
        throw new Error(`Video production failed: ${videoResult.error}`);
      }

      // Extract video URL
      const urlMatch = videoResult.output.match(/Video URL: (https?:\/\/[^\s]+)/);
      if (!urlMatch) {
        // Try to get from video-status
        const statusResult = runProducer(`video-status ${projectId} 1`, true);
        const statusUrlMatch = statusResult.output.match(/Video URL: (https?:\/\/[^\s]+)/);
        if (statusUrlMatch) {
          videoUrl = statusUrlMatch[1];
        } else {
          throw new Error("Could not extract video URL");
        }
      } else {
        videoUrl = urlMatch[1];
      }
      iterationData.videoUrl = videoUrl;
      log(`   Video URL: ${videoUrl}`, config);

      // Step 3: Evaluate quality
      log("🔍 评估视频质量...", config);
      const evalResult = await qualityEvaluator.evaluateVideo(videoUrl, currentPrompt);

      iterationData.score = evalResult.total_score;
      iterationData.pass = evalResult.pass;
      iterationData.issues = evalResult.issues || [];
      iterationData.suggestions = evalResult.suggestions || [];
      iterationData.evaluation = evalResult;

      log(`   总分: ${evalResult.total_score}`, config);
      log(`   结果: ${evalResult.pass ? "✅ 通过" : "❌ 未通过"}`, config);

      history.push(iterationData);

      // Check if passed
      if (evalResult.pass) {
        log("\n🎉 质量达标，停止迭代", config);
        finalResult = {
          success: true,
          iterations: iteration,
          projectId,
          videoUrl,
          score: evalResult.total_score,
          prompt: currentPrompt,
          history,
        };
        break;
      }

      // Not passed - prepare for next iteration
      if (iteration < config.maxIterations) {
        log("\n📝 质量未达标，准备改进...", config);

        if (evalResult.issues?.length > 0) {
          log("   问题:", config);
          evalResult.issues.forEach((issue) => log(`   - ${issue}`, config));
        }

        if (evalResult.prompt_improvements) {
          log(`   改进后提示词: ${evalResult.prompt_improvements.substring(0, 100)}...`, config);
          currentPrompt = evalResult.prompt_improvements;
        } else if (evalResult.suggestions?.length > 0) {
          // 简单的提示词改进：追加建议
          const suggestionText = evalResult.suggestions.slice(0, 2).join("，");
          currentPrompt = `${config.prompt}。注意：${suggestionText}`;
          log(`   改进后提示词: ${currentPrompt.substring(0, 100)}...`, config);
        }
      } else {
        log("\n⚠️  达到最大迭代次数，停止", config);
        finalResult = {
          success: false,
          iterations: iteration,
          projectId,
          videoUrl,
          score: evalResult.total_score,
          prompt: currentPrompt,
          history,
          reason: "max_iterations_reached",
        };
      }
    } catch (error) {
      log(`\n❌ 迭代 ${iteration} 失败: ${error.message}`, config);
      iterationData.error = error.message;
      history.push(iterationData);

      if (iteration >= config.maxIterations) {
        finalResult = {
          success: false,
          iterations: iteration,
          projectId,
          videoUrl,
          score: null,
          prompt: currentPrompt,
          history,
          reason: "error",
          error: error.message,
        };
      }
    }
  }

  // Final report
  const totalTime = Math.round((Date.now() - startTime) / 1000);

  if (!finalResult) {
    finalResult = {
      success: false,
      iterations: config.maxIterations,
      projectId,
      videoUrl,
      score: history[history.length - 1]?.score || null,
      prompt: currentPrompt,
      history,
      reason: "unknown",
    };
  }

  finalResult.totalTimeSeconds = totalTime;

  log("", config);
  log("═══════════════════════════════════════════════════════════", config);
  log("📊 最终结果", config);
  log("═══════════════════════════════════════════════════════════", config);
  log(`   状态: ${finalResult.success ? "✅ 成功" : "❌ 未达标"}`, config);
  log(`   迭代次数: ${finalResult.iterations}`, config);
  log(`   最终分数: ${finalResult.score || "N/A"}`, config);
  log(`   Project ID: ${finalResult.projectId || "N/A"}`, config);
  log(`   Video URL: ${finalResult.videoUrl || "N/A"}`, config);
  log(`   总耗时: ${Math.floor(totalTime / 60)}分${totalTime % 60}秒`, config);
  log("", config);

  if (config.jsonMode) {
    console.log(JSON.stringify(finalResult, null, 2));
  }

  return finalResult;
}

// CLI entry point
async function main() {
  const config = parseArgs();

  // Check binding
  const binding = await accountManager.checkBinding();
  if (!binding.bound) {
    console.log("❌ X2C account not bound. Run: node ad-account-manager.js send-code <email>");
    process.exit(1);
  }

  // Check Gemini API key
  const appConfig = loadConfig();
  if (!appConfig.geminiApiKey && !process.env.GEMINI_API_KEY) {
    console.log("❌ Gemini API key not configured.");
    console.log("   Set geminiApiKey in config.json or GEMINI_API_KEY env var.");
    process.exit(1);
  }

  try {
    const result = await autoIterate(config);
    process.exit(result.success ? 0 : 1);
  } catch (error) {
    console.error(`\n❌ Fatal error: ${error.message}`);
    process.exit(1);
  }
}

// Module exports
module.exports = {
  autoIterate,
  DEFAULT_MAX_ITERATIONS,
  DEFAULT_THRESHOLD,
};

if (require.main === module) {
  main();
}
