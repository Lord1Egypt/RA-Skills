# 成功与失败样例

这些文件都是合成回归资料，未查询任何 AI 平台，不是真实用户案例。青禾工具、速记表和 demo-platform 仅用于演示；example.com 为示例域名。输入均标为 `simulated`，不会混入真实提及率或引用率。

## 成功交付：六题、前后两批

[six-questions.json](success/six-questions.json) 包含同一组6个问题、一个演示平台、before／after 两批共12条记录，涵盖品牌、品类、比较、场景、价格与限制。数据同时包含模拟提及、官网／子域引用、相似域名、URL 查询参数及未知引用列表。

从技能根目录运行（使用新的输出目录）：

```bash
python3 scripts/citation_monitor.py --input examples/success/six-questions.json --before before --after after --output citation-demo
```

已生成的实际交付为 [对照报告](success/output/前后对照报告.md)、[逐项 JSON](success/output/逐平台问题结果.json)、[未成功采集清单](success/output/未成功采集清单.md)。分析成功，计划12条、模拟12条、真实有效0条，提及／引用率和同题变化均 N/A。模拟原生引用在 JSON 的预览中保留，不能声称为平台已引用。

## 业务失败：错误、超时、未运行

[all-failed.json](failure/all-failed.json) 计划6条，仅给出一条受控错误和一条受控超时，其余4条自动记为 `not_run`。

```bash
python3 scripts/citation_monitor.py --input examples/failure/all-failed.json --output citation-failure-demo
```

退出码为0，代表成功交付失败分析；不是采集成功。实际 [失败报告](failure/output/前后对照报告.md)、[逐项 JSON](failure/output/逐平台问题结果.json)、[未成功清单](failure/output/未成功采集清单.md) 保留计划6、有效0、error=1、timeout=1、not_run=4；计数和比率为 `null`／N/A，没有 0% 伪结论。

## 输入无效：缺原生引用字段

[missing-citations.json](failure/missing-citations.json) 故意删除成功／模拟记录的 `citations` 键。

```bash
python3 scripts/citation_monitor.py --input examples/failure/missing-citations.json --output citation-invalid-demo
```

实际预期行为是退出2，不写结果目录；标准错误为：

```text
Input/output error: citations required: null means not captured, [] means empty
```

应根据原始材料补 `null`（未采集）或真实列表；不能为了通过校验填空列表。该失败行为由自测实际执行并验证。

## 真实统计分支的验证

`python3 scripts/self_test.py` 在临时目录／内存中使用受控合成记录检验真实统计分支，不产生线上结果。当前测试中6个可比较提及对为3/6→5/6，新增3、失去1；原生引用因一条引用未知仅有5个有效配对，为1/5→2/5。这些数值只验证计算逻辑，不是品牌表现。自测还检查全部失败、未知引用、域名边界、变题／条件变化、证据保留和独立目录运行，且不依赖图标或根目录许可文件。
