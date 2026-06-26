# message-send

给组织成员发送飞书私信。

## 场景

- 用户说"发给 xxx：..."
- 提醒某人提交日报
- 通知某人某件事

## 操作步骤

### 1. 确定收件人

收件人可以是：
- 姓名（精确匹配）：`--to "黄永强"`
- open_id（直接使用）：`--to ou_xxx`

### 2. 预览（推荐先执行）

```bash
auwomo message send --to "黄永强" --text "请今天下班前补一下日报。" --dry-run
```

dry-run 输出会显示即将执行的命令，但不实际发送。

### 3. 实际发送

```bash
auwomo message send --to "黄永强" --text "请今天下班前补一下日报。"
```

### 4. 确认结果

成功输出（text 模式）：
```
send to=黄永强 open_id=ou_xxx dry_run=false ok=true
message_id=om_xxx
```

JSON 模式：
```bash
auwomo message send --to "黄永强" --text "hello" --format json
```

```json
{
  "ok": true,
  "dry_run": false,
  "recipient": "黄永强",
  "open_id": "ou_xxx",
  "message_id": "om_xxx"
}
```

## 错误处理

| 错误 | 原因 | 解决 |
|------|------|------|
| `cannot resolve recipient "xxx"` | 名字不在 org.yaml 中 | 确认姓名拼写，或用 `auwomo identity list` 查看可用成员 |
| `recipient "xxx" is disabled` | 成员已禁用 | 联系管理员启用该成员 |
| `--to is required` | 未指定收件人 | 必须传 `--to` 参数 |
| `--text is required` | 未指定消息内容 | 必须传 `--text` 参数 |
| lark-cli 错误 | 网络/权限问题 | 检查 lark-cli 配置和网络 |

## 批量发送

当前不支持单次批量发送。需要给多人发相同消息时，逐个调用：

```bash
auwomo message send --to "黄永强" --text "请提交日报"
auwomo message send --to "李明" --text "请提交日报"
```

## 不要这样做

- 不要根据部分姓名猜人
- 不要在收件人不在系统中时直接发送
- 不要绕过 CLI 直接调用 lark-cli
- 不要用 `--as user` 身份发送（CLI 默认 bot 身份）
