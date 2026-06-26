---
name: clawhub-publisher
description: >
  将本地 skill 目录发布到 clawhub.com 的自动化发布助手。
  当用户说"发布这个 skill 到 clawhub"、"把 XX skill 上传到 clawhub"、
  "clawhub publish"、"发布到 clawhub" 等时触发。
  自动处理：token 验证、CLI bug patch、slug 冲突、频率限制重试。
author: antonia-sz
version: 1.0.0
---

# ClawHub Publisher — Skill 自动发布器

把本地 skill 目录一键发布到 clawhub.com，自动处理所有已知坑。

---

## 需要用户提供

| 参数 | 说明 | 示例 |
|------|------|------|
| `skill 目录路径` | 本地 skill 文件夹（必须包含 SKILL.md） | `/root/.openclaw/workspace/skills/SKILL-xxx` |
| `clawhub token` | 格式 `clh_xxx`，clawhub.com → Profile → API Keys 获取 | `clh_7XoVic...` |
| `slug` | URL 名称，全小写+连字符 | `my-skill-name` |
| `displayName` | 展示名称 | `My Skill — 一句话描述` |
| `tags` | 逗号分隔（可选） | `productivity,writing` |

如果缺少任何必填项，**只问缺少的那个**，不要重复已知信息。

---

## 执行流程

### Step 1：环境检查

```bash
# 确认 clawhub CLI 已安装
which clawhub || npm install -g clawhub
clawhub --version

# 确认 skill 目录存在且包含 SKILL.md
ls {skill_dir}/SKILL.md
```

### Step 2：Patch CLI（如需要）

clawhub CLI 存在一个 bug：publish 时 payload 缺少 `acceptLicenseTerms: true`，服务端会返回 400。

检查并修复：

```bash
PUBLISH_JS=$(find /usr/local/lib /usr/lib -name "publish.js" -path "*/clawhub/*" 2>/dev/null | head -1)

# 检查是否已 patch
grep -q "acceptLicenseTerms" "$PUBLISH_JS" && echo "已 patch" || \
  # 在 payload 构建处加入 acceptLicenseTerms: true
  sed -i 's/skillName:/acceptLicenseTerms: true, skillName:/' "$PUBLISH_JS" && echo "patch 完成"
```

> 💡 patch 是幂等的，重复执行无害。

### Step 3：查重（可选但推荐）

```bash
# 用 knot_skills 搜索是否已有同名/同功能 skill
knot_skills search "{slug关键词}"
```

如果发现完全重复的 skill，告知用户，询问是否继续（换 slug 或放弃）。

### Step 4：执行发布

```bash
CLAWHUB_TOKEN={token} \
clawhub publish {skill_dir} \
  --slug {slug} \
  --name "{displayName}" \
  --version {version:-1.0.0} \
  --changelog "{changelog:-Initial release}" \
  --tags "{tags:-latest}"
```

### Step 5：错误处理

遇到以下错误时，按对应方案处理：

**`Error: Path must be a folder`**
→ 检查传入的是目录路径还是文件路径，修正后重试

**`slug already taken` / `409`**
→ 在 slug 后加 `-v2` 或更具体的后缀，询问用户确认后重试

**`rate limit exceeded` / `429`**
→ 使用 qqbot-cron skill 创建定时重试任务：
```
约 65 分钟后执行相同的 publish 命令
任务名：clawhub-publish-retry-{slug}
完成后通知用户
```

**`400 Bad Request`（含 acceptLicenseTerms）**
→ 重新执行 Step 2 的 patch，再重试

**`401 Unauthorized`**
→ token 无效或已过期，请用户在 clawhub.com 重新生成

### Step 6：验证上架

```bash
knot_skills search "{slug}"
```

发布成功后回复：
```
✅ 发布成功：{displayName}
📦 slug：{slug}
🌐 https://clawhub.com/skills/{slug}
安装命令：clawhub install {slug}
```

---

## 快速调用示例

用户说：
> "把 /workspace/skills/SKILL-my-tool 发布到 clawhub，token 是 clh_abc，slug 用 my-tool"

直接执行 Step 1-6，完成后汇报结果，无需逐步确认。
