#!/usr/bin/env node

/**
 * Daily Report Generator - 每日研究进展报告生成
 * 
 * 功能：
 * 1. 读取当前会话记录（通过 sessions_history）
 * 2. 读取最近 7 天记忆文件
 * 3. 识别项目和进展
 * 4. 生成报告并推送
 * 5. 更新当天记忆文件
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG_PATH = path.join(__dirname, 'config.json');
const TEMPLATE_PATH = path.join(__dirname, 'template.md');
const MEMORY_DIR = '/root/.openclaw/workspace/memory';
const MEMORY_FILE = '/root/.openclaw/workspace/MEMORY.md';

// 读取配置
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));

// 读取模板
const template = fs.readFileSync(TEMPLATE_PATH, 'utf-8');

/**
 * 获取当前会话记录（从 JSONL 文件读取）
 */
function getCurrentSessionHistory() {
  try {
    const SESSIONS_DIR = '/root/.openclaw/agents/main/sessions';
    const SESSIONS_FILE = path.join(SESSIONS_DIR, 'sessions.json');
    
    // 读取 sessions.json 找到最新的飞书会话
    const sessionsData = JSON.parse(fs.readFileSync(SESSIONS_FILE, 'utf-8'));
    
    // 找到最新的飞书会话文件（查找 key 中包含 feishu:direct 的）
    let latestFeishuSession = null;
    let latestTime = 0;
    
    for (const [key, session] of Object.entries(sessionsData)) {
      if (key.includes('feishu:direct') && session.updatedAt) {
        if (session.updatedAt > latestTime) {
          latestTime = session.updatedAt;
          latestFeishuSession = session;
        }
      }
    }
    
    if (!latestFeishuSession || !latestFeishuSession.sessionFile) {
      console.log('⚠️ 未找到飞书会话，跳过会话记录读取');
      return '';
    }
    
    const sessionFile = latestFeishuSession.sessionFile;
    if (!fs.existsSync(sessionFile)) {
      console.log('⚠️ 会话文件不存在:', sessionFile);
      return '';
    }
    
    // 读取 JSONL 文件
    const lines = fs.readFileSync(sessionFile, 'utf-8').split('\n');
    const messages = [];
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];
    
    lines.forEach(line => {
      if (!line.trim()) return;
      try {
        const entry = JSON.parse(line);
        if (entry.type === 'message' && entry.message) {
          const timestamp = new Date(entry.timestamp).toISOString().split('T')[0];
          if (timestamp >= todayStr) {
            messages.push({
              role: entry.message.role,
              content: entry.message.content?.[0]?.text || ''
            });
          }
        }
      } catch (e) {
        // 跳过解析失败的行
      }
    });
    
    // 拼接成文本
    const text = messages.map(msg => 
      `[${msg.role === 'user' ? '用户' : '助手'}] ${msg.content}`
    ).join('\n');
    
    console.log(`📄 读取到 ${messages.length} 条今日会话消息`);
    return text;
    
  } catch (e) {
    console.log('⚠️ 读取会话记录失败:', e.message);
    return '';
  }
}

/**
 * 获取今天的日期字符串
 */
function getTodayStr() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * 获取最近 N 天的记忆文件内容
 */
function getRecentMemories(days = 7) {
  const memories = [];
  const today = new Date();
  
  for (let i = 0; i < days; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    const memoryPath = path.join(MEMORY_DIR, `${dateStr}.md`);
    
    if (fs.existsSync(memoryPath)) {
      const content = fs.readFileSync(memoryPath, 'utf-8');
      memories.push({ date: dateStr, content });
    }
  }
  
  return memories;
}

/**
 * 从会话记录中提取项目进展
 */
function extractProgressFromSession(sessionText) {
  if (!sessionText) return [];
  
  const projects = [];
  
  // 匹配用户提到的任务/项目
  const patterns = [
    /(?:准备 | 正在 | 完成 | 搞定|done)\s*(?:的 | 了)?\s*[\u4e00-\u9fa5A-Za-z]{3,20}/g,
    /(?:研究 | 开发 | 配置 | 设置 | 创建|安装)\s*[\u4e00-\u9fa5A-Za-z\-]{3,30}/g,
  ];
  
  patterns.forEach(pattern => {
    const matches = sessionText.match(pattern);
    if (matches) {
      matches.forEach(match => {
        const name = match.replace(/(?:准备 | 正在 | 完成 | 搞定|done|的 | 了|研究 | 开发 | 配置 | 设置 | 创建 | 安装)/g, '').trim();
        if (name.length >= 2 && name.length <= 20) {
          projects.push({
            name: name,
            progress: match
          });
        }
      });
    }
  });
  
  return projects.slice(0, 5);
}

/**
 * 从文本中提取项目名和进展
 */
function extractProjects(text) {
  const projects = [];
  
  // 排除的日常词汇（不视为项目）
  const excludeKeywords = ['休息', '投标', '吃饭', '睡觉', '提醒', '日程', '安排', '计划', '明日计划', '系统状态', '延续性项目', '今日进展'];
  
  // 匹配常见的项目标记
  const patterns = [
    /\*\*(.+?)\*\*\s*[:：-]\s*(.+)/g,  // **项目名**: 进展
    /###\s*\d*\.\s*(.+?)\n([\s\S]*?)(?=###|-{3,}|$)/g,  // ### 1. 项目名
    /-\s*\*\*(.+?)\*\*\s*(.+)/g,  // - **项目名** 进展
  ];
  
  patterns.forEach(pattern => {
    let match;
    while ((match = pattern.exec(text)) !== null) {
      const name = match[1].trim();
      
      // 排除日常词汇和太短的名称
      if (name.length < 3 || excludeKeywords.some(k => name.includes(k))) {
        continue;
      }
      
      // 清理进展文本
      let progress = match[2] ? match[2].trim() : '';
      progress = progress.replace(/^[→-]\s*/, '').split('\n')[0].slice(0, 50);  // 取第一行，限 50 字
      
      projects.push({
        name: name,
        progress: progress
      });
    }
  });
  
  return projects;
}

/**
 * 识别延续性项目（在最近 7 天中出现多次的项目）
 */
function identifyContinuingProjects(memories) {
  const projectMap = new Map();
  
  memories.forEach(memory => {
    const projects = extractProjects(memory.content);
    projects.forEach(project => {
      if (!projectMap.has(project.name)) {
        projectMap.set(project.name, []);
      }
      projectMap.get(project.name).push({
        date: memory.date,
        progress: project.progress
      });
    });
  });
  
  // 筛选出出现 2 次以上的项目
  const continuing = [];
  projectMap.forEach((entries, name) => {
    if (entries.length >= 2) {
      continuing.push({
        name,
        entries,
        latestProgress: entries[entries.length - 1].progress
      });
    }
  });
  
  return continuing;
}

/**
 * 生成今日进展（从会话记录 + 当天记忆文件提取）
 */
function generateTodayProgress(sessionText, todayMemory) {
  const allProjects = [];
  
  // 1. 从会话记录提取
  if (sessionText) {
    const sessionProjects = extractProgressFromSession(sessionText);
    sessionProjects.forEach(p => {
      allProjects.push({ name: p.name, progress: p.progress });
    });
  }
  
  // 2. 从当天记忆文件提取
  if (todayMemory) {
    let content = todayMemory.content;
    const reportMarker = '## 📊 每日研究进展（自动生成）';
    const reportIndex = content.indexOf(reportMarker);
    
    if (reportIndex > 0) {
      content = content.substring(0, reportIndex);
    }
    
    const memoryProjects = extractProjects(content);
    memoryProjects.forEach(p => {
      // 避免重复
      if (!allProjects.find(ap => ap.name === p.name)) {
        allProjects.push(p);
      }
    });
  }
  
  if (allProjects.length === 0) return '今日暂无记录';
  
  return allProjects.slice(0, 5).map(p => 
    `**${p.name}** - ${p.progress}`
  ).join('\n');
}

/**
 * 生成月度工作热力图（GitHub 风格）
 */
function generateHeatmapChart(memories) {
  // 生成最近 30 天的热力图
  const days = 30;
  const today = new Date();
  const heatmapData = [];
  
  // 计算今天是今年的第几周
  const startOfYear = new Date(today.getFullYear(), 0, 1);
  const currentWeekNum = Math.ceil(((today - startOfYear) / 86400000 + startOfYear.getDay() + 1) / 7);
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    
    // 查找当天的记忆
    const memory = memories.find(m => m.date === dateStr);
    
    // 计算工作量（根据内容长度和消息数）
    let workload = 0;
    if (memory) {
      const contentLength = memory.content.length;
      // 简单分级：0=无工作，1-500=少量，501-2000=中等，2001+=大量
      if (contentLength > 2000) workload = 4;
      else if (contentLength > 500) workload = 3;
      else if (contentLength > 0) workload = 2;
      else workload = 1;
    }
    
    // 计算该日期是第几周
    const dateStartOfYear = new Date(date.getFullYear(), 0, 1);
    const weekNum = Math.ceil(((date - dateStartOfYear) / 86400000 + dateStartOfYear.getDay() + 1) / 7);
    
    heatmapData.push({
      date: dateStr,
      day: date.getDate(),
      weekday: date.getDay(),
      workload: workload,
      weekNum: weekNum
    });
  }
  
  // 按周分组（7 天一行）
  const weeks = [];
  let currentWeek = [];
  heatmapData.forEach((day, index) => {
    currentWeek.push(day);
    if ((index + 1) % 7 === 0) {
      weeks.push(currentWeek);
      currentWeek = [];
    }
  });
  if (currentWeek.length > 0) {
    weeks.push(currentWeek);
  }
  
  // 生成 ASCII 热力图 - 使用不同颜色区分工作量
  const monthLabels = ['1 月', '2 月', '3 月', '4 月', '5 月', '6 月', '7 月', '8 月', '9 月', '10 月', '11 月', '12 月'];
  const monthLabel = monthLabels[today.getMonth()];
  
  const lines = [];
  lines.push(`最近 30 天工作热力图 (${monthLabel})`);
  lines.push('');
  lines.push('图例：⬜ 无工作  🟨 少量  🟩 中等  🟥 大量');
  lines.push('');
  
  // 星期标签
  const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
  
  // 每周数据
  weeks.forEach((week, weekIndex) => {
    const actualWeekNum = week[0].weekNum;
    const weekLabel = `第${String(actualWeekNum).padStart(2, '0')}周`;
    
    const squares = week.map(d => {
      // 使用不同颜色的方块
      if (d.workload === 0) return '⬜';  // 无工作 - 白色
      if (d.workload === 1) return '🟨';  // 少量 - 黄色
      if (d.workload === 2) return '🟩';  // 中等 - 绿色
      if (d.workload === 3) return '🟥';  // 较多 - 红色
      return '🟥';  // 大量 - 红色
    }).join(' ');
    
    lines.push(`${weekLabel} ${squares}`);
  });
  
  lines.push('');
  lines.push(`        ${weekdays.join(' ')}`);
  
  return lines.join('\n');
}

/**
 * 生成延续性项目列表
 */
function generateContinuingProjects(continuingProjects) {
  if (continuingProjects.length === 0) return '无延续性项目';
  
  return continuingProjects.slice(0, 5).map(p => 
    `**${p.name}**：持续进行中 - ${p.latestProgress}`
  ).join('\n');
}

/**
 * 生成明日计划（基于今日进展推导）
 */
function generateTomorrowPlan(todayProgress, continuingProjects) {
  const plans = [];
  
  // 从未完成的项目推导
  continuingProjects.slice(0, 3).forEach(p => {
    plans.push(`继续推进 ${p.name}`);
  });
  
  // 默认计划
  if (plans.length === 0) {
    plans.push('处理日常事务');
    plans.push('跟进未完成项目');
  }
  
  return plans.map(p => `- ${p}`).join('\n');
}

/**
 * 获取上下文占用（通过 session_status）
 */
function getContextUsage() {
  try {
    const output = execSync('openclaw status', { encoding: 'utf-8', stdio: 'pipe' });
    // 适配多种格式
    const match = output.match(/Context:\s*(?:\d+k)?\/?\d+k?\s*\((\d+)%\)/) || 
                  output.match(/上下文：\s*(\d+)%/) ||
                  output.match(/(\d+)%/);
    if (match) {
      return `${match[1]}%`;
    }
  } catch (e) {
    // 忽略错误
  }
  return '未知';
}

/**
 * 填充模板
 */
function fillTemplate(data) {
  let report = template;
  
  Object.keys(data).forEach(key => {
    report = report.replace(new RegExp(`{{${key}}}`, 'g'), data[key]);
  });
  
  return report;
}

/**
 * 更新当天记忆文件
 */
function updateTodayMemory(report) {
  const todayStr = getTodayStr();
  const memoryPath = path.join(MEMORY_DIR, `${todayStr}.md`);
  
  let content = '';
  if (fs.existsSync(memoryPath)) {
    content = fs.readFileSync(memoryPath, 'utf-8');
  } else {
    content = `# ${todayStr} 工作记录\n\n`;
  }
  
  // 添加报告摘要
  const summary = `\n## 📊 每日研究进展（自动生成）\n\n${report}\n`;
  
  fs.writeFileSync(memoryPath, content + summary);
}

/**
 * 主函数
 */
async function main() {
  console.log('🐴 开始生成每日研究进展报告...');
  
  const todayStr = getTodayStr();
  
  // 1. 获取当前会话记录
  const sessionText = getCurrentSessionHistory();
  
  // 2. 获取最近 7 天记忆文件
  const memories = getRecentMemories(config.lookbackDays);
  
  // 3. 找到今天的记忆
  const todayMemory = memories.find(m => m.date === todayStr);
  
  // 4. 识别延续性项目
  const continuingProjects = identifyContinuingProjects(memories);
  
  // 5. 生成各部分内容
  const todayProgress = generateTodayProgress(sessionText, todayMemory);
  const heatmapChart = generateHeatmapChart(memories);
  const continuingList = generateContinuingProjects(continuingProjects);
  const tomorrowPlan = generateTomorrowPlan(todayProgress, continuingProjects);
  const contextUsage = getContextUsage();
  const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  
  // 填充模板
  let report = fillTemplate({
    DATE: todayStr,
    TODAY_PROGRESS: todayProgress,
    HEATMAP_CHART: heatmapChart,
    CONTINUING_PROJECTS: continuingList,
    TOMORROW_PLAN: tomorrowPlan,
    CONTEXT_USAGE: contextUsage,
    TASKS_DONE: 'N/A',
    TIMESTAMP: timestamp
  });
  
  console.log(`\n📋 报告生成完成`);
  console.log('\n--- 报告内容 ---\n');
  console.log(report);
  console.log('\n--- 结束 ---\n');
  
  // 更新记忆文件
  updateTodayMemory(report);
  console.log('✅ 已更新当天记忆文件');
  
  // 推送（这里输出报告，实际推送由 Cron 处理）
  console.log('\n📤 报告已就绪，等待推送...\n');
  
  return report;
}

// 执行
main().catch(console.error);
