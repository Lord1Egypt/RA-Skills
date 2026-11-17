# theCrag.com URL 结构参考

## 基础网址

- 主站：`https://www.thecrag.com/`
- 中文界面：`https://www.thecrag.com/zh_hans/`
- 英文界面：`https://www.thecrag.com/en/`

## 攀岩区域 URL 模式

层级 URL 结构遵循：大洲 → 国家 → 区域 → 地区 → 岩场

```
/climbing/{国家}                       - 国家级
/climbing/{国家}/{区域}                 - 区域/省级
/climbing/{国家}/{区域}/{地区}          - 地区级
/climbing/{国家}/{区域}/{地区}/{岩场}   - 具体岩场
```

## 搜索 URL

```
/zh_hans/search?q={关键词}              - 中文搜索
/en/search?q={关键词}                   - 英文搜索
```

## 常用国家/区域 Slug

### 亚洲
| 国家/地区 | Slug | URL |
|-----------|------|-----|
| 中国 | china | `/climbing/china` |
| 日本 | japan | `/climbing/japan` |
| 泰国 | thailand | `/climbing/thailand` |
| 越南 | vietnam | `/climbing/vietnam` |
| 印度尼西亚 | indonesia | `/climbing/indonesia` |
| 马来西亚 | malaysia | `/climbing/malaysia` |
| 老挝 | laos | `/climbing/laos` |
| 台湾 | taiwan | `/climbing/taiwan` |
| 韩国 | south-korea | `/climbing/south-korea` |
| 尼泊尔 | nepal | `/climbing/nepal` |
| 印度 | india | `/climbing/india` |

### 中国热门岩场区域
| 区域 | Slug | URL |
|------|------|-----|
| 阳朔 | yangshuo | `/climbing/china/yangshuo` |
| 格凸 | getu | `/climbing/china/getu` |
| 黎明 | liming | `/climbing/china/liming` |
| 云南 | yunnan | `/climbing/china/yunnan` |
| 广西 | guangxi | `/climbing/china/guangxi` |
| 贵州 | guizhou | `/climbing/china/guizhou` |
| 北京（白河） | beijing | `/climbing/china/beijing` |
| 杭州 | hangzhou | `/climbing/china/hangzhou` |
| 南高峰 | south-peak | `/climbing/china/hangzhou/south-peak` |
| 怀集 | huaiji | `/climbing/china/guangdong/area/10342227987` |
| 燕玺（怀集） | - | `/climbing/china/guangdong/area/13416816312` |
| 朝岩（怀集） | - | `/climbing/china/guangdong/area/13597121415` |
| 昆明 | kunming | `/climbing/china/yunnan/kunming` |
| 丽江 | lijiang | `/climbing/china/yunnan/lijiang` |

### 其他热门国际目的地
| 目的地 | Slug | URL |
|--------|------|-----|
| 卡林诺斯（希腊） | kalymnos | `/climbing/greece/kalymnos` |
| 休拉纳（西班牙） | siurana | `/climbing/spain/siurana` |
| 瑟于斯（法国） | ceuse | `/climbing/france/ceuse` |
| 通赛（泰国） | tonsai | `/climbing/thailand/tonsai` |
| 红河峡谷（美国） | red-river-gorge | `/climbing/usa/red-river-gorge` |
| 优胜美地（美国） | yosemite | `/climbing/usa/yosemite` |
| 格兰屏（澳大利亚） | grampians | `/climbing/australia/grampians` |
| 岩地（南非） | rocklands | `/climbing/south-africa/rocklands` |

## Slug 构造规则

1. 全部小写
2. 空格替换为连字符
3. 移除特殊字符（如重音符号）
4. 保留常用缩写（如 "usa"、"uk"）
5. 多词名称用连字符连接（如 "new-zealand"、"south-korea"）

## 页面可获取信息

成功加载页面后，通常可获得以下数据：

- **区域名称**及层级面包屑导航
- **路线总数**及按类型分类（运动攀/传统攀/抱石等）
- **难度分布**图表
- **热门路线**列表（含难度等级和星级评分）
- **子区域**（下级岩场）及各自路线数量
- **GPS 坐标**和地图视图
- **接近与进入**说明（用户贡献）
- **季节信息**及最佳攀爬时间
- **照片**和岩壁线路图（社区上传）

## API 信息

theCrag 提供 REST API 供程序化访问：
- 基础地址：`https://api.thecrag.com/`
- 需要 API 密钥认证
- 用于在第三方网站嵌入攀岩数据
- 完整文档：`https://www.thecrag.com/en/article/api`
