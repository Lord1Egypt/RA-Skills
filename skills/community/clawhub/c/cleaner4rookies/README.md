# openclaw-cleaner

> OpenClaw 临时文件自动清理工具 🧹

**状态**：v1.0.0 · 面向 ClawHub 小白用户 · 默认安全

---

## 核心理念

OpenClaw 运行过程中会产生大量临时文件（测试音频、DOCX 下载、图片草稿等），
长期不清理会导致工作区膨胀。

本工具提供**安全、可配置**的清理机制：
- 默认不删除，只归档
- 默认先 dry-run 预览
- 白名单保护重要文件

## 文件结构

```
openclaw-cleaner/
├── SKILL.md              ← ClawHub 展示 + 用户文档
├── README.md             ← 本文件
├── config.yaml           ← 内置默认规则
└── scripts/
    └── cleaner.sh        ← 核心清理脚本
```

## 快速验证

```bash
# 预览当前会清理什么
bash ~/.openclaw/workspace/skills/openclaw-cleaner/scripts/cleaner.sh

# 正式执行
bash ~/.openclaw/workspace/skills/openclaw-cleaner/scripts/cleaner.sh --force
```

## 开发备注

- 脚本完全零依赖（纯 bash + find + stat）
- macOS（stat -f）和 Linux（stat -c）均兼容
- 配置文件采用 YAML 简化解析（不用 Python/yq）
- 白名单路径支持 `~` 展开

## 发布 ClawHub checklist

- [x] SKILL.md 完整（安装/配置/安全/卸载）
- [x] config.yaml 默认规则合理
- [ ] 封面图（一张图说明功能）
- [ ] dry-run 截图示例
- [ ] 版本号更新 changelog
