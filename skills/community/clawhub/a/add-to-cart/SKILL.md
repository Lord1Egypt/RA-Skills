---
name: add-to-cart
description: |
  多平台电商加购物车/收藏自动化工具。通过 Brave Browser CDP 搜索商品并加入购物车（淘宝/京东）、收藏（拼多多）、或标记"想要"（闲鱼）。依赖 brave-browser-agent skill。不涉及支付，只做到加购/收藏为止。Not for: 价格比较、下单支付、商品推荐、订单管理。
---

# 多平台加购物车 Skill

通过 Brave Browser Agent CDP 协议，自动化多电商平台搜索和加购/收藏。

**支持**: 淘宝（加购）、京东（加购）、拼多多（收藏）、闲鱼（想要）

> ⚠️ **只做到加购/收藏，不涉及支付。** 下单付款由用户自己完成。

---

## 前置条件

1. **Brave 浏览器** 以远程调试模式运行：
   ```bash
   /Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222
   ```
2. **各平台已登录**（淘宝/拼多多/闲鱼必须，京东建议）
3. **brave-browser-agent skill** 已激活（提供 `cdp_exec.py`）

---

## 快速开始

```bash
SKILL_DIR="~/.openclaw/groups/workspace-oc_96ba3f8c3476edac2fb64ee89f842f4e/skills/brave-browser-agent"
CART_DIR="~/.openclaw/groups/workspace-oc_96ba3f8c3476edac2fb64ee89f842f4e/skills/add-to-cart"

# 1. 列出浏览器 tab
python3 $SKILL_DIR/scripts/cdp_exec.py list

# 2. 快捷搜索（任选平台）
$CART_DIR/scripts/add_to_cart.sh taobao "牛奶" price-asc
$CART_DIR/scripts/add_to_cart.sh jd "耳机" price-asc
$CART_DIR/scripts/add_to_cart.sh pdd "玩具"
$CART_DIR/scripts/add_to_cart.sh xianyu "二手书"

# 3. 查看结果
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> "document.body.innerText.substring(0, 8000)"
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/result.png
```

---

## 通用工作流程

```
搜索商品 → 浏览结果 → 进入详情 → 选择规格 → 加购/收藏 → 验证
```

每步操作后 `sleep 3`（搜索/跳转 `sleep 5`），用 `screenshot` + `innerText` 确认。

---

## 各平台要点

### 淘宝 ⚠️ 必须用 API 加购

点击按钮方式会被反爬拦截（显示"成功"但未实际加购）。**必须用 API 方式：**

1. 详情页选规格 → 提取 SKU ID（从 script 标签 JSON）
2. 导航到 `cart.taobao.com`（同域确保登录态）
3. 从 cookie 获取 `_tb_token_`
4. 调用 `https://cart.taobao.com/add_cart_item.htm?item_id=<ID>&sku_id=<SKU>&quantity=1&_tb_token_=<TOKEN>`
5. 验证返回 `cartQuantity` 增加

**天猫详情页**：按钮是动态 JS，需从 `script[44]` 提取 SKU 数据（`skuBase.props` + `skuBase.skus`）。

📖 完整操作代码见 `references/platform-guides.md#淘宝`

### 京东

- 底部按钮区 `.bottom-btns-root` 包含"加入购物车"
- 购物车数量 badge 可验证成功
- 第三方商家页面结构可能不同

📖 完整操作代码见 `references/platform-guides.md#京东`

### 拼多多（收藏）

- 无购物车，操作目标是"收藏"
- 用移动版 `mobile.yangkeduo.com` 更稳定
- SPAN `innerText === '收藏'` 匹配（已验证可靠）
- 需 `scrollIntoView` + `setTimeout(500ms)`

📖 完整操作代码见 `references/platform-guides.md#拼多多`

### 闲鱼（想要）

- 页面结构变化频繁，多用截图
- "想要"按钮可能打开聊天界面（正常）

📖 完整操作代码见 `references/platform-guides.md#闲鱼`

---

## 常见问题速查

| 问题 | 解决 |
|------|------|
| 淘宝加购"成功"但购物车为空 | 用 API 方式，不要点击按钮 |
| 滑块验证码 | 用户手动完成，间隔 5-10 秒再操作 |
| 频繁访问限制 | `sleep 5`，每分钟不超过 5 次操作 |
| 登录态失效 | 浏览器中手动重新登录 |
| SKU ID 不正确 | 购物车显示"请选择款式"，重新提取 |
| 选择器失效 | 先截图查看实际页面，按文字匹配按钮 |

**通用按钮匹配**（选择器失效时）：
```javascript
const buttons = [...document.querySelectorAll('button, a, span, div')];
const target = buttons.find(b => b.innerText.includes('加入购物车'));
if (target) { target.click(); 'clicked'; } else { 'not found'; }
```

---

## 操作规范

1. **每次操作前** `list` 获取最新 tab
2. **操作后** `sleep 3-5` 等待加载
3. **截图保存到** `/tmp/` 目录
4. **不要连续快速操作**：每次点击后等 2-3 秒，搜索间隔 5 秒，同平台每分钟 ≤5 次
5. **双重确认**：`screenshot` + `innerText`

---

## 参考文档

| 文件 | 内容 |
|------|------|
| `references/platform-guides.md` | 各平台完整操作代码和注意事项 |
| `references/platform-selectors.md` | CSS 选择器速查表 |
| `references/experience-log.md` | 历史操作经验记录 |
| `scripts/add_to_cart.sh` | 统一搜索脚本 |
