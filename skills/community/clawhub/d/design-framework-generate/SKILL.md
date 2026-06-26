---
name: design-framework-generate
description: 设计框架自动生成套件（生图交付）：用户确认后自动生成概念图并私发给 Bot 主人
---

# 设计框架套件 - 生图与交付

「设计框架自动生成套件」的第四个 skill，负责在用户确认后执行生图、私发框架文本和概念图、发送完成通知。

## 触发条件

`/tmp/design-framework-confirmed` 文件存在（由 `design-framework-confirm` skill 写入）。

## 执行流程

1. **删除 confirmed 标记**：防止重复触发
2. **提取宽高比**：从设计框架中解析输出规范
3. **生成概念图**：调用 `generate_image.sh`，使用 `bytedance-seed/seedream-4.5` 模型
4. **私发框架文本**：通过 `send.sh` 发送给 Bot 主人
5. **私发概念图**：通过 `send_image_only.sh` 发送给 Bot 主人
6. **群内完成通知**：发送「已接受，明确需求 ✅」
7. **去重记录 + 清理**：写入 `last-task.txt`，清理所有临时文件，释放锁

## 依赖脚本

所有脚本均位于 `design-framework-sender/` 目录：

- `generate_image.sh`：调用 OpenRouter API 生成图片
- `extract_ratio.sh`：从框架文本提取宽高比
- `send.sh`：私发文本消息
- `send_image_only.sh`：私发图片
- `config.py`：统一配置读取

## 异常处理

- 私发框架失败 → 群内提示失败，清理并退出
- 生图失败 → 群内提示"概念图生成失败"，清理并退出

## 安装说明

请参考 `design-framework-sender` skill 的安装文档。
