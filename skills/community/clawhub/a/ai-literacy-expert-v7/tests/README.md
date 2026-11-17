# V7.0 测试套件

本目录随技能包分发，用于验证 V7.0 的 **L4 调度行为**、**产物质量** 与 **技能包自身健康度**。
所有脚本均为**路径自适应**——技能根目录由脚本位置自动推导，不硬编码安装路径，可随包分发到任意机器运行。

## 一、套件总览

| 脚本 | 验证对象 | 项数 | 依赖 | 耗时 |
|------|---------|------|------|------|
| `t1-schedule-contract.py` | L4 调度契约静态校验：6 条注册命令参数 + 6 份自包含 prompt 的 10 段完备性 | 125 | — | <1s |
| `t2-idempotent-sim.py` | L4 运行时仿真：幂等 / 状态机 / 台账 / 失败降级 / 跨会话（复刻执行骨架 ①~⑥） | 79 | — | <1s |
| `t3-scheduler-api.sh` | 真实调度 API：只读调用 + 非法参数拦截（**不执行任何可能落库的写操作**） | 62 | `automation-task-manager` | ~10s |
| `t4-build-ops5-artifacts.py` | 生成 OPS-5 轮转场景产物（3 件正例 + 1 件负例） | — | — | <1s |
| `t4-artifact-regression.sh` | 产物控件实测回归：Playwright harness 真实点击全部控件 | 4（+11 可选） | `node` + `playwright` | ~1min |
| `t5-consistency-coverage.py` | 一致性与全模块覆盖：版本 / 资产 / OPS / 25 单元 / 引用 / 分发包 | 95 | — | <1s |
| `selfcheck.py` | **技能自身自检**：frontmatter / meta / **数字一致性** / 引用 / 卫生 / L4 资产 / 契约 / 测试资产 | 57 | — | <1s |
| `mutation-test.py` | **变异测试**：注入 12 种已知缺陷，验证 `selfcheck.py` 确实能抓出问题 | 12 | — | ~10s |

## 二、快速开始

```bash
# 1. 技能自身自检（最快，改版后必跑）
python3 tests/selfcheck.py

# 2. 验证自检本身有效（防止自检变成橡皮图章）
python3 tests/mutation-test.py

# 3. 契约与一致性（无需任何外部依赖）
python3 tests/t1-schedule-contract.py
python3 tests/t2-idempotent-sim.py
python3 tests/t5-consistency-coverage.py

# 4. 真实调度 API 校验（只读，安全）
bash tests/t3-scheduler-api.sh

# 5. 产物控件实测回归（需 node + playwright）
python3 tests/t4-build-ops5-artifacts.py     # 先生成产物
bash  tests/t4-artifact-regression.sh        # 再跑实测
```

## 三、环境变量

| 变量 | 作用 | 默认 |
|------|------|------|
| `V7_TEST_OUT` | 统一输出目录（各脚本的 JSON 报告、生成的产物） | `<skill>/tests/out` |
| `V6_ARTIFACTS` | **可选**：V6.0 遗留产物目录。设置后 T4 会额外回归 11 件历史产物；未设置则跳过该段 | 未设置 |
| `V7_DIST_ZIP` | **可选**：分发 zip 路径。设置后 T5 校验包内文件；未设置则降级为直接校验技能目录 | 未设置 |

```bash
# 示例：带上历史产物与分发包做完整回归
export V7_TEST_OUT=/tmp/v7-out
export V6_ARTIFACTS=/path/to/v6-test/artifacts
export V7_DIST_ZIP=/workspace/ai-literacy-expert-v7-l4.zip
```

## 四、退出码约定

| 退出码 | 含义 |
|--------|------|
| `0` | 全部通过 |
| `1` | 存在未通过项（可直接接入 CI 做门禁） |

`mutation-test.py` 另有特殊语义：它**期望**每个变异都被 `selfcheck.py` 捕获，
若注入缺陷后自检仍全绿，说明该项检查失效，脚本返回 `1`。

## 五、T4 负例说明

`t4-build-ops5-artifacts.py` 会生成 `neg-broken.html`——一个**故意包含 2 个损坏控件**的产物：
① 回调引用未定义函数（触发后产生 JS 报错）② 点击后移除自身（触发后控件消失）。
期望 harness 判定 `exit=2 且 fail>0`。

负例的作用是验证「强制测试门控」确实会**拦下坏产物**，而不是一律放行——
如果没有这个负例，一个永远返回「全部通过」的坏 harness 也能蒙混过关。

## 六、设计原则

- **路径自适应**：技能根目录由 `__file__` 推导，禁止硬编码 `/root/.codebuddy`、`/workspace` 等绝对前缀。
- **无网络依赖**：除 T3（真实 API 只读调用）外全部离线可跑。
- **写操作零风险**：T3 严格遵守宿主《操作确认协议》，只执行只读或「必然在 HTTP 请求之前失败」的命令。
- **可验证性内建**：`mutation-test.py` 定期证明检查本身有效，避免测试套件退化成形式主义。
