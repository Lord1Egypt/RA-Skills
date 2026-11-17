# 只读审计 JSON 契约

版本：`schemaVersion=1.0`。字段保持向后兼容；新增字段不得改变已有字段的含义。

## 命令与退出码

```sh
python3 scripts/agent_slim.py audit --json
python3 scripts/agent_slim.py audit --output report.md
python3 scripts/agent_slim.py audit --home <CODEX_HOME> --max-depth 8 --fail-on-warning
```

| 退出码 | 含义 |
| ---: | --- |
| `0` | 盘点完成；允许存在 warning，除非启用 warning 门禁 |
| `2` | `--fail-on-warning` 启用且报告含 warning |
| `64` | 命令行参数错误 |
| `74` | CODEX_HOME 不存在、输出写入失败或盘点失败 |

`--home` 优先于环境变量 `CODEX_HOME`；两者都缺省时使用当前用户的默认 Codex Home。路径不得依赖用户名或固定挂载点。

## 顶层字段

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `schemaVersion` | string | 固定为 `1.0` |
| `tool` | object | 名称和版本 |
| `runId` | string | 同一 Home 与扫描深度的稳定指纹 |
| `createdAt` | string | 本次运行的 UTC 时间；这是两次输出唯一的预期时间差异 |
| `mode` | string | 固定为 `dry-run` |
| `host` | object | `kind`、Home 绝对路径和来源 |
| `scope` | object | 深度、Home 相对路径模式、是否读取会话正文 |
| `tokenEstimate` | object | 近似算法与“不是账单实测”标记 |
| `summary` | object | 分层汇总、磁盘账本、warning/unknown 计数 |
| `layers` | object | `hot`、`warm`、`cold` 三个数组 |
| `candidates` | array | 冷热候选、动作、风险、回滚和近似内容体积 |
| `referenceGraph` | array | 从声明文件到目标路径的引用边 |
| `plugins` | array | 已启用插件的声明与文件级可发现工具面 |
| `warnings` | array | 需要处理或人工确认的问题 |
| `unknowns` | array | 缺失证据、不可读对象和平台限制 |
| `limitations` | array | 全局口径与隐私边界 |
| `errors` | array | 阻断级失败；当前主要对应 Home 不可用 |

## 条目字段

每个 `layers.*[]` 条目至少包含：

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定、可排序的对象标识 |
| `layer` | `hot`、`warm` 或 `cold` |
| `category` | `instructions`、`rules`、`skill-metadata`、`plugin`、`skill-body`、`reference`、`pack`、`template`、`sessions`、`backups`、`logs`、`databases` 等 |
| `kind` | `file` 或 `aggregate` |
| `label` | 不含正文的显示名 |
| `evidencePath` | Home 相对证据路径 |
| `loadedWhen` | 每轮、启动、触发或仅磁盘 |
| `bytes` | 文件系统字节；磁盘对象标记为 `measured` |
| `chars` | UTF-8 解码后的字符数；会话、备份、日志和数据库为 `null` |
| `estimatedTokens` | `ceil(chars * 0.6)` 的近似值；Cold 固定为 `0` |
| `evidence` | `bytes`、`chars`、`tokens` 三类证据标签 |
| `riskHint` | `R0` 至 `R3` 的风险提示 |
| `reversibility` | 只读、备份恢复、移回原路径、事务恢复或不在范围内 |
| `references` | 该对象声明的引用边 |
| `candidate` | 是否进入冷热候选清单 |
| `meta` | 分类专属的非正文元数据 |

## 排序与稳定性

- 层级顺序固定为 Hot、Warm、Cold。
- 同层先按 `category`，再按估算 Token 降序、字节降序、`id` 升序。
- 候选同层按估算 Token、字节和 `id` 稳定排序。
- `createdAt` 是唯一预期随时间变化的字段；同一 fixture 在文件状态不变时应得到相同内容。
- Token 只按字符数近似，和宿主实际 `input + output` 无关。不能把 `estimatedTokens` 写成已实现节省，也不能把 Cold 字节换算为 Token。

## 读取边界

- `sessions/`、`archived_sessions/`、`backups/`、`log/` 和 `logs/` 只做 `stat`/目录枚举，不打开正文。
- 数据库只做路径、数量、字节和时间元数据统计；不读取表、不执行 VACUUM。
- 插件 JSON 只提取服务器、工具名、应用名和 Skill 路径；不输出环境变量或密钥。
- 报告不包含 Skill/规则正文，只包含用于证据定位的相对路径和体积。
