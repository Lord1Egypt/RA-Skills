"""doc-holmes —— 保持原文排版的外文 PDF 精准翻译。

三级管线：triage 质量分级（A/B/C）→ 跳翻规则 / 降噪 → BabelDOC(pdf2zh-next)
子进程翻译。自有代码 MIT；AGPL 引擎只以子进程调用，零 vendor、零改源。
"""

__version__ = "3.0.0"
