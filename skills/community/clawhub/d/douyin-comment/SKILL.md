---
name: douyin-comment
description: 在抖音（douyin.com）上搜索指定关键词的热门视频并发布评论。当用户说「抖音评论」「在抖音上搜 XX 发评论」「抖音互动」「执行：抖音 XX 热门 N 条评论」等涉及抖音搜索+评论的任务时触发本 skill。
---

# 抖音搜索 + 评论 Skill

在托管浏览器（profile=openclaw）中完成：搜索关键词 → 选热门视频 → 发布评论。

## ⚠️ 核心原则

1. **禁止 screenshot**（无 vision 权限）
2. **最多 3-4 次 browser 调用**完成整个流程，避免超时
3. **合并操作**：用单个 evaluate 完成多步操作

## 前置条件

- 浏览器 profile `openclaw` 已启动且已登录抖音账号

## 异常处理

### Gateway 超时处理

如果 browser 工具返回 `timed out` 错误，**自动重启 Gateway**（无需询问用户）：

```bash
pkill -f "node.*openclaw.*gateway" || true
sleep 3
openclaw gateway status  # 验证重启成功（RPC probe: ok）
```

然后继续执行任务。

## 精简流程（3 步完成）

### Step 1: 搜索并获取视频ID

一次调用完成搜索 + 提取视频信息：

```
browser navigate url=https://www.douyin.com/search/关键词?type=video profile=openclaw
```

然后用 **一个 evaluate** 提取视频列表：

```javascript
(() => {
  const text = document.body.innerText;
  // 提取 modal_id 或视频信息
  const videos = [];
  const cards = document.querySelectorAll('li, [class*="card"]');
  cards.forEach((c, i) => {
    const t = c.innerText;
    if (t && t.length > 20 && !t.includes('京ICP')) {
      const plays = t.match(/([\d.]+万?)\n/);
      videos.push({ idx: i, preview: t.slice(0, 80), plays: plays?.[1] });
    }
  });
  return videos.slice(0, 5);
})()
```

从返回结果中选择播放量最高的视频。

### Step 2: 进入视频详情页 + 输入评论

**直接导航到视频详情页**（比点击弹窗更稳定）：

```
browser navigate url=https://www.douyin.com/video/视频ID profile=openclaw
```

等待 3-4 秒让页面完全加载，然后用 **snapshot** 获取评论输入框的 ref：

```
browser snapshot labels=false profile=openclaw
```

找到评论输入框（通常是 `combobox` 类型，内容为"留下你的精彩评论吧"）。

### Step 3: 输入评论（关键：必须用 slowly type）

**⚠️ 重要：必须用 `browser act type slowly` 输入文本**

抖音评论框使用 Draft.js，普通的 evaluate/execCommand 插入文本会导致内部状态不同步，发送按钮保持禁用。

```
browser act kind=click ref=评论框ref profile=openclaw  # 先点击获得焦点
browser act kind=type ref=评论框ref text="你的评论内容" slowly=true profile=openclaw
```

### Step 4: 发送评论

输入完成后，按 **Enter** 键发送：

```
browser act kind=press ref=评论框ref key=Enter profile=openclaw
```

或者等待 Draft.js 状态同步后，发送按钮会自动启用。

## 获取视频 ID 的方法

如果从搜索结果页无法直接拿到视频 ID，点击视频后 URL 会变成：
`https://www.douyin.com/search/xxx?modal_id=7615631792858565903`

提取 `modal_id` 就是视频 ID，然后可以直接访问：
`https://www.douyin.com/video/7615631792858565903`

## 评论质量建议

- 评论应与视频内容相关，15-40 字
- 避免空泛（"好看"、"不错"）
- 示例：「分析到位，终于有人把 OpenClaw 讲明白了！」
