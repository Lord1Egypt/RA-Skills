#!/usr/bin/env node
/**
 * Auto Login - 验证码识别模块 v1.1.0
 * 
 * 功能：
 * - 全屏截图 + 视觉模型识别（保持当前策略）
 * - 智能填写验证码（多层选择器策略）
 * - 可被其他脚本 import 复用
 * 
 * 导出函数：
 * - recognizeFromPage(page, config) - 从 Playwright Page 识别并填写
 * - recognizeFromFile(imagePath, config) - 从本地文件识别
 * - recognizeFromBase64(base64, config) - 从 base64 识别
 * 
 * 所属 Skill: auto-login (https://clawhub.com/skills/auto-login)
 */

import { chromium } from 'playwright-core';
import fs from 'fs';
import os from 'os';
import path from 'path';

const HOME_DIR = os.homedir();
const CONFIG_PATH = path.join(HOME_DIR, '.openclaw', 'openclaw.json');
const WORKSPACE_DIR = path.join(HOME_DIR, '.openclaw', 'workspace');

// ========== 配置加载 ==========

/**
 * 支持的视觉模型提供商
 * 注意：使用通用名称，不暴露具体厂商
 */
const MODEL_PROVIDERS = {
  // 阿里云 DashScope（通义千问 VL）- 默认
  'aliyun': {
    baseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    defaultModel: 'qwen3-vl-plus',
    name: '阿里云 Qwen VL'
  },
  // 通用提供商（用户可自行配置任何兼容 OpenAI 格式的 API）
  'generic': {
    baseUrl: '',
    defaultModel: '',
    name: '自定义提供商'
  }
};

/**
 * 加载配置
 * 优先级：函数参数 > 环境变量 (PROVIDER_* > VISION_*) > 配置文件
 */
function loadConfig(overrides = {}) {
  // 方式 1: 直接传入配置
  if (overrides.apiKey || overrides.appId) {
    const provider = overrides.provider || 'aliyun';
    const providerConfig = MODEL_PROVIDERS[provider] || MODEL_PROVIDERS.aliyun;
    return {
      baseUrl: overrides.baseUrl || providerConfig.baseUrl,
      apiKey: overrides.apiKey,
      appId: overrides.appId,
      model: overrides.model || providerConfig.defaultModel,
      provider: provider,
      extraBody: overrides.extraBody || providerConfig.extraBody
    };
  }
  
  // 方式 2: 环境变量（优先 PROVIDER_*，兼容 VISION_*）
  const envApiKey = process.env.PROVIDER_API_KEY || process.env.VISION_API_KEY || process.env.QWEN_API_KEY;
  const envAppId = process.env.PROVIDER_APP_ID;
  
  if (envApiKey || envAppId) {
    // 判断提供商类型
    let provider = 'aliyun';
    const envBaseUrl = process.env.PROVIDER_BASE_URL || process.env.VISION_BASE_URL || process.env.QWEN_BASE_URL;
    const envModel = process.env.PROVIDER_MODEL || process.env.VISION_MODEL || process.env.QWEN_MODEL;
    
    // 如果用户提供了自定义 Base URL，使用 generic 提供商
    if (envBaseUrl && !envBaseUrl.includes('dashscope') && !envBaseUrl.includes('aliyun')) {
      provider = 'generic';
    }
    
    const providerConfig = MODEL_PROVIDERS[provider];
    return {
      baseUrl: envBaseUrl,  // ✅ 允许用户完全自定义，无默认值
      apiKey: envApiKey,
      appId: envAppId,
      model: envModel,      // ✅ 允许用户完全自定义，无默认值
      provider: provider,
      extraBody: providerConfig.extraBody
    };
  }
  
  // 方式 3: 配置文件
  try {
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    
    // 支持多种配置格式
    const visionConfig = 
      config.models?.providers?.generic ||
      config.models?.providers?.bailian ||
      config.models?.providers?.aliyun ||
      config.models?.providers?.dashscope ||
      config.models?.providers?.openai;
    
    if (!visionConfig) {
      throw new Error('配置文件中缺少视觉模型配置');
    }
    
    // 判断提供商类型
    let provider = 'aliyun';
    if (visionConfig.appId || (visionConfig.baseUrl && !visionConfig.baseUrl.includes('dashscope'))) {
      provider = 'generic';
    }
    
    const providerConfig = MODEL_PROVIDERS[provider];
    return {
      baseUrl: visionConfig.baseUrl || providerConfig.baseUrl,
      apiKey: visionConfig.apiKey,
      appId: visionConfig.appId,
      model: visionConfig.model || providerConfig.defaultModel,
      provider: provider,
      extraBody: visionConfig.extraBody || providerConfig.extraBody
    };
  } catch (e) {
    throw new Error(`无法加载配置：${e.message}`);
  }
}

// ========== 核心识别函数 ==========

/**
 * 从 base64 图片识别验证码
 * @param {string} imageBase64 - base64 编码（不含前缀）
 * @param {object} config - 配置
 * @returns {Promise<string>} 验证码文字
 */
export async function recognizeFromBase64(imageBase64, config = {}) {
  const cfg = loadConfig(config);
  
  // 构建请求体
  const requestBody = {
    model: cfg.model,
    messages: [{
      role: 'user',
      content: [
        { type: 'text', text: '请识别图片中的验证码文字，只返回验证码内容，不要任何其他描述。保持原始大小写，不要转换。' },
        { type: 'image_url', image_url: { url: `data:image/png;base64,${imageBase64}` } }
      ]
    }],
    max_tokens: 100,  // ✅ GPT/Gemini 需要更多 token，避免被截断
    temperature: 0.1,
    stream: false
  };
  
  // 通用提供商特殊处理：添加 extra_body
  if (cfg.provider === 'generic' && cfg.extraBody) {
    requestBody.extra_body = cfg.extraBody;
  }
  
  // 构建 Authorization header
  // generic 提供商（如使用 AppId 的）：Authorization: Bearer <AppId>
  // 阿里云等：Authorization: Bearer <API Key>
  const authValue = cfg.provider === 'generic' && cfg.appId
    ? `Bearer ${cfg.appId}`
    : `Bearer ${cfg.apiKey}`;
  
  const response = await fetch(`${cfg.baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': authValue
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => '');
    throw new Error(`API 错误 (${cfg.provider}): ${response.status} ${errorText}`);
  }

  const data = await response.json();
  
  // 处理不同的响应格式
  let content = '';
  if (data.choices?.[0]?.message?.content) {
    content = data.choices[0].message.content.trim();
  } else if (data.choices?.[0]?.delta?.content) {
    content = data.choices[0].delta.content.trim();
  } else {
    throw new Error('API 返回格式异常');
  }
  
  // 检查是否无法识别
  if (content.toUpperCase() === 'UNRECOGNIZABLE' || content.length === 0) {
    throw new Error('视觉模型无法识别验证码');
  }
  
  // 清洗：只保留字母数字，保持原始大小写
  const cleanedText = content.replace(/[^a-zA-Z0-9]/g, '');
  
  if (cleanedText.length === 0) {
    throw new Error('视觉模型返回的内容不包含有效字符');
  }
  
  return cleanedText;
}

/**
 * 从本地文件识别验证码
 * @param {string} imagePath - 图片路径
 * @param {object} config - 配置
 * @returns {Promise<string>} 验证码文字
 */
export async function recognizeFromFile(imagePath, config = {}) {
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  return recognizeFromBase64(base64Image, config);
}

// ========== 智能选择器策略 ==========

/**
 * 查找验证码输入框（增强版）
 * 策略：精确选择器 → accessibility 评分 → 表单结构推断 → 位置启发式
 */
async function findCaptchaInput(context) {
  // ========== 策略 1: 精确选择器匹配 ==========
  
  // 高优先级：id/name/data-* 包含 captcha
  const highPrioritySelectors = [
    'input[id*="captcha" i]',
    'input[name*="captcha" i]',
    'input[aria-label*="captcha" i]',
    'input[data-testid*="captcha" i]',  // 新增：data-testid
    'input[data-captcha]',               // 新增：data-captcha
    'input[data-test="captcha"]'         // 新增：data-test
  ];
  
  // 中优先级：placeholder 多语言支持
  const mediumPrioritySelectors = [
    // 中文
    'input[placeholder*="验证码"]',
    'input[placeholder*="校验码"]',
    'input[placeholder*="识别码"]',
    // 英文
    'input[placeholder*="captcha" i]',
    'input[placeholder*="verification code" i]',
    'input[placeholder*="security code" i]',
    'input[placeholder*="auth code" i]',
    // 其他语言
    'input[placeholder*="verification" i]'
  ];

  for (const selector of highPrioritySelectors) {
    const inputs = await context.locator(selector).all();
    for (const input of inputs) {
      try {
        if (await input.isVisible()) {
          return { input, method: `精确选择器：${selector}` };
        }
      } catch (e) {}
    }
  }
  
  for (const selector of mediumPrioritySelectors) {
    const inputs = await context.locator(selector).all();
    for (const input of inputs) {
      try {
        if (await input.isVisible()) {
          return { input, method: `placeholder 匹配：${selector}` };
        }
      } catch (e) {}
    }
  }

  // ========== 策略 2: accessibility 评分 ==========
  
  const allInputs = await context.locator('input').all();
  const excludeKeywords = ['search', 'query', 'email', 'username', 'password', 'phone', 'tel', 'hidden', 'user', 'pass'];
  const captchaKeywords = ['captcha', '验证码', '校验码', 'image', 'code', 'verify', 'answer', 'security'];
  
  let bestCandidate = null;
  let bestScore = 0;
  
  for (const input of allInputs) {
    try {
      if (!await input.isVisible()) continue;
      
      const box = await input.boundingBox();
      if (!box || box.width < 50 || box.width > 400 || box.height < 15 || box.height > 100) continue;
      
      const type = await input.getAttribute('type');
      if (type === 'hidden' || type === 'submit' || type === 'button') continue;
      
      const placeholder = (await input.getAttribute('placeholder')) || '';
      const name = (await input.getAttribute('name')) || '';
      const id = (await input.getAttribute('id')) || '';
      const ariaLabel = (await input.getAttribute('aria-label')) || '';
      const dataTestid = (await input.getAttribute('data-testid')) || '';
      
      const allText = (placeholder + ' ' + name + ' ' + id + ' ' + ariaLabel + ' ' + dataTestid).toLowerCase();
      
      const isExcluded = excludeKeywords.some(kw => allText.includes(kw));
      if (isExcluded) continue;
      
      let score = 0;
      
      // 尺寸加分
      if (box.width >= 80 && box.width <= 250) score += 10;
      if (box.height >= 30 && box.height <= 60) score += 5;
      
      // 关键词加分
      for (const kw of captchaKeywords) {
        if (allText.includes(kw)) score += 20;
      }
      
      // placeholder 存在加分
      if (placeholder) score += 5;
      if (ariaLabel) score += 10;
      if (dataTestid) score += 5;
      
      if (score > bestScore) {
        bestScore = score;
        bestCandidate = input;
      }
      
    } catch (e) {}
  }
  
  if (bestCandidate && bestScore > 0) {
    return { input: bestCandidate, method: `accessibility 评分：${bestScore}` };
  }

  // ========== 策略 3: 表单结构推断 ==========
  // 登录表单中，最后一个可见的文本输入框通常是验证码
  
  const forms = await context.locator('form').all();
  for (const form of forms) {
    try {
      const textInputs = await form.locator('input[type="text"], input:not([type])').all();
      const visibleInputs = [];
      
      for (const input of textInputs) {
        if (await input.isVisible()) {
          const type = await input.getAttribute('type');
          const placeholder = (await input.getAttribute('placeholder')) || '';
          const name = (await input.getAttribute('name')) || '';
          
          // 排除账号密码
          if (/user|account|email|phone/i.test(name + placeholder)) continue;
          if (/pass|pwd/i.test(name + placeholder)) continue;
          
          visibleInputs.push(input);
        }
      }
      
      // 如果有 2-4 个输入框，最后一个很可能是验证码
      if (visibleInputs.length >= 2 && visibleInputs.length <= 4) {
        const lastInput = visibleInputs[visibleInputs.length - 1];
        return { input: lastInput, method: '表单结构推断：最后一个文本输入框' };
      }
      
    } catch (e) {}
  }

  // ========== 策略 4: 位置启发式 ==========
  // 查找验证码图片附近的输入框
  
  const captchaImgSelectors = [
    'img[alt*="captcha" i]',
    'img[id*="captcha" i]',
    'img[class*="captcha" i]',
    'img[src*="captcha" i]',
    'img[src*="code" i]',
    'img.onclick'  // 点击刷新的验证码
  ];
  
  for (const selector of captchaImgSelectors) {
    const captchaImg = context.locator(selector).first();
    try {
      if (await captchaImg.count() > 0) {
        const captchaBox = await captchaImg.boundingBox();
        if (captchaBox) {
          for (const input of allInputs) {
            try {
              const box = await input.boundingBox();
              if (box && await input.isVisible()) {
                const verticalDist = Math.abs((box.y + box.height/2) - (captchaBox.y + captchaBox.height/2));
                const horizontalDist = Math.abs((box.x + box.width/2) - (captchaBox.x + captchaBox.width/2));
                
                if (verticalDist < 150 && horizontalDist < 400) {
                  return { input, method: `位置查找：距离验证码图片 垂直${verticalDist.toFixed(0)}px` };
                }
              }
            } catch (e) {}
          }
        }
      }
    } catch (e) {}
  }

  return null;
}

/**
 * 查找提交按钮（增强版）
 */
async function findSubmitButton(context) {
  const buttonSelectors = [
    // 文本匹配
    'button:has-text("登录")',
    'button:has-text("Login")',
    'button:has-text("Submit")',
    'button:has-text("验证")',
    'button:has-text("提交")',
    'button:has-text("Validate")',
    'button:has-text("Check")',
    'button:has-text("确认")',
    'button:has-text("Sign In")',
    'button:has-text("Sign Up")',
    // 类型匹配
    'input[type="submit"]',
    'button[type="submit"]',
    // data-* 属性
    'button[data-testid*="submit" i]',
    'button[data-action="submit"]'
  ];

  for (const selector of buttonSelectors) {
    const buttons = await context.locator(selector).all();
    for (const btn of buttons) {
      try {
        if (await btn.isVisible()) {
          const text = await btn.textContent().catch(() => '');
          return { button: btn, method: `按钮选择器：${selector}`, text: text.trim() };
        }
      } catch (e) {}
    }
  }

  // accessibility 分析
  const allButtons = await context.locator('button, input[type="submit"], input[type="button"]').all();
  const buttonKeywords = ['submit', 'login', 'validate', 'verify', 'check', '确认', '提交', '验证', '登录', 'ok', 'go', 'sign'];
  const excludeKeywords = ['menu', 'header', 'nav', 'open', 'close', 'toggle', 'cancel', 'back', 'reset'];
  
  let bestBtn = null;
  let bestScore = 0;
  
  for (const btn of allButtons) {
    try {
      if (!await btn.isVisible()) continue;
      
      const box = await btn.boundingBox();
      if (!box || box.width < 40 || box.width > 250 || box.height < 25 || box.height > 100) continue;
      
      const text = (await btn.textContent().catch(() => '')).toLowerCase();
      const ariaLabel = (await btn.getAttribute('aria-label')) || '';
      const name = (await btn.getAttribute('name')) || '';
      const value = (await btn.getAttribute('value')) || '';
      const dataTestid = (await btn.getAttribute('data-testid')) || '';
      
      const allText = (text + ' ' + ariaLabel + ' ' + name + ' ' + value + ' ' + dataTestid).toLowerCase();
      
      const isExcluded = excludeKeywords.some(kw => allText.includes(kw));
      if (isExcluded) continue;
      
      let score = 0;
      
      for (const kw of buttonKeywords) {
        if (allText.includes(kw)) score += 20;
      }
      
      if (box.width >= 60 && box.width <= 150) score += 5;
      if (box.height >= 30 && box.height <= 60) score += 5;
      if (dataTestid) score += 5;
      
      if (score > bestScore) {
        bestScore = score;
        bestBtn = btn;
      }
      
    } catch (e) {}
  }
  
  if (bestBtn && bestScore > 0) {
    return { button: bestBtn, method: `accessibility 评分：${bestScore}`, text: '' };
  }

  return null;
}

// ========== 主函数 ==========

/**
 * 从 Playwright Page 识别验证码并自动填写提交
 * @param {Page} page - Playwright Page 对象
 * @param {object} options - 选项
 * @returns {Promise<object>} 结果
 */
export async function recognizeFromPage(page, options = {}) {
  const {
    outputPrefix = 'captcha_auto',
    config = {},
    skipFill = false,
    skipSubmit = false
  } = options;

  const cfg = loadConfig(config);
  let captchaText = null;
  let screenshots = {};

  try {
    // 全屏截图
    screenshots.page = path.join(WORKSPACE_DIR, `${outputPrefix}_page.png`);
    await page.screenshot({ path: screenshots.page, fullPage: true });

    // 识别验证码
    const imageBuffer = fs.readFileSync(screenshots.page);
    const base64Image = imageBuffer.toString('base64');
    captchaText = await recognizeFromBase64(base64Image, config);

    if (skipFill) {
      return {
        success: true,
        text: captchaText,
        method: 'vision',
        screenshots
      };
    }

    // 查找并填写输入框
    const inputResult = await findCaptchaInput(page);
    
    if (!inputResult) {
      return {
        success: false,
        error: '未找到验证码输入框',
        text: captchaText,
        screenshots
      };
    }

    await inputResult.input.fill(captchaText);
    
    screenshots.filled = path.join(WORKSPACE_DIR, `${outputPrefix}_filled.png`);
    await page.screenshot({ path: screenshots.filled, fullPage: true });

    if (skipSubmit) {
      return {
        success: true,
        text: captchaText,
        method: 'vision',
        inputMethod: inputResult.method,
        screenshots
      };
    }

    // 查找并点击提交按钮
    const buttonResult = await findSubmitButton(page);
    
    if (buttonResult) {
      await buttonResult.button.click();
      await page.waitForTimeout(3000);
      
      screenshots.result = path.join(WORKSPACE_DIR, `${outputPrefix}_result.png`);
      await page.screenshot({ path: screenshots.result, fullPage: true });
      
      return {
        success: true,
        text: captchaText,
        method: 'vision',
        inputMethod: inputResult.method,
        buttonMethod: buttonResult.method,
        screenshots
      };
    } else {
      return {
        success: true,
        text: captchaText,
        method: 'vision',
        inputMethod: inputResult.method,
        buttonFound: false,
        screenshots
      };
    }

  } catch (error) {
    screenshots.error = path.join(WORKSPACE_DIR, `${outputPrefix}_error.png`);
    await page.screenshot({ path: screenshots.error, fullPage: true });
    
    return {
      success: false,
      error: error.message,
      text: captchaText,
      screenshots
    };
  }
}

// ========== CLI 模式 ==========

async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
验证码识别模块 v1.1.0

用法:
  node recognize.mjs --url=<url> [选项]

选项:
  --url=<url>         目标页面 URL
  --prefix=<prefix>   输出文件前缀（默认：captcha_auto）
  --api-key=<key>     API Key
  --skip-fill         只识别不填写
  --skip-submit       填写但不提交
  --json              JSON 输出

示例:
  node recognize.mjs --url="https://example.com/login"
  node recognize.mjs --url="https://example.com" --skip-fill
`);
    return;
  }

  let options = {};
  for (const arg of args) {
    if (arg.startsWith('--url=')) options.url = arg.substring(6);
    if (arg.startsWith('--prefix=')) options.prefix = arg.substring(9);
    if (arg.startsWith('--api-key=')) options.apiKey = arg.substring(10);
    if (arg === '--skip-fill') options.skipFill = true;
    if (arg === '--skip-submit') options.skipSubmit = true;
    if (arg === '--json') options.json = true;
  }

  if (!options.url) {
    console.error('❌ 错误：缺少必需参数 --url');
    process.exit(1);
  }

  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 800 });

  try {
    await page.goto(options.url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    const result = await recognizeFromPage(page, {
      outputPrefix: options.prefix || 'captcha_auto',
      config: { apiKey: options.apiKey },
      skipFill: options.skipFill,
      skipSubmit: options.skipSubmit
    });

    if (options.json) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      if (result.success) {
        console.log(`✅ 验证码：${result.text}`);
        console.log(`   识别方式：${result.method}`);
        if (result.inputMethod) console.log(`   输入框：${result.inputMethod}`);
        if (result.buttonMethod) console.log(`   按钮：${result.buttonMethod}`);
      } else {
        console.log(`❌ 失败：${result.error}`);
      }
    }

    process.exit(result.success ? 0 : 1);

  } catch (error) {
    console.error(`❌ 错误：${error.message}`);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

// 导出函数
export { findCaptchaInput, findSubmitButton };
