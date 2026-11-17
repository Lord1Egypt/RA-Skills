---
name: caiji-for-ima
description: "教发老兵实测沉淀的 IMA 知识库补料流水线：按主题检索搜狗微信文章→筛选编码→分批导入 IMA 知识库。仅在你显式要求时运行，导入幂等（不重复）、尊重站点限流，适合给指定知识库文件夹批量补充文章素材。"
agent_created: true
---

# 老兵知识采集器（caiji-for-ima）

## Overview

教发老兵（李琰辉）经过大量实测，把"按主题批量给知识库某文件夹补文章素材"这件事固化成一条流水线：**检索 → 筛选 → 编码 → 拆波分批直导 → 核验 → 噪声清理**。默认目标"至少 100 篇、越多越好"，全程幂等、不空转。目前实现基于 **IMA 知识库（ima.qq.com）+ 搜狗微信检索通道**，可直接复用。

适用场景（用户说类似以下即触发）：
- "给【XX 知识库】的【YY 区】补一些关于『主题』的文章，至少 100 篇"
- "把科研误区/方法论/课题申报这类文章转存到我的知识库"
- 任何"按主题给知识库灌文章素材"的需求

## 安全与适用边界（必读）

本技能在以下边界内运行，安全可审计：

1. **仅显式触发**：只在你明确提出"给某库补文章"类需求时运行；不自动激活、不擅自改动任何知识库。
2. **限流合规（内置护栏）**：检索使用搜狗微信的公开搜索接口；默认每词仅 2 页、总词数≤40、词间间隔 ~1.5–2s，遇到限流自动冷却退避，不做爆破、不绕过任何鉴权。导入前会先与你确认目标知识库、文件夹与篇数目标。
3. **幂等、不删不改**：`import_urls` 对同一 URL 幂等折叠，不产生重复条目；本技能**只做导入、绝不删除**任何知识。若需移除某条，由你在 IMA 界面手动操作（IMA 无删除 API）——导入动作本身可控、可预期。
4. **并发可控**：拆波并行导入是你在确认后发起的批量操作，波数/并发可控，可随时中止。

## 核心原则（效率优先，来自实测）

1. **先搜齐筛好落盘，再分批直导**——绝不反复重搜、绝不串行 sleep 傻等。
2. **检索收窄词数**：40 词 × 2 页 ≈ 3 分钟拿 757 条候选、全程无限流阻塞；广撒网（50 词）曾卡 39 分钟+，勿取。
3. **导入拆波分批**：把批次拆成每波 13 批，每波并行起 1 个子代理各导其波；远优于串行或主 agent 手抄长 URL。
4. **核验以 import_urls 回执 ret_code=0 + media_id 为准**，不以 get_knowledge_list 的 total_size 差值（受并发写入干扰、且幂等折叠会让差值偏小）。

## Workflow

### Step 0 定位目标（必须最先做）
- 用 `get_knowledge_base_list` 遍历 `KBT_MINE_KB` / `KBT_SHARED_KB` / `KBT_SUBSCRIBED_JOIN_KB` / `KBT_SUBSCRIBED_CREATE_KB` 四种类型，找到目标知识库（固定 KB 报 222001/222000 时不要止步，可能已改名重建为共享库）。
- 用 `get_knowledge_list`（knowledge_base_id + folder_id，limit≤50 不带 filter）定位目标文件夹 folder_id。
- 常用基线见 `references/ima_kb_api.md`。

### Step 1 检索（搜狗微信通道）
- 运行 `scripts/batch_search.js`：把关键词写进一个 txt（一行一词），后台跑。脚本已含会话 cookie 刷新、增量落盘、2 次重试、每词默认 2 页，并对限流做自动冷却退避。
- 关键词策略：每个主题拆 3–5 个同义变体（如"科研误区 / 科研踩坑 / 论文写作常见错误 / 学术写作痛点"），总词数控制在 40 左右。
- 输出：`out/all_articles.json`（去重后的候选，含 url/title/source/date）。

### Step 2 筛选 + 编码 + 分批
- 运行 `scripts/filter_topic.py <out目录> [保留篇数]`：
  - 强制标题命中主题词（理论/模型/方法/模板/工具/误区/痛点等，按本次主题调 THEME 表）；
  - 排除广告/中小学/育儿等噪声（JUNK 表）；
  - 内部去重（URL + 标题近似 >0.72）；
  - **URL 统一 `quote()` 编码**——这一步挡掉 220001 的裸空格坑；
  - 输出 `batches.json`（每批 ≤10 条，已编码）。

### Step 3 拆波
- 运行 `scripts/make_waves.py batches.json waves`：拆成 `waves/wave_1..N.json`，每波 13 批。

### Step 4 分批直导（关键提速步）
- **并行起 N 个后台子代理**，每个子代理只读自己的 `waves/wave_K.json`，顺序调用 `import_urls`：
  `{"knowledge_base_id":"<KB>","folder_id":"<folder>","urls":[该波 urls]}`，URL 原样传。
- 子代理要点：每批间 sleep 0.5s；整批报 220001/429 原样重试一次（间隔 2s）；**导入幂等，重试安全**。
- 不要在主上下文里手抄长 URL——子代理 Read 自己的波次文件不会截断。
- ⚠️ folder_id 务必逐字节核对（曾因手滑把 `...7754` 写成 `...7554` 报 222000，浪费一轮）。

### Step 5 核验 + 噪声清理
- 用 `get_knowledge_list` 翻目标文件夹前几页，确认 total_size 增长、create_time 为本轮、标题主题命中。
- 混入的"搜狗搜索"验证码页 / 广告软文：IMA **无删除 API**，只能枚举其 media_id（按 parent_folder_id + 导入时间窗锁定）交用户在 IMA 界面手动清。噪声清理清单模板见 `references/pitfalls.md`。

## 坑点速查

- **220001**：先查 URL 是否含裸空格 → 替换 `%20` 重试；瞬时失败概率也不低，单条重试常成功。
- **幂等**：同 URL 重复导同一文件夹折叠为同一条，不产生重复项——去重可放宽，重试安全。
- **search_knowledge 的 folder_id 不生效**：返回全库命中，需按 parent_folder_id 二次过滤。
- **get_knowledge_list limit≤50**：传 100/200 报错；folder 的 media_type=99，别用 filter 过滤。
- **IMA 无删除/移动接口**：放错库或脏数据只能用户在 UI 手动处理。

详细工具签名与 ID 基线见 `references/ima_kb_api.md`；检索与效率复盘见 `references/pitfalls.md`。
