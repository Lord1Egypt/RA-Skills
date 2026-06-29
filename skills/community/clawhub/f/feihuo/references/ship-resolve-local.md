# ship-resolve-local 命令参考

`ship-resolve-local` 用于解析船票港口，支持模糊匹配。**搜索船票前必须先解析出发港和到达港，取得 `code`。**

## 使用前提

CLI 已内置在技能目录 `./cli/`，通过 FClaw 注入的 `FCLAW_OIDC_TOKEN_URL` 与 `FCLAW_OIDC_TOKEN_SECRET` 从本地 OIDC token 端点获取 access_token。请在 FClaw 中登录，并在技能根目录下执行命令（工作目录须包含 `cli/index.js`）。

## 命令格式

```bash
node ./cli/index.js ship-resolve-local --query <港口名称或代码>
```

## 参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--query <query>` | 是 | 港口名称、城市名称或代码，例如：`琶洲`、`香港`、`PZ` |

## 示例

模糊搜索琶洲港：

```bash
node ./cli/index.js ship-resolve-local --query "琶洲"
```

搜索香港港口：

```bash
node ./cli/index.js ship-resolve-local --query "香港"
```

查看帮助：

```bash
node ./cli/index.js ship-resolve-local --help
```

## 输出

命令输出 JSON。顶层结构为：

```json
{
  "items": []
}
```

`items` 是匹配到的港口列表。每项包含：

| 字段 | 说明 |
| --- | --- |
| `code` | 港口代码，**供 `ship-search` 的 `--dep` / `--arr` 使用** |
| `name` | 港口名称 |
| `cityName` | 所属城市名称 |

无匹配时返回 `"items": []`，不会报错。

## 与搜索命令的关系

1. 对出发港执行 `ship-resolve-local`，从 `items` 中选定 `code` 作为 `--dep`。
2. 对到达港同样解析，选定 `code` 作为 `--arr`。
3. 若 `items` 有多条候选，**必须让用户确认**后再搜索，不要自行猜测。

详细搜索参数见 [ship-search.md](ship-search.md)。
