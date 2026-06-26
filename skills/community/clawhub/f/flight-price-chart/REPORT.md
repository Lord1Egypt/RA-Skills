# Price Trend Skill 技术报告

## 一句话介绍

这是一个可以嵌入到 AI 对话中的**价格趋势图表组件**，当 AI 给用户推荐航班时，会在回答末尾自动展示一个可交互的 60 天价格走势图，帮助用户判断当前价格是贵还是便宜、是买入还是观望。使用方式：在 AI/Agent 项目中引入这个组件，当 AI 输出包含航班推荐时，调用组件渲染即可。

---

## 项目概述

**Price Trend Skill** 是一个专为 AI/Agent 开发场景设计的前端组件 Skill，用于在 AI 对话中嵌入交互式价格趋势可视化模块。

### 核心功能
- 展示 60 天历史价格走势
- 实时交互（hover/touch 查看每日价格）
- 价格水位分析（低于/高于均价）
- 趋势判断（上涨/下降/平稳）
- 统计数据显示（最低/平均/最高价）

### 应用场景
当 AI 助手回答中包含**确定 OD（Origin-Destination）的航班推荐**时，在对话末尾自动添加价格趋势模块。

---

## 目录结构

```
price-trend/
├── SKILL.md                          # Skill 元数据和使用说明
├── README.md                         # 快速入门指南
├── USAGE_EXAMPLE.md                  # AI/Agent 集成示例
├── IMPLEMENTATION_STATUS.md          # 实现状态和待办事项
├── REPORT.md                         # 本文件 - 技术报告
├── references/
│   ├── README.md                     # 参考文档索引
│   ├── configure-serpapi.md          # SerpAPI 配置指南
│   ├── data-sources.md               # 数据源方案说明
│   ├── price-api.md                  # API 数据格式文档
│   ├── price-analysis.md             # 价格分析算法文档
│   └── price-chart-component.md      # 组件 API 文档
└── components/
    ├── PriceTrendEmbed.html          # 纯 HTML/JS 版本（独立演示）
    └── PriceTrendEmbed.jsx           # React 组件版本
```

---

## 文件详解

### 1. `SKILL.md`
**作用**：Skill 的元数据定义和使用说明，供 AI Agent 系统读取和识别。

**主要内容**：
- Skill 名称、描述、版本号
- 触发模式（patterns）：匹配价格趋势、航班推荐等关键词
- 组件 API 文档：`PriceChart` 组件的 props 定义
- 数据结构说明：priceHistory、analysis、destination 的格式
- 使用场景示例：航班搜索后、价格查询、购买建议

**适用对象**：AI Agent 系统、开发者

---

### 2. `README.md`
**作用**：快速入门指南，帮助开发者快速上手集成。

**主要内容**：
- 快速配置 SerpAPI 获取真实数据（3 步完成）
- 数据流说明（配置前后的区别）
- 置信度标识说明（根据数据天数显示不同文案）
- 集成方式（React / 纯 HTML）
- 与 flyai 配合使用的示例

**适用对象**：首次接触此 Skill 的开发者

---

### 3. `USAGE_EXAMPLE.md`
**作用**：提供 AI/Agent 集成的完整代码示例和对话模板。

**主要内容**：
- 三种典型场景的代码示例：
  1. 航班推荐后自动添加价格趋势
  2. 用户询问价格走势
  3. 购买建议生成
- 完整对话示例（用户-AI 交互流程）
- 前端集成代码（React 组件 / 纯 HTML）
- 注意事项

**适用对象**：正在集成此 Skill 的前端/全栈开发者

---

### 4. `IMPLEMENTATION_STATUS.md`
**作用**：记录当前实现状态、待办事项和数据源说明。

**主要内容**：
- 已完成功能清单（组件、文档、Skill 注册）
- 数据源状态说明（当前使用模拟数据）
- 获取真实数据的实施路径（3 个阶段）
- 推荐下一步行动
- 文件清单

**适用对象**：项目维护者、技术决策者

---

### 5. `references/README.md`
**作用**：参考文档的索引页，帮助开发者快速找到所需文档。

**主要内容**：
- 快速开始链接（SerpAPI 配置）
- 文档索引表格（5 个参考文档的说明和适用人群）
- 使用场景导航
- 相关文件链接

**适用对象**：所有开发者

---

### 6. `references/configure-serpapi.md`
**作用**：指导开发者配置 SerpAPI 以获取真实航班价格数据。

**主要内容**：
- SerpAPI 注册流程（https://serpapi.com/users/sign_up）
- API Key 配置方法（修改 `price/config.json`）
- 数据流说明（配置前后对比）
- 价格数据收集机制
- 置信度说明（数据天数与 AI 文案的关系）
- 常见问题解答

**适用对象**：需要接入真实数据的开发者

---

### 7. `references/data-sources.md`
**作用**：详细说明价格数据的来源方案和实施策略。

**主要内容**：
- 现状分析（当前使用模拟数据）
- 数据源选项对比：
  - 方案 1：SerpAPI + 自建缓存（推荐）
  - 方案 2：第三方 API（AviationStack、Amadeus 等）
  - 方案 3：混合方案
- 推荐实施路径（3 个阶段）
- 数据存储方案（JSON 文件 / SQLite）
- AI Agent 集成时的注意事项

**适用对象**：架构师、技术决策者

---

### 8. `references/price-api.md`
**作用**：定义价格趋势 API 的接口规范和数据格式。

**主要内容**：
- API 端点和参数（origin、destination、days）
- 请求示例
- 响应格式（priceHistory、lowestPrice、priceLevel、analysis）
- 字段详细说明
- 错误响应格式
- 数据覆盖率和更新频率
- 集成示例代码（JavaScript / Python）
- 数据转换函数（API 响应 → Chart Props）

**适用对象**：后端开发者、API 集成人员

---

### 9. `references/price-analysis.md`
**作用**：详细说明价格分析的算法逻辑和推荐策略。

**主要内容**：
- 价格水位分类（百分位法：33%/67% 分位）
- 趋势检测算法（7 日移动平均对比）
- 购买/等待推荐逻辑（决策矩阵）
- 统计计算方法（平均、百分比差异、价格区间）
- 置信度评分算法
- 示例分析（输入/输出）
- 边缘情况处理（数据不足、缺失价格、极端异常值）

**适用对象**：算法工程师、数据分析师

---

### 10. `references/price-chart-component.md`
**作用**：PriceChart 组件的详细 API 文档。

**主要内容**：
- 组件概览
- Props 详细说明（data、currentPrice、analysis、destination）
- AnalysisResult 类型定义
- 使用示例代码
- 视觉结构图（ASCII 布局图）
- 功能特性（交互 tooltip、平均线、价格水位徽章、统计脚注）
- CSS 变量定义
- 响应式行为
- 可访问性支持
- 性能考虑

**适用对象**：前端开发者

---

### 11. `components/PriceTrendEmbed.html`
**作用**：纯 HTML/JS 版本的独立演示文件，可在浏览器中直接打开查看效果。

**主要内容**：
- 完整的 HTML 结构
- 内联 CSS 样式（所有样式变量和组件样式）
- JavaScript 实现：
  - `fmtDateShort()` / `fmtDate()` - 日期格式化
  - `calculateTrend()` - 趋势计算
  - `convertPriceInsights()` - 数据转换函数
  - `renderPriceChart()` - 图表渲染主函数
  - 交互逻辑（鼠标 hover / 触摸滑动）
- 真实 60 天价格数据（来自 SerpAPI）
- 演示页面 UI（标题、说明、代码块）

**技术特点**：
- 无需构建工具，直接打开即可演示
- SVG 图表绘制（渐变填充、平滑曲线）
- 响应式设计（适配移动端）
- 触摸交互支持

**适用对象**：所有开发者、产品经理、设计师

**使用方式**：
```bash
# 直接在浏览器打开
open components/PriceTrendEmbed.html

# 或使用本地服务器
python3 -m http.server 8000
# 访问 http://localhost:8000/components/PriceTrendEmbed.html
```

---

### 12. `components/PriceTrendEmbed.jsx`
**作用**：React 版本的组件，用于集成到 React 项目中。

**主要内容**：
- 样式对象定义（CSS-in-JS）
- 工具函数：
  - `fmtDateShort()` / `fmtDate()` - 日期格式化
  - `convertPriceInsights()` - 数据转换函数（导出）
- `PriceChart` React 组件（导出）：
  - Props：data、currentPrice、analysis、destination
  - 使用 `useMemo` 优化路径计算
  - 使用 `ResizeObserver` 响应式尺寸
  - 使用 `useCallback` 优化交互函数
  - SVG 图表渲染
  - 交互状态管理（hover）
- 默认导出

**技术特点**：
- ES6 模块导出，支持 import 引入
- React Hooks（useState、useEffect、useRef、useCallback、useMemo）
- 性能优化（memoization）
- 与 HTML 版本功能一致

**适用对象**：React 项目开发者

**使用方式**：
```jsx
import { PriceChart, convertPriceInsights } from './PriceTrendEmbed';

const chartProps = convertPriceInsights(priceInsights, searchParams);
<PriceChart {...chartProps} />
```

---

## 技术栈

| 技术 | 用途 |
|------|------|
| HTML5 / CSS3 | 基础结构和样式 |
| JavaScript (ES6+) | 交互逻辑和数据处理 |
| React 18+ | 组件框架（JSX 版本） |
| SVG | 图表绘制 |
| ResizeObserver | 响应式尺寸检测 |

**无外部依赖**：HTML 版本不需要任何构建工具或 npm 包。

---

## 数据流

```
用户查询
    ↓
AI Agent 检测航班推荐意图
    ↓
调用航班搜索 API（SerpAPI / FlyAI）
    ↓
获取航班列表 + 价格数据
    ↓
存储价格快照（用于历史数据积累）
    ↓
调用 convertPriceInsights() 转换数据
    ↓
渲染 PriceChart 组件
    ↓
AI 响应 = 航班卡片 + 价格趋势图 + 购买建议
```

---

## 当前状态

### ✅ 已完成
- [x] React 组件版本
- [x] 纯 HTML 演示版本
- [x] 完整文档（8 个文档文件）
- [x] Skill 注册（符号链接）
- [x] 真实数据示例（60 天 SerpAPI 数据）
- [x] 交互功能（hover/touch）
- [x] 响应式设计

### ⚠️ 注意事项
- 当前默认使用**模拟数据**（仅供 Demo/开发）
- 需配置 SerpAPI Key 获取真实数据
- 建议开始积累真实价格数据（每次搜索后存储）

---

## 快速开始

### 1. 查看演示
```bash
open components/PriceTrendEmbed.html
```

### 2. 配置真实数据
编辑 `price/config.json`：
```json
{
  "serpapi": {
    "apiKey": "你的 SerpAPI Key"
  }
}
```

### 3. 集成到项目
```bash
# 复制组件文件到你的项目
cp components/PriceTrendEmbed.jsx your-project/src/components/
```

```jsx
import { PriceChart, convertPriceInsights } from './PriceTrendEmbed';

// 在 AI 响应渲染中使用
const chartData = convertPriceInsights(priceInsights, searchParams);
<PriceChart {...chartData} />
```

---

## 联系方式

如有疑问，请参考文档或联系开发团队。
