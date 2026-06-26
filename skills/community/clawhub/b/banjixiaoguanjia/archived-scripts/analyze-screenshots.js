const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

async function analyzeScreenshots(courseName) {
  console.log('\n' + '='.repeat(60));
  console.log(`  AI 分析作业数量: ${courseName}`);
  console.log('='.repeat(60) + '\n');

  const desktopDir = path.join(require('os').homedir(), 'Desktop');
  const courseDir = path.join(desktopDir, courseName);
  
  if (!fs.existsSync(courseDir)) {
    console.log(`❌ 未找到课程目录: ${courseDir}`);
    return;
  }

  // 获取所有截图文件
  const screenshots = fs.readdirSync(courseDir)
    .filter(f => f.endsWith('.png') && !f.startsWith('_'))
    .map(f => path.join(courseDir, f));

  if (screenshots.length === 0) {
    console.log('❌ 未找到截图文件');
    return;
  }

  console.log(`找到 ${screenshots.length} 个学生截图\n`);

  const apiKey = process.env.DASHSCOPE_API_KEY;
  if (!apiKey) {
    console.log('❌ 未设置 DASHSCOPE_API_KEY 环境变量');
    return;
  }

  const results = [];

  for (const screenshot of screenshots) {
    const studentName = path.basename(screenshot, '.png');
    console.log(`分析: ${studentName}...`);

    const prompt = `请分析这张截图中学生提交的作业数量。

截图中格式通常如下：
认真完成课内课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）
认真完成奥数课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）

请统计：
1. 课内作业的图片数量
2. 奥数作业的图片数量

用简洁的中文回答，格式如下：
学生姓名：XXX
课内作业：X张
奥数作业：X张`;

    const base64 = fs.readFileSync(screenshot, { encoding: 'base64' });

    const pythonScript = `
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key="${apiKey}",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-vl-max-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/png;base64,${base64}"}
                },
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

    const tempScript = path.join(courseDir, `_analyze_${studentName}.py`);
    fs.writeFileSync(tempScript, pythonScript, 'utf-8');

    try {
      const result = execSync(`python3 "${tempScript}"`, { 
        encoding: 'utf-8',
        timeout: 120000
      });
      fs.unlinkSync(tempScript);

      // 解析结果
      const keNeiMatch = result.match(/课内作业：(\d+)张/);
      const aoShuMatch = result.match(/奥数作业：(\d+)张/);

      const keNeiCount = keNeiMatch ? parseInt(keNeiMatch[1]) : 0;
      const aoShuCount = aoShuMatch ? parseInt(aoShuMatch[1]) : 0;

      results.push({
        student: studentName,
        keNeiCount,
        aoShuCount,
        rawAnalysis: result.trim()
      });

      console.log(`  ✅ 课内: ${keNeiCount}张, 奥数: ${aoShuCount}张\n`);
    } catch (error) {
      if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
      console.log(`  ❌ 分析失败: ${error.message}\n`);
      results.push({
        student: studentName,
        keNeiCount: 0,
        aoShuCount: 0,
        error: true
      });
    }
  }

  // 保存分析结果
  const analysisPath = path.join(courseDir, 'analysis-results.json');
  fs.writeFileSync(analysisPath, JSON.stringify(results, null, 2), 'utf-8');

  console.log('='.repeat(60));
  console.log('  分析结果汇总');
  console.log('='.repeat(60));
  
  for (const r of results) {
    console.log(`\n${r.student}:`);
    console.log(`  课内作业: ${r.keNeiCount}张`);
    console.log(`  奥数作业: ${r.aoShuCount}张`);
    if (r.rawAnalysis) {
      console.log(`  详细: ${r.rawAnalysis.replace(/\n/g, ' ')}`);
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('  ✅ AI 分析完成！');
  console.log('='.repeat(60) + '\n');

  return results;
}

// 主入口
const courseName = process.argv[2] || '二下(第36节)';
analyzeScreenshots(courseName).catch(console.error);
