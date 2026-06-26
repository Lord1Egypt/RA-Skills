# 飞书消息发送技能

## 描述

通过飞书渠道发送文本、图片、文件消息的技能。

## 配置

- **渠道**: `feishu`
- **用户 ID**: 在 `~/.openclaw/workspace/TOOLS.md` 中配置

## 使用方法

### 方式一：自然语言指令（推荐）

直接告诉 AI 要发送什么，AI 会自动处理：

```
请给我飞书发送消息：你好！
```

### 方式二：使用 message_tool 格式

```
message_tool:send:feishu:[用户 ID]:消息内容
```

示例：
```
message_tool:send:feishu:ou_a05417a566dc000ad40fed2beb9fe057:你好
```

### 发送图片

#### 本地图片（推荐）

**使用 message_tool**
```
message_tool:send:feishu:[用户 ID]:图片说明
media: ~/.openclaw/workspace/image.jpg
```

**自然语言**
```
请用飞书发送图片到 [用户 ID]
路径：~/.openclaw/workspace/image.jpg
文字：图片说明
```

#### 网络图片

**先下载到本地，再发送**
```bash
# 1. 下载网络图片到工作区
curl -sL "https://example.com/image.jpg" -o ~/.openclaw/workspace/image.jpg

# 2. 发送
message_tool:send:feishu:[用户 ID]:图片说明
media: ~/.openclaw/workspace/image.jpg
```

**注意**：飞书不支持直接发送网络图片 URL，必须先下载到本地工作区。

### 发送文件

```
请用飞书发送文件到 [用户 ID]，
路径：~/.openclaw/workspace/file.md，文字：文件说明
```

## 注意事项

1. 所有文件必须在 `~/.openclaw/workspace/` 目录下
2. 使用绝对路径引用文件
3. 图片支持 jpg/png/gif 格式
4. 文件支持 md/pdf/doc 等常见格式
5. **不要使用 isolated session**（有编译问题），使用 main session 发送
