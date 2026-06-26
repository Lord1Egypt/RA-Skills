# search-flight · 监控/比价常用参数

以终端为准：

```bash
flyai search-flight --help
```

## 与本 skill 强相关

| 场景 | 建议参数 |
|------|----------|
| 低价优先 | `--sort-type 3` |
| 用户预算上限 | `--max-price <数字>` |
| 仅直飞 | `--journey-type 1`（`2` = 含中转） |
| 往返 | 增加 `--back-date`，或 CLI 文档中的往返日期范围 flag |
| 出发时段 | `--dep-hour-start` / `--dep-hour-end` |
| 到达时段 | `--arr-hour-start` / `--arr-hour-end` |
| 最长接受飞行时长 | `--total-duration-hour` |

## `--sort-type` 速查

| 值 | 含义 |
|----|------|
| 3 | 价格低 → 高 |
| 4 | 耗时短 → 长 |
| 8 | 直达优先 |
| 2 | 推荐排序 |

完整 1～8 以官方文档或 `--help` 为准。

## 调用示例（复制后改日期与城市）

```bash
# 单程低价
flyai search-flight \
  --origin "深圳" --destination "西安" \
  --dep-date 2026-05-01 \
  --journey-type 1 \
  --sort-type 3 \
  --max-price 800

# 往返
flyai search-flight \
  --origin "北京" --destination "广州" \
  --dep-date 2026-06-10 --back-date 2026-06-14 \
  --journey-type 1 \
  --sort-type 3
```
