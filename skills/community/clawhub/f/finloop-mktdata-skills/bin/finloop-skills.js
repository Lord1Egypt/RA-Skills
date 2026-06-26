#!/usr/bin/env node

const { installSkill, listSkills } = require('../lib/install');

const args = process.argv.slice(2);
const binName = require('path').basename(process.argv[1], '.js');

function getHelp() {
  return `
📦 Finloop Skills 安装工具

用法:
  npx ${binName} <command> [options]

命令:
  list                    列出所有可用的 skills
  install <skill-id>       安装指定的 skill
  help                    显示帮助信息

示例:
  npx ${binName} list
  npx ${binName} install finloop-news-skill
  npx ${binName} install finloop-mktdata-skill
`;
}

async function main() {
  try {
    if (args.length === 0 || args[0] === 'help' || args[0] === '--help' || args[0] === '-h') {
      console.log(getHelp());
      return;
    }

    const command = args[0];

    if (command === 'list') {
      await listSkills(binName);
    } else if (command === 'install') {
      if (args.length < 2) {
        console.error('❌ 错误: 请指定要安装的 skill ID');
        console.log(`\n💡 使用 "npx ${binName} list" 查看可用的 skills`);
        process.exit(1);
      }
      const skillId = args[1];
      await installSkill(skillId);
    } else {
      console.error(`❌ 未知命令: ${command}`);
      console.log(`\n💡 使用 "npx ${binName} help" 查看帮助信息`);
      process.exit(1);
    }
  } catch (error) {
    console.error(`\n❌ 错误: ${error.message}`);
    process.exit(1);
  }
}

main();
