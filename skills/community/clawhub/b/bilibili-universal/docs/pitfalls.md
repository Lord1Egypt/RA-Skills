# bilibili-search — 反爬坑 / 调试笔记

## 1. SPA 路由不渲染（最常见）

**症状**: `agent-browser open https://space.bilibili.com/{mid}/upload/video` 后 `document.querySelectorAll('.bili-video-card').length === 0`，但 `main` 区域显示"空间主人还没投过视频"。

**原因**: B 站新版 SPA 在 headless 模式下首次路由跳转有时不触发渲染，DOM 停在了一个空骨架状态。

**解决**:
```python
ab_open(url)
time.sleep(2)
ab_eval("location.reload()")   # 强制二次渲染
time.sleep(6)
```

`bili-fetch.py user` 已内置这个 reload。

---

## 2. wbi 签名失败 (`code=-352` 风控校验失败)

**症状**: 调 `/x/space/wbi/arc/search?mid=...&order=pubdate` 返回 `code=-352`。

**原因**: 新版 UP 主空间 API 需要 `w_rid` + `wts` 签名，需要从 `https://api.bilibili.com/x/web-interface/nav` 拿 `img_url` + `sub_url` 然后按特定算法算。

**本 skill 做法**: **不调这个接口**，直接走 SPA 拿视频列表。需要 wbi 的极少场景可以手动加。

---

## 3. `search` 接口的 `user_id` 参数被忽略

**症状**: `https://api.bilibili.com/x/web-interface/search/type?...&user_id=5294454` 返回的结果里仍混入了其他 UP 主。

**原因**: B 站的 `user_id` 参数在某些 search_type 下不生效，文档不全。

**本 skill 做法**: `bili-fetch.py user-search` 用 `search_type=bili_user` 单独搜用户；UP 主本人视频用 `bili-fetch.py user <mid>` 走 SPA 拿，不依赖 search 过滤。

---

## 4. 评论接口 IP 频控 (`code=-403` 访问权限不足)

**症状**: 连续调 `/x/v2/reply/main` 多次后，开始返回 `code=-403`。

**原因**: B 站评论接口有 IP 级别频控（具体阈值未公开，估计 30-60 次/分钟）。

**本 skill 做法**: harvest 默认每个视频之间 sleep 1s。如果还要稳：
```bash
bili-harvest.py user 5294454 --videos 40 --comments 10 --sleep 2.0
```

---

## 5. search 接口 author 字段带后缀

**症状**: `result[].author` 字段显示 `"逗比的雀巢·昨天"` 而非纯用户名。

**原因**: B 站 search 接口的 author 字段会拼接时间标签。

**本 skill 做法**: 保留原始 `author` 字段，不做裁剪；展示时自己注意。

---

## 6. `video` 接口需要 aid 而脚本用 bvid

**症状**: 想按 `aid` 抓评论但脚本入口只接 bvid。

**解决**: `bili-fetch.py video` 内部自动 `view?bvid=...` 转 aid；`bili-fetch.py comments` 接 BV 号 / aid 都行。

---

## 7. headless Chrome 与 SPA 的兼容

**症状**: 用 agent-browser 打开 UP 主空间偶尔出现 "稍后再看" 按钮覆盖整个卡片，无法点击。

**原因**: B 站 SPA 在 headless 模式下 hover 行为偶尔卡住。

**解决**: 不用 hover，直接 eval 解析 DOM。本 skill 全部 eval 解析，无 hover 依赖。

---

## 8. 弹幕抓取未实现

B 站弹幕接口是 protobuf 格式 (`/x/v2/dm/web/seg.so?type=1&oid={cid}&segment_index=1`)，需要：
1. 先调 `/x/web-interface/view` 拿 `cid`（每个分 P 不同）
2. 再调弹幕接口并 protobuf 解码

本 skill v0.1 不集成，TODO for v0.2。需要的话单独写 `bili-danmaku.py`。

---

## 9. 视频标题里的 `<em class="keyword">`

**症状**: search 结果的 `title` 字段包含 `<em class="keyword">逗比的雀巢</em>` 这种高亮标签。

**本 skill 做法**: `search` 子命令已用 `.replace(/<[^>]*>/g,'')` 清洗；`video` 子命令拿到的标题是原始干净的。

---

## 10. JSON 双层解析

agent-browser eval 返回值永远是双层 JSON：

```python
# JS 端
return JSON.stringify({a: 1})

# Python 端看到的 stdout
"\"{\\\"a\\\":1}\""   # 外层 JSON 加引号, 内层 JSON 转义

# 必须 json.loads 两次
data = json.loads(json.loads(out))
```

所有 `ab_eval(...)` 内部已封装，调用方不用关心。