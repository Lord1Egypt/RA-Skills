# Financial Data Collection

运行环境使用现有 conda 环境 `scrapyEnv`。

## 环境

如果 `scrapyEnv` 已存在，直接安装依赖：

```bash
conda activate scrapyEnv
pip install -r requirements.txt
```

如果需要按项目文件创建或更新环境：

```bash
conda env update -n scrapyEnv -f environment.yml
conda activate scrapyEnv
```

## 运行

全量抓取、全量重算：

```bash
python scripts/run_pipeline.py
```

按闭区间重算：

```bash
python scripts/run_pipeline.py --start-month 2025-01 --end-month 2025-03
```

只传一个月份也可以，会自动视为起止相同：

```bash
python scripts/run_pipeline.py --start-month 2025-03
```

## 规则

输入参数：

- `--start-month YYYY-MM`
- `--end-month YYYY-MM`

若只传一个月份：

- 只传 `--start-month`，则 `end-month` 自动等于 `start-month`
- 只传 `--end-month`，则 `start-month` 自动等于 `end-month`

闭区间规则：

- 输入区间按闭区间处理
- 例如 `--start-month 2025-01 --end-month 2025-03`，表示处理 `2025-01` 到 `2025-03`

`1-2月` 特殊规则：

- 如果输入区间只包含 `2025-01` 或只包含 `2025-02`，则自动按 `1-2月` 合并期处理
- 例如：
  - `--start-month 2025-01 --end-month 2025-01`
  - `--start-month 2025-02 --end-month 2025-02`
- 以上两种情况的区间汇总外层目录都会提升为 `202501-202502_汇总`

为了推导结果，程序会自动补抓前置累计期：

- 例如输入 `--start-month 2025-03 --end-month 2025-03`
- 实际会使用：
  - `202501-202502`
  - `202501-202503`
- 这样才能计算出 `202503` 的单月值

## 输出

输出目录默认按原始公告期间归档：

- 普通累计期：`output/YYYYMM-YYYYMM/`
- `1-2月` 合并期：`output/YYYY01-YYYY02/`

每个区间缓存文件夹内包含：

- `raw_documents.xlsx`
- `extracted_metrics.xlsx`

说明：

- `raw_documents.xlsx` 和 `extracted_metrics.xlsx` 的 `期间` 均使用 `YYYYMM-YYYYMM`
- `derived_metrics.xlsx` 不输出到区间文件夹，只在汇总目录中输出
- 若区间文件夹已存在且 `extracted_metrics.xlsx` 数据行数不少于 `40` 条，则直接复用，不重新抓取
- 若区间文件夹不完整或指标数不足 `40` 条，则重新抓取并覆盖

每次命令执行结束后，还会额外生成一个批次汇总目录：

- 全量运行：`output/全量汇总/YYYYMMDDHHMMSS/`
- 区间运行：`output/<请求区间>_汇总/YYYYMMDDHHMMSS/`

例如：

- `output/全量汇总/20260326160000/`
- `output/202501-202503_汇总/20260326160000/`

每个批次子目录内包含：

- `raw_documents_YYYYMMDDHHMMSS.xlsx`
- `extracted_metrics_YYYYMMDDHHMMSS.xlsx`
- `derived_metrics_YYYYMMDDHHMMSS.xlsx`
- `monthly_summary_YYYYMMDDHHMMSS.xlsx`
- `运行汇报_YYYYMMDDHHMMSS.md`

其中：

- 4 个 Excel 是本次命令的整批汇总结果
- `derived_metrics.xlsx` 只在汇总目录中生成
- 汇总结果按批次子目录留档，不覆盖旧汇总
- `derived_metrics.xlsx` 的 `期间` 使用结果月份格式：
  - `1-2月` 合并期会按平均值拆成 `YYYY01`、`YYYY02`
  - 普通单月：`YYYYMM`
- `derived_metrics.xlsx` 包含 `收支方向` 列：
  - 收入类为 `财政收入`
  - 支出类为 `财政支出`
  - 赤字类为 `赤字`
- `derived_metrics.xlsx` 对 `1-2月` 合并值会：
  - 按平均值拆成 1 月和 2 月两条记录
  - `推导类型` 标记为 `1-2月平均值`
  - `备注` 标记为 `1-2月合并值按平均值拆分为1月和2月`
- `monthly_summary.xlsx` 基于 `derived_metrics.xlsx` 生成：
  - 左侧为 `收支大类`、`指标归类`、`指标`
  - 右侧每列为月份
  - 对 `1-2月` 合并值，会拆成 `YYYY01`、`YYYY02` 两列，并用平均值填入两列
- 所有导出的 Excel 会自动调整列宽，并统一设置为水平、垂直居中
- `extracted_metrics.xlsx`、`derived_metrics.xlsx`、`monthly_summary.xlsx` 的指标列表头统一显示为 `指标（单位：亿元）`
- `运行汇报_YYYYMMDDHHMMSS.md` 记录本次运行的参数、时间、导出范围、数据统计、异常摘要和文件清单
