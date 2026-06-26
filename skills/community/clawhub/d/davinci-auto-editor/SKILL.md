---
name: davinci-auto-editor
description: Generate DaVinci Resolve import packages from local media plus a cloud editing API. Use when Codex needs to scan a material folder, request a cloud editing plan, and write a Resolve-importable EDL package with pure Node on the user machine.
metadata: {"openclaw":{"emoji":"🎞️","homepage":"https://github.com/imfengziaaa/video-auto-editor-skills","requires":{"bins":["node"]},"skillKey":"davinci-auto-editor","os":["darwin","linux","win32"]}}
---

# DaVinci Auto Editor

使用这个 skill 时，按下面顺序执行：

1. 读取 `examples/config.example.json` 同结构的配置文件。
2. 校验 `api_base_url`、`api_key`、`material_path`、`timeline_fps` 等关键参数。
3. 递归扫描素材目录，并向云端上报素材索引。
4. 调用云端 API 创建任务并获取剪辑计划。
5. 在本地只生成最小执行计划，不要把完整云端内部逻辑写入本地文件。
6. 由 Node 生成 Resolve 可导入的 `timeline.edl` 和导入说明文件。
7. 将准备结果回传云端。

## 输入参数

至少提供这些字段：

- `api_base_url`
- `api_key`
- `project_type`
- `aspect_ratio`
- `material_path`
- `template_id`
- `subtitle_mode`
- `music_policy`
- `pace_policy`
- `output_mode`
- `render_preset`
- `timeline_fps`
- `timeline_resolution`

可选字段：

- `task_timeout_ms`
- `poll_interval_ms`
- `request_timeout_ms`
- `task_name`
- `webhook_url`
- `extra_metadata`

## 输出结果

默认在素材目录旁创建 `_davinci_auto_editor/<taskId>/`，包含：

- `resolve-import.json`：最小本地导入计划
- `timeline.edl`：Resolve 导入文件
- `IMPORT-TO-RESOLVE.txt`：导入说明
- `execution-report.json`：本地执行报告

## 推荐工作流

- 把核心决策、模板逻辑、API Key 鉴权和配额管理放在云端服务。
- 本地只保留素材扫描、结果导出和回传逻辑。
- 优先使用短路径、稳定命名的素材目录，减少 EDL relink 成本。
- 在正式任务前先用样本素材验证时间线 FPS 和素材命名。

## 依赖要求

- Node.js 18 或更高版本
- 已安装 DaVinci Resolve
- 可访问云端 API 的网络环境

## 错误处理原则

- 缺少配置、素材目录不存在、API 调用失败时立即停止并返回非 0 退出码。
- 始终写出 `execution-report.json` 以便排查。
- 不在本地输出完整云端推理结果，只输出导入所需的最小执行数据。
- 明确提示第一版只覆盖基础拼接和时间线导入准备。
