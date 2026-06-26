# ClawHub Rate Limited Publisher

一个用于**本地排队、定时、限速上传 Skill 到 ClawHub** 的辅助 Skill。

## 为什么你之前那个版本“不能用”

根因不是路径 JSON 本身，而是设计假设错位了：

1. **Skill 只是指导与封装，不会自动获得宿主机执行权限。**  
   OpenClaw 的技能文档说明，技能负责把使用说明注入给模型；真正执行本地命令还取决于运行时工具与命令权限。运行宿主机 shell 命令要么依赖运行时工具（`exec` / `bash` / `process`），要么依赖显式开启的 `/bash` 命令。  
2. **OpenClaw 现在有原生 `cron` 工具，但它只是调度能力，不会替你绕过 shell 权限。**
3. **近期 `clawhub publish` 存在 CLI 兼容问题。**  
   2026-03-09 的公开 issue 显示，CLI v0.7.0 可能因为 `acceptLicenseTerms` 字段未正确发送而直接发布失败。

所以，正确方案不是“让 Skill 自己上传”，而是：

- Skill 提供明确的本地上传流程；
- 本地 Python 脚本负责队列、限速、日志、失败重试边界；
- 真正执行由你的 Mac 上的 Python + clawhub CLI 完成；
- 定时由 `cron` 或 `systemd timer` 负责。

## 目录

- `SKILL.md`：技能入口说明
- `README.md`：使用文档
- `SELF_CHECK.md`：自检结果
- `scripts/clawhub_rate_limited_uploader.py`：主脚本
- `resources/cron.example`：cron 示例
- `resources/systemd.timer.example`：systemd timer 示例
- `examples/queue.sample.json`：队列示例
- `tests/smoke-test.md`：冒烟测试

## 快速使用

### 1）先确认单个 skill 能手动发布

```bash
clawhub whoami
clawhub publish "/Users/yuanchangxing/Downloads/hot-skill-suite-20/workshop-agenda-designer"
```

如果这里报：

```text
acceptLicenseTerms: invalid value
```

那不是这个 Skill 的问题，而是当前 `clawhub` CLI 版本问题。

### 2）创建 queue.json

可直接复制：

```json
{
  "items": [
    {
      "path": "/Users/yuanchangxing/Downloads/hot-skill-suite-20/workshop-agenda-designer"
    }
  ]
}
```

### 3）先 dry-run

```bash
python3 scripts/clawhub_rate_limited_uploader.py   --queue /absolute/path/to/queue.json   --dry-run
```

### 4）确认后执行

```bash
python3 scripts/clawhub_rate_limited_uploader.py   --queue /absolute/path/to/queue.json   --execute
```

## 定时方案

推荐**每 12 分钟执行一次**，脚本内部再做“滚动 1 小时最多 5 次 publish attempt”控制。

这样外层调度和内层限速是双保险。

## 常见问题

### Q1：为什么聊天里不能直接帮我执行？

因为是否允许宿主机执行命令，取决于 OpenClaw 的运行时工具与命令配置，不是单个 Skill 能自行提权解决的。

### Q2：为什么队列里用绝对路径？

因为 OpenClaw / cron / systemd 的工作目录可能不同，绝对路径最稳。

### Q3：失败为什么也算额度？

为了严格遵守平台限制，避免认证失效或参数错误时高频重试。

### Q4：如果 `clawhub publish` 本身坏了怎么办？

先单独跑一次 `clawhub publish`。如果报 license terms 错误，等 CLI 修复后，这个 Skill 的队列和限速逻辑仍可直接继续使用。

## 风险提示

- 第三方 Skill 和本地脚本都应视为可执行代码，先审计再运行。
- 只允许本地受控路径，不要把队列指向未知目录。
- 不要在队列命令里加入远程下载执行链。
