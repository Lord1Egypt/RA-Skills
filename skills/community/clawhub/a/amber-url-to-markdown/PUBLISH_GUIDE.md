# Amber Url to Markdown - ClawHub 发布指南

## 版本更新说明

### V3.2.0 (2026-03-25) - 新增自动触发 Hook

**主要更新：**

1. ✅ 新增 `url-auto-fetch` Hook，实现真正的自动触发
2. ✅ 监听 `message:received` 事件，自动检测 URL 链接
3. ✅ 支持纯 URL 消息和 URL + 意图关键词两种触发方式
4. ✅ 异步执行，不阻塞消息处理
5. ✅ 更新 SKILL.md 和 _meta.json，添加 Hook 配置

**文件变更：**

```
amber-url-to-markdown/
├── hooks/                          # 新增目录
│   └── url-auto-fetch/
│       ├── HOOK.md                 # Hook 元数据 + 文档
│       └── handler.ts              # Hook 实现
├── HOOK_AUTO_TRIGGER_README.md     # 新增：Hook 自动触发方案说明
├── PUBLISH_GUIDE.md                # 新增：发布指南（本文件）
├── SKILL.md                        # 更新：添加 Hook 启用说明
└── _meta.json                      # 更新：添加 hooks 配置
```

## 发布步骤

### 1. 更新版本号

更新以下文件中的版本号：

**_meta.json:**
```json
{
  "name": "Amber_Url_to_Markdown",
  "version": "3.2.0",
  "updated_at": "2026-03-25",
  ...
}
```

**package.json (如果有):**
```json
{
  "name": "amber-url-to-markdown",
  "version": "3.2.0",
  ...
}
```

### 2. 更新 CHANGELOG

在 `CHANGELOG.md` 中添加新版本记录：

```markdown
## [3.2.0] - 2026-03-25

### Added
- 新增 `url-auto-fetch` Hook，实现真正的自动触发
- 监听 `message:received` 事件，自动检测 URL 链接
- 支持纯 URL 消息和 URL + 意图关键词两种触发方式
- 异步执行，不阻塞消息处理

### Changed
- 更新 SKILL.md，添加 Hook 启用说明
- 更新 _meta.json，添加 hooks 配置
- 优化触发逻辑，优先处理微信公众号链接

### Fixed
- 修复 AI 无法自动调用技能的问题
- 修复 URL 检测逻辑，支持更多场景
```

### 3. 测试 Hook

在发布前，确保 Hook 可以正常工作：

```bash
# 1. 复制 Hook 到 managed hooks 目录
cp -r hooks/url-auto-fetch ~/.openclaw/hooks/

# 2. 查看 Hook 列表
openclaw hooks list

# 3. 启用 Hook
openclaw hooks enable url-auto-fetch

# 4. 重启 Gateway
openclaw gateway restart

# 5. 发送测试消息
# 在飞书中发送：https://mp.weixin.qq.com/s/xxx

# 6. 验证结果
ls -lt /root/openclaw/urltomarkdown/*.md | head -1
```

### 4. 打包技能

```bash
# 确保所有文件都已提交
cd /root/openclaw/skills/amber-url-to-markdown
git add .
git commit -m "feat: add url-auto-fetch hook for auto-trigger (v3.2.0)"

# 如果使用 ClawHub 发布
clawhub publish
```

### 5. 发布到 ClawHub

#### 方式 1：使用 ClawHub CLI

```bash
# 登录 ClawHub
clawhub login

# 发布新版本
clawhub publish

# 验证发布
clawhub show amber-url-to-markdown
```

#### 方式 2：手动发布

1. 访问 https://clawhub.com
2. 进入技能管理页面
3. 上传新版本（包含 hooks 目录）
4. 填写更新说明
5. 提交审核

### 6. 通知用户更新

发布后，通知已安装用户更新技能：

**更新说明模板：**

```
🎉 Amber Url to Markdown v3.2.0 发布！

✨ 新增功能：
- 自动触发 Hook：安装后启用 Hook，发送 URL 自动抓取
- 支持纯 URL 消息和 URL + 意图关键词
- 异步执行，不阻塞消息处理

📦 更新方式：
clawhub update amber-url-to-markdown

🔧 启用自动触发：
openclaw hooks enable url-auto-fetch
openclaw gateway restart

📖 详细文档：
https://github.com/OrangeViolin/amber-url-to-markdown/blob/main/HOOK_AUTO_TRIGGER_README.md
```

## 用户安装流程

### 新用户

```bash
# 1. 安装技能
clawhub install amber-url-to-markdown

# 2. 安装依赖
pip install playwright beautifulsoup4 markdownify requests scrapling
playwright install chromium

# 3. 启用自动触发（推荐）
openclaw hooks enable url-auto-fetch
openclaw gateway restart

# 完成！现在发送 URL 会自动抓取
```

### 老用户升级

```bash
# 1. 更新技能
clawhub update amber-url-to-markdown

# 2. 启用新 Hook
openclaw hooks enable url-auto-fetch

# 3. 重启 Gateway
openclaw gateway restart

# 完成！
```

## Hook 配置说明

### 默认配置

Hook 使用以下默认配置：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "url-auto-fetch": {
          "enabled": true,
          "trigger_on_pure_url": true,
          "trigger_on_intent_keywords": true
        }
      }
    }
  }
}
```

### 自定义配置

用户可以通过配置文件自定义触发行为：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "url-auto-fetch": {
          "enabled": true,
          "trigger_on_pure_url": true,
          "trigger_on_intent_keywords": false,  // 只处理纯 URL 消息
          "allowed_domains": ["mp.weixin.qq.com", "zhihu.com"],  // 只处理特定网站
          "notify_on_complete": true  // 抓取完成后通知
        }
      }
    }
  }
}
```

## 常见问题

### Q1: Hook 未生效？

**检查步骤：**

```bash
# 1. 确认 Hook 已启用
openclaw hooks list

# 2. 确认 Gateway 已重启
openclaw gateway status

# 3. 查看 Hook 日志
tail -f ~/.openclaw/gateway.log | grep url-auto-fetch

# 4. 测试触发条件
# 发送纯 URL 消息测试
```

### Q2: 抓取失败？

**检查步骤：**

```bash
# 1. 检查 Python 依赖
pip list | grep -E "playwright|beautifulsoup4|scrapling"

# 2. 检查 Playwright 浏览器
playwright install chromium

# 3. 手动运行脚本测试
python3 /root/openclaw/skills/amber-url-to-markdown/scripts/amber_url_to_markdown.py https://mp.weixin.qq.com/s/xxx

# 4. 查看脚本输出
ls -lt /root/openclaw/urltomarkdown/*.md | head -1
```

### Q3: 如何禁用自动触发？

```bash
# 禁用 Hook
openclaw hooks disable url-auto-fetch

# 重启 Gateway
openclaw gateway restart
```

## 技术细节

### Hook 触发流程

```
用户发送消息
    ↓
Gateway 接收 (message:received)
    ↓
Hook handler 执行
    ↓
检测 URL (正则匹配)
    ↓
判断触发条件
├─ 纯 URL → 触发
├─ URL + 关键词 → 触发
└─ 其他 → 跳过
    ↓
执行 Python 脚本 (异步)
    ↓
保存 Markdown 文件
    ↓
(可选) 发送完成通知
```

### 触发条件判断

```typescript
// URL 匹配正则
const urlPattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi;

// 纯 URL 判断
const isPureUrl = content.trim().replace(urlPattern, "").trim().length === 0;

// 意图关键词判断
const intentKeywords = ["解析", "转换", "转成", "markdown", "md", ...];
const hasIntentKeyword = intentKeywords.some(k => content.toLowerCase().includes(k));

// 触发条件
const shouldTrigger = isPureUrl || hasIntentKeyword;
```

## 后续优化计划

- [ ] 支持自定义触发关键词（用户配置）
- [ ] 支持 URL 白名单/黑名单
- [ ] 抓取完成后主动发送通知
- [ ] 支持并发控制（限制同时抓取数量）
- [ ] 支持缓存（已抓取的 URL 不重复抓取）
- [ ] 支持批量抓取（多条 URL 消息）

## 参考资料

- [OpenClaw Hooks 文档](https://docs.openclaw.ai/automation/hooks)
- [OpenClaw CLI 参考](https://docs.openclaw.ai/cli/hooks)
- [Bundled Hooks 示例](https://github.com/openclaw/openclaw/tree/main/src/hooks/bundled)
- [ClawHub 发布指南](https://clawhub.com/docs/publish)

---

**发布检查清单：**

- [ ] 更新版本号（_meta.json）
- [ ] 更新 CHANGELOG.md
- [ ] 测试 Hook 功能
- [ ] 更新 SKILL.md 文档
- [ ] 提交代码到 Git
- [ ] 发布到 ClawHub
- [ ] 通知用户更新
- [ ] 监控用户反馈
