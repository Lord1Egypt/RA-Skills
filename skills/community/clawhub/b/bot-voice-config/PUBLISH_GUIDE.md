# 发布指南

## 发布到 ClawHub

### 方式 1：使用 CLI

```bash
cd /home/chenji/.openclaw/workspace/skills/bot-voice-config-clean

# 发布到 ClawHub
clawhub publish . --slug bot-voice-config --version 1.0.0
```

### 方式 2：通过 ClawHub 网站

1. 访问 https://clawhub.com
2. 登录账号
3. 点击 "Publish Skill"
4. 上传技能文件夹
5. 填写技能信息：
   - Name: `bot-voice-config`
   - Display Name: `机器人音色配置`
   - Version: `1.0.0`
   - Description: `为机器人配置和绑定火山引擎 TTS 音色`
   - Tags: `bot,voice,tts,音色，配置，火山引擎，飞书`

## 发布到 GitHub

### 步骤

1. **创建 GitHub 仓库**
   ```bash
   # 访问 https://github.com/new
   # 仓库名：bot-voice-config
   # 描述：机器人音色配置技能
   # 设为 Public
   ```

2. **推送代码**
   ```bash
   cd /home/chenji/.openclaw/workspace/skills/bot-voice-config-clean
   
   git init
   git add .
   git commit -m "feat: 机器人音色配置技能 v1.0.0"
   git branch -M main
   git remote add origin git@github.com:YOUR_USERNAME/bot-voice-config.git
   git push -u origin main
   ```

3. **替换 README**
   ```bash
   # 使用 GITHUB_README.md 作为 GitHub 的 README
   mv GITHUB_README.md README.md
   ```

### GitHub 仓库信息

- **仓库名**: `bot-voice-config`
- **描述**: 为 OpenClaw 机器人配置和绑定火山引擎 TTS 音色的完整解决方案
- **许可证**: MIT
- **标签**: openclaw, skill, tts, voice, bot, feishu

## 文件清单

发布前确认包含以下文件：

```
bot-voice-config-clean/
├── SKILL.md                          ✅ 必需
├── README.md                         ✅ 必需
├── package.json                      ✅ 必需
├── .gitignore                        ✅ 推荐
├── scripts/
│   └── voice-config.sh               ✅ 必需
└── config/
    └── bot-voice-config.json.template ✅ 必需
```

## 安全检查

发布前运行以下检查：

```bash
# 检查敏感信息
grep -r "API_KEY\|APP_SECRET\|cli_\|ou_" . \
  --exclude="*.template" --exclude=".gitignore" && \
  echo "❌ 发现敏感信息！" || echo "✅ 安全"

# 检查文件完整性
test -f SKILL.md && \
test -f README.md && \
test -f package.json && \
test -f scripts/voice-config.sh && \
echo "✅ 文件完整" || echo "❌ 文件缺失"
```

## 版本更新

### 更新版本号

```bash
# 编辑 package.json
jq '.version = "1.0.1"' package.json > package.json.tmp && \
mv package.json.tmp package.json

# 提交更改
git add package.json
git commit -m "chore: bump version to 1.0.1"
git tag v1.0.1
git push origin main --tags
```

### 发布新版本

```bash
# ClawHub
clawhub publish . --version 1.0.1

# GitHub
git push origin v1.0.1
```

## 常见问题

### Q: ClawHub 发布失败 "SKILL.md required"

A: 确保 SKILL.md 文件在技能目录的根目录下。

### Q: GitHub 推送失败

A: 检查 SSH key 是否配置正确：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# 将公钥添加到 GitHub Settings -> SSH and GPG keys
```

### Q: 配置文件包含敏感信息

A: 使用 `.template` 文件作为模板，实际配置文件添加到 `.gitignore`。

---

*最后更新：2026-03-13*
