# AutoDream 手动发布指南

## 当前状态

✅ 技能已创建完成
✅ 所有 AGENT 已可用（全局共享）
✅ 发布包已准备：`/tmp/autodream-v1.0.0.zip`
⏳ 待发布到 registry

---

## 方法 1：发布到 ClawHub（推荐）

### 步骤 1：获取 ClawHub Token

1. 访问 https://clawhub.ai
2. 登录账号
3. 进入 Settings → API Tokens
4. 创建新 token，复制保存

### 步骤 2：使用 CLI 发布

```bash
# 登录
clawhub login --token <YOUR_TOKEN> --label "research-agent-autodream"

# 发布技能
clawhub publish /root/.openclaw/workspace-research/skills/autodream
```

### 步骤 3：验证发布

```bash
clawhub search autodream
```

---

## 方法 2：发布到 SkillHub

### 步骤 1：准备技能元数据

创建 `skill-metadata.json`：

```json
{
  "slug": "autodream",
  "name": "AutoDream",
  "description": "自动记忆整理子代理，定期整理 MEMORY.md，去重合并删除过时条目",
  "description_en": "Automatic memory consolidation sub-agent for OpenClaw",
  "version": "1.0.0",
  "author": "research AGENT",
  "license": "MIT",
  "keywords": ["memory", "consolidation", "autodream", "organization"],
  "downloadUrl": "https://github.com/your-username/autodream/archive/main.zip",
  "homepage": "https://github.com/your-username/autodream"
}
```

### 步骤 2：提交到 SkillHub

发送邮件或消息给 SkillHub 维护者：

**收件人**: skillhub@lightmake.site（示例）
**主题**: Skill Submission: autodream v1.0.0

**内容**:
```
Hello SkillHub Team,

I would like to submit a new skill to the registry:

- Name: AutoDream
- Slug: autodream
- Version: 1.0.0
- Description: Automatic memory consolidation sub-agent
- Download URL: [GitHub release URL]
- License: MIT

The skill helps OpenClaw agents automatically organize memory files,
deduplicate entries, and keep MEMORY.md clean.

Please review and add to the index.

Thanks!
```

### 步骤 3：等待审核

通常 1-3 个工作日内会添加到索引。

---

## 方法 3：GitHub 发布（备选）

### 步骤 1：创建 GitHub 仓库

```bash
cd /root/.openclaw/workspace-research/skills/autodream

# 初始化 git
git init
git add .
git commit -m "Initial release: autodream v1.0.0"

# 添加远程仓库（需要创建）
git remote add origin https://github.com/your-username/autodream.git
git push -u origin main
```

### 步骤 2：创建 Release

1. 访问 https://github.com/your-username/autodream/releases/new
2. Tag version: `v1.0.0`
3. 上传 `/tmp/autodream-v1.0.0.zip`
4. 发布

### 步骤 3：更新下载链接

将 GitHub release 链接提交到 skillhub/clawhub 索引。

---

## 发布包内容

```
autodream-v1.0.0.zip (14KB)
├── SKILL.md              # 技能定义（中英文）
├── README.md             # 使用文档
├── RELEASE_v1.0.0.md     # 发布说明
├── PUBLISH_GUIDE.md      # 发布指南
├── LICENSE               # MIT 许可证
├── package.json          # NPM 元数据
├── _meta.json            # 技能元信息
├── config/
│   └── config.json       # 配置文件
└── scripts/
    ├── autodream_cycle.py
    ├── setup_24h.sh
    └── ensure_openclaw_cron.py
```

---

## 验证安装

发布后，验证技能可安装：

```bash
# 从 skillhub 安装
skillhub install autodream

# 从 clawhub 安装
clawhub install autodream

# 验证功能
python3 skills/autodream/scripts/autodream_cycle.py --workspace . --dry-run
```

---

## 联系信息

- SkillHub: skillhub@lightmake.site（示例）
- ClawHub: support@clawhub.ai（示例）
- GitHub: https://github.com/wanng-ide

---

创建时间：2026-04-02
技能版本：1.0.0
