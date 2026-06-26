import 'dotenv/config';
import { execSync } from 'child_process';
import OpenAI from 'openai';
import fs from 'fs';
import path from 'path';

// ========== 配置 ==========
const ASSEMBLYAI_KEY = process.env.ASSEMBLYAI_API_KEY;
const GEMINI_KEY = process.env.GEMINI_API_KEY;
const OPENROUTER_KEY = process.env.OPENAI_API_KEY;
const SUMMARY_KEY = process.env.OPENAI_API_KEY;
const SUMMARY_BASE = process.env.OPENAI_BASE_URL || 'https://openrouter.ai/api/v1';
const SUMMARY_MODEL = process.env.SUMMARY_MODEL || 'anthropic/claude-sonnet-4-5';

// 用户可通过 ASR_ENGINE 环境变量强制指定引擎
const FORCE_ENGINE = process.env.ASR_ENGINE; // assemblyai | gemini | whisper

// ========== 场景定义 ==========
const SCENES = {
  rowing: {
    name: '赛艇训练',
    required: ['桨', '赛艇', '划'],
    keywords: ['桨频', '配速', '起航', '入水', '蹬腿', '教练喊', '划艇', '赛艇', '申迪', '水上'],
    prompt: (transcript, date) => `你是赛艇训练分析助手。以下是今天赛艇训练的对话记录。
请分析生成训练点评报告，包括：
1. 说话人识别（教练 vs 学员）
2. 训练要点（技术强调，3-5条）
3. 改进建议
4. 整体状态评估
5. 下次训练关注点

日期: ${date}
对话记录:
${transcript}

用中文输出，格式简洁，用 emoji 让报告更直观。`,
  },

  meeting: {
    name: '工作会议',
    required: [],
    keywords: ['项目', '排期', '需求', '上线', 'bug', '迭代', '产品', '用户运营', '增长', '商业化',
               '用户', '框架', '策略', '投放', '社群', 'agent', 'kol', '运营', '团队', '会议',
               'openclaw', '节约', '街跃', '龙虾', '小龙虾', '水产市场', '硬件'],
    prompt: (transcript, date) => `你是会议纪要助手。请分析以下对话记录，生成结构化会议纪要。

重点关注：
1. 会议主题和背景
2. 讨论的核心议题及结论
3. 决策事项
4. Action Items（责任人 + 截止时间，如有提及）
5. 未决问题 / 待跟进事项

日期: ${date}
对话记录:
${transcript}

用中文输出，格式结构清晰，重点突出 Action Items。用 emoji 提升可读性。`,
  },

  interview: {
    name: '客户访谈',
    required: [],
    keywords: ['用户痛点', '使用场景', '反馈', '访谈', '受访', '你们产品', '体验如何', '需求调研'],
    prompt: (transcript, date) => `你是用户研究助手。以下是客户访谈记录，请生成访谈分析报告，包括：
1. 受访者背景
2. 核心痛点
3. 需求与期望
4. 关键洞察
5. 建议跟进方向

日期: ${date}
对话记录:
${transcript}

用中文输出，格式简洁。`,
  },

  general: {
    name: '通用对话',
    required: [],
    keywords: [],
    prompt: (transcript, date) => `请分析以下对话记录，生成结构化摘要，包括：
1. 对话主题
2. 主要内容
3. 关键结论或决定
4. 后续行动（如有）

日期: ${date}
对话记录:
${transcript}

用中文输出，格式简洁清晰。`,
  },
};

// ========== ASR 引擎: AssemblyAI ==========
async function transcribeAssemblyAI(audioPath) {
  console.log('🎙️ [AssemblyAI] 转写中...');
  const { AssemblyAI } = await import('assemblyai');
  const client = new AssemblyAI({ apiKey: ASSEMBLYAI_KEY });

  const transcript = await client.transcripts.transcribe({
    audio: audioPath,
    speaker_labels: true,
    language_code: 'zh',
    punctuate: true,
    format_text: true,
    speech_models: ['universal-2'],
  });

  if (transcript.status === 'error') {
    throw new Error(`AssemblyAI 转写失败: ${transcript.error}`);
  }

  const speakers = new Set(transcript.utterances?.map(u => u.speaker) || []);
  console.log(`✅ [AssemblyAI] 完成! ${speakers.size} 位说话人`);
  return transcript;
}

// ========== ASR 引擎: Gemini (via OpenRouter or direct) ==========
async function transcribeGemini(audioPath) {
  const apiKey = GEMINI_KEY || OPENROUTER_KEY;
  const baseURL = GEMINI_KEY
    ? 'https://generativelanguage.googleapis.com/v1beta/openai'
    : 'https://openrouter.ai/api/v1';
  const model = GEMINI_KEY
    ? 'gemini-2.5-flash'
    : 'google/gemini-2.5-flash';

  console.log(`🎙️ [Gemini] 转写中 (via ${GEMINI_KEY ? 'Google API' : 'OpenRouter'})...`);

  // Read audio file and convert to base64
  const audioBuffer = fs.readFileSync(audioPath);
  const base64Audio = audioBuffer.toString('base64');
  const ext = path.extname(audioPath).slice(1);
  const mimeMap = { m4a: 'audio/mp4', mp3: 'audio/mpeg', wav: 'audio/wav', ogg: 'audio/ogg', flac: 'audio/flac' };
  const mimeType = mimeMap[ext] || 'audio/mpeg';

  const openai = new OpenAI({ apiKey, baseURL });

  const response = await openai.chat.completions.create({
    model,
    messages: [{
      role: 'user',
      content: [
        {
          type: 'input_audio',
          input_audio: { data: base64Audio, format: ext === 'wav' ? 'wav' : 'mp3' },
        },
        {
          type: 'text',
          text: `请逐字转写这段音频。要求：
1. 如果有多个说话人，用 "说话人A:", "说话人B:" 等标注
2. 保留原始语言（中文就用中文）
3. 每段话标注大致时间（如 [00:00], [01:23]）
4. 不要总结，不要省略，完整转写每一句话`,
        },
      ],
    }],
    max_tokens: 8000,
  });

  const text = response.choices[0].message.content;
  console.log(`✅ [Gemini] 转写完成`);

  // 转换为统一格式
  return { text, utterances: null, _engine: 'gemini' };
}

// ========== ASR 引擎: Whisper (本地) ==========
async function transcribeWhisper(audioPath) {
  console.log('🎙️ [Whisper] 本地转写中...');

  try {
    // 检查 whisper 是否可用
    execSync('which whisper', { stdio: 'pipe' });
  } catch {
    throw new Error('Whisper 未安装。安装: pip install openai-whisper');
  }

  const outputDir = path.dirname(audioPath);
  const baseName = path.basename(audioPath, path.extname(audioPath));

  // 运行 whisper，输出 JSON
  execSync(
    `whisper "${audioPath}" --language zh --output_format json --output_dir "${outputDir}" --model base`,
    { stdio: 'pipe', timeout: 600000 }
  );

  const jsonPath = path.join(outputDir, `${baseName}.json`);
  if (!fs.existsSync(jsonPath)) {
    throw new Error('Whisper 输出文件未找到');
  }

  const whisperResult = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const text = whisperResult.text || '';
  const segments = whisperResult.segments || [];

  // 转换为类 AssemblyAI 格式（Whisper 没有说话人分离）
  const utterances = segments.map(seg => ({
    speaker: 'A',
    text: seg.text.trim(),
    start: Math.floor(seg.start * 1000),
    end: Math.floor(seg.end * 1000),
  }));

  console.log(`✅ [Whisper] 转写完成 (${segments.length} 段)`);
  console.log(`⚠️ [Whisper] 注意：本地 Whisper 不支持说话人分离，所有内容标记为同一说话人`);

  return { text, utterances, _engine: 'whisper' };
}

// ========== 引擎选择 ==========
async function transcribeAudio(audioPath) {
  // 检测可用引擎
  const engines = [];
  if (ASSEMBLYAI_KEY) engines.push('assemblyai');
  if (GEMINI_KEY || OPENROUTER_KEY) engines.push('gemini');
  try { execSync('which whisper', { stdio: 'pipe' }); engines.push('whisper'); } catch {}

  if (engines.length === 0) {
    console.error('❌ 没有可用的 ASR 引擎。请配置至少一个:');
    console.error('   - ASSEMBLYAI_API_KEY (推荐，最佳质量)');
    console.error('   - GEMINI_API_KEY 或 OPENAI_API_KEY (Gemini via OpenRouter)');
    console.error('   - 安装本地 Whisper: pip install openai-whisper');
    process.exit(1);
  }

  console.log(`🔍 可用引擎: ${engines.join(', ')}`);

  // 确定使用顺序
  let order;
  if (FORCE_ENGINE && engines.includes(FORCE_ENGINE)) {
    order = [FORCE_ENGINE];
    console.log(`🎯 强制使用: ${FORCE_ENGINE}`);
  } else {
    // 默认优先级: AssemblyAI > Gemini > Whisper
    order = ['assemblyai', 'gemini', 'whisper'].filter(e => engines.includes(e));
  }

  // 按顺序尝试，失败则 fallback
  for (const engine of order) {
    try {
      switch (engine) {
        case 'assemblyai': return await transcribeAssemblyAI(audioPath);
        case 'gemini': return await transcribeGemini(audioPath);
        case 'whisper': return await transcribeWhisper(audioPath);
      }
    } catch (err) {
      console.warn(`⚠️ [${engine}] 失败: ${err.message}`);
      if (order.indexOf(engine) < order.length - 1) {
        console.log(`🔄 尝试下一个引擎...`);
      } else {
        throw err;
      }
    }
  }
}

// ========== 格式化对话记录 ==========
function formatTranscript(transcript) {
  if (!transcript.utterances || transcript.utterances.length === 0) {
    return transcript.text || '(无内容)';
  }

  return transcript.utterances.map(u => {
    const startMs = u.start;
    const min = Math.floor(startMs / 60000);
    const sec = Math.floor((startMs % 60000) / 1000);
    const timeStr = `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
    return `[${timeStr}] 说话人${u.speaker}: ${u.text}`;
  }).join('\n');
}

// ========== 场景识别 ==========
function detectScene(text, manualScene) {
  if (manualScene && SCENES[manualScene]) {
    console.log(`🎯 手动指定场景: ${SCENES[manualScene].name}`);
    return manualScene;
  }

  const lowerText = text.toLowerCase();
  const scores = {};

  for (const [key, scene] of Object.entries(SCENES)) {
    if (key === 'general') continue;

    if (scene.required.length > 0) {
      const hasRequired = scene.required.every(w => lowerText.includes(w));
      if (!hasRequired) { scores[key] = 0; continue; }
    }

    const hits = scene.keywords.filter(w => lowerText.includes(w)).length;
    scores[key] = hits;
  }

  console.log('📊 场景识别得分:', scores);

  const best = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
  if (best && best[1] > 0) {
    console.log(`✅ 识别场景: ${SCENES[best[0]].name} (命中 ${best[1]} 个关键词)`);
    return best[0];
  }

  console.log('ℹ️ 未匹配特定场景，使用通用模板');
  return 'general';
}

// ========== AI 总结 ==========
async function summarize(formattedTranscript, sceneKey, date) {
  console.log('🧠 正在生成总结...');

  const scene = SCENES[sceneKey];
  const openai = new OpenAI({
    apiKey: SUMMARY_KEY,
    baseURL: SUMMARY_BASE,
  });

  const prompt = scene.prompt(formattedTranscript, date);

  const response = await openai.chat.completions.create({
    model: SUMMARY_MODEL,
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 2000,
  });

  return response.choices[0].message.content;
}

// ========== 主流程 ==========
async function main() {
  const audioPath = process.argv[2];
  const manualScene = process.argv[3];

  if (!audioPath) {
    console.log('用法: node analyze.js <录音文件路径> [场景: rowing|meeting|interview|general]');
    console.log('');
    console.log('ASR 引擎优先级: AssemblyAI → Gemini → Whisper (自动检测)');
    console.log('强制指定引擎: ASR_ENGINE=whisper node analyze.js file.m4a');
    process.exit(1);
  }

  if (!fs.existsSync(audioPath)) {
    console.log(`❌ 文件不存在: ${audioPath}`);
    process.exit(1);
  }

  const fileSize = fs.statSync(audioPath).size;
  console.log(`📁 文件: ${path.basename(audioPath)} (${(fileSize / 1024 / 1024).toFixed(2)} MB)`);

  const date = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });

  try {
    // 1. 转写（自动选引擎）
    const transcript = await transcribeAudio(audioPath);

    // 2. 格式化
    const formatted = formatTranscript(transcript);

    // 3. 保存转写
    const outputDir = path.dirname(audioPath);
    const baseName = path.basename(audioPath, path.extname(audioPath));
    const transcriptPath = path.join(outputDir, `${baseName}_transcript.txt`);
    fs.writeFileSync(transcriptPath, formatted, 'utf8');
    console.log(`📄 对话记录已保存: ${transcriptPath}`);

    // 保存原始 JSON
    const jsonPath = path.join(outputDir, `${baseName}_raw.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(transcript, null, 2), 'utf8');

    // 4. 场景识别
    const sceneKey = detectScene(formatted, manualScene);
    const sceneName = SCENES[sceneKey].name;

    // 5. AI 总结
    if (SUMMARY_KEY && SUMMARY_KEY !== 'sk-or-v1-placeholder') {
      const summary = await summarize(formatted, sceneKey, date);

      const summaryPath = path.join(outputDir, `${baseName}_summary.md`);
      const engine = transcript._engine || 'assemblyai';
      const report = `# ${sceneName}纪要 — ${date}\n\n> ASR Engine: ${engine}\n\n${summary}\n\n---\n\n## 完整对话记录\n\n\`\`\`\n${formatted}\n\`\`\``;
      fs.writeFileSync(summaryPath, report, 'utf8');
      console.log(`📋 总结已保存: ${summaryPath}`);
      console.log(`\n========== ${sceneName}总结 ==========\n`);
      console.log(summary);
    } else {
      console.log('\n========== 对话记录 ==========\n');
      console.log(formatted);
    }

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
