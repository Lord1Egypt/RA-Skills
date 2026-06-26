# eur-rail-pass-search 命令参考

`eur-rail-pass-search` 用于搜索欧铁通票（Eurail Pass 等产品），支持按欧洲国家筛选；不传国家时返回欧洲通票列表。

## 使用前提

CLI 从 `~/.openclaw/qclaw/user-info.json` 读取 `accessToken`，请求 API 时使用：

```http
Authorization: Bearer <accessToken>
```

请确保该文件存在且 `accessToken` 有效。

## 命令格式

```bash
feihuo eur-rail-pass-search [--country <欧洲国家>]
```

## 参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--country <country>` | 否 | 欧洲国家名称或代码，例如：`法国`、`瑞士`；不传入时搜索欧洲通票 |

## 自然语言 → CLI 参数

| 用户说法 | CLI 参数 |
| --- | --- |
| 法国通票 / 瑞士的欧铁通票 | `--country "法国"` / `"瑞士"` |
| 欧洲通票 / 不限国家 | 不传 `--country` |

当前 CLI **无**价格区间参数；若用户指定预算，在展示结果时说明即可，**不要**伪造筛选后的列表。

## 示例

搜索欧洲通票（不限定国家）：

```bash
feihuo eur-rail-pass-search
```

搜索指定国家的通票：

```bash
feihuo eur-rail-pass-search --country "法国"
```

```bash
feihuo eur-rail-pass-search --country "瑞士"
```

查看帮助：

```bash
feihuo eur-rail-pass-search --help
```

## 输出

命令输出 JSON。顶层结构为：

```json
{
  "items": []
}
```

`items` 是欧铁通票产品列表。每个产品包含：

| 字段 | 说明 |
| --- | --- |
| `name` | 通票名称 |
| `applicableCountries` | 适用国家/地区（展示名称） |
| `minPrice` | 最低价格（欧元） |
| `jumpUrl` | 跳转/预订地址 |

## 展示建议

向用户展示结果时，优先展示：

- 通票名称、适用国家/地区、最低价格（欧元）
- 同一行末尾展示 `[点击预订]({jumpUrl})`

```markdown
**{name}** · {applicableCountries} · {minPrice} EUR · [点击预订]({jumpUrl})
```

如果有多个通票，建议使用 Markdown 表格进行比较。

## 相关说明

- 欧铁**点对点**车次搜索见 [eur-rail-p2p-resolve-local.md](eur-rail-p2p-resolve-local.md) 与 [eur-rail-p2p-search.md](eur-rail-p2p-search.md)。
- 与国内火车票 `train-search` 不同，通票搜索不需要出发地、目的地和乘车日期。
