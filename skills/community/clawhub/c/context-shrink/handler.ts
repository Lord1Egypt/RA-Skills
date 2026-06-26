import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

// 配置参数
const CONTEXT_THRESHOLD = 0.85; // 60% 触发阈值
const DAYS_TO_KEEP = 3; // 保留最近 N 天日志
const MIN_FILES_TO_KEEP = 5; // 至少保留文件数
const COMPRESSION_MODEL = 'ollama-remote/qwen2.5:0.5b'; // 轻量压缩模型

/**
 * Context Monitor Hook Handler
 * 
 * 监听 message:sent 和 command:reset 事件，检查 context 使用率
 * 超过阈值时自动清理早期记忆并压缩
 */
const handler = async (event: any) => {
  const { type, action, context, sessionKey, timestamp, messages } = event;
  
  // 只处理特定事件
  if (type !== 'message' || !(['sent', 'received'].includes(action))) {
    return;
  }
  
  if (type !== 'command' || action !== 'reset') {
    return;
  }
  
  // 获取 workspace 目录
  const workspaceDir = context?.workspaceDir || process.env.HOME + '/.openclaw/workspace';
  const memoryDir = path.join(workspaceDir, 'memory');
  
  if (!fs.existsSync(memoryDir)) {
    console.log(`[context-monitor] Memory directory not found: ${memoryDir}`);
    return;
  }
  
  // 检查 context 使用率
  const usage = context?.sessionEntry?.usage;
  if (!usage) {
    return; // 没有使用数据，跳过
  }
  
  const promptTokens = usage.promptTokens || 0;
  const completionTokens = usage.completionTokens || 0;
  const totalTokens = promptTokens + completionTokens;
  
  // 获取模型的 maxTokens（假设 128K）
  const maxTokens = 128000;
  const usagePercent = totalTokens / maxTokens;
  
  console.log(`[context-monitor] Context usage: ${(usagePercent * 100).toFixed(1)}% (${totalTokens.toLocaleString()}/${maxTokens.toLocaleString()} tokens)`);
  
  // 如果未超过阈值，不执行操作
  if (usagePercent < CONTEXT_THRESHOLD) {
    console.log(`[context-monitor] Below threshold (${(CONTEXT_THRESHOLD * 100).toFixed(0)}%), no action needed`);
    return;
  }
  
  // 触发清理流程
  messages.push(`🔥 Context 使用率 ${(usagePercent * 100).toFixed(1)}% 超过阈值，启动自动清理...`);
  
  try {
    // 1. 获取所有记忆文件
    const memoryFiles = fs.readdirSync(memoryDir)
      .filter(file => file.match(/\d{4}-\d{2}-\d{2}\.md/))
      .sort();
    
    if (memoryFiles.length === 0) {
      console.log('[context-monitor] No memory files to clean');
      return;
    }
    
    console.log(`[context-monitor] Found ${memoryFiles.length} memory files`);
    
    // 2. 计算需要删除的文件（保留最近 N 天）
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - DAYS_TO_KEEP);
    
    const filesToDelete: string[] = [];
    const filesToKeep: string[] = [];
    
    for (const file of memoryFiles) {
      const fileDate = new Date(file.replace(/\.md$/, ''));
      if (fileDate < cutoffDate) {
        filesToDelete.push(file);
      } else {
        filesToKeep.push(file);
      }
    }
    
    // 确保至少保留 MIN_FILES_TO_KEEP 个文件
    if (filesToKeep.length < MIN_FILES_TO_KEEP) {
      const filesToRestore = filesToDelete.slice(0, MIN_FILES_TO_KEEP - filesToKeep.length);
      filesToKeep.push(...filesToRestore);
      filesToDelete.splice(0, filesToRestore.length);
    }
    
    console.log(`[context-monitor] Will delete ${filesToDelete.length} files, keep ${filesToKeep.length} files`);
    
    if (filesToDelete.length === 0) {
      console.log('[context-monitor] No files to delete');
      messages.push(`✅ 已保留所有记忆文件（${filesToKeep.length}个）`);
      return;
    }
    
    // 3. 读取要删除的文件内容（用于压缩）
    let rawMemoryContent = '';
    for (const file of filesToDelete) {
      const filePath = path.join(memoryDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      rawMemoryContent += `\n=== ${file} ===\n${content}\n`;
    }
    
    console.log(`[context-monitor] Read ${rawMemoryContent.length.toLocaleString()} characters from ${filesToDelete.length} files`);
    
    // 4. 压缩记忆（调用外部工具或简单处理）
    // TODO: 这里可以调用 memory-compression-system 或 ollama 进行智能压缩
    const compressedMemory = await compressMemory(rawMemoryContent);
    
    console.log(`[context-monitor] Compressed ${rawMemoryContent.length.toLocaleString()} → ${compressedMemory.length.toLocaleString()} chars (${(1 - compressedMemory.length / rawMemoryContent.length) * 100.toFixed(0)}% compression)`);
    
    // 5. 更新 MEMORY.md（追加压缩后的内容）
    const memoryMdPath = path.join(workspaceDir, 'MEMORY.md');
    if (fs.existsSync(memoryMdPath)) {
      const existingMemory = fs.readFileSync(memoryMdPath, 'utf-8');
      const newMemory = `\n## Compressed Memory (${cutoffDate.toISOString().split('T')[0]})\n\n${compressedMemory}\n`;
      fs.writeFileSync(memoryMdPath, existingMemory + newMemory);
      console.log(`[context-monitor] Updated MEMORY.md with compressed memory`);
    } else {
      fs.writeFileSync(memoryMdPath, `# Compressed Memories\n\n${compressedMemory}\n`);
      console.log(`[context-monitor] Created MEMORY.md with compressed memory`);
    }
    
    // 6. 删除旧文件
    for (const file of filesToDelete) {
      const filePath = path.join(memoryDir, file);
      fs.unlinkSync(filePath);
      console.log(`[context-monitor] Deleted: ${file}`);
    }
    
    // 7. Git 提交
    try {
      // 添加所有变更
      execSync(`cd ${workspaceDir} && git add -A`, { stdio: 'pipe' });
      
      // 提交
      const commitMessage = `chore: context monitor cleanup (${filesToDelete.length} files)\n\n- Deleted ${filesToDelete.length} old memory files\n- Compressed ${(rawMemoryContent.length / 1024).toFixed(1)}KB → ${(compressedMemory.length / 1024).toFixed(1)}KB\n- Kept ${filesToKeep.length} recent files`;
      execSync(`cd ${workspaceDir} && git commit -m "${commitMessage.replace(/"/g, '\"')}"`, { stdio: 'pipe' });
      
      // 可选：推送
      // execSync(`cd ${workspaceDir} && git push`, { stdio: 'pipe' });
      
      console.log('[context-monitor] Git commit successful');
      messages.push(`📦 已清理 ${filesToDelete.length} 个旧文件，压缩 ${(rawMemoryContent.length / 1024).toFixed(1)}KB → ${(compressedMemory.length / 1024).toFixed(1)}KB`);
    } catch (gitError) {
      console.error('[context-monitor] Git commit failed:', gitError);
      messages.push(`⚠️ Git 提交失败，但文件已清理（请手动提交）`);
    }
    
  } catch (error) {
    console.error('[context-monitor] Error:', error);
    messages.push(`❌ 清理失败：${error.message}`);
  }
};

/**
 * 压缩记忆内容（简单版）
 * TODO: 替换为真实的向量化压缩（调用 ollama 或其他模型）
 */
async function compressMemory(rawContent: string): Promise<string> {
  // 简单版：提取关键信息
  // 真实场景应该调用：memory-compression-system 或 ollama chat
  
  const lines = rawContent.split('\n');
  const importantLines = lines.filter(line => 
    line.includes('##') ||           // 标题
    line.includes('**') ||           // 加粗
    line.includes('- **') ||         // 列表项
    line.includes('下一步') ||        // 待办
    line.includes('TODO') ||         // TODO
    line.length > 50                 // 长句（可能重要）
  );
  
  return importantLines.join('\n');
}

export default handler;
