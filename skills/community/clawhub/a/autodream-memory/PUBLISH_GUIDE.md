# AutoDream 发布指南

## 当前状态

✅ 技能已创建：`/root/.openclaw/workspace-research/skills/autodream/`
✅ 所有 AGENT 已可用（技能全局共享）
⏳ 待发布到 clawhub
⏳ 待发布到 skillhub

## 发布到 ClawHub

### 方法 1：使用 CLI（需要登录）

```bash
# 登录（需要浏览器或 token）
clawhub login

# 或者使用 token 登录
clawhub login --token <YOUR_TOKEN> --label "research-agent"

# 发布技能
clawhub publish /root/.openclaw/workspace-research/skills/autodream
```

### 方法 2：通过 Web 界面

1. 访问 https://clawhub.com
2. 登录后进入 "Publish Skill"
3. 上传技能文件夹或填写元数据

### 发布前检查清单

- [ ] SKILL.md 包含英文描述（clawhub 要求）
- [ ] package.json 包含 version、name、description
- [ ] README.md 有使用文档
- [ ] 无敏感信息（API 密钥、密码等）
- [ ] 测试过安装流程

## 发布到 SkillHub

SkillHub 是轻量级技能存储，发布方式：

### 方法 1：提交到索引

编辑 SkillHub 索引文件，添加技能元数据：

```json
{
  "slug": "autodream",
  "name": "AutoDream",
  "description": "自动记忆整理子代理",
  "version": "1.0.0",
  "downloadUrl": "https://github.com/your-repo/autodream/archive/main.zip"
}
```

### 方法 2：GitHub 发布

1. 创建 GitHub 仓库
2. 推送技能代码
3. 提交到 SkillHub 索引

## 技能元数据

```json
{
  "name": "autodream",
  "version": "1.0.0",
  "description": "AutoDream - Automatic memory consolidation for OpenClaw",
  "author": "research AGENT",
  "license": "MIT",
  "keywords": ["memory", "consolidation", "autodream", "organization"],
  "repository": "https://github.com/your-repo/autodream"
}
```

## 发布后验证

```bash
# 测试安装
skillhub install autodream
clawhub install autodream

# 验证功能
python3 skills/autodream/scripts/autodream_cycle.py --workspace . --dry-run
```

## 当前技能文件列表

```
skills/autodream/
├── SKILL.md              # 技能定义（中英文）
├── README.md             # 使用文档
├── RELEASE_NOTES.md      # 发布说明
├── package.json          # NPM 元数据
├── _meta.json            # 技能元信息
├── config/
│   └── config.json       # 配置文件
└── scripts/
    ├── autodream_cycle.py       # 主循环
    ├── setup_24h.sh             # 定时设置
    └── ensure_openclaw_cron.py  # Cron 配置
```

## 注意事项

1. **ClawHub 要求英文描述**：SKILL.md 需要有完整的英文描述
2. **版本号管理**：每次更新需要递增 version
3. **依赖声明**：如有外部依赖需在 package.json 中声明
4. **安全审查**：发布前运行 skill-vetter 检查

## 手动发布步骤（如需）

1. 打包技能：
```bash
cd /root/.openclaw/workspace-research
tar -czf autodream-v1.0.0.tar.gz skills/autodream/
```

2. 上传到托管平台（GitHub Releases、网盘等）

3. 提交到技能索引

---

创建时间：2026-04-02
最后更新：2026-04-02
