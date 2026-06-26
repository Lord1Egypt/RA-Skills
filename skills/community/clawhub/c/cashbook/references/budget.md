# 预算管理（budget.py）

## 命令

```bash
python3 scripts/budget.py set --category 餐饮 --amount 2000 --period monthly
python3 scripts/budget.py set --total --amount 8000 --period monthly  # 总预算
python3 scripts/budget.py query --category 餐饮   # 查询某分类预算进度
python3 scripts/budget.py query --all              # 查询所有分类进度
python3 scripts/budget.py list                     # 列出所有预算设置
python3 scripts/budget.py delete --category 餐饮
```

## 查询输出格式

```
本月餐饮预算：¥2,000.00
已支出：¥1,234.00（61.7%）
剩余：¥766.00（还剩 16 天）
```

## 超支告警规则

- 某分类超过预算 100% → 在记录新支出时主动提示
- 总预算超过 80% → 主动提示（可配置阈值）
- 告警文本示例：⚠️ 本月餐饮已超支 ¥234，超预算 11.7%

## period 说明

- `monthly`：自然月（每月1日重置）
- `weekly`：自然周（每周一重置）
