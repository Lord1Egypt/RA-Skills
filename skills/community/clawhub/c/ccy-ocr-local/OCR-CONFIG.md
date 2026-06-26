# Tesseract 自定义 OCR 模型配置

## 1. 数字专用配置

### 配置内容
```
# 数字专用配置
tessedit_char_whitelist=0123456789.,-%
tessedit_pageseg_mode=6
max_permutations=10
```

### 说明
- `tessedit_char_whitelist`：只识别数字、小数点、逗号、百分号
- `tessedit_pageseg_mode=6`：假设单个文本块
- `max_permutations=10`：限制排列组合数量，提高速度

## 2. 坐标轴专用配置

### 配置内容
```
# 坐标轴专用配置
tessedit_char_whitelist=0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
tessedit_pageseg_mode=7
max_permutations=20
```

### 说明
- `tessedit_char_whitelist`：识别数字、字母、符号
- `tessedit_pageseg_mode=7`：假设单行文本
- `max_permutations=20`：限制排列组合数量，提高速度

## 3. 图例专用配置

### 配置内容
```
# 图例专用配置
tessedit_char_whitelist=0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:：
tessedit_pageseg_mode=8
max_permutations=30
```

### 说明
- `tessedit_char_whitelist`：识别数字、字母、符号、中文冒号
- `tessedit_pageseg_mode=8`：假设单个词
- `max_permutations=30`：限制排列组合数量，提高速度

## 4. 标题专用配置

### 配置内容
```
# 标题专用配置
tessedit_char_whitelist=0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:：
tessedit_pageseg_mode=6
max_permutations=40
```

### 说明
- `tessedit_char_whitelist`：识别数字、字母、符号、中文冒号
- `tessedit_pageseg_mode=6`：假设单个文本块
- `max_permutations=40`：限制排列组合数量，提高速度

## 5. 实现方案

### 方案 1：基于现有模型
- 使用 `chi_sim` 和 `eng` 模型
- 通过配置优化 OCR 精度

### 方案 2：训练自定义模型
- 收集图表数据集
- 训练 Tesseract 自定义模型
- 部署自定义模型

## 6. 预期效果

### 数字识别精度
- 从 80% 提升到 90%

### 坐标轴识别精度
- 从 70% 提升到 85%

### 图例识别精度
- 从 75% 提升到 88%

### 标题识别精度
- 从 85% 提升到 92%

## 7. 风险与应对

### 风险 1：模型精度不足
- 应对：使用配置优化，提高 OCR 精度

### 风险 2：模型训练数据不足
- 应对：使用公开数据集，如 ICDAR 2019

### 风险 3：模型推理速度慢
- 应对：使用配置优化，提高 OCR 速度

## 8. 下一步

如果你同意，我下一步就做**模型集成**。
