# bozo-jiaodu API 调用脚本

本目录包含用于调用 BizyAir 图片角度调整 API 的 Shell 脚本。

## 环境要求

### 必需环境变量

```bash
export BIZYAIR_API_KEY="your_actual_api_key_here"
```

### 系统要求

- Bash Shell
- curl (用于 HTTP 请求)
- jq (可选，用于 JSON 解析)

## 脚本说明

### create_angle_task.sh

创建摄像机角度调整任务。

**用法**：
```bash
bash scripts/create_angle_task.sh <图片URL> <摄像机提示词> [web_app_id]
```

**参数**：
| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| 图片URL | 要调整角度的原始图片URL | 是 | - |
| 摄像机提示词 | 以 `<sks>` 开头的96个标准摄像机位置提示词之一 | 是 | - |
| web_app_id | BizyAir 工作流ID | 否 | 43531 |

**示例**：
```bash
# 基础用法
bash scripts/create_angle_task.sh \
  "https://example.com/image.png" \
  "<sks> left side view low-angle shot close-up"

# 指定 web_app_id
bash scripts/create_angle_task.sh \
  "https://example.com/image.png" \
  "<sks> front view eye-level shot medium shot" \
  43531
```

### get_task_outputs.sh

查询任务状态并获取生成的图片。

**用法**：
```bash
bash scripts/get_task_outputs.sh <requestId> [轮询间隔]
```

**参数**：
| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| requestId | 任务 ID（创建任务时返回的） | 是 | - |
| 轮询间隔 | 查询间隔秒数 | 否 | 5 |

**示例**：
```bash
# 使用默认轮询间隔（5秒）
bash scripts/get_task_outputs.sh ca339473-aec3-469d-8ee6-a6657c38cd1c

# 自定义轮询间隔（10秒）
bash scripts/get_task_outputs.sh ca339473-aec3-469d-8ee6-a6657c38cd1c 10
```

## 完整工作流程示例

### 步骤 1: 创建任务

```bash
bash scripts/create_angle_task.sh \
  "https://storage.bizyair.cn/inputs/20260108/JYLqRJcgPJ1GcOrzRfXJ8qsXnia1aWSB.png" \
  "<sks> back-right quarter view high-angle shot medium shot"
```

**输出**：
```
📤 正在创建摄像机角度调整任务...
📷 图片 URL: https://storage.bizyair.cn/inputs/20260108/...
🎬 摄像机提示词: <sks> back-right quarter view high-angle shot medium shot

✅ 任务创建成功！

🔖 任务 ID: ca339473-aec3-469d-8ee6-a6657c38cd1c

⏳ 图片正在后台处理中...
💡 使用以下命令查询结果:
   bash scripts/get_task_outputs.sh ca339473-aec3-469d-8ee6-a6657c38cd1c
```

### 步骤 2: 查询结果

```bash
bash scripts/get_task_outputs.sh ca339473-aec3-469d-8ee6-a6657c38cd1c
```

**输出**：
```
🔍 查询任务结果...
🔖 任务 ID: ca339473-aec3-469d-8ee6-a6657c38cd1c
⏱️ 轮询间隔: 5 秒

⏳ 任务进行中... (Processing)
💡 等待 5 秒后重新查询...

✅ 任务完成！

📊 任务详情:

### 🎨 摄像机角度调整结果

> 🔖 任务 ID: `ca339473-aec3-469d-8ee6-a6657c38cd1c`
> ⏱️ 生成耗时: ~12.5 秒
> 🔄 共 1 张图片

| 序号 | 预览 | 图片 URL |
| --- | --- | --- |
| 1 | ![图片1](https://storage.bizyair.cn/outputs/xxx.png) | https://storage.bizyair.cn/outputs/xxx.png |

> 📥 如需下载图片，请提供保存路径
```

## 96个摄像机位置提示词参考

脚本会验证输入的摄像机提示词格式，必须以 `<sks>` 开头。完整的96个标准提示词请参考 `../SKILL.md` 或 `../evals/evals.json`。

## 错误处理

### 环境变量未设置
```
❌ 错误: 环境变量 BIZYAIR_API_KEY 未设置
💡 请设置环境变量: export BIZYAIR_API_KEY="your_api_key_here"
```

### 提示词格式错误
```
❌ 错误: 摄像机提示词必须以 <sks> 开头
💡 正确格式示例: <sks> left side view low-angle shot close-up
```

### 任务创建失败
```
❌ 任务创建失败
API 响应: {...}

💡 可能原因:
  • BIZYAIR_API_KEY 无效或已过期
  • 网络连接不稳定
  • 图片 URL 无法访问
  • 请求参数格式错误
```

### 任务执行失败
```
❌ 任务执行失败

🔖 任务 ID: xxx
API 响应: {...}

💡 建议:
  • 检查摄像机提示词格式是否正确
  • 确认原始图片 URL 可访问
  • 稍后使用相同参数重试
```
