---
name: 查询物流指数总分并输出建议
description: 当用户查询物流指数总分时，输出物流指数数据、行业排名、数据分析、定位异常指数、输出运营建议
---

## steps

### 1. 打开承运商概览页面
```bash
openclaw browser open http://jingwe.jdl.com/#/indexCenter/shipperOverview
```

### 2. 获取页面数据
```bash
openclaw browser snapshot
```
筛选条件为输入的承运商名称及统计日期，省份默认全国

3. 定位周环比行业排名下降的主要原因，这里指定为物流指数行业排名下降因为履约时效排名下降
4. 打开指数说明界面，这里指定履约时效排名下降是因为揽收及时率
```bash
openclaw browser open http://jingwe.jdl.com/#/indexCenter/shipperOverview
openclaw browser snapshot
```
5. 读取'2.xlsx'同一承运商在该统计日期的表格数据
6. 定位出主要影响子指标后，读取相同子指标名称的excel文件'揽收及时率异常明细.xlsx'，输出主要影响子指标名称，明细条数，进一步优化方向

## input
- 承运商名称、统计日期

## output
1. 输出承运商名称，统计日期，在统计日期的物流指数分数，行业平均值，行业排名
2. 列出同一承运商在该统计日期T-7至统计日期间的物流指数，并标出统计日期与这7天中最高值的差值是多少，分析趋势
3. 定位出主要影响子指标，这里固定输出为'揽收及时率'，输出承运商在该统计日期的数值是多少
4. 输出承运商在统计日期的异常明细表格中的异常条数，不达标类型分类总结共几类，分别占比是多少