---
name: Daily-EnglishNews-Reader
version: 1.0.0
description: 单次生成符合i+1学习法的英语阅读材料，自动适配CEFR难度，生成飞书云文档
author: lihua
license: MIT
required_extensions:
  - "@larksuite/openclaw-lark-tools"
tags:
  - 英语学习
  - RSS
  - 自动生成
  - i+1学习法
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "bins": ["python3", "pip3"] },
        "install":
          [
            {
              "id": "lark-plugin",
              "kind": "shell",
              "command": "npx -y @larksuite/openclaw-lark-tools install",
              "label": "Install official Lark/Feishu plugin",
            },
            {
              "id": "pip-deps",
              "kind": "shell",
              "command": "pip3 install requests feedparser",
              "label": "Install Python dependencies (requests + feedparser)",
            },
          ],
      },
  }
---

# English Daily Reader Skill for OpenClaw

## 功能说明
单次生成符合i+1学习法的英语阅读材料，解决两个核心痛点：
1. 自动搜索最新全球高质量文章，内容覆盖全球新闻、经济、科技、科学文化，学英语的同时了解行业资讯
2. 自动适配CEFR英语难度等级（A1/A2/B1/B2/C1），提供刚好匹配水平的学习语料

### 核心特性
✅ 每次调用从4个已经指定的分类RSS源各选1篇高质量文章（全球政治、经济、科技、科学文化）
✅ 改写为指定难度与字数的英文文章
✅ 每篇文章提取指定数量的+1难度生词，附带英文释义和语境例句
✅ 生成新的飞书云文档，直接返回文档链接
✅ 自动去重，不会重复推荐已经生成过的文章

## 使用方法
### 前置检查
使用前请需要确保已安装飞书官方OpenClaw插件：
1. 执行安装命令：`npx -y @larksuite/openclaw-lark-tools install`（安装出错可加`sudo`重试）
2. 安装过程中选择「新建机器人」扫码创建，或「关联已有机器人」
3. 创建完成后在飞书给机器人发任意消息激活，发送`/feishu auth`完成批量授权
4. 验证安装：发送`/feishu start`，返回版本号即安装成功

如果没有安装插件，当用户调用本Skill时你要引导用户完成上述安装步骤。

### 首次使用
当用户第一次调用本Skill时，你需要询问用户以下配置信息，并修改配置文件完成配置：
1. **阅读难度**：显示默认 A2，CEFR等级（A1/A2/B1/B2/C1，难度递增）
2. **每篇文章字数**：显示默认 350 （可自定义）
3. **每篇在文章最后讲解的可能为i+1难度的生词数量**：显示默认 3 个/篇（可自定义）

### 配置文件
所有配置都在`config`目录下，每次运行前读取一次：
- `config/config.json`：基础阅读配置，包含阅读难度、每篇文章字数、每篇讲解生词数量
- `config/rss_sources.json`：预设RSS源，你需要从这里查找用户设置的rss源
- `config/sent_articles.json`：已生成过的文章去重列表，读取过的文章你需要记录在这里，避免下次重复读取

### 调用方式与运行步骤
当用户发送类似意思的指令：`生成英语阅读材料` 或 `调用Daily-EnglishNews-Reader`，你会自动完成以下步骤：
1. 读取`config/rss_sources.json`配置
2. 运行`scripts/random_source_picker.py`，这个脚本会随机从4个rss分类中各选一个RSS源
3. 从每个源挑选一篇完整的且未在`config/sent_articles.json`中记录的高质量文章
4. 按照用户配置的难度、字数改写文章,在不影响理解的前提下，要求用词地道，且尽量保留专业技术用语
5. 在改写后的文章中，根据用户配置的讲解生词数量，在生成的短文中选取可能属于+1难度的生词加粗,在短文末尾列出所有加粗生词的英文释义和在短文中出现的语境例句；
6. 生成全新的飞书云文档，写入4篇文章内容，并附上来源和文章原始URL
7. 返回文档链接给用户
8. 将本次生成的文章的来源、标题、URL记录到`config/sent_articles.json`中，避免后续重复推荐


`config/config.json`默认配置：
```json
{
  "reading": {
    "difficulty": "A2",
    "words_per_article": 350,
    "words_per_article_to_explain": 3
  }
}
```

## 依赖工具
- `python3` 用于RSS源随机选择
- 飞书官方OpenClaw插件：`@larksuite/openclaw-lark-tools`
