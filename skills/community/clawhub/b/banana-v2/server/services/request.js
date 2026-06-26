const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const https = require('https');
const http = require('http');
const axios = require('axios');

// 存储活跃的轮询任务
const activePollingTasks = new Map();

class RequestHandler {
  constructor(db, taskHandler = null) {
    this.db = db;
    this.taskHandler = taskHandler;
  }

  // 设置 TaskHandler（用于轮询）
  setTaskHandler(taskHandler) {
    this.taskHandler = taskHandler;
  }

  // 启动轮询任务
  startPolling(workId, task_id, config) {
    // 如果已经在轮询中，跳过
    if (activePollingTasks.has(workId)) {
      console.log(`[Polling] 任务 ${workId} 已在轮询中`);
      return;
    }

    const interval = config.polling?.interval || 60000; // 默认60秒
    const maxTimes = config.polling?.max_times || 20; // 默认最多20次
    let pollCount = 0;

    console.log(`[Polling] 启动轮询任务 work_id=${workId}, task_id=${task_id}, 间隔=${interval}ms`);

    const pollTask = async () => {
      pollCount++;
      console.log(`[Polling] 第 ${pollCount}/${maxTimes} 次轮询 work_id=${workId}`);

      try {
        if (!this.taskHandler) {
          console.error('[Polling] TaskHandler 未设置');
          activePollingTasks.delete(workId);
          return;
        }

        const result = await this.taskHandler.poll(workId);
        console.log(`[Polling] work_id=${workId} 状态:`, result.status);

        // 更新轮询计数
        await this.db.updatePollInfo(workId, pollCount, Date.now() + interval);

        if (result.status === 'completed') {
          console.log(`[Polling] 任务 ${workId} 完成！`);
          activePollingTasks.delete(workId);
          return;
        }

        if (result.status === 'failed') {
          console.log(`[Polling] 任务 ${workId} 失败:`, result.msg);
          activePollingTasks.delete(workId);
          return;
        }

        // 检查是否超过最大轮询次数
        if (pollCount >= maxTimes) {
          console.log(`[Polling] 任务 ${workId} 轮询次数超限`);
          await this.db.updateWorkState(workId, 99, '轮询超时');
          activePollingTasks.delete(workId);
          return;
        }

        // 继续轮询
        const timer = setTimeout(pollTask, interval);
        activePollingTasks.set(workId, timer);

      } catch (error) {
        console.error(`[Polling] 轮询错误 work_id=${workId}:`, error.message);
        
        // 如果还有轮询次数，继续尝试
        if (pollCount < maxTimes) {
          const timer = setTimeout(pollTask, interval);
          activePollingTasks.set(workId, timer);
        } else {
          activePollingTasks.delete(workId);
        }
      }
    };

    // 首次轮询延迟5秒后开始（给API一些处理时间）
    const initialDelay = 5000;
    const timer = setTimeout(pollTask, initialDelay);
    activePollingTasks.set(workId, timer);
  }

  // 获取切割提示词
  getCutPrompt(cutNum) {
    if (cutNum <= 1) return '';
    
    const configDir = path.join(__dirname, '../../config');
    const cutPromptPath = path.join(configDir, `cut_${cutNum}.prompt`);
    
    // 如果文件不存在，创建默认提示词
    if (!fs.existsSync(cutPromptPath)) {
      const defaultPrompt = this.createDefaultCutPrompt(cutNum);
      fs.writeFileSync(cutPromptPath, defaultPrompt, 'utf-8');
      console.log(`[Request] 已创建默认切割提示词文件: cut_${cutNum}.prompt`);
      return defaultPrompt;
    }
    
    // 文件已存在，直接读取
    return fs.readFileSync(cutPromptPath, 'utf-8');
  }

  // 创建默认切割提示词（仅在文件不存在时调用）
  createDefaultCutPrompt(cutNum) {
    const prompts = {
      2: `#按要求生成以下内容
`,
      4: `#按要求生成以下内容
`,
      6: `#按要求生成以下内容
`,
      9: `#按要求生成以下内容
`
    };
    
    return prompts[cutNum] || `#按要求生成以下内容
`;
  }

  // 使用 https.request 发送请求
  async sendRequest(url, data, headers) {
    return new Promise((resolve, reject) => {
      const urlObj = new URL(url);
      const isHttps = urlObj.protocol === 'https:';
      const lib = isHttps ? https : http;
      
      const options = {
        hostname: urlObj.hostname,
        port: urlObj.port || (isHttps ? 443 : 80),
        path: urlObj.pathname + urlObj.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...headers
        }
      };

      const req = lib.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
          try {
            const response = {
              status: res.statusCode,
              statusText: res.statusMessage,
              data: JSON.parse(body)
            };
            resolve(response);
          } catch (e) {
            resolve({
              status: res.statusCode,
              statusText: res.statusMessage,
              data: body
            });
          }
        });
      });

      req.on('error', (e) => {
        reject(e);
      });

      req.setTimeout(120000, () => {
        req.destroy();
        reject(new Error('请求超时'));
      });

      req.write(JSON.stringify(data));
      req.end();
    });
  }

  async generate(data) {
    // 从请求中获取配置，并存储到环境变量（供后续轮询使用）
    if (data.api_key) {
      process.env.API_KEY = data.api_key;
    }
    if (data.platform_token) {
      process.env.PLATFORM_TOKEN = data.platform_token;
    }
    if (data.model_api_key) {
      process.env.MODEL_API_KEY = data.model_api_key;
    }
    if (data.save_path) {
      process.env.SAVE_PATH = data.save_path;
    }
    
    const apiKey = process.env.API_KEY;
    const platformToken = process.env.PLATFORM_TOKEN;
    
    // 检查 API_KEY
    if (!apiKey) {
      throw new Error('请先配置 API Key');
    }

    // 读取配置
    const configPath = path.join(__dirname, '../../config/set.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

    // 获取当前模型配置
    const modelConfig = config.models.find(m => m.model === data.model);
    
    // 获取图片URLs（前端已上传）
    const imageUrls = data.image_urls || [];
    
    console.log(`[Request] 图片URLs:`, imageUrls);

    // 构建请求参数
    // 处理切割提示词（cut > 1 时添加系统提示词到 prompt 顶部）
    let finalPrompt = data.prompt;
    const cutNum = data.cut || 1;
    if (cutNum > 1) {
      const cutPrompt = this.getCutPrompt(cutNum);
      if (cutPrompt) {
        finalPrompt = cutPrompt + data.prompt;
        console.log(`[Request] 添加 ${cutNum} 宫格切割提示词`);
      }
    }

    const requestData = {
      model: data.model || 'nano-banana-pro',
      prompt: finalPrompt,
      action: imageUrls.length > 0 ? 'edit' : 'generate',
      callback_url: 'jakey'
    };

    // 根据模型配置的request映射添加参数
    if (modelConfig && modelConfig.request) {
      const requestMapping = modelConfig.request;
      if (data.ratio && requestMapping.size) {
        requestData[requestMapping.size] = data.ratio;
      }
      if (data.quality && requestMapping.quality) {
        requestData[requestMapping.quality] = data.quality;
      }
    } else {
      if (data.ratio) requestData.aspect_ratio = data.ratio;
      if (data.quality) requestData.resolution = data.quality;
    }

    // 添加图片URLs
    if (imageUrls.length > 0) {
      requestData.image_urls = imageUrls;
    }

    // 调试日志：显示完整的请求数据
    console.log('[Request] 完整请求数据:', JSON.stringify(requestData, null, 2));

    try {
      // 使用 https.request 提交到模型服务器
      const response = await this.sendRequest(
        config.server.url,
        requestData,
        {
          'Authorization': `Bearer ${apiKey}`
        }
      );

      // 调试日志
      console.log('[Request] 响应状态:', response.status);
      console.log('[Request] 响应数据:', JSON.stringify(response.data, null, 2));

      // 检查是否有 task_id（即使状态码不是 200，只要有 task_id 就说明任务已创建）
      const task_id = response.data?.task_id;
      
      // 如果有错误信息但没有 task_id，则抛出错误
      if (!task_id) {
        if (response.data?.error?.message) {
          throw new Error(response.data.error.message);
        }
        if (!response.data.success) {
          throw new Error(response.data.message || '提交失败');
        }
        throw new Error(`HTTP ${response.status}: ${JSON.stringify(response.data)}`);
      }

      // 如果有警告信息，记录但不阻止
      if (response.data?.error?.message) {
        console.warn('[Request] API 警告:', response.data.error.message);
      }

      // 保存到数据库
      const workId = await this.db.createWork({
        task_id,
        prompt: data.prompt,
        size: data.quality || '2K',
        quality: data.quality || '2K',
        cut: data.cut || 1,
        path: '',
        model: data.model || 'nano-banana-pro',
        ratio: data.ratio || '1:1',
        request_data: requestData
      });

      // 启动轮询任务
      if (this.taskHandler) {
        this.startPolling(workId, task_id, config);
      } else {
        console.warn('[Request] TaskHandler 未设置，无法启动自动轮询');
      }

      return {
        success: true,
        msg: '任务提交成功，已启动轮询',
        work_id: workId,
        task_id,
        polling: true,
        debug: {
          request: requestData,
          response: response.data
        }
      };

    } catch (error) {
      let errorMsg = '提交失败';
      let debugInfo = {
        request_url: config.server.url,
        request_data: requestData,
        error: null
      };
      
      if (error.response) {
        debugInfo.error = {
          status: error.response.status,
          data: error.response.data
        };
        errorMsg = error.response.data?.error || error.response.data?.message || JSON.stringify(error.response.data);
      } else {
        debugInfo.error = {
          message: error.message,
          code: error.code
        };
        errorMsg = error.message;
      }
      
      throw new Error(`${errorMsg}\n\n[调试信息]\n请求URL: ${debugInfo.request_url}\n请求数据: ${JSON.stringify(debugInfo.request_data, null, 2)}\n错误: ${JSON.stringify(debugInfo.error, null, 2)}`);
    }
  }
}

module.exports = RequestHandler;
