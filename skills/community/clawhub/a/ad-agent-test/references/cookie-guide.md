# Cookie获取详细指引

## 方法1：adhome免登录（推荐）

适用于有 adhome 权限的腾讯内网用户。

### 操作步骤

1. 打开 adhome 后台
2. 找到目标广告主账户
3. 点击"免登录"按钮，选择平台为"大投放"
4. 页面跳转到 ad.qq.com 并自动登录
5. 确认已进入 Agent 页面（URL含 `/agent`）
6. F12 打开开发者工具 → Console
7. 输入 `document.cookie` 回车
8. 复制完整输出发送

### 注意事项
- 免登录Cookie约2小时有效
- 每次免登录会生成新的session
- 如遇"登录态过期"需重新免登录

## 方法2：手动登录

1. 打开 https://ad.qq.com
2. 微信扫码或QQ登录
3. 进入对应账户的Agent页面
4. F12 → Console → `document.cookie`

### Cookie验证

拿到Cookie后可快速验证关键字段是否存在：
```
gdt_mlogin=xxx     ← 必须有
gdt_owner=xxx      ← 必须有（账户ID）
```

缺少这两个字段说明Cookie不完整，需重新获取。

## 常见问题

**Q: Cookie字符串太长，发不过来？**
A: 正常的，完整Cookie通常1-3KB。可以分段发送或存为文件。

**Q: 报错"Cookie已过期"？**
A: 重新走一遍免登录流程获取新Cookie。

**Q: 截图中文显示方块？**
A: 服务器缺中文字体，运行 `yum install -y google-noto-sans-cjk-sc-fonts`。
