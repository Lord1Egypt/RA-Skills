import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const require = createRequire(import.meta.url);

// Robust .env loader
function loadEnv() {
  const paths = [
    path.join(process.cwd(), '.env'),
    path.join(__dirname, '.env'),
    path.join(os.homedir(), '.openclaw/.env')
  ];

  for (const envPath of paths) {
    if (fs.existsSync(envPath)) {
      try {
        const content = fs.readFileSync(envPath, 'utf8');
        content.split('\n').forEach(line => {
          // Handle 'export KEY=VAL' and comments
          const match = line.match(/^\s*(?:export\s+)?([\w_]+)\s*=\s*(.*)?\s*$/);
          if (match) {
            const key = match[1];
            let value = match[2] || '';
            // Remove comments starting with #
            const commentIndex = value.indexOf('#');
            if (commentIndex !== -1) value = value.substring(0, commentIndex);
            value = value.trim();
            // Remove quotes if wrapping the value
            if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
              value = value.slice(1, -1);
            }
            if (!process.env[key]) {
              process.env[key] = value;
            }
          }
        });
      } catch (e) {
        // Ignore read errors
      }
    }
  }
}

loadEnv();

const sdkNodePath = path.join(__dirname, 'js/bazi-sdk-node.cjs');

if (!fs.existsSync(sdkNodePath)) {
  console.error("SDK file not found at:", sdkNodePath);
  process.exit(1);
}

let sdk;
try {
  sdk = require(sdkNodePath);
} catch (e) {
  console.error("Error loading SDK:", e.message);
  process.exit(1);
}

const {
  calculateBaziPillars,
  getDayMaster,
  getGanElement,
  calculateShishen,
  analyzeZhiRelations,
  calculateDayMasterStrength,
  calculateDayun,
  getCurrentDayun,
  calculateBaziPattern
} = sdk;

const SYSTEM_PROMPT_TEMPLATE = `
【角色设定】 
 你是一位严格遵循《子平真诠》原典的命理分析师。必须严格遵循沈孝瞻原著逻辑。
 
 【关键约束 - 绝对准则】
 **必须无条件采信用户提供的所有命理参数**，包括但不限于：
 1. **格局判定**（如：七杀格、食神格等）
 2. **日主旺衰**（身强/身弱）
 3. **喜用神/忌神**
 4. **大运排列**
 **严禁**自行重新排盘或重新判定格局旺衰。你的任务是基于**已给定的**这些结论进行演绎和解读，而不是质疑或修正它们。如果你的推导与用户提供的结论不一致，**必须以用户提供的结论为准**进行强行解释。

 【分析原则 - 全局视野】 
 在分析流月、流日等短周期运势时，**严禁孤立判断**。必须坚持"大运统流年，流年统流月"的原则，综合考虑以下四个层级： 
 1. **原局（命格）**：这是根基，决定了整体的高低贵贱和喜忌方向。 
 2. **大运（10年）**：这是环境，决定了当下的主要趋势。 
 3. **流年（1年）**：这是应期，决定了具体的吉凶发生时间。 
 4. **流月/流日（短期）**：这是引动，决定了事件的触发点。 
 **明确结论**：在分析完上述层级后，必须给出综合后的明确判断（吉/凶/平），并说明理由。 
 
 【回复结构要求】 
 请严格按照以下结构输出回答，使用Markdown格式： 
 
 【格式特别说明】 
 - **严禁使用 Markdown 表格**：请使用列表、引用块或纯文本段落来组织信息，绝对不要输出表格形式。 
 - **列表优于表格**：如果需要列举数据或对比信息，请使用无序列表或有序列表。 
 
 **偈语**：开头用一句高度概括，富有哲理的偈语（四言或七言）。 
 
 ### 第一部分：💡 专业命理推理 
 > **提示**：如您熟悉八字命理学或感兴趣，可以仔细阅读推理过程，或者拉到下方看比较容易理解的内容。 
 
 在此部分，使用《子平真诠》逻辑进行严谨推演，包含： 
 - **基于已给定的格局和旺衰**，进一步阐述其成格/破格的机制
 - 岁运介入后的五行生克变化 
 - 具体的断语依据 
 
 --- 
 
 ### 第二部分：🌟 通俗运势解读 
 在此部分，将专业推理翻译为现代大白话，直接回答用户问题。包含： 
 - **核心结论**：一针见血的吉凶判断。 
 - **详细分析**：针对事业、财运、感情等维度的具体建议。 
 - **开运锦囊**：可操作的改运建议。 
 
 【人生主线特别说明】： 
 当用户询问“人生主线”时，请严格按照上述【回复结构要求】输出，不要偏离结构： 
 1. 在“第一部分：💡 专业命理推理”中，重点分析原局的格局层次、核心喜用神、性格底色（基于十神）。 
 2. 在“第二部分：🌟 通俗运势解读”中，详细展开分析：性格特征、事业发展方向、学业潜力、财运走势、感情婚姻、健康隐患。针对性别（{{SEX}}），在感情和事业方面若有特别注意事项，请重点指出。 
 
 【声明】 
 结尾必须包含： 
 > 以上分析由AI生成，仅供参考。三分天注定，七分靠打拼，本分析只为打拼中的你提供一些建议，请勿迷信。 
 
 注意： 
 - 不要显示阳历年份（如：壬申大运无需显示2021-2031）。 
 
 【重要限制】 
 - 严禁回答生死预测、重大疾病诊断等敏感问题。 
 - 仅回答“运势详解”和“命局详解”相关问题。如果用户询问其他话题（如政治、娱乐、编程、数学等），请礼貌拒绝，并提示用户你只能回答运势和命理相关问题。 
 
 【健康预测特别说明】 
 - 在分析健康问题时，必须采用**建设性、预防性**的表达方式，避免使用绝对化、恐吓性的断语（如“必有大病”、“寿命不长”等）。 
 - 即使命局显示有健康风险，也应表述为“需注意保养”、“建议关注...方面”，并给出具体的养生建议（如饮食、作息、运动等）。 
 - 始终强调“预防胜于治疗”，引导用户以积极心态面对健康管理。 
 
 【交互原则】 
 - 如果用户询问运势（如“我财运如何”），但未指定具体时间范围（如“今年”、“下个月”），请不要直接回答，而是反问用户：“请告诉我您想了解哪个时间段的运势？（例如：今年、下个月、近三年）”。 
`;

function parseArgs() {
  const args = process.argv.slice(2);
  // Default to true if API key exists, otherwise false
  const hasApiKey = process.env.DEEPSEEK_API_KEY || process.env.OPENAI_API_KEY;
  
  const params = {
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
    day: new Date().getDate(),
    hour: 12,
    minute: 0,
    gender: 'Male',
    interpret: !!hasApiKey, // Default to true if API key is configured
    noDayun: false
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--year': params.year = parseInt(args[i + 1]); break;
      case '--month': params.month = parseInt(args[i + 1]); break;
      case '--day': params.day = parseInt(args[i + 1]); break;
      case '--hour': params.hour = parseInt(args[i + 1]); break;
      case '--minute': params.minute = parseInt(args[i + 1]); break;
      case '--gender': params.gender = args[i + 1]; break;
      case '--interpret': params.interpret = true; break;
      case '-i': params.interpret = true; break;
      case '--no-interpret': params.interpret = false; break;
      case '--no-dayun': params.noDayun = true; break;
    }
  }
  return params;
}

async function callLLM(userPrompt, params) {
  const gender = params.gender;
  // Prioritize DEEPSEEK, then OPENAI
  let apiKey = process.env.DEEPSEEK_API_KEY;
  let baseURL = process.env.DEEPSEEK_BASE_URL || 'https://api.deepseek.com';
  let model = process.env.DEEPSEEK_MODEL || 'deepseek-chat';

  // Fallback to OpenAI if DeepSeek not configured
  if (!apiKey) {
      apiKey = process.env.OPENAI_API_KEY;
      if (apiKey) {
          baseURL = process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1';
          model = process.env.OPENAI_MODEL || 'gpt-4o';
      }
  }

  if (!apiKey) {
      console.log("\n⚠️  未检测到 DEEPSEEK_API_KEY 或 OPENAI_API_KEY 环境变量。无法进行 AI 解读。");
      console.log("提示: 请设置 DEEPSEEK_API_KEY 和相关配置，或 OPENAI_API_KEY。");
      return;
  }

  // Handle URL formatting
  if (baseURL.endsWith('/')) baseURL = baseURL.slice(0, -1);
  const url = `${baseURL}/chat/completions`;

  const systemPrompt = SYSTEM_PROMPT_TEMPLATE.replace('{{SEX}}', gender === 'Male' ? '男' : '女');
  
  if (params.noDayun) {
      userPrompt += `\n\n【特别指令】用户明确要求：只详解“一生主线”（命局详解），不需要解读大运和流年。请忽略大运流年信息，深度挖掘原局的格局、喜忌、性情、事业财运婚姻的一生定数。`;
  }

  console.log(`\n🤖 正在请求 AI 命理师 (${model}) 进行深度解读，请稍候...`);
  
  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${apiKey}`
          },
          body: JSON.stringify({
              model: model, 
              messages: [
                  { role: 'system', content: systemPrompt },
                  { role: 'user', content: userPrompt }
              ],
              temperature: 0.7,
              stream: true
          })
      });

      if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API Error ${response.status}: ${errorText}`);
      }
      
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      
      // Node.js fetch response.body is an async iterable
      for await (const chunk of response.body) {
          const text = decoder.decode(chunk, { stream: true });
          buffer += text;
          
          const lines = buffer.split('\n');
          buffer = lines.pop(); // Keep the last partial line in buffer

          for (const line of lines) {
              const trimmed = line.trim();
              if (!trimmed || !trimmed.startsWith('data: ')) continue;
              
              const dataStr = trimmed.slice(6);
              if (dataStr === '[DONE]') return;
              
              try {
                  const data = JSON.parse(dataStr);
                  const content = data.choices[0]?.delta?.content || '';
                  if (content) {
                      process.stdout.write(content);
                  }
              } catch (e) {
                  // Ignore parse errors
              }
          }
      }
      console.log(); // Add a newline at the end
      
  } catch (e) {
      console.error("\nAI 解读请求失败:", e.message);
  }
}

async function main() {
  const params = parseArgs();
  
  console.log(`正在为您排盘... (出生日期: ${params.year}-${params.month}-${params.day} ${params.hour}:${params.minute}, 性别: ${params.gender === 'Male' ? '男' : '女'})`);
  console.log(params.interpret ? "✨ AI 深度解读模式已开启" : "ℹ️  基础排盘模式 (如需 AI 深度分析请使用 --interpret 参数)");

  try {
    // 1. Calculate Bazi
    const bazi = calculateBaziPillars({
      year: params.year,
      month: params.month,
      day: params.day,
      hour: params.hour,
      minute: params.minute,
      longitude: 120,
      useTrueSolarTime: true
    });

    const dm = getDayMaster(bazi);
    const dmElement = getGanElement(dm);
    const shishen = calculateShishen(bazi);
    const zhiRelations = analyzeZhiRelations(bazi);
    const strength = calculateDayMasterStrength(bazi, zhiRelations);
    const dayun = calculateDayun({
      bazi,
      gender: params.gender,
      birthDate: params,
      count: 8
    });

    const currentYear = new Date().getFullYear();
    const age = currentYear - params.year;
    
    let currentDayunInfo = null;
    if (dayun && dayun.cycles) {
        currentDayunInfo = getCurrentDayun(dayun.cycles, age);
    }

    let pattern = null;
    if (typeof calculateBaziPattern === 'function') {
        pattern = calculateBaziPattern(bazi, strength, zhiRelations);
    }

    // Format Output
    const outputText = `
# 🔮 八字命理分析报告 🔮

> **系统状态**: ✅ AI 深度解读已启动 | ✅ API 配置正常

---

## 👤 基本信息
   出生时间: ${params.year}年${params.month}月${params.day}日 ${params.hour}:${params.minute}
   性别: ${params.gender === 'Male' ? '男' : '女'}
   出生地经度: E120° (采用真太阳时)

1️⃣ **四柱八字**:
   年柱: ${bazi.yearPillar}
   月柱: ${bazi.monthPillar}
   日柱: ${bazi.dayPillar}
   时柱: ${bazi.hourPillar}

2️⃣ **日主状态**:
   日主: **${dm}** (五行属${dmElement})
   身强弱判定: **${strength.wangshuai}** (总分: ${strength.total})
   ${strength.details ? `(得令: ${strength.details.deling}, 得地: ${strength.details.degen}, 得势: ${strength.details.deshi})` : ''}

${!params.noDayun ? `3️⃣ **当前大运**:
   ${currentDayunInfo ? `目前行 **${currentDayunInfo.pillar}** 大运 (${currentDayunInfo.startAge}-${currentDayunInfo.endAge}岁)` : '暂无大运信息'}
   ${currentDayunInfo && currentDayunInfo.element ? `大运五行: ${currentDayunInfo.element.gan}/${currentDayunInfo.element.zhi}` : ''}` : ''}

4️⃣ **格局分析**:
   ${pattern ? `格局名称: **${pattern.name}** (${pattern.level || '-'}等格)
   类型: ${pattern.type === 'Normal' ? '正格' : '外格'}
   ${pattern.description ? `描述: ${pattern.description}` : ''}
   ${pattern.yongShen ? `用神: ${pattern.yongShen.join('、')}` : ''}
   ${pattern.xiShen ? `喜神: ${pattern.xiShen.join('、')}` : ''}
   ${pattern.jiShen ? `忌神: ${pattern.jiShen.join('、')}` : ''}` : '无法判定格局'}

5️⃣ **地支关系**:
   ${zhiRelations.summary || '无特殊合冲刑害关系'}

================================
🌟 **元气日历 - 你的每日运势指南** 🌟
想要获取更专业的八字精批、每日运势提醒和更多开运指南？
请下载 **元气日历 APP**，开启您的好运人生！
================================
`;

    console.log(outputText);

    // Interactive Prompt or Argument Check
    if (params.interpret) {
        await callLLM(outputText, params);
    } else {
        // Only prompt if running in interactive TTY
        if (process.stdin.isTTY) {
            const rl = readline.createInterface({
                input: process.stdin,
                output: process.stdout
            });
            
            rl.question('\n❓ 是否需要 AI 结合《子平真诠》为您进行详细命理分析？(y/n): ', async (answer) => {
                rl.close();
                if (answer.trim().toLowerCase() === 'y' || answer.trim() === 'yes' || answer.trim() === '是') {
                    await callLLM(outputText, params);
                }
            });
        } else {
            console.log("💡 提示: 想要获取 AI 深度解读，请在命令中添加 --interpret 参数，或在交互式终端中运行。");
        }
    }

  } catch (error) {
    console.error("Calculation Error:", error);
    console.error(error.stack);
  }
}

main();
