#!/usr/bin/env node
/**
 * refine-memory.js V2
 * 每日记忆提炼脚本 - 使用阿里百炼 API (qwen-max)
 * 
 * 改进点：
 * - API Key 从环境变量读取
 * - 纯异步 httpPost + Promise
 * - 生成 ${date}.refined.md，不覆盖原文件
 * - 6层容错 JSON 提取
 * - 3次重试机制
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// ==================== 配置 ====================
const CONFIG = {
  API_KEY: process.env.DASHSCOPE_API_KEY,
  API_HOST: 'dashscope.aliyuncs.com',
  API_PATH: '/api/v1/services/aigc/text-generation/generation',
  MAX_RETRIES: 3,
  RETRY_DELAY_MS: 1000,
};

// ==================== 工具函数 ====================

/**
 * 带重试的 HTTP POST 请求
 */
function httpPostWithRetry(options, data, retryCount = 0) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(responseData);
          resolve(parsed);
        } catch (e) {
          reject(new Error(`JSON解析失败: ${e.message}, 原始响应: ${responseData.slice(0, 200)}`));
        }
      });
    });

    req.on('error', (error) => {
      if (retryCount < CONFIG.MAX_RETRIES) {
        console.log(`[重试 ${retryCount + 1}/${CONFIG.MAX_RETRIES}] 请求失败: ${error.message}`);
        setTimeout(() => {
          httpPostWithRetry(options, data, retryCount + 1)
            .then(resolve)
            .catch(reject);
        }, CONFIG.RETRY_DELAY_MS * (retryCount + 1));
      } else {
        reject(error);
      }
    });

    req.write(data);
    req.end();
  });
}

/**
 * 6层容错 JSON 提取策略
 */
function extractJson(content) {
  // 策略1: 直接 JSON.parse
  try {
    const parsed = JSON.parse(content.trim());
    console.log('[JSON提取] 策略1成功: 直接解析');
    return parsed;
  } catch (e) {
    console.log('[JSON提取] 策略1失败: 不是纯JSON格式');
  }

  // 策略2: 提取 ```json 代码块
  const jsonBlockMatch = content.match(/```json\s*([\s\S]*?)```/);
  if (jsonBlockMatch) {
    try {
      const parsed = JSON.parse(jsonBlockMatch[1].trim());
      console.log('[JSON提取] 策略2成功: ```json代码块');
      return parsed;
    } catch (e) {
      console.log('[JSON提取] 策略2失败');
    }
  }

  // 策略3: 提取任意 ``` 代码块
  const codeBlockMatch = content.match(/```\s*([\s\S]*?)```/);
  if (codeBlockMatch) {
    try {
      const parsed = JSON.parse(codeBlockMatch[1].trim());
      console.log('[JSON提取] 策略3成功: 通用代码块');
      return parsed;
    } catch (e) {
      console.log('[JSON提取] 策略3失败');
    }
  }

  // 策略4: 提取 { ... } 或 [ ... ]
  const objectMatch = content.match(/\{[\s\S]*\}/);
  if (objectMatch) {
    try {
      const parsed = JSON.parse(objectMatch[0]);
      console.log('[JSON提取] 策略4成功: 提取{...}结构');
      return parsed;
    } catch (e) {
      console.log('[JSON提取] 策略4失败');
    }
  }

  // 策略5: 提取数组
  const arrayMatch = content.match(/\[[\s\S]*\]/);
  if (arrayMatch) {
    try {
      const parsed = JSON.parse(arrayMatch[0]);
      console.log('[JSON提取] 策略5成功: 提取[...]数组');
      return parsed;
    } catch (e) {
      console.log('[JSON提取] 策略5失败');
    }
  }

  // 策略6: 查找第一个有效的 JSON 开始位置
  const startIndex = content.indexOf('{');
  if (startIndex !== -1) {
    try {
      // 尝试找到匹配的结束括号
      let depth = 0;
      let endIndex = startIndex;
      for (let i = startIndex; i < content.length; i++) {
        if (content[i] === '{') depth++;
        if (content[i] === '}') depth--;
        if (depth === 0) {
          endIndex = i + 1;
          break;
        }
      }
      const jsonStr = content.slice(startIndex, endIndex);
      const parsed = JSON.parse(jsonStr);
      console.log('[JSON提取] 策略6成功: 括号匹配提取');
      return parsed;
    } catch (e) {
      console.log('[JSON提取] 策略6失败');
    }
  }

  throw new Error('所有JSON提取策略均失败');
}

/**
 * 提炼单条记忆
 */
async function refineMemory(memoryText) {
  if (!CONFIG.API_KEY) {
    throw new Error('DASHSCOPE_API_KEY 环境变量未设置');
  }

  const prompt = `请将以下对话记忆提炼为结构化信息。提炼要求：
1. 保留关键决策、数据、踩坑记录、新概念、金句
2. 去除闲聊、重复、无信息量的内容
3. 使用简洁的要点形式
4. 保持原始时间戳

原始内容：
${memoryText}

请返回 JSON 格式：
{
  "themes": [
    {
      "topic": "主题名称",
      "highlights": [
        { "time": "时间戳", "type": "决策|数据|踩坑|概念|金句", "content": "提炼内容" }
      ]
    }
  ]
}`;

  const requestBody = JSON.stringify({
    model: 'qwen-max',
    input: {
      messages: [{ role: 'user', content: prompt }]
    },
    parameters: {
      result_format: 'message',
      max_tokens: 4096,
      temperature: 0.3
    }
  });

  const options = {
    hostname: CONFIG.API_HOST,
    port: 443,
    path: CONFIG.API_PATH,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${CONFIG.API_KEY}`,
      'Content-Length': Buffer.byteLength(requestBody)
    }
  };

  const response = await httpPostWithRetry(options, requestBody);

  if (response.output?.choices?.[0]?.message?.content) {
    const content = response.output.choices[0].message.content;
    return extractJson(content);
  }

  throw new Error('API 响应格式异常');
}

/**
 * 生成提炼后的 Markdown
 */
function generateRefinedMarkdown(date, themes) {
  let output = `# Memory - ${date} (Refined)\n\n`;
  output += `> 本文件由 AI 自动提炼生成\n`;
  output += `> 原文件: ${date}.md\n`;
  output += `> 生成时间: ${new Date().toISOString()}\n\n`;

  for (const theme of themes) {
    output += `## ${theme.topic}\n\n`;
    for (const highlight of theme.highlights) {
      output += `- **[${highlight.time}]** \`${highlight.type}\` ${highlight.content}\n`;
    }
    output += '\n';
  }

  return output;
}

// ==================== 主函数 ====================

async function main() {
  try {
    // 获取昨天日期
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const dateStr = yesterday.toISOString().split('T')[0];

    console.log(`[${new Date().toISOString()}] 开始提炼记忆: ${dateStr}`);

    // 读取原始记忆文件
    const inputPath = path.join(__dirname, '..', 'memory', 'feishu', `${dateStr}.md`);
    console.log(`[文件路径] ${inputPath}`);

    if (!fs.existsSync(inputPath)) {
      console.log(`[跳过] 原文件不存在: ${inputPath}`);
      return;
    }

    const rawContent = fs.readFileSync(inputPath, 'utf-8');
    console.log(`[文件大小] ${rawContent.length} 字符`);

    if (rawContent.trim().length === 0) {
      console.log(`[跳过] 原文件为空`);
      return;
    }

    // 检查是否已提炼过
    const outputPath = path.join(__dirname, '..', 'memory', 'feishu', `${dateStr}.refined.md`);
    if (fs.existsSync(outputPath)) {
      console.log(`[跳过] 提炼文件已存在: ${outputPath}`);
      return;
    }

    // 调用 API 提炼
    console.log('[API调用] 开始提炼...');
    const result = await refineMemory(rawContent);

    if (!result.themes || result.themes.length === 0) {
      console.log('[跳过] API 返回空结果');
      return;
    }

    // 生成提炼后的 Markdown
    const refinedMarkdown = generateRefinedMarkdown(dateStr, result.themes);

    // 写入新文件（不覆盖原文件！）
    fs.writeFileSync(outputPath, refinedMarkdown, 'utf-8');
    console.log(`[成功] 提炼完成: ${outputPath}`);
    console.log(`[统计] 提炼了 ${result.themes.length} 个主题`);

  } catch (error) {
    console.error(`[错误] ${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
