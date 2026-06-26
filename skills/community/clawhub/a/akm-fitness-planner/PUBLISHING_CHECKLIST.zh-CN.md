<!--
文件：PUBLISHING_CHECKLIST.zh-CN.md
核心功能：作为 Fitness 分支公开发布前的中文检查清单，避免私有数据泄露、口径错位和结构缺失。
输入：Fitness 分支当前 skill 包、论文稿与发布页文案。
输出：供发布前逐项核对的中文检查清单。
-->

# Fitness Publishing Checklist

## 口径

- [ ] 标题明确写成 AKM 的 Fitness 分支，而非独立母概念
- [ ] 不漂移成医疗系统、康复系统或广义疗效验证语言
- [ ] 论文口径与“真实约束下的方法论文”保持一致

## 隐私

- [ ] 不直接公开完整训练日志
- [ ] 不直接公开完整私人身体历史记录
- [ ] 仅对邵先生成立的身份细节已脱敏或泛化
- [ ] 身体限制被改写为可复用输入字段，而不是实名自述

## 结构

- [ ] `ELICITATION_PROMPT.md` 可独立阅读
- [ ] `RECORD_TEMPLATE.md` 可独立复用
- [ ] `EXECUTION_PROMPT.md` 与前两者无冲突
- [ ] `SKILL.md` 已明确方法不是单 Prompt
- [ ] 商店文案与 skill 文案使用同一口径
