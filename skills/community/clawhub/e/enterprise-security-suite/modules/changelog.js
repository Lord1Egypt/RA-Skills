/**
 * 变更日志模块
 */

const fs = require('fs');
const path = require('path');

async function logChange(options) {
  const { file, type, reason, executor = '用户', changelogPath = 'memory/CHANGELOG.md' } = options;
  
  try {
    const now = new Date();
    const timestamp = now.toISOString().slice(0, 16).replace('T', ' ');
    
    let entry = `\n## ${timestamp}\n\n`;
    entry += `### 修改文件：\`${file}\`\n`;
    entry += `- **操作类型**: ${type}\n`;
    entry += `- **修改原因**: ${reason}\n`;
    entry += `- **执行者**: ${executor}\n`;
    
    const fullChangelogPath = path.resolve(changelogPath);
    const dir = path.dirname(fullChangelogPath);
    
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    if (fs.existsSync(fullChangelogPath)) {
      fs.appendFileSync(fullChangelogPath, entry);
    } else {
      const header = `# CHANGELOG - 变更日志\n\n_所有高危/中危操作的完整记录_\n\n`;
      fs.writeFileSync(fullChangelogPath, header + entry);
    }
    
    console.log(`📝 已记录变更到 ${changelogPath}`);
    return true;
  } catch (error) {
    console.error(`❌ 记录变更失败：${error.message}`);
    return false;
  }
}

module.exports = {
  logChange
};
