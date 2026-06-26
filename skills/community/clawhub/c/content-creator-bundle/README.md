# 自媒体矩阵套装 - 快速上手指南

## 🚀 5分钟快速开始

### 1. 安装套装

```powershell
# 克隆套装仓库
git clone https://github.com/clawhub/content-creator-bundle.git
cd content-creator-bundle

# 安装所有依赖技能
./install.ps1
```

### 2. 配置平台账号

```powershell
cp config/platforms.yaml.template config/platforms.yaml
notepad config/platforms.yaml
```

### 3. 开始创作

```
openclaw run content-creator --config ./config
```

---

## 📋 常用命令速查

| 命令 | 功能 |
|------|------|
| `改写这篇文章到小红书风格` | 多平台内容改写 |
| `查看本周热门话题` | 热点追踪 |
| `帮我回复评论` | 评论管理 |
| `设置明天8点发布` | 定时发布 |
| `一文多发这篇文章` | 批量生成多平台版本 |

---

## 🔧 故障排除

### 平台授权失败
- 检查账号密码
- 确认API权限已开启
- 重新授权

### 改写效果不佳
- 调整改写规则
- 提供更多上下文
- 尝试不同风格

### 定时发布失败
- 检查cron服务
- 确认时区设置
- 查看发布日志

---

**开始你的自媒体矩阵运营！** 🚀
