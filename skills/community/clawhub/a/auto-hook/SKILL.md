---
name: auto-hook
description: >
  检查指定 SKILL 是否存在偷懒、跳步、简化执行等问题，并确保该 SKILL 末尾附有自审计钩子（autohook）；
  也可撤销已注入的钩子，将 SKILL 恢复原样。
  支持 Claude Code、OpenAI Codex CLI、OpenClaw 三大智能体，自动适配 Linux / macOS / Windows 路径。
  【注入触发词】：「检查 XX skill 有没有偷懒」「审计 XX skill」「给 XX skill 加钩子」「XX skill 有没有 hook」
  「验证 XX skill 执行质量」「XX skill 是否规范」「帮我找 XX skill 在哪」。
  【撤销触发词】：「停止检查 XX skill」「不用检查了」「取消 hook」「删除钩子」「移除 XX skill 的自审计」
  「XX skill 去掉 autohook」「关掉审计」「撤销钩子」「还原 XX skill」。
  只要用户提到上述任意触发词，立即触发本 skill。
---

# auto hook  (v4 · 跨平台 + 钩子撤销)

本 SKILL 支持两种模式，根据用户意图自动判断：

**模式 A · 注入模式**（默认）：定位 + 注入钩子
1. **定位**：在当前智能体的标准路径中找到目标 SKILL.md
2. **读取钩子**：读取 `skill-audit-hook.txt` 的完整内容作为注入内容
3. **钩子注入**：检测末尾是否已有 autohook；若无则将文件内容追加到 SKILL.md 末尾

**模式 B · 撤销模式**：删除已注入的钩子，恢复 SKILL 原样
- 触发词含"停止/取消/删除/移除/关掉/撤销/还原/不用检查"等语义时自动切换
- 执行 Step R1–R4（见撤销流程章节）

---

## 附录 A · 各智能体 SKILL 路径速查表

> 本节供 Step 1 查找文件时参考，也可直接回答用户「skill 在哪里」的问题。

### A1 · Claude Code（Anthropic）

| 层级 | Linux / macOS | Windows |
|------|--------------|---------|
| **个人全局** | `~/.claude/skills/<n>/SKILL.md` | `%USERPROFILE%\.claude\skills\<n>\SKILL.md` |
| **项目级** | `.claude/skills/<n>/SKILL.md` | `.claude\skills\<n>\SKILL.md` |
| **插件内** | `<plugin-dir>/skills/<n>/SKILL.md` | 同左 |
| **托管企业** | 管理员通过 managed settings 下发 | 同左 |

优先级：项目级 > 个人全局 > 插件 > 内置捆绑。

> ⚠️ **Windows WSL 已知问题**：Claude Code 可能将 skill 写入 Windows 挂载的项目路径而非 Linux 用户路径。
> 修复：`mkdir -p ~/.claude/skills && cp -r .claude/skills/* ~/.claude/skills/`

### A2 · OpenAI Codex CLI

| 层级 | Linux / macOS | Windows |
|------|--------------|---------|
| **用户全局** | `~/.codex/skills/<n>/SKILL.md` | `%USERPROFILE%\.codex\skills\<n>\SKILL.md` |
| **项目级** | `.agents/skills/<n>/SKILL.md` | `.agents\skills\<n>\SKILL.md` |
| **系统级** | 管理员配置 | 同左 |

优先级：项目级 > 用户全局 > 系统 > 内置（`$skill-creator`、`$skill-installer`）。

禁用而不删除，在 `~/.codex/config.toml` 中：
```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

> ⚠️ **Windows 原生为实验性**，建议在 WSL workspace 内使用。
> Windows junction 替代 symlink：
> ```powershell
> New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
> cmd /c mklink /J "$env:USERPROFILE\.agents\skills\myskill" "$env:USERPROFILE\.codex\myskill\skills"
> ```

### A3 · OpenClaw

| 层级 | Linux / macOS | Windows |
|------|--------------|---------|
| **工作区级** | `<workspace>/skills/<n>/SKILL.md` | 需 WSL2（原生支持有限）|
| **用户全局** | `~/.openclaw/skills/<n>/SKILL.md` | `%USERPROFILE%\.openclaw\skills\<n>\SKILL.md` |
| **额外目录** | `skills.load.extraDirs` in `~/.openclaw/openclaw.json` | 同左 |
| **内置捆绑** | npm 包内随安装附带 | 同左 |

优先级：工作区级 > 用户全局 > extraDirs > 内置。

> ⚠️ **Windows 限制**：官方推荐优先使用 Mac 或 Linux；Windows 需通过 WSL2 运行。

### A4 · claude.ai / Cowork（本 SKILL 原生环境）

| 层级 | 路径（容器内） |
|------|--------------|
| 用户自定义 | `/mnt/skills/user/<n>/SKILL.md` |
| 官方公共 | `/mnt/skills/public/<n>/SKILL.md` |
| 示例 | `/mnt/skills/examples/<n>/SKILL.md` |

优先级：user > public > examples（均为只读，修改后需输出文件供用户替换）。

### A5 · 通用安装工具（skills.sh · Vercel 维护）

```bash
# 自动检测已安装智能体并路由到正确目录
npx skills add vercel-labs/agent-skills

# 只安装给指定智能体
npx skills add vercel-labs/agent-skills -a claude-code -a codex

# 搜索 skill
npx skills find "react testing"

# 更新所有已安装 skill
npx skills update
```

### A6 · 公共注册表速查

| 智能体 | 注册表 | 规模（2026-03）|
|--------|-------|---------------|
| Claude Code | claude.com/connectors | 官方 + 数千社区 |
| Codex CLI | developers.openai.com/codex/skills | 内置 + 社区 |
| OpenClaw | clawhub.ai | 13,700+ |
| 跨平台通用 | skills.sh（Vercel）| top skills 26,000+ installs |

---

## Step 1 · 定位目标 SKILL 文件

从用户消息中提取 SKILL 名称（如 `html-to-pptx`）。

**若当前环境为 claude.ai / Cowork**，执行：
```bash
find /mnt/skills -path "*/<n>/SKILL.md" 2>/dev/null
```
找不到时列出所有可用：
```bash
find /mnt/skills -name "SKILL.md" | sed 's|/SKILL.md||' | xargs -I{} basename {}
```

**若用户描述的是本地环境**，根据附录 A 对应智能体告知路径，指导用户手动定位，无需执行 bash。

找到后用 `view` **完整读取**（超 300 行必须 `view_range` 分段，不得截断）。

---

## Step 2 · 读取 skill-audit-hook.txt

必须读取该文件作为注入内容，不得使用任何内置默认文本替代：

```bash
find /mnt/user-data/uploads -name "skill-audit-hook.txt" 2>/dev/null
```

找到后立即用 `view` 工具读取完整内容，将其全文保存备用。

若**找不到**该文件，停止执行并告知用户：
```
❌ 未找到 skill-audit-hook.txt，请先上传该文件后重试。
```
不得继续后续步骤，不得使用任何替代内容。

---

---

## Step 3 · 钩子检查与注入

### 3a · 检测是否已有 autohook

在 SKILL.md 全文中搜索任意关键词：`自审计` / `autohook` / `审计钩子` / `debug.txt` / `❌ 和 ⏭️`

若找到：`✅ 已检测到 autohook（行 XX–XX），无需插入。` → 结束本步骤。

### 3b · 注入钩子

未找到钩子，执行注入（内容必须来自 Step 2 读取的 skill-audit-hook.txt）：

```bash
cp <原始路径> /home/claude/<n>-SKILL.md
```

```python
# Python 追加写入，确保内容完整无截断
with open('skill-audit-hook.txt', 'r') as f:
    hook = f.read()
with open('/home/claude/<n>-SKILL.md', 'a') as f:
    f.write('\n\n')
    f.write(hook)
print("钩子注入完成")
```

验证：
```bash
tail -20 /home/claude/<n>-SKILL.md
cp /home/claude/<n>-SKILL.md /mnt/user-data/outputs/<n>-SKILL.md
```

注入完成后调用 `present_files`，并告知用户按**附录 A 对应路径**替换原文件。

---

## Step 4 · 输出摘要

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SKILL 钩子报告 · <n>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【来源】skill-audit-hook.txt（已读取）
【钩子】✅ 已存在（行 XX）/ 🔧 已注入（请按附录A路径替换）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 注意事项

- `/mnt/skills/` 为只读；所有修改在 `/home/claude/` 完成后输出文件供用户替换
- 用户若描述本地环境，直接用附录 A 路径表回答，无需执行 bash
- 同时检查多个 SKILL 时，对每个依次执行 Step 1–5
- 钩子不重复注入：每次先做 4a 检测，有钩子则跳过 4b
- 钩子内容必须来自 skill-audit-hook.txt，不得使用内置默认文本

---

## 模式 B · 钩子撤销流程

> 触发条件：用户说「停止检查」「不用检查了」「取消 hook」「删除钩子」「移除自审计」
> 「关掉审计」「撤销钩子」「还原 XX skill」「去掉 autohook」等任意语义。

### Step R1 · 定位目标 SKILL 文件

与模式 A Step 1 相同：从用户消息提取 SKILL 名称，按附录 A 路径查找，完整读取文件。

若用户未指定具体 SKILL，询问：「请问要从哪个 SKILL 中移除钩子？」

### Step R2 · 定位钩子边界

在文件全文中搜索钩子起始标记（以下任意一个即为起始行）：

```
## ⚙️ 强制自审计
## ⚙️ 自审计钩子
---\n\n## ⚙️
```

同时搜索以下关键词确认是钩子内容（必须同时出现才判定为待删除区块）：
- `debug.txt`
- `Step 1 · 提取规则` 或 `Step 1 · 读取钩子文件`
- `❌ 和 ⏭️` 或 `❌ / ⏭️`

若**找不到**钩子标记：
```
⚠️ 未在 <n> 中检测到 autohook，无需操作。
```
结束流程。

### Step R3 · 删除钩子段落

**方式一（claude.ai 环境，bash 可用）**：

```bash
cp <原始路径> /home/claude/<n>-SKILL.md
```

用 Python 脚本精确删除，从钩子起始行（含前置 `---` 分隔线）到文件末尾：

```bash
python3 << 'PYEOF'
with open('/home/claude/<n>-SKILL.md', 'r') as f:
    lines = f.readlines()

# 找到钩子起始位置（向上包含最近一个 --- 分隔线）
hook_start = None
for i, line in enumerate(lines):
    if '强制自审计' in line or '自审计钩子' in line:
        # 向上找最近的 --- 分隔线
        for j in range(i-1, max(i-5, 0)-1, -1):
            if lines[j].strip() == '---':
                hook_start = j
                break
        if hook_start is None:
            hook_start = i
        break

if hook_start is not None:
    # 删除从 hook_start 到文件末尾，并去除末尾多余空行
    cleaned = lines[:hook_start]
    while cleaned and cleaned[-1].strip() == '':
        cleaned.pop()
    cleaned.append('\n')  # 保留一个末尾换行
    with open('/home/claude/<n>-SKILL.md', 'w') as f:
        f.writelines(cleaned)
    print(f"已删除第 {hook_start+1} 行起的钩子段落")
else:
    print("未找到钩子，无操作")
PYEOF
```

验证删除结果：
```bash
tail -15 /home/claude/<n>-SKILL.md
grep -n "自审计\|autohook\|debug.txt" /home/claude/<n>-SKILL.md && echo "⚠️ 仍有残留" || echo "✅ 钩子已清除"
```

**方式二（用户本地环境）**：

告知用户手动删除：打开 SKILL.md，找到包含 `## ⚙️ 强制自审计` 的段落（通常在文件末尾），
连同上方的 `---` 分隔线一起删除到文件结尾，保存即可。

### Step R4 · 输出与交付

```bash
cp /home/claude/<n>-SKILL.md /mnt/user-data/outputs/<n>-SKILL-clean.md
```

调用 `present_files` 提供下载，并告知用户：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  钩子撤销报告 · <n>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【操作】已删除 autohook（原第 XX 行起）
【文件】<n>-SKILL-clean.md（请按附录 A 路径替换原文件）
【状态】✅ SKILL 已恢复原样，不再触发自审计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
