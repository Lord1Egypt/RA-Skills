# V2EX 推广文案 — 一稿多发助手
# 发布节点：分享创造

---

**做了个多平台内容适配的 OpenClaw Skill，自动生成 7 个平台原生版本**

痛点：运营多个平台时，同一主题需要针对每个平台重新调整格式、语调、字数。

Skill 实现：输入原始内容（或主题），一次输出微信公众号、知乎、小红书、抖音口播脚本、头条号、Twitter Thread、LinkedIn 7 个版本。

每个版本不是简单的裁剪，而是按平台原生调性重写——知乎是问答+数据驱动格式，抖音是三段式口播脚本含镜头提示，Twitter 是英文 thread 每条 280 字以内可独立阅读。

中文内容自动翻译适配英文平台（Twitter/LinkedIn），反之亦然。用户可以指定只生成某几个平台的版本。

```
openclaw skills install content-repurposer-cn
```
clawhub.ai/skills/content-repurposer-cn

Prompt 工程部分花了不少时间调各平台的格式规则，有做内容工具的可以聊聊。
