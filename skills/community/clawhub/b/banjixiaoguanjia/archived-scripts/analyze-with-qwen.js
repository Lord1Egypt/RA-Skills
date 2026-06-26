/**
 * 使用 Qwen 分析小米的课内作业
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function analyzeWithQwen() {
  const studentName = '小米';
  const homeworkType = '课内';
  const courseName = '一下(第9节)';
  
  // 学生作业目录
  const studentDir = path.join(require('os').homedir(), 'Desktop', courseName, studentName, homeworkType);
  
  // 答案文件
  const answerPath = path.join(require('os').homedir(), 'Desktop', '答案', courseName, '课内答案.png');
  
  console.log(`========================================`);
  console.log(`使用 Qwen 批改: ${studentName} - ${homeworkType}作业`);
  console.log(`========================================\n`);
  
  // 检查答案文件是否存在
  const hasAnswer = fs.existsSync(answerPath);
  console.log(`答案文件: ${hasAnswer ? '存在' : '不存在'}\n`);
  
  // 获取学生作业图片
  const homeworkFiles = fs.readdirSync(studentDir)
    .filter(f => f.endsWith('.jpg'))
    .map(f => path.join(studentDir, f))
    .sort();
  
  console.log(`作业图片: ${homeworkFiles.length} 张\n`);
  
  // 构建提示词
  let promptPrefix = '';
  if (hasAnswer) {
    promptPrefix = "第1张图片是课内答案.png，这是作业的标准答案，你需要认真参考答案进行作业批改。\n\n";
  }
  
  const prompt = promptPrefix + `帮我检查这些作业的对错，并根据学生的对错分析出该学生对于这个章节理解的薄弱环节与作业总结。对于看不清楚学生答案的按照错误处理，如果发现较多看不清楚学生手写答案那就要强调学生在作业书写规范上要重点加强(字迹潦草不算，因为孩子年龄不大)。

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
作业图片数量：${homeworkFiles.length}张

逐题批改：
第1题：...（正确/错误/看不清楚/漏题）
...

薄弱环节分析：
...

作业总结：
...`;

  // 构建Python脚本 - 使用 Qwen
  const imagePaths = hasAnswer 
    ? [answerPath, ...homeworkFiles]
    : homeworkFiles;
  
  const imageEncodings = imagePaths.map(imgPath => {
    const base64 = fs.readFileSync(imgPath, { encoding: 'base64' });
    return `"data:image/jpeg;base64,${base64}"`;
  });

  const pythonScript = `
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key="${process.env.DASHSCOPE_API_KEY || 'sk-14d72eaba86242d3ba368ee0c9b08dac'}",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-vl-max-latest",
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

  const tempScript = path.join(studentDir, '_analyze_qwen.py');
  fs.writeFileSync(tempScript, pythonScript, 'utf-8');
  
  console.log('正在使用 Qwen 分析，请稍候...\n');
  
  try {
    const result = execSync(`python3 "${tempScript}"`, { 
      encoding: 'utf-8',
      timeout: 300000  // 5分钟超时
    });
    fs.unlinkSync(tempScript);
    
    console.log(result);
    
    // 保存结果到文件
    const resultPath = path.join(require('os').homedir(), 'Desktop', courseName, `${courseName}${studentName}${homeworkType}分析.txt`);
    fs.writeFileSync(resultPath, result, 'utf-8');
    console.log(`\n分析结果已保存: ${resultPath}`);
    
  } catch (error) {
    if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
    console.error('分析失败:', error.message);
  }
}

analyzeWithQwen().catch(console.error);
