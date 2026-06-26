#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const DEFAULT_TOOL_SPECS = {
  git: {
    label: 'Git',
    commands: ['git'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'git version\\s+(.+)',
  },
  java: {
    label: 'Java',
    commands: ['java'],
    env_var_hint: 'JAVA_HOME',
    env_var_suffix_windows: ['bin', 'java.exe'],
    env_var_suffix_posix: ['bin', 'java'],
    version_command: ['{selected_executable}', '-version'],
    version_stream: 'stderr',
    version_regex: 'version "([^"]+)"',
  },
  javac: {
    label: 'javac',
    commands: ['javac'],
    env_var_hint: 'JAVA_HOME',
    env_var_suffix_windows: ['bin', 'javac.exe'],
    env_var_suffix_posix: ['bin', 'javac'],
    version_command: ['{selected_executable}', '-version'],
    version_regex: 'javac\\s+([^\\s]+)',
  },
  maven: {
    label: 'Maven',
    commands_windows: ['mvn.cmd', 'mvn'],
    commands_posix: ['mvn'],
    env_var_hint: 'MAVEN_HOME',
    env_var_suffix_windows: ['bin', 'mvn.cmd'],
    env_var_suffix_posix: ['bin', 'mvn'],
    version_command: ['{selected_executable}', '-version'],
    version_regex: 'Apache Maven\\s+([^\\s]+)',
  },
  gradle: {
    label: 'Gradle',
    commands_windows: ['gradle.bat', 'gradle'],
    commands_posix: ['gradle'],
    env_var_hint: 'GRADLE_HOME',
    env_var_suffix_windows: ['bin', 'gradle.bat'],
    env_var_suffix_posix: ['bin', 'gradle'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'Gradle\\s+([^\\s]+)',
  },
  node: {
    label: 'Node.js',
    commands: ['node', 'nodejs'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: '(v\\d+\\.\\d+\\.\\d+)',
  },
  npm: {
    label: 'npm',
    commands_windows: ['npm.cmd', 'npm'],
    commands_posix: ['npm'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: '(\\d+\\.\\d+\\.\\d+)',
  },
  pnpm: {
    label: 'pnpm',
    commands_windows: ['pnpm.cmd', 'pnpm'],
    commands_posix: ['pnpm'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: '([^\\s]+)',
  },
  yarn: {
    label: 'Yarn',
    commands_windows: ['yarn.cmd', 'yarn'],
    commands_posix: ['yarn'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: '([^\\s]+)',
  },
  python: {
    label: 'Python',
    commands_windows: ['python', 'py'],
    commands_posix: ['python3', 'python'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'Python\\s+([^\\s]+)',
  },
  go: {
    label: 'Go',
    commands: ['go'],
    env_var_hint: 'GOROOT',
    env_var_suffix_windows: ['bin', 'go.exe'],
    env_var_suffix_posix: ['bin', 'go'],
    version_command: ['{selected_executable}', 'version'],
    version_regex: 'go version go([^\\s]+)',
  },
  rustc: {
    label: 'Rust',
    commands: ['rustc'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'rustc\\s+([^\\s]+)',
  },
  cargo: {
    label: 'Cargo',
    commands: ['cargo'],
    env_var_hint: 'CARGO_HOME',
    env_var_suffix_windows: ['bin', 'cargo.exe'],
    env_var_suffix_posix: ['bin', 'cargo'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'cargo\\s+([^\\s]+)',
  },
  rustup: {
    label: 'Rustup',
    commands: ['rustup'],
    env_var_hint: 'CARGO_HOME',
    env_var_suffix_windows: ['bin', 'rustup.exe'],
    env_var_suffix_posix: ['bin', 'rustup'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'rustup\\s+([^\\s]+)',
  },
  clang: {
    label: 'Clang',
    commands: ['clang'],
    version_command: ['{selected_executable}', '--version'],
  },
  clangxx: {
    label: 'Clang++',
    commands: ['clang++'],
    version_command: ['{selected_executable}', '--version'],
  },
  gcc: {
    label: 'GCC',
    commands: ['gcc'],
    version_command: ['{selected_executable}', '--version'],
  },
  gxx: {
    label: 'G++',
    commands: ['g++'],
    version_command: ['{selected_executable}', '--version'],
  },
  cmake: {
    label: 'CMake',
    commands: ['cmake'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'cmake version\\s+([^\\s]+)',
  },
  make: {
    label: 'Make',
    commands: ['make'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'GNU Make\\s+([^\\s]+)',
  },
  ninja: {
    label: 'Ninja',
    commands: ['ninja'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: '([^\\s]+)',
  },
  ruby: {
    label: 'Ruby',
    commands: ['ruby'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'ruby\\s+([^\\s]+)',
  },
  gem: {
    label: 'RubyGems',
    commands_windows: ['gem.bat', 'gem'],
    commands_posix: ['gem'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: '([^\\s]+)',
  },
  bundler: {
    label: 'Bundler',
    commands_windows: ['bundle.bat', 'bundle', 'bundler.bat', 'bundler'],
    commands_posix: ['bundle', 'bundler'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'Bundler version\\s+([^\\s]+)',
  },
  php: {
    label: 'PHP',
    commands: ['php'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'PHP\\s+([^\\s]+)',
  },
  composer: {
    label: 'Composer',
    commands_windows: ['composer.bat', 'composer'],
    commands_posix: ['composer'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'Composer version\\s+([^\\s]+)',
  },
  dotnet: {
    label: '.NET SDK',
    commands: ['dotnet'],
    env_var_hint: 'DOTNET_ROOT',
    env_var_suffix_windows: ['dotnet.exe'],
    env_var_suffix_posix: ['dotnet'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: '([^\\s]+)',
  },
  docker: {
    label: 'Docker',
    commands: ['docker'],
    version_command: ['{selected_executable}', '--version'],
    version_regex: 'Docker version\\s+([^,\\s]+)',
  },
  kubectl: {
    label: 'kubectl',
    commands: ['kubectl'],
    version_command: ['{selected_executable}', 'version', '--client'],
    version_regex: 'Client Version:\\s*v?([^\\s]+)',
  },
};

const DEFAULT_ENV_VARS = [
  'JAVA_HOME',
  'MAVEN_HOME',
  'GRADLE_HOME',
  'GOROOT',
  'GOPATH',
  'CARGO_HOME',
  'RUSTUP_HOME',
  'NVM_DIR',
  'PYENV_ROOT',
  'RBENV_ROOT',
  'SDKMAN_DIR',
  'HOMEBREW_PREFIX',
  'VIRTUAL_ENV',
  'GEM_HOME',
  'BUNDLE_PATH',
  'COMPOSER_HOME',
  'DOTNET_ROOT',
  'CC',
  'CXX',
];

const COMMON_PATH_MARKERS = [
  'java',
  'maven',
  'gradle',
  'node',
  'python',
  'go',
  'cargo',
  'rust',
  'llvm',
  'clang',
  'gcc',
  'cmake',
  'ninja',
  'ruby',
  'php',
  'composer',
  'dotnet',
  'docker',
  'kube',
];
const PLATFORM_PATH_MARKERS = {
  windows: ['windowsapps', 'nvm', 'nodejs', 'cargo', 'rustup', 'dotnet', 'scoop', 'chocolatey', 'msys', 'mingw', 'ruby', 'php'],
  macos: ['.nvm', '.pyenv', '.rbenv', '.sdkman', '.cargo', '.rustup', '/opt/homebrew', '/usr/local/bin'],
  linux: ['.nvm', '.pyenv', '.rbenv', '.sdkman', '.cargo', '.rustup', '/usr/local/bin', '/usr/lib/jvm', '/snap/bin'],
};

function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

function detectOsFamily() {
  if (process.platform === 'win32') return 'windows';
  if (process.platform === 'darwin') return 'macos';
  if (process.platform === 'linux') return 'linux';
  return process.platform || 'unknown';
}

function expandUserHome(raw) {
  if (!raw) return raw;
  if (raw === '~') return os.homedir();
  if (raw.startsWith('~/') || raw.startsWith('~\\')) {
    return path.join(os.homedir(), raw.slice(2));
  }
  return raw;
}

function canonicalizePath(raw) {
  if (!raw) return null;
  const expanded = expandUserHome(String(raw));
  try {
    return fs.realpathSync.native(expanded);
  } catch (_) {
    try {
      return path.resolve(expanded);
    } catch (_) {
      return path.normalize(expanded);
    }
  }
}

function pathExists(raw) {
  if (!raw) return false;
  try {
    return fs.existsSync(expandUserHome(String(raw)));
  } catch (_) {
    return false;
  }
}

function normalizeToolId(raw) {
  return String(raw || '').trim().toLowerCase().replace(/_/g, '-');
}

function normalizePathKey(value) {
  if (value == null) return '';
  let normalized = path.normalize(String(value));
  if (detectOsFamily() === 'windows') {
    normalized = normalized.toLowerCase();
  }
  return normalized;
}

function uniqueStrings(values) {
  const seen = new Set();
  const output = [];
  for (const item of values) {
    const key = normalizePathKey(item);
    if (!key || seen.has(key)) continue;
    seen.add(key);
    output.push(item);
  }
  return output;
}

function trimText(text, maxChars = 1200, maxLines = 20) {
  const lines = String(text || '').split(/\r?\n/);
  const trimmedLines = lines.slice(0, maxLines);
  let trimmed = trimmedLines.join('\n');
  if (trimmed.length > maxChars) {
    trimmed = `${trimmed.slice(0, maxChars - 3)}...`;
  }
  return trimmed;
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

  return uniqueStrings(candidates.filter(Boolean));
}

function chooseDocumentLanguage(explicitLang) {
  const normalizedExplicit = normalizeLang(explicitLang);
  if (explicitLang && explicitLang !== 'auto' && normalizedExplicit) {
    return {
      documentLanguage: normalizedExplicit,
      detectedLocale: explicitLang,
      localeCandidates: [explicitLang],
      languageSource: 'argument',
    };
  }

  const candidates = detectLocaleCandidates();
  for (const candidate of candidates) {
    const normalized = normalizeLang(candidate);
    if (normalized) {
      return {
        documentLanguage: normalized,
        detectedLocale: candidate,
        localeCandidates: candidates,
        languageSource: 'system',
      };
    }
  }

  return {
    documentLanguage: 'en',
    detectedLocale: candidates[0] || null,
    localeCandidates: candidates,
    languageSource: 'default',
  };
}

function quoteWindowsArgument(value) {
  const text = String(value);
  if (!/[ \t"]/.test(text)) return text;
  return `"${text
    .replace(/(\\*)"/g, '$1$1\\"')
    .replace(/(\\+)$/g, '$1$1')}"`;
}

function windowsExecutableRank(candidate) {
  const extension = path.extname(String(candidate || '')).toLowerCase();
  if (extension === '.exe') return 0;
  if (extension === '.cmd') return 1;
  if (extension === '.bat') return 2;
  if (extension === '.com') return 3;
  if (extension) return 4;
  return 5;
}

function runCommand(command, options = {}) {
  const timeoutSeconds = options.timeout == null ? 8 : Number(options.timeout);
  try {
    let result;
    const isWindows = detectOsFamily() === 'windows';
    const executable = String(command[0] || '');
    const isBatchFile = isWindows && /\.(cmd|bat)$/i.test(executable);
    if (isBatchFile) {
      const commandText = command.map((item) => quoteWindowsArgument(item)).join(' ');
      result = spawnSync(process.env.ComSpec || 'cmd.exe', ['/d', '/s', '/c', commandText], {
        cwd: options.cwd || undefined,
        encoding: 'utf8',
        windowsHide: true,
        timeout: timeoutSeconds * 1000,
      });
    } else {
      result = spawnSync(executable, command.slice(1), {
        cwd: options.cwd || undefined,
        encoding: 'utf8',
        windowsHide: true,
        timeout: timeoutSeconds * 1000,
      });
    }

    if (result.error) {
      if (result.error.code === 'ETIMEDOUT') {
        const stdout = result.stdout || '';
        const stderr = result.stderr || '';
        return {
          status: 'timeout',
          error: `Timed out after ${timeoutSeconds}s`,
          exit_code: null,
          stdout,
          stderr,
          combined: `${stdout}\n${stderr}`.trim(),
        };
      }
      return {
        status: 'error',
        error: result.error.message,
        exit_code: null,
        stdout: result.stdout || '',
        stderr: result.stderr || '',
        combined: result.error.message,
      };
    }

    const stdout = result.stdout || '';
    const stderr = result.stderr || '';
    const combined = [stdout, stderr].filter(Boolean).join('\n').trim();
    return {
      status: result.status === 0 ? 'ok' : 'nonzero_exit',
      exit_code: result.status,
      stdout,
      stderr,
      combined,
    };
  } catch (error) {
    return {
      status: 'error',
      error: error.message,
      exit_code: null,
      stdout: '',
      stderr: '',
      combined: error.message,
    };
  }
}

function resolveCommandMatches(commandName) {
  const result = detectOsFamily() === 'windows'
    ? runCommand(['where', commandName])
    : runCommand(['which', '-a', commandName]);

  if (!['ok', 'nonzero_exit'].includes(result.status)) {
    return [];
  }

  const matches = [];
  for (const line of String(result.stdout || '').split(/\r?\n/)) {
    const stripped = line.trim();
    if (stripped && pathExists(stripped)) {
      matches.push(canonicalizePath(stripped) || stripped);
    }
  }
  const ordered = uniqueStrings(matches);
  if (detectOsFamily() === 'windows') {
    ordered.sort((left, right) => windowsExecutableRank(left) - windowsExecutableRank(right));
  }
  return ordered;
}

function extractVersion(text, regex) {
  const source = String(text || '');
  if (!source) return null;
  if (regex) {
    const match = source.match(new RegExp(regex, 'm'));
    if (match) return match[1].trim();
    return null;
  }
  const firstLine = source.split(/\r?\n/).find((line) => line.trim());
  return firstLine ? firstLine.trim() : null;
}

function readText(pathname) {
  const content = fs.readFileSync(pathname, 'utf8');
  return content.charCodeAt(0) === 0xfeff ? content.slice(1) : content;
}

function loadJson(pathname) {
  if (!pathname || !pathExists(pathname)) return null;
  return JSON.parse(readText(pathname));
}

function chooseBaselinePath(args) {
  if (args.baseline) return args.baseline;
  if (args.output && pathExists(args.output)) return args.output;
  return null;
}

function loadProbeFile(pathname) {
  if (!pathname) return {};
  return JSON.parse(readText(pathname));
}

function mergeToolSpecs(extraProbeData) {
  const merged = deepClone(DEFAULT_TOOL_SPECS);
  for (const item of extraProbeData.tools || []) {
    const toolId = normalizeToolId(item.id);
    const base = merged[toolId] || {};
    merged[toolId] = { ...deepClone(base), ...deepClone(item), id: toolId };
  }
  return merged;
}

function getRequestedToolIds(rawTools, toolSpecs, baselineData) {
  if (!rawTools) {
    return Object.keys(toolSpecs);
  }

  const requested = rawTools
    .split(',')
    .map((item) => normalizeToolId(item))
    .filter(Boolean);
  const baselineTools = (baselineData && baselineData.tools) || {};
  const unknown = requested.filter((item) => !(item in toolSpecs) && !(item in baselineTools));
  if (unknown.length) {
    const known = Object.keys(toolSpecs).sort().join(', ');
    throw new Error(`Unknown tool id(s): ${unknown.join(', ')}. Known ids: ${known}`);
  }
  return requested;
}

function lookupCommands(spec) {
  const family = detectOsFamily();
  if (family === 'windows' && spec.commands_windows) return spec.commands_windows;
  if (family === 'macos' && spec.commands_macos) return spec.commands_macos;
  if (family === 'linux' && spec.commands_linux) return spec.commands_linux;
  if ((family === 'macos' || family === 'linux') && spec.commands_posix) return spec.commands_posix;
  return spec.commands || [];
}

function envVarSuffix(spec) {
  const family = detectOsFamily();
  if (family === 'windows') return spec.env_var_suffix_windows || spec.env_var_suffix || null;
  if (family === 'macos') return spec.env_var_suffix_macos || spec.env_var_suffix_posix || spec.env_var_suffix || null;
  if (family === 'linux') return spec.env_var_suffix_linux || spec.env_var_suffix_posix || spec.env_var_suffix || null;
  return spec.env_var_suffix || null;
}

function preferredExecutableFromEnv(spec, envValues) {
  const envVarHint = spec.env_var_hint;
  if (!envVarHint) return null;
  const envValue = envValues[envVarHint];
  if (!envValue) return null;
  const suffix = envVarSuffix(spec);
  if (!suffix) return null;
  return canonicalizePath(path.join(envValue, ...suffix));
}

function firstExistingPath(values) {
  for (const value of values) {
    const normalized = canonicalizePath(value);
    if (normalized && pathExists(normalized)) {
      return normalized;
    }
  }
  return null;
}

function buildLookupSummary(commands) {
  const commandHits = {};
  const allMatches = [];
  for (const commandName of commands) {
    const matches = resolveCommandMatches(commandName);
    commandHits[commandName] = matches;
    allMatches.push(...matches);
  }
  const ordered = uniqueStrings(allMatches);
  return {
    commands,
    command_hits: commandHits,
    all_matches: ordered,
    path_hit: ordered[0] || null,
  };
}

function comparePaths(left, right) {
  if (left == null || right == null) return null;
  return normalizePathKey(left) === normalizePathKey(right);
}

function buildVersionCommand(spec, selectedExecutable) {
  if (!spec.version_command || !selectedExecutable) return null;
  return spec.version_command.map((item) => (item === '{selected_executable}' ? selectedExecutable : item));
}

function chooseSelectedExecutable(spec, baselineEntry, envValues, lookupSummary) {
  const baseline = baselineEntry || {};
  const baselineChoice = firstExistingPath([
    baseline.selected_executable,
    baseline.preferred_path,
    baseline.resolved_path,
  ]);
  if (baselineChoice) {
    return { selectedExecutable: baselineChoice, selectionReason: 'baseline' };
  }

  const envChoice = preferredExecutableFromEnv(spec, envValues);
  if (envChoice && pathExists(envChoice)) {
    return { selectedExecutable: envChoice, selectionReason: 'env_var_hint' };
  }

  const pathHit = lookupSummary.path_hit;
  if (pathHit && pathExists(pathHit)) {
    return { selectedExecutable: pathHit, selectionReason: 'path_hit' };
  }

  return { selectedExecutable: null, selectionReason: 'unresolved' };
}

function summarizeVersionProbe(spec, selectedExecutable) {
  const command = buildVersionCommand(spec, selectedExecutable);
  if (!command) {
    return {
      status: 'skipped',
      version: null,
      version_text: '',
      version_command: null,
      exit_code: null,
      stdout: '',
      stderr: '',
    };
  }

  const result = runCommand(command);
  const stream = spec.version_stream || 'combined';
  const versionText = trimText(
    stream === 'stdout' || stream === 'stderr' || stream === 'combined'
      ? result[stream] || ''
      : result.combined
  );
  const version = extractVersion(versionText || result.combined, spec.version_regex);
  return {
    status: result.status,
    version,
    version_text: versionText || trimText(result.combined),
    version_command: command,
    exit_code: result.exit_code,
    stdout: trimText(result.stdout),
    stderr: trimText(result.stderr),
  };
}

function buildPythonDetails(tool, lookupSummary) {
  const selected = tool.selected_executable;
  const executableDir = selected ? path.dirname(selected) : null;
  return {
    current_interpreter: selected,
    scripts_dir: executableDir,
    bin_dir: executableDir,
    python_launcher: (lookupSummary.command_hits.python || [])[0] || null,
    python3_launcher: (lookupSummary.command_hits.python3 || [])[0] || null,
    py_launcher: (lookupSummary.command_hits.py || [])[0] || null,
  };
}

function detectTool(toolId, spec, baselineEntry, envValues) {
  const commands = lookupCommands(spec);
  const lookupSummary = buildLookupSummary(commands);
  const selection = chooseSelectedExecutable(spec, baselineEntry, envValues, lookupSummary);
  const versionProbe = summarizeVersionProbe(spec, selection.selectedExecutable);
  const baselineSelected = canonicalizePath((baselineEntry || {}).selected_executable);
  const pathHit = canonicalizePath(lookupSummary.path_hit);
  const preferredPath = selection.selectedExecutable || preferredExecutableFromEnv(spec, envValues);

  const notes = [];
  if (selection.selectionReason === 'baseline' && comparePaths(baselineSelected, pathHit) === false) {
    notes.push('Existing baseline path was preferred over the current PATH hit.');
  }
  if (selection.selectionReason === 'env_var_hint' && comparePaths(selection.selectedExecutable, pathHit) === false) {
    const envVarHint = spec.env_var_hint;
    if (envVarHint) {
      notes.push(`PATH currently resolves a different executable; ${envVarHint} was used as the approved path.`);
    }
  }

  const entry = {
    id: toolId,
    label: spec.label || toolId,
    status: selection.selectedExecutable ? 'found' : 'missing',
    commands,
    lookup: lookupSummary,
    selected_executable: selection.selectedExecutable,
    selection_reason: selection.selectionReason,
    preferred_path: preferredPath,
    resolved_path: pathHit,
    baseline_match: comparePaths(selection.selectedExecutable, baselineSelected),
    version: versionProbe.version,
    version_text: versionProbe.version_text,
    version_command: versionProbe.version_command,
    version_probe_status: versionProbe.status,
    version_probe_exit_code: versionProbe.exit_code,
    notes,
  };

  if (toolId === 'python') {
    entry.details = buildPythonDetails(entry, lookupSummary);
  }

  return entry;
}

function collectEnvironmentVariables(extraProbeData, baselineData) {
  const requested = new Set(DEFAULT_ENV_VARS);
  for (const name of extraProbeData.env_vars || []) requested.add(name);
  for (const name of Object.keys(((baselineData || {}).environment_variables) || {})) requested.add(name);

  const output = {};
  for (const name of Array.from(requested).sort()) {
    const value = process.env[name];
    output[name] = {
      status: value ? 'set' : 'unset',
      value: value || null,
    };
  }
  return output;
}

function importantPathMarkers(extraProbeData) {
  const family = detectOsFamily();
  const markers = [
    ...COMMON_PATH_MARKERS,
    ...(PLATFORM_PATH_MARKERS[family] || []),
    ...(extraProbeData.important_path_contains || []),
  ];
  return markers.map((item) => String(item).toLowerCase());
}

function buildPathSummary(tools, envVariables, extraProbeData) {
  const rawPath = process.env.PATH || '';
  const entries = rawPath
    .split(path.delimiter)
    .filter(Boolean)
    .map((item) => canonicalizePath(item) || item);
  const importantEntries = [];

  function maybeAdd(value) {
    const normalized = canonicalizePath(value);
    if (!normalized) return;
    if (!entries.includes(normalized)) return;
    if (!importantEntries.includes(normalized)) {
      importantEntries.push(normalized);
    }
  }

  const javaHome = (envVariables.JAVA_HOME || {}).value;
  const mavenHome = (envVariables.MAVEN_HOME || {}).value;
  if (javaHome) maybeAdd(path.join(javaHome, 'bin'));
  if (mavenHome) maybeAdd(path.join(mavenHome, 'bin'));

  for (const name of [
    'NVM_DIR',
    'PYENV_ROOT',
    'RBENV_ROOT',
    'SDKMAN_DIR',
    'HOMEBREW_PREFIX',
    'VIRTUAL_ENV',
    'GRADLE_HOME',
    'GOROOT',
    'GOPATH',
    'CARGO_HOME',
    'RUSTUP_HOME',
    'GEM_HOME',
    'BUNDLE_PATH',
    'COMPOSER_HOME',
    'DOTNET_ROOT',
  ]) {
    const value = (envVariables[name] || {}).value;
    if (!value) continue;
    maybeAdd(value);
    maybeAdd(path.join(value, 'bin'));
  }

  for (const tool of Object.values(tools)) {
    if (tool.selected_executable) maybeAdd(path.dirname(tool.selected_executable));
    if (tool.id === 'python' && tool.details) {
      maybeAdd(tool.details.bin_dir);
      maybeAdd(tool.details.scripts_dir);
    }
  }

  const markers = importantPathMarkers(extraProbeData);
  for (const entry of entries) {
    if (importantEntries.includes(entry)) continue;
    const lowered = String(entry).toLowerCase();
    if (markers.some((marker) => lowered.includes(marker))) {
      importantEntries.push(entry);
    }
  }

  return {
    entries,
    important_entries: importantEntries,
    separator: path.delimiter,
  };
}

function runChecks(extraProbeData, baselineData) {
  const existingChecks = deepClone((baselineData || {}).checks || {});
  if (!extraProbeData.checks) return existingChecks;

  for (const check of extraProbeData.checks) {
    const result = runCommand(check.command, {
      timeout: check.timeout == null ? 8 : check.timeout,
      cwd: check.cwd || null,
    });
    const capture = check.capture || 'combined';
    const outputText = capture === 'stdout' || capture === 'stderr' || capture === 'combined'
      ? result[capture] || ''
      : result.combined;
    const successPatterns = check.success_patterns || [];
    const matchedPatterns = successPatterns.filter((pattern) => new RegExp(pattern).test(outputText));

    let status = 'passed';
    if (result.status === 'timeout') status = 'timeout';
    else if (result.status === 'error') status = 'error';
    else if (successPatterns.length && matchedPatterns.length !== successPatterns.length) status = 'failed';
    else if (![0, null].includes(result.exit_code) && !successPatterns.length) status = 'failed';

    existingChecks[normalizeToolId(check.id)] = {
      label: check.label || check.id,
      command: check.command,
      status,
      exit_code: result.exit_code,
      matched_patterns: matchedPatterns,
      output_excerpt: trimText(outputText),
    };
  }

  return existingChecks;
}

function computeDifferences(baselineData, currentSnapshot, scannedTools) {
  if (!baselineData) return [];

  const differences = [];
  const baselineTools = baselineData.tools || {};
  const currentTools = currentSnapshot.tools || {};

  for (const toolId of scannedTools) {
    const oldTool = baselineTools[toolId];
    const newTool = currentTools[toolId];
    if (!oldTool && newTool) {
      differences.push({ scope: 'tool', name: toolId, change: 'added' });
      continue;
    }
    if (!oldTool || !newTool) continue;
    for (const field of ['status', 'selected_executable', 'version']) {
      if (oldTool[field] !== newTool[field]) {
        differences.push({
          scope: 'tool',
          name: toolId,
          field,
          before: oldTool[field],
          after: newTool[field],
        });
      }
    }
  }

  const baselineEnv = baselineData.environment_variables || {};
  const currentEnv = currentSnapshot.environment_variables || {};
  for (const [name, currentValue] of Object.entries(currentEnv)) {
    const oldValue = baselineEnv[name] || {};
    if ((oldValue.value || null) !== (currentValue.value || null)) {
      differences.push({
        scope: 'env_var',
        name,
        before: oldValue.value || null,
        after: currentValue.value || null,
      });
    }
  }

  return differences;
}

function parseArgs(argv) {
  const args = {
    baseline: null,
    output: null,
    tools: null,
    probe_file: null,
    lang: 'auto',
    compact: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--compact') {
      args.compact = true;
      continue;
    }
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
      'Usage: node scripts/detect_environment.js [options]',
      '',
      'Options:',
      '  --baseline <path>    Existing baseline JSON to reuse as the source of truth.',
      '  --output <path>      Write the merged snapshot to this JSON file.',
      '  --tools <ids>        Comma-separated tool ids to verify.',
      '  --probe-file <path>  Optional JSON file with extra tools/env vars/checks.',
      '  --lang <value>       Document language preference: auto, en, or zh.',
      '  --compact            Print compact JSON when writing to stdout.',
    ].join('\n') + '\n'
  );
}

function buildSnapshot(args) {
  const baselinePath = chooseBaselinePath(args);
  const baselineData = loadJson(baselinePath);
  const extraProbeData = loadProbeFile(args.probe_file);
  const toolSpecs = mergeToolSpecs(extraProbeData);
  const requestedToolIds = getRequestedToolIds(args.tools, toolSpecs, baselineData);
  const environmentVariables = collectEnvironmentVariables(extraProbeData, baselineData);
  const rawEnvValues = {};
  for (const [name, details] of Object.entries(environmentVariables)) {
    if (details.value) rawEnvValues[name] = details.value;
  }

  const mergedTools = deepClone((baselineData || {}).tools || {});
  for (const toolId of requestedToolIds) {
    const spec = deepClone(toolSpecs[toolId] || { id: toolId, label: toolId, commands: [toolId] });
    spec.id = toolId;
    mergedTools[toolId] = detectTool(
      toolId,
      spec,
      ((baselineData || {}).tools || {})[toolId],
      rawEnvValues
    );
  }

  const language = chooseDocumentLanguage(args.lang);
  const snapshot = deepClone(baselineData || {});
  snapshot.schema_version = 1;
  snapshot.generated_at = utcNow();
  snapshot.context = {
    hostname: os.hostname(),
    platform: `${os.type()} ${os.release()} ${os.arch()}`,
    platform_system: os.type(),
    os_family: detectOsFamily(),
    python_version: null,
    node_version: process.version,
    detector_runtime: 'node',
    cwd: canonicalizePath(process.cwd()),
    scan_mode: args.tools || args.probe_file ? 'targeted' : 'full',
    requested_tools: requestedToolIds,
    baseline_path: canonicalizePath(baselinePath),
    probe_file: canonicalizePath(args.probe_file),
    document_language: language.documentLanguage,
    detected_locale: language.detectedLocale,
    locale_candidates: language.localeCandidates,
    document_language_source: language.languageSource,
  };
  snapshot.tools = mergedTools;
  snapshot.environment_variables = environmentVariables;
  snapshot.path = buildPathSummary(snapshot.tools, environmentVariables, extraProbeData);
  snapshot.checks = runChecks(extraProbeData, baselineData);
  snapshot.differences_from_baseline = computeDifferences(
    baselineData,
    snapshot,
    requestedToolIds
  );
  return snapshot;
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const snapshot = buildSnapshot(args);
    const jsonText = JSON.stringify(snapshot, null, args.compact ? 0 : 2);

    if (args.output) {
      fs.mkdirSync(path.dirname(args.output), { recursive: true });
      fs.writeFileSync(args.output, `${jsonText}\n`, 'utf8');
    } else {
      process.stdout.write(`${jsonText}\n`);
    }
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exit(1);
  }
}

main();
