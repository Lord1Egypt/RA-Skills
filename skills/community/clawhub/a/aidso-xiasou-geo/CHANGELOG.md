# 更新说明

## v2.1.0

- 将 `prompt_research.py` 的 API Key 读取方式改为统一配置：
  1. 优先读取系统环境变量 `AIDSO_GEO_API_KEY`
  2. 其次读取当前 Skill 根目录 `.env` 中的 `AIDSO_GEO_API_KEY`
- 问题挖掘的 `.state/prompt_research_bindings.json` 仅保留任务状态，不再保存 API Key。
- 删除 `sync_prompt_api_key.py`，因为问题挖掘脚本已直接共用统一 API Key 配置。
- 保留内容生产、品牌知识库、品牌诊断脚本原逻辑不变。
