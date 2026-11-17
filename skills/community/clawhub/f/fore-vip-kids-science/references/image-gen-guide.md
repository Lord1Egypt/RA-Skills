# 配图生成规范（ImageGen · 每段一张）

本技能为答案的**每个小节**各生成 1 张儿童友好插画。本文件规定调用方式、参数、分节提示词策略与安全边界。

## 一、调用方式
- 工具：ImageGen（延迟工具）。若当前会话未直接可用，先用 ToolSearch 加载 `ImageGen` schema，再用 DeferExecuteTool 调用。
- 参数：size = `1024x1024`（正方形，适配图文卡片）。
- 数量：**每段 1 张**（默认 4 节 = 4 张），避免多余生成。

## 二、风格档位（对齐年龄）
| 年龄档 | 画面风格 |
|--------|----------|
| 3–5 岁 | 极简圆润卡通、大色块、拟人化主角、无复杂背景 |
| 6–8 岁（默认） | 明亮绘本风、可爱卡通、1–2 个清晰主体、轻量场景 |
| 9–12 岁 | 略带写实感的科普插画、可含简单示意图元素，仍保持友好 |

## 三、分节生图（每段一张）
按输出模板的 4 节，各给 1 张图，主题对应：

| 小节 | 插画主题 |
|------|----------|
| 一句话答案 | 该问题的核心场景/主角（如仰望蓝天的小孩） |
| 为什么会这样？ | 原理示意（如阳光穿过空气、颜色被弹开） |
| 生活里的小例子 | 生活化场景（如手电筒照灰尘） |
| 冷知识 / 延伸 | 趣味事实或下一个好奇点（如傍晚红天、云朵） |

提示词模板（每节套用对应主题）：
```
Children's book illustration, [本节主题场景], cute and colorful cartoon style, soft rounded shapes, bright palette, friendly and whimsical, no text, no words, safe for kids, [年龄档风格补充]
```

示例（为什么天是蓝的？）：
- 一句话答案：`... a smiling child looking up at a blue sky with scattered soft white clouds ...`
- 为什么会这样：`... sunlight streaming through tiny floating air particles, blue light bouncing around, soft cartoon style ...`
- 生活里的小例子：`... a child shining a flashlight into a dusty room, blue light beam visible, cute cartoon ...`
- 冷知识 / 延伸：`... a sunset with orange and red sky, soft clouds, whimsical cartoon ...`

## 四、配图安全禁区
- 禁止写实血腥、恐怖、阴暗、成人向画面。
- 禁止呈现危险行为（玩火、触电、接触不明液体/动物攻击等）；如需科普危险主题，改用符号化、温和的示意。
- 人体/健康类问题：避免真实伤口、内脏、针管特写；用卡通化、正向表达。
- 不生成含文字/字母的图片（避免误导或乱码）。

## 五、退化策略
- ImageGen 不可用或超时 → 退化为纯文字，并在输出末尾注明「本次未生成配图」；不阻塞主流程。
