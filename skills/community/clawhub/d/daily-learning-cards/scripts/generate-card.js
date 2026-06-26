#!/usr/bin/env node
/**
 * 学习卡片生成器
 * 读取 extract.js 输出的 JSON，生成 Markdown 学习卡片
 */

const fs = require('fs');
const path = require('path');
const { t, getUserLanguage } = require('./i18n');

// 配置
const CONFIG = {
  learningCardsDir: process.env.LEARNING_CARDS_DIR || '/home/admin/.openclaw/workspace/memory/learning-cards',
};

// 获取语言设置
const LANG = process.env.LEARNING_CARDS_LANG || getUserLanguage();

// 生成学习卡片
function generateCard(data) {
  const date = data.date;
  const stats = data.stats;
  
  // 合并多渠道内容
  const allTopics = [];
  const allDecisions = [];
  const allPitfalls = [];
  const allConcepts = [];
  const allInsights = [];

  // 渠道标签映射
  const channelLabels = {
    feishu: '飞书',
    webui: 'WebUI',
    dingtalk: '钉钉',
    weixin: '微信'
  };

  for (const [chKey, chData] of Object.entries(data.channels || {})) {
    if (!chData) continue;
    const label = channelLabels[chKey] || chKey;
    allTopics.push(...(chData.topics || []).map(t => ({ ...t, channel: label })));
    allDecisions.push(...(chData.decisions || []).map(d => ({ ...d, channel: label })));
    allPitfalls.push(...(chData.pitfalls || []).map(p => ({ ...p, channel: label })));
    allConcepts.push(...(chData.concepts || []).map(c => ({ ...c, channel: label })));
    allInsights.push(...(chData.insights || []).map(i => ({ text: i, channel: label })));
  }

  // 去重
  const uniqueTopics = allTopics.filter((t, i, arr) => 
    arr.findIndex(x => x.title === t.title) === i
  );
  const uniqueInsights = allInsights.filter((i, idx, arr) => 
    arr.findIndex(x => x.text === i.text) === idx
  );

  // 按重要性排序主题（重要性评分：踩坑 +3、新概念 +3、金句 +2）
  const scoredTopics = uniqueTopics.map(t => {
    let score = 0;
    if (allPitfalls.some(p => p.problem && t.topicRawContent?.includes(p.problem))) score += 3;
    if (allConcepts.some(c => c.term && t.topicRawContent?.includes(c.term))) score += 3;
    if (allInsights.some(i => t.topicRawContent?.includes(i.text))) score += 2;
    return { ...t, score };
  });
  
  // 按分数降序排序，取前 10 个
  const sortedTopics = scoredTopics
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);

  // 收集所有决策（通用决策表格 + 主题下的关键决策）
  const allKeyDecisions = [];
  
  // 从通用决策表格收集
  allDecisions.forEach(d => {
    if (d.option && d.option !== '------') {
      allKeyDecisions.push({
        decision: d.option,
        choice: d.result,
        reason: d.factors,
        channel: d.channel
      });
    }
  });
  
  // 从主题下的关键决策收集
  uniqueTopics.forEach(topic => {
    if (topic.keyDecisions && topic.keyDecisions.length > 0) {
      topic.keyDecisions.forEach(kd => {
        allKeyDecisions.push({
          decision: kd.decision,
          choice: kd.choice,
          reason: kd.reason,
          channel: topic.channel
        });
      });
    }
  });

  // 生成卡片内容（支持多语言）
  const activeChannels = Object.entries(data.channels || {})
    .filter(([_, v]) => v)
    .map(([k]) => channelLabels[k] || k);
  const channelLabel = activeChannels.length > 0 ? activeChannels.join(' + ') : t('unknown', LANG);
  const unitCount = LANG === 'en' ? '' : (LANG === 'bilingual' ? '个 / ' : '个');
  const unitPieces = LANG === 'en' ? '' : (LANG === 'bilingual' ? '条 / ' : '条');
  const enCount = LANG === 'bilingual' ? ' / ' : '';
  
  let cardContent = `# ${t('title', LANG)} - ${date}

📊 **${t('stats', LANG)}**
├─ 📚 ${t('topics', LANG)}：${uniqueTopics.length}${unitCount}${enCount}${LANG === 'bilingual' ? uniqueTopics.length : ''}
├─ 📋 ${t('decisions', LANG)}：${allKeyDecisions.length}${unitCount}${enCount}${LANG === 'bilingual' ? allKeyDecisions.length : ''}
├─ ⚠️ ${t('pitfalls', LANG)}：${allPitfalls.length}${unitCount}${enCount}${LANG === 'bilingual' ? allPitfalls.length : ''}
├─ 🧠 ${t('concepts', LANG)}：${allConcepts.length}${unitCount}${enCount}${LANG === 'bilingual' ? allConcepts.length : ''}
└─ 💬 ${t('insights', LANG)}：${uniqueInsights.length}${unitPieces}${enCount}${LANG === 'bilingual' ? uniqueInsights.length : ''}

**${t('sources', LANG)}：** ${channelLabel}

---

## 📚 ${t('topics', LANG)}

`;

  // 添加主题（无emoji，只显示任务详情）
  if (sortedTopics.length > 0) {
    sortedTopics.forEach((topic, idx) => {
      const isLast = idx === sortedTopics.length - 1;
      const hasTasks = topic.tasks && (topic.tasks.P0.length > 0 || topic.tasks.P1.length > 0 || topic.tasks.P2.length > 0);
      
      cardContent += `${isLast ? '└─' : '├─'} 主题${idx + 1}：${topic.title}
`;
      const sourceIsLast = !hasTasks;
      cardContent += `${isLast ? '   ' : '│  '}${sourceIsLast ? '└─' : '├─'} 来源：${topic.channel}${topic.score > 0 ? ` · 重要度：${topic.score}` : ''}
`;
      
      // 添加任务详情
      if (hasTasks) {
        const taskPriorities = ['P0', 'P1', 'P2'];
        const validPriorities = taskPriorities.filter(p => topic.tasks[p] && topic.tasks[p].length > 0);
        validPriorities.forEach((priority, pIdx) => {
          const isLastPriority = pIdx === validPriorities.length - 1;
          const taskList = topic.tasks[priority].join('、');
          cardContent += `${isLast ? '   ' : '│  '}${isLastPriority ? '└─' : '├─'} ${priority}：${taskList}
`;
        });
      }
      
      cardContent += '\n';
    });
  } else {
    cardContent += '暂无\n\n';
  }

  // 添加决策（无emoji）
  if (allKeyDecisions.length > 0) {
    cardContent += `---

## 📋 重要决策

`;
    allKeyDecisions.forEach((d, idx) => {
      const isLast = idx === allKeyDecisions.length - 1;
      cardContent += `${isLast ? '└─' : '├─'} 决策${idx + 1}：${d.decision} → ${d.choice}\n`;
      cardContent += `${isLast ? '   ' : '│  '}└─ 理由：${d.reason}（${d.channel}）\n\n`;
    });
  } else {
    cardContent += `---

## 📋 重要决策

暂无

`;
  }

  // 添加踩坑记录（emoji改为⚠️）
  if (allPitfalls.length > 0) {
    cardContent += `---

## ⚠️ 踩坑记录

`;
    allPitfalls.forEach((p, idx) => {
      const isLast = idx === allPitfalls.length - 1;
      cardContent += `${isLast ? '└─' : '├─'} 问题${idx + 1}：${p.problem}\n`;
      cardContent += `${isLast ? '   ' : '│  '}├─ 来源：${p.channel}\n`;
      if (p.solution) {
        cardContent += `${isLast ? '   ' : '│  '}├─ 解决方案：${p.solution}\n`;
      }
      if (p.lesson) {
        cardContent += `${isLast ? '   ' : '│  '}└─ 教训：${p.lesson}\n`;
      }
      cardContent += '\n';
    });
  } else {
    cardContent += `---

## ⚠️ 踩坑记录

暂无

`;
  }

  // 添加新概念（无emoji）
  if (allConcepts.length > 0) {
    cardContent += `---

## 🧠 新概念

`;
    allConcepts.forEach((c, idx) => {
      const isLast = idx === allConcepts.length - 1;
      cardContent += `${isLast ? '└─' : '├─'} 概念${idx + 1}：${c.term}\n`;
      cardContent += `${isLast ? '   ' : '│  '}├─ 来源：${c.channel}\n`;
      if (c.definition) {
        cardContent += `${isLast ? '   ' : '│  '}├─ 定义：${c.definition}\n`;
      }
      if (c.scenario) {
        cardContent += `${isLast ? '   ' : '│  '}└─ 应用场景：${c.scenario}\n`;
      }
      cardContent += '\n';
    });
  } else {
    cardContent += `---

## 🧠 新概念

暂无

`;
  }

  // 添加金句（emoji改为💬）
  if (uniqueInsights.length > 0) {
    cardContent += `---

## 💬 金句摘录

`;
    uniqueInsights.forEach((insight, idx) => {
      const isLast = idx === uniqueInsights.length - 1;
      cardContent += `${isLast ? '└─' : '├─'} "${insight.text}"\n${isLast ? '   ' : '│  '}└─ ${insight.channel}\n\n`;
    });
  } else {
    cardContent += `---

## 💬 金句摘录

暂无

`;
  }

  // 添加来源
  cardContent += `---

## 数据来源

`;
  if (data.feishu) {
    cardContent += `- **飞书：** memory/feishu/${date}.md\n`;
  }
  if (data.webui) {
    cardContent += `- **WebUI：** memory/webui/${date}.md\n`;
  }

  cardContent += `
---

*💃 金银 Planet · 自我提升部 · ${date}*
`;

  return cardContent;
}

// 主函数
function main() {
  // 读取 stdin 的 JSON
  let input = '';
  process.stdin.setEncoding('utf8');
  
  process.stdin.on('data', (chunk) => {
    input += chunk;
  });
  
  process.stdin.on('end', () => {
    try {
      const data = JSON.parse(input);
      
      if (!data.hasContent) {
        console.error('No content found for date:', data.date);
        process.exit(1);
      }
      
      const cardContent = generateCard(data);
      
      // 输出到 stdout（供后续处理）
      console.log(cardContent);
      
      // 同时写入文件
      const cardFile = path.join(CONFIG.learningCardsDir, `${data.date}.md`);
      fs.mkdirSync(CONFIG.learningCardsDir, { recursive: true });
      fs.writeFileSync(cardFile, cardContent, 'utf-8');
      
      console.error(`✅ 学习卡片已生成: ${cardFile}`);
    } catch (e) {
      console.error('Error:', e.message);
      process.exit(1);
    }
  });
}

main();
