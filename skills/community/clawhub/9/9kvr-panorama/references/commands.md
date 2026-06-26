# 命令与参数总览（How）

以下内容按 `src/cli.py` 实现校准，按“先读懂、再执行”的顺序组织。

## 目录

1. 全局命令
2. 作品管理（`vr works`）
3. 素材管理（`vr media`）
4. 场景管理（`vr scenes`）
5. 音乐管理（`vr music`）
6. 语音管理（`vr voice`）
7. 热点管理（`vr hotspot`）
8. 评分管理（`vr score`）
9. 开发接入（`vr develop`）
10. 常见错误与排查

## 1) 全局命令

- 查看版本：`vr --version`
- 查看帮助：`vr --help`
- 查看配置：`vr config --show`
- 设置 token：`vr config --token <token>`
- 设置 uid：`vr config --uid <uid>`

建议首次执行前先完成：

1. `vr config --show` 确认 `Token`、`UID` 已配置
2. `vr info version` 确认服务可访问

## 2) 作品管理（`vr works`）

### `vr works list`

用途：分页查询作品。

示例：

```bash
vr works list --limit 10 --page 1 --keyword "展厅" --pid 0
```

参数：

- `--limit` 每页数量，默认 `3`，最大 `30`
- `--page` 页码，默认 `1`
- `--keyword` 搜索关键词
- `--pid` 目录 ID，默认 `0`

### `vr works info <work_id>`

用途：读取作品详情。

### `vr works scenes <work_id>`

用途：读取作品关联的场景列表（热点配置前必做）。

### `vr works update <work_id>`

用途：更新作品名称、描述、封面。

示例：

```bash
vr works update 9001 --name "春季展厅" --description "2026 春季版本" --cover 1208
```

参数：

- `--name` 作品名称（可选）
- `--description` 作品描述（可选）
- `--cover` 封面素材 ID（可选）

### `vr works create <media_id...> --name <name>`

用途：从一个或多个素材创建作品。

示例：

```bash
vr works create 1201 1202 --name "新品发布厅" --description "双场景"
```

注意：至少要有一个 `media_id`。

## 3) 素材管理（`vr media`）

### `vr media list`

用途：分页查询素材。

```bash
vr media list --limit 12 --page 1 --keyword "大厅"
```

### `vr media info <media_id>`

用途：读取素材详情。

### `vr media update <media_id> --name <name>`

用途：更新素材名称和描述。

### `vr media delete <media_id...>`

用途：删除一个或多个素材。

风险：高。执行前确认素材未被作品引用。

### `vr media upload <file_path>`

用途：上传本地素材文件。

```bash
vr media upload ./assets/lobby.jpg --name "大厅主图" --description "入口全景"
```

常见失败：文件不存在、路径错误、权限不足。

### `vr media download <media_id> [--force]`

用途：获取素材下载链接。

- `--force` 强制获取（按后端策略使用）

## 4) 场景管理（`vr scenes`）

### `vr scenes list`

用途：分页查询场景。

### `vr scenes info <scene_id>`

用途：读取场景详情。

### `vr scenes update <scene_id> --name <name>`

用途：更新场景名称和描述。

### `vr scenes delete <scene_id>`

用途：删除场景。

风险：高。删除后可能影响热点跳转链路。

## 5) 音乐管理（`vr music`）

### `vr music tags`

用途：查询可用音乐标签。

### `vr music search`

用途：按关键词和标签搜索音乐。

```bash
vr music search --keyword "轻快" --tag 2 --limit 12 --page 1
```

### `vr music match <work_id>`

用途：根据作品内容智能匹配背景音乐。

### `vr music add <work_id> <music_url>`

用途：给作品挂载背景音乐。

```bash
vr music add 9001 https://cdn.example.com/bgm.mp3 --loop 1 --volume 80
```

参数：

- `--loop` 是否循环，默认 `1`
- `--volume` 音量，默认 `100`

## 6) 语音管理（`vr voice`）

### `vr voice anchors [--gender male|female]`

用途：获取可用 AI 主播。

### `vr voice generate <text> <anchor_key>`

用途：发起语音生成任务。

```bash
vr voice generate "欢迎来到线上展厅" female_01 --source CLI
```

### `vr voice query <task_id>`

用途：查询语音任务状态与结果 URL。

### `vr voice upload <file_path> [--name voice.mp3]`

用途：上传已有语音文件。

### `vr voice add <work_id> <voice_url>`

用途：将语音挂载到作品。

## 7) 热点管理（`vr hotspot`）

### `vr hotspot list <work_id>`

用途：查询作品热点列表。

### `vr hotspot add-jump <work_id> <from_scene_id> <to_scene_id>`

用途：添加场景跳转热点。

```bash
vr hotspot add-jump 9001 3001 3002 --name "前往二层" --ath 10 --atv -3
```

### `vr hotspot add-text <work_id> <scene_id> <name>`

用途：添加文本热点。

### `vr hotspot delete <work_id> <hotspot_id>`

用途：删除热点。

风险：中高。删除后建议立刻 `vr hotspot list <work_id>` 复核。

## 8) 评分管理（`vr score`）

### `vr score get <work_id>`

用途：查询作品评分。

## 9) 开发接入（`vr develop`）

### `vr develop miniprogram`

用途：获取小程序接入指南。

```bash
vr develop miniprogram --platform wechat --feature basic
```

### `vr develop web`

用途：获取网页接入指南。

```bash
vr develop web --framework react
```

### `vr develop existing`

用途：获取现有项目接入建议。

```bash
vr develop existing --type website
```

### `vr develop code <type>`

用途：生成接入代码片段。

```bash
vr develop code embed --framework react --work-id 9001
```

## 10) 常见错误与排查

1. `错误：文件不存在`
原因：上传路径不对。
处理：使用绝对路径或先 `ls` 校验文件存在。

2. `需要至少一个素材ID`
原因：执行 `vr works create` 未传 `media_id`。
处理：先 `vr media list`，再把目标 ID 放入命令。

3. 删除后数据异常
原因：误删场景/热点/素材。
处理：先停写入操作，复查 `works scenes`、`hotspot list`、`media info`，再按可恢复机制回滚。
