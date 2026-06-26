# 端到端示例（How + 完整示例）

## 目录

1. 配置登录信息（uid/token）
2. 新建作品并配置热点
3. 语音生成并挂载
4. 音乐搜索并挂载
5. 接入代码生成
6. 安全删除场景

## 示例 0：配置登录信息（uid/token）

### 场景说明

用户给出 uid 和 token，要求你立即帮他完成登录配置。

### 操作命令

```bash
vr config --uid <UID>
vr config --token <TOKEN>
vr config --show
vr info version
```

### 结果检查

- UID 已显示为设置状态
- Token 不为“未设置”（应显示脱敏）
- 版本查询正常返回

## 示例 1：新建作品并配置热点（新手最常用）

### 场景说明

你有一张本地全景图，需要快速做出一个可交互作品。

### 操作命令

```bash
# 1) 上传素材
vr media upload ./assets/lobby.jpg --name "大厅场景" --description "入口主视角"

# 2) 查询素材，记录 media_id（假设 1201）
vr media list --keyword "大厅场景"

# 3) 创建作品
vr works create 1201 --name "样板展厅" --description "用于客户演示"

# 4) 查询作品，记录 work_id（假设 9001）
vr works list --keyword "样板展厅"
vr works info 9001

# 5) 查询场景，记录 scene_id（假设 3001）
vr works scenes 9001

# 6) 添加文本热点
vr hotspot add-text 9001 3001 "欢迎来到展厅" --ath 12 --atv -5

# 7) 验证热点列表
vr hotspot list 9001
```

### 结果检查

- 作品存在且名称正确
- 场景中出现新文本热点

## 示例 2：语音生成并挂载

### 场景说明

你希望自动生成讲解语音并挂到现有作品。

### 操作命令

```bash
# 1) 查看主播
vr voice anchors --gender female

# 2) 生成语音（anchor_key 示例 female_01）
vr voice generate "欢迎来到我们的线上展厅" female_01 --source CLI

# 3) 轮询任务（task_id 示例 task_xxx）
vr voice query task_xxx

# 4) 挂载语音（voice_url 取 query 返回值）
vr voice add 9001 https://cdn.example.com/voice.mp3 --loop 1 --volume 90
```

### 结果检查

- `voice query` 返回可用语音地址
- 挂载后播放逻辑符合循环与音量配置

## 示例 3：音乐搜索并挂载

### 场景说明

智能匹配效果不理想，需要手工选择更贴合的背景音乐。

### 操作命令

```bash
# 1) 查标签
vr music tags

# 2) 按关键词与标签搜索
vr music search --keyword "科技感" --tag 2 --limit 10 --page 1

# 3) 挂载目标音乐
vr music add 9001 https://cdn.example.com/bgm-tech.mp3 --loop 1 --volume 80
```

### 结果检查

- 音乐可播放
- 音量与场景语音不冲突

## 示例 4：输出 React 接入代码

### 场景说明

前端团队需要把作品嵌入 React 项目。

### 操作命令

```bash
# 1) 获取 Web 接入指南
vr develop web --framework react

# 2) 生成接入代码
vr develop code embed --framework react --work-id 9001
```

### 结果检查

- 代码中包含目标 `work-id`
- 与现有 React 项目构建链兼容

## 示例 5：安全删除场景

### 场景说明

需要移除废弃场景，避免误删。

### 操作命令

```bash
# 1) 先查场景
vr scenes list --keyword "旧场景"
vr scenes info 3009

# 2) 删除场景
vr scenes delete 3009

# 3) 复查
vr scenes info 3009
```

### 结果检查

- 目标场景不再可读
- 相关热点链路已评估并处理

## 示例使用建议

1. 第一次使用时先跑“示例 1”。
2. 需要语音讲解时直接套“示例 2”。
3. 需要前端接入时直接套“示例 4”。
4. 任何删除动作都先按“示例 5”的顺序执行。
