---
name: feishu-send-file
description: 通过飞书机器人稳定发送本地普通文件或本地图片。用于现有一等工具无法直接完成“发送本地文件附件”时，或本地图片经常规消息链路发送后在飞书里只显示路径文本而不显示图片本体时。普通文件走 `im/v1/files -> file_key -> msg_type=file`，图片走 `im/v1/images -> image_key -> msg_type=image`。
---

# 飞书发送文件

使用这个 skill 发送**本地普通文件**，或补救“**本地图片被错误发成路径文本**”的场景。

优先使用平台已有的一等飞书工具。只有在以下情况出现时，再使用本 skill：
- 需要以机器人身份发送本地普通文件附件
- 现有工具只能把本地路径当作文本发出去
- 本地图片走常规消息链路后，飞书里显示的是路径文本而不是图片本体

## 工作方式

### 普通文件

飞书普通文件消息需要两步：
1. 上传文件到 `im/v1/files`
2. 使用返回的 `file_key` 发送 `msg_type=file`

### 图片

飞书图片消息也需要两步：
1. 上传图片到 `im/v1/images`
2. 使用返回的 `image_key` 发送 `msg_type=image`

不要混用这两条链路。

## 何时切换到本 skill

如果本地图片通过常规消息路径发送后，用户在飞书里看到的是：
- 本地绝对路径，例如 `/path/to/demo.png`
- 带附件图标的路径文本
- 任何不是图片本体的回显

就视为这次发送失败，不要继续重试同一种方式，直接改用 `scripts/send_image.py`。

**成功标准只有一个：用户在飞书里实际看到文件附件或图片本体。**

## 脚本

### 发送普通文件

```bash
python3 scripts/send_file.py <file_path> <receive_id_type> <receive_id> <app_id> <app_secret> [file_name] [domain]
```

参数：
- `file_path`: 本地文件路径
- `receive_id_type`: `open_id` 或 `chat_id`
- `receive_id`: 接收者 ID
- `app_id`: 飞书或 Lark 应用 ID
- `app_secret`: 飞书或 Lark 应用密钥
- `file_name`: 可选，自定义显示文件名
- `domain`: 可选，`feishu` 或 `lark`，默认 `feishu`

示例：

```bash
python3 scripts/send_file.py /path/to/report.html open_id ou_xxx cli_xxx secret_xxx
python3 scripts/send_file.py /path/to/archive.zip chat_id oc_xxx cli_xxx secret_xxx backup.zip
python3 scripts/send_file.py /path/to/report.pdf open_id ou_xxx cli_xxx secret_xxx report.pdf lark
```

### 稳定发送图片

```bash
python3 scripts/send_image.py <image_path> <receive_id_type> <receive_id> <app_id> <app_secret> [domain]
```

参数：
- `image_path`: 本地图片路径
- `receive_id_type`: `open_id` 或 `chat_id`
- `receive_id`: 接收者 ID
- `app_id`: 飞书或 Lark 应用 ID
- `app_secret`: 飞书或 Lark 应用密钥
- `domain`: 可选，`feishu` 或 `lark`，默认 `feishu`

示例：

```bash
python3 scripts/send_image.py /path/to/demo.png open_id ou_xxx cli_xxx secret_xxx
python3 scripts/send_image.py /path/to/demo.png chat_id oc_xxx cli_xxx secret_xxx lark
```

## 获取参数

- `app_id` / `app_secret` 来自当前飞书或 Lark 应用配置
- `receive_id_type` 取决于目标是私聊还是群聊
- `receive_id` 需要从当前消息上下文、用户映射、会话元数据或上游系统明确取得
- 如果上游上下文给的是 `user:ou_xxx` 之类的复合格式，先提取真正的 ID 再传给脚本

不要把某个环境里的固定路径、固定配置文件位置、固定 inbound 字段格式写死为通用规则。

## 手动 API 流程

### 普通文件

1. 获取 tenant access token
2. 调用 `im/v1/files` 上传文件
3. 使用返回的 `file_key` 发送 `msg_type=file`

### 图片

1. 获取 tenant access token
2. 调用 `im/v1/images` 上传图片
3. 使用返回的 `image_key` 发送 `msg_type=image`

## 注意事项

- 普通文件和图片必须走各自独立的上传接口
- 如果常规消息链路返回了 `message_id`，也不能直接判定成功，仍要看飞书客户端最终显示结果
- 本 skill 面向“本地文件发送”这一缺口，不替代平台现有的一等飞书工具
- 需要群发或群聊发送时，使用 `chat_id`
- 需要国际版 Lark 时，将最后一个参数设为 `lark`
