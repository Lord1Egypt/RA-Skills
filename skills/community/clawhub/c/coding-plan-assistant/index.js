/**
 * coding-plan-assistant
 * 
 * 管理各种编程助手（Coding Plan）的注册、购买和凭据配置流程
 * 
 * @version 1.0.0
 * @author OpenClaw Skills
 */

const fs = require('fs');
const path = require('path');

// 技能目录
const SKILL_DIR = __dirname;
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');
const ENV_PATH = path.join(process.env.INIT_CWD || process.cwd(), '.openclaw', '.env');

// 加载配置
let config = {};
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
} catch (err) {
  console.error('无法加载配置文件，使用默认配置');
  config = {
    platforms: {}
  };
}

/**
 * 脱敏 API Key
 * @param {string} key - API Key
 * @returns {string} - 脱敏后的 Key
 */
function maskKey(key) {
  if (!key || key.length < 10) return '***';
  if (key.startsWith('sk-') || key.startsWith('ghp_') || key.startsWith('sk-or-')) {
    return key.substring(0, 8) + '...' + '***';
  }
  return key.substring(0, 4) + '...' + '***';
}

/**
 * 读取 .env 文件中的凭据
 * @param {string} keyName - 环境变量名
 * @returns {string|null} - 凭据值或 null
 */
function getCredential(keyName) {
  try {
    if (!fs.existsSync(ENV_PATH)) {
      return null;
    }
    const envContent = fs.readFileSync(ENV_PATH, 'utf-8');
    const lines = envContent.split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith(keyName + '=')) {
        return trimmed.substring(keyName.length + 1).trim();
      }
    }
    return null;
  } catch (err) {
    return null;
  }
}

/**
 * 保存凭据到 .env 文件
 * @param {string} keyName - 环境变量名
 * @param {string} keyValue - 凭据值
 * @returns {boolean} - 是否成功
 */
function saveCredential(keyName, keyValue) {
  try {
    // 确保 .openclaw 目录存在
    const envDir = path.dirname(ENV_PATH);
    if (!fs.existsSync(envDir)) {
      fs.mkdirSync(envDir, { recursive: true });
    }

    // 读取现有内容
    let envContent = '';
    if (fs.existsSync(ENV_PATH)) {
      envContent = fs.readFileSync(ENV_PATH, 'utf-8');
    }

    // 检查是否已存在该 key
    const lines = envContent.split('\n');
    let found = false;
    for (let i = 0; i < lines.length; i++) {
      const trimmed = lines[i].trim();
      if (trimmed.startsWith(keyName + '=')) {
        lines[i] = `${keyName}=${keyValue}`;
        found = true;
        break;
      }
    }

    if (!found) {
      lines.push(`${keyName}=${keyValue}`);
    }

    // 写回文件
    fs.writeFileSync(ENV_PATH, lines.join('\n'), 'utf-8');
    return true;
  } catch (err) {
    console.error('保存凭据失败:', err.message);
    return false;
  }
}

/**
 * 检查平台凭据状态
 * @param {string} platformId - 平台 ID
 * @returns {Object} - 状态信息
 */
function checkPlatformStatus(platformId) {
  const platform = config.platforms[platformId];
  if (!platform) {
    return { exists: false, configured: false };
  }

  const credential = getCredential(platform.envKey);
  return {
    exists: true,
    configured: !!credential,
    keyPreview: credential ? maskKey(credential) : null,
    platform: platform
  };
}

/**
 * 获取所有平台的状态
 * @returns {Array} - 平台状态列表
 */
function getAllPlatformsStatus() {
  const results = [];
  for (const platformId of Object.keys(config.platforms)) {
    results.push({
      id: platformId,
      ...checkPlatformStatus(platformId)
    });
  }
  return results;
}

/**
 * 生成注册指南
 * @param {string} platformId - 平台 ID
 * @returns {string} - 注册指南文本
 */
function generateRegisterGuide(platformId) {
  const platform = config.platforms[platformId];
  if (!platform) {
    return `❌ 未找到平台：${platformId}`;
  }

  let guide = `## 📝 ${platform.name} 注册指南\n\n`;
  guide += `### 注册链接\n`;
  guide += `${platform.registerUrl}\n\n`;
  
  if (platform.steps) {
    guide += `### 注册步骤\n`;
    platform.steps.forEach((step, index) => {
      guide += `${index + 1}. ${step}\n`;
    });
    guide += `\n`;
  }

  guide += `### 定价信息\n`;
  guide += `查看定价：${platform.pricingUrl}\n\n`;

  if (platform.freeTier) {
    guide += `### 免费额度\n`;
    guide += `${platform.freeTier}\n\n`;
  }

  return guide;
}

/**
 * 对比各平台定价
 * @returns {string} - 定价对比文本
 */
function comparePricing() {
  let output = `## 💰 编程助手平台定价对比\n\n`;
  output += `| 平台 | 免费额度 | 付费起点 | 计费方式 |\n`;
  output += `|------|----------|----------|----------|\n`;

  for (const platformId of Object.keys(config.platforms)) {
    const platform = config.platforms[platformId];
    output += `| ${platform.name} | ${platform.freeTier || '无'} | ${platform.pricing || '未知'} | ${platform.billing || '未知'} |\n`;
  }

  output += `\n### 💡 推荐方案\n\n`;
  output += `- **学生用户**: GitHub Copilot（学生免费）\n`;
  output += `- **个人开发者**: OpenRouter（有免费模型）\n`;
  output += `- **企业用户**: 根据需求选择对应平台\n`;
  output += `- **尝鲜体验**: 先使用各平台免费额度\n`;

  return output;
}

/**
 * 主函数 - 处理用户请求
 * @param {string} action - 动作类型
 * @param {Object} params - 参数
 * @returns {string} - 响应文本
 */
function main(action, params = {}) {
  switch (action) {
    case 'list':
      // 列出所有支持的平台
      let listOutput = `## 📋 支持的编程助手平台\n\n`;
      for (const platformId of Object.keys(config.platforms)) {
        const platform = config.platforms[platformId];
        const status = checkPlatformStatus(platformId);
        const statusIcon = status.configured ? '✅' : '⬜';
        listOutput += `${statusIcon} **${platform.name}**\n`;
        listOutput += `   注册：${platform.registerUrl}\n`;
        listOutput += `   免费：${platform.freeTier || '无'}\n\n`;
      }
      return listOutput;

    case 'status':
      // 检查配置状态
      const statuses = getAllPlatformsStatus();
      let statusOutput = `## 🔐 凭据配置状态\n\n`;
      const configured = statuses.filter(s => s.configured);
      const notConfigured = statuses.filter(s => !s.configured);

      if (configured.length > 0) {
        statusOutput += `### ✅ 已配置\n\n`;
        configured.forEach(s => {
          statusOutput += `- **${s.platform.name}**: ${s.keyPreview}\n`;
        });
        statusOutput += `\n`;
      }

      if (notConfigured.length > 0) {
        statusOutput += `### ⬜ 未配置\n\n`;
        notConfigured.forEach(s => {
          statusOutput += `- **${s.platform.name}**\n`;
        });
        statusOutput += `\n`;
      }

      statusOutput += `总计：${configured.length}/${statuses.length} 已配置\n`;
      return statusOutput;

    case 'register':
      // 生成注册指南
      return generateRegisterGuide(params.platform);

    case 'pricing':
      // 对比定价
      return comparePricing();

    case 'configure':
      // 配置凭据（需要用户提供 Key）
      const platform = config.platforms[params.platform];
      if (!platform) {
        return `❌ 未找到平台：${params.platform}`;
      }
      return `请提供 ${platform.name} 的 API Key，我将安全存储到 .openclaw/.env`;

    case 'save-key':
      // 保存 API Key
      const platformToSave = config.platforms[params.platform];
      if (!platformToSave) {
        return `❌ 未找到平台：${params.platform}`;
      }
      const success = saveCredential(platformToSave.envKey, params.key);
      return success 
        ? `✅ ${platformToSave.name} 的 API Key 已安全存储`
        : `❌ 保存失败，请检查权限`;

    case 'rotate':
      // 轮换 Key
      const platformToRotate = config.platforms[params.platform];
      if (!platformToRotate) {
        return `❌ 未找到平台：${params.platform}`;
      }
      return `⚠️ 轮换 ${platformToRotate.name} 的 API Key\n\n` +
             `请先在对应平台生成新的 API Key，然后提供给我进行更新。`;

    case 'help':
    default:
      return `## 🤖 coding-plan-assistant 使用指南\n\n` +
             `### 可用命令\n\n` +
             `- **list**: 列出所有支持的平台\n` +
             `- **status**: 检查凭据配置状态\n` +
             `- **register <平台>**: 获取注册指南（如：register claude-code）\n` +
             `- **pricing**: 对比各平台定价\n` +
             `- **configure <平台>**: 配置 API Key\n` +
             `- **rotate <平台>**: 轮换 API Key\n\n` +
             `### 自然语言示例\n\n` +
             `- "帮我注册 Claude Code"\n` +
             `- "查看已配置的编程助手"\n` +
             `- "哪个平台最便宜？"\n` +
             `- "配置 GitHub Copilot"\n`;
  }
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const action = args[0] || 'help';
  const params = {};
  
  if (args[1]) {
    if (args[1].startsWith('--')) {
      // 解析命名参数
      for (let i = 1; i < args.length; i += 2) {
        const key = args[i].replace('--', '');
        const value = args[i + 1];
        params[key] = value;
      }
    } else {
      params.platform = args[1];
    }
  }

  const result = main(action, params);
  console.log(result);
}

// 导出模块
module.exports = {
  main,
  checkPlatformStatus,
  getAllPlatformsStatus,
  generateRegisterGuide,
  comparePricing,
  getCredential,
  saveCredential,
  maskKey
};
