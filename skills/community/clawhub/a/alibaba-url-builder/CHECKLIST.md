# 📋 alibaba-sourcing 发布清单

## ✅ 发布前检查

### 文件完整性
- [x] SKILL.md - 技能文档（含 frontmatter 元数据）
- [x] README.md - GitHub 和 ClawHub 展示文档
- [x] LICENSE - MIT-0 许可证
- [x] .gitignore - Git 忽略文件
- [x] scripts/build_url.py - URL 构建辅助脚本
- [x] scripts/package_skill.py - 技能打包脚本
- [x] PUBLISH.md - 发布指南
- [x] PROMOTION.md - 宣传材料
- [x] alibaba-sourcing.skill - 打包好的技能文件

### SKILL.md Frontmatter
```yaml
name: alibaba-sourcing
version: 1.0.0
description: Build Alibaba.com URLs for agent navigation with traffic tracking
author: Zhou Zeyu (@zhouzeyu)
license: MIT-0
tags: [alibaba, ecommerce, url-builder, agent-navigation, b2b, sourcing, traffic-tracking]
```

### 功能测试
- [x] 搜索 URL 生成测试通过
- [x] 商品详情 URL 生成测试通过
- [x] 供应商 URL 生成测试通过
- [x] 特殊页面 URL 生成测试通过
- [x] 所有 URL 包含 `traffic_type=ags_llm` 参数

---

## 🚀 发布步骤

### 步骤 1: 安装 ClawHub CLI
```bash
npm install -g clawhub
# 或
npx clawhub@latest --version
```

### 步骤 2: 登录 ClawHub
```bash
clawdhub login
```
- 会自动打开浏览器
- 使用 GitHub 账号授权
- 授权完成后返回 CLI

### 步骤 3: 验证登录
```bash
clawdhub whoami
```
应显示你的 GitHub 用户名。

### 步骤 4: 发布到 ClawHub
```bash
cd /Users/zhouzeyu/.openclaw/workspace-code/alibaba-sourcing

clawdhub publish . --version 1.0.0 --tags latest --changelog "Initial release: Alibaba.com URL builder with traffic tracking (traffic_type=ags_llm). Includes 10+ URL patterns, Python CLI helper, and complete documentation."
```

### 步骤 5: 验证发布
```bash
# 搜索 skill
clawdhub search alibaba-sourcing

# 查看详情
clawdhub inspect alibaba-sourcing

# 在浏览器查看
open https://clawhub.ai/skills/alibaba-sourcing
```

### 步骤 6: 创建 GitHub 仓库
```bash
cd /Users/zhouzeyu/.openclaw/workspace-code/alibaba-sourcing

# 初始化 Git
git init
git add .
git commit -m "Initial release: alibaba-sourcing skill for OpenClaw

Features:
- 10+ URL patterns for Alibaba.com navigation
- Automatic traffic tracking (traffic_type=ags_llm)
- Python CLI helper script
- Complete documentation
- MIT-0 license"

# 创建远程仓库（在 GitHub 上手动创建或使用 gh CLI）
# gh repo create openclaw-skill-alibaba-sourcing --public --source=. --remote=origin --push
git remote add origin https://github.com/zhouzeyu/openclaw-skill-alibaba-sourcing.git
git branch -M main
git push -u origin main
```

---

## 📢 宣传发布

### 渠道 1: OpenClaw Discord
- [ ] 加入 Discord: https://discord.com/invite/clawd
- [ ] 在 #skills 频道发布消息（见 PROMOTION.md）
- [ ] 在 #showcase 频道分享截图
- [ ] 回复社区反馈

### 渠道 2: Twitter / X
- [ ] 发布推文（见 PROMOTION.md 文案）
- [ ] 带上话题：#OpenClaw #AI #Agent #Alibaba
- [ ] @OpenClaw 官方账号
- [ ] 回复相关讨论

### 渠道 3: LinkedIn
- [ ] 发布专业文章（见 PROMOTION.md 文案）
- [ ] 添加到个人项目经历
- [ ] 分享给相关群组

### 渠道 4: GitHub
- [ ] 添加话题标签：openclaw, openclaw-skill, alibaba
- [ ] 完善 README 展示
- [ ] 启用 Issues 功能
- [ ] 添加到个人 Profile 的置顶项目

### 渠道 5: 中文社区
- [ ] 微信群/朋友圈分享（见 PROMOTION.md）
- [ ] 知乎专栏文章
- [ ] V2EX 分享
- [ ] 掘金技术文章

---

## 📊 追踪指标

### 第一周目标
| 指标 | 目标 | 实际 |
|------|------|------|
| ClawHub 安装数 | 10+ | - |
| GitHub Stars | 5+ | - |
| Discord 反馈 | 3+ | - |
| Twitter 互动 | 20+ | - |

### 第一个月目标
| 指标 | 目标 | 实际 |
|------|------|------|
| ClawHub 安装数 | 50+ | - |
| GitHub Stars | 20+ | - |
| GitHub Forks | 5+ | - |
| Issue/PR | 2+ | - |

---

## 🔄 后续维护

### 版本更新流程
1. 收集用户反馈和功能请求
2. 在本地开发新功能
3. 更新 SKILL.md 中的 version
4. 更新 CHANGELOG（可添加到 README）
5. 发布新版本到 ClawHub

```bash
# 示例：发布小版本更新
clawdhub publish . --version 1.1.0 --tags latest --changelog "Added new URL patterns for X, improved Y"

# 或使用自动版本号
clawdhub publish . --bump minor --tags latest
```

### 文档维护
- [ ] 定期更新 README 示例
- [ ] 响应用户 Issue
- [ ] 更新分类 ID 列表（如有变化）
- [ ] 添加新的 URL 模式

---

## 📝 发布日志

| 日期 | 操作 | 备注 |
|------|------|------|
| 2026-03-17 | 创建 skill | 初始版本 1.0.0 |
| 2026-03-17 | 打包完成 | alibaba-sourcing.skill (14.5 KB) |
| 2026-03-17 | 准备发布材料 | README, LICENSE, PUBLISH.md, PROMOTION.md |
| - | - | - |

---

## 🎯 成功标准

发布成功的标志：

1. ✅ ClawHub 页面正常显示
2. ✅ `clawdhub install alibaba-sourcing` 可正常安装
3. ✅ 所有 URL 生成功能正常工作
4. ✅ GitHub 仓库创建完成
5. ✅ 至少 3 个渠道完成宣传
6. ✅ 收到至少 1 条社区反馈

---

## 📞 联系信息

**作者**: Zhou Zeyu (@zhouzeyu)
- GitHub: https://github.com/zhouzeyu
- 时区：Asia/Shanghai
- 语言：中文 / English

**项目链接**:
- ClawHub: https://clawhub.ai/skills/alibaba-sourcing
- GitHub: https://github.com/zhouzeyu/openclaw-skill-alibaba-sourcing
- OpenClaw: https://openclaw.ai
- 社区 Discord: https://discord.com/invite/clawd

---

**祝发布顺利！🚀**
