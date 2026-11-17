# 同段独立事实与冲突

输入为两份构造的功能测试资料：[manual.txt](input/manual.txt) 同段写“支持 CSV 导入。下载链接保留 7 天。”，[deadlines.txt](input/deadlines.txt) 写“下载链接保留 30 天。”。交付时导入问答可回答，期限问答保留双方证据并标为资料冲突。

可交给 Agent 的任务：

```text
请使用 $aimegeo-knowledge-distill，整理 examples/same-paragraph-conflict/input 中的 CSV 导入与下载期限问答。每项事实只引用足够支持它的原文，期限冲突不要裁决，同段的导入事实独立交付。
```

[成功数据](success.bundle.json)的输出节选：

```text
Q001 是否支持 CSV 导入？
状态：可回答
支持 CSV 导入。
来源：manual.txt · 正文 · L1-L1

Q002 下载链接保留多久？
状态：资料冲突
说明写明下载链接保留 7 天。
期限资料写明下载链接保留 30 天。
待核实：C001，需确认当前适用期限及对应依据。
```

在技能根目录运行，索引文件及结果目录须尚不存在：

```sh
python3 scripts/knowledge.py index --sources examples/same-paragraph-conflict/input --out quote-index.json
python3 scripts/knowledge.py export --sources examples/same-paragraph-conflict/input --index quote-index.json --bundle examples/same-paragraph-conflict/success.bundle.json --out quote-result
```

成功返回：

```json
{"ok": true, "questions": 2, "claims": 3, "missing": 0, "conflicts": 1}
```

资料索引中的 `manual.txt` 段落由 `C001;Q001;Q002` 使用，但只有期限问题 `Q002` 关联 `C001`；`Q001` 不会被共用段落误标为冲突。

[失败数据](failure.bundle.json)把下载期限单方面回答为 7 天且不关联冲突。在技能根目录复用上述索引检查：

```sh
python3 scripts/knowledge.py check --sources examples/same-paragraph-conflict/input --index quote-index.json --bundle examples/same-paragraph-conflict/failure.bundle.json
```

退出码 `2`，stderr：

```json
{"ok": false, "error": "Q002: conflicting evidence must link C001 and use conflict status"}
```

`python3 scripts/self_test.py` 同时检查独立事实成功导出、冲突一方禁止导出、较短/较长/部分重叠引文、同段重复引文和段内自相矛盾的边界。
