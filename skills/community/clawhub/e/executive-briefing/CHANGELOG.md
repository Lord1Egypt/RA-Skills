# CHANGELOG

## V2.0.0 (2026-07-23)

### 💥 重大重构：从「报告排版工具」到「高管汇报内容工厂」

**定位升级：** 输入详案→提炼→分层→转译→叙事→校验 → 输出面向高层的决策导向报告。

**基准框架：** Anthropic Executive Briefing（BLUF格式）

### 📋 SKILL.md
- 重写为 5 步处理流水线（信息提取→分层映射→语态转译→叙事构建→质量校验）
- 输出结构对齐 BLUF：Bottom Line → Key Findings → Implications → Actions → Risks → Decision Required
- 新增 写作铁律（6 条必须 + 6 条禁止）
- 新增 数据呈现规则（四舍五入/对比基准/relatable比较/突出delta）
- 新增 4 个标准模板体系
- 500 词硬上限约束
- 受众确认流程（开始前确认谁读、做什么决策、已有多少上下文）

### 🔧 脚本重构
- **init.py**（新增）：一键创建报告目录+模板+version.json+VERSION.md+README.md
- **bump.py**（增强）：+新文件生成 +变更注释注入 +VERSION.md/README.md自动更新 +--dry-run预览
- **validate.py**（重写）：结构校验→内容质量校验，7 项检查（BLUF/So What/数据/行动/篇幅/置信度/语态）+ JSON报告+A-D评级
- **density.py**（新增）：内容密度分析（数据密度/段落长度/空洞/行动词占比/阅读时长估算/综合判断）

### 📄 模板替换
- ~~planning-report.md~~ → `executive-summary.md`（通用高管摘要）
- ~~strategy-document.md~~ → `decision-memo.md`（决策备忘录）
- + 新增 `one-pager.md`（一页纸汇报）
- + 新增 `board-briefing.md`（董事会汇报）

### 📚 参考文档
- + 新增 `style-guide.md`（高管语态手册：中英文规范/技术→业务转译/受众分层）
- + 新增 `narrative-methodology.md`（叙事方法论：BLUF/So What/金字塔/信息密度曲线/30秒电梯法则）
- * 更新 `structure-validation.md`（7 项内容质量校验规则详解 + JSON 输出格式）
- * 更新 `edge-cases.md`（强化版 bump.py + density.py 边界场景 + 跨 SKILL 协作补充）
- * 更新 `collaboration-workflow.md`（标准化输入接口 + 上游 SKILL 对接 + 输出产物清单）
- ~~number-remap-rules.md~~ 降级为非核心（编号重排不再是主要能力）
- ~~version-bump-rules.md~~ 整合进 bump.py

---

## V1.1.0 (2026-07-21)
- SKILL.md 瘦身（130→80行）
- 新增 references/(5文档) templates/(2模板) scripts/(3脚本)
- 新增自动化工具：renumber.py / validate.py / bump.py
- 10/10 测试通过

## V1.0.0 (2026-07-21)
- 初始版本，由 delivery-platform 🚚 创建
