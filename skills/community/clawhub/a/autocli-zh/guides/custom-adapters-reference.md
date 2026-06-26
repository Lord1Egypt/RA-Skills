# Custom Adapters Reference

在需要进一步查自定义适配器细节、排障或阅读 autocli 内部实现时使用本文件。

使用本文件前，默认前提是：用户已经同意进入自定义适配器 / 定向排障流程。涉及 `evaluate`、`intercept`、`tap` 时，不把它们当作常规浏览手段滥用。

## Pipeline 扩展步骤

除主 guide 中的高频步骤外，还可按需使用：
- `filter`：过滤数据
- `sort`：排序
- `intercept`：网络拦截
- `tap`：状态管理桥接
- `download`：下载资源

## 模板表达式

Pipeline 中可使用 `${{ expression }}` 语法，例如：

```text
${{ args.limit }}
${{ item.title }}
${{ index + 1 }}
${{ item.score > 10 }}
${{ item.active ? 'yes' : 'no' }}
${{ item.title | truncate(30) }}
https://api.com/${{ item.id }}.json
${{ item.subtitle || 'N/A' }}
${{ Math.min(args.limit, 50) }}
```

内置过滤器包括：
- `default`
- `join`
- `upper`
- `lower`
- `trim`
- `truncate`
- `replace`
- `keys`
- `length`
- `first`
- `last`
- `json`
- `slugify`
- `sanitize`
- `ext`
- `basename`

## 配置与路径

可选调试环境变量（非普通使用必需）：
- `OPENCLI_VERBOSE`：启用详细输出
- `OPENCLI_DAEMON_PORT`：Daemon 端口，默认 `19825`
- `OPENCLI_CDP_ENDPOINT`：CDP 直连端点
- `OPENCLI_BROWSER_COMMAND_TIMEOUT`：命令超时，默认 `60` 秒
- `OPENCLI_BROWSER_CONNECT_TIMEOUT`：浏览器连接超时，默认 `30` 秒
- `OPENCLI_BROWSER_EXPLORE_TIMEOUT`：Explore 超时，默认 `120` 秒

相关路径：
- `~/.autocli/adapters/`：用户自定义适配器，持久化写入前须先获用户许可
- `~/.autocli/plugins/`：用户插件，持久化写入前须先获用户许可
- `~/.autocli/external-clis.yaml`：用户外部 CLI 注册表，改写前须先获用户许可

## 架构速览

自定义适配器在 autocli 中的大致位置是：
- CLI 层：`autocli <site> <command>` 负责参数解析、命令发现与执行编排。
- 发现层：YAML 适配器会被 discovery 层加载并注册成动态子命令。
- 执行层：命令进入 pipeline 引擎，按 `pipeline` 中的步骤顺序执行。
- 浏览器层：若适配器依赖浏览器能力，则通过 BrowserBridge 接到 daemon / CDP / Chrome 扩展链路。
- 输出层：结果最终按 table / json / yaml / csv / markdown 等格式渲染。

可以把它理解成：
`YAML adapter → discovery → execution/pipeline → browser bridge（如需）→ output`

## Workspace / 源码定位

若需要进一步读 autocli 源码，优先关注这些目录：
- `crates/autocli-core/`：核心数据模型与通用 trait
- `crates/autocli-pipeline/`：pipeline 引擎、表达式解析、步骤执行
- `crates/autocli-browser/`：浏览器桥接、daemon、CDP 相关实现
- `crates/autocli-output/`：输出渲染
- `crates/autocli-discovery/`：YAML 适配器发现与加载
- `crates/autocli-external/`：外部 CLI 透传
- `crates/autocli-ai/`：`explore` / `cascade` / `generate` 等 AI 能力
- `crates/autocli-cli/`：CLI 入口、执行编排、`doctor`
- `adapters/`：内置 YAML 适配器定义
- `resources/external-clis.yaml`：外部 CLI 注册表
