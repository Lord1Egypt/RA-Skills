/**
 * Embed - Ollama 向量嵌入封装
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * 检查 Ollama 是否运行
 */
export async function checkOllama(): Promise<boolean> {
  try {
    const { stdout } = await execAsync('ollama list', { timeout: 5000 });
    return stdout.includes('nomic-embed-text') || stdout.includes('embedding');
  } catch {
    return false;
  }
}

/**
 * 调用 Ollama 生成向量嵌入
 */
export async function embedText(
  text: string,
  model: string = 'nomatic-embed-text'
): Promise<number[]> {
  // 清理文本
  const cleanText = text.replace(/\n+/g, ' ').trim();
  
  if (!cleanText) {
    return new Array(768).fill(0); // 返回零向量
  }

  try {
    // 调用 Ollama API
    const curlCmd = `curl -s http://localhost:11434/api/embeddings -d '{"model": "${model}", "prompt": "${cleanText.replace(/"/g, '\\"')}"}'`;
    
    const { stdout } = await execAsync(curlCmd, { timeout: 30000 });
    const response = JSON.parse(stdout);
    
    if (response.embedding && Array.isArray(response.embedding)) {
      return response.embedding;
    }
    
    throw new Error('Invalid embedding response');
  } catch (e) {
    console.error('[Embed] 向量生成失败:', e);
    // 返回随机向量作为降级
    return generateFallbackEmbedding(text);
  }
}

/**
 * 生成降级向量（当 Ollama 不可用时）
 */
function generateFallbackEmbedding(text: string): number[] {
  // 简单的基于文本的伪随机向量
  const seed = hashString(text);
  const vector: number[] = [];
  
  for (let i = 0; i < 768; i++) {
    // 使用简单的线性同余生成器
    const next = (seed * 1103515245 + 12345) & 0x7fffffff;
    vector.push((next % 1000) / 1000 - 0.5);
  }
  
  // 归一化
  const norm = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0));
  return vector.map(v => v / norm);
}

/**
 * 字符串哈希函数
 */
function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

/**
 * 批量嵌入
 */
export async function embedTexts(
  texts: string[],
  model: string = 'nomic-embed-text'
): Promise<number[][]> {
  return Promise.all(texts.map(text => embedText(text, model)));
}

/**
 * 计算余弦相似度
 */
export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
