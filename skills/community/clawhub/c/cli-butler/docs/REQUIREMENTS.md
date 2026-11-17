# cli-butler 需求清单

> 本文档为项目唯一需求真相源，誊自 2026-11-09 已批准计划（调研会话产出）。
> 线上搜证结论与差异化依据见文末「背景搜证」。

## 目标

做一个可开源的 skill：**让任意 agent 具备管理本地 CLI 工具的能力**。纯 bash 零第三方依赖，macOS/Linux（Windows 非 MVP）。

## 名字

`cli-butler`（备选 toolbutler）。**发布前须查重**：npm / GitHub / skills.sh。

## 核心概念——来源（provenance）

每个 CLI 归属一个安装渠道，渠道决定装/卸/升级路由：

```
brew | npm -g | pnpm -g | pipx | uv tool | cargo | gem | apt(dnf/pacman) | manual
```

- 渠道管理项：从包管理器自身查询（版本、路径、升级状态）。
- `manual`（PATH 上散装二进制）：由本 skill 记账——journal 文件记录安装来源与时间。
- 详见 [provenance.md](provenance.md)。

## 功能（六项，实现顺序 F1→F5→F6→F3→F4→F2）

### F1 list — CLI 列表（分组盘点）
逐渠道枚举：`brew list --formula/-cask`、`npm ls -g --depth=0`、`pipx list`、`uv tool list`、`cargo install --list`、`gem list`、`apt --installed`（抽样）、PATH 上无主二进制。按二进制名去重合并：版本、渠道、路径、占用（du）。

**分组输出**：按渠道分组（brew / npm -g / … / system / manual），组头含渠道一句话说明与包数，让用户知道哪个组有什么 CLI、每个 CLI 是干嘛的；manual 组细分 `manual`（journal 有账）与 `untracked`（无主）。

**用途（desc）**：每个 CLI 附一句话用途，只做本地查询：渠道原生元数据优先（`brew desc`、全局 node_modules 的 package.json description、dpkg Summary、`gem list -d` 等），缺失回退 `whatis`；禁止逐包联网，查不到留空。

**system 组（系统自带）**：macOS SIP 保护前缀（`/usr/bin` `/bin` `/sbin` `/usr/sbin`）下的 CLI 单列 system 组，显式标注「系统自带，不可卸载」；Linux 下这些路径通常由发行版包管理器管理，归对应渠道，不进 system 组（口径见 provenance.md）。

输出：人读分组表格 + key=value 机器行（字段含 `category=managed|manual|untracked|system`、`desc=`）。

### F5 refchain — 引用链
`refchain <cli>` 输出五层：
1. 二进制 realpath 与软链链
2. 归属渠道凭据
3. PATH 定义行（~/.zshrc 等 shell 配置中谁把它放进 PATH）
4. launchd / cron 引用
5. 常见配置目录 grep 引用（~/.ssh/config、~/.gitconfig 等）

判活辅助：解析 `~/.zsh_history` 扩展格式 `: <epoch>:0;cmd` 报 last-used；bash 历史无时间戳时回退文件 mtime。**mtime 不可信规则**：批量同步会集体刷新 mtime，只信历史时间戳。

### F6 cap — 功能枚举
`cap <cli>`：试 `--help`/`-h`/`help`，提取顶层子命令与 usage 行；解析失败返回原文首段。

### F3 install — 安装
探测 OS 与可用渠道 → 按 CLI 选渠道（node 工具走 npm、系统工具走 brew/apt）→ 执行并回写 journal。网络约束内置：检测本机代理（有 `webget` 用之，无则显式提示代理变量）；npm -g 防 PATH 劫持（检查 prefix）。

### F4 uninstall — 卸载
路由归属渠道卸载；manual 项走 refchain 检查 → **默认 dry-run** → 显式确认 → 删除 + 残留清扫（dotfiles、launchd plist、软链）。

红线：
- **system（系统自带）项一律拒绝卸载**：直接说明不可卸载及原因（SIP/系统完整性），不进 dry-run 流程。
- **绝不对渠道管理的二进制直接 `rm`**——必须经归属渠道卸载。
- launchd 服务停用：须挪走 plist（而非只 `launchctl bootout`，bootout 只注销当前会话——dsh 教训）。
- app 内嵌软链（OrbStack 型，如 /usr/local/bin/docker → app 内 docker-tools）：只备份挪链（`.bak`），不删本体。

### F2 manage — 单项管理与升级
`info <cli>`：真实路径、软链链路、归属渠道、大小、launchd 引用。
`outdated` / `upgrade <cli>`：路由归属渠道执行；渠道不可用时明确报错，不猜。

## 非目标

- 注册表搜索与 skill 管理（find-skills / dbs-install-skill 已覆盖）
- GUI
- Windows 原生支持（CI 只测 POSIX）
- 替代包管理器本身（只做路由与追踪）

## 技术约束

- SKILL.md + `bin/*.sh` + `lib/common.sh`；POSIX bash，零第三方依赖（无 jq 时降级纯文本输出）
- SKILL.md 英文（开源规范），frontmatter description 触发词覆盖：install/uninstall/upgrade CLI、what CLI tools installed、CLI reference chain、CLI capabilities
- 渠道探测逐项容错：单渠道命令缺失/超时不阻塞整体
- tests：`tests/fixtures/` 造假渠道输出与假 PATH；GitHub Actions 跑 shellcheck + 冒烟

## 验收标准

- F1 对数本机真实数据：docker（OrbStack 软链）、node/nvm、dsh 残留（.off plist）、homebrew 包
- F5 对已知案例验证五层输出：/usr/local/bin/docker 软链链、launchd 引用（ai.deepseek.dsh.web.plist.off）
- F4 dry-run 对渠道管理项与 manual 项分别验证路由与确认流
- CI 绿：shellcheck + fixtures 冒烟

## 背景搜证（2026-11-09）

- skills.sh 注册表（`npx skills find`）与 GitHub：**无对口现成方案**。注册表只有单域技能（homebrew-formula-maintenance 366 installs、uv-package-manager 15.7K、install-android-cli-tools 等）。
- GitHub 命中的均为「skill 包管理器」（ai-agent-skills 1156★、OpenPackage 615★、kasetto 216★），管理对象是 skill 不是 CLI，方向不对口。
- 差异化：skill 形态（agent 自主操作、零安装门槛）+ 跨包管理器 + 来源追踪与引用链。
