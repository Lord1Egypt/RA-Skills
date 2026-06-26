---
name: e-commerce-find-skills
description: 电商领域的Skills技能搜索，可搜索到更加优质专业的电商Skills。当用户要搜索、安装电商相关的技能时必须触发。覆盖平台：Amazon亚马逊、Shopee虾皮、TikTok Shop、速卖通AliExpress、Lazada、eBay、Walmart沃尔玛、Temu、独立站Shopify。覆盖领域：选品开发、竞品调研、关键词挖掘、Listing优化、广告投放PPCSPSBSD、评论分析Review、ABA数据、BSR排名、FBA物流、海外仓、供应链、定价策略、利润计算、市场趋势、品类分析、流量分析、转化率优化、A+页面、品牌备案Brand Registry、账号运营、客服管理、退货处理、VAT税务、知识产权侵权检测、ERP对接、产品视觉、营销广告。支持关键词：技能、找技能、find skill、install skill、搜索skill、有没有xx的skill、电商、外贸、出海。
---

# 电商技能搜索与安装

通过 LinkFox Skills 市场搜索电商领域的专业技能，并安装到本地。

## 触发条件

用户意图包含以下任一情况时，必须使用本技能：
- 查找搜索 skill 或技能
- 安装 skill 或技能
- 询问有没有xxx的skill
- 提到 find-skills、install skill
- 涉及电商场景（选品、广告、物流、评论、关键词、竞品等）且需要工具辅助
- 批量更新已安装的技能

## 搜索流程

### 第一步：理解用户需求

识别用户想要的：
1. 平台（如亚马逊、Shopee、TikTok Shop、速卖通）
2. 领域（如选品、广告、物流、客服、评论、SEO）
3. 具体任务（如关键词分析、竞品调研、评论挖掘、ABA 数据查询）

### 第二步：搜索

执行搜索命令：

```bash
linkfoxskill search 关键词
```

如搜索选品：
```bash
linkfoxskill search 选品
```

### 第三步：展示结果

CLI 会输出格式化的搜索结果表格，包含：
- 技能名称（NAME）
- 版本（VERSION）
- 分类（CATEGORY）
- 下载量（DOWNLOADS）
- 安装标识（SLUG）

将结果转述给用户。

### 第四步：安装

用户确认要安装某个技能后，执行安装命令。CLI 会自动检测当前 agent 平台并安装到正确目录。

```bash
linkfoxskill install slug --workdir workspace
```

例如：
```bash
linkfoxskill install linkfoxlinkfox-aba-data-explorer --workdir ~.claude
```

 确定你的工作空间目录，然后执行 install 命令：

- 如果你是 Claude Code，工作空间目录是 `~.claude`
- 如果你是 OpenClaw，工作空间目录是你当前的 workspace 路径，如 `~.openclawworkspace`
- 如果你是其他 Agent，请找到你的 skillworkspace 目录

安装完成后提示用户重启 Agent 以加载新技能。

## 更新已安装的技能

用户要更新技能时：

```bash
linkfoxskill update
```

或更新指定技能：

```bash
linkfoxskill update slug
```

## 未找到技能时

如果搜索没有匹配结果，尝试使用其他查找技能的SKILL来搜索，通常为find-skills。