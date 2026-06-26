# WeChat Article Fetcher

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blue" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/version-1.0.0-green" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
</p>

一键抓取微信公众号文章，保存为本地 HTML，支持图片下载和视频封面提取。

## ✨ 功能特性

- 📄 **全文抓取** - 自动提取微信公众号文章完整内容
- 🖼️ **图片下载** - 自动下载文章内所有图片（含 GIF）
- 🎬 **视频封面** - 提取视频封面图，点击跳转原文播放
- 📝 **智能命名** - 文件名格式：`日期_英文关键词.html`
- 🌐 **本地预览** - 内置 HTTP 服务器，浏览器直接查看
- 🔧 **无需配置** - 零配置，开箱即用

## 📦 安装

### 方式一：通过 SkillHub 安装（推荐）

```bash
skillhub install wechat-article-fetcher
```

### 方式二：通过 ClawHub 安装

```bash
clawhub install yourname/wechat-article-fetcher
```

### 方式三：手动安装

1. 克隆仓库到 OpenClaw skills 目录：

```bash
cd ~/.openclaw/skills  # 或你的 OpenClaw skills 目录
git clone https://github.com/yourname/wechat-article-fetcher.git
```

2. 确保 Python 依赖已安装：

```bash
pip install requests
```

3. 赋予执行权限：

```bash
chmod +x wechat-article-fetcher/fetch.sh
```

## 🚀 使用

### 方式一：对话中直接发送链接

在 OpenClaw 对话中直接粘贴微信文章链接：

```
https://mp.weixin.qq.com/s/xxxxx
```

AI 助手会自动识别并抓取文章。

### 方式二：命令行运行

```bash
# 基本用法
./skills/wechat-article-fetcher/fetch.sh https://mp.weixin.qq.com/s/xxxxx

# 指定端口（如果 8080 被占用）
./skills/wechat-article-fetcher/fetch.sh https://mp.weixin.qq.com/s/xxxxx 8888
```

### 方式三：Python 直接调用

```bash
python3 skills/wechat-article-fetcher/fetch.py https://mp.weixin.qq.com/s/xxxxx
```

## 📂 输出文件

抓取后的文件保存在 OpenClaw 工作目录：

```
workspace/
├── 2026-03-21_LibTV_Agent.html       # 文章 HTML 文件
├── images/                            # 文章图片目录
│   ├── a1b2c3d4.jpg
│   └── ...
└── video_covers/                      # 视频封面目录
    ├── 2026-03-21_LibTV_Agent_cover_1.jpg
    └── ...
```

## 🌐 访问文章

启动 HTTP 服务器后，在浏览器访问：

```
http://localhost:8080/2026-03-21_LibTV_Agent.html
```

如果端口被占用，可以手动启动服务器：

```bash
cd ~/.openclaw/workspace
python3 -m http.server 8080
```

## 📝 文件名说明

文件名格式：`{日期}_{英文关键词}.html`

**示例：**
- 文章标题："LibTV 上线，首个同时面向人与 Agent 的专业视频创作平台"
- 生成文件名：`2026-03-21_LibTV_Agent.html`

**命名规则：**
1. 从标题提取英文单词（如 LibTV, Agent, OpenClaw）
2. 无英文时提取数字
3. 兜底使用 URL 短码

## ⚠️ 已知限制

- **微信视频**：由于防盗链和加密机制，无法直接下载或嵌入播放，仅支持封面图+跳转原文
- **登录态文章**：部分需要微信登录才能查看的文章可能无法完整抓取
- **动态内容**：文章中的动态交互内容（如投票、小程序）无法保存

## 🔧 故障排查

### 问题：图片显示不出来

**检查：**
- `images/` 目录是否存在
- HTTP 服务器是否已启动
- 图片文件是否下载成功

**解决：**
```bash
# 检查图片目录
ls -la ~/.openclaw/workspace/images/

# 重启 HTTP 服务器
cd ~/.openclaw/workspace && python3 -m http.server 8080
```

### 问题：视频封面无法显示

**原因：** 微信图片有防盗链机制

**解决：** 封面图已自动下载到 `video_covers/` 目录，检查文件是否存在

### 问题：文件名是日期+数字

**原因：** 文章标题中没有英文单词

**解决：** 属于正常情况，不影响使用

### 问题：命令未找到

**解决：**
```bash
# 添加执行权限
chmod +x ~/.openclaw/skills/wechat-article-fetcher/fetch.sh

# 或使用 Python 直接运行
python3 ~/.openclaw/skills/wechat-article-fetcher/fetch.py URL
```

## 🛠️ 开发

### 目录结构

```
wechat-article-fetcher/
├── fetch.sh              # 主入口脚本（Bash）
├── fetch.py              # Python 核心逻辑
├── SKILL.md              # OpenClaw Skill 文档
├── README.md             # 本文件
├── _meta.json            # Skill 元数据
├── evals/
│   └── evals.json        # 测试用例
├── LICENSE               # MIT 许可证
└── .gitignore            # Git 忽略配置
```

### 运行测试

```bash
# 测试基本抓取
python3 skills/wechat-article-fetcher/fetch.py https://mp.weixin.qq.com/s/xxxxx

# 检查输出
ls -la ~/.openclaw/workspace/2026-*.html
```

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

## 🙏 致谢

- 感谢 OpenClaw 社区提供的 Skill 框架
- 感谢所有测试和反馈的用户

---

<p align="center">
  Made with ❤️ for OpenClaw
</p>
