# search-flight · 亲子注意事项

完整参数以终端为准：

```bash
flyai search-flight --help
```

## 与带娃强相关的 flag

| 诉求 | 建议 | CLI 选项 |
|------|------|----------|
| 少中转、少折腾 | 优先直达 | `--journey-type 1`（`2` = 中转） |
| 对齐作息 | 避免过早/过晚出发或到达 | `--dep-hour-start` / `--dep-hour-end`，`--arr-hour-start` / `--arr-hour-end` |
| 控制飞行时长 | 太长易闹 | `--total-duration-hour` |
| 预算上限 | 比价 | `--max-price` |
| 排序习惯 | 低价 / 省时 / 直达优先 | `--sort-type` 见 `cli-capabilities.md` |

### `--sort-type` 速查

| 值 | 含义 |
|----|------|
| 3 | 价低 → 高 |
| 4 | 耗时短 → 长 |
| 8 | 直达优先 |
| 2 | 推荐 |

（完整 1～8 含义见 **`cli-capabilities.md`**。）

## 示例

```bash
# 直飞 + 出发时段不要太早（示例：9 点及以后起飞）
flyai search-flight \
  --origin "上海" --destination "东京" \
  --dep-date 2026-07-20 --back-date 2026-07-27 \
  --journey-type 1 \
  --dep-hour-start 9 --dep-hour-end 22 \
  --sort-type 8
```

```bash
# 国内单程、低价优先
flyai search-flight \
  --origin "杭州" --destination "广州" \
  --dep-date 2026-08-01 \
  --journey-type 1 \
  --sort-type 3
```

**说明**：儿童票、婴儿票、占座规则以航司与预订页为准；本命令只负责检索报价维度，**不要编造**儿童票价或证件要求。
