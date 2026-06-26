# 真实案例：企业数据迁移项目

## 背景
公司从旧系统迁移到新系统，需要处理 5 年的历史销售数据，共 2,000 个 Excel 文件，总大小 50GB。

## 项目概况
```
文件数量：2,000 个
数据总量：500 万行
文件大小：50GB
时间跨度：5 年
字段数量：25 列
数据质量：中等问题
```

## 挑战

### 1. 数据质量问题
```
问题：
- 15% 的文件有格式不一致
- 空值率平均 8%
- 重复数据约 3%
- 日期格式混乱（2020/01/01, 01-01-2020, 20200101）
- 数值字段混杂文本
```

### 2. 性能挑战
```
问题：
- 单个文件最大 200MB
- 总处理时间预估 48 小时
- 需要中断和恢复能力
```

### 3. 业务需求
```
需求：
- 保持数据完整性
- 记录处理日志
- 生成质量报告
- 可追溯和审计
```

## 解决方案

### 阶段 1：文件分析（1 天）

#### 自动扫描
```python
import os
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

def scan_excel_files(directory):
    """扫描所有 Excel 文件"""
    results = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.xlsx', '.xls')):
                file_path = Path(root) / file

                # 获取文件信息
                info = {
                    'path': str(file_path),
                    'name': file,
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }

                # 尝试读取基本信息
                try:
                    df = pd.read_excel(file_path, nrows=10)
                    info['columns'] = df.columns.tolist()
                    info['preview_rows'] = len(df)
                    info['status'] = 'readable'
                except Exception as e:
                    info['error'] = str(e)
                    info['status'] = 'error'

                results.append(info)

    # 保存扫描结果
    with open('scan_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results

# 执行扫描
files = scan_excel_files('/data/sales_files')
print(f"扫描完成: {len(files)} 个文件")
```

### 阶段 2：标准化处理（1 周）

#### 统一数据格式
```python
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ExcelDataProcessor:
    """Excel 数据处理器"""

    def __init__(self):
        self.stats = {
            'processed': 0,
            'errors': 0,
            'rows_imported': 0,
            'rows_skipped': 0
        }

    def normalize_date(self, value):
        """标准化日期格式"""
        if pd.isna(value):
            return None

        # 尝试多种日期格式
        date_formats = [
            '%Y/%m/%d',
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y%m%d'
        ]

        for fmt in date_formats:
            try:
                return pd.to_datetime(value, format=fmt)
            except:
                continue

        # 尝试自动解析
        try:
            return pd.to_datetime(value)
        except:
            logging.warning(f"无法解析日期: {value}")
            return None

    def clean_amount(self, value):
        """清洗金额字段"""
        if pd.isna(value):
            return 0.0

        # 移除货币符号和逗号
        if isinstance(value, str):
            value = value.replace('¥', '').replace('$', '').replace(',', '').strip()

        try:
            return float(value)
        except:
            logging.warning(f"无法解析金额: {value}")
            return 0.0

    def validate_row(self, row):
        """验证行数据"""
        errors = []

        # 必填字段检查
        if pd.isna(row.get('order_id')):
            errors.append('order_id 缺失')

        # 数值范围检查
        amount = row.get('amount', 0)
        if amount < 0:
            errors.append(f'金额为负: {amount}')

        # 日期合理性检查
        date = row.get('order_date')
        if date and date > datetime.now():
            errors.append(f'日期在未来: {date}')

        return errors

    def process_file(self, file_path):
        """处理单个文件"""
        try:
            logging.info(f"处理文件: {file_path}")

            # 读取 Excel
            df = pd.read_excel(file_path)

            original_rows = len(df)

            # 1. 标准化列名
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

            # 2. 处理日期字段
            if 'order_date' in df.columns:
                df['order_date'] = df['order_date'].apply(self.normalize_date)

            # 3. 处理金额字段
            if 'amount' in df.columns:
                df['amount'] = df['amount'].apply(self.clean_amount)

            # 4. 删除重复行
            duplicates = df.duplicated().sum()
            if duplicates > 0:
                logging.warning(f"发现 {duplicates} 个重复行")
                df = df.drop_duplicates()

            # 5. 验证数据
            df['validation_errors'] = df.apply(self.validate_row, axis=1)
            invalid_rows = df[df['validation_errors'].str.len() > 0]
            if len(invalid_rows) > 0:
                logging.warning(f"发现 {len(invalid_rows)} 个无效行")
                # 保存无效行到单独文件
                invalid_rows.to_excel(f'errors_{Path(file_path).stem}.xlsx', index=False)

            # 6. 只保留有效数据
            df_valid = df[df['validation_errors'].str.len() == 0]
            df_valid = df_valid.drop('validation_errors', axis=1)

            # 7. 添加元数据
            df_valid['source_file'] = Path(file_path).name
            df_valid['imported_at'] = datetime.now()

            # 更新统计
            self.stats['processed'] += 1
            self.stats['rows_imported'] += len(df_valid)
            self.stats['rows_skipped'] += (original_rows - len(df_valid))

            logging.info(f"文件处理成功: {len(df_valid)}/{original_rows} 行有效")

            return df_valid

        except Exception as e:
            logging.error(f"处理文件失败 {file_path}: {e}")
            self.stats['errors'] += 1
            return None

# 使用示例
processor = ExcelDataProcessor()

# 批量处理
for file_info in files:
    if file_info['status'] == 'readable':
        df = processor.process_file(file_info['path'])
        if df is not None:
            # 保存到数据库或新文件
            df.to_csv(f'processed/{Path(file_info["path"]).stem}.csv', index=False)

# 输出统计报告
print("\n处理统计:")
for key, value in processor.stats.items():
    print(f"{key}: {value}")
```

### 阶段 3：性能优化（2 天）

#### 并行处理
```python
from multiprocessing import Pool, cpu_count
import pandas as pd

def process_single_file(args):
    """单个文件处理函数（用于多进程）"""
    file_path, output_dir = args
    try:
        df = pd.read_excel(file_path)

        # 数据清洗逻辑...
        # （省略具体代码）

        output_path = Path(output_dir) / Path(file_path).name
        df.to_csv(output_path.with_suffix('.csv'), index=False)

        return {'status': 'success', 'file': file_path}
    except Exception as e:
        return {'status': 'error', 'file': file_path, 'error': str(e)}

def parallel_process(files, output_dir, workers=None):
    """并行处理多个文件"""
    if workers is None:
        workers = max(1, cpu_count() - 1)  # 保留一个核心

    print(f"使用 {workers} 个进程并行处理")

    # 准备参数
    args_list = [(f['path'], output_dir) for f in files if f['status'] == 'readable']

    # 创建进程池
    with Pool(workers) as pool:
        results = pool.map(process_single_file, args_list)

    # 统计结果
    success = sum(1 for r in results if r['status'] == 'success')
    errors = sum(1 for r in results if r['status'] == 'error')

    print(f"\n完成: {success} 个成功, {errors} 个失败")

    return results

# 使用
results = parallel_process(files, output_dir='processed', workers=8)
```

#### 断点续传
```python
import json
from pathlib import Path

class ResumeableProcessor:
    """支持断点续传的处理器"""

    def __init__(self, checkpoint_file='checkpoint.json'):
        self.checkpoint_file = checkpoint_file
        self.completed = self.load_checkpoint()

    def load_checkpoint(self):
        """加载检查点"""
        if Path(self.checkpoint_file).exists():
            with open(self.checkpoint_file, 'r') as f:
                return set(json.load(f))
        return set()

    def save_checkpoint(self):
        """保存检查点"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump(list(self.completed), f)

    def is_completed(self, file_path):
        """检查文件是否已处理"""
        return file_path in self.completed

    def mark_completed(self, file_path):
        """标记文件已完成"""
        self.completed.add(file_path)
        self.save_checkpoint()

    def process(self, files):
        """处理文件列表（跳过已完成的）"""
        for file_info in files:
            file_path = file_info['path']

            if self.is_completed(file_path):
                print(f"跳过已完成: {file_path}")
                continue

            # 处理文件
            result = process_file(file_path)

            if result:
                self.mark_completed(file_path)

# 使用
processor = ResumeableProcessor()
processor.process(files)
```

### 阶段 4：质量报告（1 天）

#### 生成数据质量报告
```python
def generate_quality_report(processed_files):
    """生成数据质量报告"""
    report = {
        '总文件数': len(processed_files),
        '成功处理': 0,
        '处理失败': 0,
        '总行数': 0,
        '有效数据': 0,
        '无效数据': 0,
        '数据质量指标': {}
    }

    for file_info in processed_files:
        if file_info['status'] == 'success':
            report['成功处理'] += 1
            report['总行数'] += file_info['total_rows']
            report['有效数据'] += file_info['valid_rows']
            report['无效数据'] += file_info['invalid_rows']
        else:
            report['处理失败'] += 1

    # 计算质量指标
    report['数据质量指标'] = {
        '有效率': f"{(report['有效数据'] / report['总行数'] * 100):.2f}%",
        '成功率': f"{(report['成功处理'] / report['总文件数'] * 100):.2f}%"
    }

    # 生成可视化报告
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # 处理状态分布
    axes[0, 0].pie(
        [report['成功处理'], report['处理失败']],
        labels=['成功', '失败'],
        autopct='%1.1f%%'
    )
    axes[0, 0].set_title('处理状态分布')

    # 数据质量分布
    axes[0, 1].pie(
        [report['有效数据'], report['无效数据']],
        labels=['有效', '无效'],
        autopct='%1.1f%%'
    )
    axes[0, 1].set_title('数据质量分布')

    # 保存图表
    plt.savefig('quality_report.png', dpi=300, bbox_inches='tight')

    return report

# 生成报告
report = generate_quality_report(processed_files)
print("\n数据质量报告:")
for key, value in report.items():
    print(f"{key}: {value}")
```

## 效果对比

| 指标 | 手动处理 | 自动化处理 | 提升 |
|------|----------|------------|------|
| 处理时间 | 480 小时 | 24 小时 | -95% |
| 错误率 | 12% | 2% | -83% |
| 成本 | $96,000 | $4,800 | -95% |
| 可追溯性 | 无 | 完整日志 | ✅ |
| 可重复性 | 低 | 高 | ✅ |

## 经验教训

1. **数据质量至关重要**
   - 前期验证可避免后期大量返工
   - 建立数据质量标准
   - 自动化质量检查

2. **性能优化很重要**
   - 并行处理可大幅提速
   - 分批处理降低内存占用
   - 监控资源使用情况

3. **可恢复性设计**
   - 断点续传节省时间
   - 详细日志便于排查
   - 版本控制数据文件

4. **沟通和文档**
   - 记录所有处理逻辑
   - 生成详细的报告
   - 保持与业务方沟通

5. **测试和验证**
   - 小规模测试后再全量
   - 抽样验证处理结果
   - 业务方确认数据正确性
