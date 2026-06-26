---
name: chanjing-customised-person
description: Use Chanjing customised person APIs to create, inspect, list, poll, and delete custom digital humans from uploaded source videos.
---

# Chanjing Customised Person

## L2 Product Skill

本文件是 **L2 产品层**主手册（**Agent 执行真值**）。

- **本文件（`chanjing-customised-person-SKILL.md`）**：业务逻辑、追问与异常语义；据此调度 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py) 与 [`scripts/`](scripts/) 下脚本。
- **顶层入口** [`../../SKILL.md`](../../SKILL.md)：仅负责路由到本目录，**不**承载本产品执行细则。
- **跨场景约定** [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)；L3 编排层说明见 [`../../orchestration/README.md`](../../orchestration/README.md)。

## When to Use This Skill

当用户要做这些事时使用本 Skill：

* 上传真人源视频，创建蝉镜定制数字人
* 查询定制数字人列表或单个形象详情
* 轮询定制数字人制作进度
* 删除不再需要的定制数字人

如果需求是“拿已有数字人去合成口播视频”，优先使用 `chanjing-video-compose`。  
如果需求是“上传真人视频做对口型驱动”，优先使用 `chanjing-avatar`。

## Preconditions

凭证由顶层入口统一校验；本 Skill 不重复执行凭证校验步骤。

本 Skill 共用：

* `skills/chanjing-content-creation-skill/.env`（`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`）
* `https://open-api.chanjing.cc`

## Standard Workflow

统一按“每步 = 脚本名 + 输入 + 输出 + 下一步”执行，不做额外追问，由 Agent 自主补齐可选默认值：

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|------|--------|------|------|--------|----------|
| 1 | `upload_file.py` | 本地源视频路径 `--file` | `file_id` | Step 2 | 上传失败：检查文件可读性/格式后重试 Step 1 |
| 2 | `create_person.py` | `file_id`、`name`（可自动生成）、`train_type`（默认 `figure`） | `person_id` | Step 3 | `10400` 回顶层鉴权；`40000` 修正参数后重试 Step 2；`50000` 延迟重试 Step 2 |
| 3 | `poll_person.py` | `person_id` | `preview_url`（远端预览） | Step 4 | 失败：用 `get_person.py` 拉详情并决定回 Step 2 或终止 |
| 4 | `list_persons.py`（按需） | 分页参数（可选） | 历史形象列表 | Step 5 | 失败：跳过历史查看，继续 Step 5 |
| 5 | `delete_person.py`（按需） | `person_id` | 已删除 `person_id` | 结束 | 删除失败：返回错误并保留现有结果 |

### Workflow Output Semantics

本 Skill 输出语义对齐 [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)：

- `ok`：成功返回 `person_id`、`preview_url` 或删除结果
- `need_param`：参数缺失或格式错误（典型 `40000`）
- `auth_required`：凭据不可用（典型 `10400`）
- `upstream_error`：上游接口失败（典型 `50000`）
- `timeout`：轮询超时

## Covered APIs

本 Skill 当前覆盖：

* `GET /open/v1/common/create_upload_url`
* `GET /open/v1/common/file_detail`
* `POST /open/v1/create_customised_person`
* `POST /open/v1/list_customised_person`
* `GET /open/v1/customised_person`
* `POST /open/v1/delete_customised_person`

## Scripts

脚本目录：

* `skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/`

| 脚本 | 说明 |
|------|------|
| `_auth.py` | 读取凭证、获取或刷新 `access_token` |
| `get_upload_url.py` | 获取上传链接，输出 `sign_url`、`mime_type`、`file_id` 等 JSON |
| `upload_file.py` | 上传本地素材并轮询到文件可用，输出 `file_id` |
| `create_person.py` | 创建定制数字人任务，输出 `person_id` |
| `list_persons.py` | 列出定制数字人形象 |
| `get_person.py` | 获取单个数字人详情，默认输出 JSON |
| `poll_person.py` | 轮询形象详情直到完成，默认输出 `preview_url` |
| `delete_person.py` | 删除定制数字人，输出被删除的 `person_id` |

## Usage Examples

示例 1：从本地视频创建定制数字人

```bash
FILE_ID=$(python3 skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/upload_file.py \
  --file ./source.mp4)

PERSON_ID=$(python3 skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/create_person.py \
  --name "演示数字人" \
  --file-id "$FILE_ID" \
  --train-type figure)

python3 skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/poll_person.py --id "$PERSON_ID"
```

示例 2：查看完整详情

```bash
python3 skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/get_person.py \
  --id "C-ef91f3a6db3144ffb5d6c581ff13c7ec"
```

示例 3：列出与删除

```bash
python3 skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/list_persons.py

python3 skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/delete_person.py \
  --id "C-ef91f3a6db3144ffb5d6c581ff13c7ec"
```

## Output Convention

默认不自动下载任何预览视频或封面图：

* `create_person.py` 输出 `person_id`
* `poll_person.py` 输出 `preview_url`，便于继续预览或保存
* 只有在用户明确要求时，才应把返回的资源 URL 另存到本地

如果后续需要落盘预览资源，建议使用：

* `outputs/customised-person/`

## Additional Resources

更多接口细节与触发样例见：

* `skills/chanjing-content-creation-skill/products/chanjing-customised-person/reference.md`
* `skills/chanjing-content-creation-skill/products/chanjing-customised-person/examples.md`
