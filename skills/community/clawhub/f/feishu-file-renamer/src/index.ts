/**
 * feishu-file-renamer - 飞书文件重命名助手
 * 
 * 解决飞书机器人下载文件时文件名变成哈希值的问题：
 * - 恢复原始文件名
 * - 批量重命名
 * - 飞书消息集成
 * - 多维表格联动
 * 
 * 触发命令：/rename-file, /feishu-rename, /restore-filename
 * 自然语言：重命名文件、恢复文件名、飞书文件
 */

import { existsSync, renameSync, writeFileSync, readFileSync } from 'fs';
import { join, dirname, basename, extname } from 'path';

/**
 * 文件映射接口
 */
interface FileMapping {
  hashFile: string;      // 哈希文件名（下载的文件）
  originalName: string;  // 原始文件名
  messageId?: string;    // 消息 ID（可选）
}

/**
 * 重命名结果接口
 */
interface RenameResult {
  success: number;
  failed: number;
  skipped: number;
  errors: string[];
}

/**
 * 恢复单个文件名
 */
export function restoreFileName(
  hashFile: string,
  originalName: string
): string {
  const ext = extname(hashFile);
  const baseName = basename(originalName, extname(originalName));
  const newName = `${baseName}${ext}`;
  const newPath = join(dirname(hashFile), newName);
  
  // 处理文件名冲突
  let counter = 1;
  let finalPath = newPath;
  while (existsSync(finalPath)) {
    finalPath = join(dirname(hashFile), `${baseName}_${counter}${ext}`);
    counter++;
  }
  
  renameSync(hashFile, finalPath);
  return finalPath;
}

/**
 * 批量重命名
 */
export function batchRename(
  mappings: FileMapping[],
  outputDir?: string
): RenameResult {
  const result: RenameResult = {
    success: 0,
    failed: 0,
    skipped: 0,
    errors: [],
  };
  
  for (const mapping of mappings) {
    try {
      if (!existsSync(mapping.hashFile)) {
        result.skipped++;
        result.errors.push(`文件不存在：${mapping.hashFile}`);
        continue;
      }
      
      const newPath = restoreFileName(mapping.hashFile, mapping.originalName);
      result.success++;
    } catch (error: any) {
      result.failed++;
      result.errors.push(`${mapping.hashFile}: ${error.message}`);
    }
  }
  
  return result;
}

/**
 * 智能重命名（根据上下文生成文件名）
 */
export function smartRename(
  hashFile: string,
  context?: string
): string {
  const ext = extname(hashFile);
  const timestamp = Date.now();
  
  let baseName = 'downloaded';
  if (context) {
    // 过滤特殊字符，保留中文、英文、数字、下划线
    baseName = context.replace(/[^a-zA-Z0-9\u4e00-\u9fa5_]/g, '_').substring(0, 50);
  }
  
  const newName = `${baseName}_${timestamp}${ext}`;
  const newPath = join(dirname(hashFile), newName);
  
  renameSync(hashFile, newPath);
  return newPath;
}

/**
 * 从飞书消息提取文件映射
 */
export function extractFileMappingsFromMessage(
  message: string
): FileMapping[] {
  const mappings: FileMapping[] = [];
  
  // 匹配飞书文件消息格式
  // 示例：[file_v3_0210g_xxx.pdf](产品规格书.pdf)
  const filePattern = /\[(file_v3_[^\]]+)\]\(([^\)]+)\)/g;
  let match;
  
  while ((match = filePattern.exec(message)) !== null) {
    mappings.push({
      hashFile: match[1],
      originalName: match[2],
    });
  }
  
  // 匹配图片格式
  // 示例：[img_v3_0210g_xxx.png](产品图.png)
  const imgPattern = /\[(img_v3_[^\]]+)\]\(([^\)]+)\)/g;
  
  while ((match = imgPattern.exec(message)) !== null) {
    mappings.push({
      hashFile: match[1],
      originalName: match[2],
    });
  }
  
  return mappings;
}

/**
 * 生成重命名日志
 */
export function generateRenameLog(result: RenameResult): string {
  const log = `# 文件重命名日志

**生成时间**: ${new Date().toLocaleString('zh-CN')}

## 统计
- ✅ 成功：${result.success}
- ❌ 失败：${result.failed}
- ⏭️  跳过：${result.skipped}

## 错误详情
${result.errors.length > 0 
  ? result.errors.map(e => `- ${e}`).join('\n')
  : '无错误'}

---
*日志由 feishu-file-renamer 生成*
`;
  
  return log;
}

/**
 * 匹配触发关键词
 */
function matchesTrigger(message: string): boolean {
  const triggers = [
    '/rename-file',
    '/feishu-rename',
    '/restore-filename',
    '重命名文件',
    '恢复文件名',
    '飞书文件',
    '哈希文件名',
    '批量重命名',
  ];
  
  const lowerMessage = message.toLowerCase().trim();
  return triggers.some(trigger => lowerMessage.includes(trigger.toLowerCase()));
}

/**
 * 主处理函数
 */
export async function handleFeishuFileRenamer(
  message: string,
  context?: any
): Promise<string | null> {
  if (!matchesTrigger(message)) {
    return null;
  }
  
  // 提取文件映射
  const mappings = extractFileMappingsFromMessage(message);
  
  if (mappings.length === 0) {
    return `### 📁 飞书文件重命名助手

**使用方法：**

**方式 1：单文件重命名**
\`\`\`bash
claw skill run feishu-file-renamer \\
  --file "/tmp/download/img_v3_xxx.png" \\
  --name "产品宣传图.png"
\`\`\`

**方式 2：批量重命名（从消息）**
\`\`\`bash
claw skill run feishu-file-renamer \\
  --message-id "om_x100b520xxx" \\
  --output-dir "/tmp/renamed"
\`\`\`

**方式 3：从多维表格**
\`\`\`bash
claw skill run feishu-file-renamer \\
  --bitable "APP_TOKEN" \\
  --table "TABLE_ID"
\`\`\`

---

**自然语言使用：**
发送包含文件的消息，然后回复：
- "重命名这些文件"
- "恢复文件名"
- "/rename-file"

---

*支持飞书私信、群聊、云文档附件*`;
  }
  
  // 执行批量重命名
  const result = batchRename(mappings);
  
  // 生成日志
  const log = generateRenameLog(result);
  const logPath = '/tmp/rename_log.md';
  writeFileSync(logPath, log, 'utf-8');
  
  return `### ✅ 文件重命名完成

**统计结果：**
- ✅ 成功：${result.success}
- ❌ 失败：${result.failed}
- ⏭️  跳过：${result.skipped}

${result.errors.length > 0 ? `
**错误详情：**
${result.errors.slice(0, 5).map(e => `- ${e}`).join('\n')}
${result.errors.length > 5 ? `\n... 还有 ${result.errors.length - 5} 个错误` : ''}
` : ''}

**重命名日志：** ${logPath}

---

### 📝 下一步

1. 查看重命名后的文件
2. 检查日志中的错误信息
3. 如有问题，提供详细信息

---

*支持飞书私信、群聊、云文档附件*`;
}

// 导出给 OpenClaw 使用
export default {
  name: 'feishu-file-renamer',
  version: '1.0.0',
  description: '飞书文件重命名助手 - 恢复原始文件名、批量处理',
  triggers: ['/rename-file', '/feishu-rename', '重命名文件'],
  handler: handleFeishuFileRenamer,
};
