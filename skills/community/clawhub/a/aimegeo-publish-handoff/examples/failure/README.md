# 结果未知时阻止重投

这是合成失败样例，不连接平台。输入模拟“用户已点击但连接中断，尚未确认是否受理”；业务期望是保存未知状态并阻止新的提交意图。即使提供新的提交授权，也必须先回读。

在技能目录运行以下命令，使用单独输出目录以保留成功样例：

```sh
python3 scripts/handoff.py prepare --input examples/input/plan.json --out failure-demo
python3 scripts/handoff.py record --pack failure-demo --receipt examples/failure/unknown-receipt.json
python3 scripts/handoff.py intent --pack failure-demo --target 3034745896c95dde6d83
```

前两条退出 `0`；第三条退出 `2`，返回 `READBACK_REQUIRED`，台账仍是 `unknown`，没有新提交意图。这是预期的业务阻断，不是实际投稿失败或平台查询结果。

输入见 [unknown-receipt.json](unknown-receipt.json)，实际本地命令输出见 [expected.json](expected.json)。`python3 scripts/self_test.py` 会在临时目录重放此场景，并另外验证审核中不重投、授权不匹配、正文被改、缺素材以及并发意图等边界。
