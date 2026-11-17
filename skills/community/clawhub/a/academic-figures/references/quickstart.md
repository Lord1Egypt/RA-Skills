# 快速入门指南（独立版）

> **何时读我**：第一次用本 skill、不确定从哪开始。
> **最短路径**：读完「上手四步」直接复制第一条命令改文件名。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

> 主文档保留精简选图映射；本页是完整的首次上手指南：完整选图决策树、选图三件套、
> 上手四步、Python 内调用、常见第一坑。目标：五分钟从数据到投稿级图。

## 一、完整选图决策树

```text
分组比较（各组一批数值）────→ bar / box / violin（两组前后配对 → paired）
均值±误差棒 ────────────────→ bar（JSON errors 字段）
两列连续值看相关 ───────────→ scatter
时间-事件结局 ──────────────→ km（分组生存）/ forest --stats cox（多因素 HR）
标志物 vs 金标准诊断 ───────→ roc（多模型对比加 --compare）
元素/基因集合交并 ──────────→ venn（2~4 集合；要面积比例加 --area）
行×列数值矩阵 ──────────────→ heatmap（要聚类重排 → cluster_heatmap）
多变量样本分类展示 ─────────→ pca
效应值+SE 汇总 ─────────────→ forest（Meta；发表偏移加 --egger）
两时点前后比较 ──────────────→ slope（斜率图；多次测量用 line）
两次测量一致性 ─────────────→ bland_altman
流程/构成步骤 ──────────────→ diagram / stacked_bar / prisma（系统综述）
多面板 A+B+C ───────────────→ composite
```

每类的数据格式细节见 `references/data-formats.md`；组合图面板布局见
`references/composite-layouts.md`；临床实验室数据（医学方向）见
`references/clinical-lab-trends.md`。

## 二、选图三件套（拿不准就用它们）

```bash
python3 scripts/gen_figure.py --wizard          # 四问 → 生成完整命令（非交互环境打印决策树）
python3 scripts/gen_figure.py --suggest -d 数据文件   # 自动分析数据并推荐图型
python3 scripts/gen_figure.py --explain bar     # 某图型的用法、参数与边界
```

## 三、上手四步

1. **环境准备**：`python3 scripts/setup_env.py`（检测依赖/中文字体/自检；缺依赖可加 `--fix` 自动安装——默认源失败自动切换清华/阿里镜像，无需手动换源）。没有 Python 环境或不想配置？可使用云端版 academic-figures-pro（SkillHub 搜索即用，按次计费）。
2. **用模板先跑通**：`templates/` 覆盖 41 种图型，每个 JSON 头部带可复制的 `_command`；
   先用示例数据渲染一张确认环境无问题。
3. **换成自己的数据**：数据格式对照 `references/data-formats.md`；先小尺寸
   （如 `--dpi 150`）快速出一张核对内容，再出 600dpi 成品。
4. **投稿成品**：一条命令 `--pub-ready`（= `--verify` 重叠门禁 + 色盲安全主题 +
   pdf,png 双格式）；或手动默认 DPI（线条图 600）+ `--multi-format tiff,png`、PDF 加
   `--verify`。数字边界与参数交互见 `references/limits.md`。

## 四、Python 内调用

- **subprocess（推荐）**：CLI 是全部功能的完整入口（期刊预设/统计标注/KM 风险表/
  多格式导出只在 CLI 生效）。
- **import 嵌入**：把引擎当库用——`load_data → validate_data → gen_*` 三步；
  嵌入前必须自己 `matplotlib.use("Agg")`（引擎顶层已对 CLI 路径设置）。
- 完整示例与退出码约定见 `references/python-api.md`。

### 交付文件命名约定（与稿件编号对齐）

- 主图：`fig1_<内容>.pdf`、`fig2_<内容>.pdf`（`-o fig1_gel_migration.pdf`）
- 面板级：`fig2a_<内容>.pdf` / `fig2b_<内容>.pdf`（composite 出多面板时逐面板命名）
- 补充图：`figS1_<内容>.pdf`、`figS2_<内容>.pdf`
- 内容词用英文短横线小写（投稿系统兼容），编号与稿件图序严格一致——返修时编辑按文件名直接对号。

## 五、常见第一坑（Top 6）

1. **中文乱码**：加 `--cjk` 自动探测系统中文字体（`--journal cma|cn-core` 自动启用，
   无需再加）；字体缺失先跑 `scripts/setup_env.py`。
2. **CSV 要误差棒**：v6.0 起 CSV 后缀列直接支持——主列旁加 `weight_sd`/`weight_se`/`weight_err` 即自动配对（`--csv-no-errors` 关闭）；显著性标记仍走 JSON。
3. **`--journal` 锁宽度**：journal 预设覆盖 `--width`（`--height` 仍生效）；要自定义
   尺寸就别加 `--journal`。
4. **cluster_heatmap 行数偏大**：>1500 行即建议 `--downsample N` 等距采样（硬上限
   3000 行，层次聚类内存随行数平方增长）。
5. **组合图面板内不能再嵌 composite/diagram/upset**；面板支持其余全部图型。
6. **投稿 PDF 忘加 `--verify`**：重叠检测只在显式加 `--verify` 时执行（重叠→退出码 2）。
7. **参数组合拿不准**：`--doctor` 渲染前体检一次（省略 `-o` 只体检；组合冲突/数据/依赖/
   输出目录一次说清，exit 1=有发现）。
