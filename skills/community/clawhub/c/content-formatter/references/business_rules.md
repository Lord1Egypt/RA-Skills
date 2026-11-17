# 业务规则 - content-formatter

> 来源: SKILL.md + platform_styles.json 配置

## 4层排版策略

- 规则: L0 无需转换 — Markdown原生平台(掘金/CSDN/思否等)，保持Markdown原文输出
- 规则: L1 通用HTML — 大多数HTML平台(搜狐/大鱼/网易等)，Markdown→HTML + 默认内联CSS
- 规则: L2 平台专属 — 微信公众号/知乎/百家号/微博，调用format_converter专属样式，失败降级L1
- 规则: L3 纯文本 — Twitter/X等短文本平台，去除Markdown标记 + 字符截断
- 来源: SKILL.md§4层排版策略

## 平台清单规则

- 规则: L0平台(9个): juejin, csdn, segmentfault, cnblogs, 51cto, oschina, yuque, imooc, jianshu, woshipm, bilibili_col
- 规则: L1平台(13个): toutiao, douban, sohu, dayu, netease, yidian, smzdm, xueqiu, eastmoney, douyin_img, sohufocus, wordpress, typecho
- 规则: L2平台(4个): wechat_official, zhihu, baijiahao, weibo
- 规则: L3平台(1个): x_twitter
- 来源: SKILL.md§29平台清单

## 降级规则

- 规则: 未知平台 → 默认使用 L1 通用HTML排版
- 规则: L2专属排版器不可用(format_converter.py不存在) → 降级到 L1 通用HTML
- 规则: L2专属排版器调用失败(超时/返回错误) → 降级到 L1 通用HTML
- 规则: markdown库未安装 → 使用简单正则替换进行基础转换
- 来源: SKILL.md§异常处理

## 输入参数规则

- 规则: --content（必填）: 原始内容，Markdown格式
- 规则: --platform（必填）: 目标平台名称
- 规则: --format（可选）: 目标格式(html/markdown/text)，留空则按平台配置自动判断
- 规则: --content-file（可选）: 内容文件路径，替代--content（适合长文本）
- 来源: SKILL.md§输入格式

## 输出字段规则

- 规则: html — HTML格式内容（L0/L3平台为空字符串）
- 规则: markdown — Markdown原文（L3平台为转换后的纯文本）
- 规则: text — 纯文本内容（仅L3平台有值）
- 规则: format_used — 实际使用的格式(html/markdown/text)
- 规则: layer — 实际使用的排版层级(L0/L1/L2/L1(fallback))
- 来源: SKILL.md§输出格式

## 统一排版入口规则

- 规则: 整合base.py的_ensure_content_format、format_converter.py、content_platform_adapter.py三处分散排版入口
- 规则: 被multi-publisher-mcp/publishers/base.py的_ensure_content_format方法调用
- 规则: 调用方式为subprocess子进程调用，失败时降级到base.py内置的format_converter路径
- 来源: SKILL.md§集成说明

## L3纯文本截断规则

- 规则: L3平台按 max_length 截断内容
- 规则: 截断前去除所有Markdown标记
- 来源: SKILL.md§4层排版策略 + 工作流3
