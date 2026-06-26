# 03 AI 应用任务

用于 AI 应用的参数整理、任务创建、状态查询、结果获取。

## 标准流程

1. `GET /x/v1/webapp/:bizy_model_id` → 拿 `data.id`（= web_app_id）+ `data.input_nodes`
2. 从 `input_nodes` 构建 `input_values`（variable_name → 值）
3. `POST /w/v1/webapp/task/openapi/create` 创建任务
4. 轮询 `GET /w/v1/webapp/task/openapi/detail?requestId=...`
5. 成功后 `GET /w/v1/webapp/task/openapi/outputs?requestId=...` 拿结果

## 关键规则

### web_app_id 来源

- 路径上的是 `bizy_model_id`（如 46086）
- 返回的 `data.id` 才是 `web_app_id`（如 47362）
- create 时必须用 `data.id`，不是路径上的 ID

### input_nodes → input_values

`input_nodes` 是有序 list，每项含 `variable_name`（如 `93:CLIPTextEncode.text`）。

create 时 `input_values` 是 `{variable_name: 值}` 的 dict：
```json
{
  "web_app_id": 47362,
  "input_values": {
    "93:CLIPTextEncode.text": "1girl, smile",
    "47:EmptyLatentImage.width": 960
  }
}
```

- 不需要全填：服务端会用 webapp 的 default 兜底未传字段
- 但 `input_values` 不能是空 dict `{}`（会报 40025）
- 至少传 1 个 key（通常是 prompt）

### 异步模式（默认）

加 `X-Bizyair-Task-Async: enable` header：
- HTTP **202**，345ms 立即返回 `{"request_id": "..."}`（裸 body，无 code/message 包装）
- 之后轮询 detail → outputs

不加 header（同步模式）：
- HTTP 200，阻塞 30-120s 直接返回完整结果（含 outputs）
- 仅作为调试 fallback

### suppress_preview_output

- 不传或传 `false`：outputs 正常返回
- 传 `true`：outputs 端点返回 null（**不要传 true**）

## 参数卡规则

### 排序

1. 提示词 / 素材
2. 模型档位（仅多选时展示）
3. 比例 / 尺寸 / 分辨率
4. 时长（视频）
5. 随机性 / seed
6. 其他

### 默认不等于执行

"默认" / "你定" / "按推荐" → 仅授权预填参数卡，**不等于授权执行**。
"开跑" / "直接跑" / "确认执行" → 才放行真实执行。

### 枚举字段

底层固定枚举参数必须列全可选范围，不能用开放式提问。

## Prompt 优化

> 以下规则是给 agent 的行为指导，脚本层（build_prompt_bundle_for_args）当前为 passthrough 模式，不做自动扩写。

Agent 收到用户的简短描述后，应扩写为模型友好的 prompt。用户已给详细描述的不要画蛇添足。

### 何时扩写

- 输入 < 15 字且无具体视觉描述 → 扩写
- 已有详细画面描述 → 原样使用，最多微调格式
- 用户明确说"就这样" / "不要改" → 严格原样

### 扩写维度

从用户核心意图出发，按需补充（不必全补）：

1. **主体**：是什么、在做什么、数量、姿态
2. **环境**：场景、背景、光线、天气、时间
3. **风格**：写实 / 插画 / 3D / 赛博朋克 / 水彩 等
4. **构图**：特写 / 全身 / 俯视 / 侧面 等
5. **画质**：高清、细节丰富（酌情，不堆砌）

### 语言选择

| 模型类型 | 推荐语言 | 说明 |
|---|---|---|
| Flux 系（Nano Banana、Klein） | 英文 | 英文 prompt 效果更稳定 |
| 国产模型（即梦、Qwen） | 中文 | 中文理解好，无需翻译 |
| GPT 系（ChatGPT Image） | 英文 | 擅长复杂英文指令 |
| 视频模型 | 跟用户原文 | 主流视频模型中英文都行 |

英文模型场景：Agent 把用户中文写成自然的英文画面描述，不是机翻。

### 视频额外维度

- **运动**：主体做什么动作、怎么移动
- **镜头**：推 / 拉 / 平移 / 跟随 / 固定
- **节奏**：快 / 慢 / 渐变

### 不要做

- 堆砌质量词（`masterpiece, best quality, 8k, award winning` 连排）→ 稀释主题
- 矛盾风格（`realistic photo, anime style`）→ 选一个
- 替换用户意图（用户说"简单的猫"，改成"赛博朋克机械猫"）→ 扩写是补细节，不是换主题

## 执行与状态

### 状态枚举

| status | 含义 |
|---|---|
| Queuing | 排队中 |
| Preparing | 准备中 |
| Running | 执行中 |
| Success | 成功 |
| Failed | 失败（看 data.message） |

### 输出交付

- 图片：`![生成结果](url)` 原样转发
- 视频：裸 URL 单独一行（不要包成 markdown 链接）
- 一次任务可能多输出（工作流含多个保存节点）
- 过程图（如 rgthree.compare 的 _temp_ 缩略图）不展示给用户
- 输出有 `expired_at`（~15 天后过期），建议及时下载

### 失败分类

1. 提交阶段（鉴权/参数/映射）
2. 平台执行（超时/服务忙/上游失败）
3. 材料与参数（格式/尺寸/缺项）
4. 结果回收（下载失败/地址不可达）

### 底层字段静默

REQUEST_ID / TASK_ID / STATUS / 原始 JSON 不主动展示给用户，除非用户明确要排障。

## 执行权限

- 普通 app → 可直接执行
- 带关联 app 的 workflow → 可继续执行
- 没有关联 app 的 workflow → 只看不跑（需先 fork 成 Application）
