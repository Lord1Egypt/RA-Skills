# 1688 商品详情采集

## 触发条件
用户请求采集 1688 商品详情页面，例如：
- "采集这个 1688 商品：https://detail.1688.com/offer/xxx.html"
- "把 1688 商品详情页保存下来"
- "下载 1688 商品图片和详情"

## 执行流程

### 1. 解析 URL 提取商品 ID
```javascript
const offerId = url.match(/offer\/(\d+)\.html/)[1];
```

### 2. 创建保存目录
```
桌面/1688-商品详情-{商品 ID}-图片/
```

### 3. 打开商品页面并等待加载
```javascript
browser.open(url);
browser.act({ kind: 'wait', timeMs: 5000 });
```

### 4. 深度滚动采集所有图片
```javascript
browser.act({
  fn: async () => {
    // 滚动 30 步，每步 1000px，等待 400ms
    for (let i = 0; i < 30; i++) {
      window.scrollBy(0, 1000);
      await new Promise(r => setTimeout(r, 400));
    }
    // 使用 Performance API 获取所有图片
    const urls = performance.getEntriesByType('resource')
      .filter(r => r.name.includes('cbu01.alicdn.com/img/ibank'))
      .map(r => r.name.replace(/_sum\.jpg|_b\.jpg/, ''));
    return urls;
  }
});
```

### 5. 下载所有图片
```bash
curl -sS -o "{序号}.jpg" "{图片 URL}"
```

### 6. 采集商品信息
- 标题、价格、店铺
- SKU、库存、属性
- 销售数据、评价

### 7. 保存 JSON 数据包
包含：
- 商品基本信息
- 完整图片 URLs
- 本地图片路径
- SKU 详情
- 采集时间

## 输出文件
1. `{桌面}/1688-商品详情-{商品 ID}-图片/` - 所有商品图片
2. `{桌面}/1688-商品详情-{商品 ID}.json` - 完整数据包

## 关键技术点

### ✅ 懒加载处理
- 持续滚动触发图片加载
- 每步滚动后等待 300-500ms

### ✅ Performance API
- 捕获所有网络请求的图片
- 包括 iframe 内的图片
- 比 DOM 查询更完整

### ✅ URL 清理
```javascript
url.replace(/_sum\.jpg$/, '.jpg')  // 去除缩略图后缀
   .replace(/_b\.jpg$/, '.jpg')    // 去除中等图后缀
   .replace(/_\d+x\d+\.jpg$/, '.jpg')  // 去除尺寸后缀
```

## 常见问题

### Q: 图片数量不够？
A: 增加滚动步数（scrollSteps）或延长等待时间（scrollDelay）

### Q: 图片都是 2KB 缩略图？
A: 检查 URL 清理逻辑，确保去掉了 `_sum.jpg` 后缀

### Q: 某些图片下载失败？
A: 可能是跨域或防盗链，尝试添加 User-Agent 头

## 示例输出
```json
{
  "商品 ID": "968110925640",
  "商品标题": "厂家黑金釉锔钉主人杯...",
  "本地图片路径": "/Users/xxx/Desktop/1688-商品详情 -968110925640-图片/",
  "图片总数": 24,
  "商品图片 URLs": [...]
}
```
