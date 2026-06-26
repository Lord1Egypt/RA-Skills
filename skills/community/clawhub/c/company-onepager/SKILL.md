---
name: company-onepager
description: 生成上市公司"一页纸"调研简报，整合基本信息、市场数据、近10年财务数据表格、近10年月K线图、股东结构、近期新闻。数据优先级：iFinD → Tushare → AkShare + Web Search。每个章节标注数据来源。使用场景：(1) 调研股票/公司信息 (2) 生成股票分析报告 (3) 整合多维数据形成综合报告 (4) 输出 Markdown + PDF。触发词：调研股票、公司简报、一页纸报告、股票分析。Requires TUSHARE_TOKEN (env var) and iFinD auth_token (config file).
metadata:
  clawdbot:
    requires:
      bins: ["python3"]
      env: ["TUSHARE_TOKEN"]
    primaryEnv: "TUSHARE_TOKEN"
    configFiles:
      - path: "~/.openclaw/workspace/skills/ifind-finance-data/mcp_config.json"
        key: "auth_token"
        provider: "iFinD"
        instructions: "Get token from iFinD Terminal → Tools → Data MCP"
---

# Company Onepager - 上市公司"一页纸"简报（v7.1）

## ⚠️ 必需凭证配置

本 skill 需要配置两个数据源凭证才能正常运行：

| 凭证 | 类型 | 配置方式 | 获取途径 |
|------|------|----------|----------|
| **TUSHARE_TOKEN** | 环境变量 | `export TUSHARE_TOKEN="your_token"` 或写入 `~/.bashrc` | https://tushare.pro |
| **iFinD auth_token** | 配置文件 | `~/.openclaw/workspace/skills/ifind-finance-data/mcp_config.json` 中的 `auth_token` 字段 | iFinD终端 → 工具 → 常用工具 → 数据MCP |

**配置示例：**

```bash
# Tushare Token（必需）
export TUSHARE_TOKEN="your_tushare_token"

# iFinD Token（可选，用于获取更多数据）
# 将 auth_token 写入 mcp_config.json
```

**降级机制：** 当高优先级数据源凭证缺失时，自动降级到下一级：
- iFinD 凭证缺失 → 使用 Tushare
- Tushare 凭证缺失 → 使用 AkShare（无需凭证）
- 但 TUSHARE_TOKEN 环境变量必须设置（代码会检查），即使只用 AkShare

## 核心特性

1. **数据优先级**：iFinD → Tushare → AkShare（不使用网络搜索作为主要数据源）
2. **近10年财务数据表格**：包含每股营收、每股现金流、每股盈利、每股派息、每股净资产、毛利率、净利润率、主营收入、净利润、库存等指标
3. **近10年月K线图**：价格走势 + 成交额 + Zigzag趋势线
4. **数据来源标注**：每个章节标注数据来源
5. **Web Search 增强**：通过 web_search 获取投资亮点、核心产品、品牌壁垒等信息
6. **智能股东识别**：自动过滤托管机构，识别真正控股股东

## Workflow

```bash
python3 scripts/onepager.py <股票代码>
```

示例：
```bash
python3 scripts/onepager.py 300308.SZ
python3 scripts/onepager.py 600519.SH
```

### 数据获取优先级

| 优先级 | 数据源 | 配置要求 | 数据覆盖 |
|--------|--------|----------|----------|
| 1 | **iFinD** | `auth_token` in `mcp_config.json` | 基本信息、财务数据、K线、股东、新闻 |
| 2 | **Tushare** | `TUSHARE_TOKEN` (env var) | 基本信息、市场数据、财务数据、K线、股东 |
| 3 | **AkShare** | 无需配置 | 基本信息、市场数据（兜底） |

**注意：** 即使只使用 AkShare，也必须设置 `TUSHARE_TOKEN` 环境变量（代码启动时检查）。

## 简报内容结构

### 1. 公司基本信息
- 公司名称、股票代码、交易所、申万行业、上市时间、总市值
- 来源标签：*数据来源: iFinD/Tushare/AkShare*

### 2. 市场信息
- 最新股价、52周高低、PE(TTM)、PB、总市值、股息率
- 来源标签：*数据来源: Tushare*

### 3. 近10年月K线图
- 月度收盘价走势
- 价格区间（最高/最低）
- 成交额柱状图
- Zigzag趋势线（8%阈值识别转折点）
- 统计最高最低价标注

### 4. 近10年财务数据表格

| 指标 | 说明 |
|------|------|
| 每股营收(元) | 年度营收 / 总股本 |
| 每股现金流(元) | 经营现金流 / 总股本 |
| 每股盈利(元) | EPS |
| 每股派息(元) | 年度分红 |
| 每股净资产(元) | BPS |
| 毛利率(%) | (营收-成本)/营收 |
| 净利润率(%) | 净利润/营收 |
| 主营收入(亿元) | 年度营业收入 |
| 净利润(亿元) | 年度净利润 |
| 库存(亿元) | 资产负债表库存项 |

表格列：各自然年（2016-2025），历史数据在左侧，最新年份在右侧

### 5. 股东结构
- 控股股东、前五大股东表格（名称+持股比例）

### 6. 近期主要新闻
- 近30天重要新闻（来源：iFinD 新闻服务）

### 7. 数据来源汇总表
- 汇总所有数据类型及实际使用的数据源

## 资源文件

### scripts/

| 文件 | 功能 |
|------|------|
| `onepager.py` | 主流程（数据获取→图表→Markdown→PDF） |
| `fetch_company_data.py` | 数据获取（iFinD→Tushare→AkShare降级） |
| `generate_chart.py` | 10年月K线图+Zigzag |
| `generate_markdown.py` | Markdown报告（含10年财务表格+来源标注） |
| `generate_pdf.py` | PDF生成（Google Fonts中文字体） |

### references/

| 文件 | 内容 |
|------|------|
| `data_sources.md` | 数据源优先级与字段映射 |

## 注意事项

1. **网络环境**：iFinD 和 Tushare API 需要稳定网络环境，代理可能导致超时
2. **Token 配置**：确保 iFinD/Tushare token 有效且已正确配置
3. **数据完整性**：脚本会验证数据完整性，不足时会明确提示而非"待补充"
4. **降级机制**：高优先级数据源失败时自动降级到下一级
5. **中文支持**：PDF 使用 Google Fonts (Noto Sans SC)，无需本地中文字体

## 安装依赖

```bash
pip install tushare akshare matplotlib numpy requests weasyprint markdown
```