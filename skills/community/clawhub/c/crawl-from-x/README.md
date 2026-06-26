# Crawl From X ✨

> X/Twitter 帖子抓取与管理工具 - 自动化跟踪你关注的用户动态

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.4-green.svg)](CHANGELOG.md)

Crawl From X 是一个专注于 X (Twitter) 帖子抓取的自动化工具，可以帮你轻松管理和跟踪你关注的 X 用户最新动态。

## ✨ 核心功能

- 👥 **用户列表管理** - 增删改查需要关注的 X 用户名
- 🔄 **批量抓取** - 自动访问用户主页，抓取当天发布的所有帖子
- 📝 **完整内容获取** - 通过 API 获取帖子完整文本、图片、视频等
- 📄 **Markdown 导出** - 自动生成格式化的 Markdown 文件
- 🎬 **媒体支持** - 自动提取图片、视频链接
- 📊 **互动数据** - 点赞、转发、浏览、回复数统计
- 🛡️ **容错机制** - 浏览器自动恢复、智能重试（最多 5 次）
- 📰 **X Article 支持** - 完整提取长文章内容
- 🔒 **进程锁** - 防止多个实例同时运行

## 🚀 快速开始

### 前置要求

⚠️ **重要**：此技能需要 OpenClaw 的 **Browser Relay（浏览器中转）功能**来抓取用户帖子。

#### 必要的依赖

1. **安装 OpenClaw**
   ```bash
   # 访问官网下载安装
   open https://github.com/openclaw/openclaw
   ```

2. **安装浏览器扩展**
   
   **Chrome/Edge 用户：**
   - 打开 OpenClaw 设置
   - 进入 "Browser Relay" 部分
   - 按照提示安装浏览器扩展
   - 完成后，浏览器扩展会显示 "Relay On" 或绿色图标

   **未安装浏览器扩展会导致：**
   - ❌ 无法抓取用户主页
   - ❌ 无法提取帖子 URL
   - ❌ 程序报错

3. **启动 Browser Relay 服务**
   ```bash
   # 确保 Browser Relay 已启动
   openclaw browser status
   
   # 如果未启动，使用以下命令启动
   openclaw browser start
   ```

4. **X 账号已登录**
   - 在安装了 Browser Relay 扩展的浏览器中登录 X（Twitter）
   - 技能会使用已登录的会话抓取内容

#### 验证安装

运行以下命令验证所有依赖已就绪：

```bash
# 1. 检查 OpenClaw 状态
openclaw status

# 2. 检查 Browser Relay 状态
openclaw browser status

# 3. 如果显示 "browser: enabled"，说明一切就绪
```

**如果遇到问题，请访问：**
- [OpenClaw 文档 - Browser Relay](https://docs.openclaw.ai/guide/browser-relay)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues)

### 安装技能

**通过 ClawHub 安装（推荐）：**
```bash
npx clawhub@latest install crawl-from-x
```

安装后，文件会位于：
- `$CLAWD/skills/crawl-from-x/scripts/craw_hot.py` - 主脚本
- `$CLAWD/skills/crawl-from-x/users.txt` - 用户列表（模板）
- `$CLAWD/skills/crawl-from-x/results/` - 抓取结果

**或手动克隆：**
```bash
git clone https://github.com/flyingtimes/crawl-from-x.git
cd crawl-from-x
```

安装依赖（如果需要）：
```bash
pip install -r requirements.txt
```

---

**通过 ClawHub 安装（推荐）：**
```bash
npx clawhub@latest install crawl-from-x
```

安装后，文件会位于：
- `$CLAWD/skills/crawl-from-x/scripts/craw_hot.py` - 主脚本
- `$CLAWD/skills/crawl-from-x/users.txt` - 用户列表
- `$CLAWD/skills/crawl-from-x/results/` - 抓取结果

**或手动克隆：**
```bash
git clone https://github.com/flyingtimes/crawl-from-x.git
cd crawl-from-x
```

安装依赖（如果需要）：
```bash
pip install -r requirements.txt
```

### 基本使用

#### 1. 进入脚本目录
```bash
cd skills/crawl-from-x/scripts
```

#### 2. 添加关注用户
```bash
# 添加单个用户
python3 craw_hot.py add elonmusk

# 批量添加用户
python3 craw_hot.py add elonmusk openai vista8
```

#### 3. 查看用户列表
```bash
python3 craw_hot.py list
```

#### 4. 删除用户
```bash
python3 craw_hot.py remove elonmusk
```

#### 5. 抓取帖子
```bash
# 抓取单个用户
python3 craw_hot.py crawl elonmusk

# 抓取所有用户
python3 craw_hot.py crawl
```

#### 6. 查看结果
```bash
# 查看最近的 URL 列表
ls -lt skills/crawl-from-x/results/

# 查看 Markdown 格式的完整内容
cat skills/crawl-from-x/results/posts_*.md
```

## 📖 使用场景

### 场景 1：定期跟踪行业动态

```bash
# 1. 添加关注的技术博主
python3 skills/crawl-from-x/scripts/craw_hot.py add elonmusk
python3 skills/crawl-from-x/scripts/craw_hot.py add openai
python3 skills/crawl-from-x/scripts/craw_hot.py add samaltman

# 2. 每天运行抓取
python3 skills/crawl-from-x/scripts/craw_hot.py crawl

# 3. 查看 Markdown 结果
cat skills/crawl-from-x/results/posts_$(date +%Y%m%d)*.md
```

### 场景 2：监控特定话题相关账号

```bash
# 1. 直接编辑 users.txt
vim skills/crawl-from-x/users.txt

# 2. 每行一个用户名，例如：
elonmusk
openai
vista8

# 3. 运行抓取
cd skills/crawl-from-x/scripts
python3 craw_hot.py crawl

# 4. 查看结果
cat ../results/posts_*.md
```

### 场景 3：定时任务（Cron）

```bash
# 添加到 crontab，每天早上 8 点运行
crontab -e

# 添加以下行：
0 8 * * * cd /path/to/clawd && /usr/bin/python3 skills/crawl-from-x/scripts/craw_hot.py crawl
```

## 📁 输出格式

### URL 列表文件 (`posts_YYYYMMDD_HHMMSS.txt`)

```
https://x.com/elonmusk/status/1234567890
https://x.com/openai/status/1234567891
...
```

### Markdown 文件 (`posts_YYYYMMDD_HHMMSS.md`)

每个帖子包含：
- 📌 帖子标题和作者信息
- ⏰ 发布时间和原文链接
- 📝 完整文本内容
- 🖼️ 媒体文件（图片、视频）
- 📊 互动数据（💬 回复 | ❤️ 点赞 | 🔄 转发 | 👁️ 浏览）

X Article 长文章：
- 完整文章内容
- 结构化标题（h1/h2/h3）
- 封面图和元信息

## 🔧 高级功能

### 浏览器自动恢复（v2.1+）

当检测到浏览器连接问题时，脚本会自动：
1. 🔧 重启浏览器服务
2. ⏳ 等待 30 秒让浏览器完全初始化
3. 🔄 自动重试刚才失败的操作
4. 📊 整个任务最多自动重启 10 次

### 进程锁机制（v2.4+）

防止多个实例同时运行，避免重复抓取：
- 检测到已有实例时友好提示
- 程序退出时自动清理锁文件

### 智能跳过（v2.2+）

当用户 24 小时内没有发新帖时：
- 不再反复重试
- 直接处理下一个用户
- 提高抓取效率

### 增量写入（v2.3+）

- 每抓取一个用户就立即写入文件
- 避免故障导致数据丢失
- 文件中显示实时进度 [X/Y]

## 🛠️ 故障排查

### 多实例运行错误

```
❌ Error: Another crawl-from-x instance is already running!
   Lock file: /path/to/.crawl-from-x.lock
```

**解决方案：**
```bash
# 方案 1：等待当前实例完成

# 方案 2：删除锁文件（谨慎使用）
rm /path/to/.crawl-from-x.lock
```

### 浏览器连接失败

```bash
# 检查状态
openclaw browser status

# 重启浏览器服务
openclaw browser stop
openclaw browser start

# 重新运行抓取
cd skills/crawl-from-x/scripts
python3 craw_hot.py crawl
```

### 内容获取失败

查看日志文件：
```bash
# 查看详细错误信息
tail -f skills/crawl-from-x/craw_hot.log

# 搜索错误
grep ERROR skills/crawl-from-x/craw_hot.log
```

常见原因：
- API 速率限制
- 帖子已被删除
- 私密账号
- 浏览器未登录

## 📋 注意事项

1. ⚠️ **浏览器要求**：必须安装 OpenClaw 浏览器扩展
2. 🔐 **登录状态**：浏览器必须登录 X 账号
3. ⏱️ **速率限制**：脚本已内置随机延迟（0.5-1.5 秒）
4. 🔒 **私密账号**：无法抓取私密账号内容
5. 🚫 **合规使用**：请遵守 X 的使用条款和 API 规范

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新历史。

### 最新版本 (v2.4)

- 🔒 进程锁机制：防止多个实例同时运行
- 🛑 智能检测：检测到已有实例时友好提示
- 🧹 自动清理：程序退出时自动清理锁文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [问题反馈](https://github.com/flyingtimes/crawl-from-x/issues)

---

**Made with ❤️ by OpenClaw Community**
