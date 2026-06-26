# Alpha Expression Templates

## 模板A：短期反转 + 量能冲击
```text
alpha = rank(-ret_5) + 0.5 * rank(volume / mean(volume, 20) - 1) - 0.5 * rank(std(ret_1, 20))
```
适用：超跌反弹、注意力冲击、量价型研报。

## 模板B：中期动量 + 波动率惩罚
```text
alpha = rank(ret_20) - 0.5 * rank(std(ret_1, 20)) - 0.2 * rank(max_drawdown_20)
```
适用：趋势延续、强者恒强类研报。

## 模板C：基本面质量 + 估值修复
```text
alpha = rank(roe_ttm) + rank(gross_margin_ttm) - rank(pe_ttm) - 0.5 * rank(leverage)
```
适用：财务质量、价值成长类研报。

## 模板D：增强版写法
```text
alpha_enhanced = neutralize(zscore(alpha_raw), industry, log_mktcap)
```
适用：需要行业中性、市值中性的正式复现。

## 使用原则
1. 先给最小可运行版。
2. 若研报有原始定义，优先复原，不要机械套模板。
3. 若只能代理复现，必须写明替代关系。
