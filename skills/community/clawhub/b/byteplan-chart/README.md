# BytePlan Chart - BytePlan AI 图表生成技能

通过 BytePlan AI 接口自动生成数据可视化图表，支持 12 种图表类型。

## 📦 依赖安装

### 第一步：创建虚拟环境

**Windows**:
```bash
cd C:\Users\wangshuai\.openclaw\skills\byteplan-chart
uv venv
```

**macOS / Linux**:
```bash
cd ~/.openclaw/skills/byteplan-chart
uv venv
```

### 第二步：安装 Python 包

```bash
uv pip install requests python-dotenv pycryptodome matplotlib numpy
```

**依赖包说明**：
- `requests` - HTTP 请求
- `python-dotenv` - 环境变量管理
- `pycryptodome` - RSA 加密
- `matplotlib` - 图表渲染
- `numpy` - 数值计算

### 🍎 macOS 特别说明

- **系统要求**: macOS 10.15+ (Catalina 或更高版本)
- **Python 版本**: Python 3.8+ (推荐使用 uv 管理)
- **中文字体**: 自动使用 PingFang SC（苹方）或 Heiti SC（黑体）
- **权限**: 如遇权限问题，运行 `chmod +x main.py render_chart.py`

## 🔧 配置说明

### 环境变量（`.env` 文件）

```bash
# BytePlan API 配置
BYTEPLAN_BASE_URL=https://uatapp.byteplan.com
BYTEPLAN_AUTH_USER=PC
BYTEPLAN_AUTH_PASS=你的认证密码

# 登录参数
BYTEPLAN_USERNAME=你的用户名
BYTEPLAN_PASSWORD=你的密码（会自动 RSA 加密）
BYTEPLAN_GRANT_TYPE=password
BYTEPLAN_SCOPE=write

# AI 配置
BYTEPLAN_AGENT_ID=Agent ID（可选，留空则自动生成）
BYTEPLAN_PAGE_CODE=AI_REPORT

# 图表配置
CHART_WIDTH=800
CHART_HEIGHT=600
CHART_OUTPUT_DIR=charts
```

## 🚀 使用方法

### 命令行

```bash
cd C:\Users\wangshuai\.openclaw\skills\byteplan-chart
uv run python main.py <查询内容>
```

### 示例

```bash
# 查询不同分数段学生数量
uv run python main.py 查询不同分数段学生数量

# 查看不同性别分数段分布
uv run python main.py 查看不同性别分数段分布

# 生成双轴图
uv run python main.py "在运营计划分析模型中按采购成本对商品分组，展现每组平均采购成本和每组商品数量，生成双轴图表"
```

## 📊 支持的图表类型

### 全部支持（12 种）✅

| 类型 | 说明 | 状态 |
|------|------|------|
| Line | 折线图 | ✅ |
| Column | 柱状图（支持分组/堆叠） | ✅ |
| Bar | 条形图 | ✅ |
| Area | 面积图 | ✅ |
| Pie | 饼图 | ✅ |
| Rose | 南丁格尔玫瑰图 | ✅ |
| Scatter | 散点图 | ✅ |
| Box | 箱型图 | ✅ |
| Heatmap | 热力图 | ✅ |
| DualAxisChart | 双轴图（柱状图 + 折线图） | ✅ |
| DetailTable | 明细表 | ✅ |
| PivotTable | 透视表 | ✅ |

**测试时间**: 2026-03-13  
**测试结果**: 12/12 通过 ✅

## 🔧 修复记录

### 2026-03-13 修复

1. **main.py** - 修复渲染脚本调用命令
   - 问题：使用 `py` 命令在虚拟环境中找不到 matplotlib
   - 修复：改为 `uv run python` 确保在虚拟环境中运行
   - 位置：第 473 行

2. **render_chart.py** - 修复参数检查
   - 问题：`len(sys.argv) < 4` 检查错误
   - 修复：改为 `len(sys.argv) < 3`（脚本名+JSON+ 输出路径）
   - 位置：第 607 行

3. **依赖安装** - 添加必要的 Python 包
   - 创建虚拟环境：`uv venv`
   - 安装依赖：`uv pip install requests python-dotenv pycryptodome matplotlib numpy`

## 🎨 渲染方案

**当前使用：matplotlib（纯 Python）**

| 特性 | 说明 |
|------|------|
| **渲染引擎** | matplotlib 3.10+ |
| **字体处理** | 自动检测系统字体并配置 |
| **支持平台** | Windows / macOS / Linux |
| **输出格式** | PNG（150 DPI） |

### 字体检测

渲染时自动执行：
1. 检测操作系统
2. 查找预装中文字体
3. 配置 matplotlib 字体参数
4. 输出检测日志

**支持的字体**：
- Windows: Microsoft YaHei（微软雅黑）、SimHei（黑体）、SimSun（宋体）
- macOS: PingFang SC（苹方）、Heiti SC（黑体）
- Linux: WenQuanYi Zen Hei（文泉驿）、Noto Sans CJK

**如遇到中文乱码**：
```bash
# Linux 安装字体
sudo apt-get install fonts-wqy-zenhei fonts-noto-cjk  # Ubuntu/Debian
sudo yum install wqy-zenhei-fonts google-noto-sans-cjk-fonts  # CentOS/RHEL
```

## 📁 输出

- **图表文件**: `charts/antv_chart_YYYYMMDD_HHMMSS.png`
- **控制台输出**: 完整的 API 响应和图表信息

## 🔍 工作流程

1. 🔑 请求公钥接口获取 RSA 公钥（含 keyId 和 key）
2. 🔐 使用公钥对密码进行 RSA 加密
3. 🔑 使用加密后的密码和 keyId 登录获取 access_token
4. 📡 调用 AI 接口识别 model_code
5. 📊 执行 AI 分析请求获取图表数据
6. 🎨 使用 **matplotlib** 渲染图表为 PNG（**纯 Python 方案，自动检测中文字体**）

## ⚠️ 安全提示

- `.env` 文件包含敏感信息，请勿提交到版本控制
- 建议将 `.env` 添加到 `.gitignore`
- 定期更新 API 凭证

## 📝 验证安装

```bash
cd C:\Users\wangshuai\.openclaw\skills\byteplan-chart
uv run python test_render.py
```

查看输出：
```
🔍 检测系统中文字体...
✅ 找到中文字体：Microsoft YaHei
✅ 字体配置成功：Microsoft YaHei
✅ 图表已保存：charts/test_dual_axis.png
```
