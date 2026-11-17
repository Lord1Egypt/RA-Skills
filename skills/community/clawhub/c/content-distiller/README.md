# "技能造物主" · WorkBuddy Skill

蒸馏理论框架、五层模型、体系化技能包结构规范（含局限性分析+边界实例）、SKILL.md前置条件规范、质量标准

## 特性

- 请参考 SKILL.md 中的详细说明

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「"技能造物主"」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/content-distiller.git \
  ~/.workbuddy/skills/内容蒸馏器
```

### 环境依赖

请参考 SKILL.md 中的环境要求章节

## 使用

```bash
python3 scripts/pipeline.py <参数>
```

详细参数请参考 SKILL.md

## 输出

请参考 SKILL.md

## 项目结构

```
.gitignore
LICENSE
SKILL.md
references
references/方法论索引.md
references/蒸馏框架.md
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

- [video-skill-router](https://github.com/guipi888/video-skill-router) — 视频创作技能路由器：AI video / animation skill 元技能，判定视频类别（商业宣传/知识科普/其他）→ 自动发现并安装 Manim/Remotion/Lottie 等技能包 → 编排执行输出成片。蒸馏出的技能想用于视频创作？video-skill-router 自动匹配、安装并编排执行出成片

## License

MIT License — 详见 [LICENSE](./LICENSE)
