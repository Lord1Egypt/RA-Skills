# 如何获取 app_token 和 table_id

## 方法一：从 Bitable URL 解析

当你打开飞书多维表格，URL 格式通常是：

```
https://xxx.feishu.cn/drive/base/{app_token}?table={table_id}
```

示例：
```
https://pangeedoc.feishu.cn/drive/base/ABCDEFG123456?table=tblABCxyz789
```

- **app_token**: `ABCDEFG123456`
- **table_id**: `tblABCxyz789`

就是这么简单！

## 方法二：从分享链接获取

如果你拿到的是分享链接：

```
https://applink.feishu.cn/client/drive/open?sheet={app_token}/table/{table_id}
```

解析方式相同。

## 创建飞书应用并获取 APP_ID/APP_SECRET

1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 点击「创建应用」→「企业自建应用」
3. 填写应用名称（比如：Bitable 同步工具）
4. 创建后在「凭证与基础信息」页面可以看到：
   - **App ID**: `cli_xxxxxx`
   - **App Secret**: `xxxxxx` (点击获取)
5. 在「权限管理」页面，添加以下权限：
   - `docs:bitable:read`
   - `docs:bitable:write`
   - `docs:document:read`
6. 点击「申请发布」，需要管理员审核通过
7. 回到你的多维表格，点击「分享」，把应用添加为协作者

完成！现在就可以使用了。
