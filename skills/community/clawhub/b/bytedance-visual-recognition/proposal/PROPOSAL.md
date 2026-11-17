# 3.1.1 更新提案

## 目标
精简发布，修复安全审查问题，仅上传核心文件。

## 变更
- 收紧触发词列表，移除过于宽泛的 pattern
- 批量处理改为仅复制媒体文件（不再复制整个目录树）
- 剔除非核心文件（.env, Temp, .bak, .json 等）
- 仅上传核心文件：doubao_vision_recognize.py, SKILL.md, skill-card.md
