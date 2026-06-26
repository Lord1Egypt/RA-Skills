# Agent Reach 完整安装与配置解决方案

## 概述
本技能包提供Agent Reach的完整安装和配置流程，基于实际部署经验，包含问题诊断和解决方案。适用于OpenClaw、Claude Code等AI Agent环境。

## 核心功能
- ✅ Agent Reach 1.3.0 完整安装
- ✅ 7个核心渠道自动配置
- ✅ 常见问题诊断和解决方案
- ✅ 系统兼容性处理
- ✅ 多环境支持（OpenClaw、Claude Code）

## 安装流程

### 步骤1: 安装Agent Reach
```bash
# 解决权限问题
pip install https://github.com/Panniantong/agent-reach/archive/main.zip --break-system-packages
```

### 步骤2: 自动配置
```bash
agent-reach install --env=auto
```

### 步骤3: 验证安装
```bash
agent-reach doctor
```

### 步骤4: 额外配置（可选）
```bash
# 配置Exa搜索
mcporter config add exa https://mcp.exa.ai/mcp
```

## 已验证的解决方案

### 问题1: 系统包管理限制
**症状**: `externally-managed-environment` 错误
**解决方案**: 使用 `--break-system-packages` 参数
**原因**: Python 3.13+ 默认启用外部包管理保护

### 问题2: GitHub CLI 安装失败
**症状**: 权限不足或安装失败
**解决方案**: 提供手动安装选项，不强制自动安装
**手动安装**: https://cli.github.com

### 问题3: Exa搜索配置
**症状**: mcporter已装但Exa未配置
**解决方案**: `mcporter config add exa https://mcp.exa.ai/mcp`

## 配置选项

### 基础配置（7个渠道）
- ✅ **YouTube** - 视频和字幕提取
- ✅ **RSS/Atom** - 订阅源读取
- ✅ **全网语义搜索** - Exa搜索（免费）
- ✅ **任意网页** - Jina Reader支持
- ✅ **Twitter/X** - 推文搜索和读取
- ✅ **B站** - 视频和字幕提取
- ✅ **微信公众号** - 文章搜索和阅读

### 可选配置（需要额外步骤）
- 🔧 **GitHub** - gh CLI（需手动安装）
- 🔧 **小红书** - Docker容器
- 🔧 **抖音** - douyin-mcp-server
- 🔧 **LinkedIn** - linkedin-scraper-mcp
- 🔧 **Boss直聘** - mcp-bosszp
- 🔧 **Reddit** - 需要代理配置

## 使用示例

### 检查系统状态
```bash
agent-reach doctor
```

### 监控更新和渠道状态
```bash
agent-reach watch
```

### 配置代理（可选）
```bash
agent-reach configure proxy http://user:pass@ip:port
```

## 适用环境
- **操作系统**: Linux 6.17.0-14-generic, Ubuntu 24.04+
- **Python**: 3.13+
- **Node.js**: 22+
- **环境**: OpenClaw, Claude Code, 通用AI Agent环境

## 技能包内容
- `install.sh` - 自动化安装脚本
- `config.json` - 默认配置文件
- `troubleshooting.md` - 问题诊断指南
- `usage-examples.md` - 使用示例
- `SKILL.md` - 本技能文档

## 安装验证
```bash
# 验证7个核心渠道
agent-reach doctor | grep "✅"

# 验证技能安装路径
ls -la /home/pan/.openclaw/skills/agent-reach/
ls -la /home/pan/.claude/skills/agent-reach/
```

## 贡献信息
- **贡献者**: Molty (OpenClaw Agent)
- **安装时间**: 2026-03-07 15:32 GMT+8
- **测试状态**: ✅ 已验证
- **适用版本**: OpenClaw 2.0+, Claude Code 1.0+
- **技能类型**: 工具安装与配置

## 版本历史
- **1.0.0** (2026-03-07): 初始版本，包含完整安装流程和解决方案

---

**本技能包基于实际部署经验，提供完整的Agent Reach安装和配置解决方案，包含各种问题的实际解决方法。**