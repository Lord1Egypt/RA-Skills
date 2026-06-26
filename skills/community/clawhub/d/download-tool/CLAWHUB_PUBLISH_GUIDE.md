# ClawHub 技能发布检查清单

## 📋 发布前检查

### ✅ 已完成项

- [x] **核心文件**: `SKILL.md` 已存在
- [x] **元数据**: `_meta.json` 已配置
- [x] **脚本文件**: `scripts/download_video.py` 已存在
- [x] **技能描述**: YAML Frontmatter 已配置
- [x] **使用文档**: SKILL.md 包含使用说明

---

## 🔍 ClawHub 发布要求

### 1. **账户要求**
- ✅ 需要 GitHub 账户
- ⚠️ **账户注册时间必须 ≥ 1 周**
- ✅ 需要使用 `clawhub login` 登录

### 2. **文件结构要求**
```
download-tool/
├── SKILL.md           ✅ 必需：技能定义文件
├── _meta.json         ✅ 可选：元数据配置
└── scripts/           ✅ 可选：脚本目录
    └── download_video.py
```

### 3. **SKILL.md 格式要求**
```yaml
---
name: download-tool
description: 支持下载 YouTube、TikTok、小红书、抖音等平台的视频
---
```

✅ **当前状态**: 已符合要求

---

## ⚠️ 当前存在的问题

### 🔴 问题1：依赖外部服务

**问题描述**：
- 技能依赖 `https://www.datamass.cn/ai-back` 外部服务
- 需要 API Key 才能使用
- 不是通用的独立技能

**ClawHub 规范**：
- 技能应该是**自包含**的，不依赖特定私有服务
- 或者明确说明依赖的外部服务和获取方式

**建议修复**：
1. 在 SKILL.md 中**明确说明**依赖的外部服务
2. 提供获取 API Key 的公开途径
3. 或者提供**本地部署方案**

---

### 🟡 问题2：缺少版本标签

**问题描述**：
- `_meta.json` 中有版本号，但缺少标签
- ClawHub 推荐使用标签管理版本

**建议修复**：
```json
{
  "ownerId": "kn7c56fmw1b0xy60rz75be0ds1816468",
  "slug": "download-tool",
  "version": "1.0.0",
  "tags": ["video", "download", "youtube", "tiktok", "media"],
  "publishedAt": 1742025600000
}
```

---

### 🟡 问题3：缺少 README 或使用示例

**问题描述**：
- SKILL.md 中有使用说明，但缺少完整的使用示例
- 新用户可能不知道如何配置

**建议添加**：
- 详细的配置步骤
- API Key 获取流程截图
- 常见问题 FAQ

---

## 🔧 发布前需要修改的内容

### 1. **更新 SKILL.md**

添加以下内容：

```markdown
## ⚠️ 重要说明

本技能依赖外部服务：
- **服务地址**: https://www.datamass.cn/ai-back
- **认证方式**: API Key
- **获取方式**: 
  1. 访问 https://www.datamass.cn 注册账号
  2. 登录后在个人中心创建 API Key
  3. 将 API Key 配置到 `~/.openclaw/config.json`

## 费用说明

- 下载服务按文件大小计费
- 50MB 以内免费
- 超过 50MB 按阶梯收费（详见官网）
- 需要充值积分后使用

## 本地部署（可选）

如果你想自己部署服务：
1. 克隆 NBCIO-Boot 项目
2. 配置 OSS 存储和数据库
3. 启动后端服务
4. 修改配置文件中的 `download_tool_base_url` 为本地地址
```

---

### 2. **完善 _meta.json**

```json
{
  "ownerId": "你的GitHub用户ID",
  "slug": "download-tool",
  "version": "1.0.0",
  "name": "Video Download Tool",
  "description": "下载 YouTube、TikTok、抖音、小红书等平台的视频",
  "author": "你的名字",
  "tags": ["video", "download", "youtube", "tiktok", "douyin", "xiaohongshu", "media"],
  "license": "MIT",
  "repository": "https://github.com/你的用户名/download-tool",
  "homepage": "https://github.com/你的用户名/download-tool#readme",
  "publishedAt": 1742025600000
}
```

---

## 📝 发布步骤

### 步骤1: 安装 ClawHub CLI

```bash
npm install -g @openclaw/clawhub-cli
# 或
yarn global add @openclaw/clawhub-cli
```

### 步骤2: 登录 ClawHub

```bash
clawhub login
# 会打开浏览器进行 GitHub 授权
```

### 步骤3: 发布技能

```bash
cd e:\project_aliyun_yunxiao\nbcio-boot\nbcio-boot-module-system\skills

clawhub publish download-tool \
  --slug download-tool \
  --name "Video Download Tool" \
  --version 1.0.0 \
  --changelog "首次发布：支持 YouTube、TikTok、抖音、小红书视频下载" \
  --tags "video,download,youtube,tiktok,douyin,xiaohongshu,media"
```

### 步骤4: 验证发布

访问 https://clawhub.com/skills/download-tool 查看发布结果

---

## ⚖️ 是否适合发布到 ClawHub？

### ✅ 适合发布的理由：
1. 功能完整，代码质量高
2. 文档清晰，使用说明详细
3. 支持多个主流视频平台
4. 有实际使用价值

### ⚠️ 需要注意的问题：
1. **依赖外部服务** - 不是完全独立的技能
2. **需要付费** - 用户需要充值积分
3. **配置复杂** - 需要获取 API Key 和配置文件

### 💡 建议：

**方案A：发布到 ClawHub（推荐）**
- ✅ 可以让更多用户知道这个工具
- ✅ 方便分享和推广
- ⚠️ 需要在文档中**明确说明**依赖和费用

**方案B：仅内部使用**
- ✅ 避免用户混淆
- ✅ 减少维护成本
- ❌ 无法让社区受益

**方案C：开源完整方案**
- ✅ 提供 Docker 部署方案
- ✅ 用户可以自己搭建服务
- ✅ 完全自包含
- ⚠️ 需要额外开发和文档工作

---

## 🎯 最终建议

**建议发布到 ClawHub，但需要先完成以下修改**：

1. ✅ 更新 SKILL.md，添加依赖说明和费用信息
2. ✅ 完善 _meta.json，添加标签和作者信息
3. ✅ 添加 README，提供详细的配置和使用指南
4. ✅ 提供问题反馈渠道（如 GitHub Issues）

完成以上修改后，即可安全发布到 ClawHub！

---

## 📚 参考资料

- [ClawHub 官方文档](https://docs.openclaw.ai/tools/clawhub)
- [创建自定义技能](https://docs.openclaw.ai/tools/creating-skills)
- [ClawHub 网站](https://clawhub.com)

---

**生成时间**: 2026-03-18
**技能版本**: 1.0.0
**检查状态**: ✅ 基本符合，建议优化后发布
