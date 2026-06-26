# AlphaShop 图像处理 API 参考文档

Base URL: `https://api.alphashop.cn`

所有接口均为 POST，Content-Type: application/json，Authorization: Bearer JWT token。

---

## 1. 图片翻译

**POST** `/ai.image.translateImage/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 原图URL |
| sourceLanguage | String | Y | 图片内容语种（ISO code） |
| targetLanguage | String | Y | 目标语种（ISO code） |
| includingProductArea | Boolean | N | 是否翻译商品主体上文字（默认false） |
| useImageEditor | Boolean | N | 是否使用图翻编辑器协议（默认false） |
| translatingBrandInTheProduct | Boolean | N | 是否翻译品牌上文字（默认false） |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| srcImage | String | 原图片 |
| sourceLanguage | String | 图片语言 |
| translatedImageUrl | String | 翻译后图片 |
| editInfo | String | 编辑器使用内容 |

---

## 2. 图片翻译PRO

**POST** `/ai.image.translateImagePro/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 原图URL |
| sourceLanguage | String | Y | 支持9种源语言自动识别（中文简体、英文、土耳其语、日语、韩语、法语、意大利语、葡萄牙语、西班牙语），入参"auto"。其他语种需手工传入ISO code |
| targetLanguage | String | Y | 目标语种 |
| includingProductArea | Boolean | N | 是否翻译商品主体上文字（默认false） |
| useImageEditor | Boolean | N | 是否使用图翻编辑器协议（默认false） |
| translatingBrandInTheProduct | Boolean | N | 是否翻译品牌上文字（默认false） |

**响应：** 同图片翻译。

---

## 3. 图片高清放大

**POST** `/ai.image.imageEnlargement/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 公网可访问图片地址，输入尺寸 100×100 ~ 3000×3000，放大后不超过 3000×3000 |
| upscaleFactor | Integer | N | 放大倍数 2-4，默认2 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| imageUrl | String | 放大后图片URL |
| height | String | 放大后高度 |
| width | String | 放大后宽度 |

---

## 4. 图片主题抠图

**POST** `/ai.image.imageObjectExtraction/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 公网可访问图片地址 |
| targetWidth | Integer | N | 缩放目标宽度，如800 |
| targetHeight | Integer | N | 缩放目标高度，如600 |
| transparentFlag | Boolean | Y | 是否透明底，false时需bgColor指定背景色 |
| bgColor | String | N | 背景BGR色彩值，如"255,255,255" |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| score | String | 处理得分 |
| imageUrl | String | 图片URL |
| width | Integer | 宽度 |
| height | Integer | 高度 |

---

## 5. 图片元素识别

**POST** `/ai.image.imageElementDetect/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 图片URL |
| objectDetectElements | List\<Integer\> | N | 检测主体元素（1=水印 2=Logo 3=文字 4=含字色块），可多选 |
| nonObjectDetectElements | List\<Integer\> | N | 检测非主体元素（同上） |
| returnCharacter | Integer | N | 返回OCR文字（1是 0否，默认0） |
| returnBorderPixel | Integer | N | 返回主体边缘距离（1是 0否，默认0） |
| returnProductProp | Integer | N | 返回主体面积占比（1是 0否，默认0） |
| returnProductNum | Integer | N | 返回主体数量（1是 0否，默认0） |
| returnCharacterProp | Integer | N | 返回文字占比（1是 0否，默认0）。需同时 returnCharacter=1 且检测元素包含3 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| recText | String | 图片中的文字 |
| textProp | String | 文字面积占比 |
| objLogo | Boolean | 主体logo |
| objNpx | Boolean | 主体牛皮癣 |
| objWatermark | Boolean | 主体水印 |
| objCharacter | Boolean | 主体文字 |
| pdNum | Integer | 主体数量 |
| pdProp | String | 主体占比 |
| borderPixel | String | 主体距边缘距离 |
| noobjLogo | Boolean | 非主体logo |
| noobjNpx | Boolean | 非主体含字色块 |
| noobjWatermark | Boolean | 非主体水印 |
| noobjCharacter | Boolean | 非主体文字 |

---

## 6. 图片元素智能消除

**POST** `/ai.image.imageElementRemove/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 图片URL（JPG/JPEG/PNG/BMP，256×256~3000×3000，≤10MB） |
| objRemoveWatermark | Integer | N | 主体消除水印 |
| objRemoveCharacter | Integer | N | 主体消除文字 |
| objRemoveLogo | Integer | N | 主体消除logo |
| objRemoveNpx | Integer | N | 主体消除牛皮癣 |
| objRemoveQrcode | Integer | N | 主体消除二维码 |
| noobjRemoveWatermark | Integer | N | 非主体消除水印 |
| noobjRemoveCharacter | Integer | N | 非主体消除文字 |
| noobjRemoveLogo | Integer | N | 非主体消除Logo |
| noobjRemoveNpx | Integer | N | 非主体消除牛皮癣 |
| noobjRemoveQrcode | Integer | N | 非主体消除二维码 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| imageUrl | String | 处理后图片URL |
| width | Integer | 宽度 |
| height | Integer | 高度 |

---

## 7. 图像裁剪

**POST** `/ai.image.imageCut/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 图片URL |
| targetWidth | Integer | N | 目标宽度 |
| targetHeight | Integer | N | 目标高度 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| imageUrl | String | 裁剪后图片URL |
| width | Integer | 宽度 |
| height | Integer | 高度 |

---

## 8. 创建虚拟试衣任务

**POST** `/ai.image.submitVirtualModelTask/1.0` （异步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| modelImageList | List\<String\> | Y | 模特图URL列表，单次最多8张，推荐每次1张 |
| clothesInfoList | List\<ClothesInfo\> | Y | 服饰图片列表，套装传两个元素并标明类型 |
| generateCount | Integer | Y | 生成数量。modelImageList有值时按模特数生成；为空时generateCount生效生成随机模特 |

**ClothesInfo 结构：**

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 服饰图片URL（分辨率 150×150 ~ 6500×6500） |
| type | String | Y | "tops"=上装 "bottoms"=下装 "dresses"=单件连体 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| result | String | 任务ID，用于查询结果 |

---

## 9. 查询虚拟试衣任务结果

**POST** `/ai.image.queryImageGenerateVirtualModelTask/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| taskId | String | Y | 任务ID |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| imageUrl | String | 生成后图片地址 |
| width | String | 图片宽度 |
| height | String | 图片高度 |

---

## 10. 创建模特换肤任务

**POST** `/ai.image.submitImageChangeModelTask/1.0` （异步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| imageUrl | String | Y | 图片URL |
| model | String | Y | 模特类型：YELLOW / BLACK / WHITE / BROWN |
| maskKeepBg | Boolean | N | 是否保留背景（默认true） |
| bgStyle | String | Y | 背景风格：NATURE / URBAN / INDOOR |
| age | String | Y | 年龄段：YOUTH / MIDDLE_AGE / OLD_AGE |
| gender | String | Y | 性别：MALE / FEMALE |
| imageNum | Integer | Y | 生成图片张数 |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| result | String | 任务ID，用于查询结果 |

---

## 11. 查询模特换肤任务结果

**POST** `/ai.image.queryImageChangeModelTask/1.0` （同步）

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| taskId | String | Y | 任务ID |

**响应：**

| 字段 | 类型 | 描述 |
|------|------|------|
| imageUrl | String | 换肤后图片地址 |
| width | String | 图片宽度 |
| height | String | 图片高度 |
