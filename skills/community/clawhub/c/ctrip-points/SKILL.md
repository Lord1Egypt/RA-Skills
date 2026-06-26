# 携程积分助手 (Ctrip Points)

一个帮你管理携程积分的 OpenClaw skill。

## 功能

1. **查询积分余额** - 获取当前账户积分总数和估值
2. **查看可兑换商品** - 浏览积分商城可兑换的商品
3. **推荐商品** - 根据积分余额推荐最值得兑换的商品
4. **自动监控新品** - 每天自动检查积分商城新上架的商品（通过 cron）
5. **推送通知** - 发现超值商品或新品时主动推送给你

## 使用方法

### 在 OpenClaw 中直接使用

直接对我说：
- "查询我的携程积分"
- "查看积分商城商品"
- "我有什么可兑换的"
- "推荐一些商品"
- "检查携程积分商城新品"

### 命令行使用

```bash
# 进入脚本目录
cd ~/.openclaw/skills/ctrip-points/scripts

# 查询积分
python3 ctrip.py points

# 查看商品列表
python3 ctrip.py products

# 查看可兑换商品（买得起的）
python3 ctrip.py affordable

# 推荐商品
python3 ctrip.py recommend

# 设置积分（手动更新）
python3 ctrip.py set-points <数量>

# 添加商品到列表
python3 ctrip.py add-product "<商品名称>" <积分>

# 检查新品
python3 ctrip.py check-new

# 更新全部数据（需要Cookie）
python3 ctrip.py update
```

## 数据存储

- Cookie: `~/.openclaw/data/ctrip-cookie.txt`
- 商品列表: `~/.openclaw/data/ctrip-products.json`
- 积分余额: `~/.openclaw/data/ctrip-points.json`

## 自动任务

已设置 cron 任务，每天早上 9:00 自动检查积分商城新品，发现新商品会通过飞书推送。

查看 cron 任务：
```bash
openclaw cron list
```

## 依赖

- Python 3
- 无需额外依赖（使用内置模块）

## 注意事项

1. 积分数据可能有延迟，以携程官方为准
2. 手动更新积分请使用 `set-points` 命令
3. 自动更新需要 Cookie（可选）

## 发布到 ClawHub

```bash
cd ~/.openclaw/skills/ctrip-points
npx clawhub@latest publish
```

## License

MIT
