# 飞书团队管理器发布指南

## 已完成的准备工作

### ✅ 技能完整性检查
- 修复硬编码路径：`/root/.openclaw/` → `~/.openclaw/`
- 添加开源协议：MIT License
- 添加更新日志：CHANGELOG.md
- 添加捐赠信息：SKILL.md 末尾
- 验证文件结构：所有核心文件完整

### ✅ 市场分析
- ClawHub 搜索 "feishu"：无直接竞争技能
- 市场空白：飞书多 Agent 团队管理是刚需
- 技术门槛：基于 2026-04-21 验证的路由方案

## 发布步骤

### 方案 A：使用 API 令牌（推荐）
1. 访问 https://clawhub.com 登录账户
2. 进入 Settings → API Tokens 生成新令牌
3. 运行以下命令：
```bash
cd ~/.openclaw/workspace/skills/feishu-team-manager
clawhub login --token YOUR_API_TOKEN
clawhub publish . \
  --slug "feishu-team-manager" \
  --name "飞书团队管理器 (HR 大姐头)" \
  --version "2.3.0" \
  --changelog "v2.3: 自动化部署、独立工作空间、精准路由绑定" \
  --description "自动化招聘新 Agent，配置独立飞书机器人并重构多账号路由" \
  --tags "feishu,lark,hr,recruitment,agent-management,team"
```

### 方案 B：浏览器登录
1. 运行 `clawhub login`（会自动打开浏览器）
2. 授权登录后，运行上述发布命令

### 方案 C：手动发布
如果上述方法都不可行，可以：
1. 将整个 `feishu-team-manager` 目录打包
2. 在 ClawHub 网站手动上传
3. 填写相同的元数据信息

## 图片上传步骤（发布前必做）

### 1. 上传赞赏码图片到图床
你的微信赞赏码图片已保存到本地，需要上传到公共图床获取 HTTPS URL：

**推荐图床**（任选其一）：
- **imgur.com**（匿名上传，无需注册）
- **sm.ms**（免费，有 API）
- **GitHub**（上传到仓库，获取 raw.githubusercontent.com 链接）
- **你自己的服务器**

### 2. 获取图片 URL
上传后，获取图片的 **HTTPS URL**，例如：
- `https://i.imgur.com/xxxxx.png`
- `https://sm.ms/image/xxxxx`
- `https://raw.githubusercontent.com/yourname/repo/main/donate.png`

### 3. 替换 SKILL.md 中的占位符
编辑 `SKILL.md` 文件末尾，替换：
- `{YOUR_WECHAT_DONATE_URL}` → 你的微信赞赏码图片 URL
- `{YOUR_ALIPAY_DONATE_URL}` → 你的支付宝收款码图片 URL（可选）
- `your-username` → 你的 GitHub 用户名

### 4. 验证图片可访问
在浏览器中打开图片 URL，确保能正常显示。

## 商业化建议

### 起步策略：免费 + 捐赠
1. **立即发布免费技能**，积累用户和口碑
2. **捐赠信息**：使用上面准备好的赞赏码 URL
3. **收集反馈**：迭代开发，准备付费功能

### 高级功能规划（未来收费）
- 企业多租户支持
- 自定义身份模板库
- 批量操作 API
- 优先技术支持

## 推广策略

1. **社区曝光**：
   - OpenClaw Discord `#skills-showcase`
   - 飞书开放平台社区
   - GitHub 仓库（链接到 ClawHub）

2. **内容营销**：
   - 使用教程视频（B站/YouTube）
   - 案例文章（知乎/CSDN）
   - 模板分享（更多身份模板）

3. **收入预估**：
   - 捐赠：¥500-2000/月（100用户，5-20元/人）
   - 付费技能：¥2000-5000/月（200用户，10-25元/人）
   - 定制服务：¥5000+/月（1-2企业客户）

## 技能链接
发布后技能将出现在：https://clawhub.com/skills/feishu-team-manager

## 技术支持
- 问题反馈：GitHub Issues
- 定制需求：微信/邮箱联系
- 更新通知：关注 ClawHub 技能页面