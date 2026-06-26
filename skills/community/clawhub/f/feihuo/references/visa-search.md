# visa-search 命令参考

`visa-search` 用于搜索签证，支持按目的地国家和签证类型筛选。

## 使用前提

CLI 从 `~/.openclaw/qclaw/user-info.json` 读取 `accessToken`，请求 API 时使用：

```http
Authorization: Bearer <accessToken>
```

请确保该文件存在且 `accessToken` 有效。

## 命令格式

```bash
feihuo visa-search --country <目的地国家> [--visa-type <签证类型>]
```

## 参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--country <country>` | 是 | 目的地国家名称或代码，例如：`日本` |
| `--visa-type <visaType>` | 否 | 签证类型：`tourist` 旅游签证，`business` 商务签证，`family-visit` 探亲签证 |

`--visa-type` 传给 API 的枚举值为 camelCase：`tourist`、`business`、`familyVisit`。CLI 也兼容 `family-visit`、中文（旅游、商务、探亲）及 `LY`、`SW`、`TQ`。

## 自然语言 → CLI 参数

| 用户说法 | CLI 参数 |
| --- | --- |
| 旅游签 / 商务签 / 探亲签 | `--visa-type tourist` / `business` / `family-visit` |

## 示例

搜索指定国家的签证：

```bash
feihuo visa-search --country "日本"
```

筛选旅游签证：

```bash
feihuo visa-search --country "日本" --visa-type tourist
```

筛选商务签证：

```bash
feihuo visa-search --country "日本" --visa-type business
```

筛选探亲签证：

```bash
feihuo visa-search --country "日本" --visa-type family-visit
```

查看帮助：

```bash
feihuo visa-search --help
```

## 输出

命令输出 JSON。顶层结构为：

```json
{
  "items": []
}
```

`items` 是签证产品列表。每个产品包含：

| 字段 | 说明 |
| --- | --- |
| `visaName` | 签证名称 |
| `typeName` | 签证类型名称，例如：旅游签证 |
| `validDay` | 有效期 |
| `needDay` | 办证时间 |
| `stay` | 停留期 |
| `alert` | 重要提示 |
| `price` | 售价 |
| `jumpUrl` | 跳转/预订地址 |

## 展示建议

向用户展示结果时，优先展示：

- 签证名称和类型
- 售价
- 有效期、办证时间和停留期
- 重要提示
- 同一行末尾展示 `[点击预订]({jumpUrl})`

如果有多个签证产品，建议使用 Markdown 表格进行比较。
