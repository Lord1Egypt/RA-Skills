---
name: chanjing-ai-creation
description: Use Chanjing AI creation APIs to submit image or video generation tasks across multiple models, inspect task status, poll async results, and explicitly download generated assets when requested.
---

# Chanjing AI Creation

## L2 Product Skill

本文件是 **L2 产品层**主手册（**Agent 执行真值**）。

- **本文件（`chanjing-ai-creation-SKILL.md`）**：业务逻辑、追问与异常语义；据此调度 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py) 与 [`scripts/`](scripts/) 下脚本。
- **顶层入口** [`../../SKILL.md`](../../SKILL.md)：仅负责路由到本目录，**不**承载本产品执行细则。
- **跨场景约定** [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)；L3 编排层说明见 [`../../orchestration/README.md`](../../orchestration/README.md)。

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 用蝉镜 AI 创作模型生成图片
* 用蝉镜 AI 创作模型生成视频
* 查询 AI 创作任务列表或单个任务详情
* 轮询 AI 创作异步结果
* 在用户明确要求时下载图片或视频到本地

如果需求更接近“文生数字人”，优先使用 `chanjing-text-to-digital-person`。  
如果需求更接近“已有数字人视频合成”，优先使用 `chanjing-video-compose`。

## Preconditions

凭证由顶层入口统一校验；本 Skill 不重复执行凭证校验步骤。

本 Skill 共用：

* `skills/chanjing-content-creation-skill/.env`（`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`）
* `https://open-api.chanjing.cc`

## Standard Workflow

统一按“每步 = 脚本名 + 输入 + 输出 + 下一步”执行，不做额外追问，由 Agent 自主补齐可选默认值：

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|------|--------|------|------|--------|----------|
| 1 | `submit_task.py` | 必填：`creation_type`、`model_code`；二选一：通用参数 or `--body-file/--body-json` | `unique_id` | Step 2 | `10400` 回顶层鉴权；`40000` 修正参数后重试 Step 1；`50000` 延迟重试 Step 1 |
| 2 | `poll_task.py` | `unique_id` | `output_url`（远端） | Step 3 | 超时/失败：用 `get_task.py` 取详情后回 Step 1 或终止并返回错误 |
| 3 | `get_task.py`（按需） | `unique_id` | 任务详情（状态/错误原因/参数回显） | Step 4 | 若查询失败，记录错误并继续 Step 4 |
| 4 | `list_tasks.py`（按需） | 分页参数（可选） | 历史任务列表 | Step 5 | 若查询失败，跳过历史回看，继续 Step 5 |
| 5 | `download_result.py`（仅显式下载） | `output_url`、`output_dir`（可选） | 本地文件路径 | 结束 | 下载失败：返回远端 `output_url` 与错误信息 |

执行策略：

* 常见图片/视频模型优先使用脚本通用参数
* 特殊模型参数统一走 `--body-file` 或 `--body-json` 透传

### Workflow Output Semantics

本 Skill 输出语义对齐 [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)：

- `ok`：任务成功并返回远端结果 URL 或本地文件路径
- `need_param`：提交参数无法通过脚本校验（典型 `40000`）
- `auth_required`：凭据不可用（典型 `10400`）
- `upstream_error`：上游接口失败（典型 `50000`）
- `timeout`：轮询超时或长时间未完成

## Covered APIs

本 Skill 当前覆盖：

* `POST /open/v1/ai_creation/task/submit`
* `POST /open/v1/ai_creation/task/page`
* `GET /open/v1/ai_creation/task`

## Scripts

脚本目录：

* `skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/`

| 脚本 | 说明 |
|------|------|
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `submit_task.py` | 提交 AI 创作任务，输出 `unique_id` |
| `get_task.py` | 获取单个任务详情 |
| `list_tasks.py` | 列出图片或视频任务 |
| `poll_task.py` | 轮询任务直到完成，默认输出第一个结果地址 |
| `download_result.py` | 下载图片或视频到 `outputs/ai-creation/` |

## Usage Examples

示例 1：Seedream 3.0 文生图

```bash
TASK_ID=$(python3 skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/submit_task.py \
  --creation-type 3 \
  --model-code "doubao-seedream-3.0-t2i" \
  --prompt "赛博朋克城市夜景，霓虹灯，雨夜，电影镜头" \
  --aspect-ratio "16:9" \
  --clarity 2048 \
  --number-of-images 1)

python3 skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/poll_task.py --unique-id "$TASK_ID"
```

示例 2：腾讯 Kling v2.1 Master 图生视频

```bash
TASK_ID=$(python3 skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/submit_task.py \
  --creation-type 4 \
  --model-code "tx_kling-v2-1-master" \
  --ref-img-url "https://res.chanjing.cc/chanjing/res/aigc_creation/photo/start.jpg" \
  --ref-img-url "https://res.chanjing.cc/chanjing/res/aigc_creation/photo/end.jpg" \
  --prompt "角色从静止到转身，镜头平滑移动，叙事感强" \
  --aspect-ratio "9:16" \
  --clarity 1080 \
  --quality-mode pro \
  --video-duration 5)

python3 skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/poll_task.py --unique-id "$TASK_ID"
```

示例 3：直接透传完整 JSON

```bash
python3 skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/submit_task.py \
  --body-file ./payload.json
```

## Download Rule

下载是显式动作，不是默认动作：

* `poll_task.py` 成功后应先返回远端 `output_url`
* 不要自动下载结果文件
* 只有当用户明确表达“下载到本地”“保存到 outputs”“帮我落盘”时，才执行 `download_result.py`

## Output Convention

默认本地输出目录：

* `outputs/ai-creation/`

## Additional Resources

更多接口细节见：

* `skills/chanjing-content-creation-skill/products/chanjing-ai-creation/reference.md`
* `skills/chanjing-content-creation-skill/products/chanjing-ai-creation/examples.md`
