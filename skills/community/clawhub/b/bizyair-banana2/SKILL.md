---
name: bizyair-banana2
description: 使用 BizyAir API 和 Nano Banana 2 模型生成图片。支持参考图、表情包生成。按量付费，无需本地 GPU。
---

# BizyAir Banana 2 图像生成

直接调用 BizyAir API，使用 Nano Banana 2 模型生成高质量图片。

## 前置要求

### 1. 注册 BizyAir 账号
- 访问 https://www.bizyair.cn 注册账号

### 2. 获取 API Key
- 登录后进入控制台复制 API Key

### 3. 配置 API Key（二选一）

**方式 A：环境变量**
```bash
export BIZYAIR_API_KEY="your_api_key_here"
```

**方式 B：创建配置文件（推荐）**

在技能目录创建 `.env` 文件：
```bash
# 技能目录/.env
BIZYAIR_API_KEY=your_api_key_here
```

**配置文件位置优先级：**
1. 技能目录下的 `.env`（推荐，通用）
2. `~/.config/bizyair-banana2/.env`
3. `~/.bizyair-banana2/.env`
4. `~/.baoyu-skills/bizyair-banana2/.env`（兼容旧版本）

## 使用方法

### 基础用法 - 文生图

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  --prompt "一只可爱的猫咪" \
  --image cat.png
```

### 使用参考图（图生图）

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  --prompt "近景构图，自信展示自我，姿态酷飒随性" \
  --image output.png \
  --ref input.png
```

### 多张参考图

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  --prompt "图 1 的人穿着图 2 的衣服，在图 3 的场景中" \
  --image output.png \
  --ref person.png \
  --ref clothes.png \
  --ref background.png
```

### 指定宽高比

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  --prompt "全身照" \
  --image fullbody.png \
  --ar 9:16
```

### 表情包生成（Web App 47091）

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  --prompt "搞笑表情" \
  --image emoji.png \
  --ref portrait.jpg \
  --web-app-id 47091
```

## 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-p, --prompt` | 提示词（必需） | - |
| `-i, --image` | 输出图片路径（必需） | - |
| `-r, --ref` | 参考图片路径（可多个） | - |
| `--web-app-id` | Web App ID | 47091 |
| `--ar` | 宽高比：`1:1`, `16:9`, `9:16`, `4:3`, `3:4` | `9:16` |
| `--mode` | 模式：`third-party`, `custom` | `third-party` |
| `--resolution` | 分辨率：`auto`, `1k`, `2k` | `1k` |
| `--timeout` | 超时时间（秒） | 120 |
| `--json` | JSON 格式输出 | - |

## 环境变量

| 变量 | 说明 |
|------|------|
| `BIZYAIR_API_KEY` | BizyAir API Key（必需） |
| `BIZYAIR_BASE_URL` | API 基础 URL（可选） |

## 计费说明

- 按量付费，生成成功才扣费
- 具体价格：https://docs.bizyair.cn/pricing/introduce.html

## API 参考

- 任务提交：`POST /w/v1/webapp/task/openapi/create`
- 状态查询：`GET /w/v1/webapp/task/openapi/detail?requestId={id}`
- 结果获取：`GET /w/v1/webapp/task/openapi/outputs?requestId={id}`
- 文件上传：`GET /x/v1/upload/token`

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `401 Unauthorized` | API Key 无效 | 检查 BIZYAIR_API_KEY 配置 |
| `402 Payment Required` | 余额不足 | 充值：https://www.bizyair.cn |
| `429 Too Many Requests` | 请求限流 | 稍后重试 |
| `500 Internal Error` | 服务端错误 | 检查任务状态，重试 |

## 示例工作流

### 示例 1：生成头像

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  -p "可爱的卡通女孩头像，粉色头发，大眼睛" \
  --image avatar.png \
  --ar 1:1
```

### 示例 2：生成表情包（使用参考图）

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  -p "搞笑表情，九宫格" \
  --image meme.png \
  --ref portrait.jpg \
  --web-app-id 47091
```

### 示例 3：多参考图融合

```bash
python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
  -p "图 1 的人穿着图 2 的衣服，在图 3 的场景中" \
  --image fusion.png \
  --ref person.png \
  --ref clothes.png \
  --ref background.png \
  --ar 9:16
```

### 示例 4：批量生成

```bash
for i in {1..5}; do
  python3 ${SKILL_DIR}/scripts/bizyair_gen.py \
    -p "赛博朋克风格城市夜景" \
    --image cyber_$i.png \
    --ar 16:9
done
```

## 参考资料

- [BizyAir 官网](https://www.bizyair.cn)
- [BizyAir 文档](https://docs.bizyair.cn)
- [API 参考](https://docs.bizyair.cn/api/api-reference.html)
- [工作流广场](https://www.bizyair.cn/workflows)
- [模型广场](https://www.bizyair.cn/models)

## 故障排查

### 1. 检查 API Key
```bash
# 方式 1：检查技能目录的.env
cat /path/to/skills/bizyair-banana2/.env

# 方式 2：检查用户目录配置
cat ~/.config/bizyair-banana2/.env
cat ~/.bizyair-banana2/.env
```

### 2. 运行测试
```bash
cd /home/admin/.openclaw/workspace/skills/bizyair-banana2
bash test.sh
```

### 3. 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `401 Unauthorized` | API Key 无效 | 检查配置 |
| `402 Payment Required` | 余额不足 | 充值 |
| `429 Too Many Requests` | 请求限流 | 稍后重试 |
| 任务超时 | 生成耗时过长 | 增加 `--timeout` |

## 限制

- 图片生成需通过内容审核
- 参考图大小不超过 10MB
- 支持格式：PNG, JPG, WEBP
