#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const DAILY_DIR = path.resolve(__dirname, '..');
const WORKSPACE = resolveWorkspaceDir();
const REPORTS_DIR = path.join(WORKSPACE, 'reports');
const REPO_CONTEXTS_PATH = path.join(DAILY_DIR, 'references', 'repo-contexts.json');
const GITHUB_USER = (process.env.GITHUB_USER || '').trim();
const WIB_TZ = 'Asia/Jakarta';
const TARGET_DATE = (process.env.REPORT_DATE || getWibDateKey(new Date())).trim();
const REPORT_FILE = path.join(REPORTS_DIR, `commit-report-${TARGET_DATE}.md`);
const REPORT_SCOPE = (process.env.REPORT_SCOPE || 'internship').trim().toLowerCase();

fs.mkdirSync(REPORTS_DIR, { recursive: true });

const repoInfoCache = new Map();
const repoContextCache = new Map();
const overrides = loadRepoContextOverrides();

if (require.main === module) {
  main();
}

function resolveWorkspaceDir() {
  const candidates = [
    process.env.OPENCLAW_WORKSPACE,
    path.resolve(DAILY_DIR, '..'),
    path.resolve(DAILY_DIR, '../..'),
    process.cwd(),
  ].filter(Boolean);

  for (const candidate of candidates) {
    const resolved = path.resolve(candidate);
    if (
      fs.existsSync(path.join(resolved, 'AGENTS.md'))
      || fs.existsSync(path.join(resolved, 'HEARTBEAT.md'))
      || fs.existsSync(path.join(resolved, 'MEMORY.md'))
      || fs.existsSync(path.join(resolved, 'reports'))
      || fs.existsSync(path.join(resolved, 'skills'))
    ) {
      return resolved;
    }
  }

  return path.resolve(process.cwd());
}

function main() {
  const artifacts = collectArtifacts({
    targetDates: [TARGET_DATE],
    scope: REPORT_SCOPE,
  });
  const repoGroups = buildRepoGroups(artifacts);
  const report = renderReport(repoGroups, artifacts);
  fs.writeFileSync(REPORT_FILE, report, 'utf8');

  process.stdout.write('\n');
  process.stdout.write(`=== LOGBOOK ENTRY FOR ${TARGET_DATE} ===\n`);
  process.stdout.write(renderLogbookOnly(repoGroups));
}

function collectArtifacts(options = {}) {
  const targetDates = (options.targetDates && options.targetDates.length > 0) ? options.targetDates : [TARGET_DATE];
  const scope = options.scope || REPORT_SCOPE;
  return [
    ...collectGitHubArtifacts({ targetDates, scope }),
    ...collectGitLabArtifacts({ targetDates, scope }),
  ];
}

function runCommand(bin, args, options = {}) {
  const result = spawnSync(bin, args, {
    cwd: WORKSPACE,
    env: process.env,
    encoding: 'utf8',
    maxBuffer: 20 * 1024 * 1024,
    ...options,
  });

  if (result.status !== 0) {
    const message = [result.stdout, result.stderr].filter(Boolean).join('\n').trim();
    const error = new Error(message || `${bin} exited with status ${result.status}`);
    error.status = result.status;
    throw error;
  }

  return result.stdout || '';
}

function runJson(bin, args, fallback) {
  try {
    const raw = runCommand(bin, args);
    return raw.trim() ? JSON.parse(raw) : fallback;
  } catch (error) {
    return fallback;
  }
}

function collectGitHubArtifacts(options = {}) {
  if (!GITHUB_USER) return [];

  const targetDates = new Set((options.targetDates && options.targetDates.length > 0) ? options.targetDates : [TARGET_DATE]);
  const scope = options.scope || REPORT_SCOPE;
  const events = runJson('gh', ['api', `/users/${GITHUB_USER}/events`], []);
  return events
    .filter((event) => event?.type === 'PushEvent')
    .filter((event) => targetDates.has(getWibDateKey(event.created_at)))
    .map((event) => buildGitHubArtifact(event))
    .filter((artifact) => artifactMatchesScope(artifact, scope))
    .filter(Boolean);
}

function buildGitHubArtifact(event) {
  const repoFullName = event?.repo?.name;
  const head = event?.payload?.head;
  const before = event?.payload?.before;
  if (!repoFullName || !head) return null;

  const compare = before && !isZeroSha(before)
    ? runJson('gh', ['api', `/repos/${repoFullName}/compare/${before}...${head}`], null)
    : null;

  let files = [];
  let commitMessages = [];
  let webUrl = '';

  if (compare && Array.isArray(compare.files) && compare.files.length > 0) {
    files = compare.files.map((file) => ({
      path: file.filename,
      diff: file.patch || '',
      additions: file.additions || 0,
      deletions: file.deletions || 0,
    }));
    commitMessages = Array.isArray(compare.commits)
      ? compare.commits.map((commit) => firstLine(commit?.commit?.message || '')).filter(Boolean)
      : [];
    webUrl = compare.html_url || '';
  }

  if (files.length === 0) {
    const commit = runJson('gh', ['api', `/repos/${repoFullName}/commits/${head}`], null);
    if (!commit) return null;
    files = Array.isArray(commit.files)
      ? commit.files.map((file) => ({
          path: file.filename,
          diff: file.patch || '',
          additions: file.additions || 0,
          deletions: file.deletions || 0,
        }))
      : [];
    commitMessages = [firstLine(commit?.commit?.message || '')].filter(Boolean);
    webUrl = commit.html_url || '';
  }

  if (files.length === 0) return null;

  const repoInfo = getGitHubRepoInfo(repoFullName);
  const context = getRepoContext({
    provider: 'github',
    repoName: repoInfo.name || basenameRepo(repoFullName),
    repoFullName,
    description: repoInfo.description || '',
    defaultBranch: repoInfo.default_branch || '',
  });

  return {
    provider: 'github',
    repoName: repoInfo.name || basenameRepo(repoFullName),
    repoFullName,
    displayName: context.displayName,
    context,
    ref: refName(event?.payload?.ref),
    commitKey: head,
    commitMessages,
    files,
    webUrl,
    createdAt: event.created_at,
  };
}

function collectGitLabArtifacts(options = {}) {
  const targetDates = new Set((options.targetDates && options.targetDates.length > 0) ? options.targetDates : [TARGET_DATE]);
  const scope = options.scope || REPORT_SCOPE;
  const events = runJson('glab', ['api', '/events', '-X', 'GET'], []);
  return events
    .filter((event) => ['pushed to', 'pushed new', 'created'].includes(event?.action_name))
    .filter((event) => event?.push_data?.ref_type === 'branch')
    .filter((event) => targetDates.has(getWibDateKey(event.created_at)))
    .map((event) => buildGitLabArtifact(event))
    .filter((artifact) => artifactMatchesScope(artifact, scope))
    .filter(Boolean);
}

function buildGitLabArtifact(event) {
  const projectId = event?.project_id;
  const pushData = event?.push_data || {};
  const commitTo = pushData.commit_to;
  if (!projectId || !commitTo) return null;

  const compare = pushData.commit_from && !isZeroSha(pushData.commit_from)
    ? runJson(
        'glab',
        ['api', `/projects/${projectId}/repository/compare?from=${encodeURIComponent(pushData.commit_from)}&to=${encodeURIComponent(commitTo)}`],
        null,
      )
    : null;

  let files = [];
  let commitMessages = [];
  let webUrl = '';

  if (compare && Array.isArray(compare.diffs) && compare.diffs.length > 0) {
    files = compare.diffs.map((file) => ({
      path: file.new_path || file.old_path,
      diff: file.diff || '',
      additions: countDiffLines(file.diff || '', '+'),
      deletions: countDiffLines(file.diff || '', '-'),
    }));
    commitMessages = Array.isArray(compare.commits)
      ? compare.commits.map((commit) => firstLine(commit?.message || commit?.title || '')).filter(Boolean)
      : [];
  }

  if (files.length === 0) {
    const commit = runJson('glab', ['api', `/projects/${projectId}/repository/commits/${commitTo}`], null);
    const diff = runJson('glab', ['api', `/projects/${projectId}/repository/commits/${commitTo}/diff`], []);
    if (!commit || !Array.isArray(diff) || diff.length === 0) return null;
    files = diff.map((file) => ({
      path: file.new_path || file.old_path,
      diff: file.diff || '',
      additions: countDiffLines(file.diff || '', '+'),
      deletions: countDiffLines(file.diff || '', '-'),
    }));
    commitMessages = [firstLine(commit?.message || commit?.title || pushData.commit_title || '')].filter(Boolean);
    webUrl = commit.web_url || '';
  } else {
    const commit = runJson('glab', ['api', `/projects/${projectId}/repository/commits/${commitTo}`], null);
    webUrl = commit?.web_url || '';
  }

  const projectInfo = getGitLabProjectInfo(projectId);
  const repoName = projectInfo.name || event.target_title || `gitlab-project-${projectId}`;
  const repoFullName = projectInfo.path_with_namespace || repoName;
  const context = getRepoContext({
    provider: 'gitlab',
    repoName,
    repoFullName,
    projectId,
    description: projectInfo.description || '',
    defaultBranch: projectInfo.default_branch || '',
  });

  return {
    provider: 'gitlab',
    repoName,
    repoFullName,
    displayName: context.displayName,
    context,
    ref: pushData.ref || '',
    commitKey: commitTo,
    commitMessages,
    files,
    webUrl,
    createdAt: event.created_at,
  };
}

function getGitHubRepoInfo(repoFullName) {
  const cacheKey = `github:${repoFullName}`;
  if (!repoInfoCache.has(cacheKey)) {
    repoInfoCache.set(cacheKey, runJson('gh', ['api', `/repos/${repoFullName}`], {}));
  }
  return repoInfoCache.get(cacheKey) || {};
}

function getGitLabProjectInfo(projectId) {
  const cacheKey = `gitlab:${projectId}`;
  if (!repoInfoCache.has(cacheKey)) {
    repoInfoCache.set(cacheKey, runJson('glab', ['api', `/projects/${projectId}`], {}));
  }
  return repoInfoCache.get(cacheKey) || {};
}

function getRepoContext(input) {
  const cacheKey = `${input.provider}:${input.repoFullName || input.repoName}`;
  if (repoContextCache.has(cacheKey)) return repoContextCache.get(cacheKey);

  const explicit = matchRepoOverride(input);
  const local = inferLocalRepoContext(input);
  const remote = inferRemoteRepoContext(input);

  const context = {
    displayName: explicit?.displayName || local?.displayName || input.repoName,
    summary: explicit?.summary || local?.summary || remote?.summary || genericRepoSummary(input.repoName),
    localPath: local?.localPath || null,
    internshipRelevant: inferInternshipRelevant(input, explicit),
  };

  repoContextCache.set(cacheKey, context);
  return context;
}

function matchRepoOverride(input) {
  const candidates = [input.repoName, input.repoFullName, basenameRepo(input.repoFullName || '')]
    .filter(Boolean)
    .map(normalizeKey);

  for (const repo of overrides.repos || []) {
    const matches = (repo.match || []).map(normalizeKey);
    if (matches.some((value) => candidates.includes(value))) {
      return {
        displayName: repo.displayName || input.repoName,
        summary: repo.summary || '',
        internshipRelevant: typeof repo.internshipRelevant === 'boolean' ? repo.internshipRelevant : undefined,
      };
    }
  }

  return null;
}

function inferInternshipRelevant(input, explicit) {
  if (typeof explicit?.internshipRelevant === 'boolean') {
    return explicit.internshipRelevant;
  }

  const repoFullName = normalizeKey(input.repoFullName || '');
  if (input.provider === 'gitlab' && repoFullName.startsWith('sindika/')) {
    return true;
  }

  if (input.provider === 'github') {
    return false;
  }

  return true;
}

function artifactMatchesScope(artifact, scope) {
  if (!artifact) return false;
  if (scope === 'all') return true;
  if (scope === 'internship') {
    return artifact.context?.internshipRelevant !== false;
  }
  return true;
}

function inferLocalRepoContext(input) {
  const candidates = [
    path.join(WORKSPACE, input.repoName || ''),
    path.join(WORKSPACE, basenameRepo(input.repoFullName || '')),
  ].filter((candidate, index, all) => candidate && all.indexOf(candidate) === index);

  for (const candidate of candidates) {
    if (!candidate || !fs.existsSync(candidate) || !fs.statSync(candidate).isDirectory()) continue;
    const entries = fs.readdirSync(candidate);
    const readmeName = entries.find((entry) => /^readme/i.test(entry));
    const readmeSummary = readmeName
      ? extractReadmeSummary(fs.readFileSync(path.join(candidate, readmeName), 'utf8'))
      : '';
    const hasProgramCs = entries.includes('Program.cs');
    const hasPackageJson = entries.includes('package.json');
    const hasPyproject = entries.includes('pyproject.toml');
    const csprojFiles = entries.filter((entry) => entry.endsWith('.csproj'));

    let summary = readmeSummary;
    if (!summary && hasProgramCs && csprojFiles.length > 0) {
      summary = `ASP.NET backend/API service untuk ${input.repoName}.`;
    } else if (!summary && csprojFiles.length > 0) {
      summary = `.NET library atau service untuk ${input.repoName}.`;
    } else if (!summary && hasPackageJson) {
      summary = `Aplikasi Node.js/JavaScript untuk ${input.repoName}.`;
    } else if (!summary && hasPyproject) {
      summary = `Project Python untuk ${input.repoName}.`;
    }

    if (summary) {
      return {
        displayName: input.repoName,
        summary,
        localPath: candidate,
      };
    }
  }

  return null;
}

function inferRemoteRepoContext(input) {
  if (input.description && input.description.trim()) {
    return { summary: input.description.trim().replace(/\s+/g, ' ') };
  }
  return null;
}

function buildRepoGroups(artifacts) {
  const grouped = new Map();

  for (const artifact of artifacts) {
    const key = artifact.repoFullName || artifact.repoName;
    if (!grouped.has(key)) {
      grouped.set(key, {
        repoName: artifact.repoName,
        repoFullName: artifact.repoFullName,
        displayName: artifact.displayName,
        context: artifact.context,
        artifacts: [],
        themes: new Map(),
      });
    }

    const group = grouped.get(key);
    group.artifacts.push(artifact);

    for (const theme of analyzeArtifactThemes(artifact)) {
      const existing = group.themes.get(theme.key);
      if (!existing || existing.score < theme.score) {
        group.themes.set(theme.key, theme);
      }
    }
  }

  return Array.from(grouped.values())
    .map((group) => {
      const themes = Array.from(group.themes.values())
        .sort((a, b) => b.score - a.score)
        .map((theme) => theme.text);
      return {
        ...group,
        themes,
        maxScore: Array.from(group.themes.values()).reduce((max, theme) => Math.max(max, theme.score), 0),
      };
    })
    .sort((a, b) => b.maxScore - a.maxScore || a.displayName.localeCompare(b.displayName));
}

function analyzeArtifactThemes(artifact) {
  const themes = new Map();
  const lowerText = [artifact.commitMessages.join('\n'), ...artifact.files.map((file) => file.diff || '')].join('\n').toLowerCase();
  const paths = artifact.files.map((file) => file.path || '');
  const pathsLower = paths.map((value) => value.toLowerCase());
  const modelChanges = extractJsonStringChanges(artifact.files, 'Model');
  const defaultModelChanges = extractJsonStringChanges(artifact.files, 'DefaultModel');
  const packageChanges = extractPackageVersionChanges(artifact.files);

  const addTheme = (key, text, score) => {
    if (!text) return;
    const existing = themes.get(key);
    if (!existing || existing.score < score) {
      themes.set(key, { key, text, score });
    }
  };

  if (modelChanges.some((change) => /gpt-5\.4/i.test(change.to || ''))) {
    addTheme(
      'agent-model-upgrade',
      'memperbarui konfigurasi beberapa agent ke model GPT-5.4 mini dan nano',
      10,
    );
  }

  if (defaultModelChanges.some((change) => /gpt-5\.4/i.test(change.to || ''))) {
    addTheme(
      'default-model-upgrade',
      'menyesuaikan default model OpenAI aplikasi ke GPT-5.4 mini',
      8,
    );
  }

  const orchestratorPackage = packageChanges.find((change) => /Nedo\.AspNet\.AgentOrchestration/i.test(change.name || ''));
  if (orchestratorPackage?.to) {
    addTheme(
      'orchestrator-package-bump',
      `menaikkan versi dependency Nedo.AspNet.AgentOrchestration ke ${orchestratorPackage.to}`,
      9,
    );
  }

  if (lowerText.includes('max_completion_tokens')) {
    addTheme(
      'openai-gpt5-token-field',
      'menyesuaikan payload request OpenAI agar model GPT-5 menggunakan parameter token yang sesuai',
      10,
    );
  }

  if (lowerText.includes('providerextensions') || lowerText.includes('reasoning_effort') || lowerText.includes('response_format')) {
    addTheme(
      'provider-extensions',
      'menambahkan dukungan provider extension pada request OpenAI agar opsi model tambahan dapat diteruskan',
      8,
    );
  }

  if (pathsLower.some((file) => /(^|\/)(test|tests)(\/|$)/.test(file))) {
    addTheme(
      'tests',
      'menambahkan unit test untuk memastikan perubahan provider dan konfigurasi tetap kompatibel',
      7,
    );
  }

  if (lowerText.includes('backendpublicbaseurl') || (lowerText.includes('localhost') && lowerText.includes('download'))) {
    addTheme(
      'public-download-url',
      'memperbaiki fitur generate report agar tautan unduhan PDF menggunakan base URL backend publik dari konfigurasi',
      10,
    );
  }

  if (pathsLower.some((file) => file.includes('aireportgenerationservice'))) {
    addTheme(
      'report-service-update',
      'menyesuaikan logic service generate report agar pembentukan tautan file hasil generate lebih sesuai untuk environment publik',
      8,
    );
  }

  if (pathsLower.some((file) => file.includes('readme') || file.includes('/docs/') || file.endsWith('.md'))) {
    addTheme(
      'docs',
      'memperbarui dokumentasi teknis dan panduan penggunaan pada repo yang dikerjakan',
      3,
    );
  }

  if (pathsLower.every((file) => file === '.gitignore' || file.endsWith('/.gitignore') || file.endsWith('gitignore'))) {
    addTheme(
      'repo-hygiene',
      'merapikan konfigurasi dasar repository agar file yang tidak perlu tidak ikut terlacak',
      1,
    );
  }

  if (themes.size === 0) {
    const genericTopic = inferGenericTopic(paths);
    addTheme(
      `generic-${genericTopic.key}`,
      `menyesuaikan ${genericTopic.text} pada ${artifact.displayName || artifact.repoName} berdasarkan perubahan file yang dikerjakan hari ini`,
      genericTopic.score,
    );
  }

  return Array.from(themes.values());
}

function inferGenericTopic(paths) {
  const lowerPaths = paths.map((value) => value.toLowerCase());
  if (lowerPaths.some((file) => file.includes('config') || file.endsWith('.json') || file.endsWith('.yml') || file.endsWith('.yaml'))) {
    return { key: 'configuration', text: 'konfigurasi aplikasi', score: 5 };
  }
  if (lowerPaths.some((file) => file.includes('service') || file.includes('controller') || file.includes('provider'))) {
    return { key: 'logic', text: 'logic layanan dan integrasi', score: 5 };
  }
  if (lowerPaths.some((file) => file.endsWith('.csproj') || file.endsWith('package.json') || file.endsWith('go.mod'))) {
    return { key: 'dependency', text: 'dependency dan pengaturan build', score: 4 };
  }
  if (lowerPaths.some((file) => file.endsWith('.md'))) {
    return { key: 'documentation', text: 'dokumentasi teknis', score: 3 };
  }
  return { key: 'implementation', text: 'implementasi modul utama', score: 4 };
}

function renderReport(repoGroups, artifacts) {
  const dateLabel = formatIndonesianDate(TARGET_DATE);
  const logbook = renderLogbookOnly(repoGroups);
  const evidence = renderEvidence(repoGroups);
  const sources = renderSources(artifacts);
  return [
    `# Daily Commit Report - ${TARGET_DATE}`,
    '',
    `Tanggal WIB: ${dateLabel}`,
    '',
    '## Activity Sources',
    '',
    sources,
    '',
    '## Diff-derived Findings',
    '',
    evidence,
    '',
    '---',
    '',
    '## 📋 Logbook Entry (Ready to Copy)',
    '',
    logbook,
    '',
    `Generated at: ${new Date().toISOString()}`,
    '',
  ].join('\n');
}

function renderSources(artifacts) {
  if (artifacts.length === 0) return '- Tidak ada push event GitHub/GitLab yang terdeteksi pada tanggal target.';
  const lines = artifacts.map((artifact) => {
    const provider = artifact.provider === 'gitlab' ? 'GitLab' : 'GitHub';
    const commitCount = artifact.commitMessages.length || 1;
    return `- ${provider} • ${artifact.displayName} • ref ${artifact.ref || '-'} • ${commitCount} commit/push range`;
  });
  return lines.join('\n');
}

function renderEvidence(repoGroups) {
  if (repoGroups.length === 0) return '- Tidak ada perubahan yang bisa dianalisis.';
  return repoGroups
    .map((group) => {
      const allFiles = unique(group.artifacts.flatMap((artifact) => artifact.files.map((file) => file.path))).slice(0, 12);
      const commits = unique(group.artifacts.flatMap((artifact) => artifact.commitMessages)).slice(0, 8);
      const commitLinks = unique(group.artifacts.map((artifact) => artifact.webUrl).filter(Boolean)).slice(0, 4);
      const lines = [
        `### ${group.displayName}`,
        '',
        `**Konteks repo:** ${group.context.summary}`,
        '',
        '**Commit / push yang dianalisis:**',
        ...(commits.length ? commits.map((commit) => `- ${commit}`) : ['- Tidak ada judul commit yang tersedia.']),
        '',
        '**File yang berubah (cuplikan):**',
        ...(allFiles.length ? allFiles.map((file) => `- ${file}`) : ['- Tidak ada file diff yang tersedia.']),
        '',
        '**Tema hasil baca diff:**',
        ...(group.themes.length ? group.themes.map((theme) => `- ${capitalize(theme)}`) : ['- Belum ada tema yang terdeteksi.']),
      ];

      if (commitLinks.length > 0) {
        lines.push('', '**Referensi commit:**', ...commitLinks.map((link) => `- ${link}`));
      }

      return lines.join('\n');
    })
    .join('\n\n');
}

function renderLogbookOnly(repoGroups) {
  const dateLabel = formatIndonesianDate(TARGET_DATE);
  const activityThemes = selectActivityThemes(repoGroups);
  const overview = buildOverview(repoGroups, activityThemes);
  const resultLines = buildResultLines(activityThemes);

  if (activityThemes.length === 0) {
    return [
      '### Versi 1 — Standar',
      '',
      `**Tanggal:** ${dateLabel}`,
      '',
      '**Aktivitas:**',
      'Melakukan review pekerjaan harian, pengecekan perubahan repository, dan penyusunan rencana tindak lanjut berdasarkan aktivitas pengembangan yang tersedia.',
      '',
      '**Hasil:**',
      '- Perubahan repository berhasil ditinjau untuk kebutuhan dokumentasi logbook',
      '- Catatan aktivitas harian siap disesuaikan lebih lanjut bila diperlukan',
      '- Rencana tindak lanjut pekerjaan berikutnya dapat disusun dengan lebih jelas',
      '',
      '**Jam Kerja:** 8 jam',
      '',
      '### Versi 2 — Lebih Natural untuk MIS',
      '',
      `**Tanggal:** ${dateLabel}`,
      '',
      '**Aktivitas:**',
      'Pada hari ini saya melakukan peninjauan terhadap perubahan repository yang tersedia dan menyiapkan rangkuman pekerjaan harian sebagai dasar penyusunan logbook MIS.',
      '',
      '**Hasil:**',
      '- Ringkasan perubahan harian berhasil dikumpulkan',
      '- Aktivitas kerja siap ditindaklanjuti untuk pelaporan',
      '- Catatan logbook dapat diperbarui kembali jika ada perubahan tambahan',
      '',
      '**Jam Kerja:** 8 jam',
    ].join('\n');
  }

  const standardBullets = activityThemes.map((theme) => `- ${ensureSentence(capitalize(theme))}`);
  const naturalBullets = activityThemes.map((theme) => `- ${ensureSentence(capitalize(theme))}`);

  return [
    '### Versi 1 — Standar',
    '',
    `**Tanggal:** ${dateLabel}`,
    '',
    '**Aktivitas:**',
    'Melakukan pengembangan dan penyempurnaan pada repository yang dikerjakan hari ini. Aktivitas utama meliputi:',
    '',
    ...standardBullets,
    '',
    '**Hasil:**',
    ...resultLines.map((line) => `- ${line}`),
    '',
    '**Jam Kerja:** 8 jam',
    '',
    '### Versi 2 — Lebih Natural untuk MIS',
    '',
    `**Tanggal:** ${dateLabel}`,
    '',
    '**Aktivitas:**',
    overview,
    '',
    ...naturalBullets,
    '',
    '**Hasil:**',
    ...resultLines.map((line) => `- ${line}`),
    '',
    '**Jam Kerja:** 8 jam',
  ].join('\n');
}

function selectActivityThemes(repoGroups) {
  const limit = 6;
  const buckets = repoGroups.map((group) => {
    const themed = group.themes
      .map((text) => ({ text, score: scoreTheme(text) }))
      .filter((item) => item.score >= 3)
      .sort((a, b) => b.score - a.score || a.text.localeCompare(b.text));
    return themed;
  });

  const selected = [];
  const seen = new Set();
  let round = 0;

  while (selected.length < limit) {
    let addedInRound = false;
    for (const bucket of buckets) {
      const item = bucket[round];
      if (!item || seen.has(item.text)) continue;
      selected.push(item.text);
      seen.add(item.text);
      addedInRound = true;
      if (selected.length >= limit) break;
    }
    if (!addedInRound) break;
    round += 1;
  }

  if (selected.length > 0) return selected;

  for (const group of repoGroups) {
    for (const text of group.themes) {
      if (seen.has(text)) continue;
      selected.push(text);
      seen.add(text);
      if (selected.length >= 4) return selected;
    }
  }

  return selected;
}

function buildOverview(repoGroups, activityThemes) {
  if (!activityThemes || activityThemes.length === 0) {
    return 'Pada hari ini saya melakukan peninjauan terhadap perubahan yang tersedia untuk menyusun rangkuman pekerjaan harian.';
  }

  const topNames = repoGroups.slice(0, 3).map((group) => group.displayName);
  const lowerThemes = activityThemes.join('\n').toLowerCase();
  const focusAreas = [];

  if (/gpt-5\.4|parameter token|openai|provider extension/.test(lowerThemes)) {
    focusAreas.push('integrasi dukungan model AI terbaru');
    focusAreas.push('penyesuaian request provider');
  }
  if (/generate report|pdf|base url backend publik|tautan unduhan/.test(lowerThemes)) {
    focusAreas.push('penyempurnaan fitur generate report dan akses file hasil generate');
  }
  if (/unit test|pengujian/.test(lowerThemes)) {
    focusAreas.push('penguatan pengujian untuk menjaga kompatibilitas implementasi');
  }

  const repoText = joinHumanList(topNames);
  const focusText = focusAreas.length > 0 ? `, terutama pada ${joinHumanList(focusAreas)}` : '';
  return `Pada hari ini saya berfokus pada pengembangan ${repoText}${focusText}.`;
}

function buildResultLines(activityThemes) {
  const results = [];
  const lower = activityThemes.join('\n').toLowerCase();

  if (/gpt-5\.4|max completion tokens|parameter token/.test(lower)) {
    results.push('Dukungan model GPT-5.4 berhasil diintegrasikan pada library dan konfigurasi agent yang digunakan.');
  }
  if (/dependency|versi dependency|orkestrasi/.test(lower)) {
    results.push('Konfigurasi dan dependency aplikasi berhasil diselaraskan untuk mendukung perubahan implementasi terbaru.');
  }
  if (/pdf|tautan unduhan|base url backend publik|generate report/.test(lower)) {
    results.push('Fitur generate report kini membentuk tautan unduhan yang lebih siap digunakan pada environment publik.');
  }
  if (/unit test|pengujian/.test(lower)) {
    results.push('Pengujian provider dan perubahan konfigurasi membantu menjaga kompatibilitas implementasi yang baru.');
  }
  if (/dokumentasi/.test(lower)) {
    results.push('Dokumentasi teknis pada repo yang dikerjakan ikut diperbarui agar perubahan lebih mudah ditelusuri.');
  }

  if (results.length === 0) {
    results.push('Perubahan pada repository yang dikerjakan berhasil dianalisis berdasarkan diff commit yang tersedia.');
    results.push('Implementasi hari ini membantu merapikan konfigurasi, logic, atau integrasi pada modul terkait.');
    results.push('Rangkuman aktivitas harian dapat disusun dengan lebih akurat karena berbasis file yang benar-benar berubah.');
  }

  return unique(results).slice(0, 3);
}

function extractJsonStringChanges(files, keyName) {
  const changes = [];
  const keyPattern = keyName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`^[+-]\\s*"${keyPattern}"\\s*:\\s*"([^"]+)"`, 'gm');

  for (const file of files) {
    const removed = [];
    const added = [];
    let match;
    while ((match = regex.exec(file.diff || '')) !== null) {
      const value = match[1];
      if (match[0].startsWith('-')) removed.push(value);
      if (match[0].startsWith('+')) added.push(value);
    }

    for (let index = 0; index < Math.min(removed.length, added.length); index += 1) {
      changes.push({
        file: file.path,
        key: keyName,
        from: removed[index],
        to: added[index],
      });
    }
  }

  return changes;
}

function extractPackageVersionChanges(files) {
  const changes = [];
  const packageRegex = /^[+-].*PackageReference Include="([^"]+)" Version="([^"]+)"/gm;
  const versionRegex = /^[+-]\s*<Version>([^<]+)<\/Version>/gm;

  for (const file of files) {
    const removedPackages = new Map();
    const addedPackages = new Map();
    let match;

    while ((match = packageRegex.exec(file.diff || '')) !== null) {
      const sign = match[0][0];
      const name = match[1];
      const version = match[2];
      if (sign === '-') removedPackages.set(name, version);
      if (sign === '+') addedPackages.set(name, version);
    }

    for (const [name, from] of removedPackages.entries()) {
      if (addedPackages.has(name) && addedPackages.get(name) !== from) {
        changes.push({ file: file.path, name, from, to: addedPackages.get(name) });
      }
    }

    const removedVersions = [];
    const addedVersions = [];
    while ((match = versionRegex.exec(file.diff || '')) !== null) {
      if (match[0].startsWith('-')) removedVersions.push(match[1]);
      if (match[0].startsWith('+')) addedVersions.push(match[1]);
    }
    if (removedVersions[0] && addedVersions[0] && removedVersions[0] !== addedVersions[0]) {
      changes.push({ file: file.path, name: path.basename(file.path), from: removedVersions[0], to: addedVersions[0] });
    }
  }

  return changes;
}

function loadRepoContextOverrides() {
  if (!fs.existsSync(REPO_CONTEXTS_PATH)) return { repos: [] };
  try {
    return JSON.parse(fs.readFileSync(REPO_CONTEXTS_PATH, 'utf8'));
  } catch (error) {
    return { repos: [] };
  }
}

function extractReadmeSummary(content) {
  const lines = content.split(/\r?\n/).map((line) => line.trim());
  const paragraphs = [];
  let current = [];

  for (const line of lines) {
    if (!line) {
      if (current.length > 0) {
        paragraphs.push(current.join(' '));
        current = [];
      }
      continue;
    }
    if (/^#/.test(line) || /^!\[/.test(line) || /^\[!\[/.test(line) || /^```/.test(line)) continue;
    current.push(line);
    if (current.join(' ').length > 240) break;
  }
  if (current.length > 0) paragraphs.push(current.join(' '));
  return (paragraphs[0] || '').replace(/\s+/g, ' ').trim();
}

function genericRepoSummary(repoName) {
  return `Repository ${repoName} yang sedang dikerjakan hari ini.`;
}

function scoreTheme(theme) {
  const lower = theme.toLowerCase();
  if (lower.includes('gpt-5.4') || lower.includes('base url backend publik') || lower.includes('parameter token')) return 10;
  if (lower.includes('dependency') || lower.includes('provider extension')) return 8;
  if (lower.includes('unit test') || lower.includes('service generate report')) return 7;
  if (lower.includes('konfigurasi')) return 5;
  if (lower.includes('dokumentasi')) return 3;
  if (lower.includes('gitignore') || lower.includes('repository')) return 1;
  return 4;
}

function countDiffLines(diff, prefix) {
  return (diff || '')
    .split(/\r?\n/)
    .filter((line) => line.startsWith(prefix) && !line.startsWith(prefix + prefix + prefix))
    .length;
}

function refName(ref) {
  return String(ref || '').replace(/^refs\/heads\//, '').trim();
}

function isZeroSha(value) {
  return /^0+$/.test(String(value || '').trim());
}

function basenameRepo(value) {
  return String(value || '').split('/').filter(Boolean).pop() || String(value || '');
}

function firstLine(value) {
  return String(value || '').split(/\r?\n/)[0].trim();
}

function capitalize(value) {
  if (!value) return value;
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function ensureSentence(value) {
  const trimmed = String(value || '').trim();
  if (!trimmed) return trimmed;
  return /[.!?]$/.test(trimmed) ? trimmed : `${trimmed}.`;
}

function joinHumanList(values) {
  const items = unique(values);
  if (items.length === 0) return '';
  if (items.length === 1) return items[0];
  if (items.length === 2) return `${items[0]} dan ${items[1]}`;
  return `${items.slice(0, -1).join(', ')}, dan ${items[items.length - 1]}`;
}

function unique(values) {
  return Array.from(new Set(values.filter(Boolean)));
}

function normalizeKey(value) {
  return String(value || '').trim().toLowerCase();
}

function getWibDateKey(value) {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: WIB_TZ,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date(value));
  const map = Object.fromEntries(parts.filter((part) => part.type !== 'literal').map((part) => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day}`;
}

function formatIndonesianDate(dateKey) {
  const [year, month, day] = String(dateKey).split('-');
  const monthNames = [
    'Januari',
    'Februari',
    'Maret',
    'April',
    'Mei',
    'Juni',
    'Juli',
    'Agustus',
    'September',
    'Oktober',
    'November',
    'Desember',
  ];
  return `${day} ${monthNames[Number(month) - 1]} ${year}`;
}

module.exports = {
  WORKSPACE,
  DAILY_DIR,
  REPORTS_DIR,
  REPO_CONTEXTS_PATH,
  GITHUB_USER,
  WIB_TZ,
  TARGET_DATE,
  REPORT_SCOPE,
  collectArtifacts,
  collectGitHubArtifacts,
  collectGitLabArtifacts,
  buildRepoGroups,
  analyzeArtifactThemes,
  renderReport,
  renderLogbookOnly,
  selectActivityThemes,
  buildOverview,
  buildResultLines,
  loadRepoContextOverrides,
  scoreTheme,
  unique,
  joinHumanList,
  ensureSentence,
  capitalize,
  getWibDateKey,
  formatIndonesianDate,
  firstLine,
  normalizeKey,
};
