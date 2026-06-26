/**
 * 作业分析脚本 - 完整版
 * 支持批量分析和逐一分析（备用）
 * 自动生成 Word 报告（微软雅黑，优化排版）
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class HomeworkAnalyzer {
  constructor(options = {}) {
    // 直接从脚本中读取 API Key，不再依赖环境变量
    this.apiKey = options.apiKey || 'sk-14d72eaba86242d3ba368ee0c9b08dac';
    this.baseUrl = 'https://dashscope.aliyuncs.com/compatible-mode/v1';
    this.model = 'qwen-vl-max-latest';
  }

  /**
   * 分析学生作业
   * @param {string} courseName - 课程名称
   * @param {string} studentName - 学生姓名
   * @param {string} homeworkType - 作业类型（课内/奥数）
   */
  async analyze(courseName, studentName, homeworkType) {
    console.log(`\n========================================`);
    console.log(`分析: ${studentName} - ${homeworkType}作业`);
    console.log(`========================================\n`);

    // 1. 准备路径
    const studentDir = path.join(require('os').homedir(), 'Desktop', courseName, studentName, homeworkType);
    const answerPath = path.join(require('os').homedir(), 'Desktop', '答案', courseName, `${homeworkType}答案.png`);
    const outputDir = path.join(require('os').homedir(), 'Desktop', courseName);

    // 2. 检查答案文件
    const hasAnswer = fs.existsSync(answerPath);
    console.log(`答案文件: ${hasAnswer ? '存在' : '不存在'}`);

    // 3. 获取作业图片
    const homeworkFiles = fs.readdirSync(studentDir)
      .filter(f => f.endsWith('.jpg'))
      .map(f => path.join(studentDir, f))
      .sort();
    console.log(`作业图片: ${homeworkFiles.length} 张\n`);

    if (homeworkFiles.length === 0) {
      console.log('未找到作业图片');
      return;
    }

    // 4. 尝试批量分析
    let result = null;
    try {
      result = await this.analyzeBatch(studentName, homeworkType, homeworkFiles, answerPath, hasAnswer);
      console.log('✓ 批量分析成功\n');
    } catch (error) {
      console.log('批量分析失败，切换到逐一分析...\n');
      result = await this.analyzeOneByOne(studentName, homeworkType, homeworkFiles, answerPath, hasAnswer);
    }

    // 5. 保存 TXT
    const txtPath = path.join(outputDir, `${courseName}${studentName}${homeworkType}分析.txt`);
    fs.writeFileSync(txtPath, result, 'utf-8');
    console.log(`✓ TXT 已保存: ${txtPath}`);

    // 6. 生成 Word
    console.log('\n正在生成 Word 文档...');
    await this.generateWord(courseName, studentName, homeworkType, result, outputDir);
    console.log(`✓ Word 已保存: ${courseName}${studentName}${homeworkType}分析.docx`);

    return result;
  }

  /**
   * 批量分析
   */
  async analyzeBatch(studentName, homeworkType, homeworkFiles, answerPath, hasAnswer) {
    const imagePaths = hasAnswer ? [answerPath, ...homeworkFiles] : homeworkFiles;
    
    const prompt = this.buildPrompt(studentName, homeworkType, homeworkFiles.length, hasAnswer);
    
    const pythonScript = this.buildPythonScript(imagePaths, prompt);
    
    const tempScript = path.join(homeworkFiles[0], '..', '_analyze_batch.py');
    fs.writeFileSync(tempScript, pythonScript, 'utf-8');

    try {
      const result = execSync(`python3 "${tempScript}"`, { 
        encoding: 'utf-8',
        timeout: 300000
      });
      fs.unlinkSync(tempScript);
      return result.trim();
    } catch (error) {
      if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
      throw error;
    }
  }

  /**
   * 逐一分析（备用）
   */
  async analyzeOneByOne(studentName, homeworkType, homeworkFiles, answerPath, hasAnswer) {
    const analysisResults = [];

    for (let i = 0; i < homeworkFiles.length; i++) {
      console.log(`分析第 ${i + 1}/${homeworkFiles.length} 张...`);
      
      const imagePaths = hasAnswer ? [answerPath, homeworkFiles[i]] : [homeworkFiles[i]];
      
      const prompt = `帮我检查这张作业的对错。

**重要**：
1.要严谨仔细理解题目意思，确保判改作业的正确性(重要)。
2.要检查应用题答题中是否缺少单位。
3.应用题的答案需要有计算过程。
4.对的划对勾，错的划错号，看不清楚的用问号，作业中的漏答题做漏题标注。
5.答题的位置写的算式是错误的，算式要写在相应的答题位置。
7.不要使用"识别"这种计算机技术用语。
8.不要使用繁体字。

请按以下格式输出：
第${i + 1}张作业：
题目分析：...
批改结果：...（正确/错误/看不清楚/漏题）
学生答案：...
批改说明：...`;

      const pythonScript = this.buildPythonScript(imagePaths, prompt);
      
      const tempScript = path.join(homeworkFiles[i], '..', `_analyze_${i}.py`);
      fs.writeFileSync(tempScript, pythonScript, 'utf-8');

      try {
        const result = execSync(`python3 "${tempScript}"`, { 
          encoding: 'utf-8',
          timeout: 120000
        });
        fs.unlinkSync(tempScript);
        analysisResults.push(result.trim());
        console.log(`  ✓ 完成`);
      } catch (error) {
        if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
        console.log(`  ✗ 失败`);
        analysisResults.push(`第${i + 1}张作业：分析失败`);
      }
    }

    // 汇总
    return this.summarizeResults(studentName, homeworkType, homeworkFiles.length, analysisResults);
  }

  /**
   * 构建提示词
   */
  buildPrompt(studentName, homeworkType, count, hasAnswer) {
    let prompt = '';
    
    if (hasAnswer) {
      prompt += `第1张图片是${homeworkType}答案.png，这是作业的标准答案，你需要认真参考答案进行作业批改。\n\n`;
    }
    
    prompt += `帮我检查这些作业的对错，并根据学生的对错分析出该学生对于这个章节理解的薄弱环节与作业总结。对于看不清楚学生答案的按照错误处理，如果发现较多看不清楚学生手写答案那就要强调学生在作业书写规范上要重点加强(字迹潦草不算，因为孩子年龄不大)。

**重要**：
1.要严谨仔细理解题目意思，确保判改作业的正确性(重要)。
2.要检查应用题答题中是否缺少单位。
3.应用题的答案需要有计算过程。
4.对的划对勾，错的划错号，看不清楚的用问号，作业中的漏答题做漏题标注。
5.答题的位置写的算式是错误的，算式要写在相应的答题位置。
6.总结内容要语气话一些，但是要正式，要多维度总结。
7.不要使用"识别"这种计算机技术用语。
8.不要使用繁体字。

请按以下格式输出：
学生姓名：${studentName}
作业类型：${homeworkType}
作业图片数量：${count}张

逐题批改：
第1题：...（正确/错误/看不清楚/漏题）
...

薄弱环节分析：
...

作业总结：
...`;

    return prompt;
  }

  /**
   * 构建 Python 脚本
   */
  buildPythonScript(imagePaths, prompt) {
    const imageEncodings = imagePaths.map(imgPath => {
      const base64 = fs.readFileSync(imgPath, { encoding: 'base64' });
      return `"data:image/jpeg;base64,${base64}"`;
    });

    return `
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key="${this.apiKey}",
    base_url="${this.baseUrl}"
)

response = client.chat.completions.create(
    model="${this.model}",
    messages=[
        {
            "role": "user",
            "content": [
                ${imageEncodings.map(img => `{
                    "type": "image_url",
                    "image_url": {"url": ${img}}
                }`).join(',\n                ')},
                {
                    "type": "text",
                    "text": """${prompt}"""
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
`;
  }

  /**
   * 汇总逐一分析结果
   */
  summarizeResults(studentName, homeworkType, count, results) {
    const allResults = results.join('\n\n');
    
    const summaryPrompt = `基于以下各张作业的批改结果，生成完整的作业分析报告。

各张作业批改结果：
${allResults}

请按以下格式输出完整报告：
学生姓名：${studentName}
作业类型：${homeworkType}
作业图片数量：${count}张

逐题批改：
（列出每道题的批改结果）

薄弱环节分析：
根据学生的错题情况，分析该学生对于章节理解的薄弱环节。

作业总结：
语气正式但亲切，多维度总结学生的作业情况。如果发现较多无法识别学生手写答案，要强调学生在作业书写规范上要重点加强(字迹潦草不算，因为孩子年龄不大)。

**重要**：
1.总结内容要语气话一些，但是要正式，要多维度总结。
2.不要使用"识别"这种计算机技术用语。
3.不要使用繁体字。`;

    const pythonScript = `
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key="${this.apiKey}",
    base_url="${this.baseUrl}"
)

response = client.chat.completions.create(
    model="${this.model}",
    messages=[
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": """${summaryPrompt}"""
            }
        }
    ]
)

print(response.choices[0].message.content)
`;

    const tempScript = path.join(require('os').homedir(), 'Desktop', '_summarize.py');
    fs.writeFileSync(tempScript, pythonScript, 'utf-8');

    try {
      const result = execSync(`python3 "${tempScript}"`, { 
        encoding: 'utf-8',
        timeout: 120000
      });
      fs.unlinkSync(tempScript);
      return result.trim();
    } catch (error) {
      if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
      return allResults; // 如果汇总失败，返回原始结果
    }
  }

  /**
   * 生成 Word 文档（手机阅读优化版）
   */
  async generateWord(courseName, studentName, homeworkType, content, outputDir) {
    const docxPath = path.join(outputDir, `${courseName}${studentName}${homeworkType}分析.docx`);
    
    const pythonScript = `
# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()

# 设置窄边距，适合手机阅读
sections = doc.sections
for section in sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

# 设置默认字体
doc.styles['Normal'].font.name = '微软雅黑'
doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
doc.styles['Normal'].font.size = Pt(14)  # 手机阅读用大字体

# 标题
title = doc.add_heading('', level=0)
title_run = title.add_run('📚 ${studentName} ${homeworkType}作业分析')
title_run.font.name = '微软雅黑'
title_run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
title_run.font.size = Pt(20)  # 大标题
title_run.font.bold = True
title_run.font.color.rgb = RGBColor(0, 102, 204)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 副标题
subtitle = doc.add_paragraph()
subtitle_run = subtitle.add_run('${courseName}')
subtitle_run.font.name = '微软雅黑'
subtitle_run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
subtitle_run.font.size = Pt(12)
subtitle_run.font.color.rgb = RGBColor(128, 128, 128)
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()

# 解析内容
content = """${content.replace(/"/g, '\\"').replace(/'/g, "\\'")}"""
lines = content.split('\\n')

# 跳过基本信息行
skip_lines = ['学生姓名：', '作业类型：', '作业图片数量：']

for line in lines:
    line = line.strip()
    if not line:
        continue
    if any(line.startswith(s) for s in skip_lines):
        continue
    if line == '---':
        doc.add_paragraph()
        continue
    
    # 大章节标题（如：逐题批改、薄弱环节分析）
    if line.startswith('###') or (line.startswith('**') and '批改' in line) or (line.startswith('**') and '分析' in line) or (line.startswith('**') and '总结' in line):
        heading_text = line.strip('*#').strip()
        doc.add_paragraph()  # 前面空一行
        heading = doc.add_heading('', level=1)
        run = heading.add_run('▶ ' + heading_text)
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(16)  # 章节标题
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 102, 204)
        continue
    
    # 小节标题（如：第1题、第2课时）
    if (line.startswith('第') and ('题' in line or '课时' in line)) or line.startswith('**第'):
        clean_line = line.strip('*')
        doc.add_paragraph()  # 前面空一行
        p = doc.add_paragraph()
        
        # 提取题号和内容
        if '：' in clean_line or ':' in clean_line:
            sep = '：' if '：' in clean_line else ':'
            parts = clean_line.split(sep, 1)
            run1 = p.add_run(parts[0] + ' ')
            run1.font.name = '微软雅黑'
            run1._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
            run1.font.size = Pt(15)
            run1.font.bold = True
            run1.font.color.rgb = RGBColor(51, 51, 51)
            
            if len(parts) > 1:
                run2 = p.add_run(parts[1])
                run2.font.name = '微软雅黑'
                run2._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
                run2.font.size = Pt(14)
                # 根据内容设置颜色
                if '正确' in parts[1] or '✅' in parts[1]:
                    run2.font.color.rgb = RGBColor(0, 153, 0)
                elif '错误' in parts[1] or '❌' in parts[1]:
                    run2.font.color.rgb = RGBColor(204, 0, 0)
        else:
            run = p.add_run(clean_line)
            run.font.name = '微软雅黑'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
            run.font.size = Pt(15)
            run.font.bold = True
        continue
    
    # 数字列表项（如：1. 2. 3.）
    if len(line) > 2 and line[0].isdigit() and line[1] in ['.', '、']:
        p = doc.add_paragraph()
        num_text = line[0] + '. '
        content_text = line[2:].strip()
        
        run1 = p.add_run(num_text)
        run1.font.name = '微软雅黑'
        run1._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run1.font.size = Pt(14)
        run1.font.bold = True
        run1.font.color.rgb = RGBColor(0, 102, 204)
        
        run2 = p.add_run(content_text)
        run2.font.name = '微软雅黑'
        run2._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run2.font.size = Pt(14)
        continue
    
    # 子项（以-或•开头）
    if line.startswith('-') or line.startswith('•') or line.startswith('→'):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)  # 缩进
        run = p.add_run('  ' + line)
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(13)
        
        if '正确' in line or '✅' in line:
            run.font.color.rgb = RGBColor(0, 153, 0)
        elif '错误' in line or '❌' in line:
            run.font.color.rgb = RGBColor(204, 0, 0)
        continue
    
    # 普通段落
    p = doc.add_paragraph()
    run = p.add_run(line)
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(14)  # 手机阅读用大字体

# 页脚
doc.add_paragraph()
doc.add_paragraph()
footer = doc.add_paragraph('— 分析报告结束 —')
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in footer.runs:
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(153, 153, 153)

doc.save(r'${docxPath.replace(/\\/g, '\\\\')}')
print('Word文档已保存')
`;

    const tempScript = path.join(outputDir, '_generate_word.py');
    fs.writeFileSync(tempScript, pythonScript, 'utf-8');

    try {
      execSync(`python3 "${tempScript}"`, { encoding: 'utf-8', timeout: 60000 });
      fs.unlinkSync(tempScript);
    } catch (error) {
      if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
      throw error;
    }
  }
}

module.exports = { HomeworkAnalyzer };

// 如果直接运行
if (require.main === module) {
  const analyzer = new HomeworkAnalyzer();
  
  // 分析示例
  const courseName = process.argv[2] || '一下(第9节)';
  const studentName = process.argv[3] || '大瑀';
  const homeworkType = process.argv[4] || '课内';
  
  analyzer.analyze(courseName, studentName, homeworkType)
    .then(() => console.log('\n分析完成！'))
    .catch(console.error);
}
