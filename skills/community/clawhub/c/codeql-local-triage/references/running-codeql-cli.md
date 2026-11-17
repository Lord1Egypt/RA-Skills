# 安装 CodeQL CLI 与建库跑查询 / Installing the CodeQL CLI & building a database

> 本文件承接 `SKILL.md` 中「环境搭建」类细节，让 `SKILL.md` 只保留触发与主流程。
> This file holds the environment-setup detail so `SKILL.md` stays focused on triggers and the main flow.
>
> 面向完全新手的**从零完整步骤链**：下载 → 解压 → 加入 PATH → 验证 → 最小试跑 → 建库跑单条查询。
> A complete from-scratch chain for absolute beginners: download → extract → PATH → verify → minimal try-run → build & single query.

CodeQL CLI 是**可选依赖**：预筛（`scan_sensitive_sources.py`）与读 SARIF（`read_sarif.py`）两步零依赖即可用；只有在 `bisect_taint.py` 真正建库跑查询时才需要它。`bisect_taint.py` 支持 `--codeql /abs/path`，所以**不配 PATH、不联网**也能用本机已有的 `codeql`。
The CodeQL CLI is an **optional dependency**: the prefilter and SARIF reader need it for nothing; only `bisect_taint.py` (build + analyse) uses it. Because `bisect_taint.py` accepts `--codeql /abs/path`, you can run it with a local `codeql` **without touching PATH or the network**.

---

## 0. 总览 / Overview

| 阶段 | 命令 | 需要联网? | 耗时 |
|---|---|---|---|
| ① 下载 | `gh release download …` | 是（仅这一次） | ~15 min（国内见 §5） |
| ② 解压 + PATH | `zipfile.extractall` + `export PATH` | 否 | 秒级 |
| ③ 验证 | `codeql --version` / `codeql resolve languages` | 否 | 秒级 |
| ④ 最小试跑 | `codeql database create ./_probe_db --language=python` | 否 | ~70 s |
| ⑤ 建库 + 跑单条查询 | `codeql database create` + `codeql database analyze --download` | 是（首次拉查询包） | 建库 ~9 min + 求值 ~30 s |

只有 ① 和 ⑤ 的 `--download` 会联网；④ 完全离线，足够验证 CLI 是否装好。
Only ① and the `--download` in ⑤ touch the network; ④ is fully offline and enough to prove the CLI works.

---

## 1. 下载 / Download

一次性，下载 ~400 MB。该 zip **只含提取器**，查询包在 `database analyze` 时自动拉，不用单独下。
One-off, ~400 MB. The zip contains **extractors only**; query packs are pulled during `database analyze`.

```bash
gh release download v2.27.1 --repo github/codeql-cli-binaries --pattern "codeql-win64.zip"
python -c "import zipfile; zipfile.ZipFile('codeql-win64.zip').extractall('.')"
./codeql/codeql version          # expect 2.27.1 / 应打印 2.27.1
```

| 平台 / Platform | `--pattern` |
| --- | --- |
| Windows x64 | `codeql-win64.zip` |
| Linux x64 | `codeql-linux64.zip` |
| macOS Intel | `codeql-osx64.zip` |
| macOS Apple silicon | `codeql-osx-arm64.zip` |

- 先用 `zipfile.ZipFile(...).testzip()` 校验完整性；Python 的 `zipfile` 比 `unzip` 稳。
  Validate first with `zipfile.ZipFile(...).testzip()`; Python's `zipfile` is more reliable than `unzip`.
- 查最新版本 / Latest version:
  `gh api repos/github/codeql-cli-binaries/releases/latest --jq .tag_name`
- 实测下载很慢（约 15 分钟），放后台跑。
  In practice the download is slow (~15 min) — run it in the background.
- **国内/离线场景见 §5**（镜像、预建 DB、免联网用法）。
  **Domestic / offline options — see §5** (mirror, pre-built DB, no-network usage).

---

## 2. 解压并加入 PATH / Extract & add to PATH

解压后得到 `./codeql/codeql`：
After extraction you get `./codeql/codeql`:

```bash
python -c "import zipfile; zipfile.ZipFile('codeql-win64.zip').extractall('.')"
ls codeql/codeql        # 确认二进制存在 / confirm the binary exists
```

把 `codeql` 目录加入 PATH（任选其一 / pick one）：

```bash
# Linux / macOS（写入 shell 配置后重开终端）
export PATH="$PWD/codeql:$PATH"

# Windows (PowerShell, 持久化)
setx PATH "$env:PATH;$PWD\codeql"
```

> **不想配 PATH 也行**：`bisect_taint.py` 用 `--codeql /abs/path/to/codeql` 直接指绝对路径即可，完全不需要 PATH。
> **No PATH needed**: pass `--codeql /abs/path/to/codeql` to `bisect_taint.py` and you never configure PATH.

---

## 3. 验证安装 / Verify the install

两条命令都能离线跑，用来确认 CLI 与提取器正常：
Both commands run offline and confirm the CLI + extractors work:

```bash
codeql --version            # 期望打印 2.27.1（或你下载的版本）/ expect the version you downloaded
codeql resolve languages    # 期望输出里含 python / expect "python" in the list
```

- 若 `codeql --version` 报 `command not found` → PATH 没生效（回到 §2 重开终端，或用绝对路径 `/abs/codeql/codeql`）。
  If `command not found` → PATH not effective (reopen the terminal, or use the absolute path `/abs/codeql/codeql`).
- 若 `resolve languages` 不含 `python` → 解压不完整，重新下载/解压。
  If `python` is missing from `resolve languages` → extraction incomplete, re-download/extract.

---

## 4. 最小试跑（验证 CLI 是否真的可用）/ Minimal try-run

建一个最小 Python 数据库，成功即证明 CLI + 提取器可用，**无需任何查询包、不联网**：
Build a minimal Python database; success proves the CLI + extractors work, **no query pack, no network**:

```bash
codeql database create ./_probe_db --language=python
# 期望看到 "Successfully created database(s) at ./_probe_db" / expect "Successfully created..."
#
# 注：_probe_db 只是**一次性、可丢弃**的 CodeQL 建库产物，不是任何 agent 状态 / 记忆；
# 它每轮都从源码重建（H5 幂等 rmtree+rebuild），绝不会被读回当作跨会话持久化的状态。
# Note: _probe_db is a throwaway CodeQL build artifact, NOT agent state/memory; it is rebuilt from
# source every run and is never read back as cross-session persistent state.
```

这一步是「装好没装好」的硬验证——在信任一次真实 triage 之前先跑它。
This is the hard check that the CLI is usable before you trust a real triage run.

---

## 5. 国内与离线选项 / Domestic & offline options  ← R6

> **先读这一条**：如果你只是想判断「这条告警是不是命中名字启发式、污染从哪开始」，**本节整段都可以跳过**——
> 预筛（`scan_sensitive_sources.py`）与读 SARIF（`read_sarif.py`）**零依赖、不联网**。
> 只有需要「用对照实验**证明**因果」时才需要装 CLI。
>
> **Read this first**: if you only need to know *whether* the alert is a name-heuristic hit and *where*
> the taint starts, **skip this whole section** — the prefilter and SARIF reader need no download.
> Install the CLI only when you need the controlled experiment that *proves* the cause.

CodeQL CLI 的下载源是 `github.com`，国内网络环境可能偏慢。以下方案**按需采用，第 1 条可直接复制粘贴**。
The CLI is downloaded from `github.com`, slow in some regions. Adopt as needed — **option 1 is copy-pasteable**.

### 5.1 走镜像下载（仅官方源不可达时的不可信回退）/ Download via a mirror (untrusted fallback, official source unreachable only)

> **默认且唯一被本技能推荐的来源是官方 GitHub Release**（§1 的 `gh release download … --repo github/codeql-cli-binaries`）：它走官方 TLS + `gh` 对 release 资产的校验，不经任何第三方中转。**下面的镜像 / 代理方式不是等价的「更省事选项」，而是显式不可信回退**——仅在官方源在你所在网络确实不可达时使用，且**执行前你必须亲自核对 SHA-256**。
> **The only source this skill recommends by default is the official GitHub Release** (§1 `gh release download … --repo github/codeql-cli-binaries`): official TLS + `gh`'s asset verification, no third-party hop. The mirror/proxy options below are **not an equivalent "easier" choice — they are an explicit untrusted fallback**, for when the official source is genuinely unreachable from your network, and **you must verify the SHA-256 yourself before running it**.

官方源命令（默认 / default）：

```bash
gh release download v2.27.1 --repo github/codeql-cli-binaries --pattern "codeql-win64.zip"
```

不可信回退（仅官方源不可达时 / untrusted fallback — official source unreachable only）：

```bash
# 方案 A：环境变量式镜像（最灵活，一次设置全局生效）
export GH_HOST=mirror.example.com          # ← 换成你可用的镜像域名
gh release download v2.27.1 --repo github/codeql-cli-binaries --pattern "codeql-win64.zip"

# 方案 B：只代理 GitHub release 下载走代理（gh 原生支持）
export HTTPS_PROXY=http://127.0.0.1:7890
gh release download v2.27.1 --repo github/codeql-cli-binaries --pattern "codeql-win64.zip"

# 方案 C：用 curl 走镜像直接下（不需要 gh）
curl -L -o codeql-win64.zip "https://mirror.example.com/github/codeql-cli-binaries/releases/download/v2.27.1/codeql-win64.zip"
```

> **执行前必须核对 SHA-256**（来自官方 release 页，**独立可信通道**取得；本技能不写死哈希，随版本过期会成新的假陈述）：
> **Verify the SHA-256 before running (obtain it from the official release page via an independent trusted channel — this skill does not hardcode hashes, which would go stale and become a false statement per version):**
>
> ```bash
> echo "<官方SHA256>  codeql-win64.zip" | sha256sum --check -
> ```
>
> - ❌ 不要用 `./codeql/codeql version` 当「执行前安全检查」——它**已经运行了**刚下载的二进制，被替换的二进制同样能打印期望的版本号。
>   Don't treat `./codeql/codeql version` as a pre-run safety check — it already executes the freshly downloaded binary; a replaced binary prints the expected version too.
> - ❌ `ZipFile.testzip()` 只验证归档**未被损坏**，**不验证发布者**真实性。
>   `ZipFile.testzip()` only checks the archive is **not corrupt**; it does **not** verify the publisher.
> - ❌ 删除「镜像与官方校验和相同」这类断言：第三方镜像**完全可能**提供被替换的归档，哈希自然不同。
>   Drop any "mirror == official checksum" claim — a third-party mirror can absolutely serve a replaced archive with a different hash.
> - 若你无法从独立可信通道取得官方 SHA-256，则**不要使用镜像**，直接等官方源恢复。
>   If you cannot obtain the official SHA-256 from an independent trusted channel, **do not use a mirror** — wait for the official source to recover.

### 5.2 预建数据库 + 随附查询包 / Pre-built DB + carried packs

在有访问能力的机器上先 `codeql database create` 产出 DB，并把 `~/.codeql/packages`（首次
`analyze --download` 拉下来的查询包）一并拷到离线机器。之后 `--codeql /abs/path` 指向本地二进制即可完全离线跑。

On a machine with access, build the DB and copy `~/.codeql/packages` (the packs pulled by the first
`analyze --download`) to the offline machine; then `--codeql /abs/path` runs fully offline.

```bash
# 有网机器：建库一次，并把查询包落盘带走
codeql database create ./db --language=python --source-root=src --threads=0
codeql database analyze ./db --format=sarif-latest --output=./probe.sarif \
    --download codeql/python-queries:Security/CWE-312/CleartextStorage.ql   # ← 只为把 ~/.codeql/packages 拉下来

# 拷到离线机器后
cp -r ~/.codeql/packages <离线机器>/.codeql/
./codeql/codeql database analyze <path>/db --format=sarif-latest --output=out.sarif \
    "codeql/python-queries:Security/CWE-312/CleartextStorage.ql"           # 不再需要 --download
```

> **复用同一份 DB**：同一棵源码只需建库一次，后续对照实验把 `--source-root` 指回同一目录即可，
> 把「每次 ~9 分钟建库」摊薄成「只付首次成本」。
> **Reuse one DB**: build once per source tree; point later runs at the same root, paying the build cost once.

### 5.3 零依赖两步永不需 CodeQL / The two zero-dependency steps never need CodeQL

预筛（`scan_sensitive_sources.py`）和读 SARIF（`read_sarif.py`）**完全不碰 CodeQL**，任何装有 Python 的
机器都能跑——只有第 ③ 步变体二分才需要本节安装的 CLI。换言之，**核心判定不依赖一次海外大体积下载**。

The two zero-dependency steps run on any Python machine; only step ③ needs the CLI. In other words,
**the core judgement does not depend on one large overseas download**.

```bash
# 这两条在任何装了 Python 的机器上都能跑（含离线 / 国内网络）
python scripts/scan_sensitive_sources.py src/          # 预筛
python scripts/read_sarif.py out.sarif                 # 读数据流
python tests/run_tests.py                              # 自测（也不需要 CodeQL）
```

---

## 6. 建库 + 跑单条查询 / Build a database + run a single query

**Run only the rule you care about** — never the whole **query suite** (a CodeQL *query collection* — unrelated to system services or scheduled tasks; `python-code-scanning.qls` takes tens of
minutes).

**只跑目标那一条**，别跑整个 **query suite（查询套件，CodeQL 的查询集合概念，与系统服务/计划任务无关）**（`python-code-scanning.qls` 要几十分钟）。

```bash
codeql database create  "$T/db" --language=python --source-root="$SRC" --overwrite --threads=0
codeql database analyze "$T/db" --download --format=sarif-latest \
    --output="$T/out.sarif" --threads=0 \
    "codeql/python-queries:Security/CWE-312/CleartextStorage.ql"
```

- `--download` installs `codeql/python-queries` into `~/.codeql/packages` on first use
  首次会装 `codeql/python-queries` 到 `~/.codeql/packages`
- Measured cost: single-file DB ~70 s; a whole mid-sized Python repo ~9 min (TRAP import dominates);
  single-query evaluation ~30 s
  耗时实测：单文件建库 ~70s；整仓建库 ~9 分钟（TRAP import 占大头）；单查询求值 ~30s
- Query path syntax is `<pack>:<path inside pack>`. Find paths with GitHub search:
  查询路径规则 `<pack>:<pack 内相对路径>`。找路径用 GitHub 搜索：
  `gh api "search/code?q=repo:github/codeql+<rule-id>+in:file" --jq '.items[].path'`
