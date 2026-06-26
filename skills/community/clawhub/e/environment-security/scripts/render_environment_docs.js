#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_TOOL_ORDER = [
  'git',
  'java',
  'javac',
  'maven',
  'gradle',
  'node',
  'npm',
  'pnpm',
  'yarn',
  'python',
  'go',
  'rustc',
  'cargo',
  'rustup',
  'clang',
  'clangxx',
  'gcc',
  'gxx',
  'cmake',
  'make',
  'ninja',
  'ruby',
  'gem',
  'bundler',
  'php',
  'composer',
  'dotnet',
  'docker',
  'kubectl',
];

function readText(pathname) {
  const content = fs.readFileSync(pathname, 'utf8');
  return content.charCodeAt(0) === 0xfeff ? content.slice(1) : content;
}

function loadJson(pathname) {
  return JSON.parse(readText(pathname));
}

function renderDate(isoValue) {
  if (!isoValue) return new Date().toISOString().slice(0, 10);
  const date = new Date(String(isoValue).replace(/Z$/, '+00:00'));
  return Number.isNaN(date.getTime()) ? new Date().toISOString().slice(0, 10) : date.toISOString().slice(0, 10);
}

function code(value) {
  return `\`${value || '<unknown>'}\``;
}

function firstNonempty(...values) {
  return values.find((value) => value) || null;
}

function approvedVersion(tool) {
  if (tool.version) return tool.version;
  if (tool.version_probe_status === 'ok') return tool.version_text || null;
  return null;
}

function normalizeLang(value) {
  if (!value) return null;
  const normalized = String(value).trim().toLowerCase().replace(/_/g, '-');
  if (normalized.startsWith('zh') || normalized.includes('chinese')) return 'zh';
  if (normalized.startsWith('en') || normalized.includes('english')) return 'en';
  return null;
}

function detectLocaleCandidates() {
  const candidates = [];
  for (const key of ['CODEX_DOC_LANG', 'LC_ALL', 'LC_MESSAGES', 'LANGUAGE', 'LANG']) {
    const value = process.env[key];
    if (value) candidates.push(value);
  }

  try {
    const locale = Intl.DateTimeFormat().resolvedOptions().locale;
    if (locale) candidates.push(locale);
  } catch (_) {}

  return Array.from(new Set(candidates.filter(Boolean)));
}

function chooseDocumentLanguage(data, explicitLang) {
  const normalizedExplicit = normalizeLang(explicitLang);
  if (explicitLang && explicitLang !== 'auto' && normalizedExplicit) {
    return normalizedExplicit;
  }

  const contextLanguage = normalizeLang(((data.context || {}).document_language));
  if (contextLanguage) return contextLanguage;

  const contextLocale = normalizeLang(((data.context || {}).detected_locale));
  if (contextLocale) return contextLocale;

  for (const candidate of detectLocaleCandidates()) {
    const normalized = normalizeLang(candidate);
    if (normalized) return normalized;
  }

  return 'en';
}

function L(lang, en, zh) {
  return lang === 'zh' ? zh : en;
}

function dash(label, value, lang) {
  return lang === 'zh' ? `- ${label}：${code(value)}` : `- ${label}: ${code(value)}`;
}

function detectOsFamily(data) {
  const context = data.context || {};
  if (context.os_family) return context.os_family;
  const platformSystem = String(context.platform_system || '').toLowerCase();
  if (platformSystem === 'windows_nt' || platformSystem === 'windows') return 'windows';
  if (platformSystem === 'darwin') return 'macos';
  if (platformSystem === 'linux') return 'linux';
  const platformText = String(context.platform || '').toLowerCase();
  if (platformText.includes('windows')) return 'windows';
  if (platformText.includes('darwin') || platformText.includes('mac')) return 'macos';
  if (platformText.includes('linux')) return 'linux';
  return 'unknown';
}

function osLabel(osFamily) {
  return {
    windows: 'Windows',
    macos: 'macOS',
    linux: 'Linux',
  }[osFamily] || osFamily || 'Unknown';
}

function envRef(name, suffix, osFamily) {
  if (osFamily === 'windows') {
    return suffix ? `%${name}%\\${suffix}` : `%${name}%`;
  }
  return suffix ? `$${name}/${suffix}` : `$${name}`;
}

function normalizePathKey(value) {
  if (!value) return '';
  let normalized = path.normalize(String(value));
  if (os.platform() === 'win32') normalized = normalized.toLowerCase();
  return normalized;
}

function comparePaths(left, right) {
  if (!left || !right) return false;
  return normalizePathKey(left) === normalizePathKey(right);
}

function orderedTools(data) {
  const tools = data.tools || {};
  const seen = new Set();
  const ordered = [];
  for (const toolId of DEFAULT_TOOL_ORDER) {
    if (toolId in tools) {
      ordered.push([toolId, tools[toolId]]);
      seen.add(toolId);
    }
  }
  for (const toolId of Object.keys(tools).sort()) {
    if (!seen.has(toolId)) {
      ordered.push([toolId, tools[toolId]]);
    }
  }
  return ordered;
}

function formatPathEntry(entry, envVars, osFamily) {
  const javaHome = ((envVars.JAVA_HOME || {}).value);
  const mavenHome = ((envVars.MAVEN_HOME || {}).value);
  if (javaHome && comparePaths(entry, path.join(javaHome, 'bin'))) {
    return envRef('JAVA_HOME', 'bin', osFamily);
  }
  if (mavenHome && comparePaths(entry, path.join(mavenHome, 'bin'))) {
    return envRef('MAVEN_HOME', 'bin', osFamily);
  }
  return entry;
}

function launcherLabel(commandName, osFamily, lang) {
  if (osFamily === 'windows' && (commandName === 'python' || commandName === 'py')) {
    return L(lang, `\`${commandName}\` shim`, `\`${commandName}\` shim`);
  }
  return L(lang, `\`${commandName}\` PATH entry`, `\`${commandName}\` PATH 入口`);
}

function renderToolSection(toolId, tool, sectionNumber, envVars, osFamily, lang) {
  const lines = [`### 3.${sectionNumber} ${tool.label || toolId}`, ''];
  const selected = firstNonempty(tool.selected_executable, tool.preferred_path, tool.resolved_path);
  const version = approvedVersion(tool);
  const pathHit = tool.resolved_path;

  if (toolId === 'java') {
    const javaHome = ((envVars.JAVA_HOME || {}).value);
    if (javaHome) {
      lines.push(dash(L(lang, 'Default JDK', '默认 JDK'), javaHome, lang));
      lines.push(dash('JAVA_HOME', javaHome, lang));
    } else {
      lines.push(dash(L(lang, 'Approved Java executable', '批准的 Java 可执行文件'), selected, lang));
    }
    lines.push(dash(L(lang, 'Approved Java version', '当前批准使用的 Java 版本'), version, lang));
    lines.push('');
    lines.push(L(lang, 'Notes:', '说明：'));
    if (pathHit && selected && !comparePaths(pathHit, selected)) {
      lines.push(
        L(
          lang,
          `- \`java\` currently resolves to ${code(pathHit)} on PATH.`,
          `- \`java\` 当前 PATH 先命中了 ${code(pathHit)}。`
        )
      );
    }
    let note = L(
      lang,
      '- Prefer the approved Java path before running Java-related commands',
      '- 执行 Java 相关命令前，如有需要，应优先使用批准路径'
    );
    if (javaHome) {
      note += L(
        lang,
        ` or move ${code(envRef('JAVA_HOME', 'bin', osFamily))} to the front of PATH for the current process.`,
        `或在当前进程里把 ${code(envRef('JAVA_HOME', 'bin', osFamily))} 放到 PATH 最前面。`
      );
    } else {
      note += L(lang, '.', '。');
    }
    lines.push(note);
    if (!version && tool.version_probe_status !== 'ok') {
      lines.push(
        L(
          lang,
          '- The Java launcher was found, but it did not report a usable runtime version. Treat Java as unavailable until a JDK or JRE is installed and `java -version` succeeds.',
          '- 已找到 Java 启动入口，但它没有返回可用的运行时版本。在安装好 JDK 或 JRE 且 `java -version` 成功之前，应把 Java 视为不可用。'
        )
      );
    }
    return lines;
  }

  if (toolId === 'maven') {
    const mavenHome = ((envVars.MAVEN_HOME || {}).value);
    if (mavenHome) {
      lines.push(dash('MAVEN_HOME', mavenHome, lang));
    }
    lines.push(dash(L(lang, 'Executable', '可执行文件'), selected, lang));
    lines.push(dash(L(lang, 'Approved Maven version', '当前批准使用的 Maven 版本'), version, lang));
    if (pathHit && selected && !comparePaths(pathHit, selected)) {
      lines.push('');
      lines.push(L(lang, 'Notes:', '说明：'));
      lines.push(
        L(
          lang,
          `- \`mvn\` currently resolves to ${code(pathHit)} on PATH.`,
          `- \`mvn\` 当前 PATH 先命中了 ${code(pathHit)}。`
        )
      );
      let note = L(
        lang,
        '- Prefer the approved Maven path before running Maven-related commands',
        '- 执行 Maven 相关命令前，如有需要，应优先使用批准路径'
      );
      if (mavenHome) {
        note += L(
          lang,
          ` or move ${code(envRef('MAVEN_HOME', 'bin', osFamily))} to the front of PATH for the current process.`,
          `或在当前进程里把 ${code(envRef('MAVEN_HOME', 'bin', osFamily))} 放到 PATH 最前面。`
        );
      } else {
        note += L(lang, '.', '。');
      }
      lines.push(note);
    }
    return lines;
  }

  if (toolId === 'python') {
    const details = tool.details || {};
    lines.push(dash(L(lang, 'Approved Python version', '当前版本'), version, lang));
    lines.push(dash(L(lang, 'Real interpreter path', '真实解释器路径'), details.current_interpreter, lang));
    lines.push(
      dash(
        L(lang, 'Python script directory', 'Python 脚本入口目录'),
        details.bin_dir || details.scripts_dir,
        lang
      )
    );
    for (const commandName of ['python', 'python3', 'py']) {
      const launcherValue = details[`${commandName}_launcher`];
      if (launcherValue) {
        lines.push(dash(launcherLabel(commandName, osFamily, lang), launcherValue, lang));
      }
    }
    lines.push('');
    lines.push(L(lang, 'Notes:', '说明：'));
    lines.push(
      L(
        lang,
        '- Prefer the real interpreter path when an absolute path is required.',
        '- 需要绝对路径时，优先使用真实解释器路径。'
      )
    );
    if (pathHit && selected && !comparePaths(pathHit, selected)) {
      lines.push(
        L(
          lang,
          '- `python` or `python3` may currently resolve to a shim, wrapper, alias, symlink, or launcher instead of the real install root.',
          '- `python` 或 `python3` 当前可能命中了 shim、wrapper、alias、symlink 或 launcher，不应将其误认为真实安装根目录。'
        )
      );
    }
    return lines;
  }

  if (toolId === 'node') {
    lines.push(dash('Node', selected, lang));
    lines.push(dash(L(lang, 'Approved Node version', 'Node 当前版本'), version, lang));
    if (pathHit && selected && !comparePaths(pathHit, selected)) {
      lines.push(dash(L(lang, 'Current PATH hit', '当前 PATH 命中'), pathHit, lang));
    }
    return lines;
  }

  if (toolId === 'npm') {
    lines.push(dash('npm', selected, lang));
    lines.push(dash(L(lang, 'Approved npm version', 'npm 当前版本'), version, lang));
    if (pathHit && selected && !comparePaths(pathHit, selected)) {
      lines.push(dash(L(lang, 'Current PATH hit', '当前 PATH 命中'), pathHit, lang));
    }
    return lines;
  }

  lines.push(dash(L(lang, 'Executable', '可执行文件'), selected, lang));
  if (version) lines.push(dash(L(lang, 'Version', '当前版本'), version, lang));
  if (pathHit && selected && !comparePaths(pathHit, selected)) {
    lines.push(dash(L(lang, 'Current PATH hit', '当前 PATH 命中'), pathHit, lang));
  }
  if (!version && tool.version_command && tool.version_probe_status !== 'ok') {
    lines.push(
      L(
        lang,
        '- Note: The executable was found, but its version command did not return a usable version. Treat this tool as present but not yet verified for real use.',
        '- 说明：已找到可执行入口，但版本命令没有返回可用版本。在版本命令成功之前，应将该工具视为“已命中入口但尚未真正验证可用”。'
      )
    );
  }
  for (const note of tool.notes || []) {
    lines.push(L(lang, `- Note: ${note}`, `- 说明：${note}`));
  }
  return lines;
}

function renderMissingTools(data, startSection, lang) {
  const missing = orderedTools(data).filter(([, tool]) => tool.status !== 'found');
  if (!missing.length) return [];

  const lines = [`### 3.${startSection} ${L(lang, 'Verified but currently missing tools', '未找到但曾被校验的工具')}`, ''];
  for (const [toolId, tool] of missing) {
    lines.push(
      L(
        lang,
        `- ${tool.label || toolId}: executable not found.`,
        `- ${tool.label || toolId}：未找到可执行文件。`
      )
    );
  }
  return lines;
}

function renderChecks(data, sectionNumber, lang) {
  const checks = data.checks || {};
  const checkIds = Object.keys(checks);
  if (!checkIds.length) return [];

  const lines = [`### 3.${sectionNumber} ${L(lang, 'Additional environment elements', '补充环境要素')}`, ''];
  for (const checkId of checkIds.sort()) {
    const check = checks[checkId];
    lines.push(dash(check.label || checkId, check.status, lang));
    lines.push(
      L(
        lang,
        `  - Command: ${code((check.command || []).join(' '))}`,
        `  - 命令：${code((check.command || []).join(' '))}`
      )
    );
    if ((check.matched_patterns || []).length) {
      lines.push(
        L(
          lang,
          `  - Matched patterns: ${code(check.matched_patterns.join(', '))}`,
          `  - 命中模式：${code(check.matched_patterns.join(', '))}`
        )
      );
    }
  }
  return lines;
}

function renderPolicy(data, baselineName, lang) {
  const envVars = data.environment_variables || {};
  const osFamily = detectOsFamily(data);
  const platformText = firstNonempty((data.context || {}).platform, (data.context || {}).platform_system);
  const dateText = renderDate(data.generated_at);
  const lines = [
    L(lang, '# Global Environment Policy', '# 全局环境政策'),
    '',
    L(lang, `Last updated: ${dateText}`, `最后更新：${dateText}`),
    '',
    L(lang, '## 1. Overview', '## 1. 说明'),
    '',
    L(lang, 'This document is the master environment policy for the current machine.', '这份文档是当前机器环境的主文档。'),
    '',
    L(
      lang,
      `Current baseline platform: ${code(osLabel(osFamily))}; platform fingerprint: ${code(platformText)}.`,
      `当前基线平台：${code(osLabel(osFamily))}，平台指纹：${code(platformText)}。`
    ),
    '',
    L(
      lang,
      'All models, AI agents, CLIs, OpenClaw sessions, or other automations must read this document before performing environment-related work.',
      '所有模型、AI、CLI、OpenClaw 或其他自动化代理在任何工作目录下，只要涉及环境相关任务，都应先读取本文件。'
    ),
    '',
    L(
      lang,
      `Keep the reusable machine-readable baseline in ${code(baselineName)} when possible. This document records the approved environment and the hard rules derived from verified facts.`,
      `机器可复用基线建议保存在 ${code(baselineName)}；本文件负责记录经验证后批准使用的环境与硬性规则。`
    ),
    '',
    L(lang, '## 2. Basic Rules', '## 2. 基本规则'),
    '',
    L(lang, '### 2.1 Prohibited Actions', '### 2.1 禁止事项'),
    '',
    L(
      lang,
      '- Do not download, install, upgrade, uninstall, or auto-configure software, CLIs, SDKs, runtimes, databases, browsers, drivers, plugins, or global dependencies without explicit user approval.',
      '- 未经用户明确要求，不得下载、安装、升级、卸载或自动配置任何软件、CLI、SDK、运行时、数据库、浏览器、驱动、插件或全局依赖。'
    ),
    L(
      lang,
      '- Do not modify `PATH`, `JAVA_HOME`, `MAVEN_HOME`, or other environment variables without explicit user approval.',
      '- 未经用户明确要求，不得修改 `PATH`、`JAVA_HOME`、`MAVEN_HOME` 等环境变量。'
    ),
    L(
      lang,
      '- Do not assume that tools not listed in this document or the baseline are already installed.',
      '- 对于本文件或基线中未列出的工具，不得默认假定本机已经安装。'
    ),
    '',
    L(lang, '### 2.2 What To Do When Tools Are Missing', '### 2.2 缺工具时的处理方式'),
    '',
    L(
      lang,
      'If the current task depends on a missing tool, CLI, SDK, service, or other environment component, you must:',
      '如果任务需要本机当前没有的工具、CLI、SDK、服务或其他环境组件，必须：'
    ),
    '',
    L(lang, '1. Tell the user which tool is missing.', '1. 告诉用户缺少什么工具。'),
    L(lang, '2. Explain why it is needed.', '2. 说明为什么需要。'),
    L(
      lang,
      '3. Ask the user to return the executable path or install directory after installation.',
      '3. 说明希望用户提供哪个可执行文件路径或安装目录。'
    ),
    L(
      lang,
      '4. Default to user-managed installation. Only continue with self-installation when the user explicitly authorizes it.',
      '4. 默认等待用户自行安装；只有用户明确授权并要求代理代装时，才可继续安装。'
    ),
    L(
      lang,
      `5. Update both this document and ${code(baselineName)} after installation or verification.`,
      `5. 安装或校验完成后，同时更新本文件和 ${code(baselineName)}。`
    ),
    '',
    L(lang, '## 3. Approved Environment', '## 3. 当前批准使用的环境'),
    '',
  ];

  let sectionNumber = 1;
  for (const [toolId, tool] of orderedTools(data)) {
    if (tool.status === 'found') {
      lines.push(...renderToolSection(toolId, tool, sectionNumber, envVars, osFamily, lang));
      lines.push('');
      sectionNumber += 1;
    }
  }

  const missingLines = renderMissingTools(data, sectionNumber, lang);
  if (missingLines.length) {
    lines.push(...missingLines);
    lines.push('');
    sectionNumber += 1;
  }

  const checkLines = renderChecks(data, sectionNumber, lang);
  if (checkLines.length) {
    lines.push(...checkLines);
    lines.push('');
  }

  lines.push(L(lang, '## 4. Environment Variables', '## 4. 当前环境变量'));
  lines.push('');
  for (const name of Object.keys(envVars).sort()) {
    const value = envVars[name].value;
    if (value) lines.push(`- \`${name}=${value}\``);
  }
  lines.push('');
  lines.push(L(lang, 'Important PATH entries include:', '当前用户 `PATH` 中的重要项包括：'));
  lines.push('');
  for (const entry of ((data.path || {}).important_entries) || []) {
    lines.push(`- ${code(formatPathEntry(entry, envVars, osFamily))}`);
  }

  lines.push('');
  lines.push(L(lang, '## 5. Execution Requirements', '## 5. 环境相关任务的执行要求'));
  lines.push('');
  lines.push(
    L(
      lang,
      'Before running build, run, test, debug, script, database, service, migration, or startup tasks, check:',
      '遇到构建、运行、测试、调试、脚本执行、数据库连接、服务启动、迁移、开机启动等任务时，先检查：'
    )
  );
  lines.push('');
  lines.push(L(lang, '1. The current environment facts in this document.', '1. 本文件中的当前环境说明。'));
  lines.push(L(lang, `2. Whether ${code(baselineName)} already contains a matching baseline.`, `2. ${code(baselineName)} 中是否已有对应基线。`));
  lines.push(L(lang, '3. Whether the target tool really exists.', '3. 目标工具是否真的存在。'));
  lines.push(L(lang, '4. Whether the version fits the current task.', '4. 版本是否符合当前任务要求。'));
  lines.push(
    L(
      lang,
      '5. Whether the planned operation will trigger installation, upgrade, global writes, or environment changes.',
      '5. 本次操作是否会触发安装、升级、全局写入或环境改动。'
    )
  );
  lines.push('');
  lines.push(L(lang, 'If item 5 is true, obtain explicit user approval first.', '如果第 5 项答案是“会”，必须先得到用户明确同意。'));
  lines.push('');
  lines.push(L(lang, '## 6. Maintenance Rules', '## 6. 后续维护要求'));
  lines.push('');
  lines.push(
    L(
      lang,
      `- Update both this document and ${code(baselineName)} whenever verified environment facts change.`,
      `- 只要环境事实变化，就同步更新本文件和 ${code(baselineName)}。`
    )
  );
  lines.push(
    L(
      lang,
      '- If the task only introduces one new tool, verify it surgically instead of doing a blind full rescan.',
      '- 如果任务只涉及一个新工具，先做针对性校验，不要盲目全量重扫。'
    )
  );
  lines.push(
    L(
      lang,
      '- Keep shims, wrappers, symlinks, startup scripts, and real install directories separate in the docs.',
      '- 对 shim、wrapper、symlink、启动脚本和真实安装目录要分开记录，避免混淆。'
    )
  );

  return `${lines.join('\n').replace(/\n{3,}/g, '\n\n').trim()}\n`;
}

function renderAgentsSnippet(policyName, baselineName, lang) {
  const lines = [
    L(lang, '# Environment Rules', '# 环境规则'),
    '',
    L(lang, '## Read This First', '## 先读这里'),
    '',
    L(
      lang,
      `- Read ${code(policyName)} before any task involving local tools, CLIs, SDKs, runtimes, compilers, environment variables, databases, services, startup scripts, builds, tests, or debugging.`,
      `- 只要任务涉及本机工具、CLI、SDK、运行时、编译器、环境变量、数据库、服务、脚本启动、构建、测试或调试，先读取 ${code(policyName)}。`
    ),
    L(
      lang,
      `- If ${code(baselineName)} already exists, reuse it as the machine-readable baseline. If it does not exist, detect the machine first and write it.`,
      `- 如果 ${code(baselineName)} 已存在，优先将其作为机器可复用基线；不存在时先探测并写入。`
    ),
    '',
    L(lang, '## Hard Rules', '## 硬性规则'),
    '',
    L(
      lang,
      '- Do not download, install, upgrade, uninstall, or auto-configure software, CLIs, SDKs, runtimes, databases, browsers, drivers, plugins, or global dependencies without explicit user approval.',
      '- 未经用户明确要求，不得下载、安装、升级、卸载或自动配置任何软件、CLI、SDK、运行时、数据库、浏览器、驱动、插件或全局依赖。'
    ),
    L(
      lang,
      '- Do not modify `PATH`, `JAVA_HOME`, `MAVEN_HOME`, or other environment variables without explicit user approval.',
      '- 未经用户明确要求，不得修改 `PATH`、`JAVA_HOME`、`MAVEN_HOME` 等环境变量。'
    ),
    L(
      lang,
      '- Full filesystem access does not mean you may change the machine environment without permission.',
      '- 完全访问权限不等于可以擅自改动本机环境。'
    ),
    '',
    L(lang, '## What To Do When Tools Are Missing', '## 缺工具时必须怎么做'),
    '',
    L(lang, '- Tell the user exactly which tool is missing.', '- 明确告诉用户缺少哪个工具。'),
    L(lang, '- Explain why that tool is needed.', '- 说明这个工具为什么需要。'),
    L(
      lang,
      '- Ask for the executable path or install directory that should be returned after installation.',
      '- 告诉用户安装完成后需要返回哪个可执行文件路径或安装目录。'
    ),
    L(
      lang,
      '- Default to user-managed installation. Only install the tool yourself when the user explicitly authorizes it.',
      '- 默认等待用户自行安装；只有用户明确授权并要求代理代装时，才可安装。'
    ),
    L(
      lang,
      `- Update both ${code(policyName)} and ${code(baselineName)} after verification.`,
      `- 校验完成后，更新 ${code(policyName)} 和 ${code(baselineName)}。`
    ),
    '',
    L(lang, '## Execution Style', '## 执行方式'),
    '',
    L(
      lang,
      '- Prefer tools that already exist on the machine and are already recorded in the baseline.',
      '- 优先使用机器上已经存在并已登记的工具。'
    ),
    L(
      lang,
      '- Use absolute paths, version commands, and targeted probes to verify that a tool is really available.',
      '- 用绝对路径、版本命令和针对性探针检查工具是否真的可用。'
    ),
    L(
      lang,
      '- If the existing baseline and the live machine disagree, re-check the mismatch before updating docs.',
      '- 如果已有基线与现场不一致，先局部复核，再更新文档。'
    ),
    L(
      lang,
      '- Do not confuse shims, wrappers, symlinks, or startup scripts with the real install root.',
      '- 不要把 shim、wrapper、symlink 或启动脚本误认为真实安装根目录。'
    ),
  ];
  return `${lines.join('\n').trim()}\n`;
}

function renderSkillSnippet(policyName, baselineName, lang) {
  const lines = [
    L(lang, '## Environment Baseline', '## 环境基线'),
    '',
    L(
      lang,
      `- Read ${code(policyName)} before any build, run, test, debug, install, service, database, compiler, runtime, or startup-script task.`,
      `- 在任何构建、运行、测试、调试、安装、服务、数据库、编译器、运行时或启动脚本任务之前，先读取 ${code(policyName)}。`
    ),
    L(
      lang,
      `- Reuse ${code(baselineName)} as the machine-readable baseline when it already exists.`,
      `- 如果 ${code(baselineName)} 已存在，优先复用它作为机器可读基线。`
    ),
    L(
      lang,
      '- If the baseline does not exist, detect the current machine first and write the baseline before describing the environment.',
      '- 如果基线不存在，先探测当前机器并写入基线，再描述环境。'
    ),
    L(
      lang,
      '- If a task mentions a tool that is missing from the baseline, verify that tool first and then update both the baseline and human-readable docs.',
      '- 如果任务提到一个未出现在基线中的工具，先定向校验该工具，再更新基线和人类可读文档。'
    ),
    L(
      lang,
      '- If a required tool is missing, ask the user to install it or obtain explicit approval before installing it yourself.',
      '- 如果缺少必需工具，先让用户安装，或在自行安装前取得明确授权。'
    ),
    L(
      lang,
      '- Keep shims, wrappers, symlinks, launchers, startup scripts, and real install directories clearly separated in the docs.',
      '- 在文档中清晰区分 shim、wrapper、symlink、launcher、启动脚本和真实安装目录。'
    ),
  ];
  return `${lines.join('\n').trim()}\n`;
}

function writeOutput(pathname, content) {
  if (!pathname) return;
  fs.mkdirSync(path.dirname(pathname), { recursive: true });
  fs.writeFileSync(pathname, content, 'utf8');
}

function parseArgs(argv) {
  const args = {
    baseline: null,
    policy_out: null,
    agents_out: null,
    skill_snippet_out: null,
    policy_name: 'ENVIRONMENT_POLICY.md',
    baseline_name: 'environment-baseline.json',
    lang: 'auto',
    stdout: null,
  };

  if (!argv.length) {
    printHelp();
    process.exit(1);
  }

  args.baseline = argv[0];
  for (let index = 1; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    }
    if (!arg.startsWith('--')) {
      throw new Error(`Unexpected argument: ${arg}`);
    }
    const key = arg.slice(2).replace(/-/g, '_');
    const value = argv[index + 1];
    if (value == null || value.startsWith('--')) {
      throw new Error(`Missing value for ${arg}`);
    }
    args[key] = value;
    index += 1;
  }

  return args;
}

function printHelp() {
  process.stdout.write(
    [
      'Usage: node scripts/render_environment_docs.js <baseline> [options]',
      '',
      'Options:',
      '  --policy-out <path>         Write ENVIRONMENT_POLICY markdown here.',
      '  --agents-out <path>         Write AGENTS environment snippet here.',
      '  --skill-snippet-out <path>  Write a reusable skill snippet here.',
      '  --policy-name <name>        Display name used inside rendered documents.',
      '  --baseline-name <name>      Display name used inside rendered documents.',
      '  --lang <value>              Document language preference: auto, en, or zh.',
      '  --stdout <kind>             Print one rendered document: policy, agents, or skill.',
    ].join('\n') + '\n'
  );
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const data = loadJson(args.baseline);
    const lang = chooseDocumentLanguage(data, args.lang);
    const policy = renderPolicy(data, args.baseline_name, lang);
    const agents = renderAgentsSnippet(args.policy_name, args.baseline_name, lang);
    const skill = renderSkillSnippet(args.policy_name, args.baseline_name, lang);

    writeOutput(args.policy_out, policy);
    writeOutput(args.agents_out, agents);
    writeOutput(args.skill_snippet_out, skill);

    if (args.stdout === 'policy') process.stdout.write(policy);
    else if (args.stdout === 'agents') process.stdout.write(agents);
    else if (args.stdout === 'skill') process.stdout.write(skill);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exit(1);
  }
}

main();
