# 分析任务识别规则（参考）
# Analysis Task Recognition Rules (Reference)

**版本：v7.0 | 更新日期：2026-06-02**

> 📌 本文档为**用户参考文件**，所有分析任务均由用户主动提出后执行。
> This document is a **user reference**. All analysis requires an explicit user request.
>
> ⚠️ **【重要安全声明 / IMPORTANT SAFETY NOTICE】**
> 
> **本技能不会:**
> - ❌ 未经用户请求自动触发分析
> - ❌ 自主持续监控市场或价格
> - ❌ 未经用户同意上传数据至第三方
> - ❌ 做出自主交易决策
> 
> **生成方案后的自动操作（已告知用户）:**
> - ✅ 本地保存.docx文件到技能目录
> - ✅ 通过聊天通道发送文件给用户
> 
> **ALL analysis requires an explicit user request. / 所有分析均需用户主动请求。**

---

## 一、触发关键词 / Trigger Keywords

> ⚠️ **重要：关键词仅在用户已明确发起分析请求后才生效。**
> 关键词不是自动触发的，而是辅助识别用户意图的参考标记。
> 本工具不做任何自动检测、自动监控或自动数据采集。
>
> **IMPORTANT: Keywords only activate AFTER an explicit user request.**
> They are reference markers to help identify user intent — NOT auto-triggers.
> This tool does NOT auto-detect, auto-monitor, or auto-collect data.

当用户主动要求分析时，系统可识别以下关键词类别：

### 1.1 股票类 / Stocks
- "股票" / "做个股票方案"
- 股票代码格式：6位数字（如：000001、600519）
- 股票名称 + "方案"

### 1.2 期货类 / Futures
- "期货" / "做个期货方案"
- 期货品种名称：螺纹钢、铁矿石、原油、黄金、白银、铜、铝、锌、镍等
- 期货合约格式：品种+月份

**重要规则：所有期货分析统一使用主力合约！**
- 主力合约定义：持仓量最大的合约

### 1.3 基金类 / Funds
- "基金" / "做个基金分析"
- 基金代码格式：6位数字

### 1.4 经济类 / Economy
- "经济分析" / "宏观经济"
- "大盘分析" / "市场分析"

---

## 二、执行流程 / Execution Flow（用户触发后）

当用户明确要求分析时：

### Step 1：确认任务类型 / Confirm Type
```
识别用户说的是：股票 / 期货 / 基金 / 经济
用户主动确认后开始执行。
```

### Step 2：调取实时数据 / Fetch Data

**方案生成前先获取真实数据，禁止凭空编造。**

#### 2.1 股票数据 / Stock Data

| 数据类型 | 接口 |
|---------|------|
| 实时行情 | 国信GS_API_KEY / yfinance |
| 财务数据 | 国信GS_API_KEY |
| 资金流向 | 国信GS_API_KEY |
| 宏观数据 | 国信GS_API_KEY |

#### 2.2 期货数据 / Futures Data

| 数据类型 | 接口 |
|---------|------|
| 主力合约行情 | Tushare |
| 历史K线 | Tushare |

---

## 三、输出标准 / Output Standards

### 3.1 必须包含的内容

| 项目 | 说明 |
|:----|:-----|
| ✅ 方案头部信息 | 品种名称、日期、版本号 |
| ✅ 市场风险参考 | 基于已获取数据的风险分析 |
| ✅ 完整22/27章节 | 按模板输出 |
| ✅ 风险提示 | 投资有风险声明 |

### 3.2 输出格式 / Output Format

| 项目 | 说明 |
|:----|:-----|
| 文件格式 | Word文档（.docx） |
| 文件命名 | {品种名称}交易方案.docx |
| 发送方式 | 用户确认后发送 |

---

## 四、特殊处理 / Special Cases

### 4.1 市场风险较高时
当分析显示风险较高时，在方案中标注风险等级，不自动阻止用户。

### 4.2 数据获取失败时
使用可用的估算值，并在方案中标注"估算值"。

---

## 五、规则优先级 / Rule Priority

| 级别 | 内容 |
|:----|:-----|
| 🥇 最高 | 用户主动要求的分析任务 |
| 🥈 正常 | 按本文档流程执行 |
| ❌ 不执行 | 任何无人触发的自动任务 |

> **本工具所有操作均需用户主动发起，不进行任何自动执行。**
> **This tool requires explicit user initiation for all operations.**
