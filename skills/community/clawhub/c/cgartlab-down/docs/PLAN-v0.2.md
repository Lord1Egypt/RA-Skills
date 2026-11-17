# v0.2 开发计划

> 本文件是 v0.2 的单一真源（single source of truth）。
> 每次变更都更新本文件 + CHANGELOG.md。

## 时间预算

| Phase | 内容 | 时间 |
|-------|------|------|
| A | v0.1.0 收口（6 项清理） | 0.5d |
| B | `scripts/check_tools.py` | 0.5d |
| B+' | `scripts/proxy_chain.py` | 0.25d |
| B+" | detect.py 分类扩展（cloud_drive + torrent→curl + magnet→none） | 0.5d |
| C | SKILL.md 加代理兜底章节 + 网盘/magnet/能力边界 | 0.5d |
| D | Windows 文档补齐 | 0.5d |
| E | 测试补齐（41+ 用例） | 0.5d |
| F | CHANGELOG + 版本发布 | 0.25d |
| **总计** | | **~3.5 天** |

---

## 核心设计原则

1. **skill 边界 = 用户显式说"下载"到 MEDIA: 回复之间**——超出范围的自动化不属 skill。
2. **探测器零网络**（detect.py 保持纯函数，Phase B 决策）
3. **代理链解析也不发网络**（proxy_chain.py 只读配置，不探测端口）
4. **不新增下载执行器**（Phase C 决策，下载命令 agent 手写）
5. **不静默安装**（任何工具安装前必须询问用户）
6. **验证才算完成**（ffprobe / sha256sum / file 出真实数字）
7. **NO_PROXY 强制**：目标域名匹配 NO_PROXY 时禁用代理，即使代理链里有可用项。

---

## 决策记录（Decision Log）

| # | 决策 | 理由 |
|---|------|------|
| D1 | 不做 probe_host.py（网络探测脚本） | 保持 detect.py 零网络的纯度，硬墙站点靠 agent 手写 grep |
| D2 | 不做 download.py（下载执行器） | 有副作用的动作交给 agent 手写，脚本只做只读检查 |
| D3 | check_tools.py 只做工具可用性检查 | 与 D2 一致：脚本只读，安装动作 agent 层询问 |
| D4 | Windows PowerShell 版本只补文档，代码不动 | 用户少，维护成本大 |
| D5 | 内置代理链 3 个：7897 → 7890 → 192.168.31.135:7890 | 与用户 memory 完全一致 |
| D6 | proxy_chain.py 保留，只解析不探测 | 延续 D1 决策（不发网络） |
| D7 | ~/.downrc 优先级：env > config > builtin | env 是运行时事实，builtin 是硬编码默认 |
| D8 | `.torrent` 文件用 curl 而非 aria2c | 用户只下种子文件本体，不需要 BT 客户端；依赖简化 |
| D9 | magnet 返回 tool=none，报告"请客户端处理" | magnet 是元数据 URI，非文件下载；skill 边界清晰 |
| D10 | 新增 cloud_drive kind，识别 8 个网盘但不下载 | 用户明确"给我链接就好，我自己转存"；不做网盘下载 |
| D11 | skill 不搜索资源 | "星际穿越 4K" 类请求 skill 拒绝，用户自己搜好链接再扔回来 |

---

## Phase A — v0.1.0 收口（0.5d）

| # | 事项 | 验收 |
|---|------|------|
| A1 | CHANGELOG 结构理顺：`[Unreleased]` 清空，v0.1.0 段落移到 `[0.1.0] - 2026-10-11` | `grep -c "^## \[" CHANGELOG.md == 1` |
| A2 | README 快速上手里的"clarify 问保存路径"改成"按 SKILL.md 三级优先级确定路径" | README 与 SKILL.md 语义一致 |
| A3 | README 目录树补 `docs/USAGE.md`；CHANGELOG v0.1.0 段补 USAGE.md 条目 | 目录树与实际文件系统一致 |
| A4 | `detect.py` 删掉 `mimetypes` / `shlex` 两个 dead import | `python -m py_compile scripts/detect.py` 通过 |
| A5 | 统一 `install_hint` 字段结构：`{name, purpose, install_by_platform: {windows, linux, macos}, size_mb, license}`——yt-dlp 也补全三平台安装命令 | 单元测试通过 + 新字段全用例覆盖 |
| A6 | `dest_name` 加路径净化：拒绝 `..`、替换 `/` 和 `\` 为 `_`、strip 控制字符 | 新增 test 用例：恶意 URL `%2e%2e%2fpasswd` 得到安全名 |

**提交**：
- docs fix: align README/CHANGELOG with SKILL.md (A1-A3)
- refactor(detect): unify install_hint schema + sanitize dest_name (A4-A6)

---

## Phase B — `scripts/check_tools.py`（0.5d）

**契约**：

```bash
python scripts/check_tools.py                    # 全量检查
python scripts/check_tools.py --tool curl        # 只查一个
python scripts/check_tools.py --required yt-dlp aria2c   # 指定必需集
python scripts/check_tools.py --json             # 结构化输出
```

**输出 JSON**：

```json
{
  "platform": "windows",
  "path_extended": true,
  "tools": {
    "curl":    {"available": true,  "path": "C:\\...\\curl.exe",  "version": "8.4.0"},
    "yt-dlp":  {"available": true,  "path": "C:\\Users\\...\\.local\\bin\\yt-dlp.exe", "version": "2024.09.06"},
    "aria2c":  {"available": false, "path": null, "version": null,
                "install_hint": "winget install -e --id aria2.aria2",
                "expected_size_mb": 4}
  },
  "missing": ["aria2c"],
  "missing_required": ["aria2c"],
  "verdict": "pass | partial | fail"
}
```

**关键约束**：
- Windows 自动扩展 PATH 到 `%LOCALAPPDATA%\.local\bin`（解决 SKILL.md 已知坑）
- 只查不装（严格遵守"不静默安装"红线）
- 缺失项返回安装命令提示（agent 层拿这个提示去问用户）

**验收**：
- `evals/test_check_tools.py`：mock `shutil.which` 和 `subprocess.run` 断言三种 verdict 判定正确
- 手动：`python scripts/check_tools.py --json` 在本机跑通

---

## Phase B+" — detect.py 分类扩展（0.5d）

**新增 kind**：`cloud_drive`（识别但不下载）。

**修改 kind 的 tool**：
- `torrent`：`aria2c` → `curl`（只下 .torrent 文件本体，用户手动下内容）
- `magnet`：`aria2c` → `none`（报告"请客户端处理"）

**新增 `CLOUD_DRIVE_SITES` 白名单**（detect.py 顶部）：

```python
CLOUD_DRIVE_SITES: dict[str, str] = {
    "pan.baidu.com": "百度网盘",
    "yun.baidu.com": "百度网盘",
    "pan.quark.cn": "夸克网盘",
    "www.aliyundrive.com": "阿里云盘",
    "www.alipan.com": "阿里云盘",
    "115.com": "115 网盘",
    "115cdn.com": "115 网盘",
    "cloud.189.cn": "天翼云盘",
    "wl.123pan.com": "腾讯微云",
    "wenku.baidu.com": "百度文库",
}
```

**新增 JSON 字段**（v0.2 契约扩展）：
- `user_action`：字符串或 null，用户应该做什么（如"请转存到网盘账号"）
- `reason`：字符串或 null，为什么这样建议

**扩展 `sanitize_filename`**：

```python
def sanitize_filename(name):
    name = unquote(name)
    name = name.replace("/", "_").replace("\\", "_")
    if ".." in name.split("_"): name = "download"
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)
    name = re.sub(r'[`$&|;<>(){}[\]*?"\']', '_', name)
    name = name[:200]
    return name or "download"
```

**新增 `user_action` 生成**：

```python
if kind == "magnet":
    user_action = "请将此 magnet 链接复制到 qBittorrent、Transmission 或类似客户端。"
    reason = "magnet 是元数据 URI，需要 BT 客户端解析，非文件下载。"
elif kind == "cloud_drive":
    user_action = f"请手动转存到你的 {provider} 账号。"
    reason = "skill 不处理网盘内容，用户自己转存。"
elif kind == "torrent":
    user_action = "下载 .torrent 文件本体；如需下载内容，用 BT 客户端打开此文件。"
    reason = "skill 只下载种子文件，不下载内容。"
```

**验收**：
- `evals/test_detect.py` 新增用例：cloud_drive（8 个 host）、magnet（tool=none + user_action 非空）、torrent（tool=curl）、文件名净化（shell 元字符）
- 现有 15 用例保持通过（torrent 的用例需更新 tool 期望值）

---

## Phase B+' — `scripts/proxy_chain.py`（0.25d）

**契约**：

```bash
python scripts/proxy_chain.py --json
```

**输出 JSON**：

```json
{
  "chain": [
    {"type": "direct",    "label": "直连"},
    {"type": "env",       "proxy": "http://127.0.0.1:7897", "source": "HTTPS_PROXY env"},
    {"type": "file",      "proxy": "http://...",             "source": "~/.downrc"},
    {"type": "builtin",   "proxy": "http://127.0.0.1:7890", "source": "SKILL.md default"},
    {"type": "builtin",   "proxy": "http://192.168.31.135:7890", "source": "SKILL.md default"}
  ],
  "noproxy": "sensenova.cn",
  "env_honored": ["HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY"],
  "config_file": "~/.downrc",
  "config_exists": false
}
```

**内置默认链**（脚本顶部常量）：

```python
BUILTIN_PROXY_CHAIN = [
    "http://127.0.0.1:7897",        # Hermes 当前工作代理（memory 已验证）
    "http://127.0.0.1:7890",        # Clash 默认端口
    "http://192.168.31.135:7890",   # LAN 兜底
]
```

**解析优先级**：
1. `direct`（永远第一条，除非 NO_PROXY 匹配）
2. env vars（HTTPS_PROXY / HTTP_PROXY）
3. `~/.downrc` 配置文件
4. `BUILTIN_PROXY_CHAIN` 硬编码默认

**TOML 兼容性决策**：Python 3.11+ 有 `tomllib`，但 skill 声明支持 3.9+。
**方案**：`~/.downrc` 用 **JSON 而非 TOML**（stdlib `json` 全版本支持）。SKILL.md 里预告 "TOML 支持留待 v0.3"。

**配置格式**（`~/.downrc`）：

```json
{
  "default_dir": "D:/Download",
  "proxy_chain": ["http://127.0.0.1:7897", "http://1.2.3.4:1080"],
  "prefer_tool": "curl"
}
```

**不做的事**：
- ❌ 不发网络请求（不测端口）
- ❌ 不修改环境变量
- ❌ 不探测代理可用性（真正验证靠重试下载）

**验收**：
- `evals/test_proxy_chain.py`：mock `os.environ` 三种组合，断言解析顺序 + 去重
- 手动：`python scripts/proxy_chain.py --json` 在本机输出 4 条链（direct + env 7897 + 7890 + LAN）

---

## Phase C — SKILL.md 加代理兜底 + 网盘/magnet/能力边界（0.5d）

**新增章节 1**（插在 Phase 2 之后，Phase 3 之前）——代理兜底：

### Phase 2.5 — 代理兜底

**默认行为**：先直连，失败才走代理。绝不默认代理所有请求。

**触发条件**（curl exit code 白名单）：6, 7, 28, 35, 51, 52, 53, 60, 91, 92, 99, 104, 105。

**不重试**：HTTP 4xx/5xx、认证错误、内容校验失败。

**代理链解析**：
```bash
python scripts/proxy_chain.py --json
```

按输出 chain 顺序逐条重试，第一条成功即停。

**NO_PROXY 强制规则**：目标域名匹配 `NO_PROXY` 时禁用代理，即使代理链里有可用项。
例：`https://api.sensenova.cn/...` 永远直连，不走任何代理。

**三工具的代理参数**：

| 工具 | 代理参数 |
|------|----------|
| curl | `--proxy <url>` 或 `-x` |
| yt-dlp | `--proxy <url>` |
| aria2c | `--http-proxy=<url>` / `--https-proxy=<url>` / `--all-proxy=socks5://...` |

**重试流程**（agent 手写，无脚本）：

```python
for proxy in chain:
    if domain_in_noproxy(target): break
    cmd = base_cmd + ("" if proxy.type == "direct" else f" --proxy {proxy.proxy}")
    result = run(cmd)
    if result.exit_code not in RETRYABLE: break
```

**报告**：
- 成功：告知"用了 <proxy source> 完成下载"
- 全部失败：告知"直连和 3 个代理都失败，错误码 <最后一次 exit code>"

**同步更新**：
- `references/tool-matrix.md` 加一节"代理参数速查"
- `references/commands.md` 每个配方补 `--proxy` 版本
- Phase 3 unknown 分支：明确写清 `curl -I` 探测流程

**新增章节 2**——网盘链接处理（SKILL.md 主入口后）：

```markdown
## 网盘链接（kind=cloud_drive）

识别到 kind=cloud_drive 时：
1. 不下载、不尝试、不询问
2. 回复模板：
   「这个链接是 {provider}，skill 不处理网盘内容。
    请把链接转存到你的网盘账号，需要其他帮助就说。」

覆盖的网盘：百度 / 夸克 / 阿里 / 115 / 天翼 / 微云 / 百度文库（10 个 host）。
```

**新增章节 3**——magnet 处理：

```markdown
## Magnet 链接（kind=magnet）

magnet 是元数据 URI，不是文件下载。skill 只报告，不处理：

回复模板：
「这是 magnet 链接，需要 BT 客户端解析。请复制到：
  - Windows: qBittorrent / Transmission
  - macOS: Transmission / qBittorrent
  - Linux: qBittorrent / Transmission / Deluge
  或者告诉我是否有 .torrent 文件直链，我可以下载 .torrent 本体。」
```

**新增章节 4**——能力边界（SKILL.md 顶部，紧跟"何时使用"之后）：

```markdown
## 能力边界

skill 能做的：
  ✓ 下载直链文件（HTTP/HTTPS）
  ✓ 下载平台视频（YouTube / X / Bilibili / TikTok / Douyin / ...）
  ✓ 下载 .torrent 文件本体（用户手动用 BT 客户端下内容）
  ✓ 识别网盘链接但不下载（用户手动转存）

skill 不做的：
  ✗ 搜索资源（"星际穿越 4K" 类模糊标题 → 请用户自己搜好链接）
  ✗ 从 magnet 拉内容（需要 BT 客户端，skill 只报告）
  ✗ 从网盘下载内容（需要账号登录，用户自己转存）
  ✗ 破解反爬站点（JS 挑战、Cloudflare turnstile 等）
```

**新增章节 5**——Phase 3 前置检查（文件名冲突处理）：

```markdown
## Phase 3.0 — 文件名冲突检查

如果 `<dest>/<dest_name>` 已存在：
- 追加序号：`foo.mp4` → `foo (1).mp4` → `foo (2).mp4`
- 覆盖不是默认行为
- 追加序号达到 100 时拒绝并报告
```

**新增章节 6**——Phase 3 失败应对（平台视频）：

```markdown
## 平台视频失败应对

yt-dlp 报错时不要盲目重试：

| 症状 | 应对 |
|------|------|
| "No video formats found" | 升级到最新版 yt-dlp（uv tool upgrade yt-dlp） |
| "Sign in to confirm you're not a bot" | YouTube 反爬，等 24h 或换 IP |
| "HTTP Error 429: Too Many Requests" | 触发速率限制，等 5-10 分钟 |
| Extractor 报错（具体平台） | 检查 https://github.com/yt-dlp/yt-dlp/issues 是否有已知问题 |
| 网络超时 | 尝试代理链（Phase 2.5） |

**不要**：反复重试同一命令。失败一次后升级工具或换代理。
```

**SKILL.md 结构总览（v0.2）**：
```
SKILL.md
├── 何时使用
├── 何时不用
├── 能力边界                     ← 新增
├── 触发方式
├── URL 到手后的第一件事：确定保存路径
├── 三条不可让渡的规则
├── 工作流（Phase 概览）
├── Phase 1 — 探测
├── Phase 2 — 工具检查
├── Phase 2.5 — 代理兜底          ← 新增
├── Phase 3.0 — 文件名冲突检查    ← 新增
├── Phase 3 — 执行下载
├── Phase 4 — 验证
├── Phase 5 — 回复
├── 网盘链接处理                   ← 新增
├── Magnet 链接处理                ← 新增
├── 平台视频失败应对               ← 新增
├── Pitfalls
├── 与旧 skill file-download 的关系
└── Verification
```

---

## Phase D — Windows 文档（0.5d）

**新增 `references/commands-windows.md`**：把 commands.md 的 6 个配方每个写一份 PowerShell 版：
- `curl.exe` 而非 `curl` alias
- `%USERPROFILE%\.local\bin` 而非 `$HOME/.local/bin`
- `%TEMP%` 而非 `/tmp`

**扩展 `references/tool-matrix.md` 的"Windows 特殊约定"节**：
- `curl.exe` vs `curl` 的坑
- PowerShell 里 `&` 调用外部程序的语法

**新增一节"Windows 代理配置"**：
- 环境变量设置：`setx HTTPS_PROXY http://127.0.0.1:7897`（永久）
- Clash 默认监听 7890，Hermes 建议 7897

**SKILL.md 补一行**："PowerShell 命令模板见 `references/commands-windows.md`"

---

## Phase E — 测试补齐（0.5d）

**现有 15 用例** + 新增 26 = **41 用例**：

| 类别 | 用例数 | 内容 |
|------|--------|------|
| detect.py 边界 | 8 | 空串、`file://`、`javascript:`、含凭证 URL、IPv6、超长 URL、emoji 路径、`%2e%2e%2f` 路径穿越 |
| dest_name 净化 | 5 | 路径分隔符、控制字符、超长名字截断、shell 元字符（`$&\|;<>`）、路径穿越 `..` |
| cloud_drive | 10 | 每个 host 一个用例（百度 2 / 夸克 1 / 阿里 2 / 115 2 / 天翼 1 / 微云 1 / 文库 1） |
| magnet | 2 | tool=none + user_action 非空；dn 参数解析 |
| torrent | 2 | tool=curl（非 aria2c）+ user_action 非空 |
| check_tools.py | 5 | mock `shutil.which` 三种 verdict、Windows PATH 扩展、缺失项 install_hint 字段完整性 |
| proxy_chain.py | 8 | 只有 env / env + config 去重 / 全链 / config 与 env 重复 / 只有 builtin / NO_PROXY 解析 / 空 proxy_chain / 非法 JSON 报错 |
| JSON 契约稳定性 | 3 | 固定字段 schema 断言（含 user_action / reason 字段） |

**总计**：15（原）+ 43（新增）= **58 用例**。

**运行**：
```bash
python -m unittest discover -s evals -v
```

---

## Phase F — 发布（0.25d）

**CHANGELOG.md v0.2.0 段**：

### Added
- `scripts/check_tools.py`：工具可用性检查（curl / yt-dlp / aria2c）
- `scripts/proxy_chain.py`：代理链解析（env → ~/.downrc → builtin）
- SKILL.md 代理兜底章节（Phase 2.5）
- SKILL.md 网盘/magnet 处理章节
- SKILL.md 能力边界章节（skill 不做什么）
- SKILL.md 平台视频失败应对
- `references/commands-windows.md`：PowerShell 命令模板
- `docs/PLAN-v0.2.md`：本文件
- `detect.py`：cloud_drive kind（10 个 host）

### Changed
- `detect.py`：`.torrent` 从 aria2c 改为 curl（只下种子文件本体）
- `detect.py`：magnet 从 aria2c 改为 none（skill 不处理 magnet 内容）
- `detect.py`：JSON 契约新增 `user_action` / `reason` 字段
- `detect.py`：`dest_name` 加完整路径净化（防 shell 注入 + 路径穿越）
- `detect.py`：`install_hint` 字段结构统一（`install_by_platform`）
- SKILL.md unknown 分支流程明确化
- SKILL.md 加 Phase 3.0 文件名冲突检查

### Fixed
- README 快速上手与 SKILL.md 语义冲突（"clarify 问保存路径" → "三级优先级"）
- README 目录树与文件系统不一致（缺 USAGE.md）
- CHANGELOG v0.1.0 段落与 [Unreleased] 状态矛盾
- `detect.py` dead imports（mimetypes, shlex）

### Design notes
- **skill 定位清晰**：只做文件下载，不做搜索、不做网盘下载、不拉 magnet 内容
- **代理链解析不发网络**——延续 detect.py 零网络原则
- `~/.downrc` 用 JSON 而非 TOML（stdlib 兼容 Python 3.9+）
- 内置默认代理链 3 个：7897 → 7890 → 192.168.31.135:7890
- `.torrent` 用 curl 而非 aria2c：依赖简化，用户手动下内容

---

## 提交序列（8 个 commit）

1. `docs: align README/CHANGELOG with SKILL.md v0.1.0`（Phase A1-A3）
2. `refactor(detect): unify install_hint schema and sanitize dest_name`（Phase A4-A6）
3. `feat(check_tools): add tool availability checker`（Phase B）
4. `feat(proxy_chain): add proxy chain resolver`（Phase B+'）
5. `feat(detect): add cloud_drive kind, redirect torrent→curl, magnet→none`（Phase B+"）
6. `docs(skill): add proxy fallback, cloud_drive, magnet, capability boundary`（Phase C）
7. `docs(references): add windows commands, proxy cheatsheet`（Phase D）
8. `test: expand coverage to 58 cases across detect/check_tools/proxy_chain`（Phase E）
9. `chore(release): bump to v0.2.0, update CHANGELOG`（Phase F）

---

## v0.3 展望（不做，但预告）

1. `~/.downrc` 支持 TOML（Python 3.11+ 用 `tomllib`，3.9+ 用降级 JSON）
2. `scripts/session_check.py`：扫 aria2 session 文件找未完成的下载
3. `scripts/install_hint.sh`：多平台 install 命令生成器
4. 多 profile 支持：不同 profile 有不同默认路径
5. `uvx down` 一键分发

**明确不进 v0.3**：
- probe_host.py（网络探测，D1 已否）
- download.py（下载执行器，D2 已否）
- headless browser 自动化（破坏 skill 定位）
