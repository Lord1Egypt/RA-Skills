# 中文小说工匠

一个轻量的长篇小说文件工作台：人物、世界观、卷纲、时间线和章节各自落盘，方便你和不同 Agent 接力创作。离线可用，不需要 API Key。

## 能做什么

- 建立人物、世界观、卷纲、时间线和章节目录。
- 检查必需项目文件是否存在、可读且非空；正文连续性由 AI 阅读资料后分析。
- 用可读文件支持多人或多 Agent 接力创作。

## 使用

```bash
python3 scripts/self_test.py init --output ./我的作品 --title "雾中车站"
python3 scripts/self_test.py check --input examples/success-project
```

`check` 只验证目录与必需文件，不分析人物关系、事件顺序或伏笔。进行连续性审读时，AI 需要读取相关设定与正文，并在报告中引用文件和行号/章节锚点；资料不足时应标为待核对，不会静默改写原文。
