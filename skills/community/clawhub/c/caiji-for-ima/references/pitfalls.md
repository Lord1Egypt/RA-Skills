# 检索与效率复盘（2026-08-31 实测）

## 检索（搜狗微信通道）
- 可用端点：`https://weixin.sogou.com/weixin?type=2&query=<urlencode>&page=N&ie=utf8`，每页 10 条，`&page=` 翻页。
- 字段：标题 `a[uigs^="article_title_"]`、链接 `<h3><a href="/link?url=...">`（相对路径需补全域名）、公众号 `span.all-time-y2`、时间 `<script>timeConvert('...')</script>`。
- 限流分两级：① 搜索列表页频率高返空，降频到 ~1.5–2s/词可避免；② link 跳转页偶发验证码，此时应停止并等待 4–8h 再试，切勿连续重试。→ 策略：先一口气跑完搜索拿全量元数据，link 解析/导入交给 IMA（直接 import_urls 搜狗 link，IMA 自己抓正文）。
- **脚本 `batch_search.js` 已含会话 cookie 刷新 + 增量落盘 + 2 次重试 + 限流冷却退避**，直接后台跑，别手调。
- 关键词词数收窄（40×2≈3min 无阻塞）远优于广撒网（50 词曾卡 39min+）。

## 导入提速
- 拆波并行：53 批 → 5 波（每波 13 批）→ 并行起 5 个子代理各导 1 波，分钟级铺完 530 篇。
- 子代理读自己的 `waves/wave_K.json`（文件美化、URL 单行，不截断），主上下文零开销。
- **folder_id 逐字节核对**（手滑 `...7554` vs `...7754` 报 222000，浪费一轮）。
- 每批间 sleep 0.5s；整批 220001/429 重试一次（间隔 2s）；幂等重试安全。

## 噪声清理（IMA 无删除 API）
- 脏数据两类：① 标题恰好为"搜狗搜索"的验证码中转页；② 广告软文（抗衰/高血压/集训营等）。
- 清理方式：用 `get_knowledge_list` 翻目标文件夹前几页（按 create_time 倒序），用 parent_folder_id + 导入时间窗锁定脏条目，枚举 media_id 交用户在 IMA 界面手动删。
- 清理清单模板（markdown）：
  ```
  # 噪声清理清单
  ## 必删-广告（N 条）
  - <media_id>  <标题>
  ## 可删-验证码页（M 条，主题已被成功导入覆盖）
  - <media_id>  <标题>
  ```

## 交付清单（给用户留底）
- 入库后生成 `<区名>_import_report.md`：KB/folder、入库篇数（ret_code=0 计）、检索覆盖主题词、30 篇标题抽样。
