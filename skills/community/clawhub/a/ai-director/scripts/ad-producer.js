#!/usr/bin/env node
/**
 * Ad Producer - X2C 视频生产模块
 *
 * 使用 X2C Open API 进行剧本生成和视频生产。
 * 使用前必须先绑定 X2C 账号。
 *
 * Usage:
 *   node ad-producer.js <command> [options]
 *
 * Commands:
 *   config                     获取配置选项（风格、定价等）
 *   generate-script <prompt>   生成剧本
 *   script-status <project_id> 查询剧本状态
 *   produce-video <project_id> [episode] 生产视频
 *   video-status <project_id> [episode]  查询视频进度
 *   help                       显示帮助
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// Account manager
const accountManager = require("./ad-account-manager.js");

// Configuration
const X2C_API_BASE =
  process.env.X2C_API_BASE_URL || "https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api";

// HTTP Request helper
function request(action, data = {}, apiKey) {
  return new Promise((resolve, reject) => {
    const url = new URL(X2C_API_BASE);

    const payload = JSON.stringify({ action, ...data });

    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(payload),
        "X-API-Key": apiKey,
      },
    };

    const req = https.request(options, (res) => {
      let body = "";
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => {
        try {
          const json = JSON.parse(body);
          if (json.success) {
            resolve(json);
          } else {
            const err = new Error(json.error || json.message || "API Error");
            err.code = json.code;
            reject(err);
          }
        } catch (e) {
          reject(new Error(`Parse error: ${body.substring(0, 200)}`));
        }
      });
    });

    req.on("error", reject);
    req.setTimeout(60000, () => {
      req.destroy();
      reject(new Error("Request timeout"));
    });

    req.write(payload);
    req.end();
  });
}

// Check binding and get API key
async function requireBinding() {
  const binding = await accountManager.checkBinding();

  if (!binding.bound) {
    console.log("");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("❌ X2C Account Not Bound");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("");
    console.log("You must bind your X2C account before using ad-producer.");
    console.log("");
    console.log("To bind:");
    console.log("  node ad-account-manager.js send-code your@email.com");
    console.log("  node ad-account-manager.js verify your@email.com <code>");
    console.log("");
    process.exit(1);
  }

  return binding.apiKey;
}

// Polling helper
async function poll(checkFn, options = {}) {
  const { maxAttempts = 120, intervalMs = 5000, silent = false } = options;

  for (let i = 0; i < maxAttempts; i++) {
    const result = await checkFn();
    if (result.done) return result;
    if (!silent) {
      console.log(`  [${i + 1}/${maxAttempts}] ${result.status || "waiting"}...`);
    }
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  throw new Error("Polling timeout");
}

// Commands
const commands = {
  // Get configuration options
  async config() {
    const apiKey = await requireBinding();

    console.log("📋 Fetching configuration...");
    const res = await request("config/get-options", {}, apiKey);

    console.log("");
    console.log("Available Options:");
    console.log("══════════════════════════════════════════════════════════");

    console.log("\n📹 Modes:");
    res.modes?.forEach((m) => console.log(`   - ${m}`));

    console.log("\n📐 Ratios:");
    res.ratios?.forEach((r) => console.log(`   - ${r}`));

    console.log("\n⏱️  Durations & Pricing:");
    res.durations?.forEach((d) => {
      console.log(`   - ${d.label}: ${d.credits} credits ($${d.usd})`);
    });

    console.log("\n📝 Script Pricing:");
    res.script_pricing?.forEach((p) => {
      console.log(`   - ${p.mode}: ${p.credits} credits ($${p.usd})`);
    });

    console.log("\n🎨 Styles:");
    res.styles?.forEach((s) => console.log(`   - [${s.id}] ${s.name}`));

    console.log("\n📂 Categories:");
    res.categories?.forEach((c) => console.log(`   - [${c.id}] ${c.name}`));

    return res;
  },

  // Generate script
  async "generate-script"(prompt, options = {}) {
    if (!prompt) {
      console.log('Usage: node ad-producer.js generate-script "<prompt>" [options]');
      console.log("");
      console.log("Options:");
      console.log("  --mode short_video|short_drama  (default: short_video)");
      console.log("  --duration 60|120|180|300       (default: 120)");
      console.log('  --style "风格名称"');
      console.log("  --ratio 9:16|16:9               (default: 9:16)");
      console.log("  --episodes 10                   (for short_drama)");
      console.log("  --language zh|en                (default: zh)");
      console.log('  --character-ids "uuid1,uuid2"    角色UUID数组，用作主角');
      console.log("  --wait                          Wait for completion");
      return { error: "Prompt required" };
    }

    const apiKey = await requireBinding();

    console.log("📝 Generating script...");
    console.log(`   Prompt: ${prompt.substring(0, 50)}...`);

    const payload = {
      prompt,
      mode: options.mode || "short_video",
      duration: options.duration || "120",
      ratio: options.ratio || "9:16",
      language: options.language || "zh",
    };

    if (options.style) payload.style = options.style;
    // short_drama defaults to 10 episodes, short_video defaults to 1
    payload.total_episodes = options.episodes
      ? parseInt(options.episodes)
      : payload.mode === "short_drama"
        ? 10
        : 1;
    if (options.category) payload.category_id = options.category;
    // Parse character-ids from comma-separated string to array
    if (options["character-ids"]) {
      payload.character_ids = options["character-ids"].split(",").map((id) => id.trim());
    }

    const res = await request("script/generate", payload, apiKey);

    console.log("✅ Script generation started");
    console.log(`   Project ID: ${res.project_id}`);
    console.log(`   Mode: ${res.mode}`);
    console.log(`   Episodes: ${res.total_episodes}`);
    console.log(`   Credits charged: ${res.credits_charged}`);

    // Wait for completion if requested
    if (options.wait) {
      console.log("\n⏳ Waiting for script completion...");

      const result = await poll(
        async () => {
          const status = await request("script/query", { project_id: res.project_id }, apiKey);
          if (status.status === "completed") {
            return { done: true, data: status };
          } else if (status.status === "failed") {
            throw new Error("Script generation failed");
          }
          return {
            done: false,
            status: `${status.status} (${status.completed_episodes || 0}/${status.total_episodes} episodes)`,
          };
        },
        { maxAttempts: 60, intervalMs: 5000 },
      );

      console.log("✅ Script completed!");
      console.log(`   Title: ${result.data.title}`);
      console.log(`   Episodes: ${result.data.completed_episodes}`);

      return result.data;
    }

    return res;
  },

  // Query script status
  async "script-status"(projectId) {
    if (!projectId) {
      console.log("Usage: node ad-producer.js script-status <project_id>");
      return { error: "Project ID required" };
    }

    const apiKey = await requireBinding();

    const res = await request("script/query", { project_id: projectId }, apiKey);

    console.log("");
    console.log("Script Status");
    console.log("══════════════════════════════════════════════════════════");
    console.log(`   Project ID: ${res.project_id}`);
    console.log(`   Title: ${res.title || "N/A"}`);
    console.log(`   Status: ${res.status}`);
    console.log(`   Mode: ${res.mode}`);
    console.log(`   Duration: ${res.duration}s`);
    console.log(`   Style: ${res.style || "N/A"}`);
    console.log(`   Episodes: ${res.completed_episodes}/${res.total_episodes}`);

    if (res.episodes?.length > 0) {
      console.log("\n📖 Episodes:");
      res.episodes.forEach((ep) => {
        const status = ep.has_video ? "🎬" : ep.is_published ? "📤" : "📝";
        console.log(`   ${status} Episode ${ep.episode_number}: ${ep.title || "Untitled"}`);
      });
    }

    return res;
  },

  // Produce video
  async "produce-video"(projectId, episode, options = {}) {
    if (!projectId) {
      console.log("Usage: node ad-producer.js produce-video <project_id> [episode_number]");
      console.log("");
      console.log("Options:");
      console.log("  --wait    Wait for completion");
      return { error: "Project ID required" };
    }

    const apiKey = await requireBinding();
    const episodeNum = parseInt(episode) || 1;

    console.log(`🎬 Starting video production...`);
    console.log(`   Project: ${projectId}`);
    console.log(`   Episode: ${episodeNum}`);

    const res = await request(
      "video/produce",
      {
        project_id: projectId,
        episode_number: episodeNum,
      },
      apiKey,
    );

    console.log("✅ Video production started");
    console.log(`   Task ID: ${res.task_id}`);
    console.log(`   Credits charged: ${res.credits_charged}`);

    // Wait for completion if requested
    if (options.wait) {
      console.log("\n⏳ Waiting for video completion (this may take 20-40 minutes)...");

      const result = await poll(
        async () => {
          const status = await request(
            "video/query",
            {
              project_id: projectId,
              episode_number: episodeNum,
            },
            apiKey,
          );

          if (status.is_complete && status.video_url) {
            return { done: true, data: status };
          } else if (status.is_failed) {
            throw new Error("Video production failed");
          }
          return {
            done: false,
            status: `${status.current_step || status.status} (${status.progress || 0}%)`,
          };
        },
        { maxAttempts: 360, intervalMs: 10000 },
      ); // Up to 60 minutes

      console.log("✅ Video completed!");
      console.log(`   Video URL: ${result.data.video_url}`);
      if (result.data.video_asset?.download_url) {
        console.log(`   Download: ${result.data.video_asset.download_url}`);
      }

      return result.data;
    }

    return res;
  },

  // Query video status
  async "video-status"(projectId, episode) {
    if (!projectId) {
      console.log("Usage: node ad-producer.js video-status <project_id> [episode_number]");
      return { error: "Project ID required" };
    }

    const apiKey = await requireBinding();
    const episodeNum = parseInt(episode) || 1;

    const res = await request(
      "video/query",
      {
        project_id: projectId,
        episode_number: episodeNum,
      },
      apiKey,
    );

    console.log("");
    console.log("Video Status");
    console.log("══════════════════════════════════════════════════════════");
    console.log(`   Task ID: ${res.task_id || "N/A"}`);
    console.log(`   Status: ${res.status}`);
    console.log(`   Progress: ${res.progress || 0}%`);
    console.log(`   Current Step: ${res.current_step || "N/A"}`);
    console.log(`   Complete: ${res.is_complete ? "✅" : "❌"}`);
    console.log(`   Failed: ${res.is_failed ? "❌" : "✅"}`);

    if (res.characters?.length > 0) {
      console.log("\n👥 Characters:");
      res.characters.forEach((c) => {
        console.log(`   - ${c.name}: ${c.status}`);
      });
    }

    if (res.storyboard_shots?.length > 0) {
      console.log(`\n🎞️  Storyboard: ${res.storyboard_shots.length} shots`);
    }

    if (res.video_url) {
      console.log(`\n🎬 Video URL: ${res.video_url}`);
    }

    if (res.video_asset) {
      console.log("\n📦 Video Asset:");
      if (res.video_asset.signed_url) console.log(`   Signed: ${res.video_asset.signed_url}`);
      if (res.video_asset.download_url) console.log(`   Download: ${res.video_asset.download_url}`);
      if (res.video_asset.thumbnail_url)
        console.log(`   Thumbnail: ${res.video_asset.thumbnail_url}`);
    }

    return res;
  },

  // Full workflow: script + video
  async "full-workflow"(prompt, options = {}) {
    if (!prompt) {
      console.log('Usage: node ad-producer.js full-workflow "<prompt>" [options]');
      console.log("");
      console.log("Options:");
      console.log("  --mode short_video|short_drama  (default: short_video)");
      console.log("  --duration 60|120|180|300       (default: 120)");
      console.log('  --style "风格名称"');
      console.log("  --ratio 9:16|16:9               (default: 9:16)");
      console.log("  --episodes 10                   (for short_drama)");
      console.log("  --episode 1                     Which episode to produce (default: 1)");
      return { error: "Prompt required" };
    }

    const apiKey = await requireBinding();
    const startTime = Date.now();

    console.log("");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("🎬 Full Workflow: Script + Video Production");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("");

    // Step 1: Generate script
    console.log("📝 Step 1/3: Generating script...");
    const scriptRes = await commands["generate-script"](prompt, { ...options, wait: true });
    const projectId = scriptRes.project_id;

    // Step 2: Produce video
    const episodeNum = parseInt(options.episode) || 1;
    console.log(`\n🎬 Step 2/3: Producing video for episode ${episodeNum}...`);
    const videoRes = await commands["produce-video"](projectId, episodeNum, { wait: true });

    const totalTime = Math.round((Date.now() - startTime) / 1000);

    console.log("");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("🎉 Workflow Complete!");
    console.log("═══════════════════════════════════════════════════════════");
    console.log(`   Project ID: ${projectId}`);
    console.log(`   Title: ${scriptRes.title}`);
    console.log(`   Video URL: ${videoRes.video_url}`);
    console.log(`   Total time: ${Math.floor(totalTime / 60)}m ${totalTime % 60}s`);
    console.log("");

    return {
      project_id: projectId,
      title: scriptRes.title,
      video_url: videoRes.video_url,
      total_time_seconds: totalTime,
    };
  },

  // Help
  async help() {
    console.log(`
Ad Producer - X2C Video Production

Configuration:
  config
      Get available options (styles, durations, pricing)

Script Generation:
  generate-script "<prompt>" [options]
      Generate a script from prompt
      --mode short_video|short_drama  Mode (default: short_video)
      --duration 60|120|180|300       Duration in seconds (default: 120)
      --style "风格名称"              Style name
      --ratio 9:16|16:9               Aspect ratio (default: 9:16)
      --episodes 10                   Total episodes (for short_drama)
      --language zh|en                Language (default: zh)
      --wait                          Wait for completion

  script-status <project_id>
      Check script generation status

Video Production:
  produce-video <project_id> [episode_number] [--wait]
      Start video production for an episode

  video-status <project_id> [episode_number]
      Check video production status

Full Workflow:
  full-workflow "<prompt>" [options]
      Complete workflow: script → video
      All generate-script options plus:
      --episode 1                     Which episode to produce

Examples:
  # View pricing
  node ad-producer.js config

  # Generate script and wait
  node ad-producer.js generate-script "穿越古代的程序员" --wait

  # Check script status
  node ad-producer.js script-status proj_xxx

  # Produce video and wait
  node ad-producer.js produce-video proj_xxx 1 --wait

  # Full workflow
  node ad-producer.js full-workflow "一个程序员穿越到古代" --duration 120

Credits:
  - Script: 6 credits (short_video) / 60 credits (short_drama)
  - Video: 299-999 credits depending on duration
`);
  },
};

// CLI entry point
if (require.main === module) {
  async function main() {
    const args = process.argv.slice(2);
    const cmd = args[0];

    if (!cmd || !commands[cmd]) {
      await commands.help();
      process.exit(cmd ? 1 : 0);
    }

    // Parse options
    const options = {};
    const positional = [];

    for (let i = 1; i < args.length; i++) {
      if (args[i].startsWith("--")) {
        const key = args[i].slice(2);
        const value = args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true;
        options[key] = value;
      } else {
        positional.push(args[i]);
      }
    }

    try {
      const result = await commands[cmd](...positional, options);
      if (result && result.error) {
        process.exit(1);
      }
    } catch (error) {
      console.error(`\n❌ Error: ${error.message}`);
      if (error.code === 402) {
        console.error("   Insufficient credits. Please top up at https://x2creel.ai");
      }
      process.exit(1);
    }
  }

  main();
}

// Module exports
module.exports = {
  generateScript: async (prompt, options = {}) => {
    const apiKey = accountManager.getApiKey();
    if (!apiKey) throw new Error("X2C account not bound");
    return request("script/generate", { prompt, ...options }, apiKey);
  },

  queryScript: async (projectId) => {
    const apiKey = accountManager.getApiKey();
    if (!apiKey) throw new Error("X2C account not bound");
    return request("script/query", { project_id: projectId }, apiKey);
  },

  produceVideo: async (projectId, episodeNumber = 1) => {
    const apiKey = accountManager.getApiKey();
    if (!apiKey) throw new Error("X2C account not bound");
    return request(
      "video/produce",
      { project_id: projectId, episode_number: episodeNumber },
      apiKey,
    );
  },

  queryVideo: async (projectId, episodeNumber = 1) => {
    const apiKey = accountManager.getApiKey();
    if (!apiKey) throw new Error("X2C account not bound");
    return request("video/query", { project_id: projectId, episode_number: episodeNumber }, apiKey);
  },
};
