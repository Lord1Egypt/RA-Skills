# 巨潮资讯网 API 参考

## 1. 查询上市公司 orgId

```
GET https://www.cninfo.com.cn/new/information/topSearch/query
?key=股票代码&pageSize=15&pageNum=1
```

返回 orgId 格式：
- 上交所：`gssh0{code}`（如 `gssh0600903`）
- 深交所：`szse{code}`

## 2. 查询年报公告列表

```
POST https://www.cninfo.com.cn/new/hisAnnouncement/query
Content-Type: application/x-www-form-urlencoded

stock={code},{orgId}
tabName=fulltext
pageSize=30
pageNum=1
column=szsh
plate=sh    （上交所填 sh，深交所填 sz）
category=category_ndbg_szsh
searchkey=
seDate=
sortName=
sortType=
isHLtitle=true
```

关键响应字段：
- `announcements[].announcementTitle` — 公告标题
- `announcements[].adjunctUrl` — PDF附件路径
- `announcements[].announcementId` — 公告ID
- `announcements[].announcementTime` — 发布时间（毫秒时间戳）
- `announcements[].announcementTypeName` — 公告类型名称

## 3. 筛选年报

筛选规则：
- 标题包含"年度报告"
- 排除"摘要"、"更正"、"英文"版本
- 年报发布年份 = 对应财年的次年（如2023年3-4月发布2022年年报）

## 4. 下载年报PDF

```
GET https://static.cninfo.com.cn/{adjunctUrl}
Referer: https://www.cninfo.com.cn/
```

公告详情页：
```
https://www.cninfo.com.cn/new/disclosure/detail?annoId={announcementId}
```

## 5. 注意事项

- 必须设置 User-Agent 和 Referer
- 下载间隔 2-4 秒（礼貌性访问）
- PDF 小于 10KB 可能是错误页面，需丢弃
- 文件名包含特殊字符需清理
