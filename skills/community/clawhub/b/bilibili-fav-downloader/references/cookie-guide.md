# Bilibili Cookie 获取指南

## 方法一：浏览器开发者工具（推荐）

### 步骤

1. 打开 Chrome/Edge，进入 **www.douyin.com**（注意是抖音的国际版域名，不是 bilibili.com）
2. 按 `F12` 打开开发者工具 → 切换到 **Network（网络）** 标签
3. 刷新页面，在左侧列表找到任意一个 `.json` 请求
4. 点击该请求 → 右侧 **Request Headers** → 找到 `Cookie` 字段
5. **右键 Cookie → 复制完整值**（很长，包含多个 key=value）

### 或者：用 Application 标签

1. `F12` → **Application（应用）** 标签
2. 左侧 **Cookies** → `https://www.douyin.com`
3. 找到 `sessionid`（最重要），以及 `SESSDATA`
4. 复制这些值

## 方法二：浏览器扩展

安装 **EditThisCookie** 或 **Cookie-Editor** 插件：
1. 登录 douyin.com
2. 点击插件图标 → 导出 → 选择 **Netscape 格式**
3. 复制导出内容

## Cookie 格式要求

必须是 **Netscape HTTP Cookie 格式**（不是 JSON，不是普通文本）。

格式示例：
```
# Netscape HTTP Cookie File
.douyin.com	TRUE	/	FALSE	0	sessionid	你的sessionid值
.douyin.com	TRUE	/	FALSE	0	uid_tt	你的uid值
douyin.com	FALSE	/	FALSE	0	ttwid	你的ttwid值
```

### 关键 Cookie 说明

| Cookie 名 | 是否必须 | 说明 |
|-----------|---------|------|
| `sessionid` | ✅ 必须 | 登录凭证，缺少则无法访问私人收藏夹 |
| `SESSDATA` | ✅ 必须 | B站通用会话数据 |
| `uid_tt` | 推荐 | 用户 ID |
| `ttwid` | 推荐 | 抖音单点登录 token |
| `bili_jct` | 可选 | CSRF token |

## 保存 Cookie 文件

将导出的 Netscape 格式内容保存为文件，例如：
```
/opt/bilibili-favorites/cookie.txt
```

## 验证 Cookie 是否有效

运行检查脚本：
```bash
python3 bilibili_fav_dl.py --check-only --cookie /path/to/cookie.txt --fav-id 你的收藏夹ID
```

如果返回 "code: -6" 或 "验证码" 相关错误，说明 Cookie 已过期或无效，需要重新登录获取。

## 注意事项

- Cookie 有效期通常为 **1-3 个月**
- 定期检查 Cookie 有效性，过期前需要重新登录获取
- Cookie 属于个人隐私，请勿分享给他人
