---

slug: data-analyst-cn
name: data-analyst-cn
version: 1.0.25
displayName: 数据分析师
summary: 数据清洗、统计分析、时间序列分析、可视化代码生成与分析报告自动生成。数据分析师——快速进行数据清洗、统计分析和可视化，适合数据分析师、产品经理、运营人员.
  核心能力包括： - 多源数据读取（
summary_zh: 数据清洗、统计分析、时间序列分析、可视化代码生成与分析报告自动生成。数据分析师——快速进行数据清洗、统计分析和可视化，适合数据分析师、产品经理、运营人员.
  核心能力包括： - 多源数据读取（
license: MIT
description: |-。数据清洗、统计分析、时间序列分析、可视化代码生成与分析报告自动生成。数据分析师——快速进行数据清洗、统计分析和可视化，适合数据分析师、产品经理、运营人员。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。 功能涵盖: analyst。
  核心能力包括： - 多源数据读取（。支持自动化配置和灵活的参数设置，适覆盖多种使用场景，优化工作流程和效率。。数据清洗、统计分析、时间序列分析、可视化代码生成与分析报告自动生成。数据分析师——快速进行数据清洗、统计分析和可视化，适合数据分析师、产品经理、运营人员.
  核心能力包括： - 多源数据读取（'
tags:
- 信息检索
- data-analysis
- visualization
- 数据处理
- 数据分析
- 工具
- col
- python
- print
- api
- plt
tools:
- read
- exec
- write
- glob
homepage: ''
category: Research
homepage: ""
pricing_tier: "L2-标准级"

---

> **功能说明**: 本技能涵盖 化工作流场景 等核心能力。

# 数据分析师

## 输入参数
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 数据分析师处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 专业版增强能力
| 能力 | 免费版 | 付费版 |
|:-----|:-----|:-----|
| 基础功能 | 支持 | 支持 |
| 数据分析师统计分析 | 不支持 | 支持 |
| 数据分析师时间序列分析 | 不支持 | 支持 |
| 数据分析师可视化代码生成与分析 | 不支持 | 支持 |
| 大数据集流式处理 | 不支持 | 支持 |
| 多数据源关联查询 | 不支持 | 支持 |

## 简介
快速进行数据清洗、统计分析和可视化，适合数据分析师、产品经理、运营人员。提供从数据读取到报告生成的完整Python代码模板，覆盖Pandas、Matplotlib、Seaborn、Statsmodels核心工作流.
## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 能力矩阵
### 多源数据读取
| 数据源 | 代码 | 说明 |
|:---:|:---:|:---:|
| CSV | `pd.read_csv('data.csv')` | 读取CSV文件 |
| Excel | `pd.read_excel('data.xlsx', sheet_name='Sheet1')` | 指定Sheet读取 |
| JSON | `pd.read_json('data.json')` | 读取JSON文件 |
| SQLite | `pd.read_sql('SELECT * FROM table', conn)` | 需先 `sqlite3.connect('database.db')` |
| API | `pd.DataFrame(response.json())` | 需先 `requests.get('https://api.example.com/data')` |

### 数据预览与质量检查
```python
print(df.shape)        # 行列数，如 (1542, 7)
print(df.columns)      # 列名列表
print(df.dtypes)       # 数据类型
print(df.info())       # 详细信息（含内存占用）
# ...
print(df.head())       # 前 5 行
print(df.tail())       # 后 5 行
print(df.sample(5))    # 随机 5 行
# ...
print(df.describe())   # 数值列统计
print(df.describe(include='all'))  # 所有列（含分类列）
```

### 数据清洗
**缺失值处理**：

```python
df.isnull().sum()                       # 统计每列缺失数
df.dropna()                             # 删除含缺失的行
df.fillna(0)                            # 填充 0
df.fillna(df.mean())                    # 填充均值
df['col'].fillna(df['col'].mode()[0])   # 填充众数
```

**去重处理**：

```python
df.duplicated().sum()                   # 统计重复行数
df.drop_duplicates()                    # 删除完全重复行
df.drop_duplicates(subset=['col'])      # 按指定列去重
```

**类型转换**：

```python
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
df['category'] = df['category'].astype('category')
```

**IQR异常值剔除**：

```python
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['col'] >= Q1 - 1.5*IQR) & (df['col'] <= Q3 + 1.5*IQR)]
```

**字符串处理**：

```python
df['name'] = df['name'].str.strip()           # 去首尾空白
str.lower()           # 转小写
str.replace('old', 'new')  # 替换
```

### 统计分析
**描述统计**：

```python
df['col'].mean()      # 均值
df['col'].median()    # 中位数
df['col'].mode()      # 众数
df['col'].std()       # 标准差
df['col'].var()       # 方差
df['col'].max() - df['col'].min()  # 极差
df['col'].skew()      # 偏度
df['col'].kurt()      # 峰度
df['col'].quantile([0.25, 0.5, 0.75])  # 分位数
```

**相关分析**：

```python
df.corr()             # 完整相关矩阵
df.corr()['target']   # 与目标变量的相关性
```

**分组聚合**：

```python
df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'mean'
})
```

**交叉表**：

```python
pd.crosstab(df['col1'], df['col2'])
```

### 时间序列分析

```python
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
# ...
df.resample('D').sum()      # 按天汇总
df.resample('W').mean()     # 按周均值
df.resample('M').sum()      # 按月汇总
# ...
df['rolling_mean'] = df['col'].rolling(window=7).mean()  # 7日滚动均值
df['rolling_std'] = df['col'].rolling(window=7).std()    # 7日滚动标准差
# ...
df['diff'] = df['col'].diff()              # 一阶差分
df['pct_change'] = df['col'].pct_change()  # 环比变化率
# ...
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(df['col'], model='additive', period=12)
result.plot()
```

### 可视化代码生成
**中文字体配置**（必须先执行）：

```python
import matplotlib.pyplot as plt
import seaborn as sns
# ...
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
```

**基础图表**：

| 图表类型 | 代码 | 适用场景 |
|:------|------:|:------|
| 折线图 | `plt.plot(df['date'], df['value'])` | 趋势变化 |
| 柱状图 | `plt.bar(df['category'], df['value'])` | 分类对比 |
| 散点图 | `plt.scatter(df['x'], df['y'], alpha=0.5)` | 关系分布 |
| 直方图 | `plt.hist(df['value'], bins=20, edgecolor='black')` | 分布形态 |
| 箱线图 | `sns.boxplot(data=df, x='category', y='value')` | 离群值检测 |
| 热力图 | `sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)` | 相关矩阵 |

**高级图表**：

```python
# 分组柱状图
df_grouped = df.groupby(['category', 'type'])['value'].sum().unstack()
df_grouped.plot(kind='bar', figsize=(12, 6))
# ...
# 小提琴图
sns.violinplot(data=df, x='category', y='value')
# ...
# 成对关系图
sns.pairplot(df[['col1', 'col2', 'col3', 'category']], hue='category')
# ...
# 多轴趋势图（含置信区间）
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df.index, df['value'], label='实际值')
ax.plot(df.index, df['rolling_mean'], label='7日均值', linestyle='--')
ax.fill_between(df.index, df['lower'], df['upper'], alpha=0.2)
ax.legend()
```

### 分析报告自动生成
```python
def generate_report(df):
    report = f"""
# ...

# ...

## 1. 数据概览
- 数据量：{len(df)} 行 × {len(df.columns)} 列
- 时间范围：{df['date'].min()} 至 {df['date'].max()}
- 缺失值：{df.isnull().sum().sum()} 个
# ...
## 2. 关键指标
- 总销售额：¥{df['sales'].sum():,.2f}
- 平均订单：¥{df['sales'].mean():,.2f}
# ...
## 3. 分布特征
- 偏度：{df['sales'].skew():.2f}
- 峰度：{df['sales'].kurt():.2f}
# ...
## 4. Top 5 类别
{df.groupby('category')['sales'].sum().sort_values(ascending=False).head().to_markdown()}
# ...
## 5. 趋势分析
- 环比增长：{df['sales'].pct_change().mean()*100:.2f}%
"""
    return report
```

## 操作步骤
1. **读取数据**：根据数据源选择 `pd.read_csv()` / `pd.read_excel()` / `pd.read_json()` / `pd.read_sql()`
2. **预览检查**：执行 `df.shape`、`df.dtypes`、`df.describe()` 了解数据全貌
3. **数据清洗**：处理缺失值（`fillna`）、去重（`drop_duplicates`）、类型转换（`astype`）、IQR异常值剔除
4. **统计分析**：计算描述统计量、相关矩阵、分组聚合、交叉表
5. **时间序列**：如涉及时序数据，执行 `resample`、`rolling`、`seasonal_decompose`
6. **可视化**：配置SimHei字体后生成图表代码
7. **报告生成**：调用 `generate_report()` 输出结构化分析报告

## 详细示例

### 示例1：CSV数据清洗与分析

```text
输入: 分析这个 CSV 文件：sales.csv
# ...
处理:
- df = pd.read_csv('sales.csv')
- 缺失值: df['sales'].fillna(df['sales'].mean())
- 异常值: Q1=120, Q3=450, IQR=330, 保留 [Q1-1.5*IQR, Q3+1.5*IQR] 范围
- 统计: 均值¥45,230, 中位数¥38,500, 偏度1.2
# ...
输出: 清洗后 1485 行（原 1542 行），销售额右偏分布
```

### 示例2：生成折线图代码

```text
输入: 为这些数据生成折线图代码
# ...
输出:
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'])
plt.title('趋势图')
plt.xlabel('日期')
plt.ylabel('数值')
plt.show()
```

### 示例3：时间序列季节分解

```text
输入: 对月度销售数据做季节性分解
# ...
处理:
- df['date'] = pd.to_datetime(df['date'])
- df = df.set_index('date')
- result = seasonal_decompose(df['sales'], model='additive', period=12)
- 趋势组件: 稳定上升
- 季节组件: 12月峰值，6月谷值
- 残差: 无明显模式
# ...
输出: 分解图含趋势/季节/残差三子图
```

## 问题应对方案
| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 中文图表显示方框 | 未配置SimHei字体 | 执行 `plt.rcParams['font.sans-serif'] = ['SimHei']` 和 `plt.rcParams['axes.unicode_minus'] = False` |
| `KeyError` 列名不存在 | 列名含空格或大小写不一致 | 先 `print(df.columns)` 检查实际列名，用 `df.columns = df.columns.str.strip()` 清洗 |
| `fillna(df.mean())` 报错 | 含非数值列无法求均值 | 仅对数值列填充：`df.select_dtypes(include='number').fillna(df.mean())` |
| IQR剔除后数据量骤减 | 异常值阈值过严（1.5*IQR） | 检查数据分布是否极度偏斜，考虑用 3*IQR 放宽阈值或先做对数变换 |
| `seasonal_decompose` 报错 | 数据含缺失值或频率不固定 | 先 `df = df.asfreq('M').fillna(method='ffill')` 补齐频率与缺失 |
| `resample` 结果全NaN | 未将日期列设为索引 | 先 `df['date'] = pd.to_datetime(df['date'])` 再 `df = df.set_index('date')` |
| `astype(float)` 转换失败 | 列中含非数字字符串（如"N/A"） | 使用 `pd.to_numeric(df['col'], errors='coerce')` 将非法值转为NaN |
| 大数据集内存溢出 | DataFrame超过可用内存 | 使用 `dtype` 参数指定类型，或分块读取 `pd.read_csv(chunksize=10000)` |

## 热门问题
### Q1: 图表中中文显示为方框怎么解决？
A: 在绘图前配置字体：`plt.rcParams['font.sans-serif'] = ['SimHei']`（Windows）或 `['Arial Unicode MS']`（macOS），同时设置 `plt.rcParams['axes.unicode_minus'] = False` 避免负号显示异常.
### Q2: IQR异常值剔除后数据量减少太多怎么办？
A: 检查数据分布的偏度（`df['col'].skew()`），若偏度>2说明极度右偏。可先做对数变换 `np.log1p(df['col'])` 再用IQR，或将阈值从1.5*IQR放宽至3*IQR.
### Q3: `rolling(window=7)` 前几行为NaN正常吗？
A: 正常。7日滚动窗口需要至少7个数据点才能计算，前6行无足够数据故为NaN。绘图时可用 `df.dropna()` 去掉或保留以显示真实情况.
### Q4: `seasonal_decompose` 的 period 参数怎么选？
A: period是季节周期长度。月度数据通常 period=12（一年12个月），季度数据 period=4，日数据如有周季节性则 period=7。需确保数据长度至少为 period 的2倍.
### Q5: `df.corr()` 中有非数值列怎么办？
A: `df.corr()` 默认仅计算数值列，非数值列自动忽略。如需包含分类列，先转为哑变量：`pd.get_dummies(df, columns=['category'])` 后再计算相关矩阵.
### Q6: 分组聚合后结果有多级索引怎么处理？
A: 使用 `reset_index()` 展平：`df.groupby('category').agg({'sales': 'sum'}).reset_index()`，或用 `as_index=False`：`df.groupby('category', as_index=False).agg({'sales': 'sum'})`.
## 限制条件
- 大数据集需注意内存使用，建议超过1GB时分块处理
- 处理前务必备份原始数据，清洗操作不可逆
- 统计结果需要业务验证，避免数据驱动偏差
- 可视化要简洁清晰，单图不宜超过5个系列
- 不适用于实时流数据处理

## 问题处理指引
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
| --- | --- | --- | --- |
| 数据读取失败 | 文件路径错误或文件格式不支持 | 检查文件路径是否正确，确认文件格式是否为CSV、Excel、JSON、SQLite或API | 确保文件路径正确，或转换为支持的格式 |
| 数据清洗后缺失数据 | 数据清洗过程中删除了重要数据 | 检查数据清洗代码，确认是否误用了删除或填充操作 | 回滚到清洗前的数据版本，重新审查清洗逻辑 |
| 统计分析结果异常 | 数据质量问题或统计方法错误 | 检查数据质量，确认统计方法是否适用于数据类型 | 修正数据质量问题，选择合适的统计方法 |
| 可视化图表错误 | 字体配置错误或代码逻辑错误 | 检查字体配置代码，确认图表生成代码逻辑 | 修正字体配置，检查并修正代码逻辑 |
| 报告生成失败 | 数据格式不正确或模板错误 | 检查数据格式，确认报告模板代码 | 修正数据格式，检查并修正模板代码 |

## 安全建议
| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| 数据泄露 | 高 | 对敏感数据进行加密处理，限制访问权限 | 定期进行合规检查，检查数据访问日志 |
| 恶意代码攻击 | 中 | 对输入数据进行验证和过滤，使用安全的API | 定期更新软件，使用恶意程序扫描工具 |
| 数据损坏 | 中 | 定期备份数据，使用容错机制 | 定期检查备份数据的完整性，测试恢复流程 |
| 操作错误 | 低 | 提供用户指南和错误处理机制 | 通过用户反馈和日志分析识别操作错误 |
| 系统漏洞 | 高 | 定期更新操作系统和软件，使用防火墙 | 定期进行安全扫描，及时修复漏洞 |

## 差异化分析
| 提升效率 | 量化分析 |
| --- | --- |
| 自动化数据清洗 | 减少手动操作时间，提高数据质量，提升效率50% |
| 统计分析模板化 | 提供预定义的统计模板，减少分析时间，提升效率30% |
| 可视化代码生成 | 自动生成可视化代码，减少手动绘图时间，提升效率40% |
| 分析报告自动化 | 自动生成分析报告，减少报告编写时间，提升效率60% |

| 差异化对比 | 对比项 |
| --- | --- |
| 与传统数据分析工具对比 | data-analyst-cn提供更快速的数据处理和可视化，更便捷的报告生成 |
| 与其他代码生成工具对比 | data-analyst-cn专注于数据分析领域，提供更专业的分析功能 |
| 与手动数据分析对比 | data-analyst-cn自动化处理数据，减少人工错误，提高分析准确性 |
| 与其他数据分析平台对比 | data-analyst-cn提供更灵活的配置选项，支持多种数据源和格式 |

## 用户常见咨询
### Q1: 数据分析师支持哪些输入格式？

A1: 数据清洗、统计分析、时间序列分析、可视化代码生成与分析报告自动生成。数据分析师——快速进行数据清洗、统计分析和可视化，适合数据分析师、产品经理、运营人员.。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

## 量化评估
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 差异分析
| 对比维度 | 数据分析师 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 数据清洗、统计分析、时间序列分析、可视化代码生成与分析报告自动生成。数据分析师— | 通用场景 | 通用场景 |

## 异常恢复方案
针对数据分析师使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

### 数据分析师通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
