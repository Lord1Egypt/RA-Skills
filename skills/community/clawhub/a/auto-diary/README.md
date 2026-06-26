# 日记（Diary）

一个用于 OpenClaw 的日记自动化 skill：在任务触发时自动完成“写作 + 出图”。

An OpenClaw skill that automates daily journaling and exports a shareable image.

## 功能 / Features

- 自动初始化配置（首次运行）
- 读取 SOUL / MEMORY / 每日记忆素材
- 生成指定日期日记文本
- 导出 1080px 宽图片（高度自适应）
- 可用于归档、分享、回顾

## 典型场景 / Use Cases

- “帮我写昨天日记”
- “把日记生成一张图”
- “补一篇前天的日记”
- “按既有风格继续写”

## 目录结构 / Structure

```text
.
├── SKILL.md
├── INIT.md
├── config.template.yaml
├── diary-template.html
└── .gitignore
```

## 隐私 / Privacy

- 个人配置写在 `config.yaml`（本仓库不应提交该文件）
- 公开仓库仅保留模板和通用逻辑

## License

MIT
