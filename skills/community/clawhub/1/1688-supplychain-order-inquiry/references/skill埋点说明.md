# Skill 埋点说明

本文描述 **1688-supplychain-order-inquiry** 中 Skill 调用埋点的上报时机、请求内容与失败策略。

## 1. 作用概述

埋点用于在 **Skill 网关**侧统计 Skill 被调用的次数与基础元信息（名称、版本、渠道、场景）。实现集中在 `scripts/_tracker.py` 的 `report_skill_usage()`，由统一 CLI 入口 `cli.py` 在命令生命周期末尾触发。

## 2. 上报时机

| 场景                                                                                                                           | 是否上报 | 说明                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| 已识别子命令（如 `inquiry_send`、`batch_inquiry`），且子命令 `main()` **正常执行完毕**（无未捕获异常、未中途 `sys.exit`）      | **是**   | 无论业务 JSON 中 `success` 为 `true` 或 `false`，均在子命令返回后上报一次。                                               |
| 未传入子命令、子命令名不在注册表、或展示用法后 `sys.exit(1)`                                                                   | **否**   | `cli.py` 在调用子模块前即退出，不会执行埋点逻辑。                                                                         |
| 子命令内 `argparse` 报错并 `sys.exit`（如必填参数缺失）                                                                        | **否**   | 进程在 `module.main()` 内退出，**不会**回到 `cli.py` 的埋点代码。                                                         |
| 子命令 `main()` 抛出**未捕获**异常                                                                                             | **否**   | 异常向上传播，埋点代码未执行。                                                                                            |

## 3. 上报接口与传输

| 项       | 值                                                                                          |
| -------- | ------------------------------------------------------------------------------------------- |
| 方法     | `POST`                                                                                      |
| 路径     | `/api/reportSkillsUsage/1.0.0`                                                              |
| 完整 URL | `https://skills-gateway.1688.com/api/reportSkillsUsage/1.0.0`                           |
| 请求体   | JSON，`Content-Type: application/json`                                                      |
| 鉴权     | 与能力调用一致：通过 `get_auth_headers()` 注入签名；未配置 AK 时静默忽略。                  |

埋点调用使用 `retry=False`（不重试），避免网络异常时阻塞主流程退出。

## 4. 请求体字段

| 字段         | 类型   | 取值说明                                                                         |
| ------------ | ------ | -------------------------------------------------------------------------------- |
| `apiName`    | `null` | 固定为 JSON `null`，占位字段。                                                   |
| `skillsName` | string | Skill 名称，值为 `1688-supplychain-order-inquiry`。                              |
| `version`    | string | Skill 版本，来自 `settings.SKILL_VERSION`，当前为 `0.1.0`。                      |
| `scene`      | string | 固定为 `"CLI"`，表示通过命令行入口触发。                                         |
| `channel`    | string | 发布渠道，来自环境变量 `SKILL_CHANNEL`，缺省为 `clawhub`。                       |

## 5. 失败与日志策略

- `report_skill_usage()` 整体包裹在 `try/except` 中：**任意异常均不向外抛出**，主命令的退出码与输出不受影响。
- 失败时通过 logger `order_inquiry_tracker` 输出 **DEBUG** 级别日志。
- `cli.py` 在调用 `report_skill_usage()` 外层还有一次 `try/except`，避免极端情况影响进程。

## 6. 相关文件索引

| 文件                  | 职责                                         |
| --------------------- | -------------------------------------------- |
| `scripts/_tracker.py` | 读取配置、组装请求体、调用 `api_post` 上报。 |
| `cli.py`              | 命令分发结束后调用 `report_skill_usage()`。  |
| `scripts/_http.py`    | `api_post`：网关地址、签名、重试与错误映射。 |
| `scripts/settings.py` | `SKILL_NAME`、`SKILL_VERSION` 等配置来源。   |
