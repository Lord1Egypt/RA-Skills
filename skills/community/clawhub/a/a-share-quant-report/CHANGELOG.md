# Changelog

## 1.2.0
- 按两类研报范式重构 skill：新增“因子研究型”和“热点跟踪型”分流，不再把所有研报都强行转成同一种多空回测
- 明确引入标准化 Python 回测框架 `python_report_style_factor_backtest.py` 作为可直接采用的基础脚本
- 修复结果展示逻辑：从“文件列表式输出”升级为“研报章节式输出”
- 修复图片展示规范：要求逐张内联展示，并给出图片解释
- 修复图形设计问题：建议拆分双轴图、增强热力图可读性、单独展示多头 vs 基准和多空净值
- 新增 `research-framework-patterns.md`，总结常见量化研究与回测流程
- 新增 `conversation-push-template.md`，规范对话推送顺序
- 输出模板升级到 v1.2，更接近正式金工研报
- skill 版本更新为 1.2.0

## 1.1.0
- 默认 `max_download_stocks` 提升为 1000
- 数据集选择规则更新：正常横截面回测默认目标为至少1000只股票，全市场建议1000~2000只
- 输出模板升级为多因子模型常见回测结构
- 新增因子诊断、IC/RankIC、分层收益、多头/多空/超额绩效、分年收益等模块
- 新增图片展示规范，要求自动内联展示回测过程中生成的全部关键图片并逐图解释

## 1.0.0
- Initial release
- Support A股量化金工研报逻辑拆解
- Support alpha表达式生成
- Support按研报和用户上限决定下载多少只股票回测
- Support回测平台路由：Qlib / RQAlphaPlus / JoinQuant / FinQ4Cn-MCP / QMT-MCP
