---
name: ai-pm-resume-hub
description: 用于维护 AI 产品经理校招简历中枢。当用户要提炼工作日志、去重沉淀简历要点、维护要点池、生成或更新中文一页纸简历、输出 gap 清单时使用。适合触发词包括“提炼本周日志”“更新简历”“生成一页简历”“整理简历要点池”。
---

# /ai-pm-resume-hub — AI 产品经理校招简历中枢

维护固定目录下的日志、要点池和简历输出，让用户可以用短指令反复执行同一套流程。

## 固定工作区

- 默认根目录：`career/ai-pm-campus/`
- 如果目录不存在，先创建以下结构：
  - `career/ai-pm-campus/inputs/resume/`
  - `career/ai-pm-campus/inputs/experiences/`
  - `career/ai-pm-campus/inputs/worklog/`
  - `career/ai-pm-campus/inputs/points-pool/`
  - `career/ai-pm-campus/outputs/`
- 必备文件：
  - `career/ai-pm-campus/inputs/worklog/_processed-index.md`
  - `career/ai-pm-campus/inputs/points-pool/master-points.md`
  - `career/ai-pm-campus/inputs/points-pool/label-registry.md`
  - `career/ai-pm-campus/outputs/resume-outline.md`
  - `career/ai-pm-campus/outputs/resume-onepage.md`

## 触发方式

- `/ai-pm-resume-hub extract`
- `/ai-pm-resume-hub build`
- `/ai-pm-resume-hub visualize`
- `/ai-pm-resume-hub export`

如果用户只说“提炼本周日志”“整理简历要点池”，默认走 `extract`。
如果用户只说“更新简历”“生成一页简历”“输出校招简历”，默认走 `build`。
如果用户说“可视化”“仪表盘”“dashboard”“预览简历”，默认走 `visualize`。
如果用户说“导出PDF”“生成PDF”“打印简历”，默认走 `export`。

## 通用约束

- 始终先读已有文件，再写新内容，不要覆盖用户已有材料。
- 输出必须落盘写文件，不能只在聊天中给总结。
- 严禁编造指标；缺失时必须写成 `[待补数据：...]`。
- 项目标签优先复用 `label-registry.md` 中已有写法，避免标签漂移。
- 每次运行结束都在聊天中汇报：
  - 读取了哪些文件
  - 写入了哪些文件
  - 新增了多少条要点或更新了哪些简历段落
- 若发现现有文件格式与本 skill 约定不一致，优先兼容，不要粗暴重写整份文件。

## 1) extract

用于把最近一批原始工作日志转成可复用的简历要点，并追加到要点池。

### 输入

- 用户直接粘贴的日志文本
- 或 `career/ai-pm-campus/inputs/worklog/` 下尚未处理的 `.md` 文件

### 执行流程

1. 读取：
   - `career/ai-pm-campus/inputs/worklog/_processed-index.md`
   - `career/ai-pm-campus/inputs/points-pool/master-points.md`
   - `career/ai-pm-campus/inputs/points-pool/label-registry.md`
2. 如果用户是直接粘贴日志：
   - 先将原始文本保存为 `career/ai-pm-campus/inputs/worklog/manual-YYYY-MM-DD-weekly.md`
   - 若同名已存在，则追加短后缀避免覆盖
3. 如果用户没有贴文本，则扫描 `inputs/worklog/` 中未出现在 `_processed-index.md` 的 `.md` 文件
4. 对日志做信噪比过滤：
   - 忽略纯同步会议、简单 bug 修复、例行巡检、没有动作和结果的泛化表述
   - 优先保留核心功能迭代、策略优化、数据分析闭环、Prompt/评测迭代、LLM 应用落地、模型效果/成本/延迟优化、跨部门关键推进
5. 对保留内容做 STAR 重构：
   - 重写成适合简历的短句
   - 必须体现“动作 + 结果/影响”
   - 若结果缺失，显式写 `[待补数据：需补充XX]`
6. 生成或复用项目标签：
   - 优先复用 `label-registry.md`
   - 若必须新增，命名优先级：
     - `[公司名-项目/方向]`
     - `[校园项目-主题]`
     - `[课程项目-主题]`
7. 写入 `master-points.md` 时使用以下格式追加：

```markdown
## YYYY-MM-DD
### 要点 N
- 项目标签：...
- 时间：...
- STAR短句：...
- 待补数据：...
- 来源：...
```

8. 追加前做去重：
   - 与 `master-points.md` 中已有条目比较
   - 语义高度重复时不重复写入
   - 如果只是旧条目缺少来源或待补数据，可补充旧条目而不是新建重复条目
9. 更新 `_processed-index.md`，至少记录：
   - 原始日志文件名
   - 处理日期
   - 新增要点数

### 输出

- 必写文件：
  - `career/ai-pm-campus/inputs/points-pool/master-points.md`
  - `career/ai-pm-campus/inputs/worklog/_processed-index.md`
- 按需更新：
  - `career/ai-pm-campus/inputs/points-pool/label-registry.md`
- 聊天里补充简短摘要：
  - 本次新增要点数
  - 复用了哪些标签
  - 新建了哪些标签
  - 最值得优先补的 3 条数据

## 2) build

用于基于历史简历、经历材料和要点池，生成 AI 产品经理校招方向的简历。

### 输入

- `career/ai-pm-campus/inputs/resume/`
- `career/ai-pm-campus/inputs/experiences/`
- `career/ai-pm-campus/inputs/points-pool/master-points.md`
- `career/ai-pm-campus/inputs/points-pool/label-registry.md`

### 执行流程

1. 先从历史简历提取已验证信息：
   - 教育背景
   - 基础技能
   - 已有实习/项目名称
   - 已经写得足够好的 bullet
2. 再从 `master-points.md` 按“项目标签 + 时间线”归并要点，**优先突出实习经历**
3. 去重与合并：
   - 删除重复表述
   - 保留证据更强、结果更明确、动作更具体的版本
4. 按 AI 产品经理校招方向调优：
   - 强调 LLM 应用落地
   - 强调数据闭环与产品思维
   - 强调跨团队推进能力
5. 输出两个文件：
   - `career/ai-pm-campus/outputs/resume-outline.md`：完整大纲，含Gap分析
   - `career/ai-pm-campus/outputs/resume-onepage.md`：精简版，用于生成投递简历

### 输出

- `career/ai-pm-campus/outputs/resume-outline.md`
  - 完整 Markdown 大纲
  - 包含所有经历要点和Gap分析
  - 用于后期检索和调整
- `career/ai-pm-campus/outputs/resume-onepage.md`
  - 精简版，优先突出实习经历
  - 内容精炼，适合生成投递用PDF
- 聊天里补充简短摘要：
  - 当前简历最强的 3 个卖点
  - 最需要补强的 3 个缺口

## 失败处理

- 若 `resume/` 或 `experiences/` 为空：继续生成，但在 `Gap 清单` 中明确提醒缺少原始材料。
- 若 `master-points.md` 不存在：先创建空文件，再提示用户先运行 `extract`。
- 若标签混乱或同一项目有多个别名：主动统一命名，并在聊天中说明归并规则。
- 若输入日志内容过短、几乎没有高价值信息：不要硬凑要点，直接说明“本次无新增高价值要点”并更新处理记录。

## 使用示例

- `请用 /ai-pm-resume-hub extract 处理我接下来贴的最近 7 天工作日志`
- `用 /ai-pm-resume-hub build 更新我的 AI 产品经理校招简历`
- `请用 /ai-pm-resume-hub visualize 生成白色背景可视化仪表盘`
- `请用 /ai-pm-resume-hub export 导出HR投递版和手机预览版PDF`

## 4) export

导出两种PDF版本简历，满足不同场景需求：

### 输出版本
1. **HR投递版**：A4标准大小，内容精炼，重点突出实习经历，适合正式投递和打印
2. **手机预览版**：竖屏长图格式，适配手机屏幕，字体清晰，用于快速审查简历

### 执行流程

1. 先运行 `build` 生成最新的简历内容
2. 运行脚本生成两种PDF：

```bash
python3 ~/.openclaw/workspace/skills/ai-pm-resume-hub/scripts/export_pdf.py
```

3. 产出：
   - `career/ai-pm-campus/outputs/resume-hr.pdf`（A4标准，投递用）
   - `career/ai-pm-campus/outputs/resume-mobile.pdf`（竖屏长图，手机预览用）

### 依赖与提示
- HR投递版：自动优化排版，优先展示实习经历，控制在1页内
- 手机预览版：基于可视化仪表盘生成，白色背景，竖屏适配，无需放大即可查看
- 两种版本都支持中文显示，字体清晰

## 3) visualize

生成白色/透明背景的Bento风格可视化仪表盘，用于电脑端预览：

- 一页简历（清晰渲染Markdown格式）
- 要点池统计（按项目标签聚合展示）
- Gap汇总（集中展示所有待补数据）
- 简历质量评分（可选）

### 执行流程

1. 读取：
   - `career/ai-pm-campus/outputs/resume-onepage.md`
   - `career/ai-pm-campus/inputs/points-pool/master-points.md`
2. 运行脚本生成仪表盘：

```bash
python3 ~/.openclaw/workspace/skills/ai-pm-resume-hub/scripts/render_dashboard.py
```

3. 产出：
   - `career/ai-pm-campus/outputs/resume-dashboard.html`（白色/透明背景，Bento布局）

### 输出要求

- 设计风格：极简白色/透明背景，无多余装饰元素
- 保持Bento网格布局，内容清晰易读
- 聊天中返回可打开的文件路径，并简述包含模块。


