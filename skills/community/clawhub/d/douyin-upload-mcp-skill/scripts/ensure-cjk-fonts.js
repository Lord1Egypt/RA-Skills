#!/usr/bin/env node
import { copyFileSync, existsSync, lstatSync, mkdirSync, readFileSync, readlinkSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { homedir, platform } from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const home = homedir();
const isLinux = platform() === 'linux';
const windowsFontDirs = [
  '/mnt/c/Windows/Fonts',
  '/mnt/c/WINDOWS/Fonts',
];
const systemFontDirs = [
  ...windowsFontDirs,
  '/usr/share/fonts',
  '/usr/local/share/fonts',
  '/Library/Fonts',
  '/System/Library/Fonts',
];
const bundledFontDir = join(root, 'fonts');
const targetDir = join(home, '.local', 'share', 'fonts', 'douyin-skill');
const fontconfigDir = join(home, '.config', 'fontconfig', 'conf.d');
const fontconfigFile = join(fontconfigDir, '99-douyin-cjk.conf');
const candidates = [
  'NotoSansSC-Regular.otf',
  'NotoSansSC-VF.ttf',
  'NotoSerifSC-VF.ttf',
  'msyh.ttc',
  'msyhbd.ttc',
  'msyhl.ttc',
  'simhei.ttf',
  'simkai.ttf',
  'simsun.ttc',
  'simsunb.ttf',
  'SimsunExtG.ttf',
];

function runFcMatch(pattern) {
  const res = spawnSync('fc-match', ['-f', '%{family}\\n', pattern], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  return `${res.stdout || ''}${res.stderr || ''}`.trim();
}

function ensureLinkedFile(src, dest) {
  if (existsSync(dest)) {
    try {
      const current = lstatSync(dest);
      if (current.isSymbolicLink()) {
        const linked = readlinkSync(dest);
        if (linked === src && existsSync(dest)) return 'exists';
      } else if (current.isFile()) {
        return 'exists';
      }
      rmSync(dest, { force: true, recursive: false });
    } catch {
      rmSync(dest, { force: true, recursive: false });
    }
  } else {
    try {
      if (lstatSync(dest).isSymbolicLink()) rmSync(dest, { force: true, recursive: false });
    } catch {
      // Path is absent, which is the normal creation path.
    }
  }

  try {
    symlinkSync(src, dest);
    return 'linked';
  } catch {
    copyFileSync(src, dest);
    return 'copied';
  }
}

function findSourceFiles() {
  const sources = [];
  for (const name of candidates) {
    const local = join(bundledFontDir, name);
    if (existsSync(local)) {
      sources.push({ name, path: local, source: 'skill-fonts' });
      continue;
    }
    for (const dir of systemFontDirs) {
      const path = join(dir, name);
      if (existsSync(path)) {
        sources.push({ name, path, source: dir });
        break;
      }
    }
  }
  return sources;
}

function ensureFontconfigAlias() {
  mkdirSync(fontconfigDir, { recursive: true });
  const desired = `<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer>
      <family>Noto Sans SC</family>
      <family>Microsoft YaHei</family>
      <family>SimSun</family>
      <family>DejaVu Sans</family>
    </prefer>
  </alias>
  <alias>
    <family>serif</family>
    <prefer>
      <family>Noto Serif SC</family>
      <family>SimSun</family>
      <family>DejaVu Serif</family>
    </prefer>
  </alias>
  <alias>
    <family>monospace</family>
    <prefer>
      <family>Noto Sans SC</family>
      <family>Microsoft YaHei</family>
      <family>DejaVu Sans Mono</family>
    </prefer>
  </alias>
</fontconfig>
`;
  const current = existsSync(fontconfigFile) ? readFileSync(fontconfigFile, 'utf8') : '';
  if (current !== desired) {
    writeFileSync(fontconfigFile, desired);
    return true;
  }
  return false;
}

function main() {
  const sources = findSourceFiles();
  mkdirSync(targetDir, { recursive: true });

  const installed = [];
  for (const item of sources) {
    const dest = join(targetDir, item.name);
    const action = ensureLinkedFile(item.path, dest);
    installed.push({ name: item.name, action, source: item.source });
  }

  const wroteFontconfig = ensureFontconfigAlias();
  const fcCache = isLinux
    ? spawnSync('fc-cache', ['-f'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
    : { status: 0 };

  const matches = {
    sansSerifZhCn: runFcMatch('sans-serif:lang=zh-cn'),
    notoSansSc: runFcMatch('Noto Sans SC'),
    microsoftYahei: runFcMatch('Microsoft YaHei'),
    simsun: runFcMatch('SimSun'),
  };

  const ok = Boolean(sources.length) && Object.values(matches).some((value) => /Noto Sans SC|Microsoft YaHei|SimSun/i.test(value));
  console.log(JSON.stringify({
    ok,
    bundledFontDir,
    targetDir,
    fontconfigFile,
    wroteFontconfig,
    installed,
    matches,
    fcCacheStatus: fcCache.status ?? 0,
  }, null, 2));

  if (!ok) process.exitCode = 1;
}

main();
