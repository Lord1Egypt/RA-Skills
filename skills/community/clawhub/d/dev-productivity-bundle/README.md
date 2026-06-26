# 开发者效率套装 - 快速上手指南

## 🚀 5分钟快速开始

### 1. 安装套装

```powershell
git clone https://github.com/clawhub/dev-productivity-bundle.git
cd dev-productivity-bundle
./install.ps1
```

### 2. 配置GitHub

```powershell
cp config/code-review.yaml.template config/code-review.yaml
notepad config/code-review.yaml
```

### 3. 开始开发

```
openclaw run dev-productivity --config ./config
```

---

## 📋 常用命令速查

| 命令 | 功能 |
|------|------|
| `审查这个PR` | 代码审查 |
| `查看Bug情况` | Bug追踪 |
| `生成API文档` | 文档生成 |
| `服务状态` | 部署监控 |
| `分析代码质量` | 质量分析 |

---

## 🔧 故障排除

### GitHub连接失败
- 检查token权限
- 确认webhook配置
- 查看日志排查

### 代码审查不触发
- 检查PR事件配置
- 确认规则启用
- 查看GitHub Actions日志

---

**开始你的AI驱动开发！** 👨‍💻
