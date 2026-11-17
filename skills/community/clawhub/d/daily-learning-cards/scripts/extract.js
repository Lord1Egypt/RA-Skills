#!/usr/bin/env node
/**
 * 学习卡片内容提取器
 * 读取记忆文件，提取结构化内容，输出 JSON
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 默认基础配置（与 load-config.js 保持一致）
const BASE_CONFIG = {
  channels: { sources: ['feishu', 'webui'], delivery: 'feishu' }
};

// 加载用户配置
function loadUserConfig() {
  const configPath = path.join(os.homedir(), '.daily-learning-cards', 'config.json');
  try {
    if (fs.existsSync(configPath)) {
      const raw = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      // 深度合并默认值，确保 channels 等缺失字段有默认值
      return {
        ...BASE_CONFIG,
        ...raw,
        channels: { ...BASE_CONFIG.channels, ...(raw.channels || {}) }
      };
    }
  } catch (e) {
    console.error('Config load error:', e.message);
  }
  return { ...BASE_CONFIG };
}

const userConfig = loadUserConfig();

// 配置
// 默认渠道列表
const DEFAULT_CHANNELS = [
  { key: 'feishu', dir: 'feishu', label: '飞书' },
  { key: 'webui', dir: 'webui', label: 'WebUI' },
  { key: 'dingtalk', dir: 'dingtalk', label: '钉钉' },
  { key: 'weixin', dir: 'weixin', label: '微信' },
];

// 从用户配置读取启用的渠道，默认 feishu + webui
function getEnabledChannels() {
  const userSources = userConfig.channels?.sources;
  if (Array.isArray(userSources) && userSources.length > 0) {
    return DEFAULT_CHANNELS.filter(c => userSources.includes(c.key));
  }
  return DEFAULT_CHANNELS.filter(c => c.key === 'feishu' || c.key === 'webui');
}

const CONFIG = {
  workspaceDir: process.env.WORKSPACE_DIR || '/home/admin/.openclaw/workspace',
  channels: getEnabledChannels(),
  maxTopics: userConfig.extract?.maxTopics || 20,
  maxPitfalls: userConfig.extract?.maxPitfalls || 6,
  maxConcepts: userConfig.extract?.maxConcepts || 6,
  maxInsights: userConfig.extract?.maxInsights || 6,
};

// 安全读取文件
function safeRead(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (e) {
    return null;
  }
}

// 解析记忆文件内容
function parseMemory(content) {
  const result = {
    topics: [],
    decisions: [],
    pitfalls: [],
    concepts: [],
    insights: [],
    actions: [],
    rawContent: content
  };

  if (!content) return result;

  const lines = content.split('\n');
  let currentSection = null;
  let currentTopic = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // 检测主题（## 主题 / ## 主题 1 / ## Topic）
    const topicMatch = line.match(/^##\s*(?:新?主题|Topic)\s*(?:\d+\s*)?[：:]\s*(.+)$/i);
    if (topicMatch) {
      const topicTitle = topicMatch[1].trim();
      if (topicTitle) {
        currentTopic = {
          type: 'topic',
          title: topicTitle,
          line: i,
          tasks: { P0: [], P1: [], P2: [] },
          keyDecisions: []
        };
        result.topics.push(currentTopic);
      }
      currentSection = 'topic';
    }
    else if (line.match(/^### 时间：/)) {
      // 时间标记，记录上下文
      currentSection = 'time';
      currentTopic = null;
    }

    // 检测任务小节（### P0 任务 / ### P0 Tasks）
    else if (line.match(/^###\s*P([012])\s*(?:任务|Tasks)/i)) {
      const priority = 'P' + line.match(/^###\s*P([012])\s*(?:任务|Tasks)/i)[1];
      currentSection = 'task-' + priority;
    }
    // 检测任务表格中的完成项（支持中英文表头）
    else if (currentSection && currentSection.startsWith('task-') && line.match(/^\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|$/)) {
      const parts = line.split('|').map(p => p.trim()).filter(p => p);
      // 跳过表头行（中文或英文）
      const isHeader = parts[0] === '改进项' || parts[0] === 'Task' || 
                       parts[0] === 'Item' || parts[0].toLowerCase() === 'task';
      if (parts.length >= 4 && !isHeader) {
        const status = parts[3];
        // 支持多种完成标记
        if (status.includes('✅') || status.includes('完成') || status.includes('Done') || status.includes('Complete')) {
          const priority = currentSection.replace('task-', '');
          const taskName = parts[0].replace(/\*\*/g, '');
          if (currentTopic) {
            currentTopic.tasks[priority].push(taskName);
          }
        }
      }
    }

    // 检测关键决策小节（### 关键决策 / ### Key Decisions）
    else if (line.match(/^###\s*(?:关键决策|Key Decisions)/i)) {
      currentSection = 'key-decision';
    }
    // 检测关键决策表格
    else if (currentSection === 'key-decision' && line.match(/^\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|$/)) {
      const parts = line.split('|').map(p => p.trim()).filter(p => p);
      // 过滤掉表头行和分隔行（中文或英文）
      const isHeader = parts[0] === '决策点' || parts[0] === 'Decision' ||
                       parts[0].toLowerCase() === 'decision point';
      const isSeparator = parts[0].match(/^-+$/) || parts[0].includes('---');
      if (parts.length >= 4 && !isHeader && !isSeparator) {
        if (currentTopic) {
          currentTopic.keyDecisions.push({
            decision: parts[0],
            choice: parts[2],
            reason: parts[3]
          });
        }
      }
    }

    // 检测决策过程表格（决策过程 / Decision Process）
    // 支持多种形式：### 决策过程、**决策过程：**、决策过程：
    else if (line.match(/^###\s*(?:决策过程|Decision Process)/i) || 
             line.match(/^\*\*决策过程[：:]\*\*/i) ||
             line.match(/^##\s*(?:决策|Decisions)/i) ||
             line.includes('**决策')) {
      currentSection = 'decision';
    }
    // 检测决策表格（3列或4列）
    else if (currentSection === 'decision' && line.match(/^\|[^|]+\|[^|]+\|[^|]+\|/)) {
      const parts = line.split('|').map(p => p.trim()).filter(p => p);
      // 跳过表头行（中文或英文）和分隔行
      const isHeader = parts[0] === '选项' || parts[0] === '层级' || parts[0] === 'Option' ||
                       parts[0].toLowerCase() === 'choice' || parts[0].match(/^-+$/);
      if (parts.length >= 3 && !isHeader) {
        result.decisions.push({
          option: parts[0],
          factors: parts[1],
          result: parts[2]
        });
      }
    }

    // 检测踩坑记录标题（踩坑记录 / Pitfalls）
    // 支持多种形式：### 踩坑记录、**踩坑记录：**、## 踩坑记录
    else if (line.match(/^###\s*(?:踩坑记录|Pitfalls)/i) || 
             line.match(/^\*\*踩坑记录[：:]\*\*/i) ||
             line.match(/^##\s*(?:踩坑|Pitfalls)/i)) {
      currentSection = 'pitfall';
    }
    // 检测踩坑记录内容（问题 / Problem）
    // 支持列表格式：- **问题：** 或 粗体格式：**问题：**
    else if (line.match(/^-?\s*\*\*(?:问题|Problem)[：:]\*\*(.+)$/i) ||
             (currentSection === 'pitfall' && line.match(/^\*\*(?:问题|Problem)[：:]\*\*(.+)$/i))) {
      const problem = line.replace(/^-?\s*\*\*(?:问题|Problem)[：:]\*\*/i, '').trim();
      // 查找解决方案和教训（接下来的几行）
      let solution = '';
      let lesson = '';
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        const nextLine = lines[j].trim();
        // 支持多种格式：- **解决方案：**、**解决方案：**、- 解决方案：
        if (nextLine.match(/^-?\s*\*\*(?:解决方案|Solution|Root Cause)[：:]\*\*(.+)$/i)) {
          solution = nextLine.replace(/^-?\s*\*\*(?:解决方案|Solution|Root Cause)[：:]\*\*/i, '').trim();
        }
        if (nextLine.match(/^-?\s*\*\*(?:教训|Lesson)[：:]\*\*(.+)$/i)) {
          lesson = nextLine.replace(/^-?\s*\*\*(?:教训|Lesson)[：:]\*\*/i, '').trim();
        }
        // 如果遇到新的问题或空行分隔，停止查找
        if (nextLine.match(/^\*\*(?:问题|Problem)[：:]\*\*/i) && j > i + 1) break;
        if (nextLine.match(/^##/)) break;
      }
      result.pitfalls.push({ problem, solution, lesson });
      currentSection = 'pitfall';
    }

    // 检测新概念标题（新概念 / New Concepts / 关键概念）
    // 支持多种形式：### 新概念、**新概念：**、## 新概念、**关键概念：**
    else if (line.match(/^###\s*(?:新概念|New Concepts)/i) || 
             line.match(/^\*\*(?:新概念|关键概念)[：:]\*\*/i) ||
             line.match(/^##\s*(?:新概念|Concepts|关键概念)/i)) {
      currentSection = 'concept';
    }
    // 检测新概念内容（术语 / Term / 任意粗体键值对）
    // 支持两种格式：
    //   格式A（AGENTS.md标准）：**术语：**值  （冒号在粗体内）
    //   格式B（备用）：**术语**：值  （冒号在粗体外）
    // 改进：不依赖 currentSection，而是检测上下文（前面是否有概念标题）
    else if (line.match(/^-?\s*\*\*[^*]+\*\*[：:].+$/i) ||  // 格式B：**术语**：值
             line.match(/^-?\s*\*\*[^*：:]+[：:]\*\*.+$/i)) { // 格式A：**术语：**值
      // 检查前面10行内是否有概念标题
      let hasConceptHeader = false;
      for (let k = Math.max(0, i - 10); k < i; k++) {
        if (lines[k].match(/^\*\*(?:新概念|关键概念)[：:]\*\*/i) ||
            lines[k].match(/^###\s*(?:新概念|New Concepts)/i) ||
            lines[k].match(/^##\s*(?:新概念|Concepts|关键概念)/i)) {
          hasConceptHeader = true;
          break;
        }
      }
      // 同时检查 currentSection 作为备选（兼容旧格式）
      if (hasConceptHeader || currentSection === 'concept') {
        // 提取 **键**：值 格式（支持两种冒号位置）
        // 格式A：**术语：**值
        let match = line.match(/^-?\s*\*\*([^*：:]+)[：:]\*\*(.+)$/i);
        if (!match) {
          // 格式B：**术语**：值
          match = line.match(/^-?\s*\*\*([^*]+)\*\*[：:](.+)$/i);
        }
        if (match) {
          const key = match[1].trim();
          const value = match[2].trim();
          // 如果 key 是"术语"，它就是概念本身的名称 → term = value, definition + scenario 来自后续行
          if (key === '术语' || key === '术语（Term）') {
            // 查找后续的定义/应用场景行
            let conceptDef = '';
            let conceptScenario = '';
            let skipUntil = i;
            for (let j = i + 1; j < Math.min(i + 5, lines.length); j++) {
              const nextLine = lines[j].trim();
              if (!nextLine) break;
              if (nextLine.match(/^-?\s*\*\*(?:新概念|关键概念|金句)/i)) break;
              if (nextLine.match(/^-?\s*\*\*(?:定义|定义（Definition）)[：:]\*\*(.+)$/i)) {
                const dm = nextLine.match(/^-?\s*\*\*(?:定义|定义（Definition）)[：:]\*\*(.+)$/i);
                if (dm) conceptDef = dm[1].trim();
                skipUntil = j;
              } else if (nextLine.match(/^-?\s*\*\*(?:应用场景|应用场景（Application）)[：:]\*\*(.+)$/i)) {
                const sm = nextLine.match(/^-?\s*\*\*(?:应用场景|应用场景（Application）)[：:]\*\*(.+)$/i);
                if (sm) conceptScenario = sm[1].trim();
                skipUntil = j;
              } else if (nextLine.match(/^-?\s*\*\*(?:来源|来源（Source）)[：:]\*\*(.+)$/i)) {
                const srcM = nextLine.match(/^-?\s*\*\*(?:来源|来源（Source）)[：:]\*\*(.+)$/i);
                if (srcM) conceptDef += '（来源：' + srcM[1].trim() + '）';
                skipUntil = j;
              } else if (nextLine.match(/^-?\s*\*\*[^*]+\*\*[：:]/)) {
                // 其他粗体条目，停止扫描（不会是术语的附属字段）
                break;
              } else {
                // 普通文本，追加到定义
                if (nextLine && !nextLine.match(/^#/) && !nextLine.match(/^---/)) {
                  conceptDef += ' ' + nextLine;
                }
              }
            }
            // 记录已处理行，避免外层循环重复处理这些附属行
            if (skipUntil > i) {
              i = skipUntil;
            }
            result.concepts.push({ term: value, definition: conceptDef, scenario: conceptScenario });
          }
          // 定义/应用场景/来源 等是前一个概念的附属字段，追加到最后一条概念
          else if (['定义', '定义（Definition）', '应用场景', '应用场景（Application）', '来源', '来源（Source）'].includes(key)) {
            if (result.concepts.length > 0) {
              const last = result.concepts[result.concepts.length - 1];
              if (key === '定义' || key === '定义（Definition）') {
                last.definition += ' | ' + value;
              } else if (key === '应用场景' || key === '应用场景（Application）') {
                last.scenario = value;
              } else if (key === '来源' || key === '来源（Source）') {
                last.definition += '（来源：' + value + '）';
              }
            }
          } else {
            // 正常概念条目
            result.concepts.push({ term: key, definition: value, scenario: '' });
          }
        }
      }
    }

    // 检测金句/洞见（引用格式 > ）
    else if (line.match(/^> "?(.+)"?$/)) {
      const insight = line.replace(/^> "?/, '').replace(/"?$/, '').trim();
      if (insight.length > 10) {
        result.insights.push(insight);
      }
    }

    // 检测关键数据
    else if (line.match(/关键数据|数据X/)) {
      currentSection = 'data';
    }
  }

  // 为每个主题添加 topicRawContent（从主题起始行到下一个主题之前的内容）
  const allLines = content.split('\n');
  result.topics.forEach((topic, idx) => {
    const startLine = topic.line;
    const endLine = (idx < result.topics.length - 1) ? result.topics[idx + 1].line - 1 : allLines.length;
    topic.topicRawContent = allLines.slice(startLine, endLine + 1).join('\n');
  });

  return result;
}

// 主函数
function main() {
  const date = process.argv[2] || new Date().toISOString().split('T')[0];
  
  const result = {
    status: 'ok',
    date,
    generatedAt: new Date().toISOString(),
    sources: {},
    channels: {},  // 动态渠道对象，key = 渠道名
    hasContent: false,
    stats: {
      topics: 0,
      decisions: 0,
      pitfalls: 0,
      concepts: 0,
      insights: 0
    }
  };

  // 遍历所有启用的渠道
  for (const ch of CONFIG.channels) {
    const channelDir = path.join(CONFIG.workspaceDir, 'memory', ch.dir);
    const channelFile = path.join(channelDir, `${date}.md`);
    const content = safeRead(channelFile);
    
    result.sources[ch.key] = channelFile;
    result.channels[ch.key] = content ? parseMemory(content) : null;
    
    if (content) result.hasContent = true;
  }

  // 应用限制（取前 N 个）
  for (const ch of CONFIG.channels) {
    const data = result.channels[ch.key];
    if (data) {
      data.topics = data.topics.slice(0, CONFIG.maxTopics);
      data.pitfalls = data.pitfalls.slice(0, CONFIG.maxPitfalls);
      data.concepts = data.concepts.slice(0, CONFIG.maxConcepts);
      data.insights = data.insights.slice(0, CONFIG.maxInsights);
    }
  }

  // 统计（应用限制后）
  for (const ch of CONFIG.channels) {
    const data = result.channels[ch.key];
    if (data) {
      result.stats.topics += data.topics.length;
      result.stats.decisions += data.decisions.length;
      result.stats.pitfalls += data.pitfalls.length;
      result.stats.concepts += data.concepts.length;
      result.stats.insights += data.insights.length;
    }
  }

  console.log(JSON.stringify(result, null, 2));
}

main();
