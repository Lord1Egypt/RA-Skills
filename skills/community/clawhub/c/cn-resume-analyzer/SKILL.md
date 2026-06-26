---
slug: cn-resume-analyzer
name: cn-resume-analyzer
version: "1.0.0"
description: |
  Resume Analyzer skill.
  自动生成，无人工审查。
metadata: {"openclaw": {"emoji": "🔧"}}
---

# ---

name: cn-resume-analyzer
description: "AI简历分析优化工具。解析简历内容，提供结构化评分、关键词匹配、格式建议和改进方案，帮助求职者提升简历竞争力。"
scope: "resume analysis, CV review, job application optimization"
install: |
  无额外依赖，使用Python标准库。
  pip install requests（仅用于下载网络简历时可选）
env: ""
entry:
  type: prompt
  prompt: |
    当用户需要分析简历、优化简历、检查简历格式时，使用此skill。
    识别意图：
    - "帮我看看这份简历"
    - "简历评分"
    - "简历优化建议"
    - "简历关键词匹配"
    执行流程：
    1. 获取简历内容（文本/文件路径/URL）
    2. 调用 scripts/resume_analyzer.py 分析
    3. 返回评分和改进建议
handler: |
  调用 scripts/resume_analyzer.py 处理简历分析
---


---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
