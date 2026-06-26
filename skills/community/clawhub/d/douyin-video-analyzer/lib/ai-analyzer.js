/**
 * AI 视觉分析模块 (v3.2 - 精简稳健版)
 * 专注于基于视频关键帧的视觉深度拆解方案
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { imageToBase64 } = require('./frame-extractor');

// 智谱 API 配置
const ZHIPU_API_BASE = 'open.bigmodel.cn';
const ZHIPU_API_PATH = '/api/paas/v4/chat/completions';

const SUPPORTED_MODELS = {
  FULL: 'glm-4.6v'
};

const DEFAULT_MODEL = SUPPORTED_MODELS.FULL;

/**
 * 智谱 API 调用核心
 */
async function callZhipuAPI(apiKey, messages, model = DEFAULT_MODEL) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: model,
      messages: messages,
      temperature: 0.7,
      max_tokens: 2048,
      response_format: { type: 'json_object' }
    });
    
    const options = {
      hostname: ZHIPU_API_BASE,
      path: ZHIPU_API_PATH,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(data)
      },
      timeout: 120000
    };
    
    const req = https.request(options, (res) => {
      let out = '';
      res.on('data', c => out += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(out);
          if (json.error) reject(new Error(json.error.message));
          else resolve(json);
        } catch (e) { reject(new Error('解析失败: ' + out.substring(0, 100))); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

const ANALYSIS_PROMPT = `请分析这些视频帧，提供结构化的视觉分析报告。内容要求以 JSON 格式返回，包含：
{
  "visualStyle": "视觉风格",
  "colorScheme": "配色方案",
  "textFrequency": "文字出现频率 (高/中/低)",
  "hooks": ["视觉钩子1", "视觉钩子2"],
  "recommendations": ["可复制元素1", "可复制元素2"]
}`;

/**
 * 核心：基于视频帧序列的深度分析 (分段处理版)
 * @param {string[]} framePaths - 关键帧路径数组
 * @param {string} apiKey - 智谱 API Key
 * @param {string} model - 模型名称
 */
async function analyzeFrames(framePaths, apiKey, model = DEFAULT_MODEL) {
  if (!apiKey) throw new Error('缺少 API Key');
  
  console.log(`  🤖 使用模型: ${model} 进行分段视觉拆解...`);
  
  const CHUNK_SIZE = 20; // 优化：每段处理 20 帧，确保不触发接口 Payload 溢出
  const chunks = [];
  for (let i = 0; i < framePaths.length; i += CHUNK_SIZE) {
    chunks.push(framePaths.slice(i, i + CHUNK_SIZE));
  }

  console.log(`  📦 视频共 ${framePaths.length} 帧，分为 ${chunks.length} 段进行处理...`);

  const segmentAnalyses = [];
  for (let i = 0; i < chunks.length; i++) {
    console.log(`  ⏳ 正在分析第 ${i + 1}/${chunks.length} 段 (${chunks[i].length} 帧)...`);
    const content = [{ type: 'text', text: ANALYSIS_PROMPT }];
    for (const p of chunks[i]) {
      try {
        content.push({ 
          type: 'image_url', 
          image_url: { url: `data:image/png;base64,${imageToBase64(p)}` } 
        });
      } catch (e) { console.warn(`  ⚠️ 跳过损坏的帧: ${p}`); }
    }

    const res = await callZhipuAPI(apiKey, [{ role: 'user', content }], model);
    if (res.choices?.[0]?.message?.content) {
      try {
        segmentAnalyses.push(JSON.parse(res.choices[0].message.content));
      } catch (e) {
        segmentAnalyses.push({ raw: res.choices[0].message.content });
      }
    }
  }

  // 汇总结果 (分段处理长文本避免 1214 invalid input)
  console.log('  汇总分段分析结果...');
  
  // 如果只有一段，直接返回
  if (segmentAnalyses.length === 1) return segmentAnalyses[0];

  // 压缩数据：只取关键字段进行汇总，减少 Token 压力
  const simplifiedSegments = segmentAnalyses.map(s => ({
    hooks: s.hooks || [],
    style: s.visualStyle || '',
    rec: s.recommendations || []
  }));

  const summaryPrompt = `以下是一个长视频不同时间段的视觉拆解片段，请将其提炼成一个全局的结构化报告。
要求：
1. 视觉风格和配色方案要给出最普遍适用的特征。
2. 钩子 (hooks) 汇总所有具有代表性的爆点。
3. 建议 (recommendations) 给出全局复用性最强的建议。
结果要求以 JSON 格式返回 (包含 visualStyle, colorScheme, textFrequency, hooks, recommendations)。

片段概要：${JSON.stringify(simplifiedSegments)}`;

  // 使用精简的 message 结构请求，不带图片只带纯文本汇总
  const summaryRes = await callZhipuAPI(apiKey, [{ role: 'user', content: summaryPrompt }], model);
  if (summaryRes.choices?.[0]?.message?.content) {
    try {
      return JSON.parse(summaryRes.choices[0].message.content);
    } catch (e) {
      return { rawAnalysis: summaryRes.choices[0].message.content };
    }
  }
  
  throw new Error('汇总分析失败');
}

/**
 * 获取支持的模型列表
 */
function getSupportedModels() {
  return SUPPORTED_MODELS;
}

module.exports = {
  analyzeFrames,
  getSupportedModels,
  SUPPORTED_MODELS,
  DEFAULT_MODEL
};
