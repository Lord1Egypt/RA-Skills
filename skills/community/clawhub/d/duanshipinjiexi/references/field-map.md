# 平台字段映射表

解析响应含 `platform` 字段标识来源。各平台字段结构不同，按表提取，没有的不要编造。

| 发送 | 抖音 | 快手 | 小红书 | 皮皮虾 |
|------|:---:|:---:|:-----:|:-----:|
| 标题 | `data.title` ✅ | `data.title` ✅ | `data.title` ✅ | `data.title` ✅ |
| 作者 | `data.author.name` ✅ | `data.author`(字符串) ✅ | `data.author.name` ✅ | `data.author`(字符串) ✅ |
| 点赞 | `data.stats.liked_count` ✅ | `data.like` ✅ | `data.stats.liked_count` ✅ | ❌ |
| 评论 | `data.stats.comment_count` ✅ | ❌ | `data.stats.comment_count` ✅ | ❌ |
| 分享 | `data.stats.share_count` ✅ | ❌ | `data.stats.share_count` ✅ | ❌ |
| 收藏 | `data.stats.collect_count` ✅ | ❌ | `data.stats.collected_count` ✅ | ❌ |
| 配乐 | `data.music.*` ✅ | `data.music.*` ✅ | ❌ | ❌ |
| 类型 | `data.type` ✅ | `data.type` ✅ | `data.type` ✅ | ❌(默认video) |

## 注意事项

1. **皮皮虾**的 `platform` 返回 `"api"`（不是 `"pipix"`）
2. **快手**的 `data.author` 是字符串（抖音/小红书是 `{name: xxx}` 对象）
3. **小红书**的收藏字段是 `data.stats.collected_count`（不是 `collect_count`）
4. **皮皮虾**无互动数据、无配乐、无 `data.type` → 只发标题和作者

## 发送格式

**文字先发一条**，然后视频/图片/动图逐条单独发。配乐也单独发一条。

文字消息格式：
```
📹 {平台名}
标题：xxx
作者：xxx
👍 1.2万  💬 345  ⭐ 567  🔗 89
📊 今日剩余：8次
```

没有的字段不显示。素材和配乐全部单独发送：

```
🎵 配乐：标题 - 作者名
```
