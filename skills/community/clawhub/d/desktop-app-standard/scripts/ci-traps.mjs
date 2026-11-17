// Release-path traps: patterns where the build stays green and delivery still fails.
// Line-oriented heuristics over comment-stripped workflow text. NOT a YAML parser:
// every finding is confidence "heuristic" and must be confirmed by reading the job.

/** Strip YAML comments but keep line numbers, so prose like "# gh release create collides" is not a step. */
export function stripComments(text) {
  return text.split(/\r?\n/).map(line => {
    let q = null;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (q) { if (c === q) q = null; continue; }
      if (c === '"' || c === "'") q = c;
      else if (c === '#' && (i === 0 || /\s/.test(line[i - 1]))) return line.slice(0, i);
    }
    return line;
  }).join('\n');
}
const lineOf = (text, index) => (index == null ? null : text.slice(0, index).split('\n').length);
const find = (re, text) => { const m = re.exec(text); return m ? { index: m.index, match: m } : null; };

/** Text of the job (2-space-indented key under jobs:) containing index. */
const jobBlock = (text, index) => { const head = text.slice(0, index); const starts = [...head.matchAll(/^  [\w-]+:\s*$/gm)]; const s0 = starts.length ? starts[starts.length - 1].index : 0; const rest = text.slice(index); const nx = /\n  [\w-]+:\s*$/m.exec(rest); return text.slice(s0, nx ? index + nx.index : text.length); };

/**
 * Split a workflow into its job blocks, keeping each block's offset in the
 * original text (the traps report a line number in the whole file).
 * Jobs are the keys under `jobs:`; the `on:` block also has 2-space keys, so
 * the scan starts after `jobs:`.
 */
export function jobBlocks(t) {
  const jobsAt = t.search(/^jobs:[ \t]*$/m);
  if (jobsAt < 0) return [];
  const re = /^ {2}([A-Za-z_][\w-]*):[ \t]*$/gm;
  re.lastIndex = jobsAt;
  const heads = [];
  let m;
  while ((m = re.exec(t))) heads.push({ name: m[1], start: m.index });
  const out = [];
  for (let i = 0; i < heads.length; i++) {
    const end = i + 1 < heads.length ? heads[i + 1].start : t.length;
    out.push({ name: heads[i].name, text: t.slice(heads[i].start, end), offset: heads[i].start });
  }
  return out;
}

const RELEASE_CREATORS = /tauri-apps\/tauri-action|action-gh-release|ncipollo\/release-action|gh release (create|upload)|--publish\s+(always|onTag)/;
const BUILDS = /tauri-apps\/tauri-action|electron-builder|tauri build|electron-forge|\bmake\b|--(win|mac|linux)\b/;
const isReleaseWorkflow = t => RELEASE_CREATORS.test(t) || /^\s*tags:/m.test(t);

function publishesRelease(text) {
  if (/action-gh-release|ncipollo\/release-action|gh release (create|upload)|--publish\s+(always|onTag)/.test(text)) return true;
  return /tauri-apps\/tauri-action/.test(text) && /(?:tagName|releaseId):\s*\S/.test(text);
}

// Static evidence only. A delegated workflow needs inspection in its own repository.
export function workflowCoverage(files) {
  const workflows = files.map(({file, text}) => ({file, text: stripComments(text)}));
  return {
    pullRequest: workflows.filter(w => /\bpull_request\b/.test(w.text.split(/^jobs:/m)[0])).map(w => w.file),
    release: workflows.filter(w => jobBlocks(w.text).some(job => publishesRelease(job.text))).map(w => w.file),
    delegated: workflows.filter(w => /^\s+uses:\s*(?:\.\/\.github\/workflows\/|[^\s]+\/\.github\/workflows\/)/m.test(w.text) ||
      jobBlocks(w.text).some(job => /\bnode\s+[^\n]*(?:release|publish)[^\s]*\.m?js\b/.test(job.text) &&
        /contents:\s*write|GH_TOKEN:|GITHUB_TOKEN:/.test(job.text))).map(w => w.file),
    manual: workflows.filter(w => /^\s*DESKTOP_RELEASE_MODE:\s*['"]?manual['"]?\s*$/m.test(w.text)).map(w => w.file),
  };
}

function missingReleasePermission(t) {
  const header = t.split(/^jobs:/m)[0];
  for (const job of jobBlocks(t)) {
    const creator = find(RELEASE_CREATORS, job.text);
    if (!creator || !publishesRelease(job.text)) continue;
    // An explicit token may have permissions independent of GITHUB_TOKEN.
    if (/(?:token:|GH_TOKEN:|GITHUB_TOKEN:)[^\n]*(?:secrets\.(?!GITHUB_TOKEN\b)|inputs\.)/.test(job.text)) continue;
    const own = /^    permissions:[^\n]*(?:\n {6}[^\n]*)*/m.exec(job.text)?.[0];
    const effective = own ?? header;
    if (/['"]?contents['"]?\s*:\s*['"]?write\b|permissions:\s*['"]?write-all\b/.test(effective)) continue;
    return {index: job.offset + creator.index,
      detail: `发布 job ${job.name} 未声明有效的 contents: write；其他 job 的权限不会继承到这里。`,
      fix: '核对该 job 的有效 permissions 和 token 来源，仅向需要上传或公开的 job 授予 contents: write。'};
  }
  return null;
}

export const TRAPS = [
  // ---------- P0: delivery silently broken ----------
  { id: 'rust-cache-workspace', severity: 'P0', applies: c => c.isTauri,
    test: t => { const m = find(/workspaces:\s*['"]?(\S+?)\s*->\s*(\S+?)['"]?\s*$/m, t); if (!m || m.match[2] === 'target') return null;
      return { index: m.index, detail: `rust-cache 的 \`${m.match[1]} -> ${m.match[2]}\` 缓存了整个源码树而不只是 target；恢复时会用旧快照覆盖新 checkout。`, fix: '改为 `./src-tauri -> target`（按实际 Cargo 工作区）。' }; } },
  { id: 'artifact-action-retired', severity: 'P0', applies: () => true,
    test: t => { const m = find(/actions\/(upload|download)-artifact@v[1-3]\b/, t); if (!m) return null;
      return { index: m.index, detail: `\`${m.match[0]}\` 已退役，job 会以配置错误立即失败，看起来像工作流 bug。`, fix: '升级到当前 major 并核验 v4+ 的同名产物不可覆盖语义。' }; } },
  { id: 'draft-never-published', severity: 'P0', applies: () => true,
    test: t => { const m = find(/releaseDraft:\s*true|gh release create[^\n]*--draft|draft:\s*true/, t); if (!m) return null;
      if (/^[ \t]*DESKTOP_RELEASE_MODE:[ \t]*['"]?manual['"]?[ \t]*$/m.test(t)) return null;
      if (/draft=false|^\s*(?:draft|releaseDraft):\s*false\b/m.test(t)) return null;
      return { index: m.index, detail: 'release 以草稿创建，但本工作流中没有公开步骤，updater 无法通过 releases/latest 读取草稿。', fix: '默认直接使用 draft: false / releaseDraft: false；明确采用草稿的项目补上自动公开步骤，或记录人工发布约定。' }; } },
  { id: 'release-permissions', severity: 'P0', applies: () => true,
    test: missingReleasePermission },
  { id: 'tagname-from-ref-unasserted', severity: 'P0', applies: () => true,
    // The assertion must be in the job that reads tagName: a ref_type check in an
    // unrelated publish job says nothing about what this job packed.
    test: (t, c) => { const m = find(/tagName:\s*[^\n]*github\.ref_name/, t); if (!m || c.versionAsserted(jobBlock(t, m.index))) return null;
      return { index: m.index, detail: '`tagName` 取自 `github.ref_name`，而安装包文件名和内嵌版本来自配置；两者不一致时，名为 v3.0.1 的 release 可能装着 3.0.0。`workflow_dispatch` 时 ref_name 还是分支名。', fix: '构建前把 tag 注入版本或断言 tag == manifest 版本，并限定 `github.ref_type == tag`。' }; } },
  { id: 'cache-lockfile-mismatch', severity: 'P0', applies: () => true,
    test: (t, c) => { const m = find(/cache:\s*['"]?(yarn|npm|pnpm)\b/, t); if (!m) return null; const pm = m.match[1];
      if (c.lockfiles[pm]) return null;
      return { index: m.index, detail: `setup-node 配置了 \`cache: ${pm}\`，仓库中却没有对应锁文件；job 会因缺少 cache-dependency-path 失败。`, fix: `改为实际包管理器（项目为 ${c.packageManager ?? '未知'}），或提交对应锁文件。` }; } },
  { id: 'npm-ci-without-lockfile', severity: 'P0', applies: c => !c.lockfiles.npm && Object.keys(c.lockfiles).length > 0,
    test: (t, c) => { const m = find(/(?:^|[\s;&|])npm\s+(?:ci|clean-install|install-clean|ic)\b/m, t); if (!m) return null;
      return { index: m.index, detail: `工作流用 \`npm ci\`，但仓库只有 ${Object.keys(c.lockfiles).join('/')} 锁文件、没有 package-lock.json；\`npm ci\` 没有锁文件会立即失败（从 npm 模板复制到 Yarn/pnpm 仓库时常见）。`, fix: '按仓库实际包管理器安装（Yarn 1 `yarn install --frozen-lockfile`、Yarn 4 `corepack enable` + `yarn install --immutable`、pnpm `pnpm install --frozen-lockfile`），`cache:` 同步改；或真的迁到 npm 并提交 package-lock.json。' }; } },
  { id: 'tauri-updater-manifest', severity: 'P0', applies: c => c.usesTauriUpdater,
    test: (t, c) => { const m = find(/tauri-apps\/tauri-action|gh release (create|upload)|action-gh-release/, t); if (!m) return null;
      if (/tauri-apps\/tauri-action/.test(t)) { if (c.tauriCreateUpdaterArtifacts !== false && !/uploadUpdaterJson:\s*false/.test(t)) return null;
        return { index: m.index, detail: '应用启用了 Tauri updater，但 `bundle.createUpdaterArtifacts` 未开启或 `uploadUpdaterJson:false`，release 中不会有 `latest.json`/`.sig`；更新端点 404，应用永远“没有新版本”。', fix: '开启 createUpdaterArtifacts，配置 TAURI_SIGNING_PRIVATE_KEY(_PASSWORD)，并在 publish 前校验 latest.json 含全部平台。' }; }
      if (/latest\.json/.test(t)) return null;
      return { index: m.index, detail: '手工创建 release，但没有上传 `latest.json`。', fix: '上传合并后的 latest.json 与各平台 .sig。' }; } },
  { id: 'electron-updater-manifest', severity: 'P0', applies: c => c.hasElectronUpdater,
    test: t => { if (!/electron-builder/.test(t)) return null; const m = find(/action-gh-release|gh release (create|upload)|ncipollo\/release-action/, t); if (!m) return null;
      if (/latest[\w-]*\.yml|\*\.yml|\*\.ya?ml/.test(t)) return null;
      return { index: m.index, detail: '应用使用 electron-updater，但另行上传的资产中看不到 `latest.yml` / `latest-mac.yml` / `latest-linux*.yml`。updater 依赖这些清单定位新版本。', fix: '上传每个平台的 latest*.yml、对应安装包/zip 与 .blockmap；发布前逐一校验 files[].url 存在。' }; } },
  { id: 'electron-updater-windows-target', severity: 'P0', applies: c => c.hasElectronUpdater,
    test: t => { const m = find(/--win\s+(portable|dir|zip)\b/i, t); if (!m || /\bnsis\b/i.test(t)) return null;
      return { index: m.index, detail: 'electron-updater 在 Windows 只支持 NSIS 安装版；portable/dir/zip 没有可替换的安装，Windows 用户永远收不到更新。', fix: '以 NSIS 为正式 Windows 产物，便携 zip 仅作“免安装试用”。' }; } },
  { id: 'tauri-linux-deps', severity: 'P0', applies: c => c.isTauri,
    // Only flag a Ubuntu job that actually builds Tauri. A security/audit job on
    // ubuntu-latest must not turn into a false P0 just because the workflow also
    // builds a Windows installer somewhere else.
    test: t => {
      const runner = /\bruns-on:\s*ubuntu-(?:latest|\d[\w.-]*)/g;
      let m;
      while ((m = runner.exec(t))) {
        const block = jobBlock(t, m.index);
        const buildsTauri = /tauri-apps\/tauri-action|(?:npm run |npx |yarn |cargo )?tauri build|cargo tauri build/i.test(block);
        if (buildsTauri && !/libwebkit2gtk-4\.1-dev/.test(block)) {
          return { index: m.index, detail: 'Ubuntu runner 构建 Tauri，但没有安装 `libwebkit2gtk-4.1-dev` 等系统依赖；Linux 构建会失败。', fix: '按当前 Tauri 官方 pipeline 安装 libwebkit2gtk-4.1-dev、build-essential、curl、wget、file、libxdo-dev、libssl-dev、libayatana-appindicator3-dev、librsvg2-dev、patchelf 等。' };
        }
      }
      return null;
    } },
  // ---------- P1: will bite, or breaks a platform/user group ----------
  { id: 'electron-runtime-download', severity: 'P1', applies: c => (c.electronMajor ?? 0) >= 42,
    test: (t, c) => { const inst = find(/npm ci|npm install|yarn install|yarn\s*$|pnpm install|bun install/m, t); const pack = find(/electron-builder|electron-forge|npx electron|(?:yarn|pnpm|bun)(?: run)? (?:dist|package|make|electron:build)\b|npm run (?:dist|package|make|electron:build)\b/, t);
      const directInstall = /\bnode\s+["']?(?:\.[\\/])?node_modules[\\/]electron[\\/]install\.js(?:["']|\s|$)/m.test(t);
      if (!inst || !pack || directInstall || /install-electron|install-app-deps|electron-rebuild|@electron\/rebuild/.test(t)) return null;
      return { index: pack.index, detail: 'Electron 42 起不再在 postinstall 下载二进制，`ELECTRON_SKIP_BINARY_DOWNLOAD` 已移除。**打包本身不受影响**：electron-builder 会自己下载 Electron 发行包（app-builder-lib 的 downloadElectronArtifactZip），node_modules/electron/index.js 在首次被 require 时也会按需自下载。真正变的是**下载时机**——从「npm ci 时」挪到「第一次用到时」：离线/气隙 runner 会在那一刻才失败，e2e 里启动 Electron 会在测试步骤里触发下载，自定义 electronDist 指向 node_modules/electron/dist 也会拿不到东西。', fix: `安装依赖后显式运行 \`${c.yarnFlavor ? 'yarn run install-electron' : c.lockfiles.pnpm ? 'pnpm exec install-electron' : 'node node_modules/electron/install.js'}\`（npm 直接调用已安装包的脚本；Yarn/pnpm 可用本地 bin，不要 \`npm run\`），把下载固定在安装步骤里；e2e 等会启动 Electron 的步骤同理。` }; } },
  { id: 'electron-builder-empty-csc-link', severity: 'P1', applies: c => c.hasElectron,
    test: t => { const m = /^[ \t]*(?:CSC_LINK|WIN_CSC_LINK)[ \t]*:[ \t]*(.+)$/m.exec(t);
      if (!m || !/secrets\./.test(m[1])) return null;   // a literal path is fine
      return { index: m.index, detail: 'CSC_LINK 直接取自 secrets：GitHub 把「没有这个 secret」渲染成**空字符串**（不是不设置），而 electron-builder 把空的 CSC_LINK 理解成「证书就是这个路径」，于是拿工作目录当证书去签，构建直接失败——macOS 上表现为 `⨯ <工作目录> not a file`。Windows 与 Linux 不受影响，只有 macOS 这条腿会红，看起来像平台问题，其实凭据为空。', fix: '用别的名字收下 secret，只在真的有值时再导出成 electron-builder 认的名字（`if [ -n "$MAC_CSC_LINK" ]; then export CSC_LINK="$MAC_CSC_LINK"; export CSC_KEY_PASSWORD=...; fi`）。没有凭据 = 明确的不签名，而不是一个空字符串。' }; } },
  { id: 'bash-script-on-windows-runner', severity: 'P1', applies: () => true,
    test: t => {
      // Scoped to the jobs that can actually land on a Windows runner: a
      // workflow whose bash script only runs in a Linux-only job is fine, and
      // reporting it there would be a false positive.
      for (const job of jobBlocks(t)) {
        if (!/windows-(?:latest|\d+)/i.test(job.text)) continue;
        if (/^[ \t]*shell:[ \t]*bash\b/m.test(job.text)) continue;
        // A multi-line run: block written in bash will be handed to PowerShell on
        // the Windows runner → ParserError, while macOS/Linux build fine.
        const re = /run:[ \t]*\|[ \t]*\n((?:[ \t]+[^\n]*\n)+)/g;
        let m;
        while ((m = re.exec(job.text))) {
          if (!/(set -euo|\[\[|\[\s+-n\s|export\s+[A-Za-z_]+=)/.test(m[1])) continue;
          return { index: job.offset + m.index, detail: '能跑到 Windows runner 的 job 里有**多行 bash 脚本**（`set -euo`、`export`、`[[`、`[ -n`）而没有声明 `shell: bash`。Windows runner 的默认 shell 是 PowerShell，那条腿会直接报 ParserError，而 macOS/Linux 照常通过——看着像平台问题，其实是 shell 不对。', fix: '给用到 bash 的步骤显式加 `shell: bash`（GitHub 的 Windows runner 自带 Git Bash）；或把脚本改写成两边都能跑的写法。' };
        }
      }
      return null;
    } },
  { id: 'npm-install-not-ci', severity: 'P1', applies: c => !!c.lockfiles.npm,
    test: t => { let offset = 0;
      for (const line of t.split('\n')) {
        const here = offset; offset += line.length + 1;
        if (/^\s*(-\s*)?[\w-]+:\s/.test(line) && !/^\s*(-\s*)?run:/.test(line)) continue;
        // Bare `npm install` / `npm i` (flags only): resolves and may rewrite package-lock.json. `npm i -g tool` / `npm i pkg` are not this trap.
        const m = /(?:^|[\s;&|])npm\s+(?:install|i|add)((?:\s+--?[\w-]+(?:=\S+)?)*)\s*(?:$|&&|;|\|)/.exec(line); if (!m) continue;
        if (/\s(-g|--global)\b/.test(m[1])) continue;
        return { index: here + m.index, detail: 'CI 用 `npm install` 而不是 `npm ci`：会按声明范围重新解析并可能改写 package-lock.json，构建出的依赖可能与锁文件不同。', fix: '改为 `npm ci`（严格按 package-lock.json 安装，锁文件与 package.json 不一致时直接失败）。' };
      }
      return null; } },
  { id: 'yarn-install-not-frozen', severity: 'P1', applies: c => !!c.lockfiles.yarn,
    test: (t, c) => { let offset = 0;
      for (const line of t.split('\n')) {
        const here = offset; offset += line.length + 1;
        if (/^\s*(-\s*)?[\w-]+:\s/.test(line) && !/^\s*(-\s*)?run:/.test(line)) continue;
        const m = /(?:^|[\s;&|])yarn(\s+install)?((?:\s+--?[\w-]+(?:=\S+)?)*)\s*$/.exec(line); if (!m) continue;
        const flags = m[2] ?? '', index = here + m.index;
        if (c.yarnFlavor === 'classic' && /--immutable/.test(flags)) return { index, detail: 'yarn classic 不识别 `--immutable`。', fix: '改用 `yarn install --frozen-lockfile`。' };
        if (c.yarnFlavor === 'berry' && /--frozen-lockfile/.test(flags)) return { index, detail: 'yarn berry 中 `--frozen-lockfile` 是弃用别名。', fix: '改用 `yarn install --immutable`。' };
        if (/--frozen-lockfile|--immutable/.test(flags)) continue;
        return { index, detail: 'CI 中 `yarn install` 未冻结锁文件，构建可能解析出与本地不同的依赖版本。', fix: c.yarnFlavor === 'berry' ? '使用 `yarn install --immutable`。' : '使用 `yarn install --frozen-lockfile`。' };
      }
      return null; } },
  { id: 'yarn-berry-corepack', severity: 'P1', applies: c => c.yarnFlavor === 'berry',
    test: t => { const m = find(/\byarn\b/, t); if (!m || /corepack enable|corepack prepare|setup-yarn|packageManager/.test(t)) return null;
      return { index: m.index, detail: '项目使用 yarn berry，但工作流没有 `corepack enable`；runner 自带的全局 yarn 可能是 classic，`cache: yarn` 与安装行为都会错位。', fix: '在 setup-node 缓存/安装之前执行 `corepack enable`，并在 package.json 声明 `packageManager`。' }; } },
  { id: 'tauri-macos-rust-targets', severity: 'P1', applies: c => c.isTauri,
    test: t => { const m = find(/--target\s+(x86_64|universal)-apple-darwin/, t); if (!m || /targets:[^\n]*(apple-darwin|\$\{\{\s*matrix\.)|rustup target add[^\n]*(apple-darwin|\$\{\{\s*matrix\.)/.test(t)) return null;
      return { index: m.index, detail: '为 macOS 指定了 Rust target，但没有安装对应 target；交叉架构构建会失败。', fix: 'rust-toolchain 步骤加入 `targets: aarch64-apple-darwin,x86_64-apple-darwin`（仅 macOS runner）。' }; } },
  { id: 'electron-mac-multiarch-split', severity: 'P1', applies: c => c.hasElectronUpdater,
    test: t => { const arches = t.match(/--mac[^\n]*--(x64|arm64)\b/g) ?? []; if (arches.length < 2 || /--mac[^\n]*--x64[^\n]*--arm64|--mac[^\n]*--arm64[^\n]*--x64|--universal/.test(t)) return null;
      const m = find(/--mac/, t); return { index: m.index, detail: 'macOS x64 与 arm64 在不同 job 分别打包，会各自生成同名 `latest-mac.yml` 并互相覆盖，一种架构的用户收不到正确更新。', fix: '同一 job 中 `--mac --x64 --arm64`（或 universal），生成包含双架构的单一清单。' }; } },
  { id: 'macos-not-notarized', severity: 'P1', applies: () => true,
    test: t => { const m = find(/\bmacos-(latest|\d[\w.-]*)|--mac\b|apple-darwin/i, t); if (!m || !isReleaseWorkflow(t) || !BUILDS.test(t)) return null;
      if (/notarytool|notariz|APPLE_ID|APPLE_API_KEY|APPLE_CERTIFICATE|APPLE_SIGNING_IDENTITY|signingIdentity|CSC_LINK/i.test(t)) return null;
      return { index: m.index, detail: '发布 macOS 产物但没有签名/公证配置。站外下载的未公证 App 会被 Gatekeeper 拦截（用户需手动“仍要打开”）；Electron 在 macOS 的自动更新要求应用已签名。', fix: '首选 Developer ID 签名 + 公证；暂时没有 Apple 凭据时，Tauri 配置 ad-hoc 签名并在 release 说明写明打开方式，Electron 关闭 macOS 自动更新或标注为手动更新。' }; } },
  { id: 'windows-unsigned', severity: 'P1', applies: () => true,
    test: t => { const m = find(/\bwindows-(latest|\d[\w.-]*)|--win\b/, t); if (!m || !isReleaseWorkflow(t) || !BUILDS.test(t)) return null;
      if (/signtool|azureSignOptions|AZURE_CLIENT_ID|trusted.?signing|artifact.?signing|signCommand|WIN_CSC_LINK|CSC_LINK|certificateThumbprint/i.test(t)) return null;
      return { index: m.index, detail: '公开分发的 Windows 产物未签名：首次运行显示“未知发布者”，SmartScreen 告警；winget 渠道不会消除该告警。', fix: '按 house style，公开分发后默认签名（优先 Azure Artifact Signing）；未签名期间在 release 说明中提前告知。' }; } },
  { id: 'release-trigger-missing', severity: 'P1', applies: () => true,
    test: t => { const m = find(RELEASE_CREATORS, t); if (!m || /^\s*tags:/m.test(t) || /workflow_dispatch/.test(t)) return null;
      return { index: m.index, detail: '工作流会创建 release，却没有 tag 触发器，release 步骤可能永远不运行，或在分支推送时意外发布。', fix: '使用 `on.push.tags: [v*]`（或 app 专属前缀），并在 job 中断言 ref_type == tag。' }; } },
  { id: 'release-without-test-gate', severity: 'P1', applies: () => true,
    test: t => { if (!/^\s*tags:/m.test(t) || !RELEASE_CREATORS.test(t)) return null;
      if (/needs:\s*\[?[^\n]*\b(test|tests|check|ci|validate|verify)\b/.test(t) || /\b(yarn|npm|pnpm|bun)\s+(run\s+)?(test|lint|typecheck|check)\b|cargo (test|clippy|check)/.test(t)) return null;
      const m = find(/^\s*tags:/m, t); return { index: m.index, detail: 'tag 触发的发布没有在同一工作流中运行测试，也没有 `needs:` 测试 job；只在 main 上跑 CI 时，tag 可能发布从未通过 CI 的提交。', fix: '在发布工作流内加入 validate/test job，build 与 publish `needs:` 它（红树不发布）。' }; } },
  { id: 'version-single-source', severity: 'P1', applies: c => c.isTauri || c.hasElectron,
    test: (t, c) => { const m = find(/^\s*tags:/m, t); if (!m || !RELEASE_CREATORS.test(t) || c.versionAsserted(t)) return null;
      return { index: m.index, detail: /v__VERSION__/.test(t) ? '`tagName: v__VERSION__` 用应用版本命名 release；推送的 tag 与配置不一致时，release 会挂在另一个版本号下，推送的 tag 没有 release。' : 'tag 触发发布，但没有把 tag 注入版本或断言二者一致；release 名、安装包文件名、内嵌版本可能各说各话。', fix: 'house style：tag 是唯一版本源。构建前注入（如 `npm pkg set version=${GITHUB_REF_NAME#v}` 并同步 tauri.conf/Cargo）或断言一致，不一致即失败。' }; } },
  { id: 'node-version-vs-engines', severity: 'P1', applies: c => !!c.enginesNode,
    test: (t, c) => { const m = find(/node-version:\s*['"]?(\d+)/, t); if (!m) return null; const need = Number((/(\d+)/.exec(c.enginesNode) ?? [])[1]);
      if (!need || Number(m.match[1]) >= need) return null;
      return { index: m.index, detail: `CI 固定 Node ${m.match[1]}，而 package.json engines 要求 ${c.enginesNode}。`, fix: 'CI 不能低于 engines 下限；engines 按工具链约束计算，.nvmrc 不参与。' }; } },
  { id: 'matrix-artifact-name-collision', severity: 'P1', applies: () => true,
    test: t => { if (!/matrix:/.test(t)) return null; const re = /actions\/upload-artifact@[^\n]*\n(?:[^\n]*\n){0,6}?\s*name:\s*([^\n]+)/g; let m;
      while ((m = re.exec(t))) if (!/\$\{\{\s*(matrix|runner|strategy)\./.test(m[1])) return { index: m.index, detail: `矩阵 job 上传同名 artifact \`${m[1].trim()}\`；v4+ 不允许同名覆盖，后到的平台会失败或丢失。`, fix: '名称包含 `${{ matrix.platform }}-${{ matrix.arch }}`，聚合时用 pattern + merge-multiple。' };
      return null; } },
  { id: 'get-childitem-include-glob', severity: 'P1', applies: () => true,
    test: t => { const re = /Get-ChildItem\s+([^\s|]+)([^\n]*?-Include[^\n]*)/gi; let m;
      while ((m = re.exec(t))) { if (m[1].includes('*') || /-Recurse/i.test(m[2])) continue;
        return { index: m.index, detail: `\`Get-ChildItem ${m[1]} -Include …\` 在路径不带通配符且无 -Recurse 时返回 0 个文件，计数检查会误判产物缺失。`, fix: `改为 \`Get-ChildItem ${m[1]}\\* -Include …\`。` }; }
      return null; } },
  { id: 'checksum-crlf', severity: 'P1', applies: () => true,
    test: t => { const m = find(/(Set-Content|Out-File)[^\n]*SHA256SUMS|SHA256SUMS[^\n]*(Set-Content|Out-File)/i, t); if (!m) return null;
      return { index: m.index, detail: 'PowerShell `Set-Content`/`Out-File` 在 Windows 写 CRLF，`sha256sum -c` 会把 `\\r` 当作文件名一部分，Linux/macOS 上全部 FAILED。', fix: '在 Linux job 用 `sha256sum` 生成，或用 `[IO.File]::WriteAllText` + `\\n` 拼接，或 scripts/checksums.mjs。' }; } },
  { id: 'archive-incomplete-directory', severity: 'P1', applies: () => true,
    test: t => { const m = find(/Compress-Archive[^\n]*-Path\s+[^\n]*(?:\*|Join-Path)/i, t); if (!m || !/dotnet publish/.test(t)) return null;
      return {index: m.index, detail: '发布目录用通配符交给 Compress-Archive，隐藏资源可能被跳过；仅验证源目录无法发现缺包。', fix: '完整目录用 tar 打包，保留原生库与外置资源，并从独立解包目录运行 smoke。本地和 CI 调用同一打包脚本。'}; } },
  { id: 'checksum-self-reference', severity: 'P1', applies: () => true,
    test: t => { const m = find(/sha256sum\s+\*[^\n]*>\s*SHA256SUMS(?:\.txt)?/i, t); if (!m) return null;
      return {index: m.index, detail: '通配符生成校验和会在重跑时读入旧 SHA256SUMS，产生自引用。', fix: '使用明确资产列表或显式排除校验和自身，缺摘要失败；检查重跑结果及所有必需文件。'}; } },
  { id: 'privileged-trigger', severity: 'P1', applies: () => true,
    test: t => { const m = find(/pull_request_target|workflow_run/, t); if (!m) return null;
      return { index: m.index, detail: '提权触发器：若 checkout/执行 PR 代码或消费其产物，可能泄露 secrets 或污染 release。', fix: '不可信代码只在 `pull_request`（无 secrets）中运行；提权 workflow 只处理可信数据。' }; } },
  { id: 'expression-injection', severity: 'P1', applies: () => true,
    test: t => { const m = find(/run:[^\n]*\$\{\{\s*github\.(event\.(pull_request|issue|comment|head_commit)\.(title|body|head\.ref|message)|head_ref)/, t); if (!m) return null;
      return { index: m.index, detail: '不可信事件字段直接拼进 shell。', fix: '先放进 env，再以 "$VAR" 引用。' }; } },
  { id: 'write-all-permissions', severity: 'P1', applies: () => true,
    test: t => { const m = find(/permissions:\s*write-all/, t); return m ? { index: m.index, detail: '`write-all` 让每个步骤（含第三方 Action）都能写仓库和 release。', fix: '顶层 `contents: read`，只在需要的 job 提权。' } : null; } },
  // ---------- P2: hygiene / house style ----------
  { id: 'platform-coverage', severity: 'P2', applies: c => c.isTauri || c.hasElectron,
    test: (t, c) => { if (!RELEASE_CREATORS.test(t)) return null; const want = c.platforms;
      const seen = { windows: /windows/i.test(t) || /--win\b/.test(t), macos: /macos|--mac\b|apple-darwin/i.test(t), linux: /ubuntu|linux|--linux\b|AppImage/i.test(t) };
      const missing = want.filter(p => !seen[p]); if (!missing.length) return null; const m = find(RELEASE_CREATORS, t);
      return { index: m.index, detail: `发布工作流未覆盖 house style 平台：${missing.join(', ')}。`, fix: '按 templates/ 中的多平台矩阵补齐；暂不发布的平台在 .desktop-policy.json 中写明原因与复查条件。' }; } },
  { id: 'updater-json-prefer-nsis', severity: 'P2', applies: c => c.usesTauriUpdater && c.tauriBothWindowsBundles,
    test: t => { const m = find(/tauri-apps\/tauri-action/, t); if (!m || /updaterJsonPreferNsis:\s*true/.test(t)) return null;
      return { index: m.index, detail: '同时产出 MSI 与 NSIS 时，tauri-action 默认让 latest.json 指向 MSI（历史原因）。', fix: 'house style 以 NSIS 为 Windows 正式安装包：设置 `updaterJsonPreferNsis: true`，或只打 NSIS。' }; } },
  { id: 'gh-release-create-retry', severity: 'P2', applies: () => true,
    test: t => { const m = find(/gh release create(?![^\n]*\|\|)/, t); if (!m || /gh release view|select\(\.tag_name|releases\/tags\//.test(t)) return null;
      return { index: m.index, detail: '`gh release create` 在 release 已存在时直接失败，重跑失败的发布需要手动清理。', fix: '先 `gh release view` 判断存在，再 create 或 `gh release upload --clobber`；或以草稿为重试锚点。' }; } },
  { id: 'electron-publish-never', severity: 'P2', applies: c => c.hasElectron,
    test: t => { const m = find(/electron-builder(?![^\n]*--publish)/, t); if (!m || /--publish[ =](never|always|onTag)/.test(t)) return null;
      return { index: m.index, detail: '打包步骤未显式 `--publish never`；electron-builder 可能在 CI 中自行尝试发布，并在构建完成后失败或与统一发布步骤竞争。', fix: '矩阵打包统一 `--publish never`，由单一 publish job 上传。' }; } },
  { id: 'make-latest-explicit', severity: 'P2', applies: () => true,
    test: t => { const m = find(/draft=false|--draft=false/, t); if (!m || /make_latest|--latest/.test(t)) return null;
      return { index: m.index, detail: '发布草稿时未显式设置 latest，也未断言 `releases/latest` 指向本 tag。依赖 latest 的 updater 端点可能仍指向旧版本。', fix: '`-f make_latest=true`，随后 `gh api repos/$REPO/releases/latest --jq .tag_name` 必须等于 tag。' }; } },
  // ---------- P1: release-wiring gates (job order, event recursion) ----------
  { id: 'winget-before-publish', severity: 'P1', applies: () => true,
    test: t => { const m = find(/wingetcreate|winget-releaser|komac/i, t); if (!m) return null;
      if (/needs:\s*\[?[^\n]*\b(publish|verify|release-verify|promote)\b/.test(jobBlock(t, m.index))) return null;
      return { index: m.index, detail: 'winget 提交步骤没有 `needs:` 已发布并核验的 publish job；草稿未公开、资产缺失或 latest 未切换时，winget PR 会指向不存在或错误的安装包。', fix: '放到发布工作流最后一个 job（`needs: publish`，仅稳定版、先做 WINGET_TOKEN 预检），或用 `gh workflow run` 触发独立 winget 工作流。' }; } },
  { id: 'release-event-github-token', severity: 'P1', applies: () => true,
    test: t => { const m = find(/^\s*release:\s*\n\s*types:\s*\[?[^\n]*(published|released)/m, t); if (!m) return null;
      return { index: m.index, detail: '`on: release: published` 不会被 GITHUB_TOKEN 发布的 release 触发（GitHub 防递归规则）。由 CI 发布草稿时，这个工作流会静默不运行。', fix: '改为发布工作流中的后续 job（`needs: publish`），或由 publish job 用 `gh workflow run`（workflow_dispatch 不受该限制，需要 `actions: write`）；只有人工在网页发布时才可依赖 release 事件。' }; } },
];

export function runTraps(files, ctx, onError, rules = TRAPS) {
  const findings = [];
  for (const { file, text } of files) {
    const t = stripComments(text);
    for (const trap of rules) {
      if (!trap.applies(ctx)) continue;
      let r = null;
      // A trap that throws has NOT checked anything: report it as an error instead of
      // letting it look like a clean "no finding" (the caller marks the run incomplete).
      try { r = trap.test(t, ctx); } catch (e) { onError?.({ file, id: trap.id, error: e }); r = null; }
      if (r) findings.push({ id: trap.id, severity: trap.severity, file, line: lineOf(t, r.index), detail: r.detail, fix: r.fix, confidence: 'heuristic' });
    }
  }
  return findings;
}

export function defaultContext(over = {}) {
  return { isTauri: false, hasElectron: false, hasElectronUpdater: false, usesTauriUpdater: false, tauriCreateUpdaterArtifacts: null,
    tauriBothWindowsBundles: false, electronMajor: null, lockfiles: {}, packageManager: null, yarnFlavor: null, enginesNode: null,
    platforms: ['windows', 'macos', 'linux'],
    versionAsserted: t => /npm pkg set version|yarn version|update-version|set-version|ref_type|GITHUB_REF_NAME#v|ref_name\s*#v|-replace\s+'\^v'|version mismatch|!= *"\$\{?(VERSION|version)/i.test(t),
    ...over };
}
