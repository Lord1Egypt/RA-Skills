#!/usr/bin/env node
const { program } = require('commander');
const fs = require('fs');
const yaml = require('yaml');

program
  .name('feishu-auto-reply')
  .description('飞书消息自动回复机器人');

// 加载配置文件
function loadConfig(configPath) {
  if (!fs.existsSync(configPath)) {
    throw new Error(`配置文件不存在: ${configPath}`);
  }
  const content = fs.readFileSync(configPath, 'utf8');
  return yaml.parse(content);
}

// 测试规则匹配
function testRule(message, rule) {
  switch (rule.match || 'contains') {
    case 'contains':
      return message.includes(rule.keyword);
    case 'exact':
      return message === rule.keyword;
    case 'regex':
      return new RegExp(rule.regex).test(message);
    case 'startsWith':
      return message.startsWith(rule.keyword);
    case 'endsWith':
      return message.endsWith(rule.keyword);
    default:
      return false;
  }
}

// 检查是否在工作时间
function isWorkingHours(workingHoursConfig) {
  if (!workingHoursConfig) return true;
  
  const now = new Date();
  const dayOfWeek = now.getDay(); // 0 = Sunday, 6 = Saturday
  
  // 排除周末
  if (workingHoursConfig.exclude_weekends && (dayOfWeek === 0 || dayOfWeek === 6)) {
    return false;
  }
  
  const currentTime = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
  
  // 检查时间段
  if (Array.isArray(workingHoursConfig)) {
    for (const period of workingHoursConfig) {
      if (typeof period === 'string' && period.includes('-')) {
        const [start, end] = period.split('-');
        if (currentTime >= start && currentTime <= end) {
          return true;
        }
      }
    }
  }
  
  return false;
}

program
  .command('test')
  .description('测试规则匹配')
  .option('--message <text>', '测试消息内容')
  .option('--config <path>', '配置文件路径', './config.yaml')
  .action(async (options) => {
    try {
      const config = loadConfig(options.config);
      console.log('🔍 测试规则匹配...');
      console.log(`消息内容: ${options.message}`);
      
      if (!isWorkingHours(config.working_hours)) {
        console.log('⏰ 当前不在工作时间，不会自动回复');
        return;
      }
      
      let matched = false;
      for (const rule of config.rules || []) {
        if (testRule(options.message, rule)) {
          console.log(`✅ 匹配到规则: ${rule.keyword || rule.regex}`);
          console.log(`📝 回复内容: ${rule.reply}`);
          matched = true;
          break;
        }
      }
      
      if (!matched) {
        console.log('❌ 没有匹配到任何规则');
      }
      
    } catch (error) {
      console.error('❌ 测试失败:', error.message);
      process.exit(1);
    }
  });

program
  .command('start')
  .description('启动自动回复服务')
  .option('--config <path>', '配置文件路径', './config.yaml')
  .action(async (options) => {
    try {
      const config = loadConfig(options.config);
      console.log('🚀 启动飞书自动回复机器人...');
      console.log(`✅ 加载配置成功，共 ${config.rules?.length || 0} 条规则`);
      
      // 这里需要对接飞书消息事件订阅
      // 实际实现需要配合 OpenClaw 的事件系统
      console.log('⚠️  消息事件订阅功能开发中，即将推出...');
      console.log('目前版本仅支持规则测试功能');
      
    } catch (error) {
      console.error('❌ 启动失败:', error.message);
      process.exit(1);
    }
  });

program
  .command('init')
  .description('生成示例配置文件')
  .option('--output <path>', '输出路径', './config.yaml')
  .action((options) => {
    const exampleConfig = `# 飞书自动回复配置示例
rules:
  - keyword: "你好"
    reply: "你好！我是自动回复机器人，有什么可以帮你的？"
    match: contains  # 匹配方式: contains/exact/startsWith/endsWith/regex
    only_mention: false  # 是否只有被@才回复
  
  - regex: "^(请假|休假|年假)"
    reply: "请假请直接联系人事部门，审批流程请查看内部文档。"
    match: regex
    only_mention: true
  
  - keyword: "谢谢"
    reply: "不客气，很高兴能帮到你！"
    match: contains

# 工作时间配置，只有在工作时间内才会自动回复
working_hours:
  - "9:00-12:30"
  - "14:00-18:00"
  exclude_weekends: true  # 周末不回复
`;
    
    fs.writeFileSync(options.output, exampleConfig);
    console.log(`✅ 示例配置文件已生成: ${options.output}`);
    console.log('请编辑配置文件后使用');
  });

program.parse();
