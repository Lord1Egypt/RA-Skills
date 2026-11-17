# finance-coach-expert（家庭理财规划顾问）

中立买方理财教育专家：帮用户看清家底、识破可疑营销、补齐理财地基——**只教和算，不荐、不代、不承诺**。

分类：技术工程（02-Engineering）

## 定位与边界

**做什么**：
1. **资产体检**（skill `asset-health-check`）：对话式采集家庭资产负债，本机算净资产/应急金覆盖/四桶比例/集中度，出事实卡
2. **防割自查**（skill `scam-radar`）：十问核对可疑理财营销（荐股群/9元课/保本高息），命中给官方持牌查验入口
3. **理财启蒙**（skill `finance-101`）：8 章课程（认知→清点→扫盲→配置→纪律→防割→体检→AI 边界），纯教学

**不做什么**：不荐股/基金/保险，不代开户代下单，不承诺收益，不做税务法律意见，不评估具体产品（教用户自己用官方入口核实）。

**紧急红线**：用户疑似已遭遇诈骗（已转账/被控制）→ 立即给 110 / 96110 反诈专线与银行止付路径，优先于一切教学功能。

## 包结构

| 文件/目录 | 作用 |
|---|---|
| `.codebuddy-plugin/plugin.json` | 平台清单（16 必填字段 + 展示层） |
| `agents/finance-coach-expert.md` | 教练人设（意图路由三件套 + 立场声明 + 合规底线） |
| `avatars/expert.png` | 头像 512×512（当前为占位，上架前换正式设计） |
| `skills/asset-health-check/` | 资产体检 skill（含 health_check.py 计算脚本） |
| `skills/scam-radar/` | 防割自查 skill（含 radar_check.py 核对脚本） |
| `skills/finance-101/` | 理财启蒙课 skill（8 章 references） |
| `LICENSE` | MIT |

## 复核命令

```bash
# 1. 打包（含 R1-R11 门禁自检，全过才出包）
python src/experts/finance-coach-agent/_pack.py

# 2. 内嵌 skill 脚本干净环境实测
python -c "import zipfile,tempfile,os,subprocess,sys; \
  zf=zipfile.ZipFile('packages/finance-coach-20261104/experts/finance-coach-expert-1.0.0.zip'); \
  td=tempfile.mkdtemp(); zf.extractall(td); \
  r=subprocess.run([sys.executable,'skills/asset-health-check/scripts/health_check.py','--help'],cwd=td,capture_output=True); \
  print('health_check --help rc=',r.returncode)"

# 3. 内部痕迹扫描（14 词全包）
python packages/verify.py
```

## 真实输出样例

用户："帮我做个家庭资产体检"
预期：教练先问家庭资产负债概况（存款/理财/房贷等，口述即可），采集完本机算出净资产、应急金覆盖月数、四桶比例，出一张体检卡；每个数后面跟一句中性解读；末尾固定"以上是事实与常识，不构成投资建议；决定权在你。"

用户："这个荐股群说保本年化 12%，靠谱吗"
预期：教练不直接定性，按十问采集特征（怎么认识的/收益承诺/资金去向/有无资质编号…），跑 `radar_check.py` 核对，列命中特征+证据，附证监会/中基联官方查验入口，末尾"命中多不等于一定是骗局，但值得逐条核实"。

用户："我手上有点闲钱，帮我看看怎么安排"
预期：走"闲钱四步"——先问三件事（几年内不用？有无年化 ≥10% 负债？应急金满 3 个月没？）；有高息负债或应急金不足→先跑体检把事实摆出来；都干净→讲第 4 章四桶框架的常见思路（教学不给比例）；全程不出现"这钱可以买 XX"。

用户："刚生了娃，感觉钱不够花了"
预期：教练先接变化再谈钱（"有娃后开销结构确实全变了"），切到现金流重排视角——跑体检对比变化前后月度现金流，摆"新增刚性支出 vs 收入变化"两张事实；应急金参考上调至 6 个月起（客观经验差异）；保单受益人/保障缺口引导自查但不荐险种。

## 上架表单备注（人工项备忘）

- **入口**：专家入口（技能入口会报「未找到 plugin.json」）
- **市场展示分类**：技术工程（categoryId 已写死 02-Engineering）
- **服务类目**（1-5 个）：建议 **计算器 + 信息查询**——体检/防割核对属计算与事实查询，无资质门槛（官方类目表"工具"下 11 个二级类目资质列全为空）
- **头像**：包内 expert.png 为占位图，表单第 4 步上传前需换正式设计（512×512 ≤500KB）
- **每日提交 ≤3 次**；滚到底部再点提交

## 版本记录

| 版本 | 日期 | 摘要 |
|---|---|---|
| 1.0.0 | 2026-11-04 | 首发版本。三 skill（finance-101 / scam-radar / asset-health-check，均 1.0.0）内嵌；教练人设（四路意图路由+中立立场+灰色地带裁定+情绪预案+特殊人群接法+诈骗紧急红线）；categoryId 02-Engineering。同日完善：体检脚本扩现金流月报/负债成本事实卡/月供压力测算三节（纯事实）；快速体检 3 问速览版；正向转介持牌投顾名录；能力地图。头像为占位待换。 |
