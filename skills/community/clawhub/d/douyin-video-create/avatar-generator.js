#!/usr/bin/env node

/**
 * Digital Avatar Video Generator
 * 
 * 支持多个数字人 API:
 * - HeyGen (https://www.heygen.com)
 * - D-ID (https://www.d-id.com)
 * - Synthesia (https://www.synthesia.io)
 * 
 * 用法:
 *   node avatar-generator.js --provider heygen --script script.json --output video.mp4
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

class AvatarVideoGenerator {
  constructor(options = {}) {
    this.provider = options.provider || 'heygen'; // heygen, d-id, synthesia
    this.apiKey = options.apiKey || process.env.AVATAR_API_KEY;
    this.baseUrl = this.getBaseUrl();
    this.config = options.config || {};
  }

  /**
   * 获取 API 基础 URL
   */
  getBaseUrl() {
    const urls = {
      'heygen': 'https://api.heygen.com/v1',
      'd-id': 'https://api.d-id.com',
      'synthesia': 'https://api.synthesia.io/v1'
    };
    return urls[this.provider] || urls['heygen'];
  }

  /**
   * 生成视频（HeyGen）
   */
  async generateWithHeyGen(script) {
    const payload = {
      video_inputs: [
        {
          character: {
            type: 'avatar',
            avatar_id: this.config.avatarId || 'Wayne_20220821',
            voice: {
              type: 'text_to_speech',
              input_text: this.extractText(script),
              voice_id: this.config.voiceId || 'en_us_001'
            }
          }
        }
      ],
      dimension: {
        width: 1080,
        height: 1920
      }
    };

    return this.makeRequest('/video_generate', 'POST', payload);
  }

  /**
   * 生成视频（D-ID）
   */
  async generateWithDID(script) {
    const payload = {
      source_url: this.config.sourceUrl || 'https://example.com/avatar.jpg',
      script: {
        type: 'text',
        input: this.extractText(script),
        provider: {
          type: 'microsoft',
          voice_id: this.config.voiceId || 'en-US-AriaNeural'
        }
      }
    };

    return this.makeRequest('/talks', 'POST', payload);
  }

  /**
   * 生成视频（Synthesia）
   */
  async generateWithSynthesia(script) {
    const payload = {
      test: false,
      title: script.title || 'Generated Video',
      avatar: {
        type: 'avatar',
        avatar_id: this.config.avatarId || 'avatar_1'
      },
      voice: {
        type: 'microsoft',
        voice_id: this.config.voiceId || 'en-US-AriaNeural'
      },
      scenes: script.scenes.map(scene => ({
        paragraphs: [
          {
            text: scene.text
          }
        ]
      }))
    };

    return this.makeRequest('/videos', 'POST', payload);
  }

  /**
   * 从脚本提取文本
   */
  extractText(script) {
    if (typeof script === 'string') {
      return script;
    }

    if (script.scenes && Array.isArray(script.scenes)) {
      return script.scenes.map(s => s.text).join('\n\n');
    }

    if (script.sections && Array.isArray(script.sections)) {
      return script.sections.map(s => s.text).join('\n\n');
    }

    return JSON.stringify(script);
  }

  /**
   * 发送 HTTP 请求
   */
  async makeRequest(endpoint, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.baseUrl + endpoint);
      
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        }
      };

      const req = https.request(url, options, (res) => {
        let responseData = '';

        res.on('data', chunk => {
          responseData += chunk;
        });

        res.on('end', () => {
          try {
            const parsed = JSON.parse(responseData);
            resolve({
              status: res.statusCode,
              data: parsed
            });
          } catch (e) {
            resolve({
              status: res.statusCode,
              data: responseData
            });
          }
        });
      });

      req.on('error', reject);

      if (data) {
        req.write(JSON.stringify(data));
      }

      req.end();
    });
  }

  /**
   * 生成视频
   */
  async generate(script) {
    if (!this.apiKey) {
      throw new Error(`未设置 ${this.provider.toUpperCase()} API Key`);
    }

    console.log(`📹 使用 ${this.provider} 生成视频...`);

    let result;
    switch (this.provider) {
      case 'heygen':
        result = await this.generateWithHeyGen(script);
        break;
      case 'd-id':
        result = await this.generateWithDID(script);
        break;
      case 'synthesia':
        result = await this.generateWithSynthesia(script);
        break;
      default:
        throw new Error(`不支持的提供商: ${this.provider}`);
    }

    return result;
  }

  /**
   * 检查视频生成状态
   */
  async checkStatus(videoId) {
    const endpoint = this.provider === 'heygen' 
      ? `/video_generate/${videoId}`
      : `/talks/${videoId}`;

    return this.makeRequest(endpoint, 'GET');
  }

  /**
   * 下载视频
   */
  async downloadVideo(videoUrl, outputPath) {
    return new Promise((resolve, reject) => {
      const file = fs.createWriteStream(outputPath);
      
      https.get(videoUrl, (response) => {
        response.pipe(file);
        file.on('finish', () => {
          file.close();
          resolve(outputPath);
        });
      }).on('error', reject);
    });
  }
}

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    options[key] = value;
  }

  const generator = new AvatarVideoGenerator({
    provider: options.provider || 'heygen',
    apiKey: options.apiKey || process.env.AVATAR_API_KEY
  });

  if (options.script) {
    try {
      const scriptContent = fs.readFileSync(options.script, 'utf-8');
      const script = JSON.parse(scriptContent);

      generator.generate(script).then(result => {
        console.log('✓ 视频生成请求已提交');
        console.log(JSON.stringify(result, null, 2));

        if (options.output) {
          console.log(`📁 输出路径: ${options.output}`);
        }
      }).catch(error => {
        console.error('✗ 生成失败:', error.message);
        process.exit(1);
      });
    } catch (error) {
      console.error('✗ 错误:', error.message);
      process.exit(1);
    }
  } else {
    console.log('用法: node avatar-generator.js --provider heygen --script script.json --output video.mp4');
    console.log('\n支持的提供商: heygen, d-id, synthesia');
    console.log('需要设置环境变量: AVATAR_API_KEY');
  }
}

module.exports = AvatarVideoGenerator;
