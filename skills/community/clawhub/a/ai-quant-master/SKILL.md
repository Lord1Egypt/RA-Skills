# AI全栈量化 Master Skill

> 基于B站「教育量化站」AI全栈量化8集系列视频整理的完整技能包
> 涵盖：QMT数据获取 → 因子加工 → 回测分析 → AI因子框架 → OpenClaw部署 → 多智能体架构 → 实盘交易

---

## 技能简介

本技能提供一套完整的AI量化交易解决方案，通过8集系列视频的系统讲解，覆盖从数据准备、因子研究、回测分析到多智能体实盘交易的全流程。

### 核心能力

- **QMT数据获取**：从QMT获取历史/实时行情数据
- **因子加工**：使用pandas/TALib加工因子宽表
- **数据库存储**：QuestDB时序数据库配置与写入
- **因子回测**：Backtrader框架，IC/IR/T值分析
- **AI因子框架**：Kimi+Trae对话式因子研究
- **OpenClaw部署**：全平台安装、飞书机器人配置
- **多智能体架构**：主Agent+5个子Agent协作
- **实盘交易**：QMT API下单、定时任务

---

## 适用场景

1. 散户/新手学习量化交易全流程
2. 使用QMT进行A股量化策略开发
3. 利用AI辅助因子挖掘与策略优化
4. 搭建多智能体量化投研团队
5. 实现7×24小时自动化量化交易

---

## 快速开始

### 环境要求

- Python 3.8+ (推荐3.10+)
- QMT客户端（用于获取行情数据）
- Linux服务器或本地Windows/Mac
- 飞书账号（用于机器人配置）

### 核心工具栈

| 工具 | 用途 | 费用 |
|------|------|------|
| QMT（迅投） | A股行情数据获取/实盘下单 | 免费（券商提供） |
| QuestDB | 时序数据库存储因子 | 免费版足够 |
| Backtrader | 量化回测框架 | 免费开源 |
| TALib | 技术指标计算 | 免费 |
| OpenClaw | 多智能体框架 | 开源免费 |
| 飞书 | 消息交互/机器人 | 免费 |

---

## 安装步骤

### 第一步：QMT安装

1. 联系券商客户经理获取QMT客户端
2. 安装后登录，启用「极速交易」权限
3. 获取API接口文档（迅投官网）

### 第二步：QuestDB安装

```bash
# Windows（本地）
# 1. 从GitHub下载：https://github.com/questdb/questdb/releases
# 2. 解压到本地目录（如 D:\questdb）
# 3. Shift+右键打开PowerShell窗口

# 启动QuestDB
java -p questdb.jar -m io.questdb.server.ServerMain \
  -d /path/to/data

# 访问 http://localhost:9000 查看Web控制台
# 连接端口：HTTP 9000，PGwire 8812，TCP ILP 9009
```

### 第三步：安装OpenClaw

```bash
# Windows (PowerShell 管理员模式)
# 要求：Node.js >= 22

iwr https://raw.githubusercontent.com/openclaw/openclaw/main/install.ps1 -UseBasicParsing | iex

# 安装完成后按引导配置：
# 1. 同意风险提示
# 2. 选择 Quick Start 快速安装
# 3. 配置大模型（推荐Kimi或阿里通义）
# 4. 配置飞书机器人（见飞书配置章节）
```

```bash
# Linux服务器
npm install -g openclaw
openclaw gateway start

# 或使用官方一键部署
curl -fsSL https://openclaw.sh/install.sh | bash
```

### 第四步：安装Python依赖

```bash
# 推荐使用UV管理Python环境
pip install uv

# 创建项目环境
uv venv quant_env
source quant_env/bin/activate  # Linux/Mac
# quant_env\Scripts\activate  # Windows

# 安装核心依赖
uv pip install pandas numpy akshare backtrader ta-lib
```

---

## 模块详细说明

### 模块一：QMT数据获取

**功能**：获取A股历史K线、财务数据、板块信息

**核心代码示例**（见 `examples/qmt-api-example.py`）

```python
# 基础数据获取模板
import pandas as pd

# QMT数据结构
# 订阅行情：subscribe_quote(symbols)
# 获取历史：get_history_data(symbol, period, start, end)
# 账户查询：get_account_info()
```

**注意事项**：
- API token需妥善保管，切勿外泄
- 建议将token存放在配置文件中
- 历史数据建议先存储到本地再处理

---

### 模块二：因子加工与存储

**流程**：QMT数据 → 因子计算 → 宽表整理 → QuestDB存储

**因子类型示例**：
- 量价因子：OBV能量潮、MFI资金流量、EMV波动指标
- 趋势类：MFI、EMV、VAD威廉变异量
- 反转类：VPT量价趋势、KDJ
- 情绪类：VR成交量比率、VRO3

**QuestDB存储**：

```sql
-- 创建因子宽表
CREATE TABLE factor_wide_table (
    symbol STRING,
    trade_date TIMESTAMP,
    obv DOUBLE,
    mfi DOUBLE,
    emv DOUBLE,
    mom DOUBLE,
    rsi DOUBLE,
    close DOUBLE,
    volume DOUBLE
) TIMESTAMP(trade_date) PARTITION BY DAY;

-- 插入数据
INSERT INTO factor_wide_table VALUES ...
```

---

### 模块三：因子回测

**核心指标**：
- **IC（信息系数）**：因子排序与未来收益排序的相关性
- **IR（信息比率）**：IC均值/IC标准差，衡量稳定性
- **T值**：IC均值/标准误，显著性检验（<0.05显著）

**调仓频率建议**：
- 不建议每日调仓，过于频繁
- 推荐5天/周度/月度调仓
- 选股数量20-30只效果较优

**注意事项**：
- 使用前一天因子值选股，用当天收益计算（避免未来函数）
- T+1交易：用前一天收盘后因子值，次日开盘价交易

---

### 模块四：AI因子框架

**工具**：Kimi（代码生成）+ Trae（本地IDE）

**6步操作流程**：
1. 向Kimi描述需求，生成量化引擎代码
2. 用Trae打开代码并优化
3. 用UV创建Python环境
4. 阅读AI生成的使用说明书
5. 按说明书执行策略
6. 用AI继续优化和修改

```bash
# Kimi生成代码示例需求：
# "请给我生成一个量化引擎代码，包括因子处理、因子检验和因子回测"

# Trae本地环境配置
uv init ai_quant
cd ai_quant
uv add pandas numpy backtrader akshare
uv run python main.py
```

---

### 模块五：OpenClaw Skills技能系统

**技能市场**：https://clawhub.com（每日增长大量新技能）

**安装技能**：
```bash
# 通过OpenClaw CLI安装
openclaw skills install <skill-name>

# 或手动下载skill包到 ~/.openclaw/workspace/skills/
```

**自定义技能开发**：
- 每个技能包含 `SKILL.md` 主文档
- 技能目录结构：主文档 + references/ + examples/
- 技能可组合生成新的复合技能

---

### 模块六：飞书机器人配置

**完整配置流程**：

1. **创建企业自建应用**：飞书开放平台 → 创建应用 → 添加「机器人」能力

2. **配置权限**：权限管理 → 批量导入权限（参考 `feishu-permissions.json`）

3. **安装飞书插件**：
```bash
# 在OpenClaw安装目录执行
git clone https://github.com/openclaw/feishu-plugin.git
cd feishu-plugin
npm install
```

4. **配置插件**（三条命令）：
```bash
openclaw config set channel.feishu.appId <APP_ID>
openclaw config set channel.feishu.appSecret <APP_SECRET>
openclaw channel connect
```

5. **配置事件回调**：添加基础事件 → 配置回调URL → 开启「使用长连接」

6. **发布版本**：创建版本 → 提交审核 → 等待审批通过

---

### 模块七：多智能体架构

**5个子Agent分工**：
1. **研究Agent**：市场信息、数据获取
2. **选股Agent**：标的筛选、因子排名
3. **策略Agent**：组合配置、权重分配
4. **风控Agent**：风险监控、仓位管理
5. **执行Agent**：交易执行、委托下单

**架构特点**：
- 主Agent负责任务分发与协调
- 各子Agent独立工作空间（避免冲突）
- 通过飞书群作为协作载体
- 通过AGENT.md文档定义工作流程

**创建子Agent**：
```bash
openclaw agent create <agent-name>
openclaw agent reset
```

**关键配置**：在 `~/.openclaw/openclaw.js` 中配置路由和绑定

---

### 模块八：盘中定时任务与OPC模式

**定时任务配置**：
- 建议15分钟执行一次
- 关闭深度思考（节省token）
- 开启Light Context模式

**因子评分系统**：
- 程序分值 + 趋势分值 + 强势判断
- 通过固定文件（如CSV/TXT）传递信号
- Agent读取文件后进行综合判断

**OPC模式（One Person Company）**：
- 个人借助AI Agent实现高效运营
- 7×24小时自动运行
- 飞书推送实时报告

---

## 常见问题

### Q1: QuestDB启动失败？
- 检查Java环境：`java -version`
- 确认端口9000未被占用
- 查看日志文件排查具体错误

### Q2: QMT数据获取失败？
- 确认QMT客户端已登录
- 检查API Token是否有效
- 网络代理是否影响连接

### Q3: OpenClaw连接不稳定？
- 检查服务器网络状态
- 确认API Key额度充足
- 尝试重启Gateway

### Q4: 多智能体消息路由失败？
- 确认飞书机器人已发布且审核通过
- 检查群组会话ID是否正确配置
- 确认每个Agent的绑定信息准确

### Q5: 因子回测结果与实盘差异大？
- 避免使用当天因子值计算当天收益（T+1问题）
- 考虑交易滑点和手续费
- 检查是否存在未来函数

---

## 注意事项

1. **QMT Token安全**：切勿将实盘API Token上传至公网
2. **回测≠实盘**：回测结果仅供参考，实盘需考虑滑点、流动性
3. **调仓频率**：不建议过于频繁，降低交易成本是关键
4. **AI输出质量**：AI生成的代码需审核后再使用
5. **多智能体成本**：合理配置思考深度，避免token过度消耗
6. **数据来源**：优先使用券商提供的QMT数据，确保完整性

---

## 相关技能

- `akshare-stock`：A股量化数据分析
- `backtest-expert`：交易策略回测指导
- `feishu-im-read`：飞书消息读取
- `market-sentiment`：市场情绪量化
