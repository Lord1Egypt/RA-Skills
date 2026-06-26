#!/usr/bin/env node
/**
 * ClawGuard v3 - Shield CLI
 * 主动护盾：提示词注入防护、意图验证、加固建议
 */

const { Shield } = require('./src/shield.js');

const args = process.argv.slice(2);
const commands = {
  defend: args.includes('defend') || args.includes('--defend'),
  harden: args.includes('harden') || args.includes('--harden'),
  fix: args.includes('fix') || args.includes('--fix'),
  validate: args.includes('validate') || args.includes('--validate')
};

// 找到 defend 命令后的文本参数
function findTextArg(args, command) {
  const cmdIndex = args.indexOf(command);
  if (cmdIndex >= 0 && cmdIndex < args.length - 1) {
    const nextArg = args[cmdIndex + 1];
    if (nextArg && !nextArg.startsWith('--')) {
      return nextArg;
    }
  }
  return null;
}

const options = {
  input: findTextArg(args, 'defend') || findTextArg(args, 'validate') || null,
  output: args.find(a => args[args.indexOf(a) - 1] === '--output') || null,
  config: args.find(a => args[args.indexOf(a) - 1] === '--config') || null
};

async function main() {
  const shield = new Shield();

  if (!commands.defend && !commands.harden && !commands.fix && !commands.validate) {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║         🛡️ ClawGuard v3 - Shield (主动护盾)          ║
╠═══════════════════════════════════════════════════════════════╣
║  命令:                                                     ║
║    defend <text>      检测文本中的注入攻击                  ║
║    harden <file>      生成加固配置                          ║
║    fix <file>         一键修复配置                          ║
║    validate <file>    验证意图完整性                        ║
║                                                               ║
║  选项:                                                      ║
║    --output <path>    输出文件路径                           ║
║    --config <path>    配置文件路径                          ║
╚═══════════════════════════════════════════════════════════════╝
    `);
    process.exit(0);
  }

  console.log('🛡️ Shield 启动中...\n');

  if (commands.defend) {
    const text = options.input || await readStdin();
    const result = shield.detectPromptInjection(text);
    shield.printDefenseResult(result);
  } else if (commands.validate) {
    const text = options.input || await readStdin();
    const result = shield.validateIntentIntegrity(text);
    shield.printValidationResult(result);
  } else if (commands.harden || commands.fix) {
    const configPath = options.input || process.env.OPENCLAW_CONFIG;
    if (!configPath) {
      console.error('❌ 请提供配置文件路径');
      process.exit(1);
    }
    const result = await shield.generateHardenedConfig(configPath);
    if (options.output) {
      require('fs').writeFileSync(options.output, JSON.stringify(result, null, 2));
      console.log(`\n✅ 加固配置已保存到: ${options.output}`);
    } else {
      shield.printHardeningReport(result);
    }
  }
}

async function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data.trim()));
  });
}

main().catch(err => {
  console.error('❌ Shield 错误:', err.message);
  process.exit(1);
});
