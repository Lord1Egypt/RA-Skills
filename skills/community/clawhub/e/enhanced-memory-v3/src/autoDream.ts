/**
 * AutoDream - 定时记忆整合系统
 * 
 * 灵感来自 Claude Code 的 autoDream 系统
 * 在空闲时自动整合记忆，保持记忆新鲜和结构化
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { MemorySystemConfig } from './index.js';

/**
 * MiniMax API 调用
 */
async function callMiniMax(prompt: string, apiKey: string): Promise<string> {
  const response = await fetch('https://api.minimaxi.com/anthropic/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'MiniMax-M2.7',
      max_tokens: 8192,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ]
    })
  });

  if (!response.ok) {
    throw new Error(`MiniMax API error: ${response.status}`);
  }

  const data = await response.json() as { content?: Array<{ type: string; text?: string }> };
  
  // 解析响应
  const textContent = data.content?.find(c => c.type === 'text')?.text;
  return textContent || '';
}

/**
 * AutoDream 配置
 */
export interface AutoDreamConfig {
  enabled: boolean;
  minHours: number;        // 最小触发间隔（小时）
  minSessions: number;      // 最小会话数
  memoryDir: string;
}

const DEFAULT_AUTO_DREAM_CONFIG: AutoDreamConfig = {
  enabled: true,
  minHours: 24,            // 默认 24 小时触发一次
  minSessions: 3,          // 默认 3 个新会话
  memoryDir: '~/.openclaw/workspace/memory'
};

/**
 * 整合状态文件
 */
const STATE_FILE = '.auto-dream-state.json';

interface DreamState {
  lastConsolidatedAt: number;  // 上次整合时间戳
  lastConsolidatedSessions: number;  // 上次整合时的会话数
}

/**
 * 整合结果
 */
interface DreamResult {
  added: string[];      // 新增的文件
  deleted: string[];    // 删除的文件
  updated: string[];    // 更新的文件
  summary: string;      // 总结
}

/**
 * 读取整合状态
 */
async function readDreamState(memoryDir: string): Promise<DreamState> {
  const statePath = path.join(expandPath(memoryDir), STATE_FILE);
  
  try {
    const content = await fs.readFile(statePath, 'utf-8');
    return JSON.parse(content);
  } catch {
    return {
      lastConsolidatedAt: 0,
      lastConsolidatedSessions: 0
    };
  }
}

/**
 * 写入整合状态
 */
async function writeDreamState(memoryDir: string, state: DreamState): Promise<void> {
  const statePath = path.join(expandPath(memoryDir), STATE_FILE);
  await fs.writeFile(statePath, JSON.stringify(state, null, 2));
}

/**
 * 展开路径
 */
function expandPath(p: string): string {
  if (p.startsWith('~')) {
    return path.join(process.env.HOME || '', p.slice(1));
  }
  return path.resolve(p);
}

/**
 * 扫描会话目录
 */
async function scanSessions(memoryDir: string): Promise<string[]> {
  const sessionsDir = path.join(expandPath(memoryDir), 'sessions');
  
  try {
    const entries = await fs.readdir(sessionsDir, { withFileTypes: true });
    return entries
      .filter(e => e.isFile() && e.name.endsWith('.json'))
      .map(e => path.join(sessionsDir, e.name));
  } catch {
    return [];
  }
}

/**
 * 读取 MEMORY.md 索引
 */
async function readMemoryIndex(memoryDir: string): Promise<string> {
  const indexPath = path.join(expandPath(memoryDir), 'MEMORY.md');
  
  try {
    return await fs.readFile(indexPath, 'utf-8');
  } catch {
    return '';
  }
}

/**
 * 扫描所有记忆文件
 */
async function scanMemoryFiles(memoryDir: string): Promise<{ path: string; content: string; modified: Date }[]> {
  const files: { path: string; content: string; modified: Date }[] = [];
  const baseDir = expandPath(memoryDir);
  
  async function scan(dir: string) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'sessions') {
          await scan(fullPath);
        } else if (entry.name.endsWith('.md')) {
          const stat = await fs.stat(fullPath);
          const content = await fs.readFile(fullPath, 'utf-8');
          files.push({ path: fullPath, content, modified: stat.mtime });
        }
      }
    } catch {
      // 忽略错误
    }
  }
  
  await scan(baseDir);
  return files;
}

/**
 * 获取最近修改的文件
 */
async function getRecentlyModifiedFiles(
  memoryDir: string, 
  since: number
): Promise<{ path: string; content: string; relativePath: string }[]> {
  const files: { path: string; content: string; relativePath: string }[] = [];
  const baseDir = expandPath(memoryDir);
  
  async function scan(dir: string) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'sessions') {
          await scan(fullPath);
        } else if (entry.name.endsWith('.md')) {
          const stat = await fs.stat(fullPath);
          // 只取自上次整合以来修改的文件
          if (stat.mtimeMs > since) {
            const content = await fs.readFile(fullPath, 'utf-8');
            const relativePath = fullPath.replace(baseDir + '/', '');
            files.push({ path: fullPath, content, relativePath });
          }
        }
      }
    } catch {
      // 忽略错误
    }
  }
  
  await scan(baseDir);
  return files;
}

/**
 * 解析 LLM 返回的整合结果
 */
function parseDreamResult(llmOutput: string): DreamResult {
  const result: DreamResult = {
    added: [],
    deleted: [],
    updated: [],
    summary: ''
  };

  // 提取新增记忆
  const addedMatch = llmOutput.match(/###\s*新增记忆[\s\S]*?(?=###|---|\*\*总结\*\*)/gi);
  if (addedMatch) {
    for (const block of addedMatch) {
      const fileMatch = block.match(/\[\[([^\]]+)\]\]|\[([^\]]+)\]/);
      if (fileMatch) {
        result.added.push(fileMatch[1] || fileMatch[2]);
      }
    }
  }

  // 提取删除记忆
  const deletedMatch = llmOutput.match(/###\s*删除记忆[\s\S]*?(?=###|---|\*\*总结\*\*)/gi);
  if (deletedMatch) {
    for (const block of deletedMatch) {
      const lines = block.split('\n').filter(l => l.startsWith('-'));
      for (const line of lines) {
        const fileMatch = line.match(/\[([^\]]+)\]/);
        if (fileMatch) {
          result.deleted.push(fileMatch[1]);
        }
      }
    }
  }

  // 提取更新
  const updatedMatch = llmOutput.match(/###\s*索引更新[\s\S]*?(?=###|\*\*总结\*\*|$)/gi);
  if (updatedMatch) {
    result.updated.push('MEMORY.md');
  }

  // 提取总结
  const summaryMatch = llmOutput.match(/\*\*总结\*\*[:：]?\s*([\s\S]+)$/i);
  if (summaryMatch) {
    result.summary = summaryMatch[1].trim();
  } else {
    // 取最后一段非代码块的内容
    const parts = llmOutput.split(/```/);
    if (parts.length >= 3) {
      result.summary = parts[parts.length - 1].trim();
    } else {
      result.summary = llmOutput.slice(-500).trim();
    }
  }

  return result;
}

/**
 * 检查是否应该触发整合
 */
export async function shouldTriggerDream(config: AutoDreamConfig): Promise<{ should: boolean; reason: string }> {
  if (!config.enabled) {
    return { should: false, reason: 'AutoDream 已禁用' };
  }
  
  const state = await readDreamState(config.memoryDir);
  const now = Date.now();
  
  // 检查时间间隔
  const hoursSince = (now - state.lastConsolidatedAt) / (1000 * 60 * 60);
  if (hoursSince < config.minHours) {
    return { 
      should: false, 
      reason: `距离上次整合 ${hoursSince.toFixed(1)} 小时，需等待 ${config.minHours} 小时` 
    };
  }
  
  // 检查新会话数
  const sessions = await scanSessions(config.memoryDir);
  const sessionsSinceLast = sessions.length - state.lastConsolidatedSessions;
  
  if (sessionsSinceLast < config.minSessions) {
    return { 
      should: false, 
      reason: `新会话 ${sessionsSinceLast} 个，需 ${config.minSessions} 个才触发` 
    };
  }
  
  return { 
    should: true, 
    reason: `时间 ${hoursSince.toFixed(1)}h OK，会话 ${sessionsSinceLast} 个 OK` 
  };
}

/**
 * 生成整合 Prompt
 */
function buildDreamPrompt(
  indexContent: string, 
  recentFiles: { relativePath: string; content: string }[],
  oldFiles: { relativePath: string; content: string }[],
  stats: { totalFiles: number; recentCount: number; oldCount: number }
): string {
  const recentFilesSection = recentFiles
    .map(f => `## ${f.relativePath}\n${f.content.slice(0, 2000)}`)
    .join('\n\n');

  const oldFilesSection = oldFiles.length > 0
    ? oldFiles
        .map(f => `## ${f.relativePath} (建议检查是否过时)\n${f.content.slice(0, 1000)}`)
        .join('\n\n')
    : '(无早期文件)';

  return `# Dream: 记忆整合

你是记忆整合专家。你的任务是对记忆文件进行系统性整理，让记忆保持新鲜、结构化、易于查找。

## 当前统计
- 总记忆文件: ${stats.totalFiles} 个
- 新增/修改文件: ${stats.recentCount} 个
- 早期文件: ${stats.oldCount} 个

---

## 当前索引 (MEMORY.md)
${indexContent || '(空)'}

---

## 最近新增/修改的记忆文件
${recentFilesSection}

---

## 早期记忆文件（请检查是否过时）
${oldFilesSection}

---

## 整合原则

### 1. 四类记忆分类
记忆分为四种类型，每种有明确的保存时机：

- **user** (私密): 用户角色、偏好，知识背景
- **feedback** (negative/positive): 用户的纠正和确认
- **project** (团队): 项目进展、目标、决策
- **reference** (团队): 外部系统资源指针

### 2. Feedback 双向记录格式
\`\`\`markdown
### [规则名称]
**Type:** negative | positive
**Why:** [用户给出的原因]
**How to apply:** [何时应用]
**Date:** ${new Date().toISOString().split('T')[0]}
\`\`\`

### 3. 日期规范
- 使用绝对日期："上周" → "2026-03-31"
- 包含 Why：记录原因比记录规则更有价值
- 保持简洁：索引每条 <= 150 字符

---

## 整合任务

请执行以下任务：

### 1. 分析最近的文件
- 识别哪些是新文件需要添加到索引
- 识别哪些是过时内容需要删除
- 识别哪些是重复内容需要合并

### 2. 更新索引
保持 MEMORY.md 索引：
- 每条 <= 150 字符
- 使用绝对日期
- 按 user / feedback / project / reference 分类

### 3. 标记过时内容
如果发现以下情况，请标记删除：
- 内容已被新信息覆盖
- 与当前事实矛盾
- 过于笼统无实际价值

---

## 输出格式

请按以下格式返回：

### 新增记忆
(列出需要新增的文件和内容)

### 删除记忆
(列出需要删除的文件和原因)

### 索引更新
\`\`\`markdown
(更新后的 MEMORY.md 内容)
\`\`\`

### 总结
(简述本次整合做了什么，50字以内)

---

请开始整合。`;
}

/**
 * 执行整合（包含 LLM 调用）
 */
export async function executeDream(
  config?: Partial<AutoDreamConfig>,
  apiKey?: string
): Promise<{
  success: boolean;
  triggered: boolean;
  summary: string;
  changes: DreamResult;
  reason?: string;
}> {
  const cfg: AutoDreamConfig = {
    ...DEFAULT_AUTO_DREAM_CONFIG,
    ...config
  };
  
  const memoryDir = expandPath(cfg.memoryDir);
  const resolvedApiKey = apiKey || process.env.MINIMAX_CODING_API_KEY;
  
  console.log('[AutoDream] 开始执行记忆整合...');
  
  try {
    // 1. 读取当前状态
    const state = await readDreamState(memoryDir);
    const indexContent = await readMemoryIndex(memoryDir);
    const allFiles = await scanMemoryFiles(memoryDir);
    const sessions = await scanSessions(memoryDir);
    
    // 2. 获取最近修改的文件（上次整合以来）
    const recentFiles = await getRecentlyModifiedFiles(memoryDir, state.lastConsolidatedAt);
    const oldFiles = allFiles
      .filter(f => !recentFiles.some(r => r.path === f.path))
      .map(f => ({ relativePath: f.path.replace(expandPath(memoryDir) + '/', ''), content: f.content }));
    
    console.log(`[AutoDream] 总文件: ${allFiles.length}, 新文件: ${recentFiles.length}, 旧文件: ${oldFiles.length}`);
    
    // 3. 检查是否真的需要整合
    if (recentFiles.length === 0 && allFiles.length > 0) {
      // 没有新文件，但有旧文件，检查是否需要更新索引
      if (indexContent.length < 100) {
        // 索引几乎是空的，需要生成
        console.log('[AutoDream] 索引为空，生成初始索引...');
      } else {
        return {
          success: true,
          triggered: false,
          summary: '没有新增文件，跳过整合',
          changes: { added: [], deleted: [], updated: [], summary: '无变化' }
        };
      }
    }
    
    // 4. 生成整合 Prompt
    const prompt = buildDreamPrompt(
      indexContent,
      recentFiles,
      oldFiles,
      {
        totalFiles: allFiles.length,
        recentCount: recentFiles.length,
        oldCount: oldFiles.length
      }
    );
    
    // 5. 调用 LLM
    if (!resolvedApiKey) {
      console.warn('[AutoDream] 未提供 API Key，返回 prompt 用于调试');
      return {
        success: true,
        triggered: true,
        summary: 'API Key 未配置，跳过实际整合',
        changes: { added: [], deleted: [], updated: [], summary: '未执行' },
        reason: 'missing_api_key'
      };
    }
    
    console.log('[AutoDream] 调用 MiniMax LLM...');
    const llmOutput = await callMiniMax(prompt, resolvedApiKey);
    console.log(`[AutoDream] LLM 返回 ${llmOutput.length} 字符`);
    
    // 6. 解析结果
    const changes = parseDreamResult(llmOutput);
    
    // 7. 应用更改 - 新增文件
    for (const filePath of changes.added) {
      try {
        const fullPath = path.join(memoryDir, filePath);
        await fs.mkdir(path.dirname(fullPath), { recursive: true });
        // 从 LLM 输出中提取内容（简化处理）
        await fs.writeFile(fullPath, `# ${filePath}\n\n${new Date().toISOString().split('T')[0]} 创建\n`);
        console.log(`[AutoDream] 创建文件: ${filePath}`);
      } catch (e) {
        console.error(`[AutoDream] 创建文件失败: ${filePath}`, e);
      }
    }
    
    // 8. 应用更改 - 删除文件
    for (const filePath of changes.deleted) {
      try {
        const fullPath = path.join(memoryDir, filePath);
        await fs.unlink(fullPath);
        console.log(`[AutoDream] 删除文件: ${filePath}`);
      } catch (e) {
        console.error(`[AutoDream] 删除文件失败: ${filePath}`, e);
      }
    }
    
    // 9. 更新索引
    if (changes.updated.includes('MEMORY.md')) {
      const indexMatch = llmOutput.match(/```markdown\n([\s\S]*?)```/);
      if (indexMatch) {
        await fs.writeFile(path.join(memoryDir, 'MEMORY.md'), indexMatch[1]);
        console.log('[AutoDream] 更新 MEMORY.md');
      }
    }
    
    // 10. 更新状态
    const newState: DreamState = {
      lastConsolidatedAt: Date.now(),
      lastConsolidatedSessions: sessions.length
    };
    await writeDreamState(memoryDir, newState);
    
    console.log('[AutoDream] 整合完成');
    
    return {
      success: true,
      triggered: true,
      summary: changes.summary || '整合完成',
      changes
    };
    
  } catch (e) {
    console.error('[AutoDream] 执行失败:', e);
    return {
      success: false,
      triggered: false,
      summary: `整合失败: ${e}`,
      changes: { added: [], deleted: [], updated: [], summary: `失败: ${e}` }
    };
  }
}

/**
 * 获取最近整合的时间
 */
export async function getLastDreamTime(memoryDir: string): Promise<Date | null> {
  const state = await readDreamState(memoryDir);
  return state.lastConsolidatedAt > 0 ? new Date(state.lastConsolidatedAt) : null;
}

/**
 * 获取整合统计
 */
export async function getDreamStats(memoryDir: string): Promise<{
  lastDream: Date | null;
  hoursSince: number;
  sessionsSinceLast: number;
  totalMemoryFiles: number;
}> {
  const state = await readDreamState(memoryDir);
  const memoryFiles = await scanMemoryFiles(memoryDir);
  const sessions = await scanSessions(memoryDir);
  
  const lastDream = state.lastConsolidatedAt > 0 ? new Date(state.lastConsolidatedAt) : null;
  const hoursSince = lastDream 
    ? (Date.now() - state.lastConsolidatedAt) / (1000 * 60 * 60)
    : Infinity;
  
  return {
    lastDream,
    hoursSince,
    sessionsSinceLast: sessions.length - state.lastConsolidatedSessions,
    totalMemoryFiles: memoryFiles.length
  };
}
