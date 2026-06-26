# Bilibili 收藏夹 ID (fid/media_id) 获取指南

## 方法一：URL 直接查看

在 Bilibili 网页版打开你的收藏夹，地址栏 URL 中包含 `fid` 或 `media_id` 参数：

```
https://space.bilibili.com/你的UID/favlist?fid=3220842352&ftype=create
                                        ^^^^^^^^^^^^^^
                                        这就是收藏夹 ID
```

或者：

```
https://www.bilibili.com/medialist/ml3232323232
                                 ^^^^^^^^^^^^^
                                 这是 media_id
```

**收藏夹 ID** 就是 URL 中的数字部分（`fid=xxx` 或 `ml` 后面的数字）。

## 方法二：F12 控制台查看

1. 打开收藏夹页面
2. 按 `F12` → **Console（控制台）**
3. 在控制台输入：
   ```javascript
   window.__INITIAL_STATE__.mediaListInfo.media_id
   ```
4. 回车，即可看到收藏夹的 `media_id`

## 方法三：API 调试

1. 打开 Bilibili 任意页面
2. `F12` → **Network** → 过滤 `fav`
3. 找到 `fav/resource/list` 请求
4. 查看 Query String Parameters 中的 `media_id` 参数

## 获取用户 UID

如果需要查询他人的公开收藏夹，还需要 UID：
1. 进入该用户的 B站个人空间
2. URL 中 `space.bilibili.com/` 后面的数字就是 UID
   ```
   https://space.bilibili.com/29383152/
                              ^^^^^^^^^
                              这就是 UID
   ```

## 常见问题

**Q: 我的收藏夹是私人的，能下载吗？**
A: 只要 Cookie 是你自己账号的登录态，私人收藏夹也可以下载。

**Q: 收藏夹 ID 和 media_id 有什么区别？**
A: 本质上同一个数字，在不同 API 中叫法不同。本技能中两个都可以用。

**Q: 怎么知道收藏夹 ID 是多少？**
A: 参考上面的任意一种方法，从 B站网页 URL 或开发者工具中都能看到。
