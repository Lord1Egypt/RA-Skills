# eur-rail-p2p-resolve-local 命令参考

`eur-rail-p2p-resolve-local` 用于解析欧铁城市或车站，支持模糊匹配。**搜索欧铁点对点车次前必须先解析出发地和到达地，取得 `code`。**

## 使用前提

CLI 已内置在技能目录 `./cli/`，通过 FClaw 注入的 `FCLAW_OIDC_TOKEN_URL` 与 `FCLAW_OIDC_TOKEN_SECRET` 从本地 OIDC token 端点获取 access_token。请在 FClaw 中登录，并在技能根目录下执行命令（工作目录须包含 `cli/index.js`）。

## 命令格式

```bash
node ./cli/index.js eur-rail-p2p-resolve-local --query <城市或车站> [--type <地点类型>]
```

## 参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--query <query>` | 是 | 城市或车站名称/代码，例如：`巴黎`、`Paris` |
| `--type <type>` | 否 | 地点类型：`city` 城市，`station` 车站；也兼容中文 `城市`、`车站` |

API 枚举值为 camelCase：`city`、`station`。

## 示例

模糊搜索巴黎：

```bash
node ./cli/index.js eur-rail-p2p-resolve-local --query "巴黎"
```

只搜索车站：

```bash
node ./cli/index.js eur-rail-p2p-resolve-local --query "Paris" --type station
```

查看帮助：

```bash
node ./cli/index.js eur-rail-p2p-resolve-local --help
```

## 输出

命令输出 JSON。顶层结构为：

```json
{
  "items": []
}
```

`items` 是匹配到的地点列表。每项包含：

| 字段 | 说明 |
| --- | --- |
| `code` | 地点代码，**供 `eur-rail-p2p-search` 的 `--dep` / `--arr` 使用** |
| `name` | 展示名称（优先中文名） |
| `countryName` | 国家名称 |
| `type` | 类型：`city` 城市，`station` 车站 |

无匹配时返回 `"items": []`，不会报错。

## 与搜索命令的关系

1. 对出发地执行 `eur-rail-p2p-resolve-local`，从 `items` 中选定 `code` 作为 `--dep`。
2. 对到达地同样解析，选定 `code` 作为 `--arr`。
3. 若 `items` 有多条候选，**必须让用户确认**后再搜索，不要自行猜测。

详细搜索参数见 [eur-rail-p2p-search.md](eur-rail-p2p-search.md)。
