/**
 * OpenClaw Config Tracker
 * 
 * 自动追踪并提交 OpenClaw 配置文件和关键 markdown 文件的变更
 * 
 * 触发时机：before_prompt_build hook - 每次对话轮次开始时检查并提交
 */

import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { execSync, spawnSync } from "node:child_process";

// ============================================================================
// Types
// ============================================================================

/**
 * @typedef {Object} ConfigTrackerConfig
 * @property {boolean} enabled
 * @property {string[]} workspaceFiles
 * @property {string} openclawConfig
 * @property {string} commitMessagePrefix
 * @property {string} gitUserName
 * @property {string} gitUserEmail
 */

// ============================================================================
// Config
// ============================================================================

const DEFAULT_CONFIG = {
  enabled: true,
  workspaceFiles: [
    "AGENTS.md",
    "USER.md",
    "SOUL.md",
    "MEMORY.md",
    "TOOLS.md",
    "HEARTBEAT.md",
    "IDENTITY.md"
  ],
  openclawConfig: "~/.openclaw/openclaw.json",
  commitMessagePrefix: "auto: track config changes",
  gitUserName: "OpenClaw Bot",
  gitUserEmail: "openclaw@localhost"
};

// ============================================================================
// Logger
// ============================================================================

const log = {
  debug: (...args) => console.log("[config-tracker:debug]", ...args),
  info: (...args) => console.log("[config-tracker]", ...args),
  warn: (...args) => console.warn("[config-tracker]", ...args),
  error: (...args) => console.error("[config-tracker]", ...args),
};

// ============================================================================
// Helper Functions
// ============================================================================

function expandTilde(filePath) {
  if (filePath.startsWith("~/") || filePath === "~") {
    return path.join(os.homedir(), filePath.slice(2));
  }
  return filePath;
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function gitExists(repoDir) {
  try {
    await fs.access(path.join(repoDir, ".git"));
    return true;
  } catch {
    return false;
  }
}

// ============================================================================
// Git Operations
// ============================================================================

async function gitRun(repoDir, args, gitConfig = null) {
  const env = { ...process.env };
  const configArgs = gitConfig
    ? ["-c", `user.name=${gitConfig.name}`, "-c", `user.email=${gitConfig.email}`]
    : [];
  
  try {
    const result = spawnSync("git", [...configArgs, ...args], {
      cwd: repoDir,
      env,
      encoding: "utf-8",
      timeout: 30000
    });
    
    if (result.error) {
      throw new Error(`git ${args.join(" ")} failed: ${result.error.message}`);
    }
    
    if (result.status !== 0) {
      throw new Error(`git ${args.join(" ")} exited with code ${result.status}: ${result.stderr}`);
    }
    
    return result.stdout || "";
  } catch (error) {
    throw new Error(`git ${args.join(" ")} failed: ${error.message}`);
  }
}

async function initGitRepo(repoDir, config) {
  if (await gitExists(repoDir)) {
    log.info(`Git repo already exists at ${repoDir}`);
    return;
  }
  
  log.info(`Initializing git repo at ${repoDir}`);
  
  // Initialize repo
  await gitRun(repoDir, ["init"], { name: config.gitUserName, email: config.gitUserEmail });
  
  // Create a dummy initial commit
  const placeholderPath = path.join(repoDir, ".gitkeep");
  await fs.writeFile(placeholderPath, "");
  await gitRun(repoDir, ["add", ".gitkeep"], { name: config.gitUserName, email: config.gitUserEmail });
  await gitRun(repoDir, ["commit", "-m", "Initial commit"], { name: config.gitUserName, email: config.gitUserEmail });
  
  // Remove placeholder
  await fs.unlink(placeholderPath);
}

async function hasChanges(repoDir, files) {
  try {
    const result = await gitRun(repoDir, ["status", "--porcelain", "--", ...files]);
    const changed = result
      .split("\n")
      .filter(line => line.trim().length > 0)
      .map(line => line.slice(3).trim()); // Remove status prefix like " M" or "??"
    
    return changed;
  } catch (error) {
    log.error("Error checking git status:", error);
    return [];
  }
}

async function getDiffSummary(repoDir, files) {
  const summaries = [];
  
  for (const file of files) {
    try {
      // Get diff for each file
      const diff = await gitRun(repoDir, ["diff", "--cached", "--", file]);
      if (diff.trim()) {
        // Parse diff to generate summary
        const lines = diff.split("\n");
        const additions = lines.filter(l => l.startsWith("+") && !l.startsWith("+++")).length;
        const deletions = lines.filter(l => l.startsWith("-") && !l.startsWith("---")).length;
        
        // Generate simple path display: just the filename with repo indicator
        const fileName = path.basename(file);
        const repoLabel = repoDir.includes('.openclaw') ? '.openclaw/' : 'workspace/';
        const displayPath = `${repoLabel}${fileName}`;
        
        // Generate natural language description
        const description = generateChangeDescription(file, diff, additions, deletions);
        
        summaries.push({
          path: displayPath,
          stats: `+${additions} -${deletions}`,
          description: description
        });
      }
    } catch (error) {
      log.warn(`Failed to get diff for ${file}:`, error.message);
    }
  }
  
  return summaries;
}

function generateChangeDescription(filePath, diff, additions, deletions) {
  const fileName = path.basename(filePath);
  const lines = diff.split("\n").filter(l => l.startsWith("+") && !l.startsWith("+++"));
  
  // Analyze content patterns
  const addedText = lines.map(l => l.slice(1).trim()).join(" ").toLowerCase();
  
  // Pattern matching for common changes
  if (fileName === "HEARTBEAT.md") {
    if (addedText.includes("[ ]") || addedText.includes("- [ ]")) {
      return `添加新的心跳任务项`;
    }
    if (addedText.includes("[x]") || addedText.includes("- [x]")) {
      return `标记任务为已完成`;
    }
    if (additions > deletions) {
      return `更新心跳任务配置，添加 ${additions} 行新内容`;
    }
  }
  
  if (fileName === "MEMORY.md") {
    if (addedText.includes("##") || addedText.includes("###")) {
      return `添加新的记忆条目或小节`;
    }
    return `更新长期记忆，添加 ${additions} 行内容`;
  }
  
  if (fileName === "openclaw.json") {
    if (addedText.includes("plugin") || addedText.includes("enabled")) {
      return `修改插件配置，启用或调整功能`;
    }
    if (addedText.includes("model") || addedText.includes("provider")) {
      return `调整模型或 Provider 配置`;
    }
    return `更新 OpenClaw 主配置文件`;
  }
  
  if (fileName === "AGENTS.md" || fileName === "SOUL.md" || fileName === "USER.md") {
    return `更新 Agent 配置文档，修改 ${additions} 行内容`;
  }
  
  if (fileName.endsWith(".md")) {
    if (additions > 10) {
      return `大幅修改文档内容，添加 ${additions} 行，删除 ${deletions} 行`;
    }
    return `修改文档内容，添加 ${additions} 行，删除 ${deletions} 行`;
  }
  
  // Default description
  return `修改文件，添加 ${additions} 行，删除 ${deletions} 行`;
}

async function commitChanges(repoDir, files, config) {
  if (files.length === 0) {
    return;
  }
  
  const timestamp = new Date().toISOString().slice(0, 19).replace("T", " ");
  
  log.info(`Committing changes: ${files.join(", ")}`);
  
  try {
    // Add specific files only - never use git add .
    await gitRun(repoDir, ["add", ...files], { name: config.gitUserName, email: config.gitUserEmail });
    
    // Check if there are staged changes
    const status = await gitRun(repoDir, ["status", "--porcelain"]);
    if (!status.trim()) {
      log.debug("No staged changes to commit");
      return;
    }
    
    // Generate change descriptions AFTER staging (so --cached works)
    const changeSummaries = await getDiffSummary(repoDir, files);
    
    // Build commit message with descriptions
    let message = `${config.commitMessagePrefix} [${timestamp}]`;
    if (changeSummaries.length > 0) {
      message += "\n\n" + changeSummaries.map(s => 
        `${s.path} (${s.stats}): ${s.description}`
      ).join("\n");
    }
    
    await gitRun(repoDir, ["commit", "-m", message], { name: config.gitUserName, email: config.gitUserEmail });
    log.info(`Committed: ${message.split("\n")[0]}`);
    log.debug(`Full commit message:\n${message}`);
  } catch (error) {
    log.error("Error committing changes:", error);
  }
}

// ============================================================================
// Main Plugin
// ============================================================================

/**
 * @param {Object} api - OpenClawPluginApi
 * @param {Object} options
 * @param {ConfigTrackerConfig} [options.config]
 */
export function registerConfigTrackerPlugin(api, options = {}) {
  return new ConfigTrackerPlugin(api, options.config);
}

class ConfigTrackerPlugin {
  /**
   * @param {Object} api - OpenClawPluginApi
   * @param {ConfigTrackerConfig} [userConfig]
   */
  constructor(api, userConfig) {
    this.api = api;
    this.config = { ...DEFAULT_CONFIG, ...userConfig };
    this.lastCheckTime = 0;
    this.cooldownMs = 5000; // Prevent multiple commits in quick succession
    
    log.info("ConfigTracker plugin initialized");
    log.debug("Config:", JSON.stringify(this.config));
    
    // Register hook
    this.api.on("before_prompt_build", async (event, ctx) => {
      await this.before_prompt_build(ctx);
    });
  }
  
  async before_prompt_build(context) {
    if (!this.config.enabled) {
      return;
    }
    
    // Cooldown check - prevent too frequent commits
    const now = Date.now();
    if (now - this.lastCheckTime < this.cooldownMs) {
      return;
    }
    
    await this.checkAndCommit(context.workspaceDir);
    this.lastCheckTime = now;
  }
  
  async checkAndCommit(workspaceDir) {
    // Get workspace absolute path
    const workspacePath = path.resolve(workspaceDir);
    
    // 1. Track workspace markdown files
    const workspaceFiles = this.config.workspaceFiles.map(f => path.join(workspacePath, f));
    const existingWorkspaceFiles = await Promise.all(
      workspaceFiles.map(async (f) => ({
        path: f,
        exists: await fileExists(f)
      }))
    );
    
    const validWorkspaceFiles = existingWorkspaceFiles
      .filter(f => f.exists)
      .map(f => f.path);
    
    if (validWorkspaceFiles.length > 0) {
      // Ensure git repo exists for workspace
      await initGitRepo(workspacePath, this.config);
      
      const changedWorkspaceFiles = await hasChanges(workspacePath, validWorkspaceFiles);
      if (changedWorkspaceFiles.length > 0) {
        await commitChanges(workspacePath, changedWorkspaceFiles, this.config);
      }
    }
    
    // 2. Track openclaw.json
    const openclawConfigPath = expandTilde(this.config.openclawConfig);
    const openclawDir = path.dirname(openclawConfigPath);
    
    if (await fileExists(openclawConfigPath)) {
      // Ensure git repo exists for ~/.openclaw/
      await initGitRepo(openclawDir, this.config);
      
      const changedConfigFiles = await hasChanges(openclawDir, [openclawConfigPath]);
      if (changedConfigFiles.length > 0) {
        await commitChanges(openclawDir, changedConfigFiles, this.config);
      }
    }
  }
}

// ============================================================================
// Export for skill loading
// ============================================================================

export function register(config) {
  return function (api) {
    return registerConfigTrackerPlugin(api, { config });
  };
}

// Default export for OpenClaw plugin system
export default registerConfigTrackerPlugin;

export { DEFAULT_CONFIG };
