/**
 * Garmin Sync Skill - International → China Account
 * Uses Python garminconnect library for actual Garmin API interaction.
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const SCRIPT = path.join(__dirname, 'scripts', 'garmin_sync.py');
const STATE_FILE = path.join(
  process.env.GARMIN_SYNC_DIR || path.join(require('os').homedir(), '.garmin-sync'),
  'sync-state.json'
);

/**
 * Build env for the Python script, merging process env with Garmin config.
 */
function buildEnv() {
  return {
    ...process.env,
    GARMIN_INTL_USERNAME: process.env.GARMIN_INTL_USERNAME || '',
    GARMIN_INTL_PASSWORD: process.env.GARMIN_INTL_PASSWORD || '',
    GARMIN_CN_USERNAME: process.env.GARMIN_CN_USERNAME || '',
    GARMIN_CN_PASSWORD: process.env.GARMIN_CN_PASSWORD || '',
    GARMIN_SYNC_DIR: process.env.GARMIN_SYNC_DIR || '',
    GARMIN_TOKEN_DIR: process.env.GARMIN_TOKEN_DIR || '',
    PYTHONUNBUFFERED: '1',
  };
}

function runPython(args = []) {
  try {
    const env = buildEnv();
    const output = execSync(`python3 "${SCRIPT}" ${args.join(' ')}`, {
      env,
      cwd: __dirname,
      timeout: 300000, // 5 min for sync operations
      maxBuffer: 10 * 1024 * 1024,
    });
    return { success: true, output: output.toString() };
  } catch (error) {
    return {
      success: false,
      output: error.stdout?.toString() || '',
      error: error.stderr?.toString() || error.message,
    };
  }
}

/**
 * Check if Garmin credentials are configured.
 */
function checkConfig() {
  const intlUser = process.env.GARMIN_INTL_USERNAME;
  const intlPass = process.env.GARMIN_INTL_PASSWORD;
  const cnUser = process.env.GARMIN_CN_USERNAME;
  const cnPass = process.env.GARMIN_CN_PASSWORD;

  if (!intlUser || !intlPass || !cnUser || !cnPass) {
    return {
      configured: false,
      message: [
        '❌ Garmin 账号未配置，请设置以下环境变量:',
        '',
        '```',
        'GARMIN_INTL_USERNAME=your_intl@email.com',
        'GARMIN_INTL_PASSWORD=***',
        'GARMIN_CN_USERNAME=your_cn@email.com',
        'GARMIN_CN_PASSWORD=***',
        '```',
        '',
        '或用 OpenClaw 配置:',
        '`openclaw config set env.GARMIN_INTL_USERNAME your@email.com`',
      ].join('\n'),
    };
  }

  return { configured: true };
}

/**
 * Parse input to determine command.
 */
function parseInput(input) {
  if (typeof input === 'string') {
    const cmd = input.trim().toLowerCase();
    if (['sync', 'status', 'list', 'auth-test', 'test_auth'].includes(cmd)) {
      return { command: cmd === 'test_auth' ? 'auth-test' : cmd, params: {} };
    }
    // Default to status
    return { command: 'status', params: {} };
  }

  if (typeof input === 'object') {
    const { command = 'status', ...params } = input;
    return { command: command.toLowerCase(), params };
  }

  return { command: 'status', params: {} };
}

/**
 * Main handler called by OpenClaw.
 */
async function handler(input) {
  const { command, params } = parseInput(input);
  const config = checkConfig();

  if (!config.configured) {
    return config.message;
  }

  const days = params.days || params.days_back || 7;
  const maxActivities = params.max || params.max_activities || 10;

  try {
    let result;

    switch (command) {
      case 'auth-test': {
        result = runPython(['auth-test']);
        if (result.success) {
          return '✅ **Garmin 账号认证测试通过！**\n\n国际版和国内版账号均可正常登录。';
        }
        return `❌ **认证测试失败**\n\`\`\`\n${result.error || result.output}\n\`\`\``;
      }

      case 'list': {
        result = runPython(['list', `--days=${days}`]);
        if (result.success) {
          // Return the raw log output
          return `📋 **最近 ${days} 天的活动**\n\`\`\`\n${result.output.trim()}\n\`\`\``;
        }
        return `❌ 获取活动列表失败:\n\`\`\`\n${result.error}\n\`\`\``;
      }

      case 'sync': {
        result = runPython(['sync', `--days=${days}`, `--max=${maxActivities}`]);
        // Extract the summary from output
        if (result.success) {
          const lines = result.output.trim().split('\n');
          const summary = lines.filter(l => l.includes('Sync complete') || l.includes('No new'));
          const detailLines = lines.filter(l => l.includes('[%]') || l.includes('✅') || l.includes('❌'));
          return [
            '🔄 **Garmin 数据同步完成**',
            '',
            '```',
            ...(summary.length ? summary : lines.slice(-5)),
            '```',
            '',
            '💡 提示: 使用 `status` 查看详细同步状态',
          ].join('\n');
        }
        return `❌ **同步失败**\n\`\`\`\n${result.error || result.output.slice(-500)}\n\`\`\``;
      }

      case 'status':
      default: {
        result = runPython(['status']);
        if (result.success) {
          const lines = result.output.trim().split('\n');
          return [
            '📊 **Garmin 同步状态**',
            '',
            '```',
            ...lines,
            '```',
          ].join('\n');
        }
        // Still show something useful
        return '📊 **Garmin 同步状态**\n\n尚未运行过同步。请先运行 `sync` 或 `auth-test`。';
      }
    }
  } catch (error) {
    return `❌ 执行失败: ${error.message}`;
  }
}

/**
 * Get skill info.
 */
function getInfo() {
  return {
    name: 'garmin-sync',
    description: '佳明国际账号数据同步到国内账号',
    version: '2.0.0',
    commands: ['sync', 'status', 'list', 'auth-test'],
    config: {
      env: {
        GARMIN_INTL_USERNAME: { required: true, desc: '国际版邮箱' },
        GARMIN_INTL_PASSWORD: { required: true, desc: '国际版密码' },
        GARMIN_CN_USERNAME: { required: true, desc: '国内版邮箱' },
        GARMIN_CN_PASSWORD: { required: true, desc: '国内版密码' },
      },
    },
  };
}

module.exports = { handler, getInfo };
