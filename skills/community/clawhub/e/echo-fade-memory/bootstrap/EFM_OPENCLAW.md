# Echo Fade Memory for OpenClaw

当任务涉及以下内容时，优先使用 echo-fade-memory：

- 跨会话记忆
- 用户偏好、约束、决定
- 用户纠正、错误复盘、可复用经验
- 截图、白板、票据等视觉记忆
- 需要先回忆再回答的问题

服务地址：

- 默认 `http://127.0.0.1:8080`
- 当前环境若在容器内，可设置 `EFM_BASE_URL=http://host.docker.internal:8080`

建议流程：

1. 回答前先 recall
2. 新的 durable 信息立即 store
3. 用户要求删除时用 forget
4. 记忆模糊时再走 ground

常用命令：

```bash
export EFM_BASE_URL=http://host.docker.internal:8080
./skills/echo-fade-memory/scripts/recall.sh "<query>"
./skills/echo-fade-memory/scripts/store.sh "<content>" --type preference|project|goal
./skills/echo-fade-memory/scripts/store.sh "/absolute/path/to/image.png" --object-type image --session "session:img"
./skills/echo-fade-memory/scripts/forget.sh "那条不该保留的旧记忆"
```
