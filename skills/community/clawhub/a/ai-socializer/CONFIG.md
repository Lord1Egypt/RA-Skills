# AI Socializer — 本地配置记录
> 本文件为本地安装记录，不受 clawhub 更新影响。
> 每次 skill 更新时请比对本文档与 SKILL.md 是否一致。

---

## 🔑 必需环境变量

| 变量名 | 用途 | 状态 |
|--------|------|------|
| `AI_SOCIAL_API_KEY` | 社交平台 API 认证密钥 | ❌ 未配置 |

### 配置方法

```bash
# 方式 1：写入 ~/.bashrc 或 ~/.zshrc（永久）
echo 'export AI_SOCIAL_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc

# 方式 2：仅当前终端生效
export AI_SOCIAL_API_KEY="your_key_here"
```

### ⚠️ 安全建议

- **使用专用测试账户密钥**，不要使用主账户密钥
- **不要**将生产环境的主 API Key 配置在此
- 密钥仅发送至 SKILL.md 白名单中的域名

---

## ✅ 平台接入状态

| 平台 | 状态 | API Base URL |
|------|------|-------------|
| Moltbook | ✅ 已接入（白名单硬编码） | `https://www.moltbook.com/api/v1` |
| 抓虾吧 | ❌ 未接入（需完成验证流程） | 禁止使用 |

---

## 📋 最近修改记录

| 日期 | 修改内容 | 原因 |
|------|---------|------|
| 2026-04-30 | 移除"运行时用户提供API"；新增域名白名单；新增铁律5；新增 zhuaxia8.md；更新目录结构说明 | 安全加固：防止API Key发送至恶意域名 |
