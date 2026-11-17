# CI & Release 陷阱（scripts/ci-traps.mjs）

这些模式的共同点：**构建是绿的，交付却坏了**。检测基于去掉注释后的 workflow 文本逐行启发式匹配，不是 YAML 解析器——每条发现都是 `confidence: heuristic`，修改前读对应 job 确认。

- 严重度与框架风险分开：报告里 CI & Release 是独立分区，不混进框架 P0/P1。
- P0 = 用户收不到（正确的）更新或发布必然失败；P1 = 安全/可复现性/部分用户受影响；P2 = house style 差距与卫生。
- 已知取舍（如未签名）：在 `.desktop-policy.json` 的 `deviations` 里写 `{ "rule": "<发现 id>", "reason", "revisitWhen" }`，该发现即标为 `accepted`，单列在“已接受的偏离”，不计入 P0/P1/P2；缺 reason 或 revisitWhen 的不予接受，另报 `policy-deviation-undocumented`。
- `notice` = 符合 house style、只值得看一眼的提示（不计入 P0/P1/P2），如 `action-moving-ref`、`yarn-classic`。
- 注释会被剥离：`# gh release create collides` 这类说明文字不会被当成步骤。
- `bash-script-on-windows-runner` 按 job 核对 Windows runner、Bash 语法与 shell 声明；同文件其他 job 的 `shell: bash` 无法覆盖当前 job。矩阵与条件步骤仍需人工确认实际执行路径。
- `tauri-linux-deps` 只在**同一个 job** 内既有 Ubuntu runner、又有 Tauri 构建步骤时才报；Ubuntu 上只跑 `cargo audit` 的 security job 不再误报。`runs-on: ${{ matrix.os }}` 的矩阵 job 仍需人工读 job。
- `tagname-from-ref-unasserted` 与 `version-single-source` 共用 `versionAsserted` 的标记检测；它不是 YAML 解析器。显式写了断言也要包含可识别标记（如 `ref_type`、`GITHUB_REF_NAME#v`、`npm pkg set version`、`version mismatch`），否则仍会被报。建议在 release job 第一步用 `version mismatch:` 报错，并把 job 限定 `github.ref_type == 'tag'`；标记只是让启发式看见，不替代断言。`tagname-from-ref-unasserted` 只在**出现 `tagName` 的那个 job 内**找标记（别的 job 写了 `ref_type` 不算）；`version-single-source` 是文件级判断。

| 严重度 | ID | 现象 | 修复 |
|---|---|---|---|
| P0 | `rust-cache-workspace` | rust-cache 的 `… -> …` 缓存了整个源码树而不只是 target；恢复时会用旧快照覆盖新 checkout。 | 改为 `./src-tauri -> target`（按实际 Cargo 工作区）。 |
| P0 | `artifact-action-retired` | `…` 已退役，job 会以配置错误立即失败，看起来像工作流 bug。 | 升级到当前 major 并核验 v4+ 的同名产物不可覆盖语义。 |
| P0 | `draft-never-published` | release 以草稿创建，但本工作流中没有发布草稿的步骤。updater 读的是 `releases/latest`，它忽略草稿：构建成功、没人收到更新。 | Electron/WPF 校验后直接发布；Tauri 暂存草稿时须配置校验后的自动公开步骤，人工发布仅在项目明确要求时采用。 |
| P0 | `release-permissions` | 工作流创建/上传 release，但没有授予 `contents: write`；默认 token 只读，发布步骤会失败并可能留下半成品草稿。 | 仅在 stage/publish job 授予 `contents: write`，其余 job 保持 `contents: read`。 |
| P0 | `tagname-from-ref-unasserted` | `tagName` 取自 `github.ref_name`，而安装包文件名和内嵌版本来自配置；两者不一致时，名为 v3.0.1 的 release 可能装着 3.0.0。`workflow_dispatch` 时 ref_name 还是分支名。 | 构建前把 tag 注入版本或断言 tag == manifest 版本，并限定 `github.ref_type == tag`。 |
| P0 | `cache-lockfile-mismatch` | setup-node 配了 `cache: npm/yarn/pnpm`，仓库里却没有对应锁文件；job 会因找不到 cache-dependency-path 失败。 | 改为实际包管理器，或提交对应锁文件。 |
| P0 | `npm-ci-without-lockfile` | 工作流用 `npm ci`，仓库却只有 yarn/pnpm/bun 锁文件；`npm ci` 没有 package-lock.json 立即失败（把 npm 模板复制进 Yarn 仓库时最常见）。 | 按实际包管理器安装（Yarn 1 `--frozen-lockfile`、Yarn 4 `corepack enable` + `--immutable`、pnpm `--frozen-lockfile`）并同步 `cache:`；或真迁 npm 并提交 package-lock.json。 |
| P0 | `tauri-updater-manifest` | 应用启用了 Tauri updater，但 `bundle.createUpdaterArtifacts` 未开启或 `uploadUpdaterJson:false`，release 中不会有 `latest.json`/`.sig`；更新端点 404，应用永远“没有新版本”。 | 开启 createUpdaterArtifacts，配置 TAURI_SIGNING_PRIVATE_KEY(_PASSWORD)，并在 publish 前校验 latest.json 含全部平台。 |
| P0 | `electron-updater-manifest` | 应用使用 electron-updater，但另行上传的资产中看不到 `latest.yml` / `latest-mac.yml` / `latest-linux*.yml`。updater 依赖这些清单定位新版本。 | 上传每个平台的 latest*.yml、对应安装包/zip 与 .blockmap；发布前逐一校验 files[].url 存在。 |
| P0 | `electron-updater-windows-target` | electron-updater 在 Windows 只支持 NSIS 安装版；portable/dir/zip 没有可替换的安装，Windows 用户永远收不到更新。 | 以 NSIS 为正式 Windows 产物，便携 zip 仅作“免安装试用”。 |
| P0 | `tauri-linux-deps` | Ubuntu runner 构建 Tauri，但没有安装 `libwebkit2gtk-4.1-dev` 等系统依赖；Linux 构建会失败。 | 按当前 Tauri 官方 pipeline 安装 libwebkit2gtk-4.1-dev、build-essential、curl、wget、file、libxdo-dev、libssl-dev、libayatana-appindicator3-dev、librsvg2-dev、patchelf 等。 |
| P1 | `electron-runtime-download` | Electron 42 起不再在 postinstall 下载二进制，`ELECTRON_SKIP_BINARY_DOWNLOAD` 已移除。**打包本身不受影响**：electron-builder 会自己下载发行包（app-builder-lib 的 downloadElectronArtifactZip），node_modules/electron/index.js 在首次被 require 时也会按需自下载。变的是**下载时机**——从「npm ci 时」挪到「第一次用到时」：离线/气隙 runner 会在那一刻才失败，e2e 里启动 Electron 会在测试步骤里触发下载，自定义 electronDist 指向 node_modules/electron/dist 也拿不到东西。 | 安装依赖后显式运行 `node node_modules/electron/install.js`（Yarn：`yarn run install-electron`；pnpm：`pnpm exec install-electron`），把下载固定在安装步骤里。它是 electron 包的 bin，不是 npm script——`npm run install-electron` 会报 Missing script。 |
| P1 | `npm-install-not-ci` | CI 用裸 `npm install`/`npm i`：按声明范围重新解析、可能改写 package-lock.json，构建依赖与锁文件不一致。（`npm i -g 工具`、`npm i 包名` 不算） | 改为 `npm ci`。 |
| P1 | `yarn-install-not-frozen` | CI 中 `yarn install` 没冻结锁文件；或 flag 用错：yarn classic 不识别 `--immutable`，yarn berry 中 `--frozen-lockfile` 是弃用别名。 | Yarn 1 用 `yarn install --frozen-lockfile`，Yarn 2+ 用 `yarn install --immutable`。 |
| P1 | `yarn-berry-corepack` | 项目使用 yarn berry，但工作流没有 `corepack enable`；runner 自带的全局 yarn 可能是 classic，`cache: yarn` 与安装行为都会错位。 | 在 setup-node 缓存/安装之前执行 `corepack enable`，并在 package.json 声明 `packageManager`。 |
| P1 | `tauri-macos-rust-targets` | 为 macOS 指定了 Rust target，但没有安装对应 target；交叉架构构建会失败。 | rust-toolchain 步骤加入 `targets: aarch64-apple-darwin,x86_64-apple-darwin`（仅 macOS runner）。 |
| P1 | `electron-builder-empty-csc-link` | CSC_LINK 直接取自 secrets：GitHub 把「没有这个 secret」渲染成**空字符串**（不是不设置），而 electron-builder 把空的 CSC_LINK 理解成「证书就是这个路径」，于是拿工作目录当证书去签，构建直接失败——macOS 上表现为 `⨯ <工作目录> not a file`。Windows 与 Linux 不受影响，只有 macOS 这条腿会红，看起来像平台问题，其实凭据为空。 | 用别的名字收下 secret，只在真的有值时再导出成 electron-builder 认的名字（`if [ -n "$MAC_CSC_LINK" ]; then export CSC_LINK="$MAC_CSC_LINK"; export CSC_KEY_PASSWORD=...; fi`）。没有凭据 = 明确的不签名，而不是一个空字符串。 |
| P1 | `bash-script-on-windows-runner` | 工作流里有 Windows runner，却有**多行 bash 脚本**（`set -euo`、`export`、`[[`、`[ -n`）而没有声明 `shell: bash`。Windows runner 的默认 shell 是 PowerShell，那条腿会直接报 ParserError，而 macOS/Linux 照常通过——看着像平台问题，其实是 shell 不对。 | 给用到 bash 的步骤显式加 `shell: bash`（GitHub 的 Windows runner 自带 Git Bash）；或把脚本改写成两边都能跑的写法。 |
| P1 | `electron-mac-multiarch-split` | macOS x64 与 arm64 在不同 job 分别打包，会各自生成同名 `latest-mac.yml` 并互相覆盖，一种架构的用户收不到正确更新。 | 同一 job 中 `--mac --x64 --arm64`（或 universal），生成包含双架构的单一清单。 |
| P1 | `macos-not-notarized` | 发布 macOS 产物但没有签名/公证配置。站外下载的未公证 App 会被 Gatekeeper 拦截（用户需手动“仍要打开”）；Electron 在 macOS 的自动更新要求应用已签名。 | 首选 Developer ID 签名 + 公证；暂时没有 Apple 凭据时，Tauri 配置 ad-hoc 签名并在 release 说明写明打开方式，Electron 关闭 macOS 自动更新或标注为手动更新。 |
| P1 | `windows-unsigned` | 公开分发的 Windows 产物未签名：首次运行显示“未知发布者”，SmartScreen 告警；winget 渠道不会消除该告警。 | 按 house style，公开分发后默认签名（优先 Azure Artifact Signing）；未签名期间在 release 说明中提前告知。 |
| P1 | `release-trigger-missing` | 工作流会创建 release，却没有 tag 触发器，release 步骤可能永远不运行，或在分支推送时意外发布。 | 使用 `on.push.tags: [v*]`（或 app 专属前缀），并在 job 中断言 ref_type == tag。 |
| P1 | `release-without-test-gate` | tag 触发的发布没有在同一工作流中运行测试，也没有 `needs:` 测试 job；只在 main 上跑 CI 时，tag 可能发布从未通过 CI 的提交。 | 在发布工作流内加入 validate/test job，build 与 publish `needs:` 它（红树不发布）。 |
| P1 | `version-single-source` | tag 触发发布却没把 tag 注入版本或断言一致，release 名、安装包文件名、内嵌版本可能各说各话；`tagName: v__VERSION__` 是其中一种：推送的 tag 与配置不一致时，release 会挂在另一个版本号下，推送的 tag 没有 release。 | house style：tag 是唯一版本源。构建前注入（如 `npm pkg set version=${GITHUB_REF_NAME#v}` 并同步 tauri.conf/Cargo）或断言一致，不一致即失败。 |
| P1 | `node-version-vs-engines` | CI 固定 Node N，而 package.json engines 要求更高版本。 | CI 不能低于 `engines` 下限；`engines` 按工具链约束计算，`.nvmrc` 不参与。 |
| P1 | `matrix-artifact-name-collision` | 矩阵 job 上传同名 artifact `<name>`；v4+ 不允许同名覆盖，后到的平台会失败或丢失。 | 名称包含 `${{ matrix.platform }}-${{ matrix.arch }}`，聚合时用 pattern + merge-multiple。 |
| P1 | `get-childitem-include-glob` | `Get-ChildItem <path> -Include …` 在路径不带通配符且无 -Recurse 时返回 0 个文件，计数检查会误判产物缺失。 | 改为 `Get-ChildItem <path>\* -Include …`。 |
| P1 | `checksum-crlf` | PowerShell `Set-Content`/`Out-File` 在 Windows 写 CRLF，`sha256sum -c` 会把 `\r` 当作文件名一部分，Linux/macOS 上全部 FAILED。 | 在 Linux job 用 `sha256sum` 生成，或用 `[IO.File]::WriteAllText` + `\n` 拼接，或 scripts/checksums.mjs。 |
| P1 | `privileged-trigger` | 提权触发器：若 checkout/执行 PR 代码或消费其产物，可能泄露 secrets 或污染 release。 | 不可信代码只在 `pull_request`（无 secrets）中运行；提权 workflow 只处理可信数据。 |
| P1 | `expression-injection` | 不可信事件字段直接拼进 shell。 | 先放进 env，再以 "$VAR" 引用。 |
| P1 | `write-all-permissions` | `write-all` 让每个步骤（含第三方 Action）都能写仓库和 release。 | 顶层 `contents: read`，只在需要的 job 提权。 |
| P1 | `winget-before-publish` | winget 提交步骤没有 `needs:` 已发布并核验的 publish job；草稿未公开、资产缺失或 latest 未切换时，winget PR 会指向不存在或错误的安装包。 | 放到发布工作流最后一个 job（`needs: publish`，仅稳定版、先做 WINGET_TOKEN 预检），或用 `gh workflow run` 触发独立 winget 工作流。 |
| P1 | `release-event-github-token` | `on: release: published` 不会被 GITHUB_TOKEN 发布的 release 触发（GitHub 防递归规则）。由 CI 发布草稿时，这个工作流会静默不运行。 | 改为发布工作流中的后续 job（`needs: publish`），或由 publish job 用 `gh workflow run`（workflow_dispatch 不受该限制，需要 `actions: write`）；只有人工在网页发布时才可依赖 release 事件。 |
| P2 | `platform-coverage` | 发布工作流未覆盖 house style 平台（列出缺失项）。 | 按 templates/ 中的多平台矩阵补齐；暂不发布的平台在 .desktop-policy.json 中写明原因与复查条件。 |
| P2 | `updater-json-prefer-nsis` | 同时产出 MSI 与 NSIS 时，tauri-action 默认让 latest.json 指向 MSI（历史原因）。 | house style 以 NSIS 为 Windows 正式安装包：设置 `updaterJsonPreferNsis: true`，或只打 NSIS。 |
| P2 | `gh-release-create-retry` | `gh release create` 在 release 已存在时直接失败，重跑失败的发布需要手动清理。 | 先 `gh release view` 判断存在，再 create 或 `gh release upload --clobber`；或以草稿为重试锚点。 |
| P2 | `electron-publish-never` | 打包步骤未显式 `--publish never`；electron-builder 可能在 CI 中自行尝试发布，并在构建完成后失败或与统一发布步骤竞争。 | 矩阵打包统一 `--publish never`，由单一 publish job 上传。 |
| P2 | `make-latest-explicit` | 发布草稿时未显式设置 latest，也未断言 `releases/latest` 指向本 tag。依赖 latest 的 updater 端点可能仍指向旧版本。 | `-f make_latest=true`，随后 `gh api repos/$REPO/releases/latest --jq .tag_name` 必须等于 tag。 |

另有 audit.mjs 直接给出的非 workflow 发现：

| 严重度 | ID | 含义 |
|---|---|---|
| P1 | `action-major-behind` | Action 落后于最新 release 的 major（在线模式）。`@v7` 永远不会自己升到 v8；读 release notes 后单独一个 PR 升。`dtolnay/rust-toolchain@stable` 这类工具链 ref 不比较。 |
| P1 | `mac-update-needs-zip` | macOS 的打包目标有 dmg/pkg 却没有 zip：electron-updater 的 MacUpdater 只在更新清单里找 zip（`findFile(files,"zip",["pkg","dmg"])` 里的 pkg/dmg 是**排除表**、不是兜底），清单于是指向 .dmg，检查更新抛 `ERR_UPDATER_ZIP_FILE_NOT_FOUND`——Mac 上「检查更新」100% 失败，而构建全绿、清单也在，只有用户点得到。修：mac 的 target 里加 zip（`electron-builder.yml` 的 `mac.target`，或工作流里的 `--mac dmg zip`），并在 publish job 校验 `latest-mac.yml` 指向 `.zip`。 |
| P2 | `policy-deviation-undocumented` | `.desktop-policy.json` 的偏离缺 reason 或 revisitWhen。 |
| notice | `action-moving-ref` | 能写产物的 Action（release 创建、上传、attestation、winget）用的是可移动 ref。符合 house style，只提示单独看一眼；只读 Action 不报。 |
| notice | `yarn-classic` | 存量 Yarn 1 项目：不强迁，CI 必须 `--frozen-lockfile`（违反时另报 P1）。 |

audit.mjs 在线模式还会按 Node 官方 release schedule 检查工具链 pin（pin 位置是行扫描，支持阶段来自 schedule）。P 级只针对 CI 的 `node-version` / `node-version-file`；`.nvmrc`/`.node-version` 是可选本地文件，过期只在 Heads-up 提示：

| 严重度 | ID | 含义 |
|---|---|---|
| P1 | `node-version-eol` | CI 固定的 Node major 已 EOL；构建工具链不再获得安全补丁。 |
| P2 | `node-version-maintenance` | CI 的 Node major 处于 maintenance，且已有更新的 LTS 线；house style 要求 Active LTS。 |
| P2 | `node-version-not-lts` | CI 固定在不会有 LTS 的 Current 线（奇数 major）；偶数 major 在 LTS 日期前视为即将进入 LTS，不报。 |

`--dotnet`（scripts/dotnet.mjs）另报 .NET SDK 来源检查：

| 严重度 | ID | 含义 |
|---|---|---|
| P1 | `dotnet-version-two-sources` | `setup-dotnet` 同时配置 `global-json-file` 与 `dotnet-version`；两个版本源，升级时必有一处被忘掉。 |
| P1 | `dotnet-version-shadows-global-json` | CI 用 `dotnet-version`，但仓库有 `global.json`；本地与 CI 用了两个版本源，CI 不读 `global.json`。 |
| P2 | `dotnet-setup-without-version` | `setup-dotnet` 既没有 `global-json-file` 也没有 `dotnet-version`；没有明确的 SDK 来源。 |
| P2 | `dotnet-ci-setup-missing` | 仓库有 `global.json`，但工作流没有 `setup-dotnet`；CI 依赖 runner 恰好预装了 pin 的 SDK。 |

运行时/SDK 的 `frameworkFindings`：`dotnet-runtime-eol`（P0）、`dotnet-runtime-eol-soon`（P1）、`dotnet-runtime-maintenance`（P2）、`dotnet-sdk-cannot-target`（P0）、`dotnet-sdk-pin-behind`（P2）、`dotnet-no-global-json` / `dotnet-sdk-version-missing`（notice）。

新增陷阱：在 `TRAPS` 中加 `{ id, severity, applies(ctx), test(text, ctx) }`，`test` 返回 `{ index, detail, fix }`；同时在 tests/core.test.mjs 加正例与“注释中出现同样文字”的反例，并在本表补一行（测试会检查每个 id 都在本文件里，且表中没有从代码里原样抄来、未渲染的 JS 模板插值）。

有意人工公开草稿的工作流可在 env 声明 `DESKTOP_RELEASE_MODE: manual`。审计按这个显式意图处理 `draft-never-published`，资产、版本和 feed 检查继续执行，公开动作由维护者在验证完成后执行。

## 分发回归检查

| ID | 检查与修复 |
| --- | --- |
| `archive-incomplete-directory` | .NET 发布通过 Compress-Archive 通配符打包可能丢隐藏文件。完整目录用 tar，外置资源和原生 DLL 随包，解包后启动。 |
| `checksum-self-reference` | sha256sum 通配符可能纳入旧校验和。使用明确资产列表，排除 SHA256SUMS 自身并验证重跑。 |
| `update-cache-architecture` | C# 中已知的版本单键缓存路径候选。使用进程架构选包，缓存按架构和版本隔离，测试旧 x64 缓存无法用于 ARM64。 |
| `release-manifest-inventory` | 从实际 manifests 枚举会漏掉整份缺失清单。改由必需平台清单驱动校验，验证版本、载体和摘要。 |
| `release-digest-skipped` | 缺 digest 的发布资产被过滤后可能仍成功。缺有效 SHA256 应失败，不能从校验和中悄悄省略。 |
| `release-checksum-inventory` | 本地发布脚本对 artifacts 中所有 ZIP 计算摘要，可能混入无关/旧文件。摘要与上传使用本次显式清单。 |
| `installer-ui-language` | 检查 JSON/YAML NSIS 及 Inno 的单一英文配置。动态继承、覆盖及自定义文案需要回查实际结果。 |

源文件项由 delivery-checks.mjs 读取 C#、发布脚本与安装器配置生成候选，随 audit.mjs 的 ciFindings 输出。规则只识别已知写法，未命中不代表更新与发布已经正确；发布模板的真实资产验证和设备验收继续执行。静态审计不加载应用依赖，YAML 配置标为 `notice` / `unknown`，不据排版判定语言错误。`--installer` 在应用构建环境中复用已安装的 YAML 解析器；包含继承或 hook 的项目先导出/核对实际合并的 builder JSON，不能用无关文件替代。

## 工作流覆盖与权限说明

workflowCoverage 分别列出 pullRequest、release、delegated 和 manual 的静态证据。桌面应用缺少 PR 或发布入口时生成 workflow-pull-request-missing / workflow-release-missing 候选；分发渠道及 delegated workflow 由实际项目复核。只发现 tag 触发并不足以证明存在发布步骤。

release-permissions 在执行发布的 job 中查有效 permissions，job 自己声明权限时覆盖顶层权限。显式 secret/input token 的权限需向凭据来源核实。draft-never-published 独立判断公开状态；make_latest 只控制 latest 标识。DESKTOP_RELEASE_MODE: manual 保留人工公开约定。规则仍是启发式，复杂 YAML、动态 shell 与其他工作流公开需人工确认。
