---
name: billcat-save-my-money
description: "使用 BillCat API 从自然语言中提取并保存记账信息到乖猫记账 App，并支持删除账单、账单统计、账本与资产列表查询。适合当用户想把一句中文消费/收入描述转成结构化账单、按 billId 删除账单、按时间范围统计收入支出，或查看账本/资产汇总时使用。"
homepage: https://github.com/isee15/billcat-save-my-money
metadata: {"openclaw":{"emoji":"🐱","requires":{"env":["BILLCAT_API_KEY"]},"primaryEnv":"BILLCAT_API_KEY"}}
---

# BillCat Save My Money

通过 BillCat 的 `extractbill` 与 `skill` 接口，把自然语言账单描述提取成结构化 JSON 并实际保存到 **乖猫记账 App** 中，同时支持按 `billId` 删除账单、按日期范围统计收入支出，以及查询账本和资产汇总。

## 获取 API Key

1. 下载 **乖猫记账** App。
2. 在 App 内给 OpenClaw 发送一条消息 "openclaw"。
3. 返回内容里可拿到 `BILLCAT_API_KEY`。

## 配置方式

### 方式 1：环境变量

```bash
# Windows PowerShell
$env:BILLCAT_API_KEY="你的 key"

# macOS / Linux
export BILLCAT_API_KEY="你的 key"
```

### 方式 2：写入 `~/.openclaw/.env`

```env
BILLCAT_API_KEY=你的 key
```

### 方式 3：写入 `~/.openclaw/openclaw.json`

这个 skill 现在也会自动读取 `skills.entries.billcat-save-my-money.apiKey`，并把它当作 `BILLCAT_API_KEY` 使用。

```json
{
	"skills": {
		"entries": {
			"billcat-save-my-money": {
				"apiKey": "你的 billcat key"
			}
		}
	}
}
```

也支持显式写成：

```json
{
	"skills": {
		"entries": {
			"billcat-save-my-money": {
				"env": {
					"BILLCAT_API_KEY": "你的 billcat key"
				}
			}
		}
	}
}
```

优先级：`BILLCAT_API_KEY` 环境变量 > `openclaw.json` > `~/.openclaw/.env`

## 命令

在 OpenClaw 工作区运行：

```bash
# 默认输出原始 JSON
python {baseDir}/scripts/extract_bill.py --text "中午吃饭160"

# 美化 JSON
python {baseDir}/scripts/extract_bill.py --text "打车花了35" --format pretty

# 输出简洁 Markdown
python {baseDir}/scripts/extract_bill.py --text "收到工资8000" --format md

# 删除一条账单
python {baseDir}/scripts/delete_bill.py --bill-id "账单ID" --format md

# 删除多条账单
python {baseDir}/scripts/delete_bill.py --bill-id "billId1,billId2" --format pretty

# 统计某个时间范围内的总的收入和支出
python {baseDir}/scripts/bill_statistics.py --start-date 20260301 --end-date 20260331 --format md

# 查询某个时间范围内的账本和资产汇总，也可以统计某个时间范围内的账本或者资产的收入和支出情况
python {baseDir}/scripts/list_books_assets.py --start-date 20260301 --end-date 20260324 --format md

# 不传日期，直接查询当前可用账本和资产
python {baseDir}/scripts/list_books_assets.py --format pretty

# 从标准输入读取
echo "昨天买咖啡18" | python {baseDir}/scripts/extract_bill.py --stdin --format pretty
```

## 能力说明

### 1. 提取并保存账单

- 调用 `extractbill` 接口
- 成功后会保存账单
- 建议使用 `--format md` 或 `--format pretty`，这样更容易看到返回的 `billId`

### 2. 删除账单

- 调用 `skill` 接口，`action=delete`
- 需要传入一个或多个 `billId`
- 支持逗号分隔

### 3. 账单统计

- 调用 `skill` 接口，`action=statics`
- 需要传入 `startDate` 和 `endDate`
- 日期格式固定为 `YYYYMMDD`

### 4. 账本与资产列表

- 调用 `skill` 接口，`action=list`
- 可选传入 `startDate` 和 `endDate`
- 返回账本列表 `books` 与资产列表 `assets`
- 每个账本/资产都会附带 `totalIncome`、`totalExpense`、`netAmount`

## 输出格式

### raw
直接返回 BillCat API 原始 JSON。

### pretty
格式化后的 JSON，便于阅读。

### md
优先提取常见字段并输出为 Markdown；记账结果会优先展示 `billId`，便于后续删除账单；如果接口字段未知，则回退为 JSON 代码块。

## 适用场景

- 用户想把一句消费描述转成结构化账单并直接保存到 App
- 用户想在成功记账后拿到 `billId` 以便后续删除或追踪
- 用户想按 `billId` 删除一条或多条账单
- 用户想统计某个时间范围内的收入、支出和净额
- 用户想查看某段时间内各账本、资产账户的收入/支出/净额汇总
- 用户要快速识别金额、类型、时间、备注等字段
- 用户要把聊天式输入接入记账流水线
- 用户在做“自动记账”“消费整理”“账单抽取”相关自动化

## 注意事项

- 该 skill 目前封装的是接口：`POST https://billcat.cn/api/app/openclaw/extractbill`
- 删除和统计能力封装的是接口：`POST https://billcat.cn/api/app/openclaw/skill`
- 账本/资产列表查询能力也封装在接口：`POST https://billcat.cn/api/app/openclaw/skill`
- 虽然接口名叫 `extractbill`，但调用成功后，账单也会同步保存到乖猫记账 App
- 删除账单必须依赖 `billId`，因此建议记账时保留原始 JSON，或直接使用 Markdown/pretty 输出查看 `billId`
- 统计接口当前使用的 action 是 `statics`
- 列表接口当前使用的 action 是 `list`
- 输入建议尽量简洁自然，例如：`午饭 32`、`地铁 4 元`、`3 月房租 2500`
- 如果只是想测试，请避免重复提交同一条内容，以免在 App 中生成重复账单
- 如果接口返回了更丰富的分类字段，优先保留原始 JSON 以免丢失信息
