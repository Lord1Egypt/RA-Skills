---
name: flomo-to-obsidian
description: Parse and sync flomo exported HTML data to Obsidian vault with attachment support. Supports one-time manual export conversion and automatic sync. Use when users want to import flomo notes, convert flomo to markdown, or set up automatic sync.
cn_name: Flomo到Obsidian同步工具
cn_description: 将 flomo 笔记同步到 Obsidian，支持单次手动转换和自动同步。当用户想导入 flomo 笔记、转换为 markdown 或设置自动同步时使用。
version: 3.0.0
---

**📁 SKILL DIRECTORY PATH**

`<skill-directory>`

All relative file paths mentioned in this skill are relative to the above directory.

---

# Flomo to Obsidian 同步工具

将 flomo 笔记同步到 Obsidian，支持附件、标签、语音转写等完整功能。

## 🎯 使用场景

### 场景1：首次导入（手动转换）
用户已经从 flomo 网页版导出了数据，需要转换到 Obsidian。

**触发词**：
- "帮我把 flomo 数据转换到 Obsidian"
- "转换 flomo 导出文件"
- "导入 flomo 笔记"

### 场景2：自动同步（推荐）
用户希望定期自动从 flomo 同步最新笔记到 Obsidian。

**提供两种模式**：
- 🔐 **安全模式**：不保存密码，使用浏览器登录状态（推荐个人使用）
- 🤖 **密码模式**：保存密码，完全自动化（适合服务器/定时任务）

**触发词**：
- "设置 flomo 自动同步"
- "定期同步 flomo 到 Obsidian"
- "创建 flomo 同步任务"
- "flomo 安全模式同步"

---

## 🚀 场景1：手动转换（首次导入）

### 步骤1：获取 Flomo 导出文件

引导用户：
1. 登录 flomo 网页版 (https://flomoapp.com)
2. 进入 **设置 → 账号详情**
3. 点击 **"导出数据"** 按钮
4. 下载 ZIP 文件并解压

### 步骤2：询问必要信息

向用户确认：
- **Flomo HTML 文件路径**（例如：`~/Downloads/flomo@用户名/用户名的笔记.html`）
- **Obsidian vault 目录**（例如：`~/Documents/Obsidian/Flomo`）
- **是否需要标签前缀**（建议使用 `flomo/`）

### 步骤3：执行转换

```bash
cd {skillDir}

python scripts/convert_v2.py \
  --input "{flomo_html_path}" \
  --output "{obsidian_vault_path}" \
  --mode by-date \
  --tag-prefix "flomo/"
```

### 步骤4：报告结果

转换完成后，告诉用户：
- ✅ 转换了多少条笔记
- ✅ 复制了多少个附件
- ✅ 输出目录位置
- ✅ 如何在 Obsidian 中查看

---

## ⚡ 场景2：自动同步设置

### ⚠️ 重要：先询问用户选择模式

**必须先向用户说明两种模式的区别，让用户选择：**

```
我可以帮你设置 flomo 自动同步！有两种模式可选：

🔐 安全模式（推荐）
  ✅ 不保存密码到配置文件
  ✅ 使用浏览器保存的登录状态
  ✅ 首次需要手动登录一次（5分钟内）
  ✅ 后续自动同步
  ✅ 适合个人电脑日常使用

🤖 密码模式
  ✅ 完全自动化
  ✅ 适合服务器和定时任务
  ⚠️ 需要在配置文件中保存密码

你想使用哪种模式？
1. 安全模式（推荐）
2. 密码模式
```

---

### 模式A：🔐 安全模式（推荐）

#### 工作流程

```
用户选择安全模式
    ↓
询问 Obsidian vault 路径
    ↓
运行同步脚本（打开浏览器）
    ↓
等待用户手动登录
    ↓
自动完成首次同步
    ↓
询问是否创建定时任务
    ↓
完成！
```

#### 对话流程示例

**AI**: 好的！使用安全模式设置。

请告诉我：
- Obsidian vault 路径：（例如：/Users/username/Documents/Obsidian/flomo）
- 标签前缀：（建议使用 `flomo/`，直接回车使用默认）

---

**用户**: [提供路径]

---

**AI**: 收到！现在开始首次同步。

⚠️ 重要提示：
- 脚本将打开浏览器窗口
- 请在浏览器中手动登录 flomo
- 登录后，浏览器会记住你的登录状态
- 下次运行时将自动同步

按 Enter 继续...

[执行同步脚本]

```bash
cd {skillDir}
./sync_safe.sh
```

等待用户完成登录和同步...

✅ 同步成功！
- 新增笔记：120 条
- 附件：15 个
- 输出位置：/Users/username/Documents/Obsidian/flomo

下次运行 `./sync_safe.sh` 即可自动同步，无需再次登录！

是否创建定时任务，自动同步？
[同密码模式的定时任务选项]

---

### 模式B：🤖 密码模式

#### 工作流程

```
用户选择密码模式
    ↓
询问 flomo 账号密码
    ↓
询问 Obsidian vault 路径
    ↓
创建配置文件（.env）
    ↓
测试同步一次
    ↓
询问是否创建定时任务
    ↓
完成！
```

#### 对话流程示例

**AI**: 好的！使用密码模式设置。

首先需要你的 flomo 账号信息：
- 登录邮箱/手机号：
- 登录密码：

---

**用户**: [提供邮箱和密码]

---

**AI**: 收到！接下来：
- Obsidian vault 路径：（例如：/Users/username/Documents/Obsidian/flomo）
- 标签前缀：（建议使用 `flomo/`，直接回车使用默认）

---

**用户**: [提供路径]

---

**AI**: 配置完成！现在进行首次同步测试...

[执行同步]

✅ 同步成功！
- 新增笔记：120 条
- 附件：15 个
- 输出位置：/Users/username/Documents/Obsidian/flomo

是否创建定时任务，自动同步？
1. 每天晚上 10:00
2. 每天晚上 11:00  
3. 每 6 小时一次
4. 暂时不设置

---

### 实现步骤

#### 安全模式实现

##### 步骤1：收集信息

```python
vault_path = "Obsidian vault 路径"
tag_prefix = "flomo/"  # 默认值
```

##### 步骤2：运行安全模式脚本

```bash
cd {skillDir}

# 首次运行（会打开浏览器让用户登录）
python3 scripts/auto_sync_safe.py \
  --output "{vault_path}" \
  --tag-prefix "{tag_prefix}" \
  --no-headless \
  --verbose
```

**⚠️ 重要**：
- 脚本会打开浏览器窗口
- 等待用户手动登录（最多 5 分钟）
- 登录成功后自动继续同步
- 登录状态会保存在 `flomo_browser_data` 目录

##### 步骤3：验证结果

检查输出，确认：
- ✅ 登录成功
- ✅ 导出成功
- ✅ 转换成功
- ✅ 状态已保存

---

#### 密码模式实现

##### 步骤1：收集信息

```python
email = "用户的 flomo 邮箱"
password = "用户的 flomo 密码"
vault_path = "Obsidian vault 路径"
tag_prefix = "flomo/"  # 默认值
```

##### 步骤2：创建配置文件

```bash
cd {skillDir}

cat > .env << EOF
FLOMO_EMAIL={email}
FLOMO_PASSWORD={password}
OBSIDIAN_VAULT={vault_path}
TAG_PREFIX={tag_prefix}
EOF

chmod 600 .env
```

##### 步骤3：测试同步

```bash
cd {skillDir}

python scripts/auto_sync.py \
  --email "{email}" \
  --password "{password}" \
  --output "{vault_path}" \
  --tag-prefix "{tag_prefix}" \
  --no-headless
```

**注意**：首次测试建议使用 `--no-headless` 显示浏览器窗口，让用户观察过程。

#### 步骤4：创建定时任务

使用 OpenClaw 的 `scheduled_task_create` 功能：

```python
# 通过 MCP 调用创建定时任务
task_config = {
    "name": "Flomo 自动同步",
    "command": f"cd {skillDir} && ./sync.sh",
    "schedule": "0 22 * * *",  # 每天 22:00
    "description": "自动从 flomo 同步笔记到 Obsidian"
}
```

或者手动添加 cron：
```bash
crontab -l > /tmp/crontab_backup
echo "0 22 * * * cd {skillDir} && ./sync.sh >> /tmp/flomo_sync.log 2>&1" >> /tmp/crontab_backup
crontab /tmp/crontab_backup
```

---

## 📝 对话模板

### 模板1：手动转换

```
用户: 帮我把 flomo 数据转换到 Obsidian

AI: 好的！我来帮你转换 flomo 数据。

请提供以下信息：
1. Flomo 导出的 HTML 文件路径：（如果还没导出，我可以教你如何导出）
2. Obsidian vault 的目标目录：

用户: [提供路径]

AI: 收到！开始转换...

[执行转换]

✅ 转换完成！
- 笔记数：513 条
- 附件数：54 个
- 输出位置：/Users/username/Documents/Obsidian/flomo

你可以在 Obsidian 中打开该目录查看笔记了。

是否需要设置自动同步，以后自动导入新笔记？
```

### 模板2：自动同步

```
用户: 设置 flomo 自动同步

AI: 好的！我来帮你设置 flomo 自动同步。

为了自动登录 flomo 并导出数据，需要你的账号信息：
- Flomo 登录邮箱：
- Flomo 登录密码：

（这些信息会加密存储在本地，不会上传）

用户: [提供账号]

AI: 收到！再确认一下：
- Obsidian vault 路径：（例如：/Users/username/mynote/flomo）

用户: /Users/ryanbzhou/mynote/flomo

AI: 好的！配置完成，现在测试同步...

⏳ 正在自动登录 flomo...
⏳ 正在导出数据...
⏳ 正在转换笔记...

✅ 同步成功！
- 新增笔记：120 条
- 附件：15 个

是否创建定时任务？
1. 每天晚上 10:00 自动同步
2. 每天晚上 11:00 自动同步
3. 每 6 小时同步一次
4. 暂时不设置（需要时手动运行）

用户: 1

AI: 好的！已创建定时任务：
- 任务名：Flomo 自动同步
- 执行时间：每天 22:00
- 任务命令：cd /path/to/skill && ./sync.sh

从明天开始，flomo 的新笔记会自动同步到 Obsidian！

你也可以随时手动同步：
cd /path/to/skill && ./sync.sh
```

---

## 🔧 脚本说明

### convert_v2.py - 手动转换脚本

将已导出的 flomo HTML 转换为 Obsidian markdown。

**参数**：
- `--input` (必需): Flomo HTML 文件路径
- `--output` (必需): Obsidian vault 输出目录
- `--mode`: 组织模式 (`by-date` | `individual` | `single`)，默认 `by-date`
- `--tag-prefix`: 标签前缀，默认空
- `--no-attachments`: 不复制附件
- `--verbose`: 显示详细日志

### auto_sync.py - 自动同步脚本

使用浏览器自动化从 flomo 导出并同步到 Obsidian。

**参数**：
- `--email` (必需): Flomo 登录邮箱
- `--password` (必需): Flomo 登录密码
- `--output` (必需): Obsidian vault 输出目录
- `--tag-prefix`: 标签前缀，默认空
- `--no-headless`: 显示浏览器窗口（测试用）
- `--force-full`: 强制完整同步（忽略增量）
- `--verbose`: 显示详细日志

### sync.sh - 同步快捷脚本

读取 `.env` 配置文件并执行同步。

**使用**：
```bash
./sync.sh                 # 后台运行
./sync.sh --no-headless   # 显示浏览器
./sync.sh --force-full    # 完整同步
```

---

## ⚙️ 配置文件

### .env 文件格式

```bash
FLOMO_EMAIL=your-email@example.com
FLOMO_PASSWORD=your-password
OBSIDIAN_VAULT=/path/to/obsidian/vault/flomo
TAG_PREFIX=flomo/
```

**安全提示**：
- ✅ 已自动添加到 `.gitignore`
- ✅ 文件权限设置为 `600`（仅所有者可读写）
- ✅ 不会被提交到 Git

---

## 📊 输出格式

### 笔记格式（by-date 模式）

```markdown
---
date: 2024-03-11
source: flomo
tags: [flomo/flomo, flomo/工作]
note_count: 5
---

# Flomo Notes - 2024-03-11

## 2024-03-11 09:30:15

这是笔记内容 #工作

### 附件

![[attachments/image_123.jpg]]

![[attachments/audio_456.m4a]]

**语音转写：**

> 这是语音转写的文本内容...

---

## 2024-03-11 14:20:00

另一条笔记...

---
```

### 附件组织

```
vault/flomo/
├── 2024-03-11.md
├── 2024-03-12.md
└── attachments/
    ├── image_123.jpg
    ├── audio_456.m4a
    └── ...
```

---

## 🐛 故障处理

### 问题1：浏览器自动化失败

**现象**：无法自动登录或导出

**解决**：
1. 使用 `--no-headless` 观察浏览器操作
2. 检查账号密码是否正确
3. 查看错误截图：`flomo_downloads/error_screenshot.png`
4. 查看日志：`auto_sync.log`

### 问题2：附件缺失

**现象**：图片或音频没有复制

**解决**：
1. 确认 flomo 导出的 ZIP 包含 `file/` 目录
2. 检查解压后的目录结构
3. 手动检查 HTML 文件中的附件路径

### 问题3：增量同步不工作

**现象**：每次都完整同步

**解决**：
1. 检查 `.flomo_sync_state.json` 是否存在
2. 不要删除状态文件
3. 使用 `--force-full` 强制完整同步

---

## 📈 性能说明

- **首次同步**：500 条笔记约需 30-60 秒
- **增量同步**：10 条新笔记约需 20-30 秒
- **浏览器启动**：约 5-10 秒
- **附件复制**：取决于文件大小

---

## 🔄 版本历史

### V3.0.0 (2024-03-11)
- ✅ 简化为适合 Agent 对话的工作流
- ✅ 优化用户交互流程
- ✅ 集成定时任务创建

### V2.0.0 (2024-03-11)
- ✅ 新增浏览器自动化同步
- ✅ 新增增量同步机制
- ✅ 新增附件自动复制

### V1.0.0 (2024-03-10)
- ✅ 基础 HTML 到 Markdown 转换
- ✅ 标签和元数据保留

---

## 📚 相关文档

- **AUTO_SYNC.md** - 自动同步技术文档
- **SETUP_GUIDE.md** - 环境变量设置指南
- **README.md** - 项目总览

---

## 💡 Agent 使用建议

### 首次使用

1. **探测需求**：询问用户是手动转换还是自动同步
2. **引导操作**：根据场景给出清晰的步骤
3. **收集信息**：逐步询问必要参数
4. **执行操作**：运行对应脚本
5. **确认结果**：展示转换统计并询问后续需求

### 持续使用

1. **检测状态**：查看 `.env` 是否存在，判断是否已配置
2. **快速执行**：直接运行 `./sync.sh`
3. **报告结果**：显示增量同步统计

### 错误处理

1. **友好提示**：用通俗语言解释错误
2. **提供方案**：给出 2-3 个解决建议
3. **主动帮助**：提供查看日志、截图的命令

---

## ✅ 功能检查清单

在帮助用户使用此 skill 时，确保：

- [ ] 询问了必要的参数（路径、账号等）
- [ ] 解释了数据的安全性（本地存储、不上传）
- [ ] 执行前确认了参数正确性
- [ ] 执行后展示了结果统计
- [ ] 提供了后续使用建议（自动同步、定时任务等）
- [ ] 告知了如何查看转换后的笔记

---

**记住**：这是一个面向普通用户的 skill，对话要友好、清晰、循序渐进！
