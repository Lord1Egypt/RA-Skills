# 失败与未知边界示例

这些文件都是构造的校验场景，不是线上故障记录。

`mixed-status.json` 是可成功处理的部分数据场景：query_failed、missing、not_run、simulated 各一条，observed 为 0。命令与实际输出见[expected.json](expected.json)：

```sh
python3 scripts/analyze.py examples/failure/mixed-status.json
```

程序退出 0，因为状态记录合法；它不代表检测成功。实测有效回答 0，各项实测分子与百分比 null，分母 0。没有问题可判为“在所有有效回答中缺席”；失败或未执行不能变成品牌未被提到。

`invalid-quote.json` 演示伪造证据摘录：原文没有“强烈推荐青禾工具”，应被拒绝。

```sh
python3 scripts/analyze.py examples/failure/invalid-quote.json
```

实际退出 2，stdout 为空；stderr 为[expected-error.json](expected-error.json)：

```json
{"status":"error","error":"records[0].review.recommendation.quote: quote is not an exact substring of answer"}
```

修复方式是重新审核原文：该回答只是功能介绍，推荐应为 false；不能把缺失摘录改写成原文。自测还覆盖重复运行、没有链接、普通正文链接、原生来源未采全、未审核来源关联、缺事实来源、坏时间、非法 JSON 和输出覆盖保护。
