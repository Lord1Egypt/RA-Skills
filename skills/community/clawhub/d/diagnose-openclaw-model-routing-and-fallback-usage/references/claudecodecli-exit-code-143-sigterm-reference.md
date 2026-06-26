# ClaudeCodeCLI 退出码 143 / SIGTERM 参考

## 含义
在类 Unix 环境中，进程若被 `SIGTERM` 终止，shell 常见退出码会表现为：

- `143 = 128 + 15`
- 其中 `15` 对应信号：`SIGTERM`

因此当协作任务里看到：

- `code 143`
- `Exec failed`
- 中途被杀
- 无完整 stdout/stderr

应优先按“**进程被外部终止**”处理，而不是先假定为模型 API 本身报错。

---

## 在 OpenClaw / ClaudeCodeCLI 协作场景中的常见指向
`143` 更常表示 ClaudeCodeCLI 进程还没自然跑完，就被外层环境结束，常见来源包括：

1. **宿主侧超时控制**
   - 调度器、wrapper、守护脚本设置了最大执行时长
   - 到时后先发 `SIGTERM`

2. **人工或上游任务取消**
   - 用户取消
   - 上游 agent/worker 重试或中断时主动回收子进程

3. **容器 / systemd / supervisor 回收**
   - 服务重启
   - 容器终止
   - systemd stop/restart

4. **资源压力导致的级联中止**
   - 有时不是直接 OOM kill（那更像 137 / SIGKILL）
   - 但资源紧张时上层管理器可能先选择优雅终止子进程

5. **多层包装命令中的父进程退出**
   - 父 shell/wrapper 先结束，子进程收到终止信号

---

## 它不直接说明什么
看到 `143` 时，**不能直接推出**：

- Claude 模型不可用
- prompt 有问题
- OpenClaw fallback 一定发生过
- CLI 自己逻辑崩溃

`143` 只能先说明：

> 这次 CLI 执行没有正常自然结束，而是被外部终止。

---

## 与其他常见退出码的区分

| 退出码 | 常见含义 | 解释 |
|---|---|---|
| 143 | `SIGTERM` | 被请求终止，通常是超时/取消/服务回收 |
| 137 | `SIGKILL` | 常见于 OOM 或被强杀 |
| 130 | `SIGINT` | 常见于 Ctrl+C / 中断 |
| 非信号码普通非零 | 程序内部错误 | CLI 主动返回失败码 |

---

## 排查顺序建议

### 1. 先查是否有外层超时
重点看：

- OpenClaw worker / runner 的超时设置
- systemd `TimeoutStopSec=`、`RuntimeMaxSec=`
- 容器编排平台的 job timeout
- wrapper 脚本里的 `timeout` 命令

可搜索：

```bash
rg -n "timeout|RuntimeMaxSec|TimeoutStopSec|SIGTERM|143" /etc/systemd /opt /srv ~/.* 2>/dev/null
```

### 2. 查父进程或 supervisor 日志
如果 CLI 自己只留下 `code 143`，真正原因常在父进程日志里：

- OpenClaw 主进程日志
- systemd journal
- 容器日志
- 任务调度日志

例如：

```bash
journalctl -u <service-name> --since "30 min ago"
```

### 3. 核对是否发生“先 TERM 后 KILL”
有些系统会先 `SIGTERM`，等待一段时间后再 `SIGKILL`。
如果只抓到前段日志，可能只看到 143。

### 4. 判断是否真的拿到过 CLI 输出
若无 stdout/stderr：

- 可能 CLI 还没来得及输出
- 也可能输出被 wrapper 吃掉
- 也可能缓冲区未 flush 就被终止

因此“无输出”不等于“CLI 什么都没做”。

---

## 在协作任务中的处理建议
当 OpenClaw 调起 ClaudeCodeCLI 出现 `143` 时，较稳妥的处理方式是：

1. **不要把它当作已完成结果交付**
2. **明确标注本轮执行中断**
3. **优先补救重跑**
4. **重跑时避免复用会再次被杀的同一执行方式**
5. **拿到新一轮完整输出后再汇总结果**

---

## 规避建议

### 调大或取消外层超时
如果任务天然较长，需提高 runner / supervisor 超时。

### 减少单次上下文体积
超长 prompt、超大仓库扫描、过多附件都会增加 CLI 执行时间，提升被超时终止概率。

### 保留原始 stdout/stderr
若当前包装层没完整落盘，建议把子进程输出重定向保存，便于区分：

- 模型请求失败
- CLI 内部失败
- 外层终止

### 为重试加入幂等与断点语义
避免第一次被终止后，第二次重跑产生重复副作用。

---

## 一句话判断模板
当日志里只有 `Exec failed` + `code 143` 时，可以先用这句判断：

> 该次 ClaudeCodeCLI 不是正常执行完成，而是被外部以 `SIGTERM` 终止；需继续追查上层超时、取消或进程回收原因，不能把这次结果当成有效完成产物。