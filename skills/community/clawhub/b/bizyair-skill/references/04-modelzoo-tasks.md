# 04 ModelZoo 任务

用于 modelzoo 的列表检索、详情查询、价格查询、任务创建、状态查询、调用记录。

## 使用前提

ModelZoo 现在有两种入口：

1. **菜单 6 号 / v6（ModelZoo 搜索）**：用户没指定具体 endpoint，但提到「调底层模型 / endpoint / 按次扣费」类需求时，走 `cli.py pick-modelzoo-image` / `pick-modelzoo-video` 帮用户找对路 endpoint。
2. **显式入口**：用户给了 modelzoo 链接、明确说了 endpoint 名、或从菜单 6 号搜索结果里挑了具体 endpoint。

允许：创建任务、查询状态、查询调用记录。
禁止：扫描式批量调用、压测。

## 标准流程

1. `POST /x/v1/modelzoo/list` 搜索目标能力
2. `GET /x/v1/modelzoo/detail/:endpoint` 获取 `input_params` + `outputs_example`
3. `GET /x/v1/modelzoo/price_table/:endpoint` 看价格
4. `POST /x/v1/modelzoo/tasks/openapi/:endpoint` 创建任务
5. `GET /x/v1/modelzoo/tasks/openapi/:request_id` 查状态
6. `POST /x/v1/modelzoo/mycalls` 查记录

## 列表

```bash
curl -sS -X POST "${X_BASE}/modelzoo/list?current=1&page_size=20&sort=Auto" \
  -H "lang: zh" -H "Content-Type: application/json" \
  -d '{"tags":[],"categories":[],"show_deprecated":false}'
```

sort 在 modelzoo/list 不强制校验（与 bizy_models/community 不同）。

## 详情

```bash
curl -sS "${X_BASE}/modelzoo/detail/${ENDPOINT}" -H "lang: zh"
```

重点字段：`display_name` / `input_params` / `outputs_example`

### input_params 字段类型 → payload 类型

| field_type | payload 类型 | 备注 |
|---|---|---|
| customtext | string | |
| combo | string 或 number | 必须是 field_options.values 之一 |
| boolean | bool | |
| number / slider / slides | number | |
| seed | number（-1 = 随机） | |
| images | **list[str]** | 即使一张也要包成数组 |
| audios | string URL | |

注意：modelzoo 的 `field_options` 已经是 dict（不是 JSON 字符串），不需要额外 parse。

## 价格

```bash
curl -sS "${X_BASE}/modelzoo/price_table/${ENDPOINT}" -H "lang: zh"
```

优先用 `simple_price_text` 直接展示（如 "100金币/次"、"5金币/张"）。
部分 endpoint 的 price_table 为空，展示 fallback："该模型暂无价格信息，按实际调用扣费"。

`indicative_price` 接口当前 500 不可用，不要调。

## 创建任务

```bash
curl -sS -X POST "${X_BASE}/modelzoo/tasks/openapi/${ENDPOINT}" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" -H "lang: zh" \
  -d '{"prompt":"a cat","image_size":"1024x1024"}'
```

- 始终异步，< 5s 返回 `{"code":20000,"data":{"request_id":"..."}}`
- 不需要 `X-Bizyair-Task-Async` header（那是 webapp 专属）
- body 字段名直接用 `input_params` 的 `field_name`（不需要 contract 映射）

### 媒体文件上传

通过 `--image`/`--audio`/`--video` 传入本地文件路径，脚本自动上传并**整体替换**默认示例素材：

```bash
python3 scripts/cli.py modelzoo-run <endpoint> \
  --image /path/to/user-photo.jpg \
  --param prompt="a cat"
```

规则：
- `--image` 对应 `field_type=images` 字段，整体替换默认值（不与示例素材合并）
- `--audio` 对应 `field_type=audios` 字段
- `--video` 对应 `field_type=videos` 字段
- 如果同时传了 `--image` 和 `--param image_urls=...`，`--image` 优先
- 支持多张：`--image a.jpg --image b.jpg`
- base64 data URL 不被支持，所有文件统一走 OSS 上传拿真实 HTTP URL

**重要：禁止手动拼媒体参数**

用户提供了图片/音频/视频文件时，**必须**通过 `--image`/`--audio`/`--video` 传入，
**禁止**自己拼 `--param image_urls=[...]`。原因：
1. detail 里的 `field_value` 是示例素材 URL，不要复制到参数里
2. 脚本会自动上传文件并替换默认值，不需要手动处理
3. 自己拼参数容易把示例素材混进去导致结果异常

## 查询状态

```bash
curl -sS "${X_BASE}/modelzoo/tasks/openapi/${REQUEST_ID}" \
  -H "Authorization: Bearer ${TOKEN}" -H "lang: zh"
```

返回 `data.status`：Running / Success / Failed

### outputs 四种形态

```json
{"texts": [...], "images": [...], "videos": [...], "audios": [...]}
```

四种字段并存，只有对应类型的是非空数组。

### Failed 任务

- HTTP 仍然 200 + code=20000
- `data.status = "Failed"`，`data.message` 含原因
- `data.outputs = {}`（空 dict 不是 null）
- "Third-party api response error" → 上游故障，可重试

### 参数错误

- 缺必填字段 → 400 `code=20015 "缺少必要参数: xxx"`
- combo 非法值 → 400 `code=20015 "参数无效，请重新检查 参数xxx无效"`
- 类型错误（如 number 传 string）→ **500 + 空 body**（无 message）

客户端必须做类型预校验，500 空 body 时提示"参数类型可能不对"。

## 调用记录

```bash
curl -sS -X POST "${X_BASE}/modelzoo/mycalls?current=1&page_size=20" \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" -H "lang: zh" \
  -d '{"call_type":"trd_api_record"}'
```

单条详情含 `usage.charge_amount`（精确金币消耗），展示给用户。
