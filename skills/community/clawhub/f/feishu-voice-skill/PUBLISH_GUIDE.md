# 📤 发布指南

## 方式一：ClawHub 网页发布（推荐）

1. 访问 https://clawhub.com
2. 登录账号
3. 点击 "Publish Skill" 或 "发布技能"
4. 上传以下文件：
   - SKILL.md
   - README.md
   - reference.md
   - clawhub.yaml
   - package.json
   - scripts/send_voice.sh
   - examples/morning.sh
   - examples/night.sh

5. 填写信息：
   - **名称**: Feishu Voice Skill - 飞书语音条
   - **版本**: 1.0.0
   - **标签**: feishu, voice, audio, tts, noizai, chinese
   - **描述**: 让 AI 助手能够给飞书用户发送真正的语音条
   - **价格**: 9.9 CNY（或免费）

6. 点击发布！

## 方式二：ClawHub CLI 发布

```bash
# 1. 登录
clawhub login

# 2. 发布
cd /root/.openclaw/workspace/skills/feishu-voice-skill
clawhub publish . --slug "feishu-voice-skill" --version "1.0.0"
```

## 方式三：GitHub 发布

```bash
# 1. 创建仓库
# 访问 https://github.com/new
# 仓库名：feishu-voice-skill

# 2. 推送代码
cd /root/.openclaw/workspace/skills/feishu-voice-skill
git init
git add .
git commit -m "Initial release: Feishu Voice Skill"
git branch -M main
git remote add origin https://github.com/openclaw/feishu-voice-skill.git
git push -u origin main
```

## 定价建议

- **免费版**: 基础功能（GitHub）
- **付费版**: 9.9 CNY（ClawHub，含技术支持）
- **企业版**: 99 CNY（定制服务）

## 推广渠道

1. ClawHub 技能市场
2. GitHub Trending
3. 飞书开放平台社区
4. AI 助手社群
5. Discord/Telegram 群组

---

**祝发布成功！💰**
