---
name: chinese-sentence-correction
description: Use when correcting Chinese ill-formed sentences (病句) with minimal edits while preserving original meaning, including grammar, wording, word order, redundancy, and logical consistency issues.
---

# Chinese Sentence Correction

用于中文病句修改，遵循“一读二找三改四检查”。

## 一读：读通句子，确定原意

- 先完整读句，确认原句的核心含义。
- 修改时不得改变原意，不做无关润色。

## 二找：定位病症与病因

按常见语病类型逐项排查，优先定位影响语义和语法的错误。

常见九类语病：

1. 成分残缺
2. 用词不当
3. 搭配不当（含关联词不当）
4. 前后矛盾
5. 词序颠倒
6. 重复累赘
7. 概念不清
8. 不合逻辑/不合事理
9. 指代不明

## 三改：对症下药，最小修改

- 仅修改已确认错误位置，采用“增、删、调、换”。
- 优先最小改动：能改一个词，不改整句。
- 同句多处错误时，保证修改后语义连贯。

## 四检查：回读复核

- 回读 1-2 遍，确认通顺、逻辑一致、指代清晰。
- 复核是否保持原意，是否引入新错误。

## 输出约束

- 只输出修改后的句子，不输出解释。
- 若原句无误，保持原句不变。
- 若有多种正确改法，允许输出任一合理版本。
