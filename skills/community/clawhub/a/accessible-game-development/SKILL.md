---
name: accessible-game-development
description: Accessible HTML game development for screen readers (Zhengdu, NVDA, JAWS). Supports blind and low-vision users. Trigger keywords: accessible game development, a11y game, 无障碍游戏开发.
---

# 无障碍HTML游戏开发技能

按照《无障碍HTML游戏开发规范》开发适配屏幕阅读器的HTML游戏，支持国内争渡读屏，兼顾全盲/低视力用户。

## 规范文件
[accessible-html-game-development-spec.md](accessible-html-game-development-spec.md) - 完整开发规范

## 使用方式

当用户提到「无障碍游戏开发」、「开发无障碍游戏」、「accessible game」等关键词时，自动触发本技能：

1. 读取完整开发规范
2. 根据规范要求指导/生成无障碍HTML游戏代码
3. 检查代码是否符合无障碍标准（ARIA语义、键盘导航、动态更新等）
4. 提供符合规范的最佳实践建议

## 核心原则

1. **全盲用户体验优先**，兼顾低视力和明眼陪伴
2. 所有操作必须能通过**键盘+屏幕阅读器**完成，不需要鼠标
3. 每个可交互元素必须让读屏读出**完整准确的当前信息**
4. 视觉美观辅助理解，不影响读屏操作

## 检查清单

开发完成后需要验证：
- 所有可交互元素都能Tab聚焦
- 每个可聚焦元素有完整的aria-label包含所有信息
- 状态变化后正确更新所有aria-label
- 常用操作有accesskey快捷键
- 有aria-live状态区域播报动态更新
- 焦点有清晰可见的轮廓
- 颜色区分清晰，兼顾低视力
- 模态对话框正确使用ARIA dialog属性
- 选项选择用按钮直接点击，不需要单选+确认
