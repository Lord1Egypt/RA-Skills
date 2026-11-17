# "电子书拆解成技能包" · WorkBuddy Skill

"This skill should be used when the user provides an electronic book (PDF, EPUB, TXT, MD) and wants to automatically extract knowledge, analyze structure, and generate multiple WorkBuddy skills. Trigger phrases: 拆解这本书, 从这本书提取技能, 把这本书变成技能, 生成技能包, book to skills. Supports three modes: Knowledge Base, Action Guide, Hybrid."

## 特性

- 请参考 SKILL.md 中的详细说明

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「"电子书拆解成技能包"」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/workbuddy-book-to-skills.git \
  ~/.workbuddy/skills/book-to-skills
```

### 环境依赖

请参考 SKILL.md 中的环境要求章节

## 使用

```bash
python3 path/to/skill-creator/scripts/package_skill.py \
  ~/.workbuddy/skills/{skill-name} \
  ~/workbuddy-output/{YYYY-MM-DD}-book-to-skills/{book-slug}/
```

## 输出

请参考 SKILL.md

## 项目结构

```
.gitignore
LICENSE
SKILL.md
references
scripts
scripts/extract_epub.py
scripts/extract_pdf.py
```

## 关于作者

**桂皮 Guipi** — AI Agent 开发者 · 超级个体践行者
专注 AI 效率工具与一人公司方法论，帮普通人用 AI 成为超级个体

| 平台 | 账号 |
|------|------|
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |
| 🎬 抖音 | [桂皮AI实战](https://v.douyin.com/QJRjHGAtrvA/) |
| 📺 视频号 | 微信内搜「桂皮AI实战」|
| 💬 公众号 | 微信搜「桂皮AI实战」|
| 🌟 知识星球 | [AI超级个体](https://t.zsxq.com/guSUk) — AI工具 · 创作 · 产品 · 流量 · 变现 |
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 💬 微信 | guipi996（注明来意）|

## 相关项目

- [video-skill-router](https://github.com/guipi888/video-skill-router) — 视频创作技能路由器：AI video / animation skill 元技能，判定视频类别（商业宣传/知识科普/其他）→ 自动发现并安装 Manim/Remotion/Lottie 等技能包 → 编排执行输出成片。电子书拆解出的技能想变成视频？video-skill-router 一条龙完成找技能→装技能→出片

## License

MIT License — 详见 [LICENSE](./LICENSE)
