# Digest Visible Dedupe Design

## 目标

确保一次日报中同一内容最多只可见一次。这里的“同一内容”分两层：

- 第一阶段必须覆盖确定性重复：同一链接或同一标题在最终日报中只能出现一次。
- 后续增强覆盖事件级重复：不同链接、标题不完全相同但指向同一新闻事件时，尽量只保留一条。

第一阶段采用保守策略，优先解决当前重复展示问题，避免因为过宽的语义去重误删不同角度的内容。

## 背景

当前 pipeline 已在 `scripts/merge-sources.py` 中做了多层去重：

- URL 归一化后的重复删除。
- 标题相似度去重。
- 跨 topic 分配时同一 normalized title 只进入一个 topic。

但最终日报 renderer 还有固定区块，例如 KOL Updates、GitHub Releases、GitHub Trending、Blog Picks、Podcast Remix。这些固定区块会再次从所有 topic article 中抽取指定类型内容。因此同一条内容可能先出现在普通 topic section，又出现在固定 section。

这个问题的根因不完全在 merge 层，而在最终日报的可见输出层：同一 digest render pass 缺少全局可见项注册表。

## 非目标

- 不修改抓取逻辑。
- 不重写 merge scoring 或 topic 分配策略。
- 不在第一阶段引入 aggressive semantic dedupe。
- 不要求 merge JSON 内完全没有重复；第一阶段只保证最终日报可见输出不重复。
- 不改变现有 topic section 排序、score threshold、linkless filtering、chat item shape 或 Discord item shape。

## 推荐方案

在最终 renderer 中引入 digest-scope visible dedupe。

渲染顺序保持现状：先 topic sections，后 fixed sections。普通 topic section 具有保留优先级；固定 section 只补充没有在 topic section 出现过的内容。

核心规则：

1. 每次 render digest 时创建一个可见项注册表。
2. Topic section 成功渲染一条 item 后，把该 item 的 stable key 登记为 seen。
3. Fixed section 构建 visible list 时，先检查 seen；如果 stable key 已出现，则跳过。
4. Fixed section 过滤后为空时，不渲染 header。
5. Discord 和 chat 模板共享同一规则。

这个方案让最终输出具备确定性，同时不破坏 merge JSON 作为调试和后续处理输入的完整性。

## Stable Key 设计

第一阶段使用保守 deterministic key：

1. 首选 normalized URL。
2. 无 URL 时使用 normalized title。
3. URL 和 title 都缺失时不生成 stable key，不参与全局去重。

URL normalization 应对齐 `merge-sources.py` 的现有语义：

- 去掉 `www.`。
- 去掉 query string 和 fragment。
- 去掉 path 尾部 `/`。
- YouTube watch 和 youtu.be 使用 video id 归一。
- URL 解析失败时退回 compact raw URL。

Title normalization 应对齐 `merge-sources.py` 的现有语义：

- 去掉常见 retweet 前缀。
- 去掉常见站点后缀。
- 合并空白。
- 去掉标点并 lower-case。

不建议第一阶段只用模糊标题相似度拦截最终输出，因为日报固定区块经常展示同一来源类型的不同观点。过宽相似度会误杀。

## 数据流

Discord render flow：

```text
render_digest
  create seen registry
  render topic sections and mark visible topic articles
  render fixed sections with seen filtering
  render footer
```

Chat render flow：

```text
render_chat_digest
  create seen registry
  render chat topic sections and mark visible topic articles
  render chat fixed sections with seen filtering
  render footer
```

Topic section 内部仍按现有规则筛选和排序。只有真正进入输出的 item 才会登记 seen，避免 linkless、低分、缺失分数等不可见 item 抢占 dedupe key。

Fixed section 的 `unique_articles` 仍可保留，用于 section 内部同类型去重；visible registry 是跨 section 的最终防线。

## 组件边界

建议在 `scripts/render-acceptance-digest.py` 内新增小型 helper，而不是抽到独立模块：

- `article_dedupe_key(article)`：返回 stable key 或 `None`。
- `VisibleArticleRegistry`：维护 seen keys，提供 `mark(article)` 和 `is_seen(article)`。
- topic render functions 接收 registry，并在输出 item 时调用 `mark`。
- fixed section render functions 接收 registry，并在 visible list 构建阶段跳过 seen item。

这保持改动局部、易审查，也符合 acceptance renderer 当前的单文件边界。

后续如果生产 renderer 与 acceptance renderer 分离更明显，再考虑把 key normalization 抽到共享模块。

## 错误处理和降级

- 缺失 URL 但有 title 的可见 item 使用 title key。
- URL 解析失败时使用 compact raw URL key。
- 缺失 URL 和 title 的 item 不参与 stable dedupe，避免把多个坏数据误判为同一条。
- Fixed section 因去重被清空时直接省略该 section。
- 去重只影响可见输出，不改变 footer 中现有 `Dedup` 数字语义。该数字仍来自 merged data stats。

## 测试计划

新增或扩展 `tests/test_acceptance_digest.py`：

- 同一 URL 同时出现在 topic section 和 KOL Updates，只保留 topic section。
- 同一 URL 同时出现在 topic section 和 Blog Picks，只保留 topic section。
- 同一 URL 同时出现在 topic section 和 Podcast Remix，只保留 topic section。
- 同一 title 且缺少 URL 时，topic section 与 fixed section 只出现一次。
- Fixed section 被 visible dedupe 清空后不渲染 header。
- Chat 模板遵守同一 digest-scope visible dedupe。
- Discord 模板遵守同一 digest-scope visible dedupe。
- Topic section 原有排序、score filtering、linkless filtering 继续保持。

已有 golden tests 应继续保留。若 acceptance fixture 因新增重复场景导致期望输出变化，需要显式更新 golden 并 review diff。

建议验证命令：

```bash
python3 -m unittest tests.test_acceptance_digest -v
python3 -m unittest tests.test_merge -v
python3 -m unittest discover -s tests -v
```

有意改变 golden 时：

```bash
UPDATE_GOLDEN=1 python3 -m unittest tests.test_acceptance_digest -v
git diff -- tests/golden/daily-discord.md tests/golden/daily-chat.md
```

## 后续事件级去重

事件级去重作为第二阶段，建议在第一阶段稳定后再做。可选方向：

- 在 merge 阶段生成 `story_fingerprint`，包含 normalized title tokens、canonical URL domain/path、source type metadata。
- 对已知高重复来源建立 source-specific canonicalizer，例如 GitHub release URL、YouTube URL、X status URL、Reddit external URL。
- 为相似标题建立测试驱动的 fixture，不用裸阈值直接拦截 production 输出。

事件级去重的默认策略应仍然保守：只有高置信重复才折叠，避免删除同一大事件下不同来源的独立信息。

## 风险与缓解

- 风险：固定 section 内容减少，让专门区块显得空。
  - 缓解：这是预期行为；topic section 优先，fixed section 只补充未出现内容。空 section 不渲染。

- 风险：URL normalization 与 merge 层不一致。
  - 缓解：实现时复用相同规则，并添加 YouTube 等已有边界测试。

- 风险：title-only dedupe 误杀。
  - 缓解：只有 URL 缺失时才使用 title key；正常有 URL 的内容优先按 URL 判断。

- 风险：footer `Dedup` 数字与可见 item 数不一致。
  - 缓解：保持现有语义，footer 仍表达 merged data stats；visible dedupe 是渲染层展示约束。

## 验收标准

- 同一 URL 或同一 title 的可见 item 在一次 Discord 日报中最多出现一次。
- 同一 URL 或同一 title 的可见 item 在一次 chat 日报中最多出现一次。
- 当同一内容同时符合 topic section 和 fixed section 时，保留 topic section，跳过 fixed section。
- Fixed section 去重后为空时不输出 header。
- 现有 topic section 排序、score threshold、link format 和 chat item shape 不变。
- 相关 acceptance tests 覆盖重复输入场景。
