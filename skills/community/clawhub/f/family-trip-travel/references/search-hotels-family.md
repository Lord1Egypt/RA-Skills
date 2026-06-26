# search-hotels · 亲子注意事项

完整参数以终端为准：

```bash
flyai search-hotels --help
```

## CLI 真实能力（避免误用）

- **`--hotel-bed-types`** 仅支持：**`大床房`**、**`双床房`**、**`多床房`**（多选用英文逗号分隔）。没有单独的「家庭房」「连通房」枚举。
- **`--hotel-types`**：**`酒店`**、**`民宿`**、**`客栈`**。
- **`--sort`**：`distance_asc`、`rate_desc`、`price_asc`、`price_desc`、`no_rank`。
- 需要 **亲子设施**（儿童乐园、泳池、洗衣、加床政策、连通房等）：用 **`--key-words`**（如 `亲子`）或改走 **`fliggy-fast-search --query "…"`** 描述清楚。

## 亲子场景映射表

| 诉求 | 怎么用 CLI |
|------|------------|
| 两大一小两张床 | `--hotel-bed-types "双床房"` 或 `"多床房"`（看供给） |
| 靠近乐园 / 博物馆 | `--poi-name "长隆"`、`--poi-name "迪士尼"` 等 + `--dest-name` |
| 控制预算 | `--max-price`（元/晚） |
| 口碑优先 | `--sort rate_desc` |
| 离某点近 | `--sort distance_asc`（需 POI/目的地配合） |
| 要民宿 | `--hotel-types "民宿"` |

## 示例

```bash
flyai search-hotels \
  --dest-name "珠海" \
  --poi-name "长隆" \
  --key-words "亲子" \
  --check-in-date 2026-08-01 \
  --check-out-date 2026-08-03 \
  --hotel-bed-types "双床房" \
  --sort rate_desc
```

展示给用户时：若 JSON 含 `mainPic`、`detailUrl`（或 `jumpUrl`），**先独立一行图片，再独立一行预订链接**（见主 `SKILL.md`）。
