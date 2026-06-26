# 特征识别标准规范 v7.0

## 📋 核心目标

本文档定义了 dmp-persona-insight 技能中**特征识别和筛选的完整算法标准**，确保每次分析都按照科学、严谨的方法进行。

---

## 🎯 排序计算方法

### 主排序：TGI 从高到低
```
规则：按特征的 TGI 值从高到低排列
作用：确定特征的热度排名

示例：
  排序前：[母婴 1.90, 健康运动 1.42, 教育学习 1.32]
  排序后：[母婴 1.90, 健康运动 1.42, 教育学习 1.32]  ✓ 已排序
```

### 次排序：占比降序（辅助排序）
```
规则：相同 TGI 时，按占比从高到低排列
作用：在 TGI 相近时进行微调排序

示例：
  特征A：TGI 1.50, 占比 12%  → 排名优先
  特征B：TGI 1.50, 占比 8%   → 排名靠后
```

---

## 🔍 核心特征标准（三步法 v4.0）

### 第 1 步：筛选 TGI ≥ 1.0 的特征

**规则**：
- TGI < 1.0 的特征被排除（无效特征）
- TGI ≥ 1.0 的特征保留（有效特征）

**处理逻辑**：
```python
valid_features = [f for f in features if f['tgi'] >= 1.0]
```

**示例**：
```
维度特征列表：[1.90, 1.42, 1.32, 1.24, 1.23, 0.98, 0.87]
筛选后：      [1.90, 1.42, 1.32, 1.24, 1.23]
排除数：      [0.98, 0.87] → 2 条无效
保留数：      5 条有效特征
```

---

### 第 2 步：在维度内按占比降序排名

**规则**：
- 对已筛选的特征进行相对排名
- 同一维度内比较（不跨维度）
- 占比作为辅助排序依据

**处理逻辑**：
```python
# 已筛选特征按占比降序排序
sorted_features = sorted(valid_features, 
                        key=lambda x: x['coverage'], 
                        reverse=True)

# 添加排名字段
for i, feat in enumerate(sorted_features, 1):
    feat['rank'] = i
```

**示例**：
```
特征1：TGI 1.90, 占比 12%  → 排名 1 ✓
特征2：TGI 1.42, 占比 8%   → 排名 2 ✓
特征3：TGI 1.32, 占比 9%   → 排名 3 ✓
（注：如果 TGI 相同，占比高的排名靠前）
```

---

### 第 3 步：取排名前 40% 的特征（动态阈值）

**规则**：
```
大维度（>50 特征）：最多保留 20 条 → min(int(count * 0.4), 20)
中维度（20-50）  ：取前 40%        → int(count * 0.4)
小维度（<20）   ：至少保留 5-8 条  → max(int(count * 0.4), 5)
```

**处理逻辑**：
```python
def get_core_feature_count(total_count):
    """根据维度大小计算核心特征数"""
    if total_count > 50:
        return min(int(total_count * 0.4), 20)
    elif total_count >= 20:
        return int(total_count * 0.4)
    else:
        return max(int(total_count * 0.4), 5)

core_feature_count = get_core_feature_count(len(valid_features))
core_features = sorted_features[:core_feature_count]
```

**示例**：
```
维度 A：40 条有效特征 → 40 * 0.4 = 16 条  （保留 16 条）
维度 B：12 条有效特征 → 12 * 0.4 = 4.8 → 保留 5 条（最少 5 条）
维度 C：60 条有效特征 → 60 * 0.4 = 24，取 min(24, 20) = 20 条
```

---

## 🔀 并列核心特征识别

### 条件（3 个同时满足）

**条件 1：TGI 差异小**
```
规则：max(TGI) - min(TGI) ≤ 0.2
含义：多个特征的热度接近，不存在明显差异
```

**条件 2：占比差异小**
```
规则：max(占比) / min(占比) < 1.5
含义：多个特征的覆盖面接近，不存在明显差异

示例：
  特征A 占比 12%，特征B 占比 8%
  比值 = 12 / 8 = 1.5 ✗ (等于 1.5，不符合 < 1.5)
  
  特征A 占比 12%，特征B 占比 9%
  比值 = 12 / 9 = 1.33 ✓ (< 1.5，符合)
```

**条件 3：均高于维度平均值**
```
规则：所有候选特征的 TGI 都 > 维度平均 TGI
含义：这些特征都是该维度的相对高热度特征

示例：
  维度平均 TGI = 1.20
  特征A：TGI 1.90 > 1.20 ✓
  特征B：TGI 1.42 > 1.20 ✓
  特征C：TGI 1.32 > 1.20 ✓
```

### 处理方式

**并列识别算法**：
```python
def identify_parallel_features(sorted_features, avg_tgi):
    """识别并列核心特征"""
    parallel_groups = []
    
    for i in range(len(sorted_features)):
        # 从当前特征开始检查是否并列
        group = [sorted_features[i]]
        
        for j in range(i + 1, len(sorted_features)):
            # 检查条件 1：TGI 差异
            tgi_diff = sorted_features[i]['tgi'] - sorted_features[j]['tgi']
            if tgi_diff > 0.2:
                break  # TGI 差异过大，不并列
            
            # 检查条件 2：占比差异
            coverage_ratio = (sorted_features[i]['coverage'] / 
                            sorted_features[j]['coverage'])
            if coverage_ratio >= 1.5:
                continue  # 占比差异过大，检查下一个
            
            # 检查条件 3：均超平均
            if sorted_features[j]['tgi'] > avg_tgi:
                group.append(sorted_features[j])
        
        if len(group) > 1:
            parallel_groups.append(group)
    
    return parallel_groups
```

### 示例

```
维度：兴趣偏好，平均 TGI = 1.20

候选特征：
  母婴    | TGI 1.90, 占比 12%
  健康运动 | TGI 1.42, 占比 8%
  教育学习 | TGI 1.32, 占比 9%

检查：
  TGI 差异：1.90 - 1.42 = 0.48 > 0.2 ✗ （不满足条件 1）
  
结论：各自单独，无并列特征
```

---

## ❌ 排除规则

### 规则 1：逻辑互斥标签

**定义**：两个标签为互斥关系（逻辑上不能同时成立）

**判断标准**：
```
示例互斥对：
  • "苹果手机" ↔ "Android用户"
  • "iOS系统" ↔ "安卓系统"
  • "一二线城市" ↔ "三四线城市"
  • "男性" ↔ "女性"
  • "年轻用户（18-25岁）" ↔ "中年用户（35-45岁）"
```

**处理方式**：
```
规则：保留 TGI 更高的标签，排除 TGI 较低的标签

示例：
  "苹果手机"  TGI 1.36  ✓ 保留
  "Android用户" TGI 0.95 ✗ 排除
  
  原因：苹果手机 TGI 更高，说明人群在苹果用户中的热度更高
```

**实现逻辑**：
```python
def handle_mutually_exclusive(features):
    """处理互斥特征"""
    mutually_exclusive_pairs = [
        ("苹果", "安卓"),
        ("苹果", "Android"),
        ("苹果", "华为"),
        # ... 根据业务规则添加
    ]
    
    features_to_remove = set()
    
    for feat1, feat2 in mutually_exclusive_pairs:
        f1 = next((f for f in features if feat1 in f['name']), None)
        f2 = next((f for f in features if feat2 in f['name']), None)
        
        if f1 and f2:
            # 保留 TGI 较高的
            if f1['tgi'] > f2['tgi']:
                features_to_remove.add(f2['name'])
            else:
                features_to_remove.add(f1['name'])
    
    return [f for f in features if f['name'] not in features_to_remove]
```

---

### 规则 2：无区分度特征

**定义**：两个特征缺乏明显差异，无法有效区分

**判断标准**（2 个同时满足）：

**条件 1：TGI 比值接近 1**
```
规则：0.9 ≤ TGI_A / TGI_B ≤ 1.1
含义：两个特征的热度非常接近

示例：
  特征A：TGI 1.08
  特征B：TGI 1.06
  比值 = 1.08 / 1.06 = 1.019 ✓ (在 0.9-1.1 范围内)
```

**条件 2：占比比值接近 1**
```
规则：0.9 ≤ 占比_A / 占比_B ≤ 1.1
含义：两个特征的覆盖面非常接近

示例：
  特征A：占比 10%
  特征B：占比 10.5%
  比值 = 10 / 10.5 = 0.952 ✓ (在 0.9-1.1 范围内)
```

**处理方式**：
```
方式 1：同时排除两个特征（推荐）
  理由：两个都缺乏区分度，都不是强信号

方式 2：仅保留其一（可选）
  规则：保留该特征对中 TGI 较高的
```

**实现逻辑**：
```python
def remove_low_discrimination_features(features):
    """移除无区分度的特征对"""
    features_to_remove = set()
    
    for i in range(len(features)):
        for j in range(i + 1, len(features)):
            f1, f2 = features[i], features[j]
            
            # 检查 TGI 比值
            tgi_ratio = min(f1['tgi'], f2['tgi']) / max(f1['tgi'], f2['tgi'])
            
            # 检查占比比值
            coverage_ratio = (min(f1['coverage'], f2['coverage']) / 
                            max(f1['coverage'], f2['coverage']))
            
            # 两个条件同时满足
            if 0.9 <= tgi_ratio <= 1.1 and 0.9 <= coverage_ratio <= 1.1:
                # 同时移除两个
                features_to_remove.add(f1['name'])
                features_to_remove.add(f2['name'])
                # 或仅保留 TGI 更高的：
                # if f1['tgi'] > f2['tgi']:
                #     features_to_remove.add(f2['name'])
                # else:
                #     features_to_remove.add(f1['name'])
    
    return [f for f in features if f['name'] not in features_to_remove]
```

### 示例

```
特征对 A：
  特征1：TGI 1.08, 占比 10%
  特征2：TGI 1.06, 占比 10.5%
  
  TGI 比值 = 1.08 / 1.06 = 1.019 ✓ (0.9-1.1)
  占比比值 = 10 / 10.5 = 0.952 ✓ (0.9-1.1)
  
  结论：无区分度 → 同时排除

特征对 B：
  特征3：TGI 1.50, 占比 12%
  特征4：TGI 1.08, 占比 10%
  
  TGI 比值 = 1.08 / 1.50 = 0.72 ✗ (不在 0.9-1.1)
  
  结论：有区分度 → 都保留
```

---

## 📊 完整算法流程

```
【输入】维度的特征列表 (含 TGI、占比)
    ↓
【步骤 1】排序：按 TGI 降序，占比作为次排序
    ↓
【步骤 2】筛选：TGI ≥ 1.0（排除无效特征）
    ↓
【步骤 3】取前40%：根据维度大小计算核心特征数
    ↓
【步骤 4】识别：检查并列核心特征（3条件同时满足）
    ↓
【步骤 5】排除：处理互斥关系（保留 TGI 更高者）
    ↓
【步骤 6】排除：处理无区分度特征（移除或仅保留其一）
    ↓
【输出】最终核心特征列表（已验证、已清理）
```

---

## 🎓 关键数字一览表

| 参数 | 数值 | 含义 |
|------|------|------|
| **TGI 基准线** | ≥ 1.0 | 有效特征的最低 TGI |
| **TGI 差异临界** | ≤ 0.2 | 并列特征的 TGI 差值上限 |
| **占比比例线** | < 1:1.5 | 并列特征的占比比值上限 |
| **前 40% 规则** | 40% | 核心特征的选取比例 |
| **大维度上限** | 20 条 | 大维度（>50 条）最多保留数 |
| **无区分模糊区** | 0.9-1.1 | TGI 和占比比值范围 |
| **小维度最少** | 5 条 | 小维度（<20 条）最少保留数 |

---

## ✅ 检查清单

在输出最终核心特征列表前，确保：

- [ ] 所有特征已按 TGI 降序排列
- [ ] 所有特征 TGI ≥ 1.0
- [ ] 已取前 40%（考虑维度大小）
- [ ] 已检查并列特征条件
- [ ] 已处理互斥关系（互斥的只保留 TGI 高者）
- [ ] 已移除无区分度特征（TGI 比 0.9-1.1 + 占比比 0.9-1.1）
- [ ] 最终列表中无重复
- [ ] 最终列表已验证完整性

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v7.0 | 2026-03-30 | 完整的特征识别算法规范 |
| v6.0 | 2026-03-25 | 初始三步法 |

