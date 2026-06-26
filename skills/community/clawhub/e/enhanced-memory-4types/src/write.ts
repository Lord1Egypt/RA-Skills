/**
 * Memory Write - 写入记忆文件
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { MemorySystemConfig } from './index.js';

/**
 * 展开路径中的 ~
 */
function expandPath(p: string, baseDir: string): string {
  if (p.startsWith('~')) {
    return path.join(process.env.HOME || '', p.slice(1));
  }
  if (!path.isAbsolute(p)) {
    return path.join(baseDir, p);
  }
  return path.resolve(p);
}

/**
 * 写入记忆文件
 */
export async function memoryWrite(
  filePath: string,
  content: string,
  mode: 'overwrite' | 'append' = 'append',
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  const cfg = config || {
    memoryDir: '~/.openclaw/workspace/memory'
  } as MemorySystemConfig;

  const fullPath = expandPath(filePath, cfg.memoryDir);
  
  console.log(`[MemoryWrite] 写入: ${fullPath} (mode: ${mode})`);

  // 确保目录存在
  const dir = path.dirname(fullPath);
  await fs.mkdir(dir, { recursive: true });

  if (mode === 'append') {
    // 追加模式
    try {
      const existing = await fs.readFile(fullPath, 'utf-8');
      const newContent = existing + '\n' + content;
      await fs.writeFile(fullPath, newContent, 'utf-8');
    } catch (e) {
      if ((e as NodeJS.ErrnoException).code === 'ENOENT') {
        // 文件不存在，直接创建
        await fs.writeFile(fullPath, content, 'utf-8');
      } else {
        throw e;
      }
    }
  } else {
    // 覆盖模式
    await fs.writeFile(fullPath, content, 'utf-8');
  }

  return {
    success: true,
    path: filePath
  };
}

/**
 * 便捷方法：写入每日记录
 */
export async function memoryWriteDaily(
  content: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  const today = new Date().toISOString().split('T')[0];
  return memoryWrite(`memory/${today}.md`, content, 'append', config);
}

/**
 * 便捷方法：写入长期记忆
 */
export async function memoryWritePermanent(
  content: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  return memoryWrite('MEMORY.md', content, 'append', config);
}
