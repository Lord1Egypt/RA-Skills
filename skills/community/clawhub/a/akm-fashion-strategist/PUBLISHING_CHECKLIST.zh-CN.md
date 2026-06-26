<!--
文件：PUBLISHING_CHECKLIST.zh-CN.md
核心功能：作为 Fashion 分支公开发布前的中文检查清单，避免私有资产泄露、口径错位和结构缺失。
输入：Fashion 分支当前 skill 包、论文稿与发布页文案。
输出：供发布前逐项核对的中文检查清单。
-->

# Fashion Publishing Checklist

## 口径

- [ ] 标题明确写成 AKM 的 Fashion 分支，而非独立母概念
- [ ] 不漂移成图像识别、虚拟试衣或广义 benchmark 语言
- [ ] 论文口径与“场景和资产约束下的方法论文”保持一致

## 隐私

- [ ] 不直接公开完整私有衣橱明细
- [ ] 不直接公开仅对邵先生成立的身份与体态细节
- [ ] 风格偏好已改写为可复用输入字段，而不是实名自述

## 结构

- [ ] `ELICITATION_PROMPT.md` 可独立阅读
- [ ] `RECORD_TEMPLATE.md` 可独立复用
- [ ] `EXECUTION_PROMPT.md` 与前两者无冲突
- [ ] `SKILL.md` 已明确方法不是单 Prompt
- [ ] 商店文案与 skill 文案使用同一口径
