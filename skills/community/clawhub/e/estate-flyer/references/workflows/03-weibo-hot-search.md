# 03-weibo-hot-search.md

## 目标
先扫描今日微博热搜，再决定是否联动。

## 默认工具
调用：
- `scripts/call_weibo_hot_search.py`

该脚本默认转调：
- `vendor/weibo-hot-trend/scripts/weibo.js`

## 要求
- 至少抓取前 10 条热搜
- 必须保存抓取时间
- 必须拿到标题、热度、链接
- 结果必须进入最终输出
