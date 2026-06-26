#!/usr/bin/env node
/**
 * 每周考题生成器
 * 扫描上周学习卡片，生成 20 道题（15 单选 + 5 多选）
 * 规则生成模式（AI 生成通过 cron 触发）
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  learningCardsDir: process.env.LEARNING_CARDS_DIR || '/home/admin/.openclaw/workspace/memory/learning-cards',
  examsDir: process.env.EXAMS_DIR || '/home/admin/.openclaw/workspace/memory/exam-questions',
};

// 获取上周日期范围（使用上海时区）
function getLastWeekRange() {
  const now = new Date();
  const beijingTime = new Date(now.getTime() + (8 * 60 * 60 * 1000));
  const dayOfWeek = beijingTime.getUTCDay();
  const lastMonday = new Date(beijingTime);
  lastMonday.setUTCDate(beijingTime.getUTCDate() - dayOfWeek - 6);
  lastMonday.setUTCHours(0, 0, 0, 0);
  const lastSunday = new Date(beijingTime);
  lastSunday.setUTCDate(beijingTime.getUTCDate() - dayOfWeek);
  lastSunday.setUTCHours(23, 59, 59, 999);
  return {
    start: lastMonday,
    end: lastSunday,
    startStr: lastMonday.toISOString().split('T')[0],
    endStr: lastSunday.toISOString().split('T')[0]
  };
}

// 获取周数
function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

// 扫描上周学习卡片
function scanLastWeekCards() {
  const weekRange = getLastWeekRange();
  const cards = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(weekRange.start);
    d.setDate(d.getDate() + i);
    if (d > weekRange.end) break;
    const dateStr = d.toISOString().split('T')[0];
    const cardPath = path.join(CONFIG.learningCardsDir, `${dateStr}.md`);
    if (fs.existsSync(cardPath)) {
      const content = fs.readFileSync(cardPath, 'utf-8');
      cards.push({ date: dateStr, content, path: cardPath });
    }
  }
  return { cards, weekRange };
}

// 解析学习卡片内容
function parseCard(content) {
  const topics = [], decisions = [], pitfalls = [], concepts = [];
  const lines = content.split('\n');
  let currentSection = null;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.match(/^##\s*📚\s*核心主题/i)) currentSection = 'topics';
    else if (currentSection === 'topics' && line.match(/^[├└]─\s*主题\d+：(.+)$/)) {
      const title = line.match(/^[├└]─\s*主题\d+：(.+)$/)[1];
      const tasks = { P0: [], P1: [], P2: [] };
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        const taskLine = lines[j];
        if (taskLine.match(/^[├└]─\s*来源：/)) continue;
        const pMatch = taskLine.match(/^\s+[├└]─\s*(P[012])：(.+)$/);
        if (pMatch) { tasks[pMatch[1]] = pMatch[2].split('、').map(t => t.trim()); }
        else if (taskLine.match(/^---$/)) break;
      }
      topics.push({ title, tasks });
    }
    else if (line.match(/^##\s*📋\s*重要决策/i)) currentSection = 'decisions';
    else if (currentSection === 'decisions' && line.match(/^[├└]─\s*决策\d+：(.+?)\s*→\s*(.+)$/)) {
      const match = line.match(/^[├└]─\s*决策\d+：(.+?)\s*→\s*(.+)$/);
      decisions.push({ decision: match[1].trim(), choice: match[2].trim(), reason: '' });
    }
    else if (currentSection === 'decisions' && line.match(/^\s+[├└]─\s*理由：(.+)$/)) {
      if (decisions.length > 0) decisions[decisions.length - 1].reason = line.match(/^\s+[├└]─\s*理由：(.+)$/)[1];
    }
    else if (line.match(/^##\s*⚠️\s*踩坑记录/i)) currentSection = 'pitfalls';
    else if (currentSection === 'pitfalls' && line.match(/^[├└]─\s*问题\d+：(.+)$/)) {
      pitfalls.push({ problem: line.match(/^[├└]─\s*问题\d+：(.+)$/)[1], lesson: '' });
    }
    else if (currentSection === 'pitfalls' && line.match(/^\s+[├└]─\s*教训：(.+)$/)) {
      if (pitfalls.length > 0) pitfalls[pitfalls.length - 1].lesson = line.match(/^\s+[├└]─\s*教训：(.+)$/)[1];
    }
    else if (line.match(/^##\s*🧠\s*新概念/i)) currentSection = 'concepts';
    else if (currentSection === 'concepts' && line.match(/^[├└]─\s*概念\d+：(.+)$/)) {
      const term = line.match(/^[├└]─\s*概念\d+：(.+)$/)[1];
      if (term !== '暂无') concepts.push({ term, definition: '' });
    }
  }
  return { topics, decisions, pitfalls, concepts };
}

// 生成单选题（基于 AGENTS.md 规则）
function generateSingleChoiceQuestions(materials, count = 15) {
  const questions = [];
  let qNum = 1;
  materials.topics.forEach(topic => {
    if (questions.length >= count) return;
    const p0Tasks = topic.tasks?.P0 || [];
    const p0Preview = p0Tasks.slice(0, 2).join('、') || '核心功能';
    questions.push({
      num: qNum++, type: 'single', category: '主题', source: topic.title,
      question: `面对「${topic.title}」，当资源有限时，以下哪种优先级排序最合理？`,
      options: [
        `A. 优先完成 P0 任务（${p0Preview}），P1/P2 延后`,
        'B. 平均分配资源，P0/P1/P2 同步推进',
        'C. 先做 P2 简单任务建立信心，再处理 P0',
        'D. 跳过 P0 直接做 P1，因为 P0 太难'
      ],
      answer: 'A',
      explanation: `P0 是核心优先级，必须优先完成。B 导致资源分散，C 本末倒置，D 逃避核心问题。`
    });
  });
  materials.decisions.forEach(decision => {
    if (questions.length >= count) return;
    const reasons = decision.reason ? decision.reason.split(/[，,]/) : ['需要进一步验证'];
    const mainReason = reasons[0] || '综合考量';
    questions.push({
      num: qNum++, type: 'single', category: '决策', source: decision.decision,
      question: `在「${decision.decision}」的决策中，选择「${decision.choice}」的核心理由是什么？`,
      options: [
        `A. ${mainReason}`,
        'B. 这是最简单省力的方案',
        'C. 这是成本最低的方案',
        'D. 这是大多数人选择的方案'
      ],
      answer: 'A',
      explanation: `决策依据是：${decision.reason || '综合考量'}。B/C/D 都是表面因素。`
    });
  });
  materials.pitfalls.forEach(pitfall => {
    if (questions.length >= count) return;
    const lesson = pitfall.lesson || '需要验证后再执行';
    questions.push({
      num: qNum++, type: 'single', category: '踩坑', source: pitfall.problem,
      question: `遇到「${pitfall.problem}」时，以下哪种做法最能避免重蹈覆辙？`,
      options: [
        `A. ${lesson}`,
        'B. 下次更加小心谨慎',
        'C. 寻求他人帮助',
        'D. 暂时搁置这个问题'
      ],
      answer: 'A',
      explanation: `踩坑教训是：${lesson}。B 是空话，C/D 没有解决根本问题。`
    });
  });
  materials.concepts.forEach(concept => {
    if (questions.length >= count) return;
    questions.push({
      num: qNum++, type: 'single', category: '新概念', source: concept.term,
      question: `「${concept.term}」这个概念最适合应用于以下哪种场景？`,
      options: [
        'A. 需要系统化记录决策过程时',
        'B. 需要快速做出直觉判断时',
        'C. 需要与他人争论对错时',
        'D. 需要推迟决策等待更多信息时'
      ],
      answer: 'A',
      explanation: `新概念用于扩展认知框架，最适合在系统记录决策时应用。`
    });
  });
  const agentPrinciples = [
    { topic: '第一性原理', question: '当市场说"这次像 2015 年"时，按第一性原理应该？', answer: 'A',
      options: ['A. 分解到基础层（资金流向/纳什均衡），而非类比', 'B. 参考 2015 年的历史数据', 'C. 询问专家意见', 'D. 等待市场验证'],
      explanation: '第一性原理强制分解到基础层，拒绝类比论证。' },
    { topic: '反共识验证', question: '当市场一致看多时，按反共识验证原则应该？', answer: 'A',
      options: ['A. 自动寻找做空证据（热力学约束/红皇后效应）', 'B. 跟随市场趋势加仓', 'C. 保持现状不动', 'D. 减仓避险'],
      explanation: '反共识验证要求在市场一致看多时寻找做空证据。' },
    { topic: '不确定性量化', question: '以下哪种表述符合"不确定性量化"原则？', answer: 'A',
      options: ['A. "胜率 32%±5%，置信区间源于样本量不足"', 'B. "可能涨，也可能跌"', 'C. "大概率会涨"', 'D. "风险可控"'],
      explanation: '必须给出概率区间 + 置信度，禁止"可能""大概"等含混表述。' }
  ];
  agentPrinciples.forEach(p => {
    if (questions.length >= count) return;
    questions.push({ num: qNum++, type: 'single', category: 'AGENTS.md 原则', source: p.topic, question: p.question, options: p.options, answer: p.answer, explanation: p.explanation });
  });
  return questions.slice(0, count);
}

// 生成多选题
function generateMultiChoiceQuestions(materials, count = 5) {
  const questions = [];
  let qNum = 16;
  const topicTitles = materials.topics.map(t => t.title).slice(0, 3);
  if (topicTitles.length > 0) {
    questions.push({
      num: qNum++, type: 'multi', category: '综合', source: '本周主题',
      question: '上周学习的核心主题包括以下哪些？（多选）',
      options: [`A. ${topicTitles[0] || '主题1'}`, `B. ${topicTitles[1] || '主题2'}`, `C. ${topicTitles[2] || '主题3'}`, 'D. 以上都不是'],
      answer: topicTitles.map((_, i) => String.fromCharCode(65 + i)).join(''),
      explanation: `上周学习的核心主题包括：${topicTitles.join('、')}。`
    });
  }
  materials.decisions.slice(0, 2).forEach(decision => {
    if (questions.length >= count) return;
    questions.push({
      num: qNum++, type: 'multi', category: '决策', source: decision.decision,
      question: `关于「${decision.decision}」的决策，以下说法正确的是？（多选）`,
      options: [`A. 最终选择了「${decision.choice}」`, `B. 决策理由是：${decision.reason}`, 'C. 这是一个临时决定，后续可能改变', 'D. 没有经过深思熟虑'],
      answer: 'AB',
      explanation: `根据学习记录，最终选择是「${decision.choice}」，理由是：${decision.reason}。`
    });
  });
  materials.pitfalls.slice(0, 2).forEach(pitfall => {
    if (questions.length >= count) return;
    questions.push({
      num: qNum++, type: 'multi', category: '踩坑', source: pitfall.problem,
      question: `「${pitfall.problem}」这个踩坑经历告诉我们什么？（多选）`,
      options: [`A. 问题：${pitfall.problem}`, `B. 教训：${pitfall.lesson}`, 'C. 这是一个常见错误，需要避免', 'D. 这个错误不值得记录'],
      answer: 'ABC',
      explanation: `根据踩坑记录，问题是「${pitfall.problem}」，教训是「${pitfall.lesson}」。`
    });
  });
  return questions.slice(0, count);
}

// 生成考试内容
function generateExam() {
  const { cards, weekRange } = scanLastWeekCards();
  if (cards.length === 0) return { hasContent: false, message: '上周没有学习记录，无法生成考题。' };
  const allMaterials = { topics: [], decisions: [], pitfalls: [], concepts: [] };
  cards.forEach(card => {
    const parsed = parseCard(card.content);
    allMaterials.topics.push(...parsed.topics);
    allMaterials.decisions.push(...parsed.decisions);
    allMaterials.pitfalls.push(...parsed.pitfalls);
    allMaterials.concepts.push(...parsed.concepts);
  });
  const singleChoice = generateSingleChoiceQuestions(allMaterials, 15);
  const multiChoice = generateMultiChoiceQuestions(allMaterials, 5);
  const weekNum = getWeekNumber(weekRange.start);
  const year = weekRange.start.getFullYear();
  return { hasContent: true, year, weekNum, weekRange, materials: allMaterials, questions: [...singleChoice, ...multiChoice], singleChoice, multiChoice };
}

// 格式化考试输出
function formatExam(exam) {
  const { year, weekNum, weekRange, questions, singleChoice, multiChoice } = exam;
  let output = `📝 本周学习测试（第 ${weekNum} 周）\n\n📚 测试范围：${weekRange.startStr} 至 ${weekRange.endStr}\n📊 题目数量：20 道（15 单选 + 5 多选）\n⏰ 建议用时：30 分钟\n\n---\n\n## 单选题（15 道）\n\n`;
  singleChoice.forEach(q => {
    output += `${q.num}. 【${q.category}】${q.question}\n`;
    q.options.forEach(opt => output += `   ${opt}\n`);
    output += '\n';
  });
  output += `---\n\n## 多选题（5 道）\n\n`;
  multiChoice.forEach(q => {
    output += `${q.num}. 【${q.category}】${q.question}\n`;
    q.options.forEach(opt => output += `   ${opt}\n`);
    output += '\n';
  });
  output += `---\n\n<details>\n<summary>📎 点击查看答案与解析</summary>\n\n## 答案与解析\n\n`;
  questions.forEach(q => output += `**${q.num}. 答案：${q.answer}**\n> ${q.explanation}\n\n`);
  output += `</details>\n\n---\n\n💬 **提交答案**\n直接回复题号和选项，如：\`1A 2B 3C...\`\n或口述错题编号，如：\`第 5 题和第 12 题错了\`\n\n---\n💃 金银 Planet · 自我提升部\n`;
  return output;
}

// 主函数
function main() {
  const exam = generateExam();
  if (!exam.hasContent) { console.log(exam.message); process.exit(0); }
  const examContent = formatExam(exam);
  console.log(examContent);
  const examFile = path.join(CONFIG.examsDir, `${exam.year}-W${exam.weekNum}-exam.md`);
  fs.mkdirSync(CONFIG.examsDir, { recursive: true });
  fs.writeFileSync(examFile, examContent, 'utf-8');
  console.error(`✅ 考题已生成：${examFile}`);
}

main();
