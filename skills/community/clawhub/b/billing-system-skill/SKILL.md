---
name: billing-system
version: 3.1.0
description: 对账单生成系统 — 零配置通用版。自动注册试用账户，自动下载模板。Excel含汇总分析+客户余额趋势图（万元），PDF含双利息主体明细。
agent_created: true
---

# 对账单生成系统

## 两种使用方式

| 方式 | 适合 | 说明 |
|------|------|------|
| **在线版** | 任意设备、无需安装 | 通过 SCF 云函数生成，curl 调用 |
| **EXE 版** | Windows 桌面 | 双击运行，无需联网 |

---

# 在线版

## 服务地址
```
https://1440636612-55rmw631p6.ap-beijing.tencentscf.com
```

## 首次使用（自动注册）

此 Skill 不含 API Key。首次调用时 **自动注册试用账户（3 次配额）**：

```
1. curl "https://1440636612-55rmw631p6.ap-beijing.tencentscf.com/auto-register"
   → 返回 {"key":"wb-xxxxxxxx","user":"试用用户_xxxx","quota":3,"role":"trial"}
2. 把返回的 key 保存为本地变量，后续所有请求带上这个 key
```

## 完整调用流程

### Step 1: 注册/获取 Key

如果还没有 key：
```bash
# 自动注册
RESP=$(curl -s "https://1440636612-55rmw631p6.ap-beijing.tencentscf.com/auto-register")
KEY=$(echo $RESP | python -c "import sys,json; print(json.load(sys.stdin)['key'])")
echo "你的 Key: $KEY"
```

如果已经有 key，跳过此步。

### Step 2: 下载模板

```bash
curl -o template_input.xlsx \
  "https://1440636612-55rmw631p6.ap-beijing.tencentscf.com/template?key=$KEY"
```

### Step 3: 填写模板数据

模板包含 4 个 Sheet：

| Sheet | 说明 |
|-------|------|
| 使用说明 | 模板使用指引 |
| 客户信息 | 客户名称、年利率(%)、期初余额月份、期初余额(元)、备注 |
| 借款记录 | 客户名称、月份、借款编号、借款日期、到期日期、借款金额(元)、春晖利率(%)、红润利率(%)、备注 |
| 还款记录 | 客户名称、月份、还款编号、还款日期、还款金额(元)、指定借款、备注 |

> 利率留空则使用客户信息中的默认年利率。指定借款留空则自动分配。

### Step 4: 生成对账单

```bash
curl -X POST \
  "https://1440636612-55rmw631p6.ap-beijing.tencentscf.com/generate?key=$KEY" \
  -F "file=@template_input.xlsx" \
  -o 对账单结果.zip
```

### Step 5: 解压结果

```bash
unzip 对账单结果.zip -d 对账单结果/
```

## 生成内容

### Excel 对账单（`对账单_时间戳.xlsx`）
| Sheet | 内容 |
|-------|------|
| 汇总 | 所有客户各月账务汇总表 |
| 汇总分析 ⭐ | 当月客户余额表（含合计）、下月还款预计（含合计）、月度余额趋势图（万元）、月度户数柱状图 |
| 各客户 | 每客户月度账务明细、借款/还款明细、月度余额变动折线图（万元，含数据标签） |

### PDF 对账单（按月分文件夹）
- 每客户每月一份 PDF，含账单汇总 + 借款明细 + 还款明细 + 付款账户信息
- 双利息主体独立挂账，人民币符号使用 ￥（全角）


---

# EXE 版（本地，无需联网）

## 使用方式

1. 将 `对账单生成.exe` 和 `template_input.xlsx` 放在同一文件夹
2. 填入模板数据
3. **双击 `对账单生成.exe`** → 自动在 `账单成品/` 生成所有 Excel 和 PDF

```
文件夹/
├── 对账单生成.exe        ← 双击运行
├── template_input.xlsx   ← 填入数据
└── 账单成品/             ← 自动生成
    ├── 对账单_时间戳.xlsx
    ├── 2026-04月对账单/
    │   ├── XX公司_2026-04_对账单.pdf
    │   └── ...
    └── ...
```

- **更新数据**：覆盖 `template_input.xlsx`，再次双击即可
- **系统要求**：Windows 64 位，无需安装 Python

---

# Agent 工作指引

## 在对话中使用（WorkBuddy Agent）

当用户说"生成对账单"、"制作账单"时：

1. **如果没有 key**：先 curl 调用 `/auto-register` 注册
2. **如果没有模板**：curl 下载模板到本地
3. **帮用户填写数据**：确认借款/还款数据后，用 openpyxl 写入模板
4. **POST 上传生成**：curl POST /generate
5. **解压结果**：unzip 后告知用户文件列表

### 模板填写示例（用 openpyxl）

```python
import openpyxl
wb = openpyxl.load_workbook("template_input.xlsx")

# 客户信息（Sheet 2）
ws1 = wb["客户信息"]
ws1.append(["张三", 12, "2025-01", 100000, ""])

# 借款记录（Sheet 3）
ws2 = wb["借款记录"]
ws2.append(["张三", "2025-01", "JK001", "2025-01-15", "2025-07-15", 50000, 0, 0, ""])

# 还款记录（Sheet 4）
ws3 = wb["还款记录"]
ws3.append(["张三", "2025-02", "HK001", "2025-02-28", 20000, "", ""])

wb.save("template_input.xlsx")
```

## 计费规则

- 试用账户：**3 次免费配额**
- 正式账户：按配额计费
- 余额不足返回 HTTP 402
- 联系管理员开通正式账户

## 注意事项

- 首次使用需注册（自动），Key 建议保存到本地文件
- SCF 多实例部署，注册和生成需在同一连接中快速完成
- EXE 版无需注册、无需联网
- 模板中的「使用说明」Sheet 有完整指引
