# E-commerce Logistics Adapter Selectors

This document contains the actual CSS selectors for each platform, which need to be updated based on the current website structure.

## Taobao (淘宝)

### Order List Page
- URL: `https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm`
- Order items: `.bought-table .order-item` or `[data-spm="order-item"]`
- Order ID: `.order-info .first-row .value` or `.order-no`
- Product title: `.item-title a` or `.production-title`
- Order status: `.order-status` or `.status`
- Logistics button: `.view-logistics` or `.logistics-info a`

### Logistics Detail Page
- Tracking number: `.logistics-num` or `.waybill-num`
- Carrier name: `.logistics-company` or `.carrier-name`
- Timeline items: `.logistics-timeline .timeline-item` or `.logistics-list li`
- Timeline time: `.time` or `.date`
- Timeline content: `.context` or `.detail`

## JD (京东)

### Order List Page
- URL: `https://order.jd.com/center/list.action`
- Order items: `.order-item` or `.order-list-item`
- Order ID: `.order-number` or `.o-number`
- Product title: `.p-name a` or `.goods-name`
- Order status: `.order-status` or `.o-status`
- Logistics button: `.btn-logistics` or `.view-logistics`

### Logistics Detail
- Tracking number: `.logistics-num` or `.waybill-num`
- Carrier: `.logistics-company` or `.carrier`
- Timeline: `.logistics-list li` or `.delivery-list li`

## Pinduoduo (拼多多)

### Order List Page
- URL: `https://mobile.yangkeduo.com/orders.html` (mobile)
- Order items: `.order-item` or `[data-testid="order-card"]`
- Order ID: `.order-id` or `[data-testid="order-id"]`
- Product title: `.goods-name` or `[data-testid="goods-title"]`
- Order status: `.order-status` or `[data-testid="order-status"]`

### Logistics Detail
- URL pattern: `https://mobile.yangkeduo.com/logistics.html?order_sn={orderId}`
- Tracking number: `.tracking-no` or `[data-testid="tracking-number"]`
- Carrier: `.carrier-name` or `[data-testid="carrier"]`
- Timeline: `.logistics-item` or `[data-testid="logistics-timeline"]`

## Douyin (抖音)

### Order List Page
- URL: `https://www.douyin.com/mall/order`
- Order items: `.order-card` or `[data-e2e="order-item"]`
- Order ID: `.order-id` or `[data-e2e="order-id"]`
- Product title: `.goods-title` or `[data-e2e="goods-name"]`
- Order status: `.order-status` or `[data-e2e="order-status"]`

### Logistics Detail
- URL pattern: `https://www.douyin.com/mall/order/logistics?order_id={orderId}`
- Tracking number: `.tracking-number` or `[data-e2e="tracking-no"]`
- Carrier: `.carrier` or `[data-e2e="carrier-name"]`
- Timeline: `.logistics-timeline-item` or `[data-e2e="timeline-item"]`

## Login Page Indicators

### Taobao
- URL contains: `login.taobao.com`, `login.m.taobao.com`
- Elements: `.login-box`, `#J_Quick2Static`, `.login-form`

### JD
- URL contains: `passport.jd.com`, `passport.jd.hk`
- Elements: `.login-tab`, `.login-form`, `#loginname`

### PDD
- URL contains: `mobile.yangkeduo.com/login`
- Elements: `.login-page`, `.phone-login`

### Douyin
- URL contains: `sso.douyin.com`, `douyin.com/login`
- Elements: `.login-container`, `.scan-login`

## QR Code Selectors

Used for taking screenshots of QR codes during login:

- Taobao: `canvas.qrcode`, `.qrcode img`, `[class*="qr-code"]`
- JD: `.login-qrcode img`, `.qrcode-wrapper canvas`
- PDD: `.qrcode img`, `[class*="qr-code"]`
- Douyin: `.scan-login img`, `[class*="qrcode"]`
