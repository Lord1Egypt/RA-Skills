# 柯南周报 Skill 📺🔍

名侦探柯南动画周报技能 - 每周自动收集并整理柯南最新剧情进展

## 🎯 功能

- **自动搜索** - 使用 DuckDuckGo HTML 搜索获取最新柯南资讯（无需 API 密钥）
- **主线追踪** - 关注黑衣组织、APTX-4869 等主线剧情
- **特别篇报道** - 剧场版、特别篇、联动剧集信息
- **角色动态** - 声优变动、角色登场、制作信息
- **本地保存** - 报告自动保存到 `reports/` 目录
- **Webhook 推送** - 支持配置 Webhook 自动发送报告

## 🚀 快速开始

### 安装
```bash
clawhub install conan-weekly-report
```

### 安装依赖
```bash
cd ~/.openclaw/workspace/skills/conan-weekly-report
npm install
```

### 手动运行
```bash
node index.js
```

### 设置定时任务（推荐）
```bash
openclaw cron add \
  --name "柯南周报" \
  --cron "0 21 * * 6" \
  --tz "Asia/Shanghai" \
  --system-event "柯南周报" \
  --session "main"
```

### 配置 Webhook（可选）
```bash
# 设置环境变量
export REPORT_WEBHOOK_URL="https://your-webhook.com/endpoint"
```

## 📁 输出

报告保存在 `~/.openclaw/workspace/skills/conan-weekly-report/reports/` 目录

文件名格式：`conan-report-YYYY-MM-DD.md`

## 🔧 技术实现

- **搜索源**: DuckDuckGo HTML 搜索（无需 API 密钥，真实 HTTP 请求）
- **运行环境**: Node.js 14+
- **依赖**: node-fetch（可选，用于增强 HTTP 功能）
- **网络请求**: 使用 Node.js 内置 `https` 模块进行真实 HTTP 请求
- **解析逻辑**: 正则表达式提取搜索结果标题和链接

## 📋 代码结构

```
conan-weekly-report/
├── index.js          # 主脚本（包含完整网络请求和解析实现）
├── package.json      # 项目元数据
├── SKILL.md          # OpenClaw 技能文档
├── README.md         # 本文件
└── reports/          # 生成的报告目录（运行时创建）
```

## 📡 搜索实现说明

本技能使用 **DuckDuckGo HTML 搜索接口** 进行资讯收集：

1. **无需 API 密钥** - 直接使用公开 HTML 接口
2. **真实 HTTP 请求** - 使用 Node.js `https` 模块发起实际网络请求
3. **结果解析** - 正则表达式提取标题和链接
4. **请求限流** - 内置 1.5 秒延迟避免请求过快
5. **超时保护** - 10 秒超时防止卡死

### 搜索查询示例

```javascript
[
  '名侦探柯南 动画 最新集数 剧情 2026',
  '名侦探柯南 主线剧情 黑衣组织 更新',
  '名侦探柯南 特别篇 剧场版 2026',
  '名侦探柯南 声优 角色 登场'
]
```

## ⚠️ 注意事项

1. **网络依赖** - 需要联网才能搜索最新信息
2. **搜索频率** - 内置 1.5 秒延迟避免请求过快
3. **时区设置** - 确保 cron 时区与你的位置匹配（默认 Asia/Shanghai）
4. **Webhook** - 可选配置，不配置则只保存本地文件
5. **搜索稳定性** - DuckDuckGo HTML 接口可能偶尔不稳定，建议配置备用方案

## 🔍 故障排查

### 搜索结果为空
- 检查网络连接
- 可能是 DuckDuckGo 暂时限制，稍后重试
- 查看 `reports/` 目录中的错误日志

### Webhook 发送失败
- 检查 `REPORT_WEBHOOK_URL` 环境变量是否正确
- 确认 Webhook 端点可公开访问
- 查看控制台输出的错误信息

## 📄 许可证

MIT License

---

*名侦探柯南 © 青山刚昌/小学馆·读卖电视台·TMS*
*本技能仅供学习交流，请勿用于商业用途*
