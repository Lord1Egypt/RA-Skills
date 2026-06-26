# 🌊 Flomo to Obsidian 同步工具

将 flomo 笔记无缝同步到 Obsidian，支持附件、标签、语音转写等完整功能。

---

## 🎯 这个工具能做什么？

✅ **一次性导入**：将 flomo 已有笔记批量转换到 Obsidian  
✅ **自动同步**：定期自动从 flomo 获取最新笔记  
✅ **附件支持**：自动复制图片、音频等附件  
✅ **标签保留**：flomo 标签自动转换为 Obsidian 标签  
✅ **语音转写**：保留 flomo 的语音转文字内容  
✅ **增量同步**：只同步新笔记，不重复处理

---

## 🚀 快速开始

### 方式1：在 OpenClaw 对话中使用（推荐 ⭐⭐⭐⭐⭐）

**最简单！直接在 Agent 对话中说：**

```
"帮我把 flomo 数据转换到 Obsidian"
```

或

```
"设置 flomo 自动同步到 Obsidian"
```

**Agent 会引导你完成所有步骤：**
1. 询问必要信息（账号、路径等）
2. 自动执行转换或同步
3. 报告结果
4. 询问是否创建定时任务

**就这么简单！**

---

### 方式2：命令行使用（技术用户）

#### 场景A：首次导入（手动转换）

**步骤1：从 flomo 导出数据**

1. 登录 [flomo 网页版](https://flomoapp.com)
2. 进入 **设置 → 账号详情**
3. 点击 **"导出数据"** 按钮
4. 下载 ZIP 文件并解压

**步骤2：运行转换**

```bash
cd <skill-directory>

python scripts/convert_v2.py \
  --input "~/Downloads/flomo@YourName-20260311/YourName的笔记.html" \
  --output "~/mynote/flomo" \
  --mode by-date \
  --tag-prefix "flomo/"
```

**完成！**笔记已转换到 Obsidian。

---

#### 场景B：自动同步

有两种同步模式可选：

##### 🔐 安全模式（推荐 ⭐⭐⭐⭐⭐）

**不保存密码，使用浏览器登录状态**

```bash
cd <skill-directory>

# 首次运行需要手动登录一次
./sync_safe.sh
```

**特点：**
- ✅ 不保存密码到配置文件
- ✅ 使用浏览器保存的登录状态
- ✅ 首次需要手动登录（5 分钟内完成）
- ✅ 后续自动同步，无需再次登录
- ✅ 更安全

**适合：** 个人电脑日常使用

---

##### 🤖 密码模式

**一次配置，完全自动**

```bash
cd <skill-directory>

# 创建配置文件
cat > .env << EOF
FLOMO_EMAIL=your_phone_or_email
FLOMO_PASSWORD=your_password
EOF

# 运行同步
./sync.sh
```

**特点：**
- ✅ 完全自动化
- ✅ 适合服务器和定时任务
- ⚠️ 需要在配置文件中保存密码

**适合：** 服务器、定时任务、完全自动化场景

---

## 📖 两种使用模式对比

| 特性 | 手动转换 | 自动同步 |
|------|---------|---------|
| 适用场景 | 首次导入历史笔记 | 持续同步最新笔记 |
| 需要账号密码 | ❌ 不需要 | ✅ 需要 |
| 操作方式 | 手动导出 → 运行脚本 | 自动运行，无需人工 |
| 是否支持增量 | ❌ 每次完整转换 | ✅ 只同步新笔记 |
| 推荐频率 | 一次性使用 | 定时自动运行 |

**建议**：首次使用**手动转换**导入历史数据，然后设置**自动同步**保持更新。

---

## 📂 输出格式

### 笔记组织（by-date 模式）

```
mynote/flomo/
├── 2024-03-11.md       # 当天所有笔记
├── 2024-03-12.md
└── attachments/        # 所有附件
    ├── image_123.jpg
    ├── audio_456.m4a
    └── ...
```

### 笔记内容示例

```markdown
---
date: 2024-03-11
source: flomo
tags: [flomo/flomo, flomo/工作]
note_count: 5
---

# Flomo Notes - 2024-03-11

## 2024-03-11 09:30:15

这是一条工作笔记 #工作 #flomo

### 附件

![[attachments/image_123.jpg]]

---

## 2024-03-11 14:20:00

这是一条带语音的笔记 #flomo

### 附件

![[attachments/audio_456.m4a]]

**语音转写：**

> 今天完成了项目第一阶段的开发...

---
```

---

## 🔧 配置说明

### 标签前缀

**建议使用 `flomo/` 前缀**，避免和 Obsidian 其他笔记的标签冲突。

- flomo 标签：`#工作`
- Obsidian 标签：`#flomo/工作`

### 组织模式

- **by-date**（推荐）：按日期创建文件，每天一个 markdown
- **individual**：每条笔记一个文件
- **single**：所有笔记合并为一个文件

---

## 🛠️ 技术细节

### 环境要求

- Python 3.7+
- 依赖包：
  - `beautifulsoup4` - HTML 解析
  - `markdownify` - HTML 转 Markdown
  - `playwright` - 浏览器自动化

### 自动同步原理

1. **浏览器自动化**：使用 Playwright 控制 Chromium 浏览器
2. **自动登录**：输入邮箱密码并登录 flomo
3. **导出数据**：点击导出按钮并下载 ZIP
4. **解压转换**：自动解压并转换为 Markdown
5. **增量处理**：通过 `.flomo_sync_state.json` 记录已同步笔记的时间戳
6. **复制附件**：将图片、音频复制到 `attachments/` 目录
7. **清理文件**：删除临时下载文件

### 安全性

#### 🔐 安全模式（推荐）
- ✅ **不保存密码**：配置文件中不包含任何敏感信息
- ✅ **浏览器会话**：使用浏览器保存的登录状态
- ✅ **本地存储**：登录状态保存在 `flomo_browser_data` 目录
- ✅ **权限保护**：目录权限仅当前用户可访问

#### 🤖 密码模式
- ⚠️ 账号密码存储在本地 `.env` 文件
- ✅ 文件权限设置为 `600`（仅所有者可读写）
- ✅ 已添加到 `.gitignore`，不会被提交到 Git
- ✅ 不会上传任何数据到外部服务器

---

## 📚 详细文档

- **[USAGE_SAFE_MODE.md](./USAGE_SAFE_MODE.md)** - 🔐 安全模式使用指南（推荐阅读）
- **[QUICK_START.md](./QUICK_START.md)** - 5 分钟快速开始
- **[USAGE_IN_AGENT.md](./USAGE_IN_AGENT.md)** - 在 OpenClaw 中使用
- **[AUTO_SYNC.md](./AUTO_SYNC.md)** - 自动同步技术文档
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - 环境变量设置指南
- **[SKILL.md](./SKILL.md)** - Skill 使用说明（Agent 视角）

---

## 🐛 故障排查

### 问题1：浏览器自动化失败

**解决方案**：
```bash
# 使用可视化模式调试
./sync.sh --no-headless
```

观察浏览器操作，查看哪一步失败。

### 问题2：找不到附件

**检查**：
1. flomo 导出的 ZIP 是否包含 `file/` 目录
2. 解压后的目录结构是否正确
3. HTML 文件中的附件路径是否正确

### 问题3：定时任务不执行

**检查 crontab**：
```bash
crontab -l | grep flomo
```

**查看日志**：
```bash
tail -f /tmp/flomo_sync.log
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🎉 示例对话

### 在 OpenClaw 中使用

**用户**：
> 帮我设置 flomo 自动同步

**AI**：
> 好的！我来帮你设置 flomo 自动同步到 Obsidian。
> 
> 首先需要你的 flomo 账号信息：
> - 登录邮箱：
> - 登录密码：
> 
> （这些信息会加密存储在本地，不会上传）

**用户**：
> your-email@example.com
> your-password

**AI**：
> 收到！再确认一下：
> - Obsidian vault 路径：（例如：/Users/username/mynote/flomo）

**用户**：
> ~/Documents/Obsidian/flomo

**AI**：
> 好的！配置完成，现在测试同步...
> 
> ⏳ 正在自动登录 flomo...
> ⏳ 正在导出数据...
> ⏳ 正在转换笔记...
> 
> ✅ 同步成功！
> - 新增笔记：120 条
> - 附件：15 个
> 
> 是否创建定时任务？
> 1. 每天晚上 10:00 自动同步
> 2. 每天晚上 11:00 自动同步
> 3. 每 6 小时同步一次
> 4. 暂时不设置

**用户**：
> 1

**AI**：
> 好的！已创建定时任务：
> - 任务名：Flomo 自动同步
> - 执行时间：每天 22:00
> - 任务命令：cd /path/to/skill && ./sync.sh
> 
> 从明天开始，flomo 的新笔记会自动同步到 Obsidian！
> 
> 你也可以随时手动同步：
> ```
> cd /path/to/skill && ./sync.sh
> ```

---

## ⭐ 为什么选择这个工具？

- 🎯 **专为 OpenClaw 设计**：对话式操作，无需复杂配置
- 🔄 **完整功能**：支持附件、标签、语音转写等所有 flomo 特性
- 🚀 **自动化**：设置一次，终身自动同步
- 🔒 **安全可靠**：数据本地处理，不上传外部服务器
- 📖 **格式友好**：输出标准 Obsidian Markdown，完美兼容

---

**开始使用吧！在 OpenClaw 中说：**

```
"帮我设置 flomo 自动同步"
```

就这么简单！🎉
