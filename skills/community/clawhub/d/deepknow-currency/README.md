# deepknow-currency

`deepknow-currency` 是北京宽客进化科技有限公司旗下“知汇 InkRate”的验证版 / 内测版汇率 Skill。

它默认连接 `https://rate.feedai.cn` 这个官方公共入口；收费场景下连接到京东的 `clawtip` A2A 支付服务。

## Services

- 查询汇率（免费）
- 计算兑换金额（免费）
- 汇率提醒服务（收费）
- 汇率涨跌概率查询（收费）

前两项免费服务直接访问公开 API；后两项收费服务通过 `clawtip` 收款，并将支付后的履约请求转发给 InkRate 服务端。

当前支持币种：`USD / EUR / JPY / GBP`

## Files

- `SKILL.md`: ClawHub / OpenClaw 使用说明
- `manifest.yaml`: 发布元数据
- `config.example.yaml`: 本地或远程部署时的示例配置
- `scripts/quote.py`: 免费查询最新汇率
- `scripts/convert.py`: 免费计算兑换金额
- `scripts/create_order.py`: Phase 1，创建订单并写入本地订单文件
- `scripts/service.py`: Phase 3，读取支付凭证并调用履约接口
- `scripts/clean_release.py`: 发布前清理 Python 缓存文件

## Runtime Configuration

优先级从高到低：

1. 环境变量 `INKRATE_SKILL_BASE_URL`
2. Skill 根目录 `config.yaml` 中的 `base_url`
3. 默认值 `https://rate.feedai.cn`

示例：

```yaml
base_url: "https://rate.feedai.cn"
```

## Important Notes

- 这是验证版 / 内测版，不是最终正式版。
- 服务主体：北京宽客进化科技有限公司
- 产品名称：知汇 InkRate
- 官方公共入口：`https://rate.feedai.cn`
- 收费链路会走真实 JD `clawtip` A2A，请按真实扣费预期使用。
- 支付过程中，用户可能需要在手机端完成京东登录、支付密码、银行卡验证或风控确认。

## Local Checks

```bash
python3 scripts/clean_release.py
python3 scripts/clean_release.py --check
```

如果你刚执行过测试、`compileall` 或其它会生成 Python 缓存的命令，先执行一次清理，再做 `--check`。

可选在线检查：

```bash
python3 scripts/quote.py USD
python3 scripts/convert.py CNY USD 100
```

如需额外做语法编译检查，可执行：

```bash
python3 -m compileall scripts
python3 scripts/clean_release.py
python3 scripts/clean_release.py --check
```

## Publish

在 Skill 根目录执行：

```bash
python3 scripts/clean_release.py
python3 scripts/clean_release.py --check
clawhub login
clawhub publish .
```

如果你不想在当前机器安装 `clawhub`，可以把整个 `openclaw/deepknow-currency/` 目录同步到另一台已安装 `clawhub` CLI 的机器上再发布。
