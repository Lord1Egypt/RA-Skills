#!/usr/bin/env node
/**
 * query.mjs - 关键字检索 deep-memory 记忆索引
 * 
 * 功能概述：
 *   在 DEEP-MEMORY.md 索引文件（Markdown 表格）中根据关键字进行模糊匹配，
 *   返回所有匹配条目的信息（关键字、描述、文件路径）。
 * 
 * 匹配逻辑：
 *   采用双向包含匹配（case-insensitive），即以下任一条件成立即视为匹配：
 *     - 索引中的关键字包含查询词（如索引为 "@k3000"，查询 "k3000"）
 *     - 查询词包含索引中的关键字（如索引为 "fastify"，查询 "fastify,routing"）
 *   这种宽松策略可以让用户在只知道部分关键字时也能检索到结果。
 * 
 * 命令行用法：
 *   node query.mjs <关键字>
 *   例: node query.mjs fastify
 *        node query.mjs k3000
 * 
 * 输出格式（JSON）：
 *   - 有结果时：{ found: true, keyword: "...", results: [{ keyword, description, filePath }, ...] }
 *   - 无结果时：{ found: false, keyword: "..." }
 * 
 * 设计考量：
 *   输出 JSON 格式便于其他脚本或工具二次调用，不输出额外日志或彩色字符。
 */

import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

// -------------------------------------------------------------------
// 路径设置
// -------------------------------------------------------------------
// ESM 模块中通过 import.meta.url 反推当前脚本所在目录
const __dirname = dirname(fileURLToPath(import.meta.url));
// 索引文件位于工作区根目录 DEEP-MEMORY.md
const indexPath = resolve(__dirname, '../../../DEEP-MEMORY.md');

// -------------------------------------------------------------------
// 解析命令行参数
// -------------------------------------------------------------------
// process.argv 形状：[node路径, 脚本路径, 用户输入的关键字]
const keyword = process.argv[2] || '';

// 简单参数校验：必须提供关键字
if (!keyword) {
  // 将用法说明输出到 stderr，区别于正常结果的 stdout
  console.error('用法: node query.mjs <关键字>');
  process.exit(1);
}

// -------------------------------------------------------------------
// 读取并解析索引文件
// -------------------------------------------------------------------
// 读取整个索引文件内容（UTF-8 编码的 Markdown 文本）
const content = readFileSync(indexPath, 'utf-8');

// 按行分割，逐行处理 Markdown 表格
// 索引文件格式示例：
// | Keywords | Description | File |
// | --- | --- | --- |
// | fastify,routing | Fastify 常用路由技巧 | `deep-memory/2026-05-05 18_25_30.md` |
const lines = content.split('\n');
const results = [];

// -------------------------------------------------------------------
// 表格解析与匹配
// -------------------------------------------------------------------
/**
 * 遍历索引文件的每一行，识别有效的数据行并进行关键字匹配。
 * 
 * Markdown 表格行的特征：
 *   - 包含竖线 |
 *   - 不是表头行（如 "| Keywords |" 自身）
 *   - 不是分隔行（包含 "---"）
 * 
 * 有效数据行拆分后得到的三个字段：
 *   parts[0] = 关键字（可能包含 @ 前缀，如 "@k3000,fastify"）
 *   parts[1] = 描述文本
 *   parts[2] = 文件路径（带反引号包裹）
 */
for (const line of lines) {
  
  // 跳过不相关行：
  //   - 不含竖线：非表格行（普通文本、标题等）
  //   - 包含 ---：Markdown 表格分隔线（如 | --- | --- | --- |）
  //   - 以表头关键字开头（如 "| Keywords" 本身）
  if (!line.includes('|')
      || line.includes('---')
      || line.startsWith('| Keywords')) {
    continue;
  }

  // 竖线分割后得到数组，每个元素可能含前导/尾随空白，需 trim 清理
  // filter(Boolean) 移除空字符串（表格首尾竖线产生的空段）
  const parts = line.split('|').map(s => s.trim()).filter(Boolean);
  
  // 过滤掉列数不足的行（正常的有效行应有 3 列）
  if (parts.length < 2) continue;

  // 结构化解构：关键字 | 描述 | 文件路径
  const [kw, desc, filePath] = parts;
  
  /**
   * 匹配判断（大小写不敏感）：
   *   - kw 包含 keyword：索引关键字更具体，查询词更宽泛
   *     例：索引="@k3000,fastify"，查询="fastify"  → 包含匹配
   *   - keyword 包含 kw：查询词更具体，索引关键字更宽泛
   *     例：索引="fastify"，查询="@k3000,fastify"  → 被包含匹配
   * 
   * 这种双向匹配的好处：
   *   用户可以用部分关键字（如 "k3000"）匹配带前缀的索引（"@k3000"），
   *   也可以用完整列表（"k3000,fastify"）匹配单条索引（"fastify"）。
   */
  const kwLower = kw.toLowerCase();
  const keyLower = keyword.toLowerCase();
  
  const matched = kwLower.includes(keyLower) || keyLower.includes(kwLower);
  
  if (matched) {
    // 去除文件路径两端的反引号（如 "`deep-memory/xxx.md`" → "deep-memory/xxx.md"）
    results.push({
      keyword:    kw,
      description: desc,
      filePath:   filePath.replace(/`/g, ''),
    });
  }
}

// -------------------------------------------------------------------
// 输出结果
// -------------------------------------------------------------------
/**
 * 输出格式统一为 JSON，方便管道传给其他命令或脚本。
 * 不输出额外日志，保证 stdout 纯净。
 */
if (results.length === 0) {
  // 无匹配结果
  console.log(JSON.stringify({ found: false, keyword }));
} else {
  // 有匹配结果，包含匹配数和详细列表
  console.log(JSON.stringify({ found: true, keyword, results }));
}