/**
 * Memory Get - 读取记忆文件
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
  // 相对路径基于 memoryDir
  if (!path.isAbsolute(p)) {
    return path.join(baseDir, p);
  }
  return path.resolve(p);
}

/**
 * 读取记忆文件
 */
export async function memoryGet(
  filePath: string,
  from?: number,
  lines?: number,
  config?: MemorySystemConfig
): Promise<{ path: string; content: string; totalLines: number }> {
  const cfg = config || {
    memoryDir: '~/.openclaw/workspace/memory'
  } as MemorySystemConfig;

  const fullPath = expandPath(filePath, cfg.memoryDir);
  
  console.log(`[MemoryGet] 读取: ${fullPath}`);

  try {
    const content = await fs.readFile(fullPath, 'utf-8');
    const allLines = content.split('\n');
    const totalLines = allLines.length;

    // 默认读取全部
    let startLine = 1;
    let endLine = totalLines;

    // 如果指定了 from，从该行开始读取
    if (from !== undefined && from > 0) {
      startLine = from;
    }

    // 如果指定了 lines，读取指定行数
    if (lines !== undefined && lines > 0) {
      endLine = Math.min(startLine + lines - 1, totalLines);
    }

    // 提取指定行
    const selectedLines = allLines.slice(startLine - 1, endLine);
    const selectedContent = selectedLines.join('\n');

    return {
      path: filePath,
      content: selectedContent,
      totalLines
    };
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === 'ENOENT') {
      return {
        path: filePath,
        content: '',
        totalLines: 0
      };
    }
    throw e;
  }
}

/**
 * 读取多个文件（用于自动加载）
 */
export async function memoryGetMultiple(
  filePaths: string[],
  config?: MemorySystemConfig
): Promise<{ path: string; content: string }[]> {
  const results: { path: string; content: string }[] = [];

  for (const fp of filePaths) {
    try {
      const result = await memoryGet(fp, undefined, undefined, config);
      if (result.content) {
        results.push({
          path: result.path,
          content: result.content
        });
      }
    } catch (e) {
      // 忽略不存在的文件
    }
  }

  return results;
}
