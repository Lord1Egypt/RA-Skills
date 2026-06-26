# 讲师管理流程

画像数据通过 Write-Through 双写管线同步到 SQLite 和文件系统。
所有写入操作通过 `db_query.py` CLI 完成，智能体不可自行写文件或创建脚本。

## 核心架构：Write-Through 双写

每次 save/delete 操作自动更新 DB 和文件系统，无需手动调用 db_sync.py：

| 操作 | DB | 文件系统 | 自动? |
|------|-----|---------|------|
| 保存画像 | INSERT OR REPLACE | 写 profile.json + 创建目录 | YES |
| 删除讲师 | DELETE | 移入回收站 + .meta.json | YES |
| 添加样本 | INSERT | 写 样本/ 文件 | YES |
| 保存文案 | INSERT (元数据) | 写 .txt 文件 | YES |
| 删除文案 | DELETE | 删 .txt 文件 | YES |
| 删除知识 | DELETE | 删私有层源文件 | YES |

## 新增讲师画像（3步流程）

### Step 1: 定量分析

用户粘贴文案或提供文件，调用分析脚本获取定量数据。

**长文本** (用户粘贴完整文章，典型场景)：
1. 用原生文件写入工具将样本文本写到控制台 staging 位置：
   ```
   <控制台目录>/讲师列表/<名称>/样本/_staging.txt
   ```
2. 调用分析 + 自动保存样本：
   ```bash
   python scripts/lecturer_analyzer.py --input "<控制台目录>/讲师列表/<名称>/样本/_staging.txt" --lecturer <名称> --data-dir <控制台目录> --save-sample
   ```
   `--save-sample` 自动将 _staging.txt rename 为 `sample_YYYYMMDD.txt` 并注册 DB（Write-Through）。

**文件输入**：
```bash
python scripts/lecturer_analyzer.py --input <文件路径> --lecturer <名称> --data-dir <控制台目录> --save-sample
```

**短文本** (<500字)：
```bash
python scripts/lecturer_analyzer.py --lecturer <名称> --text "<文案>" --data-dir <控制台目录> --save-sample
```

输出定量分析结果。首次分析 `merge_status: "new"`，需继续 Step 2。

### Step 2: 构建完整画像

分析脚本只产出定量指标（词频、句长、标点比等）。智能体必须结合定量数据和自身推断构建完整画像。

画像格式见 [profile-format.md](profile-format.md)。必须包含：
- `qualitative`: persona_mapping, style_dimensions
- `quantitative`: Step 1 的完整输出
- `sample_texts`: 代表性短摘录

### Step 3: 保存画像（Write-Through: DB + profile.json）

**小型画像** (<2000字符JSON)：
```bash
python scripts/db_query.py --type lecturer --action save \
  --id <名称> --query '<完整画像JSON>' --data-dir <控制台目录>
```

**大型画像** (典型——定量数据很长)：
1. 用原生文件写入工具将画像 JSON 写到控制台 staging 位置：
   ```
   <控制台目录>/讲师列表/<名称>/_profile_staging.json
   ```
2. 调用保存（`_staging.json` 文件在成功后自动删除）：
   ```bash
   python scripts/db_query.py --type lecturer --action save \
     --id <名称> --query-file "<控制台目录>/讲师列表/<名称>/_profile_staging.json" --data-dir <控制台目录>
   ```

保存后自动完成双写：
- DB: `lecturers` 表（可查询、对比、检索）
- 文件系统: `讲师列表/{名称}/profile.json`（人类可读、可导出）

无需手动调用 `db_sync.py`。

### 验证
```bash
python scripts/db_query.py --type lecturer --action lite --id <名称> --data-dir <控制台目录>
```

## 增量学习（给已有讲师加新样本）

**长文本**：写到 staging + `--input` + `--save-sample` + `--merge`：
```bash
python scripts/lecturer_analyzer.py --input "<控制台目录>/讲师列表/<名称>/样本/_staging.txt" --lecturer <名称> --merge --data-dir <控制台目录> --save-sample
```

**短文本**：
```bash
python scripts/lecturer_analyzer.py --lecturer <名称> --text "<新样本>" --merge --data-dir <控制台目录> --save-sample
```

自动加权合并定量数据，并通过 Write-Through 写透到 DB + profile.json。

如需更新定性特征，再执行 Step 2-3 重新保存画像。

## 查看讲师列表

```bash
python scripts/db_query.py --type lecturer --action list --data-dir <控制台目录>
```

## 查看讲师详情

- 轻量版（文案生成用，~400 tokens）：`--action lite`
- 完整版（管理用）：`--action get`
- 样本文案：`--action samples`

## 修改讲师画像

- **改属性**：先 `--action get` 获取当前画像 → 智能体修改 → `--action save` 保存
  ```bash
  python scripts/db_query.py --type lecturer --action get --id <名称> --data-dir <控制台目录>
  # 修改后保存（Write-Through 自动双写）
  # 大型画像用 --query-file + staging 文件
  python scripts/db_query.py --type lecturer --action save \
    --id <名称> --query-file "<控制台目录>/讲师列表/<名称>/_profile_staging.json" --data-dir <控制台目录>
  ```

## 添加样本

```bash
python scripts/db_query.py --type lecturer --action add_sample \
  --id <名称> --query '{"sample_name":"样本2.txt","content":"文案内容..."}' \
  --data-dir <控制台目录>
```

Write-Through: 同时写入 DB (`lecturer_samples` 表) 和文件系统 (`讲师列表/{名称}/样本/样本2.txt`)。

## 删除讲师

```bash
python scripts/db_query.py --type lecturer --action delete --id <名称> --data-dir <控制台目录>
```

Write-Through: 同时删除 DB 记录并将 `讲师列表/{名称}/` 目录移入回收站（含 .meta.json 恢复信息）。

恢复时从回收站移回并 `db_sync.py --direction to-db` 同步。

## 对比讲师

```bash
python scripts/db_query.py --type lecturer --action compare --id 讲师A --id2 讲师B --data-dir <控制台目录>
```

## 导出讲师

```bash
python scripts/lecturer_transfer.py --action export --lecturer <名称> --data-dir <控制台目录> --output <导出目录>
```

导出完整讲师目录（画像 + 样本 + 系列文案）。
