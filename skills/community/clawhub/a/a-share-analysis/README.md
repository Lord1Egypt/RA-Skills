# A 股分析系统 - 完整使用说明

**版本**: v2.8 专业版  
**更新日期**: 2026-03-01  
**作者**: A 股专业分析系统

---

## 📖 目录

1. [系统简介](#系统简介)
2. [快速开始](#快速开始)
3. [功能特性](#功能特性)
4. [安装部署](#安装部署)
5. [使用方法](#使用方法)
6. [报告说明](#报告说明)
7. [配置说明](#配置说明)
8. [常见问题](#常见问题)
9. [技术支持](#技术支持)

---

## 系统简介

A 股分析系统是一套专业的股票分析工具，提供：

- 📊 **实时行情** - 新浪财经 API（带重试机制）
- 🔧 **技术分析** - 东方财富 API（免费数据源）
- 📰 **新闻情绪** - Firecrawl 网页抓取（可选）
- 🧠 **历史记忆** - Elite Memory 存储
- 📝 **专业报告** - Markdown/PDF 格式
- 📄 **详细报告** - 6-8 页详细分析
- 💼 **商业报告** - 可商用专业报告

---

## 快速开始

### 环境要求

- Python 3.8+
- Windows/Linux/macOS
- 网络连接

### 安装依赖

```bash
pip install requests reportlab
```

### 第一个分析

```bash
cd C:\Users\fj\.openclaw\workspace\skills\a-share-analysis\scripts

# 分析单只股票
python analyze_stock_pro.py 600519 贵州茅台
```

### 输出示例

```
======================================================================
A 股专业分析系统
======================================================================
分析标的：贵州茅台 (600519)
分析时间：2026-03-01 12:30:00
======================================================================

[1/6] 获取实时行情...
[OK] 贵州茅台：1455.02 (-0.76%)

[2/6] 技术分析（东方财富免费 API）...
[OK] 信号：neutral | 趋势：neutral
[OK] 支撑：1455.02 | 阻力：1568.00

[3/6] 新闻情绪分析 (Firecrawl)...
[!] Firecrawl 未认证，使用简化分析

[4/6] 历史分析回顾 (Elite Memory)...
[OK] 历史分析次数：3
[OK] 主要建议：观望

[5/7] 生成专业报告...
[OK] 专业版报告：...\600519_贵州茅台_*.md
[*] 正在生成详细 PDF 报告...
[OK] 详细 PDF 报告：...\600519_贵州茅台_*.pdf

[6/7] 存储分析记录...
[OK] 分析记录已存储

======================================================================
分析摘要
======================================================================
股票：贵州茅台 (600519)
价格：1455.02 (-0.76%)
技术信号：neutral
综合建议：观望
======================================================================
```

---

## 功能特性

### 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时行情 | ✅ | 新浪财经 API |
| 技术分析 | ✅ | 东方财富 API |
| 新闻情绪 | ⚠️ | Firecrawl（可选） |
| 记忆存储 | ✅ | Elite Memory |
| Markdown 报告 | ✅ | 详细文本报告 |
| PDF 报告 | ✅ | 6-8 页详细 PDF |
| 错误重试 | ✅ | 自动重试 3 次 |
| 数据缓存 | ✅ | 5 分钟 TTL |
| 日志系统 | ✅ | 文件 + 控制台 |
| 批量分析 | ✅ | 支持多股分析 |

### 报告版本

| 版本 | 章节 | 页数 | 适用场景 |
|------|------|------|----------|
| 专业版 | 10 个 | 2-3 页 | 快速查看 |
| 详细版 | 12 个 | 5-6 页 | 深度研究 |
| 商业版 | 18 个 | 8-10 页 | 商业使用 |
| PDF 详细版 | 11 个 | 6-8 页 | 专业打印 |

---

## 安装部署

### 方式一：自动安装

```bash
# 进入部署目录
cd a-share-analysis-deploy

# 运行安装脚本
python install.py
```

### 方式二：手动安装

```bash
# 1. 复制脚本
cp -r scripts/* ~/.openclaw/workspace/a-share-analysis/scripts/

# 2. 复制文档
cp docs/* ~/.openclaw/workspace/a-share-analysis/

# 3. 创建目录
mkdir -p ~/.openclaw/workspace/a-share-reports
mkdir -p ~/.openclaw/workspace/memory/a-share

# 4. 安装依赖
pip install requests reportlab
```

---

## 使用方法

### 基本用法

```bash
# 分析单只股票
python analyze_stock_pro.py 600519 贵州茅台

# 分析多只股票
python analyze_stock_pro.py 600519 贵州茅台 000858 五粮液

# 批量分析（默认股票）
python analyze_stock_pro.py --batch

# 从文件批量分析
python analyze_stock_pro.py -f stocks.txt
```

### 报告版本选择

```bash
# 专业版报告（默认）
python analyze_stock_pro.py 600519 贵州茅台

# 详细版报告
python analyze_stock_pro.py 600519 贵州茅台 --detailed

# 商业版报告
python analyze_stock_pro.py 600519 贵州茅台 --commercial

# 静默模式
python analyze_stock_pro.py 600519 贵州茅台 --quiet
```

### 命令行参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--batch` | `-b` | 批量分析模式 |
| `--file` | `-f` | 股票列表文件 |
| `--detailed` | `-d` | 详细版报告 |
| `--commercial` | `-c` | 商业版报告 |
| `--json` | `-j` | JSON 输出 |
| `--quiet` | `-q` | 静默模式 |
| `--help` | `-h` | 显示帮助 |

### 股票列表文件格式

```
600519 贵州茅台
000858 五粮液
603258 电魂网络
300750 宁德时代
```

---

## 报告说明

### 报告输出位置

```
C:\Users\fj\.openclaw\workspace\a-share-reports\
├── 600519_贵州茅台_20260301_123000_PRO.md      # 专业版
├── 600519_贵州茅台_20260301_123000_DETAILED.md # 详细版
├── 600519_贵州茅台_20260301_123000.pdf         # PDF 详细版
└── ...
```

### 报告章节

#### 专业版（10 章）
1. 报告封面
2. 核心摘要
3. 实时行情
4. 技术分析
5. 新闻情绪
6. 历史回顾
7. 投资建议
8. 风险提示
9. 数据源说明
10. 报告尾部

#### 详细版（12 章）
在专业版基础上增加：
- 重要声明（6 项）
- 投资评级（详细）
- 情景分析
- 报告附录

#### 商业版（18 章）
在详细版基础上增加：
- 公司概况
- 行业分析
- 资金流向
- 估值分析
- 详细风险提示

---

## 配置说明

### 环境变量（可选）

```bash
# OpenClaw 工作区路径
export OPENCLAW_WORKSPACE="/path/to/workspace"

# Firecrawl API 密钥（可选）
export FIRECRAWL_API_KEY="sk-xxx"
```

### 内置配置

编辑 `utils.py`:

```python
CONFIG = {
    'cache_enabled': True,      # 启用缓存
    'cache_ttl': 300,           # 缓存时间（秒）
    'max_retries': 3,           # 重试次数
    'timeout': 10,              # 请求超时（秒）
    'output_dir': 'a-share-reports',
    'memory_dir': 'memory',
}
```

---

## 常见问题

### Q1: Firecrawl 未认证？

**现象**: `[!] Firecrawl 未认证，使用简化分析`

**解决**（可选）:
```bash
npm install -g firecrawl-cli
firecrawl login --browser
```

### Q2: 中文乱码？

**解决**:
```bash
# Windows 用户
chcp 65001
```

### Q3: API 请求失败？

**解决**:
- 检查网络连接
- 重试机制已自动启用（3 次）
- 查看日志文件

### Q4: 如何查看历史分析？

**解决**:
```bash
# 查看记忆文件
cat ~/.openclaw/workspace/memory/a-share/600519.json
```

### Q5: 如何清除缓存？

**解决**:
```bash
python -c "from utils import clear_cache; clear_cache()"
```

---

## 技术支持

### 文档

| 文档 | 说明 |
|------|------|
| `README.md` | 本使用说明 |
| `DETAILED_REPORT.md` | 详细版报告说明 |
| `COMMERCIAL_REPORT.md` | 商业版报告说明 |
| `DETAILED_PDF_REPORT.md` | 详细 PDF 说明 |
| `OPTIMIZATION_IMPLEMENTED.md` | 优化实施报告 |

### 日志

```bash
# 查看分析日志
cat ~/.openclaw/workspace/analysis.log

# 实时查看
tail -f ~/.openclaw/workspace/analysis.log
```

### 系统信息

```bash
python -c "from utils import get_system_info; print(get_system_info())"
```

---

## 更新日志

### v2.8 详细 PDF 版 (2026-03-01)
- ✅ 详细 PDF 报告生成器
- ✅ 11 个详细章节
- ✅ 专业配色方案
- ✅ 6-8 页详细分析

### v2.7 详细版 (2026-03-01)
- ✅ 详细版报告生成器
- ✅ 12 个分析章节
- ✅ 情景分析
- ✅ 超详细技术分析

### v2.6 商业版 (2026-03-01)
- ✅ 商业版报告生成器
- ✅ 18 个分析章节
- ✅ 中英文双语
- ✅ 可商用免责声明

### v2.5 优化版 (2026-03-01)
- ✅ 清理冗余文件
- ✅ 修复中文编码
- ✅ 添加错误重试
- ✅ 添加数据缓存
- ✅ 添加日志系统

---

## 附录

### 文件结构

```
a-share-analysis/
├── scripts/
│   ├── analyze_stock_pro.py        # 主入口
│   ├── fetch_realtime_data.py      # 实时行情
│   ├── fetch_technical_indicators_free.py  # 技术分析
│   ├── fetch_news_sentiment.py     # 新闻情绪
│   ├── generate_report_pro.py      # 专业版报告
│   ├── generate_report_detailed.py # 详细版报告
│   ├── generate_report_commercial.py # 商业版报告
│   ├── generate_pdf_report.py      # PDF 报告
│   ├── memory_store.py             # 记忆存储
│   ├── analysis_tools.py           # 分析工具
│   ├── utils.py                    # 通用工具
│   └── firecrawl_auto_auth.py      # Firecrawl 认证
├── a-share-reports/                 # 报告输出
└── memory/a-share/                  # 股票记忆
```

### 依赖库

| 库 | 版本 | 用途 |
|------|------|------|
| requests | 2.32.5+ | HTTP 请求 |
| reportlab | 4.4.10+ | PDF 生成 |

---

**感谢使用 A 股分析系统！** 📊

**最后更新**: 2026-03-01 12:37
