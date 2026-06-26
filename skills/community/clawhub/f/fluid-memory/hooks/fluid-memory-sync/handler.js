/**
 * Fluid Memory Sync Hook
 * 记录对话到临时文件，等 OpenClaw 原生 flush 触发时再处理
 */

import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import os from "os";

const USER_HOME = os.homedir();
const FLUID_SKILL_PATH = path.join(
  USER_HOME,
  ".openclaw",
  "workspace",
  "skills",
  "fluid-memory",
  "fluid_skill.py"
);

const CONVERSATION_LOG = path.join(
  USER_HOME,
  ".openclaw",
  "workspace",
  "database",
  "conversation_log.txt"
);

function getPythonPath() {
  const candidates = [
    "python",
    "python3",
    path.join(USER_HOME, "miniconda3", "python.exe"),
    path.join(USER_HOME, "anaconda3", "python.exe"),
  ];
  
  for (const candidate of candidates) {
    try {
      return candidate;
    } catch (e) {
      continue;
    }
  }
  return "python";
}

export default async function handler(event) {
  // Only handle message:sent events
  if (event.type !== "message" || event.action !== "sent") {
    return;
  }

  // Skip if no content
  if (!event.content) {
    return;
  }

  try {
    // 记录对话到临时文件
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] 用户说: ${event.content}\n`;
    
    // 确保目录存在
    const dir = path.dirname(CONVERSATION_LOG);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    // 追加到日志文件
    fs.appendFileSync(CONVERSATION_LOG, logEntry);
    
    console.log("[fluid-memory-sync] 对话已记录，等待原生 flush 触发...");
    
  } catch (error) {
    console.error("[fluid-memory-sync] Failed to log conversation:", error.message);
  }
}
