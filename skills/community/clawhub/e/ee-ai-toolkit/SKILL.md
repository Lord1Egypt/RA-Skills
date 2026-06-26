---
name: ee-ai-toolkit
description: 电气工程师 AI 工具包。用于 AI in Electrical Engineering、电气工程 AI、prompt engineering、power systems、smart grids、electrical calculations、design automation、data visualization、optimization、career toolkit、以及 100 个电气工程 Python 示例脚本相关问题。
compatibility: 需要 python3；可选使用 numpy、pandas、matplotlib、scikit-learn 运行部分附录示例。
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# EE AI Toolkit

这个技能由本目录的 HTML 课程资料压缩生成，主题是电气工程师如何用 AI、Python 和提示工程处理计算、设计、分析、自动化、优化和职业发展任务。

激活此技能时，优先按问题类型读取最小必要资料：

- 课程结构、资料来源、主题路由：读取 `references/course-index.md`。
- 快速回答或复习：读取 `references/condensed-lessons.md`。
- 需要接近原文、练习、示例流程或完整上下文：读取 `references/source-digest.md`。
- 提示词、提示词改写、提示词模板：读取 `references/prompt-library.md`。
- Python 示例脚本、脚本编号、脚本用途：读取 `references/python-script-catalog.md`，再使用 `assets/python-scripts/` 中的对应脚本。
- 需要核对原始 HTML：使用 `assets/source-html/`，或解压 `assets/source-html.tar.gz`。

资料较大时，先用检索脚本定位，再读取相关引用文件：

```bash
python3 {baseDir}/scripts/search_ee_ai.py --query "load forecasting"
```

生成或修改工程答案时，保持以下约束：

- 明确单位、输入假设、公式、计算步骤和验证方法。
- AI 生成的设计、保护、配电、并网、优化和故障分析结果只能作为工程草案或教学示例。
- 对安全关键或合规相关电气工程问题，要求用户用适用标准、仿真工具、现场数据和有资质工程审查进行验证。
- 需要代码时，优先复用或改造 `assets/python-scripts/` 中最接近的脚本，而不是从零编造。
- 回答可以中英文混合，但用户用中文提问时默认用中文回答。
