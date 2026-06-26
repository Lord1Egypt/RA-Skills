# API 参考文档 — 亿邦原创新闻频道 JSON 接口

## 接口基础信息

| 属性 | 值 |
|------|----|
| Base URL | `https://www.ebrun.com/` |
| 路径模板 | `{base_url}{channel_path}` |
| 方法 | `GET` |
| 认证 | 无需认证 |
| 推荐请求头 | `User-Agent`、`Accept`、`Referer` |
| 响应格式 | `application/json` |
| 顶层结构 | `array` |
| 默认读取条数 | Skill 默认取前 `10` 条，脚本可用 `--limit` 调整 |
| 频道映射来源 | `references/channel-list.json` |

## 频道路径说明

该接口没有公开的业务参数文档，Skill 通过 `references/channel-list.json` 中维护的 `channel_path` 访问不同频道。

| 频道 | 子频道 | channel_path |
|------|--------|--------------|
| 推荐 | 最新 | `_index/ClaudeCode/SkillJson/information_recommend.json` |
| AI | 最新 | `_index/ClaudeCode/SkillJson/information_channel_88.json` |
| 跨境电商 | 最新 | `_index/ClaudeCode/SkillJson/information_channel_51.json` |
| 跨境电商 | 亚马逊 | `_index/ClaudeCode/SkillJson/information_channel_68.json` |
| 未来零售 | 抖音 | `_index/ClaudeCode/SkillJson/information_channel_56.json` |
| 品牌 | 品牌全球化 | `_index/ClaudeCode/SkillJson/information_channel_90.json` |

完整频道清单请直接读取 `references/channel-list.json`，不要手写猜测频道路径。

## 请求示例

```http
GET https://www.ebrun.com/_index/ClaudeCode/SkillJson/information_channel_88.json
```

```http
GET https://www.ebrun.com/_index/ClaudeCode/SkillJson/information_recommend.json
```

也可以优先通过 Skill 自带脚本访问：

```bash
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10
bash scripts/fetch_news.sh "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10
```

默认输出为 JSON；只有显式传 `--table` 时才输出表格文本。

## 响应结构

### 顶层结构

接口成功时返回 JSON 数组，每个元素代表一篇文章。

| 字段 | 类型 | 说明 |
|------|------|------|
| `[]` | array | 文章列表；为空数组表示当前频道暂无数据或筛选后无结果 |

### 数组元素字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `title` | string | 文章标题 | `"阿里“电商龙虾”重大更新：中国工厂可一键搬上跨境电商平台！"` |
| `author` | string | 作者名称 | `"王浩然"` |
| `summary` | string | 文章摘要 | `"3月底，阿里在海外发布的企业级Agent..."` |
| `publish_time` | string | 发布时间，格式 `YYYY-MM-DD HH:mm:ss` | `"2026-04-20 09:34:57"` |
| `url` | string | 原文链接，HTTPS 地址 | `"https://www.ebrun.com/20260420/656585.shtml"` |

### 兼容字段说明

当前真实接口返回的主字段为 `title`、`author`、`summary`、`publish_time`、`url`。

Skill 脚本在输出前还会做两层防御性处理：

1. 清理标题、作者、摘要、发布时间中的控制字符和异常空白
2. 如果 `url` / `link` 不是指向亿邦白名单域名的 HTTPS 地址，则清空该字段，避免把不可信链接继续传到上层输出

Skill 自带脚本为了兼容潜在格式波动，也会兼容读取以下备用字段：

| 主字段 | 兼容备用字段 |
|--------|--------------|
| `publish_time` | `publishTime` |
| `summary` | `description` |
| `url` | `link` |

## 完整响应示例

```json
[
  {
    "summary": "3月底，阿里在海外发布的企业级Agent——Accio Work，凭借着电商领域专有Skills和系统性的稳定落地能力，在海外中小商家群体，甚至OPC群体中引起了一场狂欢 。",
    "author": "王浩然",
    "publish_time": "2026-04-20 09:34:57",
    "title": "阿里“电商龙虾”重大更新：中国工厂可一键搬上跨境电商平台！",
    "url": "https://www.ebrun.com/20260420/656585.shtml"
  }
]
```

## 错误处理

| 场景 | 说明 | 处理建议 |
|------|------|----------|
| `200` | 成功，返回 JSON 数组 | 正常解析并截取前 N 条 |
| `403` | 访问被拒绝 | 检查请求来源、请求头或站点策略变化 |
| `404` | 频道 JSON 不存在 | 检查 `channel_path` 是否正确，优先从 `channel-list.json` 读取 |
| `429` / `500` / `502` / `503` / `504` | 服务暂时不可用或被限流 | 等待后重试，建议最多 3 次 |
| 网络超时 | 请求超时或连接失败 | 稍后重试，必要时切换脚本或网络环境 |
| JSON 解析失败 | 返回内容不是合法 JSON | 视为接口格式异常，停止继续解析 |
| 顶层不是数组 | 接口格式变更 | 视为接口格式异常，停止继续解析 |

## 防御性处理示例

优先直接使用 Skill 自带脚本，而不是在运行时重写抓取逻辑。

```bash
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10 --timeout 10 --retries 3
```

脚本当前已内置以下防御性处理：

1. 域名白名单校验，仅允许请求 `www.ebrun.com` 和 `api.ebrun.com`
2. 参数校验，禁止非法 `--limit`、`--timeout`、`--retries`
3. HTTP 状态码分类处理，对 `403`、`404`、`503` 等返回明确错误
4. 对 `429`、`500`、`502`、`503`、`504` 和超时场景做有限重试
5. JSON 结构校验，要求顶层必须为对象数组

## 数据来源说明

该接口数据来自亿邦动力站点的频道 JSON 文件，不同主频道和子频道对应不同的 `channel_path`。Skill 不直接抓取网页 HTML，而是优先读取这些 JSON 资源，以降低解析复杂度并提升稳定性。

## URL 构造规则速查

```text
BASE_URL     = "https://www.ebrun.com/"
CHANNEL_PATH = "_index/ClaudeCode/SkillJson/information_channel_88.json"

完整 URL = BASE_URL + CHANNEL_PATH
示    例 = "https://www.ebrun.com/_index/ClaudeCode/SkillJson/information_channel_88.json"
```

## 版本检查接口

### 接口基础信息

| 属性 | 值 |
|------|----|
| URL | `https://www.ebrun.com/_index/ClaudeCode/SkillJson/skill_version.json` |
| 方法 | `GET` |
| 认证 | 无需认证 |
| 响应格式 | `application/json` |
| 顶层结构 | `object` |
| 当前关心字段 | `ebrun-original-news` |

### 请求示例

```http
GET https://www.ebrun.com/_index/ClaudeCode/SkillJson/skill_version.json
```

### 响应结构

接口成功时返回一个 JSON 对象，key 为 skill 名称，value 为对应的远端版本号。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `ebrun-original-news` | string | 当前 skill 的远端版本号 | `"1.0.0"` |

### 响应示例

```json
{
  "ebrun-original-news": "1.0.0"
}
```

## 版本比较规则

版本检查时，不使用本地 `references/version.json` 中的 `latest_version` 作为比较依据。

实际比较规则如下：

1. 优先请求版本接口，读取 `ebrun-original-news` 字段
2. 读取本地 `references/version.json` 中的 `current_version`
3. 将远端接口版本号与本地 `current_version` 做比对
4. 如果两者不一致，则提示更新

## 检查频率控制

本地 `references/version.json` 中的 `check_interval_hours` 用于控制最短检查间隔，避免每次调用都访问远端。
运行时缓存单独写入临时缓存文件，不回写 `references/version.json`。

| 字段 | 类型 | 说明 |
|------|------|------|
| `check_interval_hours` | number | 最短检查间隔，单位为小时 |
| `last_check_time` | int | 上次成功获取远端版本信息的 Unix 时间戳（秒） |
| `last_known_version` | string | 上次成功检查到的远端版本号 |
| `last_check_source` | string | 上次成功检查的来源，如 `remote_api`、`github_version_json` |
| `last_update_available` | boolean | 上次检查时是否检测到更新 |
| `last_version_file_url` | string | 上次降级到远端仓库版本文件时使用的实际地址 |

### 频率控制规则

1. 如果当前时间距离 `last_check_time` 未超过 `check_interval_hours`
2. 且本地已有 `last_known_version`、`last_check_source` 等缓存字段
3. 则默认直接返回缓存结果，不再联网请求
4. 此时脚本返回的 `status` 为 `cached`
5. 如需忽略间隔限制，可使用 `--force` 强制执行远端检查
6. 如果显式传入自定义 `--version-url`，只会复用同一版本接口地址对应的缓存结果

## 版本接口失败时的降级策略

如果版本接口请求失败，不再使用本地 `latest_version` 做兜底比较，而是继续执行以下降级流程：

1. 读取本地 `references/version.json` 中的 `update_url_github` 和 `update_url_gitee`
2. 从仓库地址推导远端 `references/version.json` 地址
3. 优先读取远端仓库中的 `current_version`
4. 将远端仓库中的 `current_version` 与本地 `current_version` 做比对
5. 如果版本接口和远端仓库版本文件都失败，才返回“当前无法判断是否有更新”

### 远端仓库版本文件地址推导规则

#### GitHub

由仓库地址：

```text
https://github.com/<owner>/<repo>
```

推导候选地址：

```text
https://raw.githubusercontent.com/<owner>/<repo>/main/references/version.json
https://raw.githubusercontent.com/<owner>/<repo>/master/references/version.json
```

#### Gitee

由仓库地址：

```text
https://gitee.com/<owner>/<repo>
```

推导候选地址：

```text
https://gitee.com/<owner>/<repo>/raw/main/references/version.json
https://gitee.com/<owner>/<repo>/raw/master/references/version.json
```

## 更新脚本输出字段

`scripts/update.py` 和 `scripts/update.sh` 会输出以下关键字段：

| 字段 | 说明 |
|------|------|
| `current_version` | 本地 `references/version.json` 中的当前版本 |
| `latest_version` | 远端版本接口或远端仓库版本文件中的版本号 |
| `update_available` | 是否检测到新版本 |
| `check_source` | 版本来源，可能为 `remote_api`、`github_version_json`、`gitee_version_json` 或 `unavailable` |
| `version_file_url` | 降级到远端仓库版本文件时，实际使用的远端 `references/version.json` 地址 |
| `remote_check_error` | 版本接口失败原因 |
| `repo_version_check_error` | 远端仓库版本文件检查失败原因 |

### 更新脚本示例

```bash
python3 scripts/update.py --json
bash scripts/update.sh --json
python3 scripts/update.py --json --force
```

默认输出为 JSON；只有显式传 `--table` 时才输出文本结果。

## 版本检查错误处理

| 场景 | 处理方式 |
|------|----------|
| 版本接口返回 `200` | 读取 `ebrun-original-news` 字段并直接比较 |
| 版本接口返回 `403` / `404` / `503` | 记录错误并降级到远端仓库 `references/version.json` |
| 版本接口超时或网络失败 | 重试后降级到远端仓库 `references/version.json` |
| 远端仓库版本文件可读 | 读取其中的 `current_version` 做比较 |
| 远端仓库版本文件不可读 | 返回 `check_source = unavailable`，表示当前无法判断是否有更新 |
