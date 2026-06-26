# Executor Spec: content-extraction

## Goal

把 router 的执行计划固化成统一的 extractor 规范，保证不同平台输出一致。

## Layer 1: Router

输入 URL，输出：
- source_type
- handler
- fallback_chain
- save_name
- extraction_steps
- failure_modes

## Layer 2: Executor

根据 handler 分发：
- browser executor
- feishu executor
- transcript executor
- web fallback executor

## Layer 3: Normalizer

统一输出：
- title
- author
- source
- url
- summary
-正文
- save_path

## Layer 4: Persistence

长内容优先落盘：
- 默认保存到 `extracted/`
- 文件名优先 title
- 没有 title 就用 source_type
- 同名时后缀追加序号或时间戳

## 固化原则

- 计划和执行分离
- 结构化输出优先
- 失败信息必须可解释
- 不把噪音结果当成功
