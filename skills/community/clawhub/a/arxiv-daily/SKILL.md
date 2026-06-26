---
name: arxiv-daily
description: 每日 arXiv 论文获取加整理技能。当用户想要获取每日 arXiv 论文相关领域论文、设置论文订阅、管理论文推送时间、添加新的论文领域时触发。也用于用户询问"arxiv"、"每日论文"、"论文推送"等相关话题时。
---

# arxiv-daily

每日 arXiv 论文整理技能。

## 功能概述

这个技能帮助用户在指定时间自动获取整理 arXiv 论文，并在指定时间推送总结给用户。

工作流程：
1. **提取**（如 09:38）- 调用 `fetch.py` 获取当天指定领域的论文
2. **推送**（如 14:00）- Agent 读取论文信息，生成总结并推送给用户

## 目录结构

```
arxiv-daily/
├── SKILL.md              # 本文件
├── scripts/
│   └── fetch.py          # 获取论文的脚本
├── references/           # 用户配置文件目录
│   └── like-<category>.txt   # 用户喜好配置
└── data/                 # 论文数据存储目录
    └── <category>/
        ├── YYYY-MM-DD-<category>.txt   # 每日论文数据
        └── YYYY-MM-DD-<category>.md   # 每日论文的翻译总结
```

## 首次使用 / 初始化配置

当用户首次安装、询问或调用此技能时，通过对话引导用户完成初始化：

### 需要询问用户的信息：

1. **感兴趣的领域**
   - 引导用户访问 https://arxiv.org/ 查看分类
   - 确认领域关键字，如 `cs.AI`、`cs.CV`、`cond-mat.mtrl-sci` 等
   
2. **提取时间**
   - 建议在人少的凌晨，如 9:38
   - 记录为 cron 表达式格式
   - 提醒用户注意时区，arxiv在工作日的00:00 UTC更新。

3. **推送时间**
   - 如 14:00
   - ⚠️ **重要**：如果提取时间和推送时间相近，提醒用户拉长间隔
   - 建议：要么更早提取（如 9:00），要么更晚推送（如 20:00）

4. **推送配置**
   - 如： channel: WeCom, account: papa_wecom, chat_id: wecom-agent:LinHaoWei
   - 建议：询问用户是否要通过现在正在使用的聊天渠道推送，并向用户展示当前对话的 channel，account，chat_id

5. **语言偏好**
   - 如：中文

6. **翻译内容**
   - 选项：仅摘要 / 标题+摘要

### 初始化流程：

```
1. 询问上述6个问题
2. 生成配置文件 like-<category>.txt 保存到 references/ 目录
3. 引导用户创建定时器（提取任务 + 推送任务）
4. 确认初始化完成
```

## 配置文件格式

`references/like-<category>.txt` 示例：

```
# arXiv 论文推送配置
category: cs.CV
fetch_time: 38 9 * * *      # 每天早上 9:38
push_time: 0 14 * * *       # 每天下午 14:00
channel: WeCom, account: papa_wecom, chat_id: wecom-agent:LinHaoWei
language: zh-CN
translate: title+abstract  # 可选: abstract-only, title+abstract
```

## 每日提取流程

1. **读取配置**
   - 扫描 `references/like-<category>.txt` 获取对应领域用户配置

2. **调用脚本**
   - 根据读取的配置信息，调用fetch.py脚本

3. **读取论文数据**
   - 根据 `category` 读取最新的 `data/<category>/YYYY-MM-DD-<category>.txt`

4. **生成总结**
   - 对txt文档的**每篇**论文生成 2-3 句话的摘要总结
   - 包含：标题、链接、摘要总结、Comment
   - 保存到 `data/<category>/YYYY-MM-DD-<category>.md`
   - 注意要处理txt文档中所有论文，不要只处理一部分。
   - 总结文档的格式为：

```
今日 arXiv 论文速递 (cs.CV - 2024-01-15)

共 61 篇新论文

1. **论文标题**
   🔗 https://arxiv.org/abs/xxxx.xxxxx

   💡 摘要：这篇论文提出了...（2-3句话总结）

   💬 Comment：CVPR 2026 Main Track

2. **论文标题**
   🔗 https://arxiv.org/abs/xxxx.xxxxx

   💡 摘要：...

   💬 Comment：Project page:this https URL

...

61. **论文标题**
   🔗 https://arxiv.org/abs/xxxx.xxxxx

   💡 摘要：...

   💬 Comment：IEEE

📊 查看全部：https://arxiv.org/list/cs.CV/recent
```

**内容要求**：
- **标题**：原文标题（或翻译后的标题）
- **链接**：arXiv 论文链接
- **摘要**：2-3句话总结论文核心内容
- **Comment**：文章中的comment内容

## 每日推送流程

当到达推送时间时：

1. **读取配置**
   - 扫描 `references/like-<category>.txt` 获取对应领域用户配置

2. **推送**：
   - 根据读取的配置，按照约定的渠道将处理好的当天md文件发送给用户。
   - 发送文案为：

```
🌅 下面将今日 arXiv 论文速递 (cs.CV - 2024-01-15)发送给您。
```

## 添加新领域

当用户想要添加新的论文领域时：

1. 参考「初始化配置」流程，询问同样的5个问题
2. 生成新的配置文件 `like-<new-category>.txt`
3. 引导用户创建新的定时器
4. 确认添加完成

## 脚本使用

### run.sh
```bash
./rscripts/run.sh cs.CV data/cs.CV/ 2026-03-19
```

### fetch.py

```bash
python scripts/fetch.py cs.CV data/cs.CV/ 2026-03-19
```

参数：
- arXiv 分类，如 cs.CV, cs.AI
- 保存路径
- 日期（留空为今日）

## 注意事项

1. **时间间隔**：提取时间和推送时间至少间隔 3 小时以上，确保数据已准备好
2. **多领域支持**：用户可以有多个 `like-*.txt` 配置文件
3. **数据保留**：论文数据保留 7 天，自动清理过期文件
4. **错误处理**：如果某天的数据获取失败，推送时告知用户
5. **周六周日**：arxiv在周六和周日不更新，设置定时任务时可以跳过周六周日。

