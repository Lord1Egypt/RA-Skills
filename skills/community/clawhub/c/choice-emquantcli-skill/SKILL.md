---
name: emq-cli
description: 使用 emq-cli 命令行进行安装与环境准备、认证登录、行情查询（market）、组合创建与下单（portfolio）、额度查询（quota）、以及 raw 透传命令调用与常见排障。遇到“如何安装 emq”“如何登录”“如何查快照/序列”“如何创建组合/下单”“参数报错如何修复”等场景时使用本技能。
---

# EMQ CLI

## 快速开始

1) 安装并确认命令可用：

```bash
pip install emq-cli
emq --help
```

2) 登录（支持环境变量）：

```bash
export EMQ_USER='your_user'
export EMQ_PASS='your_pass'
emq auth login
```

3) 查看状态：

```bash
emq auth status
```

## 任务流程

1) 先确认认证状态（`auth status`）。
2) 数据查询优先使用 `market snapshot` / `market series`。
3) 组合操作优先使用 `portfolio create` / `portfolio list` / `portfolio qorder`。
4) 额度检查使用 `quota usage`。
5) 需要直接透传 SDK 参数时使用 `raw css/csd/pquery/porder`。

## 常用命令模板

```bash
emq market snapshot 000001.SZ CLOSE --output table
emq market series 000001.SZ CLOSE --start 2025-01-01 --end 2025-01-31 --output csv
emq portfolio create --code DEMO_PF --name "Demo Portfolio" --initial-fund 1000000
emq portfolio list --output table
emq portfolio qorder --code DEMO_PF --stock 300059.SZ --volume 1000 --price 10.5 --date 2025-01-15
emq quota usage --start 2025-01-01 --end 2025-01-31
emq raw css 000001.SZ CLOSE --options "TradeDate=2025-01-15"
```

## 输出与参数规则

1) 默认输出为 `json`；可用 `--output json|table|csv`。
2) 叶子命令末尾的 `--output` 会覆盖全局 `--output`。
3) 日期参数统一使用 `YYYY-MM-DD`。

## 排障约定

1) 参数报错先执行 `emq <domain> <command> --help` 确认 flags。
2) 登录失败先检查 `EMQ_USER` / `EMQ_PASS`，再尝试显式 `auth login --user ... --password ...`。
3) 业务命令失败时先执行 `auth status --check` 验证远端状态。

## 参考

更完整的场景化命令见 [references/command-recipes.md](references/command-recipes.md)。
