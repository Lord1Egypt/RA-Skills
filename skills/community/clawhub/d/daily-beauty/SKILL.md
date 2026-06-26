---
name: daily-beauty
description: 每日美图推送。当用户发送"今日美图"、"美图"、"看美女"等关键词时触发。从小红书搜索真人美女博主，返回1位博主的9张全身照美图。自动排除壁纸号、AI账号、营销号。
---

# 每日美图

从小红书获取真人美女博主的全身照美图，每次返回 **1位博主的9张图片**。

## 触发词

- "今日美图"
- "美图"
- "看美女"
- "推荐美女"

## 执行方式

运行 Python 脚本：

```bash
python3 ~/.openclaw/workspace/skills/daily-beauty/daily_beauty.py
```

脚本会自动：
1. 搜索小红书博主
2. 筛选真人博主（排除已推送的、AI账号、壁纸号、营销号）
3. 下载9张全身照图片
4. 更新去重记录
5. 输出 JSON 格式的结果

## 去重数据文件

- `data/pushed_bloggers.json` - 已推送博主 user_id 列表
- `data/pushed_images.json` - 已推送图片 URL 列表

## 输出格式

```json
{
  "success": true,
  "blogger": {
    "nickname": "昵称",
    "fans": "粉丝数",
    "likes": "获赞数",
    "desc": "简介"
  },
  "images": ["图片路径1", "图片路径2", ...]
}
```

## 推送到飞书

使用 message tool 发送图片：

```
message action=send channel=feishu target=user:ou_2f7b674673f4020ca4a64deda675ccc9 message="博主介绍" path=图片路径
```

## 注意事项

1. 脚本会自动跳过已推送的博主和图片
2. 图片必须是全身照（宽高比 >= 1.3）
3. 博主粉丝数必须 > 1000
4. 自动排除包含黑名单关键词的账号
