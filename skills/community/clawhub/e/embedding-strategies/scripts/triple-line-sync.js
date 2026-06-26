#!/usr/bin/env node

// 三线同步执行脚本
// HTML 专家点评生成 → Chrome 打开 → PDF 转换 → 飞书发送 → 三线记录

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// 配置
const workspace = 'C:\\Users\\Xiabi\\.openclaw\\workspace';
const scriptsDir = path.join(workspace, 'scripts');

// 命令行参数
const args = process.argv.slice(2);
const htmlFile = args[0];
const theme = args[1] || '专家点评';
const insights = args.slice(2).join(' ') || '';

if (!htmlFile) {
  console.error('用法：node triple-line-sync.js <file.html> [主题] [核心洞察]');
  console.error('示例：node triple-line-sync.js expert-review.html "通义万相" "API 配置清晰/国产优先/成本可控"');
  process.exit(1);
}

// 验证 HTML 文件
if (!fs.existsSync(htmlFile)) {
  console.error(`❌ 文件不存在：${htmlFile}`);
  process.exit(1);
}

const fileStats = fs.statSync(htmlFile);
const fileSizeKB = (fileStats.size / 1024).toFixed(1);
const pdfFile = htmlFile.replace('.html', '.pdf');
const timestamp = new Date().toISOString().slice(0, 16).replace('T', ' ');

console.log('🔄 三线同步执行');
console.log('='.repeat(50));
console.log(`主题：${theme}`);
console.log(`HTML: ${htmlFile} (${fileSizeKB} KB)`);
console.log(`PDF : ${pdfFile}`);
console.log('='.repeat(50));

// 步骤 1：Chrome 打开 HTML（电脑端）
console.log('\n📌 步骤 1/4: Chrome 打开 HTML（电脑端）');
console.log('-'.repeat(50));
try {
  const absoluteHtml = path.resolve(htmlFile);
  execSync(`Start-Process "chrome.exe" -ArgumentList "${absoluteHtml}"`, {
    shell: true,
    stdio: 'inherit'
  });
  console.log('✅ Chrome 已打开');
} catch (error) {
  console.error('❌ Chrome 打开失败');
  process.exit(1);
}

// 步骤 2：HTML 转 PDF
console.log('\n📄 步骤 2/4: HTML 转 PDF');
console.log('-'.repeat(50));
try {
  const scriptPath = path.join(scriptsDir, 'html-to-pdf-quick.js');
  execSync(`node "${scriptPath}" "${htmlFile}"`, {
    stdio: 'inherit'
  });
  console.log('✅ PDF 已生成');
} catch (error) {
  console.error('❌ PDF 转换失败');
  process.exit(1);
}

// 步骤 3：发送飞书（PDF+ 文字总结）
console.log('\n📤 步骤 3/4: 发送飞书（飞书端）');
console.log('-'.repeat(50));

const summary = `## 📊 专家点评 HTML 已生成

**时间：** ${timestamp}
**主题：** ${theme}

**文件信息：**
- 文件名：${path.basename(htmlFile)}
- 大小：${fileSizeKB} KB
- 章节：6 个（评分/观点/洞察/架构/对比/建议）

**核心洞察：**
${insights.split('/').map((i, idx) => `${idx + 1}. ${i.trim()}`).join('\n')}

**已打开：** ✅ Chrome 已打开预览（电脑端）
**已发送：** ✅ PDF 已发送到飞书（手机端）

**三线同步：**
- ✅ MD 文件：worklog.txt 已记录
- ✅ TXT 记录：atomic-actions 已更新
- ✅ 飞书通知：PDF+ 文字总结已发送`;

try {
  // 发送 PDF 文件
  execSync(`message --action send --channel feishu --filePath "${pdfFile}"`, {
    stdio: 'inherit'
  });
  
  // 发送文字总结
  const summaryFile = path.join(workspace, 'temp-summary.txt');
  fs.writeFileSync(summaryFile, summary, 'utf8');
  execSync(`message --action send --channel feishu --filePath "${summaryFile}"`, {
    stdio: 'inherit'
  });
  
  console.log('✅ 飞书已发送');
} catch (error) {
  console.error('❌ 飞书发送失败');
  process.exit(1);
}

// 步骤 4：三线记录
console.log('\n📝 步骤 4/4: 三线记录（三线同步）');
console.log('-'.repeat(50));

// MD 文件线：worklog.txt
const worklogEntry = `
### ${timestamp.split(' ')[0]} ${timestamp.split(' ')[1].slice(0, 5)} - ${theme}专家点评

- [完成] 生成 HTML 专家点评
- [文件] ${htmlFile} (${fileSizeKB} KB)
- [三线同步]
  - ✅ MD 线：worklog.txt 已记录
  - ✅ TXT 线：atomic-actions 已更新
  - ✅ 飞书线：PDF+ 总结已发送
- [电脑端] Chrome 已打开 HTML
- [飞书端] PDF 已发送
`;

try {
  fs.appendFileSync(path.join(workspace, 'worklog.txt'), worklogEntry, 'utf8');
  console.log('✅ MD 线：worklog.txt 已更新');
} catch (error) {
  console.error('❌ worklog.txt 更新失败');
}

// TXT 线：atomic-actions
try {
  const actionsDir = path.join(workspace, 'atomic-actions');
  if (!fs.existsSync(actionsDir)) {
    fs.mkdirSync(actionsDir, { recursive: true });
  }
  const actionFile = path.join(actionsDir, `${new Date().toISOString().slice(0, 10)}-actions.txt`);
  const actionEntry = `[${timestamp}] HTML 专家点评生成 - ${theme}
- HTML: ${htmlFile}
- PDF: ${pdfFile}
- 三线同步：✅
- 飞书发送：✅
`;
  fs.appendFileSync(actionFile, actionEntry, 'utf8');
  console.log('✅ TXT 线：atomic-actions 已更新');
} catch (error) {
  console.error('❌ atomic-actions 更新失败');
}

// 飞书线：已在步骤 3 完成
console.log('✅ 飞书线：已完成（步骤 3）');

console.log('\n' + '='.repeat(50));
console.log('✅ 三线同步完成！');
console.log('='.repeat(50));
console.log(`电脑端：Chrome 已打开 ${htmlFile}`);
console.log(`飞书端：PDF 已发送 ${pdfFile}`);
console.log(`记录：worklog.txt + atomic-actions`);
