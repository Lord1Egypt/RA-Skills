# Config JSON Schema

`scripts/search_cnki.js` 接受一个 JSON config（文件路径、默认 demo、`--json` 字符串三种方式传入）。

## 入口 URL（cnki_url）

CNKI 入口 URL **不通过 config 传入**，而是从 `scripts/user_config.json` 的 `url` 字段读取（首次运行由 agent 收集并写入）。
若 config 本身带 `cnki_url` 字段则优先使用。详见 `SKILL.md` 工作流第 1 步。

```jsonc
// scripts/user_config.json
{
  "url": "https://www.cnki.net/"
}
```

## 完整字段

```json
{
  "cnki_url": "https://www.cnki.net/",          // 可选：覆盖 user_config.json；省略则自动从 user_config.json 读
  "keyword": "区块链",                         // 必填：检索关键词（字符串）
  "sort": {                                    // 可选
    "field": "发表时间",                        //  必填：字段名
    "order": "DESC"                             //  必填：DESC 降序 / ASC 升序
  },
  "filters": [                                 // 可选：多筛选条件
    {
      "col":   "来源类别",                      //  必填：筛选项名
      "values": ["北大核心", "CSSCI"]           //  必填：选项值列表
    },
    { "col": "年度", "values": ["2024", "2025"] }
  ],
  "download_count": 5                          // 必填：要下载的篇数（>= 1）
}
```

## 字段枚举


### `filters[].col`
- `来源类别`
- `年度`


### `sort.field`
- `相关度`（默认）
- `发表时间`
- `被引`
- `下载`
- `综合`

### `sort.order`
- `DESC`（降序，默认）
- `ASC`（升序）


## 必填校验

| 字段 | 校验 |
|---|---|
| `cnki_url` | 非空字符串 + 合法 URL（最终由 search_cnki.js 从 user_config.json 注入；缺失则 CLI 退出码 2） |
| `keyword` | 非空字符串 |
| `download_count` | 整数且 >= 1 |
| `sort` | 省略则用知网默认排序 |
| `filters` | 省略则不筛选 |

校验失败时 `runPipeline` 会直接抛错（CLI 退出码 2）。

## 落地路径

下载目录固定为 `./scripts/download/`（自动创建）。文件命名由知网返回的 PDF 二进制内容决定（一般是 `{DocID}.pdf`）。

## 三个调用方式示例

```powershell
# A. 默认 demo（不传参数 = 用 assets/default-config.json 类似的 hard-coded demo）
cd skills/cnki-download
node scripts/search_cnki.js

# B. 读 JSON 配置文件（任意路径都行）
node scripts/search_cnki.js path/to/your-config.json

# C. 直接传 JSON 字符串
node scripts/search_cnki.js --json '{"keyword":"深度学习","download_count":3}'
```

> PowerShell 中 `&&` 不可用，请分多行；`--json` 字符串外层用单引号更稳。