---
name: chanjing-text-to-digital-person
description: Use Chanjing text-to-digital-person APIs to create AI portrait images, turn them into talking videos, optionally run LoRA training, poll async tasks, and explicitly download generated assets when requested.
---

# Chanjing Text To Digital Person

## L2 Product Skill

本文件是 **L2 产品层**主手册（**Agent 执行真值**）。

- **本文件（`chanjing-text-to-digital-person-SKILL.md`）**：业务逻辑、追问与异常语义；据此调度 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py) 与 [`scripts/`](scripts/) 下脚本。
- **顶层入口** [`../../SKILL.md`](../../SKILL.md)：仅负责路由到本目录，**不**承载本产品执行细则。
- **跨场景约定** [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)；L3 编排层说明见 [`../../orchestration/README.md`](../../orchestration/README.md)。

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 根据人物提示词生成数字人形象图
* 把生成的人物图转成会说话的短视频
* 查询文生图 / 图生视频 / LoRA 任务状态
* 在用户明确要求时，把生成图片或视频下载到本地

如果需求是“上传真人素材训练定制数字人”，优先使用 `chanjing-customised-person`。  
如果需求是“拿已有数字人做口播视频合成”，优先使用 `chanjing-video-compose`。

## Preconditions

凭证由顶层入口统一校验；本 Skill 不重复执行凭证校验步骤。

本 Skill 共用：

* `skills/chanjing-content-creation-skill/.env`（`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`）
* `https://open-api.chanjing.cc`

## Standard Workflow

统一按“每步 = 脚本名 + 输入 + 输出 + 下一步”执行，不做额外追问，由 Agent 自主补齐可选默认值：

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|------|--------|------|------|--------|----------|
| 1 | `create_photo_task.py` | 人物形象参数（年龄/性别/细节等，未指定项走默认） | `photo_unique_id` | Step 2 | `10400` 回顶层鉴权；`40000` 修正参数后重试 Step 1；`50000` 延迟重试 Step 1 |
| 2 | `poll_photo_task.py` | `photo_unique_id` | `photo_path`（远端图片 URL） | Step 3 | 超时/失败：用 `get_photo_task.py` 拉详情；可回 Step 1 重建 |
| 3 | `create_motion_task.py` | `photo_unique_id`、`photo_path`、动作/情绪参数（可选） | `motion_unique_id` | Step 4 | 参数异常回 Step 3 修正；服务异常延迟重试 Step 3 |
| 4 | `poll_motion_task.py` | `motion_unique_id` | `video_url`（远端视频 URL） | Step 5 | 超时/失败：用 `get_motion_task.py` 拉详情；必要时回 Step 3 |
| 5 | `download_result.py`（仅显式下载） | `video_url` 或 `photo_path`、`output_dir`（可选） | 本地文件路径 | 结束 | 下载失败：返回远端 URL 与错误信息 |

LoRA 扩展链路（按需）：

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|------|--------|------|------|--------|----------|
| L1 | `create_lora_task.py` | 训练名、样本图 URL 列表 | `lora_id` | L2 | 参数或服务异常：修正后重试 L1 |
| L2 | `poll_lora_task.py` | `lora_id` | `photo_task_id` | L3 | 失败：返回错误；成功后继续 L3 |
| L3 | `poll_photo_task.py` | `photo_task_id` | LoRA 结果图 URL | 结束 | 失败：返回错误信息 |

### Workflow Output Semantics

本 Skill 输出语义对齐 [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)：

- `ok`：成功返回远端图片/视频 URL 或本地下载路径
- `need_param`：必要参数缺失或参数不合法（典型 `40000`）
- `auth_required`：凭据不可用（典型 `10400`）
- `upstream_error`：上游接口失败（典型 `50000`）
- `timeout`：轮询超时

## Covered APIs

本 Skill 当前覆盖：

* `POST /open/v1/aigc/photo`
* `GET /open/v1/aigc/photo/task`
* `GET /open/v1/aigc/photo/task/page`
* `POST /open/v1/aigc/motion`
* `GET /open/v1/aigc/motion/task`
* `POST /open/v1/aigc/lora/task/create`
* `GET /open/v1/aigc/lora/task`

## Scripts

脚本目录：

* `skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/`

| 脚本 | 说明 |
|------|------|
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `create_photo_task.py` | 创建文生图任务，输出 `photo_unique_id` |
| `get_photo_task.py` | 获取单个文生图任务详情 |
| `list_tasks.py` | 列出文生图任务列表；返回中 `type=1` 为 photo，`type=2` 为 motion |
| `poll_photo_task.py` | 轮询文生图任务直到完成，默认输出第一张图片地址 |
| `create_motion_task.py` | 创建图生视频任务，输出 `motion_unique_id` |
| `get_motion_task.py` | 获取单个图生视频任务详情 |
| `poll_motion_task.py` | 轮询图生视频任务直到完成，默认输出视频地址 |
| `create_lora_task.py` | 创建 LoRA 训练任务，输出 `lora_id` |
| `get_lora_task.py` | 获取 LoRA 任务详情 |
| `poll_lora_task.py` | 轮询 LoRA 任务直到完成，默认输出第一条 `photo_task_id` |
| `download_result.py` | 下载图片或视频到 `outputs/text-to-digital-person/` |

## Usage Examples

示例 1：文生图后直接图生视频

```bash
PHOTO_TASK_ID=$(python3 skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/create_photo_task.py \
  --age "Young adult" \
  --gender Female \
  --number-of-images 1 \
  --industry "教育培训" \
  --background "现代直播间背景" \
  --detail "短发，亲和力强，职业装" \
  --talking-pose "上半身特写，站立讲解")

PHOTO_URL=$(python3 skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/poll_photo_task.py \
  --unique-id "$PHOTO_TASK_ID")

MOTION_TASK_ID=$(python3 skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/create_motion_task.py \
  --photo-unique-id "$PHOTO_TASK_ID" \
  --photo-path "$PHOTO_URL" \
  --emotion "自然播报，语气清晰自信" \
  --gesture)

python3 skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/poll_motion_task.py \
  --unique-id "$MOTION_TASK_ID"
```

示例 2：LoRA 训练

```bash
LORA_ID=$(python3 skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/create_lora_task.py \
  --name "演示LoRA" \
  --photo-url https://example.com/1.jpg \
  --photo-url https://example.com/2.jpg \
  --photo-url https://example.com/3.jpg \
  --photo-url https://example.com/4.jpg \
  --photo-url https://example.com/5.jpg)

python3 skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/poll_lora_task.py \
  --lora-id "$LORA_ID"
```

## Download Rule

下载是显式动作，不是默认动作：

* `poll_photo_task.py` 和 `poll_motion_task.py` 成功后应先返回远端 URL
* 不要自动下载结果文件
* 只有当用户明确表达“下载到本地”“保存到 outputs”“帮我落盘”时，才执行 `download_result.py`

## Output Convention

默认本地输出目录：

* `outputs/text-to-digital-person/`

## Additional Resources

更多接口细节见：

* `skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/reference.md`
* `skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/examples.md`
