#!/usr/bin/env node
/**
 * FunASR ASR - OpenClaw Skill Integration
 * 本地语音识别，使用阿里达摩院 FunASR
 * 优化版本：支持小内存模式
 */

const { exec } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');

module.exports = {
  name: 'funasr-asr',
  description: 'FunASR 本地语音识别 - 内存优化版 v2（单进程分段，SenseVoiceSmall 默认）',

  // 加载配置
  async loadConfig() {
    try {
      const configPath = path.join(__dirname, 'config.yaml');
      const configContent = await fs.readFile(configPath, 'utf8');
      return yaml.load(configContent);
    } catch (error) {
      // 默认配置（小内存模式）
      return {
        model: {
          mode: 'small'
        }
      };
    }
  },

  // 检查是否已安装
  async checkInstalled() {
    try {
      await exec('python3 -c "import funasr"');
      return true;
    } catch {
      return false;
    }
  },

  // 转录音频文件
  async transcribe(audioPath, options = {}) {
    const {
      format = 'text',
      mode = null,  // null = 使用配置文件默认值
      verbose = false,
      noWait = false
    } = options;

    // 检查文件是否存在
    try {
      await fs.access(audioPath);
    } catch {
      throw new Error(`音频文件不存在: ${audioPath}`);
    }

    // 加载配置
    const config = await this.loadConfig();
    const modelMode = mode || config.model?.mode || 'small';
    const segmentSeconds = options.segmentSeconds || 600;

    return new Promise((resolve, reject) => {
      const scriptPath = path.join(__dirname, 'scripts', 'transcribe.py');

      // 构建命令
      let cmd = `python3 ${scriptPath} "${audioPath}"`;
      cmd += ` --mode ${modelMode}`;
      cmd += ` --format ${format}`;
      cmd += ` --segment ${segmentSeconds}`;

      if (verbose) cmd += ' --verbose';
      if (noWait) cmd += ' --no-wait';

      console.log(`[FunASR] 模式: ${modelMode}, 分段: ${segmentSeconds}s, 内存: ${modelMode === 'small' ? '~500MB' : '~2GB'}`);

      exec(cmd, { maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
        if (error) {
          // 检查是否是内存不足错误
          if (stderr.includes('内存不足')) {
            reject(new Error(`内存不足: ${stderr.trim()}`));
          } else {
            reject(new Error(`FunASR 转录失败: ${error.message}`));
          }
          return;
        }

        try {
          if (format === 'json') {
            resolve(JSON.parse(stdout));
          } else {
            // 提取纯文本（过滤掉进度信息）
            const lines = stdout.split('\n');
            const textLines = lines.filter(line => {
              // 过滤掉进度条和控制字符
              return !line.includes('[34m') &&
                     !line.includes('[31m') &&
                     !line.includes('rtf_avg') &&
                     !line.includes('load_data') &&
                     !line.includes('batch_size') &&
                     !line.trim().match(/^[0-9%|]+$/);
            });

            // 提取转录结果（在分隔线之间）
            const separator = '='.repeat(60);
            const startIdx = textLines.findIndex(line => line.includes(separator));
            const endIdx = textLines.lastIndexOf(separator);

            if (startIdx >= 0 && endIdx > startIdx) {
              const result = textLines.slice(startIdx + 1, endIdx).join('\n').trim();
              resolve(result);
            } else {
              // 没有找到分隔线，返回过滤后的内容
              resolve(textLines.join('\n').trim());
            }
          }
        } catch (e) {
          resolve(stdout.trim());
        }
      });
    });
  },

  // OpenClaw 工具接口
  tools: [
    {
      name: 'transcribe_audio',
      description: '使用 FunASR 转录音频文件为文字（小内存模式）',
      inputSchema: {
        type: 'object',
        properties: {
          audioPath: {
            type: 'string',
            description: '音频文件路径'
          },
          format: {
            type: 'string',
            enum: ['text', 'json'],
            description: '输出格式',
            default: 'text'
          },
          mode: {
            type: 'string',
            enum: ['small', 'large'],
            description: '模型模式: small(500MB) / large(2GB)，默认使用 small',
            default: 'small'
          },
          verbose: {
            type: 'boolean',
            description: '显示详细信息（内存使用等）',
            default: false
          }
        },
        required: ['audioPath']
      },
      handler: async (params) => {
        return await this.transcribe(params.audioPath, {
          format: params.format || 'text',
          mode: params.mode || 'small',
          verbose: params.verbose || false
        });
      }
    }
  ]
};
