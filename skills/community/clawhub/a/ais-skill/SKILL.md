---
name: kb-skill
description: 通过 TorchV AIS 知识库远端与用户协作使用这个技能，可进行的操作包括阅读结构、搜索和读取文档、创建文档或目录、修改文档、发布或返回可跳转的文档链接时。需要利用脚本将 `kb ...` 命令发送到远端 AIS 执行。
---

# KB Skill

你拥有一个内置的知识库AIS(通过kb命令操作)。你的职责是精确完成当前 KB 任务，除非用户要求，不要大规模进行改动。
AIS 是一个**持久化、版本化的Knowledge Base**
AIS 中的操作会真实生效，且用户也会通过UI使用。可能因为权限、并发或约束失败。
通过这个技能操作远端 KB/AIS 时，不要假设本机存在 `kb` 可执行文件。普通 `kb ...` 命令始终交给 [scripts/kb_execute.py](./scripts/kb_execute.py) 发送到 KB 执行服务；文件上传、文件直下载、生成下载链接属于特殊能力，走脚本内置的文件接口，不走 `kb ...` 字符串。


## 术语约定：

- “AIS / 知识库 / KB”默认都指知识库本身
- AIS 中存储的是知识内容： `仓库` 包含 `目录` 包含 `文档`,每个都有稳定唯一标识（code），但可能存在同name。
- `仓库`：别名空间、space、container、知识库,工作区也是一种仓库，一般用户在工作区工作。
- `目录`：别名文件夹、folder，视为一种特殊的文档，没有内容。
- `文档`：别名页面、Page、Wiki，有多种格式如pdf、md、excel。但无论哪种，你阅读到的都是AIS解析后的干净文本。


## 配置执行环境

优先使用环境变量：

```bash
export KB_EXECUTE_URL="https://bot.torchv.com"
export KB_TOKEN="xxxxxx"
```

也可以在调用时显式传参如下：

```bash
./scripts/kb_execute.py --url "https://bot.torchv.com" --token "xxxxxx" "kb cat --code 2031630406710923264"
```

如果命令较长、包含多行 patch，优先把完整命令写入本地 UTF-8 文本文件，再用 `--command-file` 发送：

```bash
./scripts/kb_execute.py --command-file /tmp/kb-command.txt
```

> 若无 token，直接向用户索要，并说明可以在已登录 AIS 页面里打开开发者工具，找到一个知识库请求，从请求头中复制 `token` 或 `Authorization` 的值。

默认请求体为：

```json
{
  "command": "kb <command> [args]"
}
```

并自动带上请求头：

```text
Content-Type: application/json
token: <KB_TOKEN>
```

如还需要其他头，追加 `--header key=value`。

## 运行命令

把真实 KB 命令整体作为一个字符串传给脚本：

```bash
./scripts/kb_execute.py "kb ls"
./scripts/kb_execute.py "kb search --query \"发布流程\" --repo-code TEAM_DOCS --mode hybrid --topk 10"
./scripts/kb_execute.py "kb cat --code 2031630406710923264"
./scripts/kb_execute.py "kb render 2031630406710923264"
```

脚本会向执行服务发起 POST 请求并输出响应；如果服务返回 JSON，脚本会格式化打印。命令失败后，不要假设 KB 状态已经变化，先重新读取确认。

文件相关能力直接走脚本内置参数，不走 `kb ...` 字符串：

```bash
./scripts/kb_execute.py --upload-file ./demo.pdf --path-name "/团队空间/附件"
./scripts/kb_execute.py --download-code 2031630406710923264 --save-to /tmp/
./scripts/kb_execute.py --download-code 2031630406710923264 --extract-is true --save-to /tmp/result.md
./scripts/kb_execute.py --download-link-code 2031630406710923264 --extract-is false
```

如果 `--download-code` 返回的是 JSON 错误而不是文件内容，脚本会直接失败退出。此时优先改用 `--download-link-code` 生成票据，再用 `wget` 或 `curl` 验证下载链路。

## 执行前检查

- 先确认 `KB_EXECUTE_URL` 和 `KB_TOKEN` 已提供，或本次调用显式传入 `--url` 和 `--token`。
- 如果缺少执行地址或 token，立即停止并向用户索取，不要继续猜测或尝试 KB 命令。
- 多行命令、复杂 HTML 或 patch 优先走 `--command-file`，避免 shell 转义破坏命令正文。

## 默认工作流

0. 先打开[references/read.md](./references/read.md)了解阅读、搜索相关能力。
1. 先定位范围：用 `kb ls`、`kb tree` 或 `kb search`。
2. 锁定唯一对象后，优先使用稳定 `code`。
3. 任何修改前，先执行 `kb cat` 读取当前内容，后按需阅读修改或写入文档。
4. 选择满足需求的最小操作，不要默认整篇重写。
5. 如果最终答复需要 KB 链接，最后再执行 `kb render`。

## 全局规则


- 仓库、目录、文档都可能同名；不唯一时先消歧，不要猜。
- 后续分析和修改以 `kb cat` 返回内容为准。
- `kb write` 或 `kb edit --patch` 写入的正文优先是 HTML，不是 Markdown 正文。
- 只有在明确不存在目标文档时才新建。
- 修改已有文档时优先局部变更。
- 删除、移动、发布属于高风险操作，只有用户明确要求时才执行。
- 处理 `.pdf`、`.xlsx`、`.docx` 等不可直接编辑格式时，默认先读取内容再创建语义等价的 `.md` 文档，除非工具明确支持原格式编辑。


## 按需加载的参考资料

- 读取、搜索、定位和渲染链接：看 [references/read.md](./references/read.md)
- 新建文档、目录、移动、删除、发布：看 [references/write.md](./references/write.md)
- 对已有文档做 patch 精确修改：看 [references/update.md](./references/update.md)
- 文件上传、下载：看 [references/file-transfer.md](./references/file-transfer.md)
