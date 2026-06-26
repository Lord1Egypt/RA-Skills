# execute — 执行操作

## 功能说明

执行实际的商品修改操作（修改标题/主图/设置限时折扣/发布会员号动态）。属于写操作，会直接变更商品数据。**必须在 `before_check` 通过且用户确认后才能调用**。

## 前置条件

- 已配置 AK（通过 `cli.py configure YOUR_AK` 或设置环境变量 `ALI_1688_AK`）
- 已调用 `before_check` 且检查结果为"可以执行"或"协议已确认"
- 用户已明确确认执行

## CLI 调用

```bash
python {baseDir}/cli.py execute --item_id <商品ID> --spi_code <操作码> --spi_params '<参数JSON>'
```

**参数说明**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--item_id` | str | 是 | 商品ID |
| `--spi_code` | str | 是 | 操作码（见下方操作类型表） |
| `--spi_params` | str | 是 | 操作参数，JSON 字符串 |

**操作类型**：

| 操作 | spi_code | spi_params 示例 |
|------|----------|----------------|
| 修改标题 | `spi_hsf_automatic_title` | `{"newTitle": "新标题"}` |
| 修改主图 | `spi_hsf_modify_main_img` | `{"newMainImg": "图片URL"}` |
| 设置限时折扣 | `spi_hsf_offer_promotion_dszk` | `{"discountRate": "9.5", "activityDay": "15"}` |
| 发布会员号动态 | `spi_hsf_offer_send_dynamics` | `{"title": "动态标题", "description": "动态内容"}` |

## 调用示例

```bash
# 执行修改标题
python {baseDir}/cli.py execute --item_id 944549591224 --spi_code spi_hsf_automatic_title --spi_params '{"newTitle": "轻奢沙发岩板茶几客厅设计师款2025新款茶桌"}'

# 执行修改主图
python {baseDir}/cli.py execute --item_id 944549591224 --spi_code spi_hsf_modify_main_img --spi_params '{"newMainImg": "https://cbu01.alicdn.com/img/ibank/O1CN01hLNyMN1a35P8QlySb_!!2220298283273-0-cib.jpg"}'

# 执行设置限时折扣
python {baseDir}/cli.py execute --item_id 944549591224 --spi_code spi_hsf_offer_promotion_dszk --spi_params '{"discountRate": "9.5", "activityDay": "15"}'

# 执行发布会员号动态
python {baseDir}/cli.py execute --item_id 944549591224 --spi_code spi_hsf_offer_send_dynamics --spi_params '{"title": "夏季新品上架", "description": "清凉透气面料，限时优惠中"}'
```

## 返回结果说明

### 执行成功

```json
{
  "success": true,
  "markdown": "✅ 执行成功，成功信息是：标题一键优化成功",
  "data": {
    "__msgInfo__": "执行成功，成功信息是：标题一键优化成功",
    "data": "沙发岩板茶几客厅设计师款2025新款茶桌",
    "__userId__": true
  }
}
```

**Agent 行为**：向用户展示操作成功信息和修改后的内容。

### 执行失败

```json
{
  "success": false,
  "markdown": "❌ 执行失败，原因是：新标题和原标题一致",
  "data": {
    "__msgInfo__": "执行失败，原因是：新标题和原标题一致",
    "__userId__": false
  }
}
```

**Agent 行为**：向用户展示失败原因。

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| AK 未配置 | 提示用户配置 AK |
| 商品ID 未提供 | 提示用户提供 --item_id 参数 |
| 操作码 未提供 | 提示用户提供 --spi_code 参数 |
| 操作参数 格式错误 | 提示用户检查 --spi_params 是否为合法 JSON |
| 新标题和原标题一致 | 提示用户提供不同的标题 |
| 签名无效（401） | 提示用户检查 AK 是否有效 |
| 请求被限流（429） | 建议用户等待 1-2 分钟后重试 |
| 服务异常（500） | 提示用户稍后重试 |

## 展示规范

展示时必须：
1. 展示商品ID（item_id）
2. 展示操作类型（修改标题/修改主图）
3. 展示操作结果（成功/失败）
4. 如果成功，展示修改后的内容
5. 如果失败，展示失败原因
