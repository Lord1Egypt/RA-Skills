# 失败样例：没有引文的肯定答案

输入 [无引文答案.json](无引文答案.json) 声称所有客户都享有无限存储，但四份资料没有这项事实，且陈述的 `refs` 为空。它不是可用问答，不能转换成成功交付。

在技能根目录复现：

```sh
python3 scripts/knowledge.py check --sources examples/input --index examples/source-index.json --bundle examples/failure/无引文答案.json
```

退出码 `2`，stderr：

```json
{"ok": false, "error": "Q001: each claim requires evidence"}
```

正确处理方式是把存储空间限制列为待补，或取得当前版本的说明后重新编写有证据的答案；不要补一个看似相关但不能支持结论的引文。`self_test.py` 也验证失败的 `export` 不创建结果目录。
