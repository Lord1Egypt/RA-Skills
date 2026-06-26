#!/usr/bin/env node
/**
 * 考题数据提取器
 * 扫描学习卡片和记忆文件，提取结构化数据供 AI 出题使用
 * 输出：memory/exam-questions/last-week-data.json
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  learningCardsDir: process.env.LEARNING_CARDS_DIR || '/home/admin/.openclaw/workspace/memory/learning-cards',
  memoryFeishuDir: '/home/admin/.openclaw/workspace/memory/feishu',
  memoryWebuiDir: '/home/admin/.openclaw/workspace/memory/webui',
  outputDir: process.env.EXAMS_DIR || '/home/admin/.openclaw/workspace/memory/exam-questions',
};

function getLastWeekRange() {
  const now = new Date();
  const beijingTime = new Date(now.getTime() + (8 * 60 * 60 * 1000));
  const dayOfWeek = beijingTime.getUTCDay();
  // Last Monday = today - (dayOfWeek - 1) - 7
  const offset = dayOfWeek === 0 ? 13 : dayOfWeek + 6;
  const lastMonday = new Date(beijingTime);
  lastMonday.setUTCDate(beijingTime.getUTCDate() - offset);
  lastMonday.setUTCHours(0, 0, 0, 0);
  const lastSunday = new Date(lastMonday);
  lastSunday.setUTCDate(lastMonday.getUTCDate() + 6);
  lastSunday.setUTCHours(23, 59, 59, 999);
  return { start: lastMonday, end: lastSunday, startStr: formatDate(lastMonday), endStr: formatDate(lastSunday) };
}

function formatDate(d) { return d.toISOString().split('T')[0]; }

function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

// 解析学习卡片（精炼版格式）
function parseLearningCard(content) {
  const result = { topics: [], decisions: [], pitfalls: [], concepts: [], quotes: [] };
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // 主题
    const topicMatch = line.match(/^[├└]─\s*主题\d+：(.+)$/);
    if (topicMatch) {
      const title = topicMatch[1].trim();
      const detailLines = [];
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        if (lines[j].match(/^[├└]─\s*(主题\d+|来源|重要度)/)) detailLines.push(lines[j].trim());
        else if (lines[j].match(/^---/) || lines[j].match(/^##\s/)) break;
      }
      result.topics.push({ title, detail: detailLines.join('; ') });
      continue;
    }

    // 决策
    const decMatch = line.match(/^[├└]─\s*决策\d+：(.+?)\s*→\s*(.+)$/);
    if (decMatch) {
      result.decisions.push({ decision: decMatch[1].trim(), choice: decMatch[2].trim(), reason: '' });
      continue;
    }
    if (line.match(/^\s+[├└]─\s*理由：(.+)$/) && result.decisions.length > 0) {
      result.decisions[result.decisions.length - 1].reason = line.match(/^\s+[├└]─\s*理由：(.+)$/)[1];
      continue;
    }

    // 踩坑
    const pitMatch = line.match(/^[├└]─\s*问题\d+：(.+)$/);
    if (pitMatch) {
      result.pitfalls.push({ problem: pitMatch[1].trim(), lesson: '', solution: '' });
      continue;
    }
    if (line.match(/^\s+[├└]─\s*解决方案：(.+)$/) && result.pitfalls.length > 0) {
      result.pitfalls[result.pitfalls.length - 1].solution = line.match(/^\s+[├└]─\s*解决方案：(.+)$/)[1];
      continue;
    }
    if (line.match(/^\s+[├└]─\s*教训：(.+)$/) && result.pitfalls.length > 0) {
      result.pitfalls[result.pitfalls.length - 1].lesson = line.match(/^\s+[├└]─\s*教训：(.+)$/)[1];
      continue;
    }

    // 概念
    const concMatch = line.match(/^[├└]─\s*概念\d+：(.+)$/);
    if (concMatch && concMatch[1].trim() !== '暂无') {
      result.concepts.push({ term: concMatch[1].trim(), definition: '' });
      continue;
    }

    // 金句（精炼版）
    if (line.match(/^[├└]─\s*(.+)/) && !line.match(/^[├└]─\s*(概念\d+|主题\d+|决策\d+|问题\d+|暂无)/)) {
      const text = line.replace(/^[├└]─\s*/, '').trim();
      if (text && !text.startsWith('暂无') && !text.startsWith('来源：') && !text.startsWith('原文件') && !text.startsWith('生成时间')) {
        // Check previous line for emoji marker
        const prevLine = i > 0 ? lines[i-1] : '';
        if (prevLine.match(/##\s*💬/)) {
          result.quotes.push(text);
        }
      }
    }
  }

  return result;
}

// 解析原始记忆文件（fallback，提取更有深度的内容）
function parseMemoryFile(content) {
  const sections = [];
  const lines = content.split('\n');
  let currentSection = { title: '', content: [] };
  let inSection = false;

  for (const line of lines) {
    const topicMatch = line.match(/^##\s*(?:新主题：|主题\d+[：:])\s*(.+)$/);
    if (topicMatch) {
      if (inSection && currentSection.content.length > 0) {
        sections.push({ ...currentSection, content: currentSection.content.join('\n') });
      }
      currentSection = { title: topicMatch[1].trim(), content: [] };
      inSection = true;
      continue;
    }
    if (line.match(/^##\s*(?:新主题|主题)/) && inSection && currentSection.content.length > 0) {
      sections.push({ ...currentSection, content: currentSection.content.join('\n') });
      currentSection = { title: '', content: [] };
      continue;
    }
    if (inSection) {
      currentSection.content.push(line);
    }
  }
  if (inSection && currentSection.content.length > 0) {
    sections.push({ ...currentSection, content: currentSection.content.join('\n') });
  }

  return sections;
}

// 从记忆文件中提取金句
function extractQuotes(content) {
  const quotes = [];
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Match: > "quote text"
    let qMatch = line.match(/^>\s*"(.+)"$/);
    if (!qMatch) qMatch = line.match(/^>\s*【?金句.*】?\s*"(.+)"$/);
    if (!qMatch) qMatch = line.match(/^>\s*(.+)$/);
    if (qMatch) {
      const quote = qMatch[1].trim();
      if (quote.length > 10 && !quote.includes('来源：') && !quote.includes('原文件') && !quote.includes('生成时间')) {
        quotes.push(quote);
        continue;
      }
    }
    // Match: **金句/洞见:** followed by >
    if (line.match(/金句/)) {
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        const nextLine = lines[j].trim();
        const qm = nextLine.match(/^>\s*"(.+)"$/);
        if (qm) quotes.push(qm[1]);
        else if (nextLine.match(/^>\s*(.+)$/) && !nextLine.match(/^>\s*$/)) {
          quotes.push(nextLine.replace(/^>\s*/, '').trim());
        }
        else if (nextLine === '' || nextLine.startsWith('#')) break;
      }
    }
  }
  return [...new Set(quotes)];
}

// 从记忆文件中提取踩坑
function extractPitfallsFromMemory(content) {
  const pitfalls = [];
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    // Match: - **问题：** ... - **解决方案：** ... - **教训：** ...
    const probMatch = lines[i].match(/^[-*]\s*\*\*问题[：:]\*\*\s*(.+)/);
    if (probMatch) {
      const pit = { problem: probMatch[1].trim(), solution: '', lesson: '' };
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        const solMatch = lines[j].match(/^[-*]\s*\*\*解决方案[：:]\*\*\s*(.+)/);
        if (solMatch) pit.solution = solMatch[1].trim();
        const lesMatch = lines[j].match(/^[-*]\s*\*\*教训[：:]\*\*\s*(.+)/);
        if (lesMatch) pit.lesson = lesMatch[1].trim();
        if (lines[j].match(/^##\s/) || lines[j].match(/^---$/)) break;
      }
      pitfalls.push(pit);
    }
  }
  return pitfalls;
}

// 从记忆文件中提取新概念
function extractConceptsFromMemory(content) {
  const concepts = [];
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const termMatch = lines[i].match(/^[-*]\s*\*\*术语[：:]\*\*\s*(.+)/);
    if (termMatch) {
      const concept = { term: termMatch[1].trim(), definition: '', scenario: '' };
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        const defMatch = lines[j].match(/^[-*]\s*\*\*定义[：:]\*\*\s*(.+)/);
        if (defMatch) concept.definition = defMatch[1].trim();
        const scMatch = lines[j].match(/^[-*]\s*\*\*应用场景[：:]\*\*\s*(.+)/);
        if (scMatch) concept.scenario = scMatch[1].trim();
        if (lines[j].match(/^##\s/) || lines[j].match(/^---$/)) break;
      }
      concepts.push(concept);
    }
  }
  return concepts;
}

// 主函数
function main() {
  const weekRange = getLastWeekRange();
  const weekNum = getWeekNumber(weekRange.start);
  const year = weekRange.start.getFullYear();

  const allData = {
    meta: {
      year, weekNum, weekRange, generatedAt: new Date().toISOString(),
      startStr: weekRange.startStr, endStr: weekRange.endStr
    },
    topics: [],
    decisions: [],
    pitfalls: [],
    concepts: [],
    quotes: [],
    sessionSections: [],  // Raw sections from memory files
    cardCount: 0,
    activeDays: 0,
    totalLinesOfMemory: 0
  };

  // 1. 扫描学习卡片
  for (let i = 0; i < 7; i++) {
    const d = new Date(weekRange.start);
    d.setDate(d.getDate() + i);
    if (d > weekRange.end) break;
    const dateStr = formatDate(d);
    const cardPath = path.join(CONFIG.learningCardsDir, `${dateStr}.md`);

    if (fs.existsSync(cardPath)) {
      const content = fs.readFileSync(cardPath, 'utf-8');
      // Skip "no content" cards
      if (content.includes('暂无学习内容') || content.includes('💭 昨日无学习记录') || content.includes('📭 昨日无学习记录')) continue;

      const parsed = parseLearningCard(content);
      allData.topics.push(...parsed.topics);
      allData.decisions.push(...parsed.decisions);
      allData.pitfalls.push(...parsed.pitfalls);
      allData.concepts.push(...parsed.concepts);
      allData.quotes.push(...parsed.quotes);
      allData.cardCount++;
      allData.activeDays++;
    }
  }

  // 2. 从原始记忆文件补充数据（fallback for sparse cards）
  for (const memDir of [CONFIG.memoryFeishuDir, CONFIG.memoryWebuiDir]) {
    for (let i = 0; i < 7; i++) {
      const d = new Date(weekRange.start);
      d.setDate(d.getDate() + i);
      if (d > weekRange.end) break;
      const dateStr = formatDate(d);
      const memPath = path.join(memDir, `${dateStr}.md`);

      if (fs.existsSync(memPath)) {
        const content = fs.readFileSync(memPath, 'utf-8');
        allData.totalLinesOfMemory += content.split('\n').length;

        // Extract sections
        const sections = parseMemoryFile(content);
        const channelLabel = memDir.includes('feishu') ? '飞书' : 'WebUI';
        sections.forEach(s => {
          allData.sessionSections.push({
            channel: channelLabel,
            date: dateStr,
            title: s.title,
            content: s.content.substring(0, 2000) // Cap to avoid huge files
          });
        });

        // Extract pitfalls and concepts
        const memPitfalls = extractPitfallsFromMemory(content);
        memPitfalls.forEach(p => {
          if (!allData.pitfalls.some(x => x.problem === p.problem)) {
            allData.pitfalls.push(p);
          }
        });

        const memConcepts = extractConceptsFromMemory(content);
        memConcepts.forEach(c => {
          if (!allData.concepts.some(x => x.term === c.term)) {
            allData.concepts.push(c);
          }
        });

        // Extract quotes
        const memQuotes = extractQuotes(content);
        memQuotes.forEach(q => {
          if (!allData.quotes.includes(q)) {
            allData.quotes.push(q);
          }
        });

        if (allData.activeDays === 0 && sections.length > 0) {
          allData.activeDays++;
        } else if (sections.length > 0) {
          // Count unique days with content
          const days = allData.sessionSections.map(s => s.date);
          allData.activeDays = new Set(days).size;
        }
      }
    }
  }

  // 3. 去重
  const seenTopicTitles = new Set();
  allData.topics = allData.topics.filter(t => {
    const key = t.title.toLowerCase();
    if (seenTopicTitles.has(key)) return false;
    seenTopicTitles.add(key);
    return true;
  });

  const seenPitfallProblems = new Set();
  allData.pitfalls = allData.pitfalls.filter(p => {
    const key = p.problem.toLowerCase().substring(0, 40);
    if (seenPitfallProblems.has(key)) return false;
    seenPitfallProblems.add(key);
    return true;
  });

  const seenConceptTerms = new Set();
  allData.concepts = allData.concepts.filter(c => {
    const key = c.term.toLowerCase();
    if (seenConceptTerms.has(key)) return false;
    seenConceptTerms.add(key);
    return true;
  });

  allData.quotes = [...new Set(allData.quotes)];

  // 4. 构建统计
  allData.stats = {
    cardCount: allData.cardCount,
    activeDays: allData.activeDays,
    totalTopics: allData.topics.length,
    totalDecisions: allData.decisions.length,
    totalPitfalls: allData.pitfalls.length,
    totalConcepts: allData.concepts.length,
    totalQuotes: allData.quotes.length,
    sessionSectionCount: allData.sessionSections.length,
    totalLinesOfMemory: allData.totalLinesOfMemory
  };

  // 5. 输出 JSON
  const outputPath = path.join(CONFIG.outputDir, 'last-week-data.json');
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(allData, null, 2), 'utf-8');

  // Also output to stdout for shell script
  console.log(JSON.stringify({
    status: 'ok',
    outputPath,
    stats: allData.stats,
    weekNum,
    weekRange: weekRange
  }));

  console.error(`✅ 考题数据已提取：${outputPath}`);
  console.error(`   活跃天数：${allData.stats.activeDays}`);
  console.error(`   主题：${allData.stats.totalTopics}  决策：${allData.stats.totalDecisions}  踩坑：${allData.stats.totalPitfalls}  概念：${allData.stats.totalConcepts}`);
}

main();