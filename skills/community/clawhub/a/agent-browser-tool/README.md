# 🤖 Agent Browser - 浏览器自动化

## 📖 功能说明

基于 Rust 的无头浏览器自动化 CLI，支持导航、点击、输入、截图等操作。

## 🚀 使用方法

### 在 OpenClaw 中使用

```
打开这个网页 https://example.com
点击登录按钮
在搜索框输入关键词
截图这个页面
```

### 命令行调用

```bash
# 打开网页
agent-browser open https://example.com

# 截图
agent-browser screenshot --url https://example.com --output page.png

# 执行 JavaScript
agent-browser eval --url https://example.com "document.title"
```

## 📁 文件结构

```
agent-browser/
├── SKILL.md              # 技能描述
├── CONTRIBUTING.md       # 贡献指南
└── README.md             # 本文件
```

## 🔧 依赖安装

```bash
# 安装 Rust (如果还没有)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 克隆并编译
git clone https://github.com/openclaw/agent-browser.git
cd agent-browser
cargo build --release
```

## 📊 示例输出

```
✅ 网页已打开：https://example.com
📸 截图已保存：page.png
📊 页面标题：Example Domain
```

## 🛠️ 开发计划

- [x] 基础浏览器控制
- [x] 截图功能
- [x] JavaScript 执行
- [ ] 表单自动填充
- [ ] 等待元素出现
- [ ] 多标签页支持

## 📝 更新日志

### v1.0.0
- 🎉 初始版本

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License
