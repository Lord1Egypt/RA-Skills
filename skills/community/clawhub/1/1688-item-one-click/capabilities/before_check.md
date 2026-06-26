# before_check — 执行前检查

## 功能说明

执行操作前的前置检查，判断是否可以执行、是否有协议需要签署。**每次修改操作前必须先调用此命令**。

## 前置条件

- 已配置 AK（通过 `cli.py configure YOUR_AK` 或设置环境变量 `ALI_1688_AK`）

## CLI 调用

```bash
python {baseDir}/cli.py before_check --item_id <商品ID> --spi_code <操作码> --spi_params '<参数JSON>'
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
| 发布会员号动态 | `spi_hsf_offer_send_dynamics` | `{"title": "动态标题", "description": "动态内容"}`（参数可选，未提供时返回推荐值） |

## 调用示例

```bash
# 检查修改标题
python {baseDir}/cli.py before_check --item_id 944549591224 --spi_code spi_hsf_automatic_title --spi_params '{"newTitle": "轻奢沙发岩板茶几客厅设计师款2025新款茶桌"}'

# 检查修改主图
python {baseDir}/cli.py before_check --item_id 944549591224 --spi_code spi_hsf_modify_main_img --spi_params '{"newMainImg": "https://cbu01.alicdn.com/img/ibank/O1CN01hLNyMN1a35P8QlySb_!!2220298283273-0-cib.jpg"}'

# 检查设置限时折扣
python {baseDir}/cli.py before_check --item_id 944549591224 --spi_code spi_hsf_offer_promotion_dszk --spi_params '{"discountRate": "9.5", "activityDay": "15"}'

# 检查发布会员号动态（不传参数，获取推荐值）
python {baseDir}/cli.py before_check --item_id 944549591224 --spi_code spi_hsf_offer_send_dynamics --spi_params '{}'

# 检查发布会员号动态（用户指定内容）
python {baseDir}/cli.py before_check --item_id 944549591224 --spi_code spi_hsf_offer_send_dynamics --spi_params '{"title": "夏季新品上架", "description": "清凉透气面料，限时优惠中"}'
```

## 返回结果说明

### 可以执行

```json
{
  "success": true,
  "markdown": "✅ 检查通过，让用户确认后可以执行",
  "data": {
    "__msgInfo__": "让用户确认后可以执行",
    "__success__": true
  }
}
```

**Agent 行为**：向用户展示待修改内容，请求确认后调用 `execute`。

### 需签署协议

```json
{
  "success": true,
  "markdown": "📋 需要签署协议\n\n协议名称：《XX协议》，协议链接：https://terms.alicdn.com/...\n\n让用户确认协议后可以继续执行",
  "data": {
    "data": "协议名称：《XX协议》，协议链接：https://terms.alicdn.com/...",
    "success": true,
    "message": "让用户确认协议后可以继续执行"
  }
}
```

**Agent 行为**：向用户展示协议名称和链接，等待用户确认已阅读协议后再调用 `execute`。

### 不可执行

```json
{
  "success": false,
  "markdown": "❌ 不可执行，最近已经操作过",
  "data": {
    "__msgInfo__": "不可执行，最近已经操作过",
    "__success__": true
  }
}
```

**Agent 行为**：向用户展示不可执行的原因，**终止流程，禁止调用 execute**。

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| AK 未配置 | 提示用户配置 AK |
| 商品ID 未提供 | 提示用户提供 --item_id 参数 |
| 操作码 未提供 | 提示用户提供 --spi_code 参数 |
| 操作参数 格式错误 | 提示用户检查 --spi_params 是否为合法 JSON |
| 签名无效（401） | 提示用户检查 AK 是否有效 |
| 请求被限流（429） | 建议用户等待 1-2 分钟后重试 |
| 服务异常（500） | 提示用户稍后重试 |
