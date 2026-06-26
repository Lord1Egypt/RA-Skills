---
name: qianfan-chat
description: "千帆AI应用对话接口调用技能。用于调用百度千帆平台的对话API进行AI对话交互。支持流式和非流式响应、Function Call工具调用、文件上传等功能。触发场景：(1) 用户需要调用千帆对话API；(2) 用户提到\"千帆\"、\"qianfan\"、\"百度AI对话\"；(3) 需要与千帆应用进行对话交互。"
homepage: https://cloud.baidu.com/doc/qianfan-api/s/7m7wqq361
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      env:
        - QIANFAN_API_KEY
      bins:
        - python3
---

# 千帆对话技能

调用百度千帆平台的对话API，与千帆AI应用进行对话交互。

## 初始化配置

**⚠️ 必须设置环境变量 `QIANFAN_API_KEY`：**

```bash
export QIANFAN_API_KEY="your-api-key-here"
```

API Key 可从 [千帆平台](https://cloud.baidu.com/product/wenxinworkshop) 获取。

## 默认配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `app_id` | `e52a2419-4327-48e8-b9dc-9bf037199fc2` | 应用ID，可在调用时通过 `--app-id` 覆盖 |
| `stream` | `false` | 流式返回 |

---

## 接口详情

详细的请求/响应参数、错误码、curl 示例等，请参阅 [API 参考文档](references/api.md)。

---

## 基本用法

### 发起对话

使用 `scripts/chat.py` 脚本调用：

```bash
python3 scripts/chat.py --query "你好，请介绍一下自己"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--query` | 用户提问内容（必选） | - |
| `--app-id` | 应用ID | e52a2419-4327-48e8-b9dc-9bf037199fc2 |
| `--stream` | 是否流式返回 | true |
| `--conversation-id` | 会话ID（多轮对话时传入） | - |
| `--file-ids` | 文件ID列表，逗号分隔 | - |

### 多轮对话

**会话状态自动管理：**
- 首次调用不传 `conversation_id`，API返回后会自动保存
- 后续调用自动使用已保存的 `conversation_id`
- 使用 `--new-session` 开始新会话

```bash
# 首次对话（自动保存 conversation_id）
python3 scripts/chat.py --query "你好"
# 输出: [conversation_id: xxx-xxx-xxx]

# 后续对话（自动使用已保存的 conversation_id）
python3 scripts/chat.py --query "刚才我们聊了什么"
# 输出: [使用已保存的会话: xxx-xxx-xxx]

# 开始新会话
python3 scripts/chat.py --query "新话题" --new-session
```

**手动指定会话ID：**

```bash
python3 scripts/chat.py --query "继续" --conversation-id "xxx-xxx-xxx"
```

### 非流式响应

```bash
python3 scripts/chat.py --query "你好" --stream false
```

## 高级功能

### Function Call

定义工具并上报结果：

```bash
python3 scripts/chat.py --query "今天北京天气" --tools-file tools/weather.json
```

## 注意事项

1. 确保 `QIANFAN_API_KEY` 环境变量已设置
2. 首次对话不需要 `conversation_id`，后续多轮对话需传入
3. 流式模式下，响应以 `data: ` 开头，以 `data: [DONE]` 结束
