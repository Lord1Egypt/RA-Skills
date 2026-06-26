---
name: bilibili-subtitle-analysis
description: |
  B站字幕下载分析工具，基于 biliSub 项目。
  支持：下载字幕、批量下载、内容分析、内容分析报告。
  触发条件：用户要求下载B站字幕、分析字幕内容、生成内容报告。
---

# Bilibili 字幕下载分析 Skill

基于 [biliSub](https://github.com/lvusyy/biliSub) 项目实现。

## 功能

### 1. 字幕下载
- 单个视频字幕下载（官方字幕）
- 自动语音识别（ASR）生成字幕
- 支持多种格式：JSON, TXT, SRT, ASS, VTT

### 2. 内容分析
- **基础统计**：行数、字符数、平均行长、时间戳数量、视频时长
- **词频分析**：中文高频词 TOP 30、英文高频词 TOP 30
- **双词组分析**：bigrams TOP 20
- **情感分析**：正面/负面/中性判断，情感得分
- **关键词提取**：中英文关键词 TOP 10
- **文本密度**：有效文本行占比

### 3. 详细总结报告（默认行为）
下载字幕后自动整理成详细的中文总结报告，包含：
- **视频概览**：标题、时长、主题分类
- **核心内容**：分段总结，主要观点提炼
- **关键引用**：重要或精彩的原句摘录
- **结构化分析**：分类整理（技术点、案例、观点等）
- **一句话点评**：总结性评价

报告格式示例：
```
## 📺 视频总结：[视频标题]

**视频来源**：[BV号]
**视频时长**：X分钟
**主要内容**：一句话描述

---

### 🎮 核心内容
[分段详细总结，每段包含要点和原句]

### 💡 关键引用
- "摘录的精彩原句"

### 📊 结构化分析
| 类别 | 内容 |
|------|------|
| 分类1 | 要点 |

### 🎯 一句话点评
[总结评价]
```

## 使用方式

### 下载字幕
```
node index.js download <视频URL> [--formats json,txt] [--use-asr] [--asr-model small]
```

### 分析字幕
```
node index.js analyze <字幕文件路径>
```

### 批量下载
```
node index.js batch <URL列表文件路径>
```

### 设置 biliSub 路径
```
node index.js setpath <本地路径>
```

## Node.js API

```javascript
const BilibiliSubtitleAnalyzer = require('./index.js');

const analyzer = new BilibiliSubtitleAnalyzer({
  outputDir: './output',
  biliSubPath: 'C:\\Users\\lml\\biliSub',
  proxy: 'http://127.0.0.1:7890'
});

// 下载字幕
const files = await analyzer.downloadSubtitle('BV1xx411c79H', {
  formats: ['json', 'txt'],
  useAsr: true,
  asrModel: 'small'
});

// 分析字幕
const result = analyzer.analyzeContent('./output/BV1xx411c79H.json');

// 生成报告
const report = analyzer.generateReport(result, 'BV1xx411c79H');
console.log(report);
```

## 报告示例

```
╔══════════════════════════════════════════════════════════════════════╗
║                    📺 B站字幕内容分析报告                              ║
╚══════════════════════════════════════════════════════════════════════╝

🎬 视频信息: BV1xx411c79H

📊 字幕基础统计
───────────────────────────────────────────────────────────────────────
  • 总行数: 1250
  • 字符数（去空格）: 45000
  • 平均行长: 36.0 字符/行
  • 时间戳数量: 1250
  • 视频时长: 00:45:30

🔤 高频词 TOP 15（中）
  1. 你好: 45
  2. 我们: 38
  ...

💭 情感分析
  • 情感倾向: 🟡 中性
  • 情感得分: +5
```

## 安装依赖

```bash
# 克隆 biliSub 项目（MIT 许可证）
git clone https://github.com/lvusyy/biliSub

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 bilibili-api
pip install bilibili-api-python==17.1.2

# 可选：安装 whisper（用于 ASR）
pip install openai-whisper
```

## 许可证声明

本技能基于 MIT 许可证开源的 [biliSub](https://github.com/lvusyy/biliSub) 项目构建。
详细许可证声明请查看 [LICENSE](LICENSE) 文件。

## 注意事项

1. 使用 ASR 功能需要安装 ffmpeg
2. 批量下载时注意控制并发（默认 3）
3. 长视频处理可能需要较长时间（尤其 ASR）
