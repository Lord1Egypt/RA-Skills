# 安装到任意机器 / 任意智能体

本包不需要安装器，**拷贝目录 + 装 4 个 Python 依赖**即可。
包内不含 cookie、不含密钥、不含任何个人路径——登录态由使用者在本机扫码产生。

---

## 0. 前置条件

| 项 | 要求 | 备注 |
|:--|:--|:--|
| Python | 3.9+ | 只用标准库 + 2 个第三方包 |
| 浏览器 | Google Chrome / Chromium / Edge（任一 Chromium 内核） | 需要支持 `--remote-debugging-port` |
| ffmpeg | 可选 | 只有「视频规格核对」需要（ffprobe 探宽高/时长/帧率/音轨） |
| 操作系统 | Windows / macOS / Linux | Chrome 路径自动探测；探测不到用 `DOUBAO_CHROME` 指定 |

```bash
pip install -r requirements.txt
# websocket-client  pillow
```

---

## 1. 装法 A：通用智能体框架（原生 skill）

把本目录整个拷到 通用智能体框架 的 skills 目录下：

```bash
# 默认 profile
cp -r doubao-account-pool "<你的智能体框架>/skills/"
# 指定 profile（Windows）
cp -r doubao-account-pool "<你的智能体框架>/skills/"
```

之后该 profile 的智能体在相关任务里会自动加载 `SKILL.md`。
不需要重启网关——技能是每轮按需读取的。

**验证**：
```bash
cd "<你的智能体框架>/skills/doubao-account-pool/scripts"
python doubao_cli.py doctor
```

---

## 2. 装法 B：裸脚本（任何环境、任何智能体）

不装成 skill，直接把 `scripts/` 当工具目录用：

```bash
export DOUBAO_HOME="$HOME/.doubao_studio"      # 状态目录：实例 profile + 产出
export DOUBAO_CHROME="/path/to/chrome"       # 不设则自动探测
export DOUBAO_FFMPEG="/path/to/ffmpeg"       # 可选
cd doubao-account-pool/scripts
python doubao_cli.py doctor
python doubao_cli.py up 1
python doubao_cli.py login 1
```

写进 shell profile 或 `.env` 都行。**`DOUBAO_HOME` 是唯一必须记住的变量**——
所有实例登录态都在它下面，备份它 = 备份所有账号登录状态（**别提交到 git**）。

---

## 3. 装法 C：其他 Agent 框架（Claude Code / Codex / 自研）

### C-1 提示词型框架（Claude Code、Codex、Cursor、Gemini CLI…）
把 `SKILL.md` 的内容作为项目的规则文件（`CLAUDE.md` / `AGENTS.md` / `.cursorrules`）挂上，
再告诉它：**执行一律通过 `scripts/doubao_cli.py <子命令>`，只读 `@@` 开头的输出行**。

### C-2 function calling / MCP（自研 Agent）
`doubao_cli.py` 的每个子命令就是一个天然工具：

```json
{
  "name": "doubao_studio",
  "description": "操控豆包网页版多实例工作台。所有命令只返回 @@ 开头的结构化短行。",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {"type": "string", "enum": ["doctor","status","up","down","login","check","nick","selfcheck","visible","ask","img","img-batch","vid","vid-regrab","fetch","trim"]},
      "args": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["command"]
  }
}
```

执行：`subprocess.run([python, "doubao_cli.py", command, *args])` → 把 stdout 里的 `@@` 行回给模型。
**不要把整段 stdout 全灌进上下文**——`@@` 短行才是给模型看的，其余是给人排障的。

### C-3 多智能体协作（一个调度方 + 多个执行方）
1. 调度方（主脑）先 `status` 看实例，再按实例切分任务；
2. 任务书里写死「**只准用分给你的实例，禁止 up、禁止 down、禁止整屏截图、禁止 dump DOM**」；
3. 执行方只回 `@@` 短行 + 自己的产物路径；
4. 全部结束后，**调度方统一 `down --all`**。

---

## 4. 首次运行检查清单

```bash
python doubao_cli.py doctor            # ① Chrome / ffmpeg / 依赖 / 状态目录
python doubao_cli.py status            # ② 应逐实例输出 @@SLOT n port=... alive=YES/no logged=...
python doubao_cli.py up 1              # ③ 起一个实例（应见 @@UP slot=1 port=... 与 @@READY）
python doubao_cli.py visible 1           # ④ 修可见性（窗口几何在配置里设）
python doubao_cli.py login 1           # ⑤ 出二维码 PNG → 手机扫
python doubao_cli.py check 1           # ⑥ 登录态三重校验
python doubao_cli.py down 1            # ⑦ **收尾，别让它挂着**
```

✅ 七步全过 = 环境就绪。
❌ `doctor` 报「未找到 Chrome」→ 设 `DOUBAO_CHROME` 指向可执行文件。
❌ `up` 超时 → 换 `DOUBAO_PORT_BASE`（可能被占用）。

---

## 5. 常见问题

| 症状 | 原因 | 处置 |
|:--|:--|:--|
| 提示词注入了但点发送无效 | 标签页 `visibilityState=hidden`（后台标签） | 用 `visible N on ...` 把窗口挪回屏内露出 ≥100×100 |
| `outerWidth/outerHeight = 0` | 窗口被挪到屏幕外，自动化特征极明显 | 同上，改用「屏内露一小块」而不是挪出屏 |
| 注入成功、豆包一个字不回 | 基础用量耗尽（静默拒答） | 换实例；连续多实例全静默才判用量见底 |
| 图片取到的是旧图 | 没做基线闸 | 本包 `img` 已内置：投喂前记基线，数量不增长一律判失败 |
| 不同文件名 md5 相同 | 静默失效（抓到同一张） | 整批结果不可信，先修链路再谈质检 |
| 二维码扫不上 | 过期码 / 整屏截图被压缩 | 取码后查「二维码失效」，且只发裁切放大的单张图 |
| 生成卡住或页面脏了 | 上一轮遗留状态 | `down N` 再 `up N` 回干净状态，别在脏页面反复盲试 |
| `down` 返回码 0 但实例没关掉（stderr 有 `UnicodeDecodeError` / `_readerthread`） | 中文 Windows + `PYTHONUTF8=1`：`powershell`/`taskkill` 输出是 GBK，被按 UTF-8 解码，异常在子线程里被吞掉 | 已在本包修复（所有 `subprocess.run` 显式带 `encoding='utf-8', errors='replace'`）。**如果你自己扩了调用，照抄这个参数** |
| 改了代码但"验证"却显示正常 | `__pycache__` 里的旧字节码把错误盖住了 | 验证前清 `__pycache__`，或全程 `export PYTHONDONTWRITEBYTECODE=1` |

---

## 6. 卸载 / 清理

```bash
python doubao_cli.py down --all          # 先关掉所有实例
rm -rf "$DOUBAO_HOME"                    # 删除状态目录 = 删除所有账号登录态
rm -rf doubao-account-pool               # 删除工具本身
```

⚠️ 删 `DOUBAO_HOME` 前想清楚：里面是每个账号的浏览器 profile，删了要重新扫码。
