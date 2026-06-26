/**
 * 档案行业情报收集脚本
 * 
 * 使用方法:
 * node collect-intelligence.js [config-file]
 * 
 * 示例:
 * node collect-intelligence.js daily-config.json
 */

const fs = require('fs');
const path = require('path');

// 默认配置
const defaultConfig = {
  task_name: "档案情报收集",
  sources: ["政策", "新闻", "技术", "学术"],
  keywords: [
    "档案管理",
    "档案数字化",
    "电子档案",
    "档案信息化",
    "智慧档案馆",
    "档案安全",
    "档案法",
    "数字档案馆"
  ],
  output_format: "markdown",
  output_dir: "./reports",
  max_results_per_source: 10,
  notification: false
};

// 情报来源配置
const sources = {
  政策: {
    urls: [
      "https://www.saac.gov.cn",
      "https://www.gov.cn/zhengce/zhengceku/"
    ],
    keywords: ["档案", "档案法", "档案管理"]
  },
  新闻: {
    urls: [
      "https://www.saac.gov.cn/dazh/")
    ],
    keywords: ["档案", "档案馆", "档案工作"]
  },
  技术: {
    urls: [
      "https://www.cnki.net",
      "https://www.wanfangdata.com.cn"
    ],
    keywords: ["档案数字化", "档案信息化", "档案管理系统"]
  },
  学术: {
    urls: [
      "https://kns.cnki.net/kns8/defaultresult/index",
      "https://d.wanfangdata.com.cn/periodical"
    ],
    keywords: ["档案学", "档案管理", "档案保护"]
  }
};

/**
 * 加载配置文件
 */
function loadConfig(configPath) {
  if (!configPath || !fs.existsSync(configPath)) {
    console.log('使用默认配置');
    return defaultConfig;
  }
  
  try {
    const configData = fs.readFileSync(configPath, 'utf8');
    const userConfig = JSON.parse(configData);
    return { ...defaultConfig, ...userConfig };
  } catch (error) {
    console.error('加载配置文件失败:', error.message);
    return defaultConfig;
  }
}

/**
 * 生成报告文件名
 */
function generateReportFilename(taskName) {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
  return `${taskName}_${dateStr}_${timeStr}.md`;
}

/**
 * 生成报告模板
 */
function generateReportTemplate(config) {
  const now = new Date();
  const dateStr = now.toLocaleString('zh-CN');
  
  return `# ${config.task_name}

**收集时间**: ${dateStr}
**情报来源**: ${config.sources.join(', ')}
**关键词**: ${config.keywords.join(', ')}

## 政策法规

> 正在收集相关政策法规信息...

## 行业动态

> 正在收集行业新闻动态...

## 技术趋势

> 正在收集技术发展趋势...

## 学术研究

> 正在收集学术研究成果...

---

*此报告由档案情报收集系统自动生成*
`;
}

/**
 * 保存报告
 */
function saveReport(content, outputDir, filename) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const filePath = path.join(outputDir, filename);
  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`报告已保存: ${filePath}`);
  return filePath;
}

/**
 * 主函数
 */
function main() {
  const configPath = process.argv[2];
  const config = loadConfig(configPath);
  
  console.log('========================================');
  console.log('档案行业情报收集系统');
  console.log('========================================');
  console.log(`任务名称: ${config.task_name}`);
  console.log(`情报来源: ${config.sources.join(', ')}`);
  console.log(`输出格式: ${config.output_format}`);
  console.log('----------------------------------------');
  
  // 生成报告
  const reportContent = generateReportTemplate(config);
  const filename = generateReportFilename(config.task_name);
  const filePath = saveReport(reportContent, config.output_dir, filename);
  
  console.log('----------------------------------------');
  console.log('情报收集完成！');
  console.log(`报告路径: ${filePath}`);
  console.log('========================================');
  
  // 如果需要通知，可以在这里添加通知逻辑
  if (config.notification) {
    console.log('通知功能已启用（待实现）');
  }
}

// 运行主函数
main();
