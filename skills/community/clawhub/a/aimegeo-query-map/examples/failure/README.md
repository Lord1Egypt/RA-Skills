# 失败样例

[cross-audience.json](cross-audience.json) 把小型内容团队的试用限制与大型代理公司的客户管理问题写成同一个 `merge_key`。受众和答案范围不能共用；脚本应拒绝合并，不生成误导性地图。

从技能目录运行：

```bash
python3 scripts/map_queries.py examples/failure/cross-audience.json --output-dir failure-result
```

预期退出码2，标准错误见实际保存的 [error.json](error.json)：

```json
{"ok": false, "code": "MERGE_CONFLICT", "error": "同一组的受众、实体、意图、范围与主题须一致"}
```

校验失败时不会创建 `failure-result`。修复方法是分别判断两类受众需要的答案，为不同范围使用不同归并键，不为通过校验把真实受众改成同一个。

其他边界由业务自测实际构造并检查：仅有标题却声称覆盖、正文引文不存在、事实状态冲突、字面重复拆组、未运行/失败却填空引用数组、回答时间缺失、试图覆盖已有结果。运行 `python3 scripts/self_test.py` 可复现；不需要网络、账号或父目录资料。
