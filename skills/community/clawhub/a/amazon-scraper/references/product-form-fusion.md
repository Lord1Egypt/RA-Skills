# Amazon 产品形态融合创意（视觉化选品思路）

## 场景
用户提出类似"亚马逊 X 品类首页 Top 5 产品外观形态融合，能产生什么新产品"的需求 —— 这是一种**视觉化选品** + **形态组合创意**工作流。

## 典型流程

### 1. 抓数据
用 `amazon_handler.js` 抓亚马逊类目 / 搜索结果：

```bash
# 两种入口
# (a) 类目页（标题全有）
docker run --rm amazon-scraper node assets/amazon_handler.js \
  "https://www.amazon.com/gp/bestsellers/electronics/5180508011"

# (b) 关键词搜索（经常 title=null，备 image URL）
docker run --rm amazon-scraper node assets/amazon_handler.js \
  "https://www.amazon.com/s?k=cable+management+organizer"
```

### 2. 取 Top N + 提取 image URL
```python
import json
data = json.load(open('/tmp/cm.json'))
for p in (data.get('products') or [])[:5]:
    print(f"ASIN: {p['asin']}")
    print(f"Img:  {p['image']}")
    print(f"Price: ${p['price']}  Rating: {p['rating']}★  Reviews: {p.get('reviews')}")
```

### 3. 关键 fallback：搜索页 title 缺失时
如果 `p.get('title')` 是 `None`（**搜索页极常见**），**用 `p['image']` URL + `vision_analyze` 看图识物**：

```python
vision_analyze(
    image_url=p['image'],
    question="这是一个亚马逊 [类目] 类的产品图片。请详细描述产品外观、形态、材质、颜色、尺寸感。"
)
```

这是**唯一可靠**识别搜索结果产品形态的方法。

### 4. 形态融合创意结构

每张图分析完，整理出 Top N 产品的"形态词条"：
- 形态 1（扎带 / 卷状 / 尼龙）
- 形态 2（卡扣 / 圆形 / 黑色塑料）
- 形态 3（理线槽 / 长条 / 梳齿）
- 形态 4（金属托盘 / 网格 / 桌下）
- 形态 5（PVC 软槽 / 自粘 / 桌边）

然后做"5 → 1 融合"创意，**输出 3-5 个候选产品外观方案**，每个包含：
- 命名（一句话）
- 形态融合说明（哪 5 个怎么组合）
- 外观描述（材质、颜色、尺寸感、造型比喻）
- 功能描述（解决什么用户痛点）
- 推荐指数 + 理由（客单价 / A+ 好做度 / 安装便捷 / 视觉冲击）

### 5. 推荐筛选标准
- **客单价提升空间**：单一功能 $7-15 → 多合一 $25-40
- **视觉冲击**：黑色磨砂金属 / 极简铝型材 > 普通黑塑料
- **安装便捷**：磁吸 / 3M 胶 / 0 工具 = 转化率高
- **配件生态**：模块化 = 复购
- **目标人群**：苹果/华为桌面办公 / 电竞 RGB / 家庭办公升级

## Pitfalls
- ❌ 搜索页 `title=null` 时以为抓失败 → 实际上数据齐了，**用 image URL + vision 即可**
- ❌ 强行用 `/s?k=...` 拿 BSR Top → 搜索页没排名概念，混淆数据
- ❌ 创意堆砌"什么都加上" → 一个产品主形态要明确，最多 2-3 个融合点
- ❌ 给传统线下/工业产品做这种融合 → 亚马逊 C 端才吃这套
- ✅ Top 5 足够（再多了信息冗余，融合时反而抓不到重点）
- ✅ 形态描述尽量用视觉化语言（"鹅卵石"、"桌面港湾"、"科技树"）便于后面做产品图
- ✅ 推荐 Top 1 时给出"客单价 / 视觉 / 安装 / 配件"4 维理由，不只是"我觉得好"

## 相关 reference
- 主 SKILL.md "搜索页 title 缺失" fallback 章节
- 选品决策树（SKILL.md "Agent 调用决策树"）
