# OpenClaw 自然触发接入建议

目标：让 agent 在不需要用户显式说“调用 echo-fade-memory”的情况下，自然使用这套长期记忆。

## 触发条件

出现以下语义时，应优先进入 echo-fade-memory 流程：

- 记忆类指令：记住这个、你记一下、以后按这个来、先别忘了
- 跨会话回忆：上次我们说过什么、之前定的是啥、你还记得吗、我不是说过吗
- 稳定信息写入：用户偏好、长期约束、项目决策、用户纠正、可复用 workaround、feature request
- 视觉记忆：截图、白板、票据、流程图、UI 状态
- 复用记忆回答：需要先回忆上下文再回答的问题

## OpenClaw 内部行为建议

### 回答前

如果问题明显依赖过去信息，先 recall：

```bash
export EFM_BASE_URL=http://host.docker.internal:8080
./skills/echo-fade-memory/scripts/recall.sh "<query>"
```

### 新信息出现时

立即 store，不要等会话结束：

```bash
export EFM_BASE_URL=http://host.docker.internal:8080
./skills/echo-fade-memory/scripts/store.sh \
  "用户偏好极简回答" \
  --summary "偏好：简洁直接" \
  --type preference
```

### 用户发来截图时

```bash
export EFM_BASE_URL=http://host.docker.internal:8080
./skills/echo-fade-memory/scripts/store.sh \
  "/absolute/path/to/screenshot.png" \
  --object-type image \
  --caption "关键截图" \
  --tag screenshot
```

### 用户要求删除时

```bash
export EFM_BASE_URL=http://host.docker.internal:8080
./skills/echo-fade-memory/scripts/forget.sh "那条旧的部署说明"
```

## 推荐的 memory_type 映射

| 场景 | memory_type |
|------|-------------|
| 用户偏好 | preference |
| 项目决定 | project |
| 纠正/经验/报错 workaround | project |
| 未来想做的能力 | goal |
