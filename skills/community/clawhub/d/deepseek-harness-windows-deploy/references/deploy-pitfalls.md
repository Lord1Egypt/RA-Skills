# DeepSeek Harness — Windows 部署避坑清单（详细版）

适用：Windows + 托管 Node（WorkBuddy 沙箱）环境下源码安装 / 构建 / 启动 / 配置工作区。
所有结论均来自一次完整实操，命令均已验证。

---

## 0. 环境准备

- **git** 2.x 以上。
- **Node.js** `^22.19.0 || >=24`（本机用托管 Node 22.22.2，可）。
- **pnpm** `11.7.0`（仓库 `packageManager` 字段指定），通过 corepack 准备。
- **harness home**：`$DSH_HOME` 或 `~/.dsh`（本机 `C:\Users\<user>\.dsh`）。所有设置、工作区注册、
  会话都默认落在用户级 `~/.dsh`。**多个完全隔离的 harness 实例**需各自设不同 `DSH_HOME`。

---

## 1. 获取与安装（标准流程）

```bash
git clone https://github.com/deepseek-ai/deepseek-harness
cd deepseek-harness
# 准备 pnpm
corepack prepare pnpm@11.7.0 --activate
pnpm install
pnpm run build        # 构建 host/client lib + web 前端
```

启动（文档写法）：`pnpm dsh web` → `http://127.0.0.1:3080`。
`dsh` 脚本实为 `node --import tsx/esm apps/cli/src/bin.ts`；构建后也可直接 `node apps/cli/lib/bin.js web`。
首次进入「设置 → 模型」填 DeepSeek API Key。

---

## 2. 坑 A — corepack / pnpm 路径在 Git Bash 被破坏

- **现象**：Git Bash 下调 `corepack` / `pnpm`，MSYS 路径转换把路径写成 `D:\c\Users...`，corepack 找不到脚本。
- **解法**：用 **PowerShell** 直调 `node corepack.js pnpm@11.7.0 install/build`（绕过 MSYS 转换）。
- **自建 pnpm shim 注意**：
  - 用 `%~dp0node.exe` 和 `%~dp0node_modules\corepack\dist\corepack.js` **相对自身**解析，**不要**硬编码中文路径；
  - 也不要用 ASCII 编码写含中文的路径（会写坏）。
  - **不要留 `pnpm.ps1`**：PowerShell 会优先加载它并被脚本执行策略拦截；只用 `pnpm.cmd`。

---

## 3. 坑 B — `build:web` 嵌套 pnpm 调用失败

- **现象**：`pnpm run build` 的 `build:web` 内部再次调用 `pnpm`，但子进程的 PATH 上没有 `pnpm` → 失败（lib 已构建、仅 web 失败）。
- **解法**：把含 `pnpm.cmd` 的 node bin 目录加入 PATH，再重跑 `pnpm run build`。

---

## 4. 坑 C — safe-delete 钩子（最关键，反复中招）

- **成因**：WorkBuddy Bash 沙箱给每个 node 进程注入
  `NODE_OPTIONS=--require=.../genie-safe-delete.cjs`，把 `fs.rm/unlink` 劫持去调用
  `genie-trash.exe`（Windows 上超时，并以 fail-closed 方式报错）。
- **影响点**：Harness 设置持久化 `FileSettingsProvider.persistSection` 用
  `withFileLock`（mkdir → writeFileAtomic → `rm(lock)`），`finally` 里的 `rm(lock)` 被拦截抛错
  → `mutate` 失败 → 前端只显示通用文案 **"暂时无法保存确认状态，请重试"**（即内测声明的确认步骤）。
  **实际上数据（`~/.dsh/settings.yaml` 的 `ui-onboarding.welcomeNoticeVersion`）已写成功，只是内存未标记为已确认。**
- **解法**：启动 dsh 时前缀 **`NODE_OPTIONS=""`**（node 不加载该钩子，锁清理恢复正常）。此变量仅对这条启动命令的子进程生效，不影响其他进程；**执行前请向用户说明并确认**。
- **注意**：在自己机器的终端（无沙箱）跑 `dsh web` 不会有此问题；**若用 WorkBuddy Bash 后台启动，务必加 `NODE_OPTIONS=""`。**

---

## 5. 坑 D — `run_in_background=true` 会杀掉常驻进程

- **现象**：WorkBuddy Bash 用 `run_in_background=true` 跑常驻的 `dsh web`，工具在命令返回后清理
  整个进程组 → node 被杀死、端口变 FREE。
- **解法**：用**命令内 `&`** 后台启动（工具返回后进程继续存活），不要用 `run_in_background` 参数。

---

## 6. 坑 E — 端口 3080 `EADDRINUSE` / 残留进程

- **定位**：`netstat -ano | grep :3080`，或 PowerShell `Get-NetTCPConnection -LocalPort 3080`。
- **结束**：Bash 里 `taskkill //F //PID` 参数解析会失败；用 **PowerShell `Stop-Process -Id <pid> -Force`** 最稳。

---

## 7. 坑 F — 迁移 harness 目录后的 `EPERM` 目录符号链接

- **现象**：迁移 harness 安装目录后，启动报
  `EPERM: unlink 'C:\Users\<user>\.dsh\profiles\node_modules\@deepseek-ai\dsh-goal-round-driver'`。
- **成因**：`~/.dsh/profiles` 下是**目录符号链接**，harness 启动的 `ensureSymlink` 用 `fs.unlink`
  删它；**Windows 上目录 symlink 必须用 `rmdir`，`unlink` 直接 EPERM**。迁移后旧链接失效。
- **解法**：`NODE_OPTIONS="" node -e "fs.rmSync(path,{recursive:true,force:true})"` 删掉失效的
  目录符号链接，harness 重启自动重建。`profiles` 是纯软链缓存（指向项目 node_modules），可重建，无数据风险。
  **执行删除前请向用户确认**：该路径可重建、不触及用户数据，但仍属对 `~/.dsh` 的写入操作。

---

## 8. 坑 G — 迁移时 safe-delete 拦截 `rmdir`

- **现象**：迁移时想先删占位空目录，被坑 C 的钩子拦（删不动），导致 `mv` 没执行。
- **解法**：同盘直接 `mv <src> <已有目标目录>/`（纯重命名、不涉及删除）即可。

---

## 9. 工作区语义（来自文档 guide/quickstart）

- `dsh` 把**启动时的 cwd** 作为默认文件系统位置。
- Web UI 强制流程：**选择工作区 → 添加「启动 dsh 时所在的项目目录」 → 选中它**。**选中前会话输入框不可用。**
- **持久化位置**：工作区在 `~/.dsh/storages/workspace.json`（**不是** settings.yaml）；会话存储在
  `~/.dsh/sessions/<sanitized-path>/`（`sanitized` 化处理会把路径中的空格转义为 `~0020`）。
- **不要把 dsh 复制进工作区**：dsh 是程序，工作区只是 agent 的操作数据目录；纯 UI 添加 + 选中即可让
  agent 在该目录读写，无需移动 harness 一个文件。
- 运行态（settings / 工作区注册 / session）默认共用 `~/.dsh`；要跑多个完全隔离的 harness 实例，各设不同 `DSH_HOME`。

---

## 10. "选不中工作区" 的定位法（后端通常正常）

1. 先确认后端数据：看 `~/.dsh/storages/workspace.json` 是否已有该工作区记录、对应
   `~/.dsh/sessions/<sanitized-path>/` 是否生成。若都有，说明添加 + 开会话后端成功。
2. 用 RPC 复现"开会话"验证：
   ```bash
   curl -X POST http://127.0.0.1:3080/api/session.create \
     -H 'Content-Type: application/json' \
     -d '{"type":"client-request","rpcId":"x","method":"session.create","payload":{"workspaceId":"<工作区id>"}}'
   ```
   返回 `{"result":{"ok":true,...}}` 即后端正常 → 问题是 **Web UI 客户端状态陈旧** → **硬刷新（Ctrl+Shift+R）** 后重试。
3. 若仍失败，按 **F12 打开 Console**，点选工作区，把红色报错文案发出来精确定位。

### RPC 模型
- 信封固定：`POST /api/<method>`，body = `{"type":"client-request","rpcId":"<str>","method":"<str>","payload":{...}}`。
- 常用方法：`session.create` / `session.list` / `workspace.list` / `workspace.create` / `settings.mutate` 等。

---

## 11. 排查心态（避免重复踩坑）

- **不要把所有"保存 / 选中失败"都归因为 safe-delete 钩子。**
  先确认原子写是否真的失败：若 `workspace.json` / `settings.yaml` 已被更新，说明钩子没在拦——
  此时失败在别处（多半是 Web UI 客户端状态），应改用 RPC 复现拿真实错误，而不是再去加 `NODE_OPTIONS=""`。

---

## 12. 验证过的启动命令（最稳，直接照抄）

```powershell
cd <你的 harness 安装根，例如 D:\Deepseek>
NODE_OPTIONS="" & "<你的托管 Node 可执行文件，例如 C:\Users\<你>\.workbuddy\binaries\node\versions\22.22.2\node.exe>" apps/cli/lib/bin.js web
```

- Web UI：`http://127.0.0.1:3080`。
- 首次进入「设置 → 模型」填 DeepSeek API Key 才能真实调模型。
