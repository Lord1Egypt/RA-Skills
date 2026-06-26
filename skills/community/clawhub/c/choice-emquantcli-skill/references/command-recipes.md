# EMQ CLI Command Recipes

## 行情查询

```bash
# 单票快照
emq market snapshot 000001.SZ CLOSE

# 多票多指标快照
emq market snapshot 000001.SZ,000002.SZ CLOSE,VOLUME,OPEN --output table

# 序列查询
emq market series 000001.SZ CLOSE --start 2025-01-01 --end 2025-01-31 --output csv
```

## 组合管理与下单

```bash
# 创建组合
emq portfolio create --code DEMO_PF --name "Demo Portfolio" --initial-fund 1000000 --remark "created by cli"

# 查看组合
emq portfolio list --output table

# 快速单笔下单
emq portfolio qorder --code DEMO_PF --stock 300059.SZ --volume 1000 --price 10.5 --date 2025-01-15 --time 14:30:00 --type 1
```

### 批量下单 JSON 示例

```json
{
  "code": ["300059.SZ", "000001.SZ"],
  "volume": [1000, -500],
  "price": [10.5, 12.2],
  "date": ["20250115", "20250115"]
}
```

```bash
emq portfolio order --code DEMO_PF --orders-file ./orders.json --remark "batch order"
emq raw porder --code DEMO_PF --orders-file ./orders.json --remark "raw batch order"
```

## 额度查询

```bash
# 最近 30 天默认窗口
emq quota usage

# 指定窗口 + 功能过滤
emq quota usage --start 2025-01-01 --end 2025-01-31 --func css --output table
```

## 原始命令透传

```bash
emq raw css 000001.SZ CLOSE --options "TradeDate=2025-01-15"
emq raw csd 000001.SZ CLOSE --start 2025-01-01 --end 2025-01-31 --options "Ispandas=0"
emq raw pquery --options "CombinCode=DEMO_PF"
```
