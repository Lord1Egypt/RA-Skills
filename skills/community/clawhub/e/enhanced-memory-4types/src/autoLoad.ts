/**
 * Auto Load - 会话启动时自动加载记忆
 */

import * as path from 'path';
import * as fs from 'fs/promises';
import { memoryGet } from './get.js';
import type { MemorySystemConfig } from './index.js';

/**
 * 展开路径
 */
function expandPath(p: string, baseDir: string): string {
  if (p.startsWith('~')) {
    return path.join(process.env.HOME || '', p.slice(1));
  }
  return path.join(baseDir, p);
}

/**
 * 获取日期字符串
 */
function getDateString(daysAgo: number = 0): string {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  return date.toISOString().split('T')[0];
}

/**
 * 自动加载记忆
 */
export async function setupAutoLoad(
  context: {
    sessionType: 'direct' | 'group';
    groupId?: string;
    userId?: string;
  },
  config: MemorySystemConfig
): Promise<{ loaded: string[]; content: string }> {
  const memoryDir = expandPath(config.memoryDir, '');
  const filesToLoad: string[] = [];
  
  console.log(`[AutoLoad] 会话类型: ${context.sessionType}, 加载记忆...`);

  // 1. 加载长期记忆 MEMORY.md
  filesToLoad.push('MEMORY.md');

  // 2. 加载当日和昨日日记
  const today = getDateString(0);
  const yesterday = getDateString(1);
  filesToLoad.push(`memory/${today}.md`);
  filesToLoad.push(`memory/${yesterday}.md`);

  // 3. 如果是群组，加载群组记忆
  if (context.sessionType === 'group' && context.groupId) {
    filesToLoad.push(`memory/groups/${context.groupId}/MEMORY.md`);
  }

  // 读取所有文件
  const loaded: string[] = [];
  const contents: string[] = [];

  for (const fp of filesToLoad) {
    try {
      const result = await memoryGet(fp, undefined, undefined, config);
      if (result.content && result.content.trim()) {
        loaded.push(fp);
        contents.push(`\n--- ${fp} ---\n${result.content}`);
      }
    } catch (e) {
      // 文件不存在，跳过
    }
  }

  const combinedContent = contents.join('\n');
  
  console.log(`[AutoLoad] 已加载 ${loaded.length} 个记忆文件`);

  return {
    loaded,
    content: combinedContent
  };
}

/**
 * 便捷函数：加载指定群组的记忆
 */
export async function loadGroupMemory(
  groupId: string,
  config: MemorySystemConfig
): Promise<string> {
  const result = await setupAutoLoad(
    { sessionType: 'group', groupId },
    config
  );
  return result.content;
}

/**
 * 便捷函数：加载个人记忆
 */
export async function loadPersonalMemory(
  config: MemorySystemConfig
): Promise<string> {
  const result = await setupAutoLoad(
    { sessionType: 'direct' },
    config
  );
  return result.content;
}
