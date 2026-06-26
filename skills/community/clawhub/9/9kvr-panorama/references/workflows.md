# 标准操作流程（How）

## 执行前检查（所有流程共用）

1. 运行 `vr config --show`，确认 token 和 uid 已设置。
2. 运行 `vr info version`，确认服务在线。
3. 对目标对象做一次读取：作品用 `works info`，素材用 `media info`，场景用 `scenes info`。
4. 若操作涉及删除/覆盖/批量修改，先明确记录目标 ID 清单。

## 流程 0：配置登录信息（uid/token）

### 目标

将用户提供的 `uid` 与 `token` 写入本地登录态，保证后续 API 可用。

### 步骤

1. 优先使用 MCP 工具配置：
   - 调用 `config_account(uid, token)`
2. 或使用 CLI 配置：

```bash
vr config --uid <UID>
vr config --token <TOKEN>
```

3. 验证配置：

```bash
vr config --show
vr info version
```

### 验收标准

- `vr config --show` 显示 UID 已设置，Token 非“未设置”
- `vr info version` 可正常返回（说明鉴权/网络可用）

## 流程 A：从 0 到 1 创建作品

### 目标

将本地素材上传并生成一个可继续编辑的作品。

### 步骤

1. 上传素材

```bash
vr media upload ./assets/lobby.jpg --name "大厅场景" --description "入口视角"
```

2. 获取 `media_id`

```bash
vr media list --keyword "大厅场景"
```

3. 创建作品

```bash
vr works create 1201 --name "样板展厅" --description "基础版本"
```

4. 验证作品创建结果

```bash
vr works list --keyword "样板展厅"
vr works info 9001
```

### 验收标准

- 能在 `works list` 中检索到新作品
- `works info` 返回名称、描述与预期一致

## 流程 B：更新作品并验证

### 目标

修改作品文案或封面，确保修改可见且无副作用。

### 步骤

1. 读取原始数据（留存对比）

```bash
vr works info 9001
```

2. 执行更新

```bash
vr works update 9001 --name "样板展厅-春季" --description "2026 春季活动" --cover 1208
```

3. 复核结果

```bash
vr works info 9001
```

### 验收标准

- 更新字段值正确
- 未更新字段保持原值

## 流程 C：配置场景热点跳转

### 目标

实现用户在场景间跳转。

### 步骤

1. 查看作品场景

```bash
vr works scenes 9001
```

2. 添加跳转热点

```bash
vr hotspot add-jump 9001 3001 3002 --name "进入展区B" --ath 8 --atv -2
```

3. 验证热点是否生效

```bash
vr hotspot list 9001
```

4. 异常回滚（可选）

```bash
vr hotspot delete 9001 7001
```

### 验收标准

- 热点列表可见新增记录
- 位置参数（`ath`/`atv`）和名称符合预期

## 流程 D：配置音乐与语音

### 目标

给作品补齐背景音乐和语音解说。

### 步骤（音乐）

1. 智能匹配

```bash
vr music match 9001
```

2. 不满意时人工搜索

```bash
vr music search --keyword "科技感" --limit 10 --page 1
```

3. 添加音乐

```bash
vr music add 9001 https://cdn.example.com/bgm.mp3 --loop 1 --volume 80
```

### 步骤（语音）

1. 选择主播

```bash
vr voice anchors --gender female
```

2. 发起生成

```bash
vr voice generate "欢迎来到产品体验区" female_01
```

3. 查询任务直到成功

```bash
vr voice query task_xxx
```

4. 挂载语音

```bash
vr voice add 9001 https://cdn.example.com/voice.mp3 --loop 1 --volume 90
```

### 验收标准

- 音乐、语音均已绑定到目标作品
- 音量与循环策略符合预期

## 流程 E：输出接入代码

### 目标

为业务方提供可直接集成的接入片段。

### 步骤

1. 选择渠道与框架

- 小程序：`wechat/toutiao/kuaishou`
- Web：`vue/react/vanilla`
- 存量系统：`website/app/cms`

2. 获取指南

```bash
vr develop web --framework react
```

3. 生成代码

```bash
vr develop code embed --framework react --work-id 9001
```

4. 提交前校验

- work_id 是否正确
- 输出代码是否包含目标环境所需参数

## 通用执行策略

1. 先查后改：`list/info` 永远优先于 `create/update/delete`。
2. 改后复查：每次写入后必须追加一次读取验证。
3. 小步提交：复杂任务分阶段执行，不要一次性做多类写入。
4. 风险隔离：删除和批量操作尽量单独执行并留日志。
