# transfer_inquiries（转人工询盘明细查询）

## 功能说明

按日期分页查询当日转人工的询盘明细记录（接待助手答不上来、主动转给商家处理的会话）。与 `daily_report` 关系：`daily_report` 只给「转人工次数」的**汇总值**，本命令给**逐条明细**（什么时间 / 哪个买家 / 询盘总结 / 转人工原因）。

## CLI 调用

```bash
python3 cli.py transfer_inquiries                                  # 默认 today / 第 1 页 / 每页 10 条
python3 cli.py transfer_inquiries --date 2026-05-14
python3 cli.py transfer_inquiries --date today --page-num 2 --page-size 20
```

### TPP 接口

`POST /api/query_transfer_inquiries/1.0.0`

请求体：
```json
{"date": "2026-05-14", "pageNum": 1, "pageSize": 10}
```

### 完整参数表

| 参数            | 简写 | 说明                              | 默认值 |
| --------------- | ---- | --------------------------------- | ------ |
| `--date`        | `-d` | 查询日期：'today' 或 YYYY-MM-DD   | today  |
| `--page-num`    | `-p` | 页码，>=1                         | 1      |
| `--page-size`   | `-s` | 每页大小，1~100                   | 10     |

## 输出格式

```json
{
  "success": true,
  "markdown": "## 转人工询盘（2026-05-14）\n\n> 共 **5** 条 · 第 1 / 1 页（每页 10 条）\n\n| 时间 | 买家 | 公司 | 询盘总结 | 转人工原因 |\n...",
  "data": {
    "date": "2026-05-14",
    "elapsed_seconds": 0.4,
    "page_num": 1,
    "page_size": 10,
    "total": 5,
    "total_pages": 1,
    "inquiries": [
      {
        "id": "INQ001",
        "inquiry_time": "2026-05-14 10:30:00",
        "inquiry_summary": "询问商品材质和是否能定制 logo",
        "transfer_reason": "涉及定制需求，超出标准接待范围",
        "buyer_nickname": "张三",
        "buyer_login_id": "zhangsan",
        "buyer_company_name": "上海科技有限公司",
        "buyer_tags": "VIP客户, 老客户",
        "buyer_avatar": "https://..."
      }
    ]
  }
}
```

### 字段映射（网关 → 项目内部）

| 网关字段             | 项目内部字段           | 说明              |
| -------------------- | ---------------------- | ----------------- |
| `id`                 | `id`                   | 询盘 ID           |
| `inquiryTime`        | `inquiry_time`         | 转人工发生时间    |
| `inquirySummary`     | `inquiry_summary`      | 询盘总结          |
| `transferReason`     | `transfer_reason`      | 转人工原因        |
| `buyerNickname`      | `buyer_nickname`       | 买家昵称          |
| `buyerLoginId`       | `buyer_login_id`       | 买家登录 ID       |
| `buyerCompanyName`   | `buyer_company_name`   | 买家公司名        |
| `buyerTags`          | `buyer_tags`           | 买家标签          |
| `buyerAvatar`        | `buyer_avatar`         | 买家头像 URL      |
| `buyerLoginIdEncode` | —（**不暴露**）        | 系统内部编码值    |

## 注意事项

1. **双层 Result 包装**：网关返回的 `data` 字段是内层 `AiSellerCcPageResult { data: [...DTO], total, pageNum, pageSize, totalPages }`，需剥两层才能拿到真正的 DTO 列表
2. **日期格式**：仅接受 ISO 格式 `YYYY-MM-DD`，斜杠格式不合法
3. **sellerUserId 不需传递**：网关会根据 AK 自动注入实际调用方 userId
4. **`buyerLoginIdEncode` 严禁向商家展示**：属于系统内部编码值，不得透出
5. 空列表时输出"该日期暂无转人工询盘"，不要编造数据
6. 分页边界：`pageNum >= 1`、`pageSize` 在 1~100 之间，超出 CLI 层直接拒绝

## 关联页面

商家看完转人工明细后，常见追问是"我要在哪里接手 / 补答这些询盘"——主 Agent 应同时调 `show_interaction(name='manage_reception')` 打开接待管理 Tab，让商家在页内手动接管 / 调整接待范围；**主 Agent 不在对话里代回询盘**。
