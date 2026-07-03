# 各平台 CSS 选择器参考

> ⚠️ 电商平台前端频繁更新，以下选择器仅作参考。操作前务必先截图确认实际页面结构。

---

## 淘宝 (Taobao)

### 搜索结果页
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 搜索结果列表 | `.items .item`, `[class*="ContentItem"]` | 页面结构变化频繁 |
| 商品标题 | `.title`, `[class*="Title"]` | |
| 商品价格 | `.price`, `[class*="Price"]`, `[class*="price"]` | |
| 商品链接 | `a[href*="item.taobao.com"]`, `a[href*="detail.tmall.com"]` | |
| 商品图片 | `.pic img`, `[class*="mainPic"]` | |

### 商品详情页
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 商品标题 | `[class*="ItemHeader"]`, `[class*="title"]` | |
| 价格 | `[class*="Price"]`, `.tb-rmb` | |
| 规格选择 | `[class*="sku"]`, `[class*="SkuItem"]`, `[class*="skuItem"]` | 颜色/尺码 |
| 加入购物车按钮 | `button[action*="cart"]`, `[class*="addCart"]`, `[class*="cart"]`, `[class*="addToCart"]` | 多种备选 |
| 立即购买按钮 | `[class*="buyNow"]`, `button[action*="buy"]` | 不使用 |
| 数量输入 | `[class*="quantity"] input`, `[class*="Quantity"] input` | |

### 购物车页面
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 购物车列表 | `[class*="cartItem"]`, `[class*="CartItem"]` | |
| 商品标题 | `[class*="itemTitle"]`, `[class*="title"]` | |
| 商品价格 | `[class*="price"]`, `[class*="Price"]` | |

---

## 京东 (JD.com)

### 搜索结果页
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 搜索结果列表 | `.gl-item`, `[class*="gl-item"]`, `#J_goodsList .gl-item` | 相对稳定 |
| 商品标题 | `.p-name a`, `[class*="p-name"]` | |
| 商品价格 | `.p-price i`, `[class*="p-price"]` | |
| 商品链接 | `.p-name a`, `a[href*="item.jd.com"]` | |
| 店铺名称 | `.p-shop a`, `[class*="p-shop"]` | |
| 评论数 | `.p-commit strong a` | |

### 商品详情页
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 商品标题 | `.sku-name`, `[class*="itemInfo"] .sku-name` | |
| 价格 | `.p-price .price`, `#jd-price`, `[class*="price"]` | |
| 规格选择 | `#choose-attr-1 a`, `[class*="choose"] a`, `.sku-item` | 颜色/版本 |
| 加入购物车按钮 | `#InitCartUrl`, `#btn-addtocart`, `[class*="add-to-cart"]`, `a.btn-addtocart` | 多种备选 |
| 数量选择 | `.quantity-input`, `#buy-num` | |

### 购物车页面
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 购物车列表 | `.item-form`, `[class*="cart-item"]` | |
| 商品标题 | `.p-name a` | |
| 去结算按钮 | `#cart-submit`, `.submit-btn` | 不使用 |

---

## 拼多多 (PDD)

> ⚠️ 拼多多 PC 端搜索建议使用 `mobile.yangkeduo.com` 移动版页面，结构更稳定。
> 拼多多没有购物车概念，操作目标是"收藏"商品。

### 搜索结果页（移动版）
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 搜索结果列表 | `[class*="goodsList"]`, `[class*="goods-list"]` | |
| 商品标题 | `[class*="goodsName"]`, `[class*="name"]` | |
| 商品价格 | `[class*="price"]`, `[class*="Price"]` | |
| 商品链接 | `a[href*="goods"]` | |

### 商品详情页
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 商品标题 | `[class*="goodsName"]`, `[class*="title"]` | |
| 价格 | `[class*="price"]` | |
| 收藏按钮 | `[class*="collect"]`, `[class*="favorite"]`, `[class*="star"]` | 无购物车，用收藏替代 |
| 领券按钮 | `[class*="coupon"]` | |

### 收藏列表页面
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 入口 | `https://mobile.yangkeduo.com/user_fav.html` | 个人中心收藏夹 |
| 收藏列表 | `[class*="fav"]`, `[class*="collect"]` | |

---

## 闲鱼 (Xianyu / Goofish)

### 搜索结果页
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 搜索结果列表 | `[class*="feedItem"]`, `[class*="item-card"]`, `[class*="search-item"]` | 结构频繁变化 |
| 商品标题 | `[class*="title"]`, `[class*="desc"]` | |
| 商品价格 | `[class*="price"]` | |
| 商品链接 | `a[href*="item"]`, `a[href*="goofish"]` | |

### 商品详情页
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 商品标题 | `[class*="title"]`, `[class*="desc"]` | |
| 价格 | `[class*="price"]` | |
| "想要"按钮 | `[class*="want"]`, `[class*="Want"]`, `button[class*="chat"]` | 核心操作 |
| 聊天/咨询按钮 | `[class*="chat"]`, `[class*="contact"]` | 辅助入口 |

### 我的闲鱼（已想要/收藏）
| 元素 | 选择器 | 备注 |
|------|--------|------|
| 入口 | `https://www.goofish.com/personal` | 个人中心 |

---

## 通用选择器策略

当平台特定选择器失效时，可尝试以下通用策略：

```javascript
// 查找包含特定文字的按钮
const buttons = [...document.querySelectorAll('button, a, span')];
const target = buttons.find(b => b.innerText.includes('加入购物车'));
if (target) target.click();

// 查找包含特定文字的链接
const links = [...document.querySelectorAll('a')];
const item = links.find(a => a.innerText.includes('<商品关键词>'));

// 按文字模糊匹配
const allElements = [...document.querySelectorAll('*')];
const match = allElements.find(el => el.innerText.includes('目标文字') && el.children.length === 0);
```

---

## 更新记录

| 日期 | 平台 | 变更 | 备注 |
|------|------|------|------|
| 2026-04-27 | 淘宝 | 初始记录 | 欧瑞博小圆红外控制器操作成功 |
| 2026-05-11 | 全平台 | 创建多平台选择器文档 | 从 taobao-cart 扩展为 add-to-cart |
