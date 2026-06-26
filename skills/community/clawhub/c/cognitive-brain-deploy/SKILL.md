---
name: cognitive-brain-deploy
description: Cognitive Brain 语义记忆系统一键部署工具。当用户需要部署 OpenClaw 认知脑、部署 PostgreSQL+pgvector 向量数据库、安装 Cognitive Brain Skill、配置定时任务和 Hook 时使用。
---

# Cognitive Brain Deploy

OpenClaw 语义记忆系统的自动化部署 Skill。

## 快速部署

执行一键部署脚本：

```bash
bash ~/.openclaw/workspace/skills/cognitive-brain-deploy/scripts/deploy.sh
```

或手动分步部署，详见 [references/deploy-guide.md](references/deploy-guide.md)。

## 部署检查清单

- [ ] PostgreSQL 14+ with pgvector 安装完成
- [ ] Redis 6+ 安装完成
- [ ] `cognitive_brain` 数据库创建完成
- [ ] 表结构初始化完成（memories + associations 表）
- [ ] Cognitive Brain Skill 下载到 `~/.openclaw/workspace/skills/cognitive-brain`
- [ ] `config.json` 数据库密码配置正确
- [ ] Cron 定时任务添加完成
- [ ] Hook 启用完成

## 验证命令

部署完成后，执行以下命令验证：

```bash
# 健康检查
cd ~/.openclaw/workspace/skills/cognitive-brain && node scripts/recall.cjs health_check

# 测试写入
node scripts/encode.cjs --content "测试记忆" --metadata '{"type":"fact","importance":0.8}'

# 测试搜索
node scripts/recall.cjs --query "测试"
```

## 参考文档

- [部署详细步骤](references/deploy-guide.md) — 从零开始的完整部署流程
- [常见问题排查](references/troubleshooting.md) — 9 个高频问题和解决方案
