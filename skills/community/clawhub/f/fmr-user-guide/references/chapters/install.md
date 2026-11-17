# 安装 Free Model Router（FMR）

## 进入条件

- 状态前置：探针 P1 判定**未安装态**——环境变量路径（`FMR_DATA_DIR`/`FMR_ROOT_DIR`）与本用户默认路径均无数据目录，**且连接层反证无应答**（发现跨用户/异位置实例时不进本章，按 SKILL.md 该分支处置：用现有实例或停旧重装）。
- 意图话术："帮我装 FMR""部署免费模型路由"；未装状态下的任何使用请求（先安装，再回到用户原本的意图）。

## 流程

### 1. 前置检查

- 操作系统：Windows / Linux / macOS 均支持；无 systemd 的环境（容器、WSL）走 crontab `@reboot` 兜底。
- Node：Linux/macOS 需 Node ≥14（一键脚本检测不足时可代装至 v20）；Windows 便携包内嵌 node.exe，免装。
- 端口 5678 空闲（或改绑后的配置端口；占用时的陷阱见第 3 步）。

### 2. 执行安装

现行分发物 = 全平台便携 zip（win/linux/darwin × x64/arm64）+ 一键脚本，从 OSS latest 键下载：

- Linux / macOS：

  ```
  curl -sSL https://freemodel.eu.org/install.sh | bash
  ```

- Windows（PowerShell）：

  ```
  iwr https://freemodel.eu.org/install.ps1 | iex
  ```

- 指定版本/回退：`--package <url|本地zip>`（bash）/ `-PackageUrl`（PowerShell）。

exe 安装器已停发：用户引用 setup.exe 类文档（如包内 DEPLOYMENT-USER.md 的 exe 章节）时，说明该渠道已停发，改用上述脚本。npm 上没有 FMR 包。Linux 权限：执行账号需有 sudo，但整脚本不加 sudo（脚本内部自行提权）。

装完的界面 = `/admin` 面板 + 本机 REST——**便携包内没有 CLI**（`scripts/` 不随包分发）；若用户提到 CLI 命令，那是 Skill 形态的产物，见 migrate 章背景。

### 3. 端口占用陷阱

5678 被占时，新进程因端口冲突直接退出，但安装器的就绪轮询可能拿到**旧进程的 200 应答**而误报"安装成功"。因此完成判定只认下方完成判据，不接受脚本"安装成功"的自述输出。

### 4. 确认持久面

安装完成后 FMR 由平台服务面管理（同 SKILL.md 平台拉起面）：

- Linux：`systemctl --user status free-model-router.service`（或系统级）
- macOS：`launchctl list | grep free-model-router`
- Windows：管理员 `schtasks /query /tn FreeModelRouter`；非管理员查启动文件夹内的隐藏启动项

## 完成判据（全部机器观测，不接受 CLI/脚本自述）

1. P1 通过：数据目录存在；
2. P2 通过：5678 有 HTTP 应答——`/healthz` 返回 200 为准；所装版本若无此端点，以 `/api/status`、`/v1/models` 等任一已知状态端点应答为准（判定走 SKILL.md 证据层级）；
3. `current` 指针存在，且其指向版本目录根的 `package.json` 版本 = 所装 zip 根 `package.json` 版本；
4. 平台服务面查询在位（上方 systemctl / launchctl / schtasks 之一有结果；用户级与系统级都查）。

四条全过才算装完。卸载语义预告：standalone 卸载脚本**默认连数据目录一起删除**，保数据须加 `-k`/`-KeepData`（详见 upgrade 章）。

## 收尾：能力速览一屏

完成判据全过后，主动附**能力速览一屏**——按 `${CLAUDE_SKILL_DIR}/references/chapters/capabilities.md` 的"一屏速览"形态输出：装完即正常态，走 `/api/features` 主通道；Router 未起则按其降级分支。这一屏回答用户接下来最自然的问题——"装好了，它能干什么"。

## 禁则

- 不推荐 exe 安装器。
- 安装过程中不展开隧道/跨机话题（用户问起 → access 章）。
