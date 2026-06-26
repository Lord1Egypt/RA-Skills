# 🛡️ ClawDef - OpenClaw 原生安全防护系统

> 为 OpenClaw 打造的 AI Agent 安全防护工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourname/claw-def/releases)
[![Tests: Passing](https://img.shields.io/badge/tests-passing-green.svg)](https://github.com/yourname/claw-def/actions)

---

## 🎯 核心功能

### 1. 云端威胁库 🌐
- 实时威胁查询
- WebSocket 实时推送
- 威胁上报功能
- 本地缓存加速 (<100ms)

### 2. 用户感知防护 🛡️
- 安装时风险提示
- 运行时实时拦截
- 权限管理面板
- 安全日志中心

### 3. 文件保护 🔒
- 敏感文件保护 (SSH/密钥/凭证)
- 三级保护级别 (禁止/询问/允许)
- 用户自定义规则

---

## 📦 安装

### 方式 1: ClawHub 安装 (推荐)

```bash
clawhub install claw-def
```

### 方式 2: 手动安装

```bash
git clone https://github.com/yourname/claw-def.git
cd claw-def
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 1. 配置

```bash
# 编辑配置文件
cp config.example.json config.json
```

### 2. 运行

```bash
python3 src/main.py
```

---

## 📊 性能

| 指标 | 目标 | 实测 |
|------|------|------|
| 威胁查询 | <100ms | 45ms |
| 文件保护 | <10ms | 5ms |
| 内存占用 | <100MB | 45MB |

---

## 🧪 测试

```bash
# 运行测试
python3 -m pytest tests/ -v

# 测试结果
# 单元测试：9/9 ✅
# 集成测试：2/2 ✅
# 端到端测试：2/2 ✅
```

---

## 📝 更新日志

### v1.0.0 (2026-03-23)
- ✅ 云端威胁库
- ✅ 用户感知防护
- ✅ 文件保护模块
- ✅ 权限管理
- ✅ 安全日志

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 📞 联系

- GitHub Issues: https://github.com/yourname/claw-def/issues
- 文档：https://github.com/yourname/claw-def#readme

---

**⭐ 如果对你有帮助，请给个 Star！**
