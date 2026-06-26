# 数字人生成技能 (focusavatar)

命令行数字人生成工具，通过 **accessKeyId** 与 **accessKeySecret** 调用后端 API，输入 MP3 地址、MP4 地址和文字内容，生成数字人视频；支持提交任务与按 orderNo 查询结果。

---

## 目的与能力

- **目的**：在命令行或技能环境中，快速调用数字人视频生成服务，完成「音频 + 视频模板 + 文本」到合成视频的流程。
- **能力**：
  - 提交生成任务：传入 MP3/MP4 地址（本地路径或 URL）及合成文字，提交到后端并可选轮询结果。
  - 查询任务结果：凭任务单号 `orderNo` 查询状态与视频链接。
  - 不落盘处理：仅传递地址与文本给后端，不在本地存储用户媒体文件。
  - 交互式引导：分步输入、确认与重填，出错可追溯。

---

## 使用前必读：凭证（accessKeyId / accessKeySecret）

**安装完成后或首次使用前**，请先获取认证凭证：

1. **注册账号**：前往控制台（如 [https://login.joycoreai.com/](https://login.joycoreai.com/) 或部署方提供的地址）注册。
2. **购买/开通**：按需完成购买或开通流程。
3. **创建密钥**：在控制台创建密钥，复制 **accessKeyId** 和 **accessKeySecret**。

**使用方式**：

- **方式一**：运行脚本时按提示输入 accessKeyId、accessKeySecret。
- **方式二**：设置环境变量，免每次输入（将下面的 `你的accessKeyId`、`你的accessKeySecret` 替换为控制台复制的真实值）：

  **Windows（PowerShell，当前窗口有效）**：
  ```powershell
  $env:FOCUSAVATAR_ACCESS_KEY_ID = "你的accessKeyId"
  $env:FOCUSAVATAR_ACCESS_KEY_SECRET = "你的accessKeySecret"
  ```

  **Windows（CMD，当前窗口有效）**：
  ```cmd
  set FOCUSAVATAR_ACCESS_KEY_ID=你的accessKeyId
  set FOCUSAVATAR_ACCESS_KEY_SECRET=你的accessKeySecret
  ```

  **Windows（永久：用户环境变量）**：  
  设置 → 系统 → 关于 → 高级系统设置 → 环境变量 → 用户变量 → 新建：变量名 `FOCUSAVATAR_ACCESS_KEY_ID`，变量值填 accessKeyId；再新建 `FOCUSAVATAR_ACCESS_KEY_SECRET`，变量值填 accessKeySecret。

  **Linux / macOS（当前终端有效）**：
  ```bash
  export FOCUSAVATAR_ACCESS_KEY_ID="你的accessKeyId"
  export FOCUSAVATAR_ACCESS_KEY_SECRET="你的accessKeySecret"
  ```

  **Linux / macOS（永久）**：  
 将上面两行 `export` 写入 `~/.bashrc` 或 `~/.zshrc`，然后执行 `source ~/.bashrc` 或 `source ~/.zshrc`。

请求认证通过请求头传递：`X-Access-Key-Id`、`X-Access-Key-Secret`。本工具不保存、不上传凭证到除后端 API 以外的任何地方。

---

## 功能特性

- ✅ 使用前引导至指定地址获取 accessKeyId / accessKeySecret
- ✅ **两种模式**：**提交任务**（走 focusavatar 原流程）/ **查询任务结果**（需提供 orderNo）
- ✅ 分步引导输入：MP3 地址 → MP4 地址 → 文字内容
- ✅ 用户确认：可选择提交或重新输入
- ✅ 不下载文件：直接将地址传给后端处理，节省空间
- ✅ 进度显示：自动增长到 99% 后等待后端返回结果
- ✅ 轮询机制：异步任务自动轮询状态
- ✅ 一键输出：生成完成直接返回视频链接
- ✅ 任务完成后可凭 orderNo 通过「查询任务结果」再次查询
- ⏱️ **需等待超时说明**：**提交任务（生成视频）** 需等待后端处理，通常约 **5–10 分钟**；若由 OpenClaw/助手等执行，建议将超时时间设为 **600 秒（10 分钟）** 以上，避免中途被中断。

---

## 搜索关键词

focusavatar, 数字人, 数字人生成, AI数字人, 视频生成, ai视频, 语音合成, 唇形同步

---

## 安装

通过 OpenClaw Skills 安装（示例，仓库地址以实际为准）：

```bash
npx skills add https://github.com/lintqiu/focusavatar -s focusavatar -y 下载安装
```

**首次安装完成后**：使用前请先前往指定地址获取 **accessKeyId** 与 **accessKeySecret**，否则无法调用接口。  
→ 控制台地址（注册 → 购买/开通 → 创建密钥）：**[https://login.joycoreai.com/](https://login.joycoreai.com/)** 或部署方提供的同等地址。  
获取后可在下方「体验操作流程」中按提示输入，或设置环境变量免输入。

安装后通过技能入口使用即可。

---

## 体验操作流程（使用技能时）

使用技能后，按以下步骤完成**一次完整体验**：

| 步骤 | 说明 |
|------|------|
| **① 设置凭证** | **自动**：若已设置环境变量 `FOCUSAVATAR_ACCESS_KEY_ID`、`FOCUSAVATAR_ACCESS_KEY_SECRET`，无需输入。<br>**一步一步**：未设置时，按提示依次输入 **accessKeyId**、**accessKeySecret**（从控制台复制）。 |
| **② 选择模式** | **两种模式**：<br>• **[1] 提交任务（生成视频）**：走 focusavatar 原流程，后续需输入 MP3、MP4、文字。<br>• **[2] 查询任务结果**：需提供任务单号 **orderNo**，仅查询状态与视频链接。 |
| **③ 设置 MP3 地址** | 仅在选择「提交任务」时出现。一步输入 **MP3 路径或 URL**。 |
| **④ 设置 MP4 地址** | 上一步完成后，一步输入 **MP4 路径或 URL**。 |
| **⑤ 设置文字内容** | 一步输入 **需要合成的文字内容**。 |
| **⑥ 确认并提交** | 确认 MP3、MP4、文字无误后选择「提交」；提交后等待生成（约 5–10 分钟），完成后输出视频链接。若选「查询任务结果」，输入 orderNo 后即返回状态与链接。 |

**简要顺序**：凭证（①）→ 选模式（②）→ 若提交任务则依次：MP3（③）→ MP4（④）→ 文字（⑤）→ 确认提交（⑥）；若查询则输入 orderNo 即可。

---

## 安装机制

**1. 通过 OpenClaw Skills 安装到本地**

- 前置条件：本机已安装 **Node.js**（含 npm），以便使用 `npx`。未安装可前往 [https://nodejs.org/](https://nodejs.org/) 下载安装。
- 在终端中执行（将 `https://github.com/lintqiu/focusavatar` 替换为实际技能仓库地址，例如 `https://github.com/lintqiu/focusavatar`）：
  ```bash
  npx skills add https://github.com/lintqiu/focusavatar -s focusavatar -y 下载安装
  ```
- 参数说明：`-s focusavatar` 为技能名称，`-g` 表示按全局/规范安装，`-y` 表示默认确认、非交互。
- 安装完成后，技能会出现在 OpenClaw 的本地技能目录（具体路径由 OpenClaw 约定，如用户目录下的 `.openclaw/workspace/skills/focusavatar`）。

**2. 运行环境与依赖**

- **Python**：需要 **Python 3.6 及以上**。  
  - 检查版本：终端执行 `python3 --version` 或 `python --version`。  
  - 未安装时请从 [https://www.python.org/downloads/](https://www.python.org/downloads/) 安装；Windows 安装时建议勾选「Add Python to PATH」。
- **requests**：必须安装该库，否则无法发起 HTTP 请求。  
  - Linux / macOS：`pip3 install requests` 或 `python3 -m pip install requests`  
  - Windows：`pip install requests` 或 `py -m pip install requests`  
  - 若使用虚拟环境，请在对应环境中执行上述命令。

**3. 权限与网络**

- **无需系统级或 root/管理员权限**：以当前登录用户安装和运行即可，不需要以管理员或 root 执行。
- **需要网络访问**：本技能会访问由环境变量 `FOCUSAVATAR_API` 指定的后端地址（未设置时使用默认地址）。请确保本机能够访问该地址（防火墙、代理等允许出站访问）。

---

## 使用

通过技能入口启动后，先完成 **① 设置凭证**（见上方「体验操作流程」），再 **② 选择模式**：

- **[1] 提交任务（生成视频）**：按顺序 **③ MP3 地址 → ④ MP4 地址 → ⑤ 文字内容**，确认后提交；支持轮询直至完成并输出视频链接。
- **[2] 查询任务结果**：输入任务单号 `orderNo`，即可获取状态与视频链接。

详细步骤见 **「体验操作流程（使用技能时）」** 小节。

---

## 后端 API 协议

**BASE_URL**：由环境变量 `FOCUSAVATAR_API` 指定，默认示例：`https://yunji.focus-jd.cn`。

**认证**：请求头  
`X-Access-Key-Id`、`X-Access-Key-Secret`。

**提交接口**

- `POST {BASE_URL}/skill/api/submit`
- Body (JSON)：`{ "mp3": "地址/URL", "mp4": "地址/URL", "text": "合成文字" }`
- 返回：直接完成时 `{"videoUrl": "..."}`；异步时 `{"orderNo": "任务单号"}`，需轮询查询接口。

**查询结果接口**

- `POST {BASE_URL}/skill/api/api/result`
- Body (JSON)：`{ "orderNo": "任务单号" }`
- 返回：JSON，含 `status`（如 done/error）、`progress`、`videoUrl`、`message` 等。

---

## 隐私说明

- **数据归属**：本工具仅作为客户端调用方，**不存储、不收集**用户的 MP3/MP4 地址、文字内容或生成的视频。
- **请求流向**：所有请求直接发往用户配置的后端服务（如 `FOCUSAVATAR_API`），数据处理与存储由该后端及所属方负责。
- **凭证**：accessKeyId、accessKeySecret 仅用于当次请求的请求头，不写入磁盘、不上传到本技能仓库或第三方。
- **合规**：用户需自行确保所提交内容符合当地法律法规，不侵犯第三方知识产权及其他权益。

---

## 坚持与特权

- **坚持（Persistence）**：本技能不持久化用户数据；凭证可通过环境变量在会话间复用，由用户自行管理。
- **特权（Privileges）**：无需 root 或系统级权限；需要网络访问以调用后端 API；若通过 OpenClaw/助手运行，建议对「提交任务」设置较长超时（如 600 秒），因生成可能需数分钟。

---

## 依赖

- Python 3.6+
- `requests`：`pip install requests`

---

## 许可证

MIT