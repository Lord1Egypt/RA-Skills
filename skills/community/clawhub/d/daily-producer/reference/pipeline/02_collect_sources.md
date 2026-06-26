# 02 采集候选池

## 脚本

```bash
python3 scripts/collect_sources_with_opencli.py --date {date} --max-keywords 5 --max-results 5
```

## 作用

从 `config/profile.yaml` 读取信息源配置（`sources.platforms` + `sources.websites`），用 opencli 逐平台采集资讯，建立候选池。

## 输入

- `config/profile.yaml` — `sources.platforms`（opencli 平台列表 + 命令模板）和 `sources.websites`（媒体/官网 URL）
- `config/profile.yaml` — `topics[*].keywords`（关键词，cn 给国内平台，en 给国外平台）

## 输出

- `output/raw/{date}_index.txt` — 原始候选池（自动保存）

## 采集流程

```
1. opencli doctor 检查连接
2. 从 profile keywords 提取关键词（cn + en 各 max_keywords 个）
3. 国内平台采集（cn 关键词）：
   - 每个平台按 commands 模板执行（hot/search 等）
   - 关键词逐个搜索，每次间隔 3 秒防限流
4. 国外平台采集（en 关键词）：
   - 同上，Reddit 特殊处理（自动探测 opencli 可用性，不通走 API+代理）
5. 网站类采集：
   - opencli web read 抓首页
   - opencli google search "site:域名 关键词 after:日期" 定向搜索
6. 合并所有结果，保存到 index.txt
```

## 输出格式

每条记录：

```
--- [平台名] (cn/global/website) ---
command: 实际执行的 opencli 命令
keyword: 搜索关键词
status: success/FAILED
fetch_stack: opencli / reddit-api-proxy
count: 结果数

  [1] 标题/内容全文
      author: 作者
      subreddit: r/xxx（仅 Reddit）
      time: 时间字段（各平台格式不同）
      duration: 视频时长（仅 YouTube）
      hot: 热度值
      url: 链接
```

## 各平台时间字段

| 平台 | 时间字段 | 格式 |
|------|---------|------|
| Twitter | created_at | `Fri Apr 03 14:00:17 +0000 2026` |
| 小红书 | published_at | `2026-04-03` |
| 微博 | time | `04月03日 12:40` / `今天08:04` / `3小时前` |
| Reddit (API) | created_utc | 自动转为 `2026-04-03 14:00` |
| YouTube | published | `2 days ago` |
| 36氪 | date | `2026-04-05` |
| B站/知乎/HN/V2EX | 无 | — |

详细参考：`reference/opencli_output_formats.md`

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--date` | 今天 | 目标日期 |
| `--max-keywords` | 15 | 每个语言组最多搜索的关键词数 |
| `--max-results` | 0 | 每次搜索最多保留的结果数，0=不限 |
| `--platform` | 空 | 只采集指定平台（逗号分隔，如 `weibo,twitter`） |
| `--skip-websites` | false | 跳过媒体/官网采集 |
| `--no-save` | false | 不保存到文件 |

## 注意事项

- 统计数量以 `--max-results` 截断后的实际输出为准（头部 `# 总候选条目` 和文件内 `[N]` 条目数一致）
| `--dry-run` | false | 只输出要执行的命令，不实际执行 |

## 特殊处理

- **Reddit**：自动探测 opencli reddit 是否可用。不通则切换到 Reddit JSON API + 代理（`PROXY_CONFIG` 中配置）
- **请求间隔**：每次 opencli 请求间隔 3 秒（`REQUEST_DELAY`），防止平台限流
- **未登录降级**：平台返回 `🔒 Not logged in` 时记录失败，不中断采集
