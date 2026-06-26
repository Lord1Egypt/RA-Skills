# 平台CSS选择器参考

本文档整理了各主流平台的CSS选择器，用于数据抓取。

## 抖音 (Douyin)

### 视频页面

| 数据项 | CSS选择器 |
|--------|-----------|
| 点赞数 | `[data-e2e="like-count"]` |
| 评论数 | `[data-e2e="comment-count"]` |
| 分享数 | `[data-e2e="share-count"]` |
| 播放量 | `[data-e2e="play-count"]` |
| 视频标题 | `[data-e2e="video-title"]` |
| 作者昵称 | `[data-e2e="user-name"]` |

### 用户主页

| 数据项 | CSS选择器 |
|--------|-----------|
| 获赞数 | `.like-num` |
| 关注数 | `.follow-num` |
| 粉丝数 | `.follower-num` |

## 小红书 (Xiaohongshu)

### 笔记页面

| 数据项 | CSS选择器 |
|--------|-----------|
| 点赞数 | `.like-wrapper .count` |
| 收藏数 | `.collect-wrapper .count` |
| 评论数 | `.comment-wrapper .count` |
| 笔记标题 | `.title` |
| 作者昵称 | `.author-name` |

### 用户主页

| 数据项 | CSS选择器 |
|--------|-----------|
| 获赞与收藏 | `.follows-num` |
| 关注数 | `.follow-num` |
| 粉丝数 | `.fans-num` |

## 微博 (Weibo)

### 单条微博

| 数据项 | CSS选择器 |
|--------|-----------|
| 转发数 | `.woo-repost-count` |
| 评论数 | `.woo-comment-count` |
| 点赞数 | `.woo-like-count` |
| 阅读量 | `.woo-read-count` |
| 微博内容 | `.weibo-text` |

### 用户主页

| 数据项 | CSS选择器 |
|--------|-----------|
| 关注数 | `.follow_num` |
| 粉丝数 | `.follower_num` |
| 微博数 | `.WB_frame_b .tab .current` |

## B站 (Bilibili)

### 视频页面

| 数据项 | CSS选择器 |
|--------|-----------|
| 播放量 | `.view-text` |
| 弹幕数 | `.dm-text` |
| 点赞数 | `.video-like .like-text` |
| 投币数 | `.video-coin .coin-text` |
| 收藏数 | `.video-fav .fav-text` |
| 分享数 | `.video-share .share-text` |
| 视频标题 | `.video-title` |
| UP主名称 | `.username` |

### 用户空间

| 数据项 | CSS选择器 |
|--------|-----------|
| 关注数 | `.n-followers` |
| 粉丝数 | `.n-fans` |
| 获赞数 | `.n-like` |

## 快手 (Kuaishou)

### 视频页面

| 数据项 | CSS选择器 |
|--------|-----------|
| 点赞数 | `.like-count` |
| 评论数 | `.comment-count` |
| 分享数 | `.share-count` |
| 播放量 | `.play-count` |
| 视频标题 | `.video-title` |

## 淘宝/天猫 (Taobao/Tmall)

### 商品详情页

| 数据项 | CSS选择器 |
|--------|-----------|
| 商品标题 | `.tb-detail-hd h1` |
| 价格 | `.tb-rmb-num` |
| 月销量 | `.sell-count` |
| 累计评价 | `.rate-count` |
| 店铺名称 | `.shop-name` |
| 店铺评分 | `.shop-score` |

## 京东 (JD)

### 商品详情页

| 数据项 | CSS选择器 |
|--------|-----------|
| 商品名称 | `.sku-name` |
| 京东价 | `.p-price .price` |
| 评价数 | `#comment-count` |
| 好评率 | `.percent-con` |
| 店铺名称 | `.shop-name` |

## 拼多多 (PDD)

### 商品详情页

| 数据项 | CSS选择器 |
|--------|-----------|
| 商品名称 | `.goods-name` |
| 价格 | `.price` |
| 已拼数量 | `.sold-num` |
| 店铺名称 | `.shop-name` |

## 选择器使用技巧

### 1. 多选择器备选

当单一选择器不稳定时，可以使用多个选择器：

```python
selectors = [
    '[data-e2e="like-count"]',
    '.video-count .like-count',
    'span[class*="like"]'
]
```

### 2. 等待元素加载

```python
# Playwright
page.wait_for_selector('[data-e2e="like-count"]', timeout=5000)
```

### 3. 处理动态内容

```python
# 等待页面完全加载
page.wait_for_load_state('networkidle')

# 等待JavaScript渲染完成
page.wait_for_timeout(2000)
```

### 4. 提取数字

```python
import re

def extract_number(text):
    # 处理"1.2万"格式
    match = re.search(r'(\d+\.?\d*)\s*万', text)
    if match:
        return int(float(match.group(1)) * 10000)
    
    # 处理普通数字
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    
    return None
```

## 注意事项

1. **选择器可能变化**：平台更新时选择器可能改变，需要定期维护
2. **反爬机制**：频繁抓取可能触发反爬，建议控制频率
3. **动态加载**：部分数据通过JavaScript动态加载，需要等待渲染
4. **登录限制**：部分数据需要登录后才能查看

## 调试方法

### 使用浏览器开发者工具

1. 打开目标页面
2. 按F12打开开发者工具
3. 使用元素选择器工具选中目标元素
4. 右键选择"Copy > Copy selector"获取选择器

### 使用Playwright调试

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://...')
    
    # 暂停等待调试
    page.pause()
```
