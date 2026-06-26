---
name: social-media-search
description: "社交媒体搜索技能。支持抖音,小红书,b站搜索。当用户提到 /搜索抖音 或 /搜索小红书 或 /B站搜索 时，自动打开对应网站并搜索指定内容，返回搜索结果。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
      },
  }
---

# social-media-search

**社交媒体搜索技能**

支持 **抖音** , **小红书** , **bilibili** 三个平台的搜索功能。

---

## 触发词

### 抖音搜索
- `/搜索抖音`
- `搜索抖音`
- `抖音搜索`
- `在抖音搜索`

### 小红书搜索
- `/搜索小红书`
- `搜索小红书`
- `小红书搜索`
- `在小红书搜索`

### B站搜索
- `/bilibili搜索`
- `/B站搜索`
- `/哔哩哔哩搜索`
- `bilibili搜索`
- `B站搜索`
- `哔哩哔哩搜索`

---

## 抖音搜索

### 已知信息
- **网址**: https://www.douyin.com
- **搜索框 ref**: `e31`（已验证稳定）
- **直接导航**: 可用 ✅

### 推荐执行流程（方式一：直接导航）
```bash
# 直接构建搜索URL
openclaw browser navigate "https://www.douyin.com/search/{搜索关键词}"
openclaw browser wait --time 3000
openclaw browser snapshot --limit 150
```

### 备选执行流程（方式二：使用已知 ref）
```bash
# 使用已知的搜索框 ref=e31
openclaw browser open https://www.douyin.com
openclaw browser type e31 "{搜索关键词}" --submit
openclaw browser wait --time 3000
openclaw browser snapshot --limit 150
```

---

## 小红书搜索

### 已知信息
- **网址**: https://www.xiaohongshu.com
- **搜索框 ref**: `e2`（已验证稳定）
- **直接导航**: 不可用 ❌（会跳转到其他页面）
- **必须使用搜索框方式**

### 执行流程（使用已知 ref）
```bash
# 1. 打开小红书首页
openclaw browser open https://www.xiaohongshu.com/

# 2. 直接使用已知的搜索框 ref=e2 输入内容
openclaw browser type e2 "{搜索关键词}" --submit

# 3. 等待结果加载
openclaw browser wait --time 3000

# 4. 获取搜索结果
openclaw browser snapshot --limit 150
```

### 关键发现
- **搜索框位置**: 页面顶部中央
- **placeholder**: "搜索小红书"
- **ref=e2 验证时间**: 2026-04-15
- **稳定性**: 大型网站结构一般不会频繁变动

---

## B站搜索

### 已知信息
- **网址**: https://search.bilibili.com
- **搜索URL格式**: `https://search.bilibili.com/all?keyword={关键词}`
- **直接导航**: ✅ 可用
- **中文编码**: 自动URL编码

### 执行流程（直接导航）
```bash
# 直接构建搜索URL
openclaw browser navigate "https://search.bilibili.com/all?keyword={搜索关键词}"

# 等待页面加载
openclaw browser wait --time 3000

# 获取搜索结果
openclaw browser snapshot --limit 150
```

### 关键发现
- **URL格式**: 支持直接通过URL参数搜索
- **中文自动编码**: 无需手动处理URL编码
- **结果类型**: 视频列表，包含播放量、弹幕数、时长
- **验证时间**: 2026-04-15

---

## 使用示例

### 抖音搜索示例
```
用户：/搜索抖音 教育行业

执行：
openclaw browser navigate "https://www.douyin.com/search/教育行业"
openclaw browser wait --time 3000
openclaw browser snapshot --limit 150
```

### 小红书搜索示例
```
用户：/搜索小红书 AI工具

执行：
openclaw browser open https://www.xiaohongshu.com/
openclaw browser type e2 "AI工具" --submit
openclaw browser wait --time 3000
openclaw browser snapshot --limit 150
```

### B站搜索示例
```
用户：/bilibili搜索 AI工具

执行：
openclaw browser navigate "https://search.bilibili.com/all?keyword=AI工具"
openclaw browser wait --time 3000
openclaw browser snapshot --limit 150
```

---

## 输出格式

### 抖音输出
```
## 抖音"{搜索词}"搜索结果 - 前五个视频

1. **{视频标题}**
   - @{作者名} · {日期} · {点赞数}赞

2. **{视频标题}**
   - @{作者名} · {日期} · {点赞数}赞
...
```

### 小红书输出
```
## 小红书"{搜索词}"搜索结果

### 大家都在搜
- {相关搜索词1}
- {相关搜索词2}
...

### 搜索结果
1. **{笔记标题}**
   - @{作者名} · {日期} · {点赞数}赞

2. **{笔记标题}**
   - @{作者名} · {日期} · {点赞数}赞
...
```

### B站输出
```
## B站"{搜索词}"搜索结果

1. **{视频标题}**
   - @{UP主名} · {日期} · {播放量}播放 · {弹幕数}弹幕 · {时长}

2. **{视频标题}**
   - @{UP主名} · {日期} · {播放量}播放 · {弹幕数}弹幕 · {时长}
...
```

---

## 使用经验总结

### 核心原则
1. **用户给出确定指令时，直接执行** - 不需要额外的探测/快照操作
2. **已知 ref 直接使用** - 如抖音 e31、小红书 e2
3. **优先使用直接导航** - 如果可用（抖音可用，小红书不可用）

### 平台差异
| 平台 | 直接导航 | 已知 ref | 推荐方式 | 登录检查 |
|------|----------|----------|----------|----------|
| 抖音 | ✅ 可用 | e31 | 方式一（直接导航）| 可能需要 |
| 小红书 | ❌ 不可用 | e2 | 方式二（搜索框）| 可能需要 |
| B站 | ✅ 可用 | - | 方式一（直接导航）| 可能需要 |

### 最佳实践
1. **等待时间** - 建议等待 3 秒让页面完全加载
2. **快照限制** - 使用 `--limit 150` 获取足够的结果内容
3. **中文自动编码** - 无需手动 URL 编码
4. **登录检查** - ⚠️ **重要**：执行搜索后检查页面是否提示需要登录
   - 如页面显示登录提示或无法显示结果，询问用户是否已登录
   - 建议用户登录后重新尝试
   - 部分平台（如B站）可能需要登录才能查看完整搜索结果

### 稳定性说明
- **抖音 ref=e31** - 2026-04-15 验证稳定
- **小红书 ref=e2** - 2026-04-15 验证稳定
- **B站直接导航** - 2026-04-15 验证稳定
- 大型网站结构一般不会频繁变动
- 如 ref 失效，需要重新探测

---

## 依赖

- openclaw browser 插件
- 目标网站可访问

---

## 版本

v1.0.1 - 2026-04-15
- 新增B站搜索支持
- 添加B站搜索触发词：/bilibili搜索、/B站搜索、/哔哩哔哩搜索
- 强化登录检查提示

v1.0.0 - 2026-04-15
- 重命名为 social-media-search
- 新增小红书搜索支持
- 添加平台差异对比表
- 总结使用经验，明确执行原则

v0.1.0 - 2026-04-15
- 验证搜索框 ref=e31 稳定性
- 更新方式二为已知稳定 ref 的快速路径

v0.0.2 - 2026-04-15
- 优化搜索流程，增加直接导航方式
- 添加使用经验总结

v0.0.1 - 2026-04-15
- 初始版本（抖音搜索）
