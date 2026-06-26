#!/usr/bin/env node

/**
 * 飞书凭证配置工具
 * 帮助用户快速配置飞书 API 凭证
 */

import * as fs from "fs";
import * as path from "path";
import * as readline from "readline";

const CREDENTIALS_FILE = path.join(process.env.HOME, ".openclaw", "feishu-credentials.json");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askQuestion(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

async function main() {
  console.log("📝 飞书凭证配置工具\n");
  console.log("此工具将帮助你配置飞书 API 凭证，用于工作日志记录功能。\n");
  
  // 检查是否已存在配置
  if (fs.existsSync(CREDENTIALS_FILE)) {
    console.log("⚠️  检测到已存在的配置文件：");
    console.log(`   ${CREDENTIALS_FILE}\n`);
    
    const existing = JSON.parse(fs.readFileSync(CREDENTIALS_FILE, "utf-8"));
    console.log("当前配置：");
    console.log(`  App ID: ${existing.app_id || "未设置"}`);
    console.log(`  App Secret: ${existing.app_secret ? "********" + existing.app_secret.slice(-4) : "未设置"}`);
    console.log(`  Root Folder Token: ${existing.root_folder_token || "未设置"}\n`);
    
    const overwrite = await askQuestion("是否覆盖现有配置？(y/n) [n]: ");
    if (overwrite.toLowerCase() !== "y") {
      console.log("\n✅ 已取消，保留现有配置。");
      rl.close();
      return;
    }
  }
  
  console.log("\n📖 获取凭证指南：");
  console.log("  1. 访问 https://open.feishu.cn/ 创建应用");
  console.log("  2. 在「凭证管理」获取 App ID 和 App Secret");
  console.log("  3. 在云空间 URL 中获取 Folder Token（或使用 \"root\" 表示根目录）\n");
  
  const appId = await askQuestion("请输入 App ID (格式：cli_xxx): ");
  const appSecret = await askQuestion("请输入 App Secret: ");
  const rootToken = await askQuestion("请输入 Folder Token (或直接回车使用 \"root\"): ");
  
  const config = {
    app_id: appId.trim() || "cli_a93b936aa9391cc7",
    app_secret: appSecret.trim() || "aMRJMyi3KSXbSJhRgyx7ycvyT5D3rsrs",
    root_folder_token: rootToken.trim() || "root"
  };
  
  // 确保目录存在
  const configDir = path.dirname(CREDENTIALS_FILE);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  // 写入配置
  fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(config, null, 2));
  
  console.log("\n✅ 配置已保存：");
  console.log(`   ${CREDENTIALS_FILE}\n`);
  console.log("📋 配置内容：");
  console.log(`  App ID: ${config.app_id}`);
  console.log(`  App Secret: ${config.app_secret ? "********" + config.app_secret.slice(-4) : "未设置"}`);
  console.log(`  Root Folder Token: ${config.root_folder_token}\n`);
  
  console.log("💡 下一步：");
  console.log("  1. 确保飞书应用已添加以下权限：");
  console.log("     - drive:drive (云盘文件管理)");
  console.log("     - docx:document (文档创建和编辑)");
  console.log("  2. 发布应用使权限生效");
  console.log("  3. 运行以下命令测试：");
  console.log(`     cd /Users/one/.openclaw/workspace/skills/feishu-log`);
  console.log(`     node log-work.mjs\n`);
  
  rl.close();
}

main().catch(console.error);
