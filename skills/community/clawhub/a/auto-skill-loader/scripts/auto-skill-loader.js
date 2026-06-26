#!/usr/bin/env node
/**
 * Auto Skill Loader v2.0 - Core Module
 * 
 * 功能：
 * 1. 扫描 OpenClaw 标准目录（L1-L4）发现所有 Skill
 * 2. 解析 SKILL.md frontmatter（name, level, description）
 * 3. 按 level 过滤：core 不碰，protected 需确认，dynamic 自由加载
 * 4. 输出可加载 Skill 列表供 Agent 做意图匹配
 * 
 * 设计原则：
 * - 零配置启动（所有参数有合理默认值）
 * - 不硬编码任何 Agent 名称/路径
 * - 跨平台兼容（Windows/macOS/Linux）
 * 
 * 用法：
 *   node auto-skill-loader.js                    # 列出所有可加载 Skill
 *   node auto-skill-loader.js --all              # 列出所有 Skill（含 core/protected）
 *   node auto-skill-loader.js --check <name>     # 检查指定 Skill 的保护级别
 *   node auto-skill-loader.js --dry-run "<msg>"  # 模拟匹配（输出候选，不加载）
 *   node auto-skill-loader.js --json             # JSON 格式输出
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const yaml = require('./yaml-lite');  // 轻量 YAML 解析，零依赖

// ============================================================
// 常量
// ============================================================

const CORE_NAME_PATTERNS = [
  /memory/i,
  /audit/i,
  /security/i,
  /proactive/i,
];

const DEFAULT_CONFIG = {
  coreSkills: [],
  skipSkills: [],
  enableRouting: true,
  matchMode: 'normal',   // strict | normal | fuzzy
  logLevel: 'info',      // silent | info | debug
  dryRun: false,
};

// ============================================================
// Frontmatter 解析
// ============================================================

/**
 * 从 SKILL.md 内容中提取 YAML frontmatter
 * @param {string} content - SKILL.md 文件内容
 * @returns {object|null} 解析后的 frontmatter 对象
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;
  try {
    return yaml.parse(match[1]);
  } catch (e) {
    return null;
  }
}

/**
 * 从 SKILL.md 提取 description 正文（frontmatter 之后的第一段非空文本）
 * 用于补充 frontmatter 中 description 缺失的情况
 */
function extractDescriptionFromBody(content) {
  const body = content.replace(/^---[\s\S]*?---\r?\n?/, '').trim();
  // 取第一个非标题、非空行的段落
  const lines = body.split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith('#') && !trimmed.startsWith('```') && !trimmed.startsWith('|')) {
      return trimmed.slice(0, 200);  // 限制长度
    }
  }
  return '';
}

// ============================================================
// 目录扫描
// ============================================================

/**
 * 获取 OpenClaw 安装目录
 * 尝试多种方式检测，保证跨平台兼容
 */
function getOpenClawInstallDir() {
  // 方式 1：环境变量
  if (process.env.OPENCLAW_HOME) {
    return process.env.OPENCLAW_HOME;
  }

  // 方式 2：常见 npm 全局安装路径
  const candidates = [
    path.join(os.homedir(), 'AppData', 'Roaming', 'npm', 'node_modules', 'openclaw'),  // Windows
    path.join('/usr', 'local', 'lib', 'node_modules', 'openclaw'),                      // macOS/Linux
    path.join('/usr', 'lib', 'node_modules', 'openclaw'),                                // Linux alt
    path.join(os.homedir(), '.nvm', 'versions', 'node'),                                 // nvm (需进一步查找)
  ];

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return null;
}

/**
 * 获取当前 workspace 目录
 * 优先级：环境变量 > cwd > 默认 ~/.openclaw/workspace
 */
function getWorkspaceDir() {
  if (process.env.OPENCLAW_WORKSPACE) {
    return process.env.OPENCLAW_WORKSPACE;
  }
  // 检查 cwd 是否在 .openclaw 下
  const cwd = process.cwd();
  if (cwd.includes('.openclaw')) {
    return cwd;
  }
  // 默认 workspace
  const defaultWs = path.join(os.homedir(), '.openclaw', 'workspace');
  if (fs.existsSync(defaultWs)) {
    return defaultWs;
  }
  return cwd;
}

/**
 * 按 L1-L4 优先级扫描所有 Skill 目录
 * @param {string} [workspace] - workspace 路径（可选）
 * @returns {Array<{skillDir: string, level: string, priority: number}>}
 */
function scanSkillDirs(workspace) {
  workspace = workspace || getWorkspaceDir();
  const openclawDir = getOpenClawInstallDir();

  const scanPaths = [
    // L1: Agent 专属（最高优先级）
    { dir: path.join(workspace, '.agents', 'skills'), priority: 1, label: 'L1-workspace' },
    // L2: 全局共享
    { dir: path.join(os.homedir(), '.agents', 'skills'), priority: 2, label: 'L2-global' },
  ];

  // L3: OpenClaw 内置
  if (openclawDir) {
    scanPaths.push({
      dir: path.join(openclawDir, 'skills'),
      priority: 3,
      label: 'L3-builtin',
    });
    // L4: 扩展 Skill
    scanPaths.push({
      dir: path.join(openclawDir, 'extensions'),
      priority: 4,
      label: 'L4-extensions',
    });
  }

  const results = [];

  for (const { dir, priority, label } of scanPaths) {
    if (!fs.existsSync(dir)) continue;

    if (priority === 4) {
      // L4 扩展：需要进入每个扩展目录的 skills/ 子目录
      const extensions = safeReaddir(dir);
      for (const ext of extensions) {
        const extSkillsDir = path.join(dir, ext, 'skills');
        if (!fs.existsSync(extSkillsDir)) continue;
        const skills = safeReaddir(extSkillsDir);
        for (const skill of skills) {
          const skillMd = path.join(extSkillsDir, skill, 'SKILL.md');
          if (fs.existsSync(skillMd)) {
            results.push({ skillDir: path.join(extSkillsDir, skill), skillMd, priority, label: `${label}/${ext}` });
          }
        }
      }
    } else {
      const skills = safeReaddir(dir);
      for (const skill of skills) {
        const skillMd = path.join(dir, skill, 'SKILL.md');
        if (fs.existsSync(skillMd)) {
          results.push({ skillDir: path.join(dir, skill), skillMd, priority, label });
        }
      }
    }
  }

  return results;
}

function safeReaddir(dir) {
  try {
    return fs.readdirSync(dir).filter(f => {
      try {
        return fs.statSync(path.join(dir, f)).isDirectory();
      } catch { return false; }
    });
  } catch { return []; }
}

// ============================================================
// Skill 解析 + Level 判定
// ============================================================

/**
 * 判断 Skill 的保护级别
 * @param {string} name - Skill 名称
 * @param {string|undefined} declaredLevel - frontmatter 声明的 level
 * @param {object} config - 用户配置
 * @returns {'core'|'protected'|'dynamic'}
 */
function resolveLevel(name, declaredLevel, config) {
  // 1. 用户配置的 coreSkills 优先
  if (config.coreSkills && config.coreSkills.includes(name)) {
    return 'core';
  }

  // 2. frontmatter 显式声明
  if (declaredLevel && ['core', 'protected', 'dynamic'].includes(declaredLevel)) {
    return declaredLevel;
  }

  // 3. 内置名称模式匹配（安全兜底）
  for (const pattern of CORE_NAME_PATTERNS) {
    if (pattern.test(name)) {
      return 'core';
    }
  }

  // 4. 默认 dynamic
  return 'dynamic';
}

/**
 * 解析单个 Skill
 */
function parseSkill(entry, config) {
  let content;
  try {
    content = fs.readFileSync(entry.skillMd, 'utf-8');
  } catch {
    return null;
  }

  const fm = parseFrontmatter(content);
  const name = (fm && fm.name) || path.basename(entry.skillDir);
  const declaredLevel = fm && fm.level;
  const description = (fm && fm.description) || extractDescriptionFromBody(content);
  const version = (fm && fm.version) || '0.0.0';
  const level = resolveLevel(name, declaredLevel, config);

  return {
    name,
    level,
    declaredLevel: declaredLevel || null,
    description: typeof description === 'string' ? description.trim() : String(description || '').trim(),
    version,
    priority: entry.priority,
    source: entry.label,
    path: entry.skillMd,
    dir: entry.skillDir,
  };
}

// ============================================================
// 配置加载
// ============================================================

function loadConfig(workspace) {
  const configPaths = [
    path.join(workspace || getWorkspaceDir(), 'auto-skill-loader.config.yaml'),
    path.join(workspace || getWorkspaceDir(), '.agents', 'skills', 'auto-skill-loader', 'auto-skill-loader.config.yaml'),
  ];

  for (const configPath of configPaths) {
    if (fs.existsSync(configPath)) {
      try {
        const content = fs.readFileSync(configPath, 'utf-8');
        const parsed = yaml.parse(content);
        return { ...DEFAULT_CONFIG, ...parsed };
      } catch {
        // 配置解析失败，用默认值
      }
    }
  }

  return { ...DEFAULT_CONFIG };
}

// ============================================================
// 主逻辑
// ============================================================

function loadAllSkills(workspace) {
  const config = loadConfig(workspace);
  const entries = scanSkillDirs(workspace);
  const skills = [];
  const seen = new Set();  // 去重：同名 Skill 高优先级覆盖低优先级

  for (const entry of entries) {
    const skill = parseSkill(entry, config);
    if (!skill) continue;

    // 同名去重（高优先级保留）
    if (seen.has(skill.name)) continue;
    seen.add(skill.name);

    // skipSkills 过滤
    if (config.skipSkills && config.skipSkills.includes(skill.name)) continue;

    skills.push(skill);
  }

  return { skills, config };
}

/**
 * 获取可加载 Skill 列表（排除 core，protected 标记但保留）
 */
function getLoadableSkills(workspace) {
  const { skills, config } = loadAllSkills(workspace);

  return {
    loadable: skills.filter(s => s.level === 'dynamic'),
    protected: skills.filter(s => s.level === 'protected'),
    core: skills.filter(s => s.level === 'core'),
    all: skills,
    config,
  };
}

/**
 * 检查指定 Skill 的保护级别
 */
function checkSkill(name, workspace) {
  const { skills } = loadAllSkills(workspace);
  const skill = skills.find(s => s.name === name);
  if (!skill) {
    return { found: false, name };
  }
  return { found: true, ...skill };
}

// ============================================================
// CLI
// ============================================================

function formatSkillLine(s) {
  const levelIcon = { core: '🔒', protected: '🛡️', dynamic: '🔄' };
  const icon = levelIcon[s.level] || '❓';
  const declared = s.declaredLevel ? '' : ' (auto)';
  return `  ${icon} ${s.name.padEnd(30)} ${s.level.padEnd(12)}${declared}  [${s.source}]`;
}

function main() {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const allMode = args.includes('--all');
  const checkIdx = args.indexOf('--check');
  const dryRunIdx = args.indexOf('--dry-run');

  // --check <name>
  if (checkIdx !== -1) {
    const name = args[checkIdx + 1];
    if (!name) {
      console.error('Usage: --check <skill-name>');
      process.exit(1);
    }
    const result = checkSkill(name);
    if (jsonMode) {
      console.log(JSON.stringify(result, null, 2));
    } else if (!result.found) {
      console.log(`❓ Skill "${name}" 未找到`);
    } else {
      const levelIcon = { core: '🔒', protected: '🛡️', dynamic: '🔄' };
      console.log(`${levelIcon[result.level]} ${result.name}: ${result.level}`);
      if (result.level === 'core') {
        console.log('   ⛔ 此 Skill 为核心级，自动加载器不可操作');
      } else if (result.level === 'protected') {
        console.log('   ⚠️ 此 Skill 为保护级，需显式确认才能操作');
      } else {
        console.log('   ✅ 此 Skill 可自由加载/卸载');
      }
    }
    return;
  }

  // --dry-run "<message>"
  if (dryRunIdx !== -1) {
    const message = args[dryRunIdx + 1] || '';
    const { loadable, protected: prot, core } = getLoadableSkills();
    if (jsonMode) {
      console.log(JSON.stringify({ message, loadable, protected: prot, core, blocked: core.length }, null, 2));
    } else {
      console.log(`🔍 Auto Skill Loader - Dry Run`);
      console.log(`任务: "${message}"`);
      console.log(`\n可匹配 Skill (${loadable.length} 个):`);
      loadable.forEach(s => console.log(formatSkillLine(s)));
      if (prot.length) {
        console.log(`\n保护级 Skill (${prot.length} 个, 需确认):`);
        prot.forEach(s => console.log(formatSkillLine(s)));
      }
      console.log(`\n核心级 Skill (${core.length} 个, 已屏蔽):`);
      core.forEach(s => console.log(formatSkillLine(s)));
      console.log(`\n💡 意图匹配由 Agent 完成，此处仅列出候选池`);
    }
    return;
  }

  // 默认：列出 Skill
  const { loadable, protected: prot, core, all } = getLoadableSkills();

  if (jsonMode) {
    console.log(JSON.stringify(allMode ? { all } : { loadable, protected: prot, core }, null, 2));
    return;
  }

  if (allMode) {
    console.log(`📦 所有 Skill (${all.length} 个):\n`);
    all.forEach(s => console.log(formatSkillLine(s)));
  } else {
    console.log(`🔄 可加载 Skill (${loadable.length} 个):\n`);
    loadable.forEach(s => console.log(formatSkillLine(s)));

    if (prot.length) {
      console.log(`\n🛡️ 保护级 (${prot.length} 个):`);
      prot.forEach(s => console.log(formatSkillLine(s)));
    }

    console.log(`\n🔒 核心级 (${core.length} 个, 不可操作):`);
    core.forEach(s => console.log(formatSkillLine(s)));
  }

  console.log(`\n总计: ${all.length} 个 Skill | 可加载: ${loadable.length} | 保护: ${prot.length} | 核心: ${core.length}`);
}

// ============================================================
// 导出（供其他脚本调用）
// ============================================================

module.exports = {
  parseFrontmatter,
  scanSkillDirs,
  resolveLevel,
  loadAllSkills,
  getLoadableSkills,
  checkSkill,
  loadConfig,
  DEFAULT_CONFIG,
};

// CLI 直接运行
if (require.main === module) {
  main();
}
