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
 * 读取整合状态
 */
async function readDreamState(memoryDir: string): Promise<DreamState> {
  const statePath = path.join(expandPath(memoryDir), STATE_FILE);
  
  try {
    const content = await fs.readFile(statePath, 'utf-8');
    return JSON.parse(content);
  } catch {
    // 首次运行，返回默认值
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
function buildDreamPrompt(memoryDir: string, indexContent: string, memoryFiles: { path: string; content: string }[]): string {
  const memoryFilesList = memoryFiles
    .map(f => `- ${f.path.replace(expandPath(memoryDir), '')}`)
    .join('\n');
  
  return `# Dream: 记忆整合

你是记忆整合专家。你的任务是对记忆文件进行系统性整理，让记忆保持新鲜、结构化、易于查找。

## 记忆目录
${memoryDir}

## 当前索引 (MEMORY.md)
${indexContent || '(空)'}

## 现有记忆文件
${memoryFilesList || '(无)'}

---

## 整合原则

### 1. 四类记忆分类
记忆分为四种类型，每种有明确的保存时机：

- **user** (私密): 用户角色、偏好、知识背景
- **feedback** (私密/团队): 用户的纠正和确认（都要记录！）
- **project** (团队): 项目进展、目标、决策
- **reference** (团队): 外部系统资源指针

### 2. Feedback 双向记录
不仅要记录"不要做什么"，也要记录"什么做对了"：

\`\`\`markdown
### 不要mock数据库
**Type:** negative
**Why:** 上一季度mock测试通过了但生产迁移失败
**How to apply:** 集成测试必须用真实数据库

### 接受单PR而非多个小PR
**Type:** positive
**Why:** 拆分反而造成不必要的开销
**How to apply:** 重构类需求优先合并为大PR
\`\`\`

### 3. 日期规范
- 使用绝对日期："上周" → "2026-03-25"
- 包含 Why：记录原因比记录规则更有价值
- 保持简洁：索引每条 <= 150 字符

---

## 整合任务

请执行以下整合任务：

1. **读取现有记忆** - 查看重要记忆文件的内容
2. **识别过时信息** - 删除已被否定或过期的记忆
3. **更新索引** - 保持 MEMORY.md 索引在 200 行以内
4. **合并重复** - 将相似记忆合并，避免冗余

## 输出格式

请返回你的整合结果，格式如下：

### 新增记忆（如果有）
\`\`\`
### [文件名]
[内容]
\`\`\`

### 删除记忆（如果有）
- [要删除的文件和原因]

### 索引更新（如果有）
\`\`\`markdown
[更新后的索引内容]
\`\`\`

### 总结
[简述本次整合做了什么]

---

请开始整合。`;
}

/**
 * 执行整合
 */
export async function executeDream(
  config?: Partial<AutoDreamConfig>
): Promise<{
  success: boolean;
  summary: string;
  changes: {
    added: string[];
    deleted: string[];
    updated: string[];
  };
}> {
  const cfg: AutoDreamConfig = {
    ...DEFAULT_AUTO_DREAM_CONFIG,
    ...config
  };
  
  const memoryDir = expandPath(cfg.memoryDir);
  console.log('[AutoDream] 开始执行记忆整合...');
  
  try {
    // 1. 读取当前状态
    const indexContent = await readMemoryIndex(memoryDir);
    const memoryFiles = await scanMemoryFiles(memoryDir);
    const sessions = await scanSessions(memoryDir);
    
    console.log(`[AutoDream] 索引长度: ${indexContent.length}`);
    console.log(`[AutoDream] 记忆文件: ${memoryFiles.length} 个`);
    console.log(`[AutoDream] 会话文件: ${sessions.length} 个`);
    
    // 2. 生成整合 Prompt
    const prompt = buildDreamPrompt(memoryDir, indexContent, memoryFiles);
    
    // 3. 更新状态
    const state: DreamState = {
      lastConsolidatedAt: Date.now(),
      lastConsolidatedSessions: sessions.length
    };
    await writeDreamState(memoryDir, state);
    
    // 4. 返回结果（实际 LLM 调用由调用者执行）
    return {
      success: true,
      summary: `整合完成。扫描了 ${memoryFiles.length} 个记忆文件和 ${sessions.length} 个会话。`,
      changes: {
        added: [],
        deleted: [],
        updated: []
      },
      prompt  // 返回 prompt 供外部 LLM 调用
    };
    
  } catch (e) {
    console.error('[AutoDream] 执行失败:', e);
    return {
      success: false,
      summary: `整合失败: ${e}`,
      changes: {
        added: [],
        deleted: [],
        updated: []
      }
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
