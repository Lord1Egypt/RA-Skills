---
name: douyin-search-keyword
description: 抖音公开数据智能获取工具。支持抖音关键词搜索、抖人作品抓取、获取作品评论、实时热榜跟踪，适用于短视频营销、竞品分析、舆情分析和热点监控，助力爆款内容策划与流量追踪。
version: 1.1.5
license: MIT
metadata:
  enabled: true
  type: command
  runtime: "nodejs@16.14.0+"
  requires:
    bins:
      - "node"
    env:
      - "GUAIKEI_API_TOKEN"
  category:
    - "Data&APIs"
    - "内容创作"
  tags:
    - "douyin"
    - "抖音"
    - "search"
    - "搜索"
    - "数据挖掘"
    - "content-analysis"
    - "营销分析"
    - "数据分析"
    - "competitor-analysis"
    - "竞品分析"
    - "评论分析"
    - "热点追踪"
    - "marketing"
    - "trend-tracking"
    - "workflow"
    - "insight"
    - "automation"
  schemas:
    - name: "搜索入参"
      file: "assets/search_cli_req.schema.json"
    - name: "搜索出参"
      file: "assets/search_cli_resp.schema.json"
    - name: "作品入参"
      file: "assets/post_cli_req.schema.json"
    - name: "作品出参"
      file: "assets/post_cli_resp.schema.json"
    - name: "热榜出参"
      file: "assets/hot_cli_resp.schema.json"
    - name: "评论入参"
      file: "assets/comment_cli_req.schema.json"
    - name: "评论出参"
      file: "assets/comment_cli_resp.schema.json"
  examples:
    - name: 搜索"AI 教程"的抖音内容
      command: 'node src/douyin/search-cli.js --keyword "AI 教程"'
      description: 快速获取关键词相关视频数据，助力内容创作灵感
    - name: 搜索 AI 获取最多点赞的抖音内容
      command: 'node src/douyin/search-cli.js --keyword "AI" --sort 1'
      description: 挖掘爆款视频特征，优化内容策略
    - name: 搜索近7天"AI 模型"的抖音内容
      command: 'node src/douyin/search-cli.js --keyword "AI 模型" --time 7'
      description: 追踪近期热点趋势，把握内容窗口期
    - name: 搜索半年内最新20条"AI 教程"的抖音内容
      command: 'node src/douyin/search-cli.js --keyword "AI 教程" --sort 2 --time 180 --limit 20'
      description: 监控长期内容趋势，制定内容规划
    - name: 获取抖人 MS4wLjABxxx 已发布的作品
      command: 'node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"'
      description: 获取抖人已发布的作品，助力竞品分析
    - name: 获取抖音作品 https://www.douyin.com/video/xxx 评论区内容
      command: 'node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx"'
      description: 获取抖音评论详情，分析舆情方向
    - name: 获取抖音实时热搜榜单
      command: "node src/douyin/hot-cli.js"
      description: 实时掌握平台热点，快速响应热门话题
---

# 🚀 抖音关键词搜索、竞品分析、舆情监控与热点跟踪工具 (Douyin Search & Analytics)

> **💡一句话价值**：一键抓取抖音公开视频/作者/评论/热榜数据，帮你做爆款选题、竞品分析、舆情监控、热点追踪。
>
> **🔥核心优势**
>
> - 安全: 无需登录你的抖音账号，不担心风控风险 / 封号问题
> - 强大: 一次可获取最多1W条数据，技能内置批量操作，使用简单方便
> - 全面: 各功能出参数据全面，可见及有价值数据都会返回
> - 灵活: 支持多维度筛选、批量操作
> - 轻量: 无需部署服务，Node.js 一键运行
> - 低耗: 日志自动归档，适配营销报告 / 内容策划场景 ，便于数据二次分析

## 1. ✅ 我能帮你解决什么（10 秒判断）

- 🔍 按关键词搜抖音视频（点赞/最新排序）：找爆款选题、分析高赞视频规律
- 🦸 竞品监控：批量抓取对标账号所有公开作品数据，分析内容策略
- 💬 评论分析：获取抖音评论详情，分析舆情方向
- 📡 热点追流：实时获取抖音热榜，抢占流量风口
- 📊 数据导出：自动生成JSON日志，方便对比分析和使用

## 2. 🚀 最快上手（复制就能跑，30 秒出结果）

> **Note:** 请先通过微信 <13395823479> 申请TOKEN ，或访问[抖音搜索技能官网](https://www.guaikei.com)开通TOKEN，配置环境变量 `GUAIKEI_API_TOKEN` 后才能正常运行。

### 2.1 🔎 抖音关键词搜索（最简单）

```bash
node src/douyin/search-cli.js --keyword "AI"
```

### 2.2 🔎 按点赞排序找爆款（最常用）

```bash
node src/douyin/search-cli.js --keyword "AI" --sort 1
```

### 2.3 🦸 抓取抖音抖人全部作品

```bash
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"
```

### 2.4 💬 获取抖音作品评论内容

```bash
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx"
```

### 2.5 📡 获取抖音实时热榜

```bash
node src/douyin/hot-cli.js
```

## 3. 📌 适用场景（我该不该用？）

- 你需要做短视频选题 → 关键词搜索 + 点赞排序
- 你需要模仿爆款文案 → 查看高赞视频详情
- 你需要监控竞品账号 → 批量抓取对方作品
- 你需要分析内容舆情 → 获取抖音评论详情
- 你需要快速追热点 → 实时获取抖音热榜
- 你需要做营销报告 → 导出结构化数据

## 4. 🔧 参数详解表

> 详细选项参数说明， 可参阅 [完整选项说明](references/options.md)
>
> LLM理解技能的详细选项，可参阅技能 `assets` 目录中文件，其遵循 JSON Schema draft-07 版本规范。
>
> - 抖音关键词搜索，[入参规范](assets/search_cli_req.schema.json)
> - 抖音关键词搜索，[出参规范](assets/search_cli_resp.schema.json)
> - 抖音抖人作品获取，[入参规范](assets/post_cli_req.schema.json)
> - 抖音抖人作品获取，[出参规范](assets/post_cli_resp.schema.json)
> - 抖音评论获取，[入参规范](assets/comment_cli_req.schema.json)
> - 抖音评论获取，[出参规范](assets/comment_cli_resp.schema.json)
> - 抖音热榜获取，[出参规范](assets/hot_cli_resp.schema.json)

## 5. ⚠️ 重要限制（不踩坑）

- 仅抓取抖音公开数据，不支持私密 / 隐藏内容
- 需要配置 GUAIKEI_API_TOKEN 才能正常运行
- 数据仅限个人 / 团队内部使用，禁止违规分发

## 6. ❓ 常见问题（秒解决）

> **💡Q：运行报错，提示无权限？**
>
> A：配置环境变量：
>
> - Windows: `set GUAIKEI_API_TOKEN=你的TOKEN`
> - Linux/MacOS: `export GUAIKEI_API_TOKEN=你的TOKEN`
>
> - 私有TOKEN申请后请留意使用安全，避免泄露给他人
>
> **💡Q：搜索结果为空？**
>
> A：换常用关键词，或把 `--time` 改为 0（全部时间）
>
> **💡Q：输出文件在哪里？**
>
> A：自动保存在技能目录的 `logs` 文件夹下
>
> - 搜索任务日志: 默认保存为「时间戳\_关键词\_排序\_时间\_时长\_search.json」
> - 抖人作品获取日志: 默认保存为「时间戳\_(抖人sec_uid)\_post.json」
> - 抖音评论获取日志: 默认保存为「时间戳\_(视频aweme_id)\_comment.json」
>
> **💡Q：支持 Windows/Mac/Linux 吗？**
>
> A：全平台支持，仅需安装 Node.js 环境

## 7. 📞 帮助与支持

- 联系微信 13395823479（备注抖音技能）开通TOKEN或获得技能使用支持；
- 或通过 [抖音关键词搜索技能官网](https://www.guaikei.com) 自助开通TOKEN或查阅使用帮助。

> 🆕 [更新日志](references/changelog.md) 可查阅这里
