/**
 * 配置读取模块
 * 按照优先级读取配置：注入参数 > 环境变量
 */

function getConfig() {
  const apiKey = process.env.OPENCLAW_SKILL_CLAWPARTY_REPORTER_APIKEY
    || process.env.CLAWPARTY_API_KEY;

  const communityUrl = process.env.CLAWPARTY_COMMUNITY_URL
    || 'https://clawparty.club';

  const agentName = process.env.OPENCLAW_AGENT_NAME
    || process.env.OPENCLAW_SKILL_CLAWPARTY_REPORTER_AGENT_NAME
    || 'Anonymous Agent';

  return {
    apiKey,
    communityUrl: communityUrl.replace(/\/$/, ''), // 移除末尾斜杠
    agentName
  };
}

function validateConfig(config) {
  if (!config.apiKey) {
    throw new Error(
      'Missing API key. Please configure via:\n' +
      '  openclaw config set skills.entries.clawparty-reporter.apiKey "claw_xxx"\n' +
      'Or set environment variable OPENCLAW_SKILL_CLAWPARTY_REPORTER_APIKEY or CLAWPARTY_API_KEY'
    );
  }

  if (!config.apiKey.startsWith('claw_')) {
    console.warn('[clawparty-reporter] Warning: API key should start with "claw_"');
  }
}

module.exports = {
  getConfig,
  validateConfig
};
