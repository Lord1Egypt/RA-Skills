#!/usr/bin/env node
/**
 * add.mjs - 新增 deep-memory 记忆条目
 * 
 * 功能概述：
 *   向 deep-memory 系统中添加一个新的记忆条目，包括标题、关键字、描述和正文内容。
 *   支持两种使用方式：
 *     1. 命令行模式：一次性传入所有参数，适合脚本或自动化调用
 *     2. 交互模式：不带参数时启动问答式交互，适合手动使用
 * 
 * 命令行用法：
 *   node add.mjs [标题] [关键字1,关键字2] [描述] [正文...]
 *   例: node add.mjs "Fastify 路由技巧" "fastify,routing" "总结几种常用路由写法" "更多内容..."
 * 
 * 交互模式用法：
 *   node add.mjs
 *   然后按提示依次输入标题、关键字（逗号分隔）、描述，正文通过 Ctrl+D 结束输入
 * 
 * 输出：
 *   - 在 deep-memory/ 目录下创建以时间戳命名的 .md 文件
 *   - 自动更新根目录的 DEEP-MEMORY.md 索引表格
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

// -------------------------------------------------------------------
// 路径设置
// -------------------------------------------------------------------
// 由于是 ESM 模块，无法使用 __dirname，手动通过 import.meta.url 反推
const __dirname = dirname(fileURLToPath(import.meta.url));
// 工作区根目录（lab1），deep-memory 目录和索引文件都相对于此
const ROOT = resolve(__dirname, '../../../');
// 记忆文件存放目录：<ROOT>/deep-memory/
const DEEP_MEM_DIR = resolve(ROOT, 'deep-memory');
// 主索引文件路径，格式为 Markdown 表格
const INDEX_PATH = resolve(ROOT, 'DEEP-MEMORY.md');

// -------------------------------------------------------------------
// 辅助函数：生成时间戳文件名
// -------------------------------------------------------------------
/**
 * 生成形如 "2026-05-05 18_25_30" 的时间戳字符串，
 * 用于给记忆文件命名，保证唯一性与可排序性。
 * 注意：时分秒之间用下划线而非冒号，是避免文件系统路径歧义。
 */
function now() {
  const d = new Date();
  // 补零工具：确保一位数也显示为两位，如 9 -> "09"
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} `
       + `${pad(d.getHours())}_${pad(d.getMinutes())}_${pad(d.getSeconds())}`;
}

// -------------------------------------------------------------------
// 辅助函数：向用户提一个问题并等待回答
// -------------------------------------------------------------------
/**
 * 使用 readline 模块向标准输出打印问题，并从标准输入读取用户回答。
 * 返回一个 Promise， resolve 后即为用户输入的字符串（不含换行符）。
 * 
 * @param {string} question - 要打印给用户的问题提示文本
 * @returns {Promise<string>} 用户输入的原始字符串
 */
async function prompt(question) {
  const readline = await import('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  // question() 是异步的，但 readline.createInterface 不是 promise，
  // 所以用 Promise 包装回调风格的 question()
  return new Promise(resolve => {
    rl.question(question, ans => {
      rl.close();
      resolve(ans);
    });
  });
}

// -------------------------------------------------------------------
// 辅助函数：从 stdin 读取多行正文内容
// -------------------------------------------------------------------
/**
 * 读取用户在交互模式下输入的大段正文（可能包含多行）。
 * 用户按 Ctrl+D (Unix) / Ctrl+Z + 回车 (Windows) 表示结束。
 * 
 * @returns {Promise<string>} 用户输入的完整文本
 */
function readContentStdin() {
  return new Promise(resolve => {
    let data = '';
    process.stdin.setEncoding('utf-8');
    // data 事件：每当 stdin 收到一行数据就累加
    process.stdin.on('data', chunk => data += chunk);
    // end 事件：用户发送 EOF 信号后触发，此时 data 即为完整内容
    process.stdin.on('end', () => resolve(data));
  });
}

// -------------------------------------------------------------------
// 主逻辑
// -------------------------------------------------------------------
/**
 * 程序入口。根据参数数量决定是命令行模式还是交互模式：
 * 
 * - 命令行模式（process.argv.length > 3）：
 *     argv[2] = 标题
 *     argv[3] = 关键字列表（逗号分隔）
 *     argv[4] = 描述
 *     argv[5...] = 正文（多个元素用空格连接）
 * 
 * - 交互模式（参数不足）：
 *     依次向用户询问标题、关键字、描述、正文
 * 
 * 执行步骤：
 *   1. 参数解析 / 交互收集数据
 *   2. 校验标题和关键字非空
 *   3. 在 deep-memory/ 下创建 .md 文件
 *   4. 在 DEEP-MEMORY.md 索引表中追加一行
 */
async function main() {
  let title, keywords, description, content;

  // -------------------------------------------------------
  // 步骤 1：解析输入参数（CLI 或交互）
  // -------------------------------------------------------
  if (process.argv.length > 3) {
    // ---- 命令行模式 ----
    // 格式：node add.mjs <标题> <关键字> <描述> [正文...]
    title       = process.argv[2];
    // 关键字支持多个，用逗号分隔，去首尾空白
    keywords    = process.argv[3].split(',').map(k => k.trim());
    description = process.argv[4] || '';
    // 正文可能包含空格，所以取 argv[5] 之后所有元素，用换行拼接
    content     = process.argv.slice(5).join('\n');
  } else {
    // ---- 交互模式 ----
    console.log('=== 新增 Deep Memory 条目 ===\n');
    
    title = await prompt('标题: ');
    
    const kwInput = await prompt('关键字（逗号分隔，如 @k3000,fastify）: ');
    // 分割后去空并过滤掉空字符串（如连续逗号产生的情况）
    keywords = kwInput.split(',').map(k => k.trim()).filter(Boolean);
    
    description = await prompt('描述: ');
    
    console.log('\n内容（输入完成后按 Ctrl+D）:\n');
    content = await readContentStdin();
  }

  // -------------------------------------------------------
  // 步骤 2：参数校验
  // -------------------------------------------------------
  if (!title) {
    console.error('❌ 标题不能为空');
    process.exit(1);
  }
  if (keywords.length === 0) {
    console.error('❌ 至少需要一个关键字');
    process.exit(1);
  }

  // -------------------------------------------------------
  // 步骤 3：写入记忆文件
  // -------------------------------------------------------
  // 文件名使用时间戳确保唯一，如 "2026-05-05 18_25_30.md"
  const filename  = `${now()}.md`;
  const filepath  = resolve(DEEP_MEM_DIR, filename);
  
  // 按固定格式组装 Markdown 内容
  // ## 关键字 以列表形式呈现，方便索引脚本解析
  const fullContent = [
    `# ${title}`,
    '',
    '## 关键字',
    ...keywords.map(k => `- ${k}`),
    '',
    '## 描述',
    description,
    '',
    content,        // 正文原样追加，可能为空
  ].join('\n');
  
  writeFileSync(filepath, fullContent, 'utf-8');
  console.log(`\n✅ 记忆已保存: deep-memory/${filename}`);

  // -------------------------------------------------------
  // 步骤 4：更新主索引 DEEP-MEMORY.md
  // -------------------------------------------------------
  // 索引是 Markdown 表格，格式为：
  // | Keywords | Description | File |
  // | --- | --- | --- |
  // | fastify | 路由技巧 | `deep-memory/2026-...md` |
  // 
  // 我们在表头分隔线（---）之后插入新行，保持格式整洁
  const relPath      = `deep-memory/${filename}`;
  const indexContent = readFileSync(INDEX_PATH, 'utf-8');
  
  // 构造新索引行，关键字用逗号连接
  const newEntry = `\n| ${keywords.join(', ')} | ${description} | \`${relPath}\` |`;
  
  const lines = indexContent.split('\n');
  // 找到 Markdown 表格分隔行（在表头之后的那条 --- | --- | --- 线）的位置
  const insertAt = lines.findIndex(l => l.includes('---'));
  
  if (insertAt !== -1) {
    // 在分隔线之后插入，保持表头和数据的清晰分隔
    lines.splice(insertAt, 0, newEntry);
  } else {
    // 找不到分隔线（索引文件可能被破坏），直接追加到末尾
    lines.push(newEntry);
  }
  
  writeFileSync(INDEX_PATH, lines.join('\n'), 'utf-8');
  console.log('✅ 索引已更新');
}

// -------------------------------------------------------------------
// 启动
// -------------------------------------------------------------------
// async IIFE，避免顶层 await 兼容性问题
main().catch(console.error);