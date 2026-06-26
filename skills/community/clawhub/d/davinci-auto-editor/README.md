# DaVinci Auto Editor

`davinci-auto-editor` 现在是本地纯 Node skill：负责扫描素材、调用云端任务服务、下载最小执行计划，并生成 DaVinci Resolve 可导入的 `CMX3600 EDL` 包。

这版不再要求用户本地安装 Python，也不再在本地调用 Python bridge。核心剪辑决策、模板逻辑、API Key 鉴权、配额与任务状态都应该放在云端服务里。

## 安装要求

- Node.js >= 18
- 已安装 DaVinci Resolve
- 能访问你的云端剪辑 API

## 环境依赖

- Windows / macOS / Linux 都可以运行 Node 主入口
- 需要用户能把生成的 `timeline.edl` 导入到 DaVinci Resolve
- 推荐先把素材导入 Resolve Media Pool，再导入 EDL

## API Key 配置方法

1. 复制 `examples/config.example.json` 为真实配置文件。
2. 填入 `api_base_url` 和 `api_key`。
3. 配置 `material_path`、`timeline_fps`、`timeline_resolution`。

## 调用方式

```bash
node scripts/index.js --config ./examples/config.example.json
```

也可以通过包入口调用：

```bash
npx davinci-auto-editor --config ./examples/config.example.json
```

## 运行过程

脚本会依次完成：

1. 读取并校验配置
2. 扫描 `material_path`
3. 调用 `/v1/tasks/create`
4. 调用 `/v1/tasks/{id}/material-index`
5. 调用 `/v1/tasks/{id}/plan`
6. 生成最小本地执行计划 `resolve-import.json`
7. 生成 Resolve 可导入的 `timeline.edl`
8. 生成导入说明 `IMPORT-TO-RESOLVE.txt`
9. 回传 `/v1/tasks/{id}/execute-report`

## 输出内容

默认输出到素材目录旁的 `_davinci_auto_editor/<taskId>/`：

- `resolve-import.json`
- `timeline.edl`
- `IMPORT-TO-RESOLVE.txt`
- `execution-report.json`

## 配置说明

公共配置：

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

达芬奇本地导入配置：

- `render_preset`
- `timeline_fps`
- `timeline_resolution`

可选增强配置：

- `task_name`
- `task_timeout_ms`
- `poll_interval_ms`
- `request_timeout_ms`
- `webhook_url`
- `extra_metadata`

## 常见问题

### 1. 为什么这版不再直接操控 Resolve？

因为面向普通用户交付时，本地要求 Python 不稳定、暴露面也更大。这版改成“云端出计划，本地 Node 生成 EDL”，让本地依赖只剩 Node。

### 2. 核心逻辑是不是还在本地？

不是。当前本地只保存最小导入计划，不保存完整云端推理结果。模板编排和剪辑决策应放在云端服务。

### 3. EDL 导入后如果要求 relink 怎么办？

先把素材导入 Media Pool，再导入 `timeline.edl`；若 Resolve 仍要求定位素材，指向 `material_path` 对应的素材目录即可。

## 限制说明

- 当前输出格式是 `CMX3600 EDL`，适合基础自动拼接，不覆盖复杂转场、Fusion、调色和高级字幕设计。
- 不保证一次导入后 100% 自动匹配所有素材命名规则；复杂项目仍建议人工复核。
- Resolve 的高级项目构建仍需要用户在本地手动导入时间线文件。
