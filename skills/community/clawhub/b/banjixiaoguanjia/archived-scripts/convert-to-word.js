/**
 * 生成小米课内作业分析的 Word 文档
 */

const fs = require('fs');
const path = require('path');

// 读取已有的分析结果
const courseName = '一下(第9节)';
const studentName = '小米';
const homeworkType = '课内';

const txtPath = path.join(require('os').homedir(), 'Desktop', courseName, `${courseName}${studentName}${homeworkType}分析.txt`);
const docxPath = path.join(require('os').homedir(), 'Desktop', courseName, `${courseName}${studentName}${homeworkType}分析.docx`);

if (!fs.existsSync(txtPath)) {
  console.log('未找到分析结果文件');
  process.exit(1);
}

const content = fs.readFileSync(txtPath, 'utf-8');

// 创建简单的 Word 文档（使用 HTML 格式，Word 可以打开）
const htmlContent = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>${courseName}${studentName}${homeworkType}作业分析</title>
  <style>
    body { font-family: "Microsoft YaHei", SimSun, sans-serif; line-height: 1.8; padding: 40px; }
    h1 { text-align: center; font-size: 24px; margin-bottom: 30px; }
    h2 { font-size: 18px; margin-top: 25px; margin-bottom: 15px; color: #333; }
    p { margin: 10px 0; }
    .correct { color: green; }
    .wrong { color: red; }
    .unknown { color: orange; }
  </style>
</head>
<body>
  <h1>${courseName} ${studentName} ${homeworkType}作业分析报告</h1>
  <pre style="white-space: pre-wrap; font-family: inherit;">${content.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
</body>
</html>`;

// 保存为 HTML 文件（Word 可以直接打开并另存为 docx）
const htmlPath = path.join(require('os').homedir(), 'Desktop', courseName, `${courseName}${studentName}${homeworkType}分析.html`);
fs.writeFileSync(htmlPath, htmlContent, 'utf-8');

console.log(`HTML 报告已生成: ${htmlPath}`);
console.log('可以用 Word 打开此 HTML 文件，然后另存为 .docx 格式');

// 同时尝试使用 Python 生成真正的 docx
try {
  const { execSync } = require('child_process');
  
  const pythonScript = `
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# 添加标题
title = doc.add_heading('${courseName} ${studentName} ${homeworkType}作业分析报告', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 添加内容
content = """${content.replace(/"/g, '\\"').replace(/'/g, "\\'")}"""

# 按段落添加
for line in content.split('\\n'):
    if line.strip():
        if line.startswith('**') and line.endswith('**'):
            # 标题
            p = doc.add_heading(line.strip('*'), level=2)
        elif line.startswith('第') and '题' in line:
            # 题目
            p = doc.add_paragraph(line)
            if '正确' in line:
                p.runs[0].font.color.rgb = RGBColor(0, 128, 0)
            elif '错误' in line:
                p.runs[0].font.color.rgb = RGBColor(255, 0, 0)
        else:
            p = doc.add_paragraph(line)

# 保存
doc.save(r'${docxPath}')
print('Word 文档已生成: ${docxPath}')
`;

  const tempPy = path.join(require('os').homedir(), 'Desktop', courseName, '_to_docx.py');
  fs.writeFileSync(tempPy, pythonScript, 'utf-8');
  
  execSync(`python3 "${tempPy}"`, { encoding: 'utf-8', timeout: 60000 });
  fs.unlinkSync(tempPy);
  
  console.log(`Word 文档已生成: ${docxPath}`);
  
} catch (error) {
  console.log('生成 Word 文档失败（可能需要安装 python-docx）:', error.message);
  console.log('已生成 HTML 版本，可用 Word 打开');
}
