# 调用路由（How：先判定调用哪个脚本）

本文件只解决一件事：**用户说了一个需求，应该先调用哪个模块/命令**。

## 0. 总入口规则

1. 先识别任务意图（创建、查询、更新、删除、配置、接入）。
2. 按下方“意图路由表”选择模块脚本（`src/tools/*.py`）和 CLI 组（`vr <group>`）。
3. 先执行读取命令（`list/info/scenes/hotspot list`），再执行写入命令。
4. 写入后必须复查一次读取命令。

## 1. 意图路由表（任务 -> 脚本 -> 命令）

### A. 用户要“创建/查看/更新作品”

- 模块脚本：`src/tools/works.py`
- CLI 分组：`vr works`
- 常用命令：
  - 查列表：`vr works list ...`
  - 看详情：`vr works info <work_id>`
  - 建作品：`vr works create <media_id...> --name ...`
  - 改信息：`vr works update <work_id> ...`
  - 看场景：`vr works scenes <work_id>`

### B. 用户要“上传/管理素材”

- 模块脚本：`src/tools/media.py`
- CLI 分组：`vr media`
- 常用命令：
  - 查列表：`vr media list ...`
  - 看详情：`vr media info <media_id>`
  - 上传：`vr media upload <file_path> ...`
  - 修改：`vr media update <media_id> ...`
  - 删除：`vr media delete <media_id...>`
  - 下载：`vr media download <media_id>`

### C. 用户要“管理场景”

- 模块脚本：`src/tools/scenes.py`
- CLI 分组：`vr scenes`
- 常用命令：
  - 查列表：`vr scenes list ...`
  - 看详情：`vr scenes info <scene_id>`
  - 更新：`vr scenes update <scene_id> ...`
  - 删除：`vr scenes delete <scene_id>`

### D. 用户要“配置热点（跳转/文本）”

- 模块脚本：`src/tools/hotspot.py`
- CLI 分组：`vr hotspot`
- 常用命令：
  - 查热点：`vr hotspot list <work_id>`
  - 加跳转：`vr hotspot add-jump <work_id> <from_scene_id> <to_scene_id> ...`
  - 加文本：`vr hotspot add-text <work_id> <scene_id> <name> ...`
  - 删热点：`vr hotspot delete <work_id> <hotspot_id>`

### E. 用户要“给作品加背景音乐”

- 模块脚本：`src/tools/music.py`
- CLI 分组：`vr music`
- 常用命令：
  - 标签：`vr music tags`
  - 搜索：`vr music search ...`
  - 智能匹配：`vr music match <work_id>`
  - 挂载：`vr music add <work_id> <music_url> ...`

### F. 用户要“生成或挂载语音讲解”

- 模块脚本：`src/tools/voice.py`
- CLI 分组：`vr voice`
- 常用命令：
  - 主播：`vr voice anchors ...`
  - 生成：`vr voice generate <text> <anchor_key> ...`
  - 轮询：`vr voice query <task_id>`
  - 上传：`vr voice upload <file_path> ...`
  - 挂载：`vr voice add <work_id> <voice_url> ...`

### G. 用户要“看评分”

- 模块脚本：`src/tools/score.py`
- CLI 分组：`vr score`
- 常用命令：`vr score get <work_id>`

### H. 用户要“生成接入方案/接入代码”

- 模块脚本：`src/tools/develop.py`
- CLI 分组：`vr develop`
- 常用命令：
  - 小程序：`vr develop miniprogram ...`
  - Web：`vr develop web ...`
  - 存量系统：`vr develop existing ...`
  - 生成代码：`vr develop code <type> ...`

### I. 用户要“版本/上下文/配置诊断/登录配置”

- 模块脚本：`src/tools/info.py`（信息） + `src/config.py`（配置）
- CLI 分组：`vr info` / `vr config`
- 常用命令：
  - `vr info version`
  - `vr info context`
  - `vr config --show`
  - `vr config --uid <UID>`
  - `vr config --token <TOKEN>`
- MCP 工具：
  - `config_account(uid, token)`（推荐用于“帮我配置登录信息”场景）

触发语句示例：

- “请使用 9kvr-panorama 技能帮我配置登录信息，uid 是 xxx，token 是 xxx”
- “帮我登录，uid=xxx token=xxx”

## 2. 路由冲突处理（多意图任务）

当用户一句话里包含多个动作时，按顺序拆解执行：

1. 素材准备（`media`）
2. 作品建立/更新（`works`）
3. 场景与热点（`scenes`/`hotspot`）
4. 音频（`music`/`voice`）
5. 接入导出（`develop`）

## 3. 最小调用模板

- 查询模板：`vr <group> list|info ...`
- 写入模板：`vr <group> create|update|add|delete ...`
- 验证模板：再次调用 `list|info` 进行状态确认

如果不确定归属模块，先用以下问题判定：

- “这是在操作作品本身吗？”-> `works`
- “这是在操作源文件吗？”-> `media`
- “这是在操作场景结构吗？”-> `scenes`
- “这是在操作交互点吗？”-> `hotspot`
- “这是在操作配乐吗？”-> `music`
- “这是在操作语音讲解吗？”-> `voice`
- “这是在看评分数据吗？”-> `score`
- “这是在做嵌入接入吗？”-> `develop`
