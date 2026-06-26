#!/usr/bin/env node
/**
 * Bilibili 字幕下载分析工具
 * 基于 biliSub 项目: https://github.com/lvusyy/biliSub
 * 
 * 功能:
 * 1. 下载 B 站视频字幕（调用 Python 脚本）
 * 2. 分析字幕内容（词频、统计、情感）
 * 3. 生成内容分析报告
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class BilibiliSubtitleAnalyzer {
  constructor(options = {}) {
    // 可配置路径（支持环境变量和参数）
    this.outputDir = options.outputDir 
      || process.env.BILI_OUTPUT_DIR 
      || './bilibili-output';
    this.biliSubPath = options.biliSubPath 
      || process.env.BILISUB_PATH 
      || this.findBiliSubPath();
    this.pythonLibPath = options.pythonLibPath 
      || process.env.BILI_PYTHON_LIB 
      || '';
    this.proxy = options.proxy || process.env.BILI_PROXY || '';
    this.asrModel = options.asrModel || 'small';
    this.asrLang = options.asrLang || 'zh';
    this.ensureOutputDir();
  }

  ensureOutputDir() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  findBiliSubPath() {
    // 智能搜索 biliSub 项目位置
    const possiblePaths = [
      // 1. 技能目录的同级目录
      path.join(__dirname, '..', 'biliSub'),
      path.join(__dirname, '..', '..', 'biliSub'),
      // 2. 当前工作目录
      path.join(process.cwd(), 'biliSub'),
      // 3. 用户 home 目录
      path.join(process.env.HOME || process.env.USERPROFILE || '', 'biliSub'),
      path.join(process.env.HOME || process.env.USERPROFILE || '', '.openclaw', 'biliSub'),
      // 4. 常见下载目录
      path.join(process.env.HOME || process.env.USERPROFILE || '', 'Downloads', 'biliSub'),
      path.join(process.env.HOME || process.env.USERPROFILE || '', 'Documents', 'biliSub'),
    ];
    
    // 动态构建 Windows 用户路径
    if (process.platform === 'win32' && process.env.USERNAME) {
      possiblePaths.push(
        `C:\\Users\\${process.env.USERNAME}\\biliSub`,
        `C:\\Users\\${process.env.USERNAME}\\.openclaw\\biliSub`,
        `D:\\biliSub`,
      );
    }
    
    for (const p of possiblePaths) {
      if (p && fs.existsSync(p) && fs.existsSync(path.join(p, 'enhanced_bilisub.py'))) {
        return p;
      }
    }
    
    // 返回默认位置，不抛出错误
    return path.join(process.cwd(), 'biliSub');
  }

  /**
   * 获取 Python 解释器
   */
  getPythonCommand() {
    // 优先使用环境变量指定的 Python
    if (process.env.BILI_PYTHON) {
      return process.env.BILI_PYTHON;
    }
    
    // 常见 Python 命令（按优先级）
    const pythonCommands = ['python', 'python3', 'py', 'python3.10', 'python3.11', 'python3.12'];
    
    for (const cmd of pythonCommands) {
      try {
        const result = execSync(cmd + ' --version', { encoding: 'utf-8', timeout: 5000 });
        if (result.includes('3.')) {
          return cmd;
        }
      } catch (e) {
        continue;
      }
    }
    
    return 'python'; // 默认
  }

  /**
   * 下载单个视频字幕
   * @param {string} videoUrl - B站视频URL或BV号
   * @param {Object} options - 下载选项
   */
  async downloadSubtitle(videoUrl, options = {}) {
    const formats = options.formats || ['json', 'txt'];
    const useAsr = options.useAsr !== false;
    const asrModel = options.asrModel || this.asrModel;
    const asrLang = options.asrLang || this.asrLang;
    const proxy = options.proxy || this.proxy;

    console.log(`[下载] 开始下载字幕: ${videoUrl}`);
    
    const scriptPath = path.join(this.biliSubPath, 'enhanced_bilisub.py');
    
    if (!fs.existsSync(scriptPath)) {
      throw new Error(
        `biliSub 脚本不存在: ${scriptPath}\n\n` +
        `请确保已克隆 biliSub 项目：\n` +
        `  git clone https://github.com/lvusyy/biliSub\n\n` +
        `并通过以下方式指定路径：\n` +
        `  1. 环境变量: export BILISUB_PATH=/path/to/biliSub\n` +
        `  2. 或运行时: analyzer = new BilibiliSubtitleAnalyzer({ biliSubPath: '/path/to/biliSub' })`
      );
    }

    const pythonCmd = this.getPythonCommand();
    const args = [
      pythonCmd, '-u', scriptPath,
      '-i', videoUrl,
      '-o', this.outputDir,
      '-f', formats.join(','),
      '-c', '3'
    ];

    if (useAsr) {
      args.push('--use-asr', '--asr-model', asrModel, '--asr-lang', asrLang);
    } else {
      args.push('--no-asr');
    }

    if (proxy) {
      args.push('--proxy', proxy);
    }

    try {
      console.log(`[下载] 执行: ${pythonCmd} -u enhanced_bilisub.py -i ${videoUrl}`);
      
      // 构建环境变量
      const env = { ...process.env };
      if (this.pythonLibPath) {
        env.PYTHONPATH = this.pythonLibPath;
      }
      
      const result = execSync(args.join(' '), { 
        encoding: 'utf-8',
        timeout: 600000, // 10分钟超时
        maxBuffer: 10 * 1024 * 1024,
        env
      });
      
      console.log('[下载] 字幕下载成功');
      return this.getLatestFiles();
    } catch (error) {
      console.error('[下载] 字幕下载失败:', error.message);
      throw error;
    }
  }

  /**
   * 批量下载字幕
   * @param {string} urlFile - 包含URL列表的文件路径
   * @param {Object} options - 下载选项
   */
  async batchDownload(urlFile, options = {}) {
    console.log(`[批量下载] 从文件: ${urlFile}`);
    return this.downloadSubtitle(urlFile, { ...options, isBatch: true });
  }

  /**
   * 分析字幕文件内容
   * @param {string} subtitleFile - 字幕文件路径
   */
  analyzeContent(subtitleFile) {
    console.log(`[分析] 开始分析字幕: ${subtitleFile}`);
    
    if (!fs.existsSync(subtitleFile)) {
      throw new Error(`字幕文件不存在: ${subtitleFile}`);
    }

    const ext = path.extname(subtitleFile).toLowerCase();
    let content;

    if (ext === '.json') {
      const data = JSON.parse(fs.readFileSync(subtitleFile, 'utf-8'));
      content = this.extractTextFromJson(data);
    } else {
      content = fs.readFileSync(subtitleFile, 'utf-8');
    }

    const lines = content.split('\n').filter(line => line.trim());
    
    // 统计信息
    const stats = {
      file: subtitleFile,
      totalLines: lines.length,
      totalChars: content.replace(/\s/g, '').length,
      totalCharsWithSpaces: content.length,
      avgLineLength: lines.length > 0 ? (content.length / lines.length).toFixed(2) : 0,
      timestamps: this.extractTimestamps(content),
      duration: this.extractDuration(content),
      wordFrequency: this.calcWordFrequency(content),
      bigrams: this.calcBigrams(content),
      sentiment: this.analyzeSentiment(content),
      keywords: this.extractKeywords(content),
      textDensity: this.calcTextDensity(content, lines)
    };

    console.log('[分析] 分析完成');
    return stats;
  }

  extractTextFromJson(data) {
    // 处理 AI 字幕格式（包含 body 数组）
    if (data.body && Array.isArray(data.body)) {
      return data.body.map(item => item.content || '').filter(c => c).join('\n');
    }
    
    // 处理标准字幕格式
    if (Array.isArray(data)) {
      return data.map(item => item.content || item.text || '').join('\n');
    }
    if (data.subtitle || data.content) {
      const arr = data.subtitle || data.content;
      if (Array.isArray(arr)) {
        return arr.map(s => s.content || s.text || '').join('\n');
      }
    }
    return JSON.stringify(data);
  }

  extractTimestamps(content) {
    const srtRegex = /\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,\.]\d{3}/g;
    const srtMatches = content.match(srtRegex) || [];

    const assRegex = /Dialogue:\s*\d+,\d+:\d{2}:\d{2}\.\d{2},/g;
    const assMatches = content.match(assRegex) || [];

    return {
      count: srtMatches.length + assMatches.length,
      srt: srtMatches.length,
      ass: assMatches.length
    };
  }

  extractDuration(content) {
    const srtRegex = /\d{2}:(\d{2}):(\d{2})[,.](\d{3})/g;
    const matches = [...content.matchAll(srtRegex)];
    
    if (matches.length >= 2) {
      const first = matches[0];
      const last = matches[matches.length - 1];
      
      const firstSec = parseInt(first[1]) * 3600 + parseInt(first[2]) * 60 + parseInt(first[3]) / 1000;
      const lastSec = parseInt(last[1]) * 3600 + parseInt(last[2]) * 60 + parseInt(last[3]) / 1000;
      
      const duration = lastSec - firstSec;
      const hours = Math.floor(duration / 3600);
      const minutes = Math.floor((duration % 3600) / 60);
      const seconds = Math.floor(duration % 60);
      
      return { total: duration, formatted: `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}` };
    }
    return { total: 0, formatted: '00:00:00' };
  }

  calcWordFrequency(content) {
    let text = content
      .replace(/\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->/g, '')
      .replace(/<[^>]+>/g, '')
      .replace(/Dialogue:\s*\d+,\d+:\d{2}:\d{2}\.\d{2},/g, '')
      .replace(/[^a-zA-Z\u4e00-\u9fa5\s]/g, ' ')
      .toLowerCase();
    
    const chineseChars = text.match(/[\u4e00-\u9fa5]/g) || [];
    const chineseFreq = {};
    chineseChars.forEach(char => {
      chineseFreq[char] = (chineseFreq[char] || 0) + 1;
    });

    const englishWords = text.match(/[a-z]+/g) || [];
    const englishFreq = {};
    englishWords.forEach(word => {
      if (word.length > 1) {
        englishFreq[word] = (englishFreq[word] || 0) + 1;
      }
    });

    return {
      chinese: Object.entries(chineseFreq).sort((a, b) => b[1] - a[1]).slice(0, 30).reduce((obj, [char, count]) => { obj[char] = count; return obj; }, {}),
      english: Object.entries(englishFreq).sort((a, b) => b[1] - a[1]).slice(0, 30).reduce((obj, [word, count]) => { obj[word] = count; return obj; }, {})
    };
  }

  calcBigrams(content) {
    let text = content.replace(/<[^>]+>/g, '').replace(/[^a-zA-Z\u4e00-\u9fa5\s]/g, ' ');
    const words = text.split(/\s+/).filter(w => w.length > 0);
    const bigrams = {};
    
    for (let i = 0; i < words.length - 1; i++) {
      const bigram = words[i] + words[i + 1];
      bigrams[bigram] = (bigrams[bigram] || 0) + 1;
    }
    
    return Object.entries(bigrams).sort((a, b) => b[1] - a[1]).slice(0, 20).reduce((obj, [bigram, count]) => { obj[bigram] = count; return obj; }, {});
  }

  analyzeSentiment(content) {
    const positivePatterns = ['好', '棒', '赞', '喜欢', '厉害', '优秀', '完美', '牛', '强', '精彩', '实用', '有用', '成功', '收获', '进步'];
    const negativePatterns = ['差', '烂', '糟', '讨厌', '难看', '无聊', '失望', '垃圾', '弱', '难', '失败', '糟糕', '可恶'];
    
    let positiveCount = 0;
    let negativeCount = 0;
    
    positivePatterns.forEach(word => {
      positiveCount += (content.match(new RegExp(word, 'g')) || []).length;
    });
    
    negativePatterns.forEach(word => {
      negativeCount += (content.match(new RegExp(word, 'g')) || []).length;
    });

    let sentiment = 'neutral';
    let intensity = 'normal';
    
    if (positiveCount > negativeCount * 1.5) sentiment = 'positive';
    else if (negativeCount > positiveCount * 1.5) sentiment = 'negative';
    
    if (positiveCount + negativeCount > 50) intensity = 'strong';
    else if (positiveCount + negativeCount < 10) intensity = 'weak';

    return { sentiment, intensity, positiveCount, negativeCount, score: positiveCount - negativeCount };
  }

  extractKeywords(content) {
    const wordFreq = this.calcWordFrequency(content);
    return {
      chinese: Object.entries(wordFreq.chinese).slice(0, 20),
      english: Object.entries(wordFreq.english).slice(0, 20)
    };
  }

  calcTextDensity(content, lines) {
    const nonEmptyLines = lines.filter(line => line.trim().length > 0).length;
    return {
      effective: nonEmptyLines,
      total: lines.length,
      density: lines.length > 0 ? ((nonEmptyLines / lines.length) * 100).toFixed(1) + '%' : '0%'
    };
  }

  generateReport(analysis, videoInfo = '') {
    const report = `
╔══════════════════════════════════════════════════════════════════════╗
║                    📺 B站字幕内容分析报告                              ║
╚══════════════════════════════════════════════════════════════════════╝

🎬 视频信息: ${videoInfo || analysis.file || '未提供'}

═══════════════════════════════════════════════════════════════════════
📊 字幕基础统计
───────────────────────────────────────────────────────────────────────
  • 总行数: ${analysis.totalLines}
  • 字符数（去空格）: ${analysis.totalChars.toLocaleString()}
  • 平均行长: ${analysis.avgLineLength} 字符/行
  • 时间戳数量: ${analysis.timestamps.count}
  • 视频时长: ${analysis.duration.formatted}

🔤 高频词 TOP 15（中）
───────────────────────────────────────────────────────────────────────
${Object.entries(analysis.wordFrequency.chinese || {}).slice(0, 15).map(([word, count], i) => 
  `  ${(i + 1).toString().padStart(2)}. ${word}: ${count}`).join('\n') || '  无数据'}

🔤 高频词 TOP 15（英）
───────────────────────────────────────────────────────────────────────
${Object.entries(analysis.wordFrequency.english || {}).slice(0, 15).map(([word, count], i) => 
  `  ${(i + 1).toString().padStart(2)}. ${word}: ${count}`).join('\n') || '  无数据'}

💭 情感分析
───────────────────────────────────────────────────────────────────────
  • 情感倾向: ${analysis.sentiment.sentiment === 'positive' ? '🟢 正面' : analysis.sentiment.sentiment === 'negative' ? '🔴 负面' : '🟡 中性'}
  • 情感得分: ${analysis.sentiment.score > 0 ? '+' : ''}${analysis.sentiment.score}
`;
    return report;
  }

  generateDetailedSummary(subtitlePath, videoInfo = {}) {
    if (!fs.existsSync(subtitlePath)) {
      throw new Error(`字幕文件不存在: ${subtitlePath}`);
    }

    const ext = path.extname(subtitlePath).toLowerCase();
    let text;
    
    if (ext === '.json') {
      const data = JSON.parse(fs.readFileSync(subtitlePath, 'utf-8'));
      text = this.extractTextFromJson(data);
    } else {
      text = fs.readFileSync(subtitlePath, 'utf-8');
    }

    const analysis = this.analyzeContent(subtitlePath);
    const lines = text.split('\n').filter(line => line.trim());
    const duration = analysis.duration.formatted;
    
    const topChineseWords = Object.entries(analysis.wordFrequency.chinese || {}).slice(0, 20).map(([w]) => w);
    const topEnglishWords = Object.entries(analysis.wordFrequency.english || {}).slice(0, 10).map(([w]) => w);

    const report = `
══════════════════════════════════════════════════════════════════════════════
                    📺 视频详细总结报告
══════════════════════════════════════════════════════════════════════════════

**视频标题**：${videoInfo.title || path.basename(subtitlePath, ext)}
**视频时长**：${duration}
**字幕字数**：${analysis.totalChars.toLocaleString()} 字符
**生成时间**：${new Date().toLocaleString('zh-CN')}

══════════════════════════════════════════════════════════════════════════════
📊 内容概览
• 字幕行数：${lines.length} 行 | 字符数：${analysis.totalChars.toLocaleString()} | 文本密度：${analysis.textDensity.density}
• 情感倾向：${analysis.sentiment.sentiment === 'positive' ? '正面' : analysis.sentiment.sentiment === 'negative' ? '负面' : '中性'}

🔤 高频关键词
  中文：${topChineseWords.slice(0, 15).join('、') || '无'}
  英文：${topEnglishWords.join('、') || '无'}

📝 内容摘要（分段整理）
───────────────────────────────────────────────────────────────────────────
${this.generateContentSummary(lines)}

══════════════════════════════════════════════════════════════════════════════
`;
    return report;
  }

  generateContentSummary(lines) {
    const summaryParts = [];
    const chunkSize = 8;
    
    for (let i = 0; i < Math.min(lines.length, 50); i += chunkSize) {
      const chunk = lines.slice(i, i + chunkSize);
      const firstLine = chunk[0].trim();
      const lastLine = chunk[chunk.length - 1].trim();
      
      if (firstLine && lastLine && firstLine !== lastLine) {
        summaryParts.push(`【第${Math.floor(i / chunkSize) + 1}段】${firstLine}...${lastLine}`);
      } else if (firstLine) {
        summaryParts.push(`【第${Math.floor(i / chunkSize) + 1}段】${firstLine}`);
      }
    }
    
    return summaryParts.length > 0 ? summaryParts.join('\n\n') : '  （内容提取中...）';
  }

  extractKeyQuotes(lines) {
    const quotes = lines.filter(line => line.length > 15 && line.length < 100).slice(0, 10);
    return quotes.map((q, i) => `  ${i + 1}. "${q.trim()}"`).join('\n') || '  （无）';
  }

  classifyContent(topWords) {
    const techKeywords = ['游戏', '引擎', '开发', '代码', '软件', '技术', '系统', 'Unity', 'AI', 'MCP', '渲染'];
    const techCount = topWords.filter(w => techKeywords.includes(w)).length;
    if (techCount >= 3) return '技术科普类';
    return '综合科普类';
  }

  evaluateContentValue(analysis) {
    const score = analysis.sentiment.positiveCount - analysis.sentiment.negativeCount + 5;
    if (score >= 8) return '⭐⭐⭐⭐⭐ 深度好文';
    if (score >= 6) return '⭐⭐⭐⭐ 有价值';
    if (score >= 4) return '⭐⭐⭐ 中规中矩';
    return '⭐⭐ 较浅显';
  }

  getAudience(topWords) {
    const devKeywords = ['开发', '代码', '引擎', 'Unity', '程序员'];
    if (topWords.filter(w => devKeywords.includes(w)).length >= 2) return '技术开发者';
    return '大众科普受众';
  }

  getLatestFiles() {
    if (!fs.existsSync(this.outputDir)) return [];
    return fs.readdirSync(this.outputDir)
      .filter(f => ['.json', '.txt', '.srt', '.ass', '.vtt'].includes(path.extname(f).toLowerCase()))
      .map(f => path.join(this.outputDir, f));
  }

  setBiliSubPath(customPath) {
    this.biliSubPath = customPath;
    console.log(`[配置] biliSub 路径已设置为: ${customPath}`);
  }
}

// CLI 入口
if (require.main === module) {
  const analyzer = new BilibiliSubtitleAnalyzer();
  
  const command = process.argv[2];
  const arg = process.argv[3];
  
  (async () => {
    try {
      switch (command) {
        case 'download':
          const files = await analyzer.downloadSubtitle(arg);
          console.log('[结果] 下载的文件:', files);
          break;
          
        case 'analyze':
          const result = analyzer.analyzeContent(arg);
          console.log(analyzer.generateReport(result, arg));
          break;
          
        case 'summary':
          console.log(analyzer.generateDetailedSummary(arg));
          break;
          
        case 'full':
          console.log('[开始] 下载字幕...');
          const fullFiles = await analyzer.downloadSubtitle(arg);
          console.log('[下载完成]', fullFiles);
          if (fullFiles.length > 0) {
            const jsonFile = fullFiles.find(f => f.endsWith('.json')) || fullFiles[0];
            console.log('\n' + analyzer.generateDetailedSummary(jsonFile));
          }
          break;
          
        case 'setpath':
          analyzer.setBiliSubPath(arg);
          break;
          
        default:
          console.log(`
🎬 Bilibili 字幕下载分析工具 v1.1

📖 使用方法:
  node index.js download <视频URL>     下载字幕
  node index.js analyze <字幕文件>   分析字幕内容
  node index.js summary <字幕文件>   生成详细总结
  node index.js full <视频URL>       一键下载+总结
  node index.js setpath <路径>       设置 biliSub 路径

📋 环境变量（可选）:
  BILISUB_PATH     - biliSub 项目路径
  BILI_PYTHON_LIB  - Python 库路径（如需要）
  BILI_PYTHON      - Python 解释器命令
  BILI_OUTPUT_DIR  - 输出目录
  BILI_PROXY       - 代理服务器
`);
      }
    } catch (error) {
      console.error('[错误]', error.message);
      process.exit(1);
    }
  })();
}

module.exports = BilibiliSubtitleAnalyzer;
