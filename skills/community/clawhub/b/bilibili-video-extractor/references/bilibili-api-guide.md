# B站API调用参考（优化版）

## 目录
- [视频信息API](#视频信息api)
- [弹幕API](#弹幕api)
- [评论API](#评论api) **新增**
- [搜索API](#搜索api) **新增**
- [UP主信息API](#up主信息api) **新增**
- [注意事项](#注意事项)
- [常见错误](#常见错误)

---

## 视频信息API

### 接口地址
- BV号查询: `https://api.bilibili.com/x/web-interface/view?bvid={BV号}`
- AV号查询: `https://api.bilibili.com/x/web-interface/view?aid={AV号}`

### 请求头
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com"
}
```

### 完整响应字段
```json
{
  "code": 0,
  "data": {
    "bvid": "BV1xx411c7mD",
    "aid": 170001,
    "title": "视频标题",
    "tname": "视频分区",
    "desc": "视频简介",
    "desc_v2": [{"raw_text": "简介文本"}],
    "owner": {
      "mid": 123456,
      "name": "UP主名称",
      "face": "头像URL"
    },
    "stat": {
      "view": 1000000,
      "danmaku": 5000,
      "reply": 2000,
      "favorite": 3000,
      "coin": 1000,
      "share": 500,
      "like": 8000,
      "his_rank": 100,
      "now_rank": 0,
      "argue_msg": ""
    },
    "duration": 360,
    "pubdate": 1234567890,
    "tags": [
      {"tag_id": 1, "tag_name": "标签1"}
    ],
    "pages": [
      {
        "cid": 12345,
        "page": 1,
        "part": "P1标题",
        "duration": 180
      }
    ],
    "subtitle": {
      "allow_submit": true,
      "list": []
    },
    "interactive": 0,
    "mission_id": 0,
    "no_cache": false,
    "维度": {
      "dx": 0,
      "dy": 0
    },
    "stroy_pv": 0
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| bvid | string | BV号 |
| aid | int | AV号 |
| title | string | 视频标题 |
| tname | string | 视频所属分区 |
| desc | string | 视频简介 |
| owner.name | string | UP主昵称 |
| owner.mid | int | UP主UID |
| stat.view | int | 播放量 |
| stat.like | int | 点赞数 |
| stat.coin | int | 投币数 |
| stat.favorite | int | 收藏数 |
| stat.share | int | 分享数 |
| stat.danmaku | int | 弹幕数 |
| stat.reply | int | 评论数 |
| duration | int | 视频时长(秒) |
| pubdate | int | 发布时间(时间戳) |
| tags | array | 视频标签 |
| pages | array | 分P信息列表 |

---

## 弹幕API

### 接口地址
```
https://api.bilibili.com/x/v1/dm/list.so?oid={cid}
```

### 请求方式
- 方法: `GET`
- 无需特殊认证

### 响应格式（XML）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<i>
  <d p="0.123,1,25,16777215,1234567890,0,abcdef,0">弹幕内容1</d>
  <d p="5.678,5,16777215,16777215,1234567891,0,123456,0">弹幕内容2</d>
</i>
```

### p字段解析
| 位置 | 含义 | 示例值 |
|------|------|--------|
| 0 | 出现时间(秒) | 0.123 |
| 1 | 弹幕类型 | 1=滚动, 4=底部, 5=顶部, 6=逆向, 7=高级, 8=代码, 9=BASS |
| 2 | 字体大小 | 25 |
| 3 | 字体颜色(十进制) | 16777215 |
| 4 | 发送时间戳 | 1234567890 |
| 5 | 弹幕池 | 0=普通, 1=字幕 |
| 6 | 用户ID哈希 | abcdef |
| 7 | 弹幕ID | 0 |

### 注意事项
- 每个分P视频有独立的cid
- 最多返回1000条弹幕
- 需要先获取视频cid才能请求弹幕

---

## 评论API **新增**

### 主评论接口
```
https://api.bilibili.com/x/v2/reply?type=1&oid={aid}&mode={mode}&ps={ps}&pn={pn}
```

| 参数 | 说明 | 可选值 |
|------|------|--------|
| type | 类型(视频=1) | 1 |
| oid | 视频aid | - |
| mode | 排序模式 | 2=最新, 3=最热 |
| ps | 每页数量 | 1-20 |
| pn | 页码 | 1,2,3... |

### 完整响应字段
```json
{
  "code": 0,
  "data": {
    "cursor": {
      "is_begin": true,
      "is_end": false,
      "mode": 3,
      "next": 2
    },
    " Replies": [
      {
        "rpid": 123456,
        "oid": 170001,
        "type": 1,
        "mid": "user123",
        "root": 0,
        "parent": 0,
        "dialog": 0,
        "count": 5,
        "rcount": 3,
        "state": 0,
        "fansgrade": 0,
        "attr": 0,
        "ctime": 1234567890,
        "rpid_str": "123456",
        "root_str": "0",
        "parent_str": "0",
        "like": 100,
        "action": 0,
        "member": {
          "mid": "user123",
          "uname": "用户名",
          "sex": "保密",
          "sign": "签名",
          "avatar": "头像URL",
          "rank": 100,
          "face": "头像URL",
          "fans_detail": null,
          "official_verify": {"type": -1, "desc": ""},
          "vip": {"type": 1, "status": 1, "vip_pay_type": 0}
        },
        "content": {
          "message": "评论内容",
          "plat": 1,
          "device": "string",
          "emote": {},
          "jump_url": {},
          "pictures": null,
          "rich_text": {"emoji_cards": []},
          "at_name_to_mid": {},
          "keyword_cancel": "",
          "emojis": null,
          "settings": {"reaction_card_type": 1}
        },
        "replies": [],
        "assist": 0,
        "folder": {"has_folded": false, "is_folded": false, "rule": ""},
        "up_action": {"like": false, "reply": false},
        "show_follow": true,
        "invisible": false,
        "reply_control": {
          "time_desc": "3天前"
        }
      }
    ],
    "top_replies": [],
    "top_replies_v2": [],
    "hots": [],
    "notice": null,
    "reply_control": {}
  }
}
```

### 子回复接口
```
https://api.bilibili.com/x/v2/reply/reply?type=1&oid={rpid}&pn={pn}&ps={ps}
```

---

## 搜索API **新增**

### 视频搜索
```
https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={keyword}&page={page}
```

### 响应字段
```json
{
  "code": 0,
  "data": {
    "numPages": 100,
    "numResults": 1000,
    "result": [
      {
        "type": "video",
        "id": 170001,
        "author": "UP主",
        "mid": 123456,
        "title": "标题",
        "description": "描述",
        "aid": 170001,
        "bvid": "BV1xx411c7mD",
        "pic": "封面URL",
        "duration": "12:34",
        "play": 100000,
        "video_review": 5000,
        "favorites": 3000,
        "pubdate": 1234567890,
        "tag": "标签1,标签2",
        "desc": "描述"
      }
    ]
  }
}
```

---

## UP主信息API **新增**

### 获取UP主信息
```
https://api.bilibili.com/x/web-interface/card?mid={mid}&photo=true
```

### 获取UP主视频列表
```
https://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&ps={ps}&pn={pn}
```

### 获取UP主粉丝数
```
https://api.bilibili.com/x/relation/stat?vmid={mid}
```

---

## 注意事项

### 1. 请求频率限制
- 普通API: 约100次/分钟
- 搜索API: 约20次/分钟
- 建议添加 0.3-1秒 间隔

### 2. 必须的请求头
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com"
}
```

### 3. 短链接解析
```python
response = requests.head(url, allow_redirects=True)
real_url = response.url
```

### 4. 时间格式化
```python
from datetime import datetime
pubdate_str = datetime.fromtimestamp(pubdate).strftime("%Y-%m-%d %H:%M")
```

---

## 常见错误

| code | 错误 | 解决方案 |
|------|------|----------|
| -404 | 视频不存在 | 检查BV号是否正确 |
| -403 | 访问被拒绝 | 添加Referer头，降低请求频率 |
| -400 | 参数错误 | 检查参数格式 |
| -509 | 请求过于频繁 | 等待后重试，使用代理 |
| -352 | 请求异常 | 风控拦截，更换IP或等待 |

---

## 示例代码

### 完整视频信息获取
```python
import requests
import json

def get_video_info(bvid: str) -> dict:
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com"
    }
    
    resp = requests.get(url, headers=headers, timeout=10)
    data = resp.json()
    
    if data["code"] == 0:
        return data["data"]
    else:
        raise Exception(f"API错误: {data['message']}")

# 使用
info = get_video_info("BV1xx411c7mD")
print(f"标题: {info['title']}")
print(f"播放: {info['stat']['view']}")
```

### 批量获取弹幕
```python
def get_all_danmaku(pages: list) -> list:
    """获取多P视频的所有弹幕"""
    all_danmaku = []
    
    for page in pages:
        cid = page["cid"]
        url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
        
        resp = requests.get(url, headers=headers)
        # 解析XML...
        
        time.sleep(0.3)  # 避免限流
    
    return all_danmaku
```
