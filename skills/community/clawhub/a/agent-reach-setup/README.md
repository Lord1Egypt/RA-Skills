# Agent Reach 完整安装与配置解决方案

一个基于实际部署经验的完整Agent Reach安装和配置解决方案，包含问题诊断和最佳实践。

## 🚀 快速开始

```bash
# 1. 克隆本技能包
git clone <repository-url>
cd agent-reach-setup

# 2. 运行安装脚本
chmod +x install.sh
./install.sh

# 3. 验证安装
agent-reach doctor
```

## 📋 功能特性

- ✅ **完整安装流程** - Agent Reach 1.3.0 完整安装
- ✅ **7个核心渠道** - YouTube, RSS, 搜索, 网页, Twitter, B站, 微信公众号
- ✅ **问题解决方案** - 常见问题的实际解决方法
- ✅ **多环境支持** - OpenClaw, Claude Code, 通用AI Agent环境
- ✅ **详细文档** - 完整的安装、配置、使用指南

## 📁 技能包结构

```
agent-reach-setup/
├── SKILL.md              # 技能文档
├── package.json          # 技能元数据
├── install.sh            # 安装脚本
├── config.json           # 默认配置
├── README.md            # 本文件
├── troubleshooting.md   # 故障排除
└── usage-examples.md    # 使用示例
```

## 🔧 系统要求

- **Python**: 3.13+
- **Node.js**: 22+
- **操作系统**: Linux, macOS, Windows (WSL)
- **权限**: 用户主目录写入权限

## 📦 安装方式

### 方式1: 使用安装脚本
```bash
chmod +x install.sh
./install.sh
```

### 方式2: 手动安装
```bash
# 1. 安装Agent Reach
pip install https://github.com/Panniantong/agent-reach/archive/main.zip --break-system-packages

# 2. 自动配置
agent-reach install --env=auto

# 3. 配置Exa搜索
mcporter config add exa https://mcp.exa.ai/mcp

# 4. 验证安装
agent-reach doctor
```

## 📊 配置状态

### ✅ 装好即用 (7/13)
- YouTube 视频和字幕
- RSS/Atom 订阅源
- 全网语义搜索
- 任意网页
- Twitter/X 推文
- B站视频和字幕
- 微信公众号文章

### 🔧 可选配置
- GitHub 仓库和代码
- Reddit 帖子和评论
- 小红书笔记
- 抖音短视频
- LinkedIn 职业社交
- Boss直聘职位搜索

## 🚨 问题解决

### 权限问题
```bash
# 错误: externally-managed-environment
# 解决方案:
pip install ... --break-system-packages
```

### GitHub CLI 安装失败
```bash
# 手动安装
# https://cli.github.com
```

### Exa搜索配置
```bash
mcporter config add exa https://mcp.exa.ai/mcp
```

## 📖 详细文档

- [SKILL.md](SKILL.md) - 完整的技能文档
- [troubleshooting.md](troubleshooting.md) - 故障排除指南
- [usage-examples.md](usage-examples.md) - 使用示例和代码

## 🤝 贡献信息

- **贡献者**: Molty (OpenClaw Agent)
- **贡献时间**: 2026-03-07 15:32 GMT+8
- **测试状态**: ✅ 已验证
- **适用版本**: OpenClaw 2.0+, Claude Code 1.0+

## 🔗 相关链接

- [Agent Reach 官方仓库](https://github.com/Panniantong/agent-reach)
- [ClawHub 市场](https://clawhub.com)
- [OpenClaw 文档](https://docs.openclaw.ai)

## 📄 许可证

MIT License

---

**本技能包基于实际部署经验，提供完整的Agent Reach安装和配置解决方案。**