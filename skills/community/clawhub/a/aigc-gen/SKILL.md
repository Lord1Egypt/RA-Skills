---
name: aigc-gen
description: AIGC 内容生成助手，支持图片生成（文生图）。当用户想要生成图片、AI 绘画、创作内容时自动触发。支持负面提示词、图片比例、批量生成等参数。
---

# AIGC Generator

文生图生成技能。

## 触发场景

当用户要求生成图片时自动触发，例如：
- "生成一张图片..."
- "画一张..."
- "帮我生成..."
- "创作图片"
- "AI 绘画"

## 响应流程

### 第一步：立刻回复用户（毫秒级）

**收到请求后必须立刻回复**，不等图片生成完成。

回复示例（随机选一种）：
- "收到！我来帮你生成【xxx】，稍等片刻，马上就好~ 🎨"
- "好嘞！开始创作【xxx】，请耐心等待，完成后第一时间发给你 ✨"

### 第二步：启动独立 session 执行生成

使用 `sessions_spawn` 启动 **isolated session**：

```
runtime: "isolated"
sessionTarget: "isolated"
payload.kind: "agentTurn"
message: 请帮我生成图片并发送到飞书...
```

#### 子 session 执行内容

1. **构造并运行 generate.py 命令**（使用 `exec`，同步等待，超时 300 秒）：

   ```bash
   python3 C:/Users/79112/.openclaw/workspace/skills/aigc-gen/scripts/generate.py "用户原始 prompt" --ratio 比例数字 --batch 数量
   ```

   > 如果用户指定了比例（如"帮我生成16:9的图片"），从对话中提取正确的数字：
   > - 1=1:1, 2=3:4, 3=4:3, 4=9:16, 5=16:9

2. **等待命令完成**，在输出中查找 `__RESULT_JSON__{...}__`，解析 JSON 获取 `local_paths`（本地图片路径列表）。

3. **发送图片到飞书**：对每个本地图片路径，调用 `feishu_doc(action=upload_image, file_path=图片路径)`。

4. **完成**：直接结束子 session 即可（OpenClaw 会自动通知主 session）。

## 配置说明

### 获取 API Key

1. 访问注册页面：
   - 英文版：https://tczlld.com/aistudio/en/
   - 中文版：https://tczlld.com/aistudio/zh/
2. 注册并登录，在后台创建 API Key（格式：`accessKeyId.secret`）
3. 配置环境变量 `AIGC_API_KEY`

### 环境变量

| 环境变量 | 必填 | 默认值 | 说明 |
|---------|------|--------|------|
| `AIGC_API_KEY` | ✅ | — | API Key（accessKeyId.secret 格式） |
| `AIGC_BASE_URL` | 否 | `https://tczlld.com/aistudio/api` | API 前缀 |
| `AIGC_CLIENT_ID` | 否 | `openclaw-default` | 客户端标识 |
| `AIGC_PROVIDER` | 否 | `4` | Provider ID |
| `AIGC_TIMEOUT` | 否 | `120` | 任务超时秒数 |

## 参数说明

| 参数 | 说明 |
|------|------|
| `--ratio` | 宽高比：1=1:1, 2=3:4, 3=4:3, 4=9:16, 5=16:9 |
| `--batch` | 生成数量（1-4） |
| `--negative` | 负面提示词 |
| `--timeout` | 超时秒数 |

## 状态码

| status | 含义 |
|--------|------|
| 0 | 排队中 |
| 1 | 生成中 |
| 2 | 成功 |
| <0 | 失败 |
