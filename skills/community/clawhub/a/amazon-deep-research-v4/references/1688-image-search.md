# 1688 以图搜图策略 (V4)

## 核心原则

**必须用Amazon主图做图片搜索**，不接受关键词搜索。
关键词搜索会返回不同产品（外观/规格不匹配），以图搜图才能找到真正同款。

## 搜索URL模板

```
https://air.1688.com/app/1688-lp/landing-page/comparison-table.html?bizType=browser&currency=CNY&customerId=dingtalk&outImageAddress={URL_ENCODED_IMAGE}
```

## 操作流程

1. 从Amazon产品页获取主图URL：
```javascript
document.querySelector('#landingImage')?.src
|| document.querySelector('#imgTagWrapperId img')?.src
|| document.querySelector('.a-dynamic-image')?.src
```

2. URL编码主图地址：
```python
import urllib.parse
encoded = urllib.parse.quote(image_url, safe='')
search_url = f"https://air.1688.com/app/1688-lp/landing-page/comparison-table.html?bizType=browser&currency=CNY&customerId=dingtalk&outImageAddress={encoded}"
```

3. browser agent 导航到搜索URL，等待5秒

4. 提取结果：
```javascript
const rows = document.querySelectorAll('tr.ant-table-row');
const results = [];
rows.forEach((row, i) => {
  if (i >= 3) return; // TOP 3
  const tds = row.querySelectorAll('td');
  const img = row.querySelector('img')?.src || '';
  const name = tds[1]?.innerText || '';
  const price = tds[2]?.innerText || '';
  const sales = tds[3]?.innerText || '';
  const link = row.querySelector('a')?.href || '';
  results.push({img, name, price, sales, link});
});
JSON.stringify(results);
```

## 匹配度标注

- **✓** 高度匹配：外观/规格/功能基本一致
- **~** 近似匹配：同类产品但规格/颜色/配件可能不同
- **✗** 不匹配：需要人工确认或换搜索策略

## 约束

1. 链接格式必须是 `detail.1688.com/offer/` — 不接受 `alibaba.com`
2. 优先选择有"实力商家"或"源头工厂"标签的供应商
3. 价格取中间值（如 "50-120" → 85）
4. 运费金额不纳入采购成本

## 并发

3个browser agent并行，每个处理3-5个ASIN

## Fallback

如果以图搜图无结果（图片被防盗链/搜索无匹配）：
1. 用中文关键词搜索: `{中文产品名} site:detail.1688.com`
2. 人工确认匹配度后标注为 **~**
