# 各平台操作指南

> 操作前务必先 `list` 获取 tab，操作后 `sleep 3-5`。用 `screenshot` + `innerText` 双重确认。

---

## 淘宝 (Taobao)

### 搜索 & 排序

```bash
# 快捷方式
$CART_DIR/scripts/add_to_cart.sh taobao "牛奶" price-asc

# 手动
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://s.taobao.com/search?q=牛奶&sort=price-asc'"
sleep 3
```

| 排序参数 | 说明 |
|---------|------|
| `default` | 综合 |
| `price-asc` | 价格↑ |
| `price-desc` | 价格↓ |
| `sale-desc` | 销量↓ |

### 进入详情页

```bash
# 用商品ID导航
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://item.taobao.com/item.htm?id=<商品ID>'"
sleep 3
```

### ⚠️ 加购方式：必须使用 API

**点击按钮不可靠**（反爬拦截，显示"成功"但未实际加购）。

#### API 加购流程

```bash
# Step 1: 导航到详情页，选规格
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://item.taobao.com/item.htm?id=<商品ID>'"
sleep 5

# Step 2: 选择规格（如有）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var all = document.querySelectorAll('*');
    for(var i=0; i<all.length; i++){
      var t = (all[i].innerText || '').trim();
      if(t.includes('CR2032') && t.length < 30){
        all[i].click();
        return 'selected: ' + t;
      }
    }
    return 'spec not found';
  })()"
sleep 1

# Step 3: 提取 SKU ID（从 script 标签 JSON）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerHTML.match(/skuId['\"]:\\s*['\"](\\d+)['\"]/)[1]"

# Step 4: 导航到购物车页（确保同域 + 登录态）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://cart.taobao.com/cart.htm'"
sleep 4

# Step 5: 获取 token + 调用 API
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(async function(){
    var token = document.cookie.match(/_tb_token_=([^;]+)/)[1];
    var url = 'https://cart.taobao.com/add_cart_item.htm?item_id=<商品ID>&sku_id=<SKU_ID>&quantity=1&_tb_token_=' + token;
    var r = await fetch(url, { method: 'GET', credentials: 'include' });
    return await r.text();
  })()"
# 返回: TB.Detail.CartResult = { "cartQuantity": "20", "cartPrice": "" }
```

### 天猫 SKU 提取（detail.tmall.com）

天猫新版详情页按钮是动态 JS 加载，DOM 不可见。需：

1. 从 `script[44]`（或附近）提取 SKU 数据
2. 结构：`skuBase.props` → 属性定义，`skuBase.skus` → propPath→skuId 映射
3. 找到目标选项的 `vid`，从 `skus` 找对应 `skuId`

```bash
# 提取 SKU JSON
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelectorAll('script')[44].text" | jq -r '...'

# 选择步骤：
# 1. props[0].values 找目标 vid
# 2. skus 数组找 propPath 含该 vid 的 skuId
# 3. 用 skuId 调 API
```

### 验证购物车

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://cart.taobao.com/cart.htm'"
sleep 3
```

### 注意事项

- API 必须从 `cart.taobao.com` 域发起
- 频繁调用触发风控（`rgv587_flag: "sm"`），间隔 10-15 秒
- SKU ID 不正确会导致购物车显示"请选择款式"

---

## 京东 (JD)

### 搜索 & 排序

```bash
$CART_DIR/scripts/add_to_cart.sh jd "耳机" price-asc

# 手动: psort=3 价格↑, 4 价格↓, 5 销量, 0 综合
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://search.jd.com/Search?keyword=耳机&psort=3'"
sleep 3
```

### 进入详情页

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://item.jd.com/<商品ID>.html'"
sleep 3
```

### 选择规格 + 加购物车

```bash
# 截图查看规格
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/jd_sku.png

# 选择规格（innerText 匹配）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var all = document.querySelectorAll('*');
    for(var i=0; i<all.length; i++){
      var t = (all[i].innerText || '').trim();
      if(t.includes('13升普通款') && t.length < 30){
        all[i].click(); return 'selected: ' + t;
      }
    }
    return 'spec not found';
  })()"
sleep 1

# 点击加入购物车（底部按钮区域）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var btn = document.querySelector('.bottom-btns-root');
    if(!btn) return 'bottom-btns-root not found';
    var items = btn.querySelectorAll('div');
    for(var i=0; i<items.length; i++){
      if(items[i].innerText && items[i].innerText.trim() === '加入购物车'){
        items[i].click(); return 'clicked 加入购物车';
      }
    }
    return 'button not found';
  })()"
sleep 2

# 验证购物车数量
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var badge = document.querySelector('[class*=cart-count], [class*=cart-num], [class*=badge]');
    return badge ? 'Cart count: ' + badge.innerText : 'Cart count not found';
  })()"
```

### 注意事项

- `.bottom-btns-root` 包含"加入购物车"和"立即购买"
- 购物车 badge 可验证成功
- 某些商品需选配送地址后才显示价格
- 第三方商家页面结构可能不同

### 验证购物车

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://cart.jd.com'"
sleep 3
```

---

## 拼多多 (PDD) — 收藏

> 拼多多无购物车，操作目标为"收藏"。

### 搜索

```bash
$CART_DIR/scripts/add_to_cart.sh pdd "货车满当当"

# 手动（用移动版页面更稳定）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://mobile.yangkeduo.com/search_result.html?search_key=货车满当当'"
sleep 5
```

### 收藏操作

```bash
# 导航到详情页
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://mobile.yangkeduo.com/goods1.html?goods_id=<商品ID>'"
sleep 3

# 收藏（SPAN innerText 匹配，已验证可靠）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var spans = document.querySelectorAll('span');
    for(var i=0; i<spans.length; i++){
      if(spans[i].innerText === '收藏'){
        spans[i].scrollIntoView({behavior: 'instant', block: 'center'});
        setTimeout(function(){ spans[i].click(); }, 500);
        return '找到收藏按钮，正在点击...';
      }
    }
    return '未找到收藏按钮';
  })()"
sleep 2

# 验证："收藏" → "已收藏"
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var spans = document.querySelectorAll('span');
    for(var i=0; i<spans.length; i++){
      if(spans[i].innerText === '已收藏') return '✅ 收藏成功！';
    }
    return '⚠️ 可能未收藏成功';
  })()"
```

### 注意事项

- 使用移动版 `mobile.yangkeduo.com`，结构更稳定
- 收藏按钮在页面底部，需 `scrollIntoView` 再 `click`
- 通常无需选规格

### 验证收藏夹

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://mobile.yangkeduo.com/user_fav.html'"
sleep 3
```

---

## 闲鱼 (Xianyu) — 想要

### 搜索

```bash
$CART_DIR/scripts/add_to_cart.sh xianyu "二手书"

python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://www.goofish.com/search?q=二手书'"
sleep 3
```

### 点击"想要"

```bash
# 进入详情
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelectorAll('a[href*=\"item\"]')[0].click()"
sleep 3

# 点击"想要"
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(
    document.querySelector('[class*=\"want\"]') ||
    document.querySelector('[class*=\"Want\"]') ||
    document.querySelector('button[class*=\"chat\"]')
  ).click(); 'clicked want'"
sleep 2
```

### 注意事项

- 页面结构变化频繁，多用截图
- "想要"按钮可能打开聊天界面（正常）
- 某些商品需先验证

### 验证

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://www.goofish.com/personal'"
sleep 3
```
