# 🚀 Tencent SkillHub — Publishing Guide
## Cultural Naming & AI Art Creation v2.0.0

This guide walks you through publishing the **Cultural Naming & AI Art Creation** skill to Tencent SkillHub (skillhub.cloud.tencent.com) and the global ClawHub (clawhub.ai).

---

## 📁 Required Files (already prepared)

```
cultural-naming-art/
├── .trae/skills/cultural-naming-art/
│   ├── SKILL.md                        ✅ 核心行为规范（必需）
│   ├── openclaw_config.yaml             ✅ OpenClaw/Lobster Claw 配置
│   ├── tencent_skilhub_manifest.json   ✅ 腾讯 SkilHub 清单（必需）
│   └── requirements.txt                 ✅ Python 依赖（可选）
├── skill.py                            ✅ Python 核心逻辑
├── prompts.py                          ✅ 艺术提示词库
├── cultural-naming-art-README.md        ✅ GitHub 仓库说明
└── DEPLOYMENT_GUIDE.md                ✅ 本文件
```

---

## 🅰️ Option A: Publish via GitHub Import (Recommended)

### Step 1: Create a Public GitHub Repository

```
Create new repo on GitHub: https://github.com/new
Repo name: cultural-naming-art
Description: "Transform a foreign identity into a Chinese cultural masterpiece"
Visibility: Public ⭐
Add README: YES | Add .gitignore: Python
```

### Step 2: Push All Files to GitHub

```bash
cd /Users/admin/WorkBuddy/20260517145203

git init
git add .
git commit -m "feat: Cultural Naming & AI Art Creation v2.0.0

- Chinese name generation (semantic-phonetic fusion)
- Jueju (七言绝句) & Lüshi (七言律诗) poetry
- Seal carving art prompts (篆刻)
- Shanshui landscape prompts (水墨山水)
- Ancient portrait avatar prompts (古风人物头像)
- 200+ taboo character safety filter
- OpenClaw + Tencent SkilHub compatible"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cultural-naming-art.git
git push -u origin main
```

### Step 3: Publish to Tencent SkillHub

1. **访问发布页面：**
   - 腾讯 SkillHub: `https://skillhub.cloud.tencent.com/developer/publish`
   - 或全局版: `https://clawhub.ai/import`

2. **选择 "Import from GitHub" 标签页**

3. **填写表单：**

| 字段 | 填写内容 |
|------|----------|
| **GitHub URL** | `https://github.com/YOUR_USERNAME/cultural-naming-art` |
| **Skill Name** | `cultural-naming-art` |
| **Display Name** | `Cultural Naming & AI Art Creation` |
| **Description** | `Transform a foreign name into a complete Chinese cultural identity. Chinese names, Tang/Song poetry, seal carving art, ink-wash landscapes, ancient portrait avatars.` |
| **Category** | `Culture & Art` |
| **Tags** | `chinese-name, poetry, seal, shanshui, ai-art, china-travel` |
| **Version** | `2.0.0` |
| **License** | `MIT` |

4. **点击 "Detect" 自动填充** → 检查所有字段是否正确

5. **审核说明：**
```
This skill transforms foreign tourist identities into complete Chinese
cultural masterpieces. Features: semantic Chinese naming, Jueju/Lüshi
poetry generation, seal carving, Shanshui landscape, and ancient
portrait avatar art prompts. Includes 200+ taboo character filter
for cultural safety.
```

6. **点击 "Publish Skill"**

7. **确认发布成功** → 技能 URL：
```
https://skillhub.cloud.tencent.com/skills/cultural-naming-art
```

---

## 🅱️ Option B: Direct Folder Upload

### Step 1: Prepare Upload Folder

```bash
mkdir -p /tmp/cultural-naming-art-upload
cp -r /Users/admin/WorkBuddy/20260517145203/.trae/skills/cultural-naming-art/* \
  /tmp/cultural-naming-art-upload/
```

### Step 2: 上传到 SkillHub

1. 访问 `https://clawhub.ai/import`
2. 选择 **"Upload Folder"** 标签页
3. 拖拽上传文件夹
4. 填写与 Option A 相同的表单字段
5. 点击 **"Publish Skill"**

---

## ⚠️ 常见问题排查

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Slug must be lowercase` | Slug 包含大写字母 | 改为全小写：`cultural-naming-art` |
| `Remove non-text files` | 包含 `.git`、`LICENSE` 等 | 删除非文本文件后重新上传 |
| `SKILL.md not found` | 根目录找不到 SKILL.md | 确保 SKILL.md 在仓库根目录 |
| `Invalid manifest JSON` | manifest 格式错误 | 检查 JSON 语法，确保无尾随逗号 |
| `GitHub API rate limit` | GitHub 请求超限 | 等待10分钟或改用文件夹上传 |
| `Connection lost` | 网络波动 | 刷新页面，精简文件后重试 |

---

## ✅ 发布前检查清单

```
Pre-publish Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] GitHub 仓库已设为 Public（公开）
[ ] SKILL.md 在仓库根目录
[ ] tencent_skilhub_manifest.json 已包含所有6个模块定义
[ ] 所有触发词（Trigger Phrases）已填写中英文
[ ] 版本号格式正确（SemVer: x.y.z）
[ ] 无 .git / .DS_Store / LICENSE 等非文本文件
[ ] manifest JSON 格式验证通过（jsonlint.com）
[ ] skill 描述已填写（3句话以上）
[ ] 至少3个示例用法（Example Utterances）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔗 发布后验证

```
腾讯 SkillHub:    https://skillhub.cloud.tencent.com/skills/cultural-naming-art
全局 ClawHub:     https://clawhub.ai/skills/cultural-naming-art
GitHub 仓库:      https://github.com/YOUR_USERNAME/cultural-naming-art
```

---

*Guide v1.0.0 — Published for Tencent SkillHub & ClawHub*
