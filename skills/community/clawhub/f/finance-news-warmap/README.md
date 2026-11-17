# finance-news-warmap

> 金融 / 行业「新闻作战地图」构建 Skill —— Palantir 风格、可离线双击打开的单文件 HTML 生成器。

把真实搜索到的新闻按城市经纬度落点，生成一张 Palantir 风格的作战地图：ECharts 地理散点 + 中国/世界切换 + 可筛选可悬停 + 右侧数据驱动的「建议区」。配套 `search → compile → fill` 流水线，自动把每个细分领域补满 N 条**真实**新闻并去重，**绝不编造数据**。

---

## 它能做什么

- **真实新闻地图**：每个细分方向搜满目标条数（默认 5 条）的真实国内新闻，按城市经纬度在地图上落点。
- **离线单文件 HTML**：echarts 库 + 世界/中国 GeoJSON + 新闻数据 + 建议区 JSON **全部内联**，双击即开、可邮件分享。
- **数据驱动「建议区」**：基于当前新闻实时统计趋势，并给指定角色/视角的高管生成可执行建议（默认「金融高管视角」，任意角色可经 `--role` 固化）。
- **去重幂等**：已存在新闻按 `norm_key` 去重，合并时 existing 在前，绝不重复存储。

---

## 触发场景

- 做新闻情报地图 / 作战地图 / 创新动态地图
- 搜新闻自动补满、去重并入
- 给高管出「趋势 + 建议」面板
- 要离线自包含 HTML 交付物

---

## 工作流（端到端）

```
〇 环境前置检查（Gate）：先探测 WebSearch 是否可用，不支持则立即中止，不编造
① 定义分类法 TAXONOMY（唯一真理源）
② 搜索真实新闻（默认最近一周 d7，不询问）
③ 编译成 JSON（13 字段，event/why/innovation/learn 各 ≥100 字）
④ 去重并入（pipeline.py fill）
⑤ 查缺口 → 补满（pipeline.py status / fill 循环）
⑥ 重建单文件 HTML（build.py build）
⑦ 校验交付（占位符无残留、JSON 合法、每子方向计数）
```

### 调用前需确认的问题（Question Flow）

| # | 问题 | 默认 | 处置 |
|---|---|---|---|
| 1 | 关注领域 / 分类法 | 银行10 + 金融科技5 + 保险5 = 20 子方向 | 不询问 |
| 2 | 每方向填满几条 | 5 | 不询问 |
| 3 | 时间窗口 | 最近一周（d7） | **不询问** |
| 4 | 地理范围 | 中国为主 | 不询问 |
| 5 | 新闻来源 / 语言 | 国内官媒 + 主流财经 | 不询问 |
| 6 | **你是什么角色 / 视角？** | 无 | **必问**（经 `--role` 固化，不在浏览器输入） |
| 7 | 视觉风格 | Palantir 深色三栏 | 不询问 |
| 8 | 长字段 ≥100 字 | 是 | 不询问 |
| 9 | 输出位置 / 文件名 | 默认名 + news.xlsx | 不询问 |
| 10 | 定时自动刷新 | 手动 | 不询问 |

> 真正要用户拍板的只有 **#6 角色**；其余用默认值直接跑。

---

## 环境准备（Setup）

```bash
# 1. 安装依赖（核心只需 openpyxl；supabase 仅 pull/push 时需要）
pip install -r requirements.txt

# 2. 在你自己的项目目录里运行（数据与产物写到「当前工作目录」，不污染技能安装目录）
cd your-project-dir
python references/build.py init     # 用内置示例生成 news.xlsx（可编辑数据源）
python references/build.py build    # 读 news.xlsx -> 生成离线单文件 HTML 到当前目录

# 跳过 init 直接 build 也行（缺 news.xlsx 时自动回退内置示例）
python references/build.py build --role "浙江省分行行长"   # 指定建议区视角并固化进 HTML
```

> 只读资产（`template.html` / `assets/` / `news_sample.json`）已随仓库分发，无需联网下载。

---

## 文件结构

```
finance-news-warmap/
├── SKILL.md              # 方法论总结（何时用 / 硬规则 / 架构 / 工作流 / 关键代码模式 / 坑）
├── README.md
├── requirements.txt      # 依赖：openpyxl（核心）/ supabase（可选）
├── .gitignore
└── references/
    ├── template.html     # Palantir 风三栏地图模板（占位符、中国/世界切换、右侧建议区）
    ├── build.py          # 生成器（init/build/merge/replace + 建议区计算 + 去重）
    ├── pipeline.py       # 20 子领域 taxonomy 驱动的 search/status/fill/rebuild 补满流水线
    ├── news_sample.json  # 内置示例数据源（11 条，init/build 缺 xlsx 时回退用）
    ├── db.py             # Supabase 读写（可选，pull/push 用；凭据走本地 config.toml）
    ├── config.example.toml
    └── assets/           # 离线单文件必需，已随仓库分发
        ├── echarts.min.js
        ├── world.json
        └── china.json
```

---

## 硬规则（默认开启，除非用户明确授权跳过）

1. **环境前置 Gate**：调用时第一步探测 `WebSearch` 是否可用；不支持则立即中止整个流程，绝不退化为编造或离线占位。
2. **只用真实新闻**：全部来自 WebSearch（默认 freshness=`d7`），绝不编造、绝不虚构事件/链接。
3. **每细分领域搜满目标条数**（默认 TARGET=5）：不足只报缺口，不编造占位补齐。
4. **长字段写足**：`event / why / innovation / learn` 各 ≥ 100 字（必须在 fill 前补全，去重保首次）。
5. **离线单文件**：echarts 库与 world/china GeoJSON 全内联。
6. **去重不重复**：已存在新闻按 `norm_key` 去重，合并时 existing 在前。

---

## 关键代码模式

- `norm_key(n)`：链接去 `?#.*$` 转小写优先，否则标题去空格 —— 稳定去重主键。
- `dedup(news, keep_first=True)`：按 `norm_key` 保留首次出现。
- `build_suggestions(news, role)`：build 时实时计算概览 / 趋势 Top6 / 单一角色建议块。
- 占位符替换 + `assert` 无残留：保证离线单文件完整。
- 光点按时间错落闪烁（非齐闪）；大体积 GeoJSON 解析后置，提速首屏。

---

## 在 WorkBuddy 中使用

1. 将本仓库内容放入 `~/.workbuddy/skills/finance-news-warmap/`（或项目级 `.workbuddy/skills/`）。
2. 调用该 Skill，按 Question Flow 回答必要项（角色必问）。
3. Skill 自动执行 search → compile → fill → build，产出 `金融创新全球作战地图.html` + `news.xlsx`。

---

## 联系方式

- **邮箱**：zhenshida@foxmail.com
- **交流群（QQ）**：1037432340

---

> ⚠️ 本 Skill 强制「真实新闻、不编造、去重不重复、离线单文件」四条底线，请勿用于生成虚假情报或误导式可视化。
