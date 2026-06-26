# Canvas Claw 发布说明

## 发布前检查

先确认当前技能目录是干净的，并且本地测试通过：

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw
python3 -m pytest -v
```

## 登录 ClawHub

如果当前机器还没有登录：

```bash
npx clawhub login
```

登录完成后确认身份：

```bash
npx clawhub whoami
```

## 发布命令

首次发布建议显式传 slug、名称和版本：

```bash
npx clawhub publish /Users/apple/bangongziliao/hebing/canvas-claw \
  --slug canvas-claw \
  --name "Canvas Claw" \
  --version 0.1.0 \
  --changelog "Initial public release for AI-video-agent phase-one flows"
```

## 发布建议

- `slug` 使用 `canvas-claw`
- 第一版建议从 `0.1.0` 开始
- 在真正发布前先人工确认 `SKILL.md` 中的描述、环境变量、示例命令是否准确
- 如果后续要声明与 `neo-ai` 的关系，可以在发布时加 `--fork-of neo-ai@1.0.1`

## 当前阻塞

当前这台机器还没有执行 `npx clawhub login`，`npx clawhub whoami` 返回未登录，所以现在还不能直接代你发布。

等你登录后，可以在这个目录继续执行上面的 `npx clawhub publish` 命令。
