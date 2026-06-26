/**
 * CodeBuddy CLI Wrapper
 * 封装 CodeBuddy CLI 的调用和输出解析
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class CodeBuddyCLIWrapper {
  constructor(options = {}) {
    this.codebuddyPath = options.codebuddyPath || 'codebuddy';
    this.debug = options.debug || false;
    this.outputFormat = options.outputFormat || 'json';
    this.permissionMode = options.permissionMode || 'bypassPermissions';
  }

  /**
   * 检查 CodeBuddy CLI 是否可用
   */
  async checkAvailable() {
    return new Promise((resolve) => {
      const proc = spawn(this.codebuddyPath, ['--version'], {
        shell: true,
        stdio: 'pipe'
      });

      let output = '';
      proc.stdout.on('data', (data) => {
        output += data.toString();
      });

      proc.on('close', (code) => {
        if (code === 0) {
          const version = output.trim();
          resolve({
            available: true,
            version: version
          });
        } else {
          resolve({
            available: false,
            error: 'CodeBuddy CLI not found'
          });
        }
      });

      proc.on('error', () => {
        resolve({
          available: false,
          error: 'CodeBuddy CLI not found'
        });
      });
    });
  }

  /**
   * 执行编程任务
   */
  async execute(task, options = {}) {
    const startTime = Date.now();
    
    // 构建命令参数
    const args = [
      '-p', task.prompt || task.task || task,
      '--output-format', options.outputFormat || this.outputFormat,
      '--permission-mode', options.permissionMode || this.permissionMode
    ];

    // CodeBuddy CLI 不支持 --workspace 参数
    // 使用 cwd 选项来设置工作目录（在 spawn 时指定）

    if (this.debug) {
      console.log('[CodeBuddy CLI] Executing:', this.codebuddyPath, args.join(' '));
      console.log('[CodeBuddy CLI] Working Directory:', options.cwd || process.cwd());
    }

    return new Promise((resolve, reject) => {
      const proc = spawn(this.codebuddyPath, args, {
        shell: true,
        cwd: options.cwd || process.cwd(),
        stdio: 'pipe'
      });

      const result = {
        status: 'running',
        toolCalls: [],
        filesModified: [],
        reasoning: [],
        rawOutput: [],
        duration: 0
      };

      let stdoutBuffer = '';
      let stderrBuffer = '';

      // 解析 JSON 流输出
      proc.stdout.on('data', (data) => {
        const chunk = data.toString();
        stdoutBuffer += chunk;
        result.rawOutput.push(chunk);

        // 尝试解析 JSON 行
        const lines = chunk.split('\n');
        for (const line of lines) {
          if (line.trim()) {
            try {
              const json = JSON.parse(line);
              this._parseOutput(json, result, options.onProgress);
            } catch (e) {
              // 不是 JSON，可能是普通文本
              if (this.debug) {
                console.log('[CodeBuddy CLI] Non-JSON output:', line);
              }
            }
          }
        }
      });

      // 捕获错误输出
      proc.stderr.on('data', (data) => {
        stderrBuffer += data.toString();
      });

      // 进程结束
      proc.on('close', (code) => {
        result.duration = (Date.now() - startTime) / 1000;

        if (code === 0) {
          result.status = 'success';
          resolve(result);
        } else {
          result.status = 'failed';
          result.error = stderrBuffer || 'Unknown error';
          reject({
            type: 'CLI_ERROR',
            message: stderrBuffer,
            result: result
          });
        }
      });

      // 进程错误
      proc.on('error', (error) => {
        result.status = 'failed';
        result.duration = (Date.now() - startTime) / 1000;
        
        reject({
          type: 'CLI_NOT_FOUND',
          message: 'CodeBuddy CLI not found. Please install it first.',
          error: error.message
        });
      });
    });
  }

  /**
   * 解析 JSON 输出
   */
  _parseOutput(json, result, onProgress) {
    // 解析工具调用
    if (json.tool_calls) {
      result.toolCalls.push(...json.tool_calls);
    }

    // 解析修改的文件
    if (json.files_modified) {
      const newFiles = json.files_modified.filter(f => !result.filesModified.includes(f));
      result.filesModified.push(...newFiles);
    }

    // 解析推理过程
    if (json.reasoning) {
      result.reasoning.push(...json.reasoning);
    }

    // 解析进度信息
    if (json.progress && onProgress) {
      onProgress({
        percentage: json.progress.percentage || 0,
        currentTask: json.progress.current_task || '处理中',
        elapsedTime: json.progress.elapsed_time || 0,
        estimatedTime: json.progress.estimated_time,
        filesModified: result.filesModified,
        toolCalls: result.toolCalls.length
      });
    }

    // 更新状态
    if (json.status) {
      result.status = json.status;
    }
  }

  /**
   * 执行后台任务（不等待完成）
   */
  executeBackground(task, options = {}) {
    const args = [
      '-p', task.prompt || task,
      '--output-format', options.outputFormat || this.outputFormat,
      '--permission-mode', options.permissionMode || this.permissionMode
    ];

    if (this.debug) {
      console.log('[CodeBuddy CLI] Background task:', this.codebuddyPath, args.join(' '));
    }

    const proc = spawn(this.codebuddyPath, args, {
      shell: true,
      cwd: options.cwd || process.cwd(),
      stdio: 'pipe',
      detached: true
    });

    return {
      pid: proc.pid,
      process: proc,
      stdout: proc.stdout,
      stderr: proc.stderr
    };
  }
}

module.exports = CodeBuddyCLIWrapper;
