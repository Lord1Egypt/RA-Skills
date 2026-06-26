# 命令参考

## 全局参数

```bash
.venv/bin/python3 scripts/skill.py [全局选项] <子命令> [子命令选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --env-file | 指定 env.sh 路径（**强制覆盖**已有环境变量） | 自动查找 |
| --region | LAS/LLM 服务区域 | cn-beijing |
| --api-base | 自定义 API 地址 | 根据区域自动推断 |

## submit - 提交解析任务

```bash
.venv/bin/python3 scripts/skill.py [--env-file /path/to/env.sh] submit --url "{路径或URL}" [选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --url | PDF/图片的路径或 URL（必填） | - |
| --parse-mode | 解析模式：normal / detail | normal |
| --start-page | 起始页码 | 1 |
| --num-pages | 解析页数 | 全部 |
| --tos-bucket | TOS 存储桶（提供则在完成后归档到 TOS） | 环境变量 TOS_BUCKET |
| --tos-prefix | TOS 归档路径前缀 | las_pdf_parse |
| --no-use-llm | 关闭长图 LLM 智能裁剪 | 默认开启 |

**stdout**: 一行 JSON `{"task_id": "...", "eta": "...", "input_type": "...", "tos_bucket": "...(如有)", "source_tos_url": "...(如有)", ...}`
**stderr**: 过程日志（上传进度、裁剪信息等）

## check-and-notify - Agent 工作流（核心）

这是一个专门为 Agent 封装的“全包”后处理管道。**在工作流中必须使用此命令**。

其核心价值在于：
1. **自动下载图片**：将所有解析出的图片下载到本地 `images/` 目录。
2. **重写链接**：自动将 Markdown 正文中的远端 URL 替换为本地相对路径。
3. **打包归档**：可自动将结果（MD + 图片）打包为 ZIP 并上传到 TOS 供用户下载。
4. **内部阻塞轮询**：配合 `--poll`，Agent 仅需一次调用，脚本会自动等待直到出结果。

推荐使用 `--poll` 模式（一次调用完成全部等待）：

```bash
.venv/bin/python3 scripts/skill.py [全局选项] check-and-notify --task-id {id} --output {目录路径} --poll [--tos-bucket {bucket}]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --task-id | 任务 ID（必填） | - |
| --output | 结果保存**目录**（必填），如 `/tmp/las_parse_{task_id}` | - |
| --poll | **推荐**。启用脚本内部 sleep + 重试循环，直到终态 | 关闭 |
| --poll-interval | 轮询间隔秒数 | 30 |
| --tos-bucket | 若提供，将结果打包为 ZIP 上传到此存储桶并返回链接 | - |

| Exit Code | 含义 | stdout JSON 主要字段 |
|-----------|------|---------------------|
| 0 | 成功，结果已保存 | `{status, task_id, output_dir, preview, download_link_markdown, ...}` |
| 1 | 失败 | `{status, error_msg}` |
| 3 | 轮询超时 | `{status, message}` |

---

💡 **异常恢复场景（重要）**：
如果因为对话中断、超时等原因，导致之前提交的任务没有完成本地下载和打包。第二天想恢复时，应该直接使用相同的参数**重新执行一次 `check-and-notify`**。
因为后端会缓存解析结果，重新执行 `check-and-notify` 可以无缝完成之前中断的图片下载、结果落盘和 ZIP 打包流程。

## info - 打印 endpoint 信息（调试用）

```bash
.venv/bin/python3 scripts/skill.py [全局选项] info
```

输出到 stderr（纯文本，非 JSON），仅供人工调试使用。
