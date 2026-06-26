# 标书魔方 - AI 标书制作及检查工具（Skill）

本项目提供“招标文件解析专家”Skill：从招标文件读取（支持doc/docx/pdf格式）、行业识别、模板加载、要求抽取，到完整性/符合性检查与自动补抽，最终仅输出一份可直接在线预览的pdf结果页，助力高效、专业地生成投标材料要点清单。

## 功能亮点
- 行业自动识别：从招标文件判断“一级/二级行业”。
- 行业模板驱动：按行业要点组织抽取结构，支持通用与细分行业模板。
- 招标要求抽取：调用大模型按模板结构抽取关键信息，统一结构化。 
- 智能校核：完整性检查与符合性检查，自动补抽/重抽


## 环境要求
- Python 3.10+（建议 3.10 或 3.11）
- 可访问的 LLM 服务（OpenAI SDK 兼容接口）

## 安装skill
1) npx install

2）配置模型
在scripts文件夹下的 `env_config.md`中填入你的大模型接口配置，需支持文件url解析与内容提取。
```ini
# env_config.md
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://your-openai-compatible-endpoint
LLM_MODEL=qwen # 或你的可用模型名称
```

## 常见问题（FAQ）
- 支持哪些行业？  
  详见 `SKILL.md` 的“行业分类体系”。若找不到精确模板，将回退到通用模板，模板可配置。


## 许可证
本项目解释权为标书魔方所有，若需外部发布或商用，请联系标书魔方团队（https://biaoshu.supcon.com/）确认授权范围。

