/**
 * 日报/周报生成器
 * 根据工作内容自动生成结构化日报/周报
 */

function generateDailyReport(input, options = {}) {
  const {
    type = 'daily',    // daily | weekly
    format = 'general', // general | military | simple | detailed
    name = '（姓名）',
    department = '（部门）',
    project = '（项目）',
    date = new Date().toISOString().slice(0, 10)
  } = options;

  const {
    completed = [],
    inProgress = [],
    tomorrow = [],
    problems = [],
    notes = ''
  } = input;

  let report = '';

  if (format === 'military') {
    report = generateMilitaryFormat(type, { name, department, project, date, completed, inProgress, tomorrow, problems, notes });
  } else if (format === 'simple') {
    report = generateSimpleFormat(type, { date, completed, tomorrow, problems });
  } else if (format === 'detailed') {
    report = generateDetailedFormat(type, { name, department, project, date, completed, inProgress, tomorrow, problems, notes });
  } else {
    report = generateGeneralFormat(type, { name, department, project, date, completed, inProgress, tomorrow, problems, notes });
  }

  return report;
}

function generateGeneralFormat(type, data) {
  const { name, department, project, date, completed, inProgress, tomorrow, problems } = data;
  const title = type === 'daily' ? '工 作 日 报' : '工 作 周 报';
  
  let report = `${title}\n`;
  report += `${'─'.repeat(40)}\n`;
  report += `日期：${date}\n`;
  report += `姓名：${name}\n`;
  report += `部门：${department}\n`;
  report += `项目：${project}\n\n`;

  report += `【已完成】\n`;
  if (completed.length === 0) {
    report += `- （无）\n`;
  } else {
    completed.forEach((item, i) => {
      report += `${i + 1}. ${item}\n`;
    });
  }
  report += `\n`;

  report += `【进行中】\n`;
  if (inProgress.length === 0) {
    report += `- （无）\n`;
  } else {
    inProgress.forEach((item, i) => {
      report += `${i + 1}. ${item}\n`;
    });
  }
  report += `\n`;

  report += `【${type === 'daily' ? '明日计划' : '下周计划'}】\n`;
  if (tomorrow.length === 0) {
    report += `- （无明确计划）\n`;
  } else {
    tomorrow.forEach((item, i) => {
      report += `${i + 1}. ${item}\n`;
    });
  }
  report += `\n`;

  report += `【问题与风险】\n`;
  if (problems.length === 0) {
    report += `- （无）\n`;
  } else {
    problems.forEach((item, i) => {
      report += `⚠️ ${item}\n`;
    });
  }

  return report;
}

function generateMilitaryFormat(type, data) {
  const { name, department, project, date, completed, inProgress, tomorrow, problems, notes } = data;
  const title = type === 'daily' ? '军品项目工作日报' : '军品项目工作周报';
  
  let report = `${'═'.repeat(50)}\n`;
  report += `          ${title}\n`;
  report += `${'═'.repeat(50)}\n\n`;
  
  report += `【基本信息】\n`;
  report += `├── 日期：${date}\n`;
  report += `├── 姓名：${name}\n`;
  report += `├── 部门：${department}\n`;
  report += `├── 项目名称：${project}\n`;
  report += `├── 技术状态：${completed.length > 0 ? '设计阶段' : '（待填写）'}\n`;
  report += `└── 质量记录编号：QR-${date.replace(/-/g, '')}-001\n\n`;

  report += `【已完成工作】\n`;
  if (completed.length === 0) {
    report += `（无）\n`;
  } else {
    completed.forEach((item, i) => {
      report += `${i + 1}. ${item}\n`;
      if (item.includes('仿真') || item.includes('设计')) {
        report += `   └─ 依据：GJB9001C-2017 §7.3\n`;
      }
      if (item.includes('评审') || item.includes('评审会')) {
        report += `   └─ 记录：设计评审报告 DR-${date.replace(/-/g, '')}-${String(i + 1).padStart(2, '0')}\n`;
      }
    });
  }
  report += `\n`;

  report += `【进行中工作】\n`;
  if (inProgress.length === 0) {
    report += `（无）\n`;
  } else {
    inProgress.forEach((item, i) => {
      report += `${i + 1}. ${item}\n`;
    });
  }
  report += `\n`;

  report += `【下一步计划】\n`;
  if (tomorrow.length === 0) {
    report += `（无明确计划）\n`;
  } else {
    tomorrow.forEach((item, i) => {
      report += `${i + 1}. ${item}\n`;
    });
  }
  report += `\n`;

  report += `【问题/风险/需支持事项】\n`;
  if (problems.length === 0) {
    report += `（无）\n`;
  } else {
    problems.forEach((item, i) => {
      report += `⚠️ ${i + 1}. ${item}\n`;
    });
  }
  report += `\n`;

  report += `【备注】\n`;
  report += `${notes || '（无）'}\n\n`;

  report += `${'─'.repeat(50)}\n`;
  report += `编制：${name}    审核：___________    批准：___________\n`;
  report += `日期：${date}\n`;
  report += `${'═'.repeat(50)}\n`;

  return report;
}

function generateSimpleFormat(type, data) {
  const { date, completed, tomorrow, problems } = data;
  let report = `# ${type === 'daily' ? '日报' : '周报'} ${date}\n\n`;
  report += `## ✅ 完成\n`;
  completed.forEach(item => { report += `- ${item}\n`; });
  report += `\n## 📋 计划\n`;
  tomorrow.forEach(item => { report += `- ${item}\n`; });
  if (problems.length > 0) {
    report += `\n## ⚠️ 问题\n`;
    problems.forEach(item => { report += `- ${item}\n`; });
  }
  return report;
}

function generateDetailedFormat(type, data) {
  return generateGeneralFormat(type, data); // 详细格式同通用格式
}

// CLI
const args = process.argv.slice(2);
if (args.length > 0) {
  try {
    const { input, options } = JSON.parse(args.join(' '));
    console.log(generateDailyReport(input, options));
  } catch (e) {
    console.log('用法: node generator.js \'{"completed":["任务1"],"inProgress":["任务2"],"tomorrow":["计划1"],"problems":["问题1"]}\' \'{"type":"daily","format":"military","name":"张三"}\'');
  }
}

module.exports = { generateDailyReport };
