// Read-only source clues. Dynamic configuration and delegated helpers need review.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';

export function assertNsisEnglish(file, text) {
  let options;
  if (/\.json$/.test(file)) {
    const data = JSON.parse(text);
    const config = file.endsWith('package.json') ? data.build : data;
    options = config?.nsis;
  } else {
    // Use the application's parser, including electron-builder's nested dependency.
    // The Skill itself remains dependency-free; never approximate YAML with regexes.
    const require = createRequire(path.resolve(file));
    let yaml;
    try { yaml = require('js-yaml'); }
    catch {
      try {
        const builder = createRequire(require.resolve('electron-builder'));
        yaml = createRequire(builder.resolve('app-builder-lib'))('js-yaml');
      } catch {
        throw new Error('YAML parser unavailable: install the application dependencies or pass its effective builder JSON');
      }
    }
    // js-yaml 5 uses Core by default; retain the merge keys supported by builder
    // configurations under v4 without enabling YAML 1.1 boolean coercion.
    const schema = yaml.CORE_SCHEMA?.withTags && yaml.mergeTag
      ? yaml.CORE_SCHEMA.withTags([yaml.mergeTag]) : yaml.DEFAULT_SCHEMA;
    options = yaml.load(text, {schema})?.nsis;
  }
  if (JSON.stringify(options?.installerLanguages) !== '["en_US"]' || options?.displayLanguageSelector !== false)
    throw new Error('NSIS requires installerLanguages: [en_US] and displayLanguageSelector: false in the effective builder config');
}
export function deliveryFindings(files) {
  const findings = [];
  for (const {file, text} of files) {
    if (/(^|\/)(?:tests?|fixtures|node_modules)\//i.test(file)) continue;
    const add = (id, match, detail, fix) => findings.push({id, file,
      line: match ? text.slice(0, match.index).split('\n').length : null,
      severity: 'P1', confidence: 'heuristic', detail, fix});
    if (/\.cs$/.test(file)) {
      const code = text.replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g, comment => comment.replace(/[^\n]/g, ' '));
      const match = /Path\.Combine\(\s*(?:UpdatesRoot|updatesRoot|updateCacheRoot)\s*,\s*(?:version|tag)\s*\)/.exec(code);
      if (match) add('update-cache-architecture', match,
        '更新缓存仅按版本命名，新增 ARM64 后可能复用旧 x64 完成目录。',
        '按 ProcessArchitecture 选包，缓存键包含架构与版本；旧版无架构缓存不作为新架构的完成缓存。使用 wpf-desktop 的 UpdatePackage.cs 并补跨架构回归。');
    }
    if (/(?:release|publish)[^/]*\.[cm]?js$/i.test(file)) {
      const match = /Object\.keys\(manifests\)/.exec(text);
      if (match && /verifyAssets/.test(text)) add('release-manifest-inventory', match,
        '发布校验从实际读到的 manifests 枚举清单，整份平台清单缺失时可能完全跳过检查。',
        '从配置的必需清单/平台集合枚举，分别断言文件存在、版本、载体和摘要；增加整份清单缺失回归。');
      const skipped = /\.filter\([^\n]*\.digest\s*&&/.exec(text);
      if (skipped) add('release-digest-skipped', skipped,
        '生成摘要时过滤无 digest 的资产，可能生成不完整但成功的校验和。',
        '所有分发文件缺有效 SHA256 时失败；SHA256SUMS 自身排除，重跑仍覆盖同一份完整资产集合。');
    }
    if (/(?:release|publish)[^/]*\.ps1$/i.test(file)) {
      const match = /Get-ChildItem[^\n]*(?:\$artifacts|artifacts)[^\n]*['"]\*\.zip['"]/i.exec(text);
      if (match && /Get-FileHash/.test(text)) add('release-checksum-inventory', match,
        '发布摘要按 artifacts 下所有 ZIP 枚举，可能纳入旧版本或无关压缩包。', '从本次生成的明确资产列表计算摘要，核对文件集合与 CI 上传列表一致。');
      const archive = /Compress-Archive[^\n]*-Path[^\n]*\*/i.exec(text);
      if (archive) add('archive-incomplete-directory', archive, '本地发布脚本通过通配符压缩目录，隐藏文件可能遗漏。', '完整目录用 tar 打包；本地和 CI 调用同一脚本，并对解包内容运行 smoke。');
    }
    if (/\.iss$/i.test(file)) {
      const code = text.replace(/^\s*;.*$/gm, '');
      const languages = /^\[Languages\]\s*\n([\s\S]*?)(?=^\[|$(?![\s\S]))/mi.exec(code)?.[1] ?? '';
      const entries = languages.split(/\r?\n/).filter(line => /^\s*Name:/i.test(line));
      if (entries.length !== 1 || !/MessagesFile:\s*"compiler:Default\.isl"/i.test(entries[0] ?? '') || !/^ShowLanguageDialog\s*=\s*no\s*$/mi.test(code))
        add('installer-ui-language', null, 'Inno 安装/卸载语言未显式固定为单一英文。',
          '仅保留 compiler:Default.isl 并设置 ShowLanguageDialog=no；自定义消息和实际两个向导仍需检查。');
    }
    if (/(^|\/)package\.json$/.test(file) || /electron-builder\.(?:json|json5|ya?ml)$/.test(file)) {
      let config;
      try { const data = JSON.parse(text); config = file.endsWith('package.json') ? data.build : data; } catch { /* YAML is checked as a source clue below. */ }
      const targets = config?.win?.target;
      const usesNsis = config?.nsis || (config?.win && (!targets || (Array.isArray(targets) ? targets : [targets]).some(target => /^(?:nsis|nsis-web)$/.test(typeof target === 'string' ? target : target?.target))));
      if (config && usesNsis) {
        if (JSON.stringify(config.nsis?.installerLanguages) !== '["en_US"]' || config.nsis?.displayLanguageSelector !== false)
          add('installer-ui-language', null, 'Electron NSIS 安装/卸载语言未固定英文。', '配置 nsis.installerLanguages: [en_US] 和 displayLanguageSelector: false，并在 tag 校验中运行配置检查。');
      } else if (/electron-builder\.ya?ml$/.test(file) && /^\s*(?:nsis|win):/m.test(text)) {
        // Static audits never load application dependencies or guess YAML semantics.
        findings.push({id: 'installer-config-unverified', file, line: null, severity: 'notice', confidence: 'unknown',
          detail: 'NSIS YAML 需在应用构建环境中解析并核对覆盖配置；静态扫描不判定安装语言错误。',
          fix: '在应用依赖安装后运行 delivery-checks.mjs --installer <配置路径>，动态配置需提供实际生效的 builder JSON。'});
      }
    }
  }
  return findings;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    if (process.argv[2] !== '--installer' || !process.argv[3]) throw new Error('Usage: delivery-checks.mjs --installer <effective-builder.json|electron-builder.yml|package.json>');
    assertNsisEnglish(process.argv[3], fs.readFileSync(process.argv[3], 'utf8'));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
