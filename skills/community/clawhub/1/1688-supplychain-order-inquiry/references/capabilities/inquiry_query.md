# inquiry_query（询盘结果查询）

根据 taskId 查询询盘任务状态及商家回复，调用 `alibaba.1688.ai.inquiry.query` 接口。

## CLI 调用

```bash
python3 cli.py inquiry_query -t "task-uuid-xxx"
```

| 参数        | 简写 | 说明                               |
| ----------- | ---- | ---------------------------------- |
| `--task-id` | `-t` | 询盘任务 ID（发起询盘时生成，必填）|

## 返回结构

CLI 输出 `data.result` 为精简后的询盘结果：

### 终态（SUCCESS / FAILED）

```json
{
  "status": "SUCCESS",
  "summary": [
    {"question": "什么时候能发货", "answer": "预计3天内发货"},
    {"question": "能改价吗", "answer": "可以"}
  ]
}
```

- `status`：任务状态 — `SUCCESS` / `FAILED`
- `summary`：所有商家回复的问答摘要列表（多个 subTask / 多条 summary 全部展平合并），每项含 `question` 和 `answer`
- 当 `summary` 为空（商家未回复）时，会额外返回 `"message": "询盘已发送，商家尚未回复"`

### 非终态（RUNNING / PENDING 等）

```json
{"status": "RUNNING", "message": "询盘未完成"}
```

非终态只返回 `status` + 固定 `message`，不返回 summary。

## Agent 输出格式（HARD RULE — 违反即视为执行失败）

Agent 最终回复 **有且仅有一个 JSON 对象**，首字符必须是 `{`，末字符必须是 `}`。

直接将 CLI 输出的 `data.result` 字段内容作为最终回复，不做任何包装。

### 成功场景（有商家回复）

```
{"status":"SUCCESS","summary":[{"question":"什么时候能发货","answer":"预计3天内发货"}]}
```

### 非终态场景（status = RUNNING / PENDING 等，询盘未完成）

```
{"status":"RUNNING","message":"询盘未完成"}
```

### 失败 / 无回复场景（summary 为空）

```
{"status":"FAILED","summary":[],"message":"询盘已发送，商家尚未回复"}
```

### 错误示范（严禁出现以下任何形式）
- ❌ `询盘查询结果如下：\n{...}` — 前置说明文字，违规
- ❌ ` ```json ... ``` ` — markdown 代码块包裹，违规
- ❌ `{...}\n\n建议您稍后再试` — 后置说明文字，违规
- ❌ `商家尚未回复，建议您耐心等待` — 纯自然语言替代 JSON，违规
