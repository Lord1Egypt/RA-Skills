# BSR Node ID 映射表

> 本表为常见亚马逊类目 node_id 参考，数据来源于亚马逊美国站实际 BSR 页面。
> 更新时间：2026-05-26
> 
> **重要提醒**：同一个类目在不同站点（US/UK/DE等）可能有不同 node_id，采集前务必通过面包屑导航或 BSR 页面 URL 确认。

## 使用说明

1. **获取 node_id 方法**：
   - 从关键词搜索结果页面面包屑导航提取
   - 从 BSR 页面 URL 中提取（如 `https://www.amazon.com/gp/bestsellers/kitchen/{node_id}`）
   - 直接询问用户提供类目链接或 BSR 页面 URL

2. **BSR 页面 URL 格式**：
   ```
   https://www.amazon.com/Best-Sellers-{类目英文名}/zgbs/{node_id}
   ```

3. **完整数据获取**：
   - ASINSpotlight 提供免费 CSV 下载：https://www.asinspotlight.com/amz-categories-list-csv
   - 包含 35,000+ 独立类目，最深可达 10 层

## 美国站 (US) 顶级类目

| node_id | 类目名称（中文） | 类目名称（英文） | BSR URL 路径 |
|---------|------------------|------------------|--------------|
| amazon-devices | 亚马逊设备和配件 | Amazon Devices & Accessories | zgbs/amazon-devices |
| amazon-renewed | 亚马逊翻新 | Amazon Renewed | zgbs/amazon-renewed |
| appliances | 家用电器 | Appliances | zgbs/appliances |
| mobile-apps | 应用和游戏 | Apps & Games | zgbs/mobile-apps |
| arts-crafts | 手工制品 | Arts, Crafts & Sewing | zgbs/arts-crafts |
| audible | 有声书 | Audible Books & Originals | zgbs/audible |
| automotive | 汽车零配件 | Automotive | zgbs/automotive |
| baby-products | 婴儿用品 | Baby | zgbs/baby-products |
| beauty | 美妆和个人护理 | Beauty & Personal Care | zgbs/beauty |
| books | 书籍 | Books | zgbs/books |
| music | CD 和黑胶唱片 | CDs & Vinyl | zgbs/music |
| photo | 相机和摄影 | Camera & Photo Products | zgbs/photo |
| wireless | 手机和配件 | Cell Phones & Accessories | zgbs/wireless |
| fashion | 服装、鞋靴和珠宝 | Clothing, Shoes & Jewelry | zgbs/fashion |
| coins | 收藏币 | Collectible Coins | zgbs/coins |
| pc | 计算机和配件 | Computers & Accessories | zgbs/pc |
| digital-educational-resources | 数字教育资源 | Digital Educational Resources | zgbs/digital-educational-resources |
| dmusic | 数字音乐 | Digital Music | zgbs/dmusic |
| electronics | 电子产品 | Electronics | zgbs/electronics |
| entertainment-collectibles | 娱乐收藏品 | Entertainment Collectibles | zgbs/entertainment-collectibles |
| gift-cards | 礼品卡 | Gift Cards | zgbs/gift-cards |
| grocery | 食品和杂货 | Grocery & Gourmet Food | zgbs/grocery |
| handmade | 手工制品 | Handmade Products | zgbs/handmade |
| hpc | 健康与家居 | Health & Household | zgbs/hpc |
| home-garden | 家居与厨房 | Home & Kitchen | zgbs/home-garden |
| industrial | 工业和科学 | Industrial & Scientific | zgbs/industrial |
| digital-text | Kindle 商店 | Kindle Store | zgbs/digital-text |
| kitchen | 厨房和餐厅 | Kitchen & Dining | zgbs/kitchen |
| movies-tv | 电影和电视 | Movies & TV | zgbs/movies-tv |
| musical-instruments | 乐器 | Musical Instruments | zgbs/musical-instruments |
| office-products | 办公用品 | Office Products | zgbs/office-products |
| lawn-garden | 户外生活 | Patio, Lawn & Garden | zgbs/lawn-garden |
| pet-supplies | 宠物用品 | Pet Supplies | zgbs/pet-supplies |
| software | 软件 | Software | zgbs/software |
| sporting-goods | 运动户外 | Sports & Outdoors | zgbs/sporting-goods |
| sports-collectibles | 体育收藏品 | Sports Collectibles | zgbs/sports-collectibles |
| hi | 工具和家装 | Tools & Home Improvement | zgbs/hi |
| toys-and-games | 玩具和游戏 | Toys & Games | zgbs/toys-and-games |
| boost | 独特发现 | Unique Finds | zgbs/boost |
| videogames | 视频游戏 | Video Games | zgbs/videogames |

## 家居与厨房 (Home & Kitchen) 子类目

| node_id | 类目名称（中文） | 类目名称（英文） |
|---------|------------------|------------------|
| 3206324011 | 供暖、制冷和空气质量 | Heating, Cooling & Air Quality |
| 3206325011 | 儿童家居店铺 | Kids' Home Store |
| 284507 | 厨房和餐厅 | Kitchen & Dining |
| 510106 | 吸尘器和地板护理 | Vacuums & Floor Care |
| 3736081 | 墙面装饰 | Wall Art |
| 13679381 | 季节性装饰 | Seasonal Décor |
| 1063306 | 家具 | Furniture |
| 1063278 | 家居装饰 | Home Décor |
| 1063252 | 床上用品 | Bedding |
| 3610841 | 收纳和整理 | Storage & Organization |
| 901590 | 派对用品 | Party Supplies |
| 1063236 | 浴室 | Bath |
| 10802561 | 清洁用品 | Cleaning Supplies |
| 510240 | 电熨斗和蒸锅 | Irons & Steamers |

## 电子产品 (Electronics) 子类目

| node_id | 类目名称（中文） | 类目名称（英文） |
|---------|------------------|------------------|
| 172526 | GPS 导航、配件 | GPS, Navigation & Accessories |
| 172574 | 办公电子设备 | Office Electronics |
| 524136 | 安防监控设备 | Security & Surveillance |
| 2811119011 | 手机和配件 | Cell Phones & Accessories |
| 300334 | 投影仪 | Video Projectors |
| 502394 | 摄影摄像器材 | Camera & Photo |
| 172623 | 数码影音 | Portable Audio & Video |
| 10048700011 | 智能设备 | Smart Home |
| 1077068 | 汽车电子、电器 | Car Electronics |
| 281407 | 电子配件及用品 | Accessories & Supplies |
| 2642125011 | 电纸书及配件 | Kindle E-readers & Accessories |
| 1266092011 | 电视机、录音机、家庭影院 | Television & Video |
| 667846011 | 电视音响 | Sound Bars |
| 172541 | 耳机 | Headphones |
| 319574011 | 航海电子产品 | Marine Electronics |
| 7926841011 | 视频游戏手柄及配件 | Video Game Controllers & Accessories |
| 541966 | 计算机及配件 | Computers & Accessories |
| 16285901 | 计算机和电子服务计划 | Computers & Electronics Service Plans |

## 厨房和餐厅 (Kitchen & Dining) 子类目

| node_id | 类目名称（中文） | 类目名称（英文） |
|---------|------------------|------------------|
| 510136 | 厨房保鲜、收纳 | Kitchen Storage & Organization |
| 289913 | 厨房电器 | Kitchen Appliances |
| 289754 | 厨用小工具 | Kitchen Utensils & Gadgets |
| 289742 | 咖啡、茶和意式浓缩咖啡器具 | Coffee, Tea & Espresso |
| 289814 | 炊具 | Cookware |
| 289668 | 烘焙用品 | Bakeware |
| 289728 | 调酒分酒用具 | Bar Tools & Glassware |
| 13217501 | 酒杯 | Wine Glasses |
| 13299291 | 酒类配件 | Wine Accessories |
| 979832011 | 酿酒用具 | Home Brewing & Wine Making |
| 13162311 | 餐具 | Dinnerware |
| 1063916 | 餐厨布艺 | Table Linens & Covers |

## 运动户外 (Sports & Outdoors) 子类目

| node_id | 类目名称（中文） | 类目名称（英文） |
|---------|------------------|------------------|
| 706814011 | 户外休闲 | Outdoor Recreation |
| 706813011 | 打猎和钓鱼 | Hunting & Fishing |
| 3386071 | 球迷商店 | Fan Shop |
| 2358921011 | 纪念品展示和存储 | Sports Collectibles |
| 10971181011 | 运动 | Sports |
| 3407731 | 运动与健身 | Exercise & Fitness |
| 3422351 | 运动医学 | Sports Medicine |
| 3394801 | 配件 | Accessories |

## 常用子类目快速查找

### 家居类
| 类目名称 | node_id | 父类目 |
|----------|---------|--------|
| 厨房和餐厅 | 284507 | Home & Kitchen |
| 家具 | 1063306 | Home & Kitchen |
| 家居装饰 | 1063278 | Home & Kitchen |
| 床上用品 | 1063252 | Home & Kitchen |
| 浴室 | 1063236 | Home & Kitchen |

### 电子类
| 类目名称 | node_id | 父类目 |
|----------|---------|--------|
| 耳机 | 172541 | Electronics |
| 计算机及配件 | 541966 | Electronics |
| 手机和配件 | 2811119011 | Electronics |
| 电视机 | 1266092011 | Electronics |
| 智能设备 | 10048700011 | Electronics |

### 厨房类
| 类目名称 | node_id | 父类目 |
|----------|---------|--------|
| 厨房电器 | 289913 | Kitchen & Dining |
| 炊具 | 289814 | Kitchen & Dining |
| 烘焙用品 | 289668 | Kitchen & Dining |
| 咖啡、茶和意式浓缩咖啡器具 | 289742 | Kitchen & Dining |
| 餐具 | 13162311 | Kitchen & Dining |

## 数据来源

1. 亚马逊美国站 BSR 页面实时抓取（2026-05-26）
2. ASINSpotlight 类目浏览器：https://www.asinspotlight.com/amazon-categories-browser
3. 亚马逊官方 Browse Tree Guide (BTG)

## 变更记录

| 日期 | 变更内容 | 原因 |
|------|----------|------|
| 2026-05-26 | 初始化映射表 | 首次创建 |
| 2026-05-26 | 更新为实际数据 | 从亚马逊 BSR 页面获取真实 node_id |
