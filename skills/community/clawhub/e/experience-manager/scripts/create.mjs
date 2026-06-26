#!/usr/bin/env node
/**
 * 经验创建脚本
 * 将自然语言描述转化为标准格式的经验包（exp.yml + references/）
 */

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import AdmZip from 'adm-zip';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const EXPERIENCES_DIR = path.join(process.env.HOME, '.openclaw', 'experiences');
const PACKAGES_DIR = path.join(EXPERIENCES_DIR, 'packages');
const WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE || '/data/openclaw';

// 确保目录存在
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// 从文件提取关键词
function extractKeywords(text) {
  if (!text) return [];
  
  // 提取技术词汇、工具名、概念
  const keywords = [];
  
  // 技能/工具名（大写或特定格式）
  const skillMatches = text.match(/[a-z]+[_-][a-z]+/g) || [];
  keywords.push(...skillMatches);
  
  // 中文技术词汇
  const chineseTech = text.match(/[\u4e00-\u9fa5]{2,8}/g) || [];
  keywords.push(...chineseTech);
  
  // 英文技术词汇
  const englishTech = text.match(/\b[a-z]{3,}\b/g) || [];
  keywords.push(...englishTech);
  
  return [...new Set(keywords)].slice(0, 20);
}

// 计算文本相似度（改进版）
function calculateSimilarity(text1, text2) {
  // 方法1：关键词匹配
  const words1 = new Set(extractKeywords(text1.toLowerCase()));
  const words2 = new Set(extractKeywords(text2.toLowerCase()));
  
  const intersection = [...words1].filter(w => words2.has(w));
  const union = [...new Set([...words1, ...words2])];
  
  const keywordScore = union.length > 0 ? intersection.length / union.length : 0;
  
  // 方法2：直接包含检查（如果 text2 包含 text1 的关键部分）
  const text1Lower = text1.toLowerCase();
  const text2Lower = text2.toLowerCase();
  
  // 提取 text1 中的核心词汇（2-4字词组）
  const coreTerms = [];
  for (let i = 0; i < text1Lower.length - 1; i++) {
    for (let len = 2; len <= 4 && i + len <= text1Lower.length; len++) {
      coreTerms.push(text1Lower.substring(i, i + len));
    }
  }
  
  let matchCount = 0;
  for (const term of coreTerms) {
    if (text2Lower.includes(term)) {
      matchCount++;
    }
  }
  
  const containmentScore = coreTerms.length > 0 ? matchCount / coreTerms.length : 0;
  
  // 综合分数（取最大值）
  return Math.max(keywordScore, containmentScore);
}

// 读取历史记忆文件（memory/YYYY-MM-DD.md）
function readHistoricalMemories() {
  const memories = [];
  const memoryDir = path.join(WORKSPACE_DIR, 'memory');
  
  if (!fs.existsSync(memoryDir)) {
    return memories;
  }
  
  // 获取所有记忆文件，按日期排序（最新的在前）
  const files = fs.readdirSync(memoryDir)
    .filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/))
    .sort()
    .reverse();
  
  // 只读取最近 7 天的记忆
  for (const file of files.slice(0, 7)) {
    const filePath = path.join(memoryDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const date = file.replace('.md', '');
    
    // 分割成条目
    const entries = content.split(/\n## /);
    for (let i = 0; i < entries.length; i++) {
      const entry = entries[i];
      if (entry.trim() && !entry.startsWith('# ')) {
        memories.push({
          source: `memory/${file}`,
          date: date,
          title: entry.split('\n')[0].trim(),
          content: i > 0 ? '## ' + entry : entry,
          keywords: extractKeywords(entry)
        });
      }
    }
  }
  
  return memories;
}

// 读取记忆文件（按优先级）
function readMemoryFiles() {
  const memories = [];
  
  // 优先级 3: 读取历史记忆 memory/YYYY-MM-DD.md
  const historicalMemories = readHistoricalMemories();
  memories.push(...historicalMemories.map(m => ({ ...m, priority: 3 })));
  
  // 优先级 2: 读取 MEMORY.md
  const memoryPath = path.join(WORKSPACE_DIR, 'MEMORY.md');
  if (fs.existsSync(memoryPath)) {
    const content = fs.readFileSync(memoryPath, 'utf8');
    const entries = content.split(/\n## /).slice(1);
    for (const entry of entries) {
      memories.push({
        source: 'MEMORY.md',
        priority: 2,
        title: entry.split('\n')[0].trim(),
        content: entry,
        keywords: extractKeywords(entry)
      });
    }
  }
  
  // 优先级 1: 读取 .learnings/（最近的经验记录）
  // 读取 .learnings/LEARNINGS.md
  const learningsPath = path.join(WORKSPACE_DIR, '.learnings', 'LEARNINGS.md');
  if (fs.existsSync(learningsPath)) {
    const content = fs.readFileSync(learningsPath, 'utf8');
    const entries = content.split(/\n## /).slice(1);
    for (const entry of entries) {
      memories.push({
        source: 'LEARNINGS.md',
        priority: 1,
        title: entry.split('\n')[0].trim(),
        content: entry,
        keywords: extractKeywords(entry)
      });
    }
  }
  
  // 读取 .learnings/ERRORS.md
  const errorsPath = path.join(WORKSPACE_DIR, '.learnings', 'ERRORS.md');
  if (fs.existsSync(errorsPath)) {
    const content = fs.readFileSync(errorsPath, 'utf8');
    const parts = content.split(/\n## /);
    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      if (i === 0 && part.startsWith('# ')) continue;
      if (part.trim()) {
        const entry = i > 0 ? '## ' + part : part;
        memories.push({
          source: 'ERRORS.md',
          priority: 1,
          title: part.split('\n')[0].trim(),
          content: entry,
          keywords: extractKeywords(entry)
        });
      }
    }
  }
  
  return memories;
}

// 搜索相关记忆（考虑优先级）
function searchRelatedMemories(keywords, memories, topK = 5) {
  const scored = memories.map(m => {
    const baseScore = calculateSimilarity(keywords.join(' '), m.content);
    // 优先级加成：priority 越小越重要（1 > 2 > 3）
    // priority 1 的加成 0.2，priority 2 的加成 0.1，priority 3 的加成 0
    const priorityBonus = m.priority ? (4 - m.priority) * 0.05 : 0;
    return {
      ...m,
      baseScore,
      priorityBonus,
      score: Math.min(baseScore + priorityBonus, 1.0) // 最高不超过 1.0
    };
  });
  
  return scored
    .filter(m => m.baseScore > 0.1)  // 使用基础分数过滤
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}

// 读取当前 Agent 配置
function readAgentConfig() {
  const config = {
    soul: {},
    agents: {},
    tools: {},
    skills: []
  };
  
  // 读取 SOUL.md
  const soulPath = path.join(WORKSPACE_DIR, 'SOUL.md');
  if (fs.existsSync(soulPath)) {
    const content = fs.readFileSync(soulPath, 'utf8');
    config.soul = {
      principles: extractPrinciples(content),
      constraints: extractConstraints(content),
      keywords: extractKeywords(content)
    };
  }
  
  // 读取 AGENTS.md
  const agentsPath = path.join(WORKSPACE_DIR, 'AGENTS.md');
  if (fs.existsSync(agentsPath)) {
    const content = fs.readFileSync(agentsPath, 'utf8');
    config.agents = {
      workflows: extractWorkflows(content),
      rules: extractRules(content),
      keywords: extractKeywords(content)
    };
  }
  
  // 读取 TOOLS.md
  const toolsPath = path.join(WORKSPACE_DIR, 'TOOLS.md');
  if (fs.existsSync(toolsPath)) {
    const content = fs.readFileSync(toolsPath, 'utf8');
    config.tools = {
      allowed: extractAllowedTools(content),
      bestPractices: extractBestPractices(content),
      keywords: extractKeywords(content)
    };
  }
  
  // 读取已安装 Skills（多个可能的位置）
  const possibleDirs = [
    path.join(process.env.HOME || '/root', '.openclaw', 'skills'),
    '/app/skills',
    path.join(__dirname, '../../skills')
  ];
  
  let allSkills = [];
  for (const dir of possibleDirs) {
    if (fs.existsSync(dir)) {
      try {
        const skills = fs.readdirSync(dir)
          .filter(d => {
            try {
              return fs.statSync(path.join(dir, d)).isDirectory() && !d.startsWith('.');
            } catch {
              return false;
            }
          })
          .map(d => ({ name: d, path: path.join(dir, d) }));
        allSkills.push(...skills);
      } catch (e) {
        // 忽略无法读取的目录
      }
    }
  }
  config.skills = allSkills;
  
  return config;
}

// 提取原则
function extractPrinciples(content) {
  const principles = [];
  const matches = content.match(/[-*]\s*(.+)/g) || [];
  for (const match of matches.slice(0, 10)) {
    principles.push(match.replace(/^[-*]\s*/, '').trim());
  }
  return principles;
}

// 提取约束
function extractConstraints(content) {
  const constraints = [];
  const matches = content.match(/禁止|不能|不要|拒绝/g) || [];
  return matches.length;
}

// 提取工作流
function extractWorkflows(content) {
  const workflows = [];
  const matches = content.match(/流程|步骤|workflow/g) || [];
  return matches.length;
}

// 提取规则
function extractRules(content) {
  const rules = [];
  const matches = content.match(/必须|应该|需要/g) || [];
  return matches.length;
}

// 提取允许的工具
function extractAllowedTools(content) {
  const tools = [];
  const matches = content.match(/`(\w+)`/g) || [];
  for (const match of matches) {
    tools.push(match.replace(/`/g, ''));
  }
  return [...new Set(tools)];
}

// 提取最佳实践
function extractBestPractices(content) {
  const practices = [];
  const matches = content.match(/✅|推荐|最佳|实践/g) || [];
  return matches.length;
}

// OpenClaw 基础工具（预装，不需要作为依赖）
const BUILTIN_TOOLS = new Set([
  // 文件系统工具
  'read', 'write', 'edit',
  // 运行时工具
  'exec', 'process',
  // 网络工具
  'web_search', 'web_fetch', 'browser',
  // 消息工具
  'message',
  // 系统工具
  'sessions_spawn', 'sessions_list', 'sessions_send', 'subagents',
  // 其他基础工具
  'canvas', 'tts', 'agents_list'
]);

// 系统命令（不需要作为依赖）
const SYSTEM_COMMANDS = new Set([
  'python', 'node', 'npm', 'npx', 'bash', 'sh', 'zsh', 'curl', 'wget',
  'git', 'docker', 'kubectl', 'jq', 'awk', 'sed', 'grep', 'cat', 'ls',
  'cd', 'mkdir', 'rm', 'cp', 'mv', 'echo', 'printf', 'tar', 'zip', 'unzip'
]);

// 需要作为依赖的 Skills（插件带入）
const SKILL_ALIASES = {
  'feishu_doc': ['feishu_doc', 'feishu doc', '飞书文档', '飞书doc'],
  'feishu_wiki': ['feishu_wiki', 'feishu wiki', '飞书知识库'],
  'feishu_bitable': ['feishu_bitable', 'feishu bitable', '飞书多维表格', '飞书表格', 'bitable'],
  'feishu_drive': ['feishu_drive', 'feishu drive', '飞书云空间'],
  'feishu_chat': ['feishu_chat', 'feishu chat', '飞书群'],
  'popo_team_space': ['popo_team_space', 'popo team', 'popo 团队空间'],
  'weather': ['weather', '天气'],
  'healthcheck': ['healthcheck', '健康检查'],
  'skill_creator': ['skill_creator', 'skill-creator', '创建 skill'],
  'ep_cli': ['ep_cli', 'ep-cli', 'overmind'],
  'china_holiday_checker': ['china_holiday_checker', 'holiday', '节假日']
};

// 检查是否为内置工具（不需要作为依赖）
function isBuiltinTool(name) {
  const normalized = name.toLowerCase().replace(/[_-]/g, '');
  // 检查 BUILTIN_TOOLS
  for (const tool of BUILTIN_TOOLS) {
    if (normalized === tool.toLowerCase().replace(/[_-]/g, '')) {
      return true;
    }
  }
  // 检查 SYSTEM_COMMANDS
  for (const cmd of SYSTEM_COMMANDS) {
    if (normalized === cmd.toLowerCase()) {
      return true;
    }
  }
  return false;
}

// 扫描全局 Skills（~/.openclaw/skills/）
function scanGlobalSkills() {
  const skillsDir = path.join(process.env.HOME || '/home/appops', '.openclaw', 'skills');
  const skills = [];
  
  if (!fs.existsSync(skillsDir)) {
    return skills;
  }
  
  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && !entry.name.startsWith('.') && !entry.name.startsWith('node_modules')) {
      skills.push(entry.name);
    }
  }
  
  return skills;
}

// 扫描 Agent 特定的 Skills（/data/openclaw/agents/{name}-workspace/skills/）
function scanAgentSkills(agentName) {
  const agentSkillsDir = path.join('/data/openclaw/agents', `${agentName}-workspace`, 'skills');
  const skills = [];
  
  if (!fs.existsSync(agentSkillsDir)) {
    return skills;
  }
  
  const entries = fs.readdirSync(agentSkillsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && !entry.name.startsWith('.') && !entry.name.startsWith('node_modules')) {
      skills.push(entry.name);
    }
  }
  
  return skills;
}

// 扫描工作空间 Skills（/data/openclaw/skills/）
function scanWorkspaceSkills() {
  const skillsDir = path.join(WORKSPACE_DIR, 'skills');
  const skills = [];
  
  if (!fs.existsSync(skillsDir)) {
    return skills;
  }
  
  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory() && !entry.name.startsWith('.') && !entry.name.startsWith('node_modules')) {
      skills.push(entry.name);
    }
  }
  
  return skills;
}

// 获取所有可用的 Skills（全局 + 内置 + Agent特定）
function getAllAvailableSkills(agentName = null) {
  const allSkills = new Set();
  
  // 1. 全局 Skills
  const globalSkills = scanGlobalSkills();
  globalSkills.forEach(s => allSkills.add(s));
  
  // 2. 工作空间 Skills
  const workspaceSkills = scanWorkspaceSkills();
  workspaceSkills.forEach(s => allSkills.add(s));
  
  // 3. 内置 Skills（作为基础能力）
  for (const tool of BUILTIN_TOOLS) {
    allSkills.add(tool);
  }
  
  // 4. Agent 特定的 Skills
  if (agentName) {
    const agentSkills = scanAgentSkills(agentName);
    agentSkills.forEach(s => allSkills.add(s));
  }
  
  return [...allSkills];
}

// 从描述和相关记忆中提取实际使用的 skills
function extractSkillsFromMemories(relatedMemories, description, agentName = null) {
  const desc = description.toLowerCase();
  const skills = new Set();
  
  // 1. 获取所有可用的 skills（全局 + 内置 + Agent特定）
  const allSkills = getAllAvailableSkills(agentName);
  
  // 2. 从描述中精确匹配 skills
  // 匹配形如 feishu_doc, feishu-doc, web_search 等格式
  const skillPattern = /\b([a-z]+[_-][a-z]+(?:[_-][a-z]+)*)\b/g;
  const matches = desc.match(skillPattern) || [];
  
  for (const match of matches) {
    const normalizedMatch = match.toLowerCase().replace(/[_-]/g, '');
    
    // 检查是否匹配某个可用的 skill
    for (const skillName of allSkills) {
      const normalizedSkill = skillName.toLowerCase().replace(/[_-]/g, '');
      if (normalizedMatch === normalizedSkill) {
        skills.add(skillName);
        break;
      }
    }
    
    // 检查 SKILL_ALIASES
    for (const [skillName, aliases] of Object.entries(SKILL_ALIASES)) {
      for (const alias of aliases) {
        const normalizedAlias = alias.toLowerCase().replace(/[_-]/g, '');
        if (normalizedMatch === normalizedAlias) {
          skills.add(skillName);
          break;
        }
      }
    }
  }
  
  // 3. 从相关记忆中提取 skills（仅当记忆中明确提到该经验使用了某个 skill）
  for (const memory of relatedMemories) {
    const content = memory.content.toLowerCase();
    
    // 检查记忆标题是否与当前描述高度相关
    const titleSimilarity = calculateSimilarity(desc, memory.title || '');
    if (titleSimilarity < 0.5) {
      continue; // 不相关的记忆，跳过
    }
    
    // 从相关记忆中提取 skill 引用
    const memMatches = content.match(skillPattern) || [];
    for (const match of memMatches) {
      const normalizedMatch = match.replace(/[_-]/g, '');
      
      for (const skillName of allSkills) {
        const normalizedSkill = skillName.toLowerCase().replace(/[_-]/g, '');
        if (normalizedMatch === normalizedSkill) {
          skills.add(skillName);
          break;
        }
      }
    }
  }
  
  return [...skills];
}

// 识别相关依赖
function identifyDependencies(description, config, relatedMemories = [], agentName = null) {
  const desc = description.toLowerCase();
  const deps = {
    skills: [],
    tools: [],
    soul_principles: [],
    agent_rules: []
  };
  
  // 从记忆和描述中提取实际使用的所有 skills（包括内置的）
  deps.skills = extractSkillsFromMemories(relatedMemories, description, agentName);
  
  // 识别相关原则（通过关键词匹配）
  for (const principle of config.soul.principles || []) {
    const similarity = calculateSimilarity(desc, principle);
    if (similarity > 0.3) {
      deps.soul_principles.push(principle.substring(0, 50));
    }
  }
  
  return deps;
}

// 生成经验包 name
// 格式约束：仅允许英文小写字母、中划线、数字
function generateName(title) {
  // 先转换为小写，将空格替换为中划线
  let normalized = title
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '')  // 仅保留小写字母、数字、中划线
    .replace(/^-+|-+$/g, '')     // 去掉首尾中划线
    .replace(/-+/g, '-');        // 多个中划线合并为一个
  
  // 如果为空，返回 null 表示需要用户输入
  if (!normalized) {
    return null;
  }
  
  return normalized.substring(0, 50);
}

// 将中文描述总结为英文表达（用于提示用户）
function summarizeToEnglish(description) {
  // 提取关键词并转换为英文风格
  const keywords = description
    .toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 2)
    .slice(0, 5);
  
  if (keywords.length === 0) {
    return 'experience-name';
  }
  
  return keywords.join('-').substring(0, 50);
}

// 识别经验类型
function detectType(description) {
  const desc = description.toLowerCase();
  if (desc.includes('错误') || desc.includes('失败') || desc.includes('crash') || desc.includes('exception')) {
    return 'error_lesson';
  }
  if (desc.includes('技巧') || desc.includes('tip') || desc.includes('必须') || desc.includes('注意')) {
    return 'tool_tip';
  }
  if (desc.includes('最佳') || desc.includes('实践') || desc.includes('pattern') || desc.includes('应该')) {
    return 'best_practice';
  }
  if (desc.includes('不知道') || desc.includes('原来') || desc.includes('学到了')) {
    return 'knowledge_gap';
  }
  return 'best_practice';
}

// 识别适用角色
function detectRoles(description) {
  const roles = [];
  const desc = description.toLowerCase();
  
  if (/后端|backend|api|数据库|server/.test(desc)) roles.push('backend');
  if (/前端|frontend|ui|react|vue/.test(desc)) roles.push('frontend');
  if (/devops|部署|docker|k8s|ci\/cd/.test(desc)) roles.push('devops');
  if (/数据|data|spark|flink|etl/.test(desc)) roles.push('data');
  if (/测试|test|qa/.test(desc)) roles.push('qa');
  if (/产品|pm|需求/.test(desc)) roles.push('product');
  
  if (roles.length === 0) roles.push('general');
  
  return roles;
}

// 解析经验描述
function parseExperience(description) {
  // 提取标题（第一句或前50字）
  const title = description.split(/[。，；;]/)[0].substring(0, 50);
  
  // 识别类型
  const type = detectType(description);
  
  // 提取问题和解决方案
  let problem = description;
  let solution = { steps: [], code: '' };
  
  // 尝试提取 "问题：... 解决：..." 格式
  const problemMatch = description.match(/问题[：:]\s*([^解决]+)/);
  const solutionMatch = description.match(/解决[：:]\s*(.+)/);
  
  if (problemMatch) {
    problem = problemMatch[1].trim();
  }
  if (solutionMatch) {
    const solutionText = solutionMatch[1].trim();
    // 尝试提取代码块
    const codeMatch = solutionText.match(/```[\s\S]*?```/);
    if (codeMatch) {
      solution.code = codeMatch[0].replace(/```/g, '').trim();
    }
    // 提取步骤
    solution.steps = solutionText
      .replace(/```[\s\S]*?```/g, '')
      .split(/[。，；;]/)
      .map(s => s.trim())
      .filter(s => s.length > 0);
  }
  
  // 如果没有提取到步骤，将整个描述作为步骤
  if (solution.steps.length === 0) {
    solution.steps = description.split(/[。，；;]/).map(s => s.trim()).filter(s => s.length > 0);
  }
  
  return {
    title,
    type,
    problem,
    solution,
    roles: detectRoles(description)
  };
}

// 分析依赖类型（从描述和记忆中推断），并记录具体内容
function analyzeDependencyTypes(description, deps, relatedMemories) {
  const allContent = description + ' ' + relatedMemories.map(m => m.content).join(' ');
  
  const dependencies = {
    soul: {
      has: false,
      items: []  // 具体涉及的原则、价值观
    },
    agents: {
      has: false,
      items: []  // 具体涉及的工作流程、规则
    },
    tools: {
      has: false,
      items: []  // 具体涉及的工具使用技巧
    },
    skills: {
      has: false,
      items: []  // 依赖的 skills 列表
    }
  };
  
  // 1. 检查 SOUL 相关（原则、价值观、行为准则）
  const soulKeywords = [
    { kw: '原则', desc: '行为原则' },
    { kw: '准则', desc: '行为准则' },
    { kw: '价值观', desc: '价值观' },
    { kw: '态度', desc: '工作态度' },
    { kw: '风格', desc: '沟通风格' },
    { kw: '必须', desc: '强制性要求' },
    { kw: '禁止', desc: '禁止性规定' },
    { kw: '保密', desc: '保密要求' },
    { kw: '安全', desc: '安全准则' },
    { kw: '谨慎', desc: '谨慎原则' },
    { kw: '直接', desc: '直接沟通' },
    { kw: '高效', desc: '高效执行' }
  ];
  
  for (const { kw, desc } of soulKeywords) {
    if (allContent.includes(kw)) {
      dependencies.soul.has = true;
      if (!dependencies.soul.items.includes(desc)) {
        dependencies.soul.items.push(desc);
      }
    }
  }
  
  // 从 soul_principles 中提取
  for (const principle of deps.soul_principles) {
    dependencies.soul.has = true;
    if (!dependencies.soul.items.includes(principle)) {
      dependencies.soul.items.push(principle);
    }
  }
  
  // 2. 检查 AGENTS 相关（工作流程、规则、职责、群聊）
  const agentsKeywords = [
    { kw: '流程', desc: '工作流程' },
    { kw: '步骤', desc: '操作步骤' },
    { kw: '规则', desc: '规则约束' },
    { kw: '职责', desc: '职责边界' },
    { kw: '边界', desc: '边界限制' },
    { kw: '约束', desc: '约束条件' },
    { kw: '检查', desc: '检查流程' },
    { kw: '群聊', desc: '群聊规则' },
    { kw: '群', desc: '群组管理' },
    { kw: '处理', desc: '处理流程' },
    { kw: '回复', desc: '回复规范' },
    { kw: '负责', desc: '职责分工' }
  ];
  
  for (const { kw, desc } of agentsKeywords) {
    if (allContent.includes(kw)) {
      dependencies.agents.has = true;
      if (!dependencies.agents.items.includes(desc)) {
        dependencies.agents.items.push(desc);
      }
    }
  }
  
  // 3. 检查 TOOLS 相关（工具使用技巧）
  if (deps.tools.length > 0) {
    dependencies.tools.has = true;
    dependencies.tools.items = [...deps.tools];
  }
  
  // 4. 记录 skills 依赖
  if (deps.skills.length > 0) {
    dependencies.skills.has = true;
    dependencies.skills.items = [...deps.skills];
  }
  
  return dependencies;
}

// 生成 references 目录下的文件内容
function generateReferences(parsed, deps, dependencyTypes) {
  const references = {};
  
  // 1. SOUL.md - 原则、价值观相关内容
  if (dependencyTypes.soul.has) {
    const lines = [];
    lines.push(`# ${parsed.title} - 行为准则`);
    lines.push('');
    lines.push(`> 来源: 经验包`);
    lines.push(`> 类型: ${parsed.type}`);
    lines.push('');
    lines.push('## 涉及原则');
    for (const item of dependencyTypes.soul.items) {
      lines.push(`- ${item}`);
    }
    lines.push('');
    lines.push('## 行为准则');
    if (parsed.solution.steps.length > 0) {
      for (const step of parsed.solution.steps) {
        lines.push(`- ${step}`);
      }
    }
    references['soul.md'] = lines.join('\n');
  }
  
  // 2. AGENTS.md - 工作流程、规则相关内容
  if (dependencyTypes.agents.has) {
    const lines = [];
    lines.push(`# ${parsed.title} - 工作流程`);
    lines.push('');
    lines.push(`> 来源: 经验包`);
    lines.push(`> 类型: ${parsed.type}`);
    lines.push('');
    lines.push('## 场景');
    lines.push(parsed.problem);
    lines.push('');
    lines.push('## 处理流程');
    for (let i = 0; i < parsed.solution.steps.length; i++) {
      lines.push(`${i + 1}. ${parsed.solution.steps[i]}`);
    }
    lines.push('');
    lines.push('## 相关规则');
    for (const item of dependencyTypes.agents.items) {
      lines.push(`- ${item}`);
    }
    references['agents.md'] = lines.join('\n');
  }
  
  // 3. TOOLS.md - 工具使用技巧相关内容
  if (dependencyTypes.tools.has) {
    const lines = [];
    lines.push(`# ${parsed.title} - 工具使用`);
    lines.push('');
    lines.push(`> 来源: 经验包`);
    lines.push(`> 类型: ${parsed.type}`);
    lines.push('');
    lines.push('## 问题');
    lines.push(parsed.problem);
    lines.push('');
    lines.push('## 解决方案');
    for (let i = 0; i < parsed.solution.steps.length; i++) {
      lines.push(`${i + 1}. ${parsed.solution.steps[i]}`);
    }
    if (parsed.solution.code) {
      lines.push('');
      lines.push('## 代码示例');
      lines.push('```');
      lines.push(parsed.solution.code);
      lines.push('```');
    }
    lines.push('');
    lines.push('## 涉及工具');
    for (const item of dependencyTypes.tools.items) {
      lines.push(`- ${item}`);
    }
    references['tools.md'] = lines.join('\n');
  }
  
  return references;
}

// 生成经验包
function generateExperiencePackage(parsed, deps, relatedMemories, author, providedName = null) {
  // 使用用户提供的 name，或从 title 生成
  let name = providedName || generateName(parsed.title);
  
  // 如果 name 为空，返回 null 让上层处理
  if (!name) {
    return { name: null, expYml: null, references: null };
  }
  
  // 分析依赖类型
  const dependencyTypes = analyzeDependencyTypes(parsed.problem, deps, relatedMemories);
  
  // 生成 references 文件
  const references = generateReferences(parsed, deps, dependencyTypes);
  
  // Schema 版本定义
// v1.0.0: 初始版本，精简格式
// 格式: schema, name, description, metadata, soul, agents, tools, skills
const SCHEMA_VERSION = 'openclaw.experience.v1';

// 构建 exp.yml（精简格式）
  const expYml = {
    schema: SCHEMA_VERSION,
    name,
    description: parsed.problem.substring(0, 200),
    metadata: {
      version: '1.0.0',
      author: author || 'unknown'
    },
    soul: dependencyTypes.soul.has ? 'references/soul.md' : null,
    agents: dependencyTypes.agents.has ? 'references/agents.md' : null,
    tools: dependencyTypes.tools.has ? 'references/tools.md' : null,
    skills: deps.skills.length > 0 ? deps.skills : []
  };
  
  return { name, expYml, references };
}

// 保存经验包（包含 exp.yml 和 references/ 目录）
function saveExperiencePackage(name, expYml, references) {
  ensureDir(PACKAGES_DIR);
  
  const zipPath = path.join(PACKAGES_DIR, `${name}.zip`);
  
  // 创建 zip
  const zip = new AdmZip();
  
  // 添加 exp.yml
  zip.addFile('exp.yml', Buffer.from(yaml.dump(expYml), 'utf8'));
  
  // 添加 references/ 目录下的文件
  for (const [filename, content] of Object.entries(references)) {
    zip.addFile(`references/${filename}`, Buffer.from(content, 'utf8'));
  }
  
  zip.writeZip(zipPath);
  
  return zipPath;
}

// 获取优先级标签
function getPriorityLabel(priority) {
  switch (priority) {
    case 1: return '🔥 当前上下文';
    case 2: return '📌 长期记忆';
    case 3: return '📜 历史记忆';
    default: return '📝 其他';
  }
}

// 显示相关记忆供选择
function displayMemoryOptions(relatedMemories) {
  console.log('\n📚 发现相关记忆（按优先级排序）：\n');
  
  // 按优先级分组显示
  let currentPriority = null;
  
  for (let i = 0; i < relatedMemories.length; i++) {
    const m = relatedMemories[i];
    
    // 显示优先级分组标题
    if (m.priority !== currentPriority) {
      currentPriority = m.priority;
      console.log(`${getPriorityLabel(m.priority)}:`);
    }
    
    console.log(`  ${i + 1}. [${m.source}] ${m.title}`);
    console.log(`     相关度: ${Math.round(m.score * 100)}% (基础 ${Math.round(m.baseScore * 100)}% + 优先级 ${Math.round(m.priorityBonus * 100)}%)`);
    if (m.date) {
      console.log(`     日期: ${m.date}`);
    }
    console.log(`     预览: ${m.content.substring(0, 80).replace(/\n/g, ' ')}...`);
    console.log();
  }
  
  console.log('选项：');
  console.log('  - 输入数字 (1-5) 选择具体记忆');
  console.log('  - 输入 "all" 使用所有相关记忆');
  console.log('  - 输入 "none" 不使用记忆');
  console.log('  - 输入 "more" 查看更多匹配');
}

// 主函数
async function main() {
  const args = process.argv.slice(2);

  // 解析参数
  let providedName = null;
  let targetAgent = null;
  const descriptionParts = [];

  for (const arg of args) {
    if (arg.startsWith('--name=')) {
      providedName = arg.replace('--name=', '').trim();
    } else if (arg.startsWith('--agent=')) {
      targetAgent = arg.replace('--agent=', '').trim();
    } else {
      descriptionParts.push(arg);
    }
  }

  const description = descriptionParts.join(' ');

  if (!description) {
    console.error('用法: node create.mjs <经验描述> [--name=经验包名称] [--agent=agent名称]');
    console.error('示例: node create.mjs "feishu_doc 写入验证"');
    console.error('示例: node create.mjs "中文描述" --name=feishu-doc-validation');
    console.error('示例: node create.mjs "feishu_doc 使用技巧" --agent=严哥');
    process.exit(1);
  }

  // 显示目标 Agent（如果指定）
  if (targetAgent) {
    console.log(`🎯 目标 Agent: ${targetAgent}`);
    console.log(`📁 Agent Skills: /data/openclaw/agents/${targetAgent}-workspace/skills/\n`);
  }
  
  console.log('📝 正在分析经验...\n');
  console.log(`输入: "${description}"\n`);
  
  // 1. 读取记忆
  console.log('🔍 搜索相关记忆...');
  const memories = readMemoryFiles();
  const keywords = extractKeywords(description);
  const relatedMemories = searchRelatedMemories(keywords, memories, 5);
  
  if (relatedMemories.length > 0) {
    displayMemoryOptions(relatedMemories);
    
    // 这里简化处理，自动选择最相关的
    console.log(`\n✅ 自动选择最相关的 ${Math.min(3, relatedMemories.length)} 条记忆`);
  } else {
    console.log('  未找到相关记忆\n');
  }
  
  // 2. 读取 Agent 配置
  console.log('🔧 分析 Agent 配置...');
  const config = readAgentConfig();
  console.log(`  已安装 Skills: ${config.skills.length} 个`);
  console.log(`  允许的工具: ${config.tools.allowed?.length || 0} 个`);
  console.log(`  SOUL 原则: ${config.soul.principles?.length || 0} 条`);
  console.log();
  
  // 3. 识别依赖（传入相关记忆和目标 Agent 以提取实际使用的 skills）
  console.log('🔗 识别依赖关系...');
  const deps = identifyDependencies(description, config, relatedMemories, targetAgent);
  console.log(`  相关 Skills: ${deps.skills.join(', ') || '无'}`);
  if (targetAgent) {
    console.log(`  包含 Agent 特定 Skills: 是`);
  }
  console.log(`  相关原则: ${deps.soul_principles.length} 条`);
  console.log();
  
  // 4. 解析经验
  console.log('📋 解析经验内容...');
  const parsed = parseExperience(description);
  console.log(`  标题: ${parsed.title}`);
  console.log(`  类型: ${parsed.type}`);
  console.log(`  适用角色: ${parsed.roles.join(', ')}`);
  console.log();
  
  // 5. 生成经验包
  const author = process.env.OPENCLAW_USER_ID || 'unknown';
  let { name, expYml, references } = generateExperiencePackage(
    parsed, 
    deps, 
    relatedMemories.slice(0, 3),
    author,
    providedName
  );
  
  // 如果 name 为空，提示用户输入
  if (!name) {
    const suggestedName = summarizeToEnglish(description);
    console.log('\n⚠️  无法从描述自动生成有效的经验包名称');
    console.log('   格式要求：仅英文小写字母、中划线、数字');
    console.log(`   建议名称：${suggestedName}`);
    console.log('\n   请使用以下方式提供名称：');
    console.log(`   node create.mjs "${description}" --name=${suggestedName}`);
    console.log('\n   或修改描述，加入英文关键词');
    process.exit(1);
  }
  
  // 6. 显示依赖分析（重点确认）
  console.log('📦 生成经验包：');
  console.log(`  name: ${name}`);
  console.log(`  version: ${expYml.metadata.version}`);
  console.log();
  
  console.log('⚠️  【重点确认】依赖引用分析：');
  if (expYml.soul) {
    console.log(`  ✅ SOUL.md: ${expYml.soul}`);
  }
  if (expYml.agents) {
    console.log(`  ✅ AGENTS.md: ${expYml.agents}`);
  }
  if (expYml.tools) {
    console.log(`  ✅ TOOLS.md: ${expYml.tools}`);
  }
  if (expYml.skills.length > 0) {
    console.log(`  ✅ Skills: ${expYml.skills.join(', ')}`);
  }
  console.log();
  console.log('  💡 学习时将读取 references/ 目录下的对应文件');
  console.log();
  
  // 7. 保存
  const zipPath = saveExperiencePackage(name, expYml, references);
  
  console.log('✅ 经验包已保存');
  console.log(`📁 路径: ${zipPath}`);
  console.log(`📁 包含文件:`);
  console.log(`   - exp.yml`);
  for (const filename of Object.keys(references)) {
    console.log(`   - references/${filename}`);
  }
  console.log();
  console.log('💡 提示：使用 "学习经验 ' + zipPath + '" 来学习这条经验');
  console.log('   或: node learn.mjs ' + zipPath);
  
  // 显示 exp.yml 预览
  console.log('\n--- exp.yml 预览 ---');
  console.log(yaml.dump(expYml).substring(0, 500) + '...');
  
  // 显示 references 文件预览
  for (const [filename, content] of Object.entries(references)) {
    console.log(`\n--- references/${filename} 预览 ---`);
    console.log(content.substring(0, 300) + '...');
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  console.error(err.stack);
  process.exit(1);
});
