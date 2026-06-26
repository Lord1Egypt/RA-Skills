# 详细安装说明

## Claude Code 安装

### 项目级安装（推荐）

在你的 git 仓库根目录执行：

`bash
mkdir -p .claude/skills
git clone https://github.com/xmlans/codegirl-skill .claude/skills/codegirl
`

### 全局安装

`bash
git clone https://github.com/xmlans/codegirl-skill ~/.claude/skills/codegirl
`

### OpenClaw 安装

`bash
git clone https://github.com/xmlans/codegirl-skill ~/.openclaw/workspace/skills/codegirl
`

---

## 依赖安装

### 基础依赖（可选）

`bash
cd .claude/skills/codegirl # 或你的安装路径
pip3 install -r requirements.txt
`

目前唯一的可选依赖是 Pillow，用于读取照片 EXIF 信息。如果你不需要照片分析功能，可以跳过。

---

## Telegram / 微信 聊天记录导出指南

要获取聊天记录，你需要使用第三方导出工具。以下是推荐的工具：

### Telegram 导出（推荐）

- 使用 Telegram Desktop
- 点击 Settings -> Advanced -> Export Telegram data
- 选择对应的聊天联系人，格式选择 JSON
- 在 /create-gf 时使用方式 D（Telegram 导出）

### WeChatMsg（推荐）

- GitHub: https://github.com/LC044/WeChatMsg
- 支持 Windows
- 导出格式：txt / html / csv
- 使用方法：下载安装 → 登录微信PC版 → 选择联系人 → 导出

### PyWxDump

- GitHub: https://github.com/xaoyaoo/PyWxDump
- 支持 Windows
- 导出格式：SQLite 数据库
- 适合有编程基础的用户

### 留痕

- 支持 macOS
- 导出格式：JSON
- 适合 Mac 用户

### 手动复制

如果以上工具都不方便，你也可以：
1. 在微信/Telegram中打开与 Codegirl 的聊天窗口
2. 手动选择并复制关键技术对话或 Debug 崩溃历史
3. 粘贴到一个 txt 文件中
4. 在 /create-gf 时使用方式 E（手动文本）

---

## QQ 聊天记录导出指南

1. 打开 QQ → 点击左下角 ≡ → 设置
2. 通用 → 聊天记录 → 导出聊天记录
3. 选择联系人 → 导出为 txt 格式
4. 在 /create-gf 时使用方式 B

---

## 常见问题

### Q: 数据会上传到云端吗？
A: 不会。所有数据都存储在你的本地文件系统中，不会上传到任何服务器。

### Q: 可以同时创建多个 Codegirl 的 Skill 吗？
A: 可以。每个 Codegirl 会生成独立的 gfs/{slug}/ 目录。

### Q: 创建后还能修改吗？
A: 可以。说“她不会这样说代码”触发对话纠正，或“我有新的提交记录”追加原材料。每次修改都有版本存档，可以回滚。

### Q: 我想删除怎么办？
A: 使用 /delete-gf {slug} 或 /let-go {slug} 命令。
