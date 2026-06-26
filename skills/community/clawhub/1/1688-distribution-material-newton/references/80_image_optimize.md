# 图片优化（组合流程）

## 功能说明

图片优化是一个**组合流程**，由以下两个子 skill 组成：

1. **商品图片查询**（`references/30_product_image.md`）— 通过商品 ID 获取主图 URL
2. **图片编辑**（`references/40_image_edit.md`）— 对图片进行 AI 编辑优化

当用户直接提供图片 URL 时，跳过步骤 1，直接执行步骤 2。

## 触发关键词

> 优化图片、优化主图、生成图片、换背景、去水印、AI 生图、场景图

## 完整流程

### 步骤 1：判断输入类型

从用户 query 中判断：

- **用户提供了 1688 商品 ID（纯数字串）** → 执行步骤 2
- **用户直接提供了图片 URL** → 跳到步骤 3

### 步骤 2：商品图片查询

加载并执行 `references/30_product_image.md` 中的流程：

```bash
python3 {baseDir}/cli.py image_info --offer_id 商品ID
```

- 从输出的 `data.main_image_urls` 中取**第一张**作为主图 URL
- 将主图 URL 传入步骤 3

### 步骤 3：图片编辑

加载并执行 `references/40_image_edit.md` 中的流程：

```bash
python3 {baseDir}/cli.py image_optimize \
  --image_urls "主图URL" \
  --prompt "用户原始query" \
  [--size "1:1"] \
  [--offer_id "商品ID"]
```

### 步骤 4：结果展示

成功后向用户展示：

1. 生成的图片：`![优化后的图片](gen_image_url)`
2. 优化说明（reasoning_context 的关键内容）

## 多图并发优化

当用户要求同时优化多张图片时：

1. 先通过步骤 2 获取所有主图 URL
2. 对每张图片**并行**执行步骤 3（各自独立调用 `image_optimize`）
3. 最多支持 **5 张图片**并发优化
4. 每个命令独立处理一张主图

## 与其他子 skill 的区别

| 操作 | 使用的子 skill | 说明 |
|------|---------------|------|
| 图片优化（AI 编辑） | 本流程（图片优化） | 组合流程：图片查询 + 图片编辑 |
| 抠图（白底图） | `references/50_cutout_image.md` | 独立子 skill，不经过图片编辑 |
| 只查看商品图片 | `references/30_product_image.md` | 仅查询，不做编辑 |
