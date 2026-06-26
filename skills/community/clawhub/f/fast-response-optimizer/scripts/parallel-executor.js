#!/usr/bin/env node
/**
 * 并行工具执行器
 * 并行执行独立的工具调用
 */

/**
 * 并行执行多个工具
 * @param {Array} tasks - 任务数组 [{name, fn}, ...]
 * @returns {Promise<Object>} - 结果对象 {name: result}
 */
async function parallelExecute(tasks) {
  console.log(`🚀 并行执行 ${tasks.length} 个任务...\n`);
  
  const startTime = Date.now();
  
  // 创建并行任务
  const promises = tasks.map(async ({ name, fn }) => {
    try {
      const taskStart = Date.now();
      const result = await fn();
      const duration = Date.now() - taskStart;
      console.log(`✅ ${name} 完成 (${duration}ms)`);
      return { name, result, duration, success: true };
    } catch (error) {
      console.error(`❌ ${name} 失败:`, error.message);
      return { name, error: error.message, success: false };
    }
  });
  
  // 等待所有任务完成
  const results = await Promise.all(promises);
  
  const totalDuration = Date.now() - startTime;
  console.log(`\n⏱️ 总耗时: ${totalDuration}ms`);
  
  // 整理结果
  const output = {};
  results.forEach(({ name, result, error, success }) => {
    output[name] = success ? result : { error, success: false };
  });
  
  return output;
}

/**
 * 带超时的并行执行
 */
async function parallelExecuteWithTimeout(tasks, timeoutMs = 10000) {
  const timeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error('并行执行超时')), timeoutMs);
  });
  
  return Promise.race([
    parallelExecute(tasks),
    timeoutPromise
  ]);
}

/**
 * 批量文件读取（并行）
 */
async function parallelReadFiles(files) {
  const fs = require('fs').promises;
  
  const tasks = files.map(file => ({
    name: file,
    fn: async () => {
      try {
        const content = await fs.readFile(file, 'utf-8');
        return { content, size: content.length };
      } catch (e) {
        return { error: e.message };
      }
    }
  }));
  
  return parallelExecute(tasks);
}

/**
 * 批量命令执行（并行）
 */
async function parallelExecCommands(commands) {
  const { exec } = require('child_process');
  const util = require('util');
  const execPromise = util.promisify(exec);
  
  const tasks = commands.map(cmd => ({
    name: cmd,
    fn: async () => {
      try {
        const { stdout, stderr } = await execPromise(cmd, { timeout: 30000 });
        return { stdout, stderr };
      } catch (e) {
        return { error: e.message, code: e.code };
      }
    }
  }));
  
  return parallelExecute(tasks);
}

// 导出
module.exports = {
  parallelExecute,
  parallelExecuteWithTimeout,
  parallelReadFiles,
  parallelExecCommands
};

// CLI 测试
if (require.main === module) {
  const fs = require('fs');
  const path = require('path');
  
  // 测试并行读取文件
  const workspace = process.env.OPENCLAW_WORKSPACE || process.cwd();
  const testFiles = [
    path.join(workspace, 'SOUL.md'),
    path.join(workspace, 'USER.md'),
    path.join(workspace, 'MEMORY.md')
  ].filter(f => fs.existsSync(f));
  
  if (testFiles.length > 0) {
    console.log('🧪 测试并行文件读取...\n');
    parallelReadFiles(testFiles).then(results => {
      console.log('\n📊 结果:');
      Object.entries(results).forEach(([file, result]) => {
        if (result.content) {
          console.log(`   ${path.basename(file)}: ${result.size} 字符`);
        } else {
          console.log(`   ${path.basename(file)}: ❌ ${result.error}`);
        }
      });
    });
  } else {
    console.log('⚠️ 测试文件不存在');
  }
}
