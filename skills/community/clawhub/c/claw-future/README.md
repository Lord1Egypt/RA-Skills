# Claw Future · 期货交易助理

**版本**：v1.0.0-beta　｜　**平台**：中国期货市场（CTP 接口）　｜　**免费开源**

---

## 简介

通过聊天对话完成期货交易的全流程操作：实时行情、下单/撤单、条件单、定时委托、收盘日报。底层对接上期技术（CTP）标准接口，支持全国各主要期货公司。

**支持平台**：Windows x64 / macOS / Linux x64

**主要功能**：
- 查资金、查持仓、查委托、查成交（实时向交易所查询，数据直接来自 CTP 回调）
- 限价单 / 市价单，支持开仓 / 平仓 / 平今 / 平昨
- 本地条件单：价格触及阈值自动发单，无需人工盯盘
- 定时委托：指定时间自动下单，支持每日 / 工作日 / 仅一次
- 每日 15:20 自动推送收盘日报（权益、持仓、成交、风控提示）
- 首次运行自动编译接口层、自动引导账户配置，开箱即用

## 写操作幂等性

所有会改变交易、订阅、条件单、定时任务或 daemon 状态的命令默认具备幂等性。`order`、`cancel`、`cancel-all`、`subscribe`、`unsubscribe`、`alert`、`alert-order`、`remove-alert`、`schedule-order`、`schedule-login`、`remove-schedule` 和 `stop` 支持 `--idempotency-key`；省略时系统根据完整请求自动生成稳定键，相同请求重试不会重复执行。

同一个显式幂等键不能用于不同参数的请求。若要有意再次执行完全相同的操作（尤其是再次下单），必须显式换一个新的键。若进程在请求结果返回前异常退出，重试会提示状态未知，请先查询委托/成交后再决定是否使用新键。

条件单和定时任务会保存在项目根目录的 `.clawtrader_runtime.json`，幂等请求日志保存在 `.clawtrader_idempotency.json`；这两个文件包含运行状态，不应提交或分享。`start` 在 daemon 已运行时返回现状而不重复启动，`setup` 在动态库已存在时默认跳过，`config` 在配置内容未变化时不重复写入；明确使用 `setup --force` 才会重新编译。

## 多账户、MCP 与 Web

服务器部署采用“一个账户一个实例”：A、B、C、D、E 分别拥有独立的配置、CTP 流文件、daemon、状态、幂等账本和日志。agent 不由平台替用户决定组合策略，而是通过 MCP 工具显式传入 `account_id` 自己调度；同一台服务器可同时运行多个账户，账户租约会阻止同一真实 CTP 账户被重复启动。

复制 `accounts.example.json` 为 `accounts.json` 后，可用下面的命令查看账户并逐个初始化：

```bash
python3 scripts/clawtrader.py --registry accounts.json accounts
python3 scripts/clawtrader.py --registry accounts.json --account A config
python3 scripts/clawtrader.py --registry accounts.json --account A start
```

MCP 服务提供账户状态、资金、持仓、委托、成交、行情、订阅、准备下单、下单、撤单和全撤工具：

```bash
python3 scripts/mcp_server.py --registry accounts.json --transport streamable-http --port 17880
```

Web 界面提供账户切换、行情、下单、二次确认、撤单、全撤、持仓/委托/成交查询和实时事件推送。开发或单机使用：

```bash
python3 scripts/web_server.py --registry accounts.json --host 127.0.0.1 --port 17890
```

打开 `http://127.0.0.1:17890/`。非本机监听必须设置 `CLAW_WEB_TOKEN`；完整的 systemd 部署示例见 [`deploy/README.md`](deploy/README.md)。

---

## 安装

1. 解压 `claw-future.zip`
2. 进入 `claw-future/` 目录，执行一条命令：
   ```
   python scripts/clawtrader.py start
   ```
   自动完成编译 → 账户配置 → 启动，无需其他手动步骤。

**环境要求**：
- Python 3.9+
- 编译工具：Windows → Visual Studio 2019+；macOS → Xcode Command Line Tools；Linux → `sudo apt install build-essential`
- 期货公司 CTP 账户（可先用 SimNow 仿真账户测试）

---

## ⚠️ 免责声明

**请在使用前仔细阅读以下内容：**

1. **纯技术分享，免费使用。** 本项目为个人技术作品，以学习和交流为目的，不收取任何费用，不提供任何形式的商业服务。

2. **仅经过 SimNow 仿真测试。** 当前版本仅在上期技术 SimNow 仿真环境中进行过功能验证，**尚未经过充分的实盘验证**。

3. **实盘使用风险自负。** 期货交易本身具有高风险性。若您计划将本项目接入实盘账户，请务必：
   - 在仿真环境中充分测试，确认所有功能符合预期
   - 小资金试运行，逐步验证下单、撤单、条件单等核心流程
   - 自行评估网络稳定性、系统故障等异常场景下的风险

4. **概不负责。** 因使用本项目导致的任何直接或间接损失（包括但不限于交易亏损、错单、漏单、系统异常），作者及贡献者**不承担任何法律责任**。

5. **不构成投资建议。** 本项目仅提供交易执行工具，不提供任何交易策略或投资建议。所有交易决策由用户自行做出。

> **使用即视为您已阅读并同意以上免责条款。**

---

*issues / PR 欢迎提交至项目主页*
