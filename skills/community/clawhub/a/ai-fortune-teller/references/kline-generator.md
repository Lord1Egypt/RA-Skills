# 人生K线图生成器

## 功能说明

将八字命盘分析结果可视化为「股票K线风格」的运势曲线图。

## 算法逻辑

### 运势分段
根据八字大运流年，将一辈子分为多个运势段：
- 每段10年为主
- 每个阶段赋予1-10的运势评分
- 评分规则：7-10为绿色（吉），4-6为黄色（平），1-3为红色（凶）

### 评分维度
运势评分综合以下维度：
- **事业运**：官星/印星旺衰
- **财运**：财星状态
- **感情运**：配偶星/桃花星
- **健康运**：五行流通情况

## 生成提示词模板

```
Chinese fortune chart styled as a stock market K-line graph showing 100 years of life fortune.
Style: Professional financial chart aesthetic, dark background with glowing neon lines.

Design elements:
- Y-axis: Fortune score 0-100
- X-axis: Age/Year from birth to 100 years old
- Green candles for auspicious years (wealth, career advancement, love success)
- Red candles for challenging years (setbacks, health issues, losses)  
- Yellow candles for neutral/transition years
- Key turning points marked with labels

Title in Chinese: '人生运势K线图 - 一生财富命运曲线'
Subtitle showing birth year and name
Professional financial chart font and style
Mark major life events (marriage, career change, health crisis) with annotations
Bottom legend explaining colors
Clean, modern, Instagram-worthy design
```

## 使用方式

### 命令行调用
```bash
python3 scripts/kline_generator.py '{"name":"张三","birth_year":1995}'
```

### 输出
- 运势分段预览（文字）
- K线图图片链接（24小时有效）
- JSON结果文件

## API依赖

- MiniMax Image Generation API (image-01)
- 模型支持aspect_ratio: 9:16（竖版），1:1（横版）
