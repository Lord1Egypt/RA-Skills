# toy_set 类目映射配置

## 类目信息

- **商品类型**: toy_set
- **一级/二级类目 ID**: 17028973
- **商品类型 ID**: 970895715
- **生成时间**: 2026-03-27 09:54:24
- **总属性数**: 41
- **已配置**: 32
- **待配置**: 9

---

## 必填属性（6个）

| 属性名 | 属性 ID | 数据来源 | 默认值 | 说明 |
|--------|--------|---------|--------|------|
| 商品标题 | N/A | 1688-tt.copy_writing | - | 从文案提取俄文标题 |
| 售价 | N/A | ozon-pricer.price_rub | - | 卢布售价 |
| 主图 | N/A | ozon-image-translator.images | - | 5 张主图 |
| 类型 | 8229 | fixed | Набор игрушек | 固定值，根据类目设置 |
| 品牌 | 85 | fixed | Нет бренда | 无品牌商品 |
| 型号名称（针对合并为一张商品卡片） | 9048 | auto_generate | - | 自动生成 |

## 可选属性（已配置 26个）

| 属性名 | 属性 ID | 数据来源 | 默认值 | 说明 |
|--------|--------|---------|--------|------|
| 商品描述 | N/A | 1688-tt.copy_writing | - | 从文案提取俄文描述 |
| 划线价 | N/A | ozon-pricer.old_price_rub | - | 卢布划线价 |
| 富文本详情 | N/A | ozon-image-translator.images | - | 详情图生成富文本 JSON |
| 标签/话题 | N/A | 1688-tt.copy_writing |  | 从文案提取标签 |
| 含包装重量 | N/A | 1688-tt.product_info.weight | 200 | 单位：g |
| 包装长度 | N/A | 1688-tt.product_info.package_length | 10 | 单位：cm |
| 包装宽度 | N/A | 1688-tt.product_info.package_width | 10 | 单位：cm |
| 包装高度 | N/A | 1688-tt.product_info.package_height | 5 | 单位：cm |
| 散装最低数量 | 23518 | fixed | 1 | 固定值 1 |
| 一个商品中的件数 | 8962 | fixed | 1 | 固定值 1 |
| 原厂包装数量 | 11650 | fixed | 1 | 固定值 1 |
| 材料 | 4975 | 1688-tt.product_info.material | Пластик | 从 1688 获取，智能转换 |
| 保质期（天） | 7578 | fixed | - | 无保质期 |
| 商品颜色 | 10096 | 1688-tt.product_info.color | Синий | 从 1688 获取，智能转换 |
| 简介 | 4191 | 1688-tt.copy_writing | - | 从文案提取简短描述 |
| 原产国 | 4389 | fixed | Китай | 固定值：中国 |
| 儿童性别 | 13216 | fixed | Унисекс | 固定值：中性 |
| #主题标签 | 23171 | 1688-tt.copy_writing | - | 从文案提取 |
| 原厂包装数量 | 11650 | fixed | 1 | 固定值 1 |
| 颜色名称 | 10097 | 1688-tt.product_info.color | - | 颜色名称（可选） |
| 含包装重量，克 | 4497 | 1688-tt.product_info.weight | 200 | 从 1688 获取（克） |
| 卖家代码 | 9024 | auto_generate | - | 自动生成 SKU |
| 统一计量单位中的商品数量 | 23249 | fixed | 1 | 固定值 1 |
| 散装最低数量 | 23518 | fixed | 1 | 固定值 1 |
| 名称 | 4180 | 1688-tt.copy_writing | - | 商品名称 |
| 保修期 | 4385 | fixed | - | 无保修 |

## 待配置属性（9个）

> ⚠️ 这些属性没有数据来源，需要手动配置 `source` 字段

| 属性名 | 属性 ID | 是否必填 | 说明 |
|--------|--------|---------|------|
| 臭氧。视频：视频产品 | 22273 | ❌ 否 | ⚠️ 需手动配置 - 视频产品信息 |
| 臭氧。视频：链接 | 21841 | ❌ 否 | ⚠️ 需手动配置 - 视频 URL |
| 臭氧。视频：标题 | 21837 | ❌ 否 | ⚠️ 需手动配置 - 视频标题 |
| JSON富内容 | 11254 | ❌ 否 | ⚠️ 需手动配置 - 使用JSON格式的模板添加带有照片和视频的扩展产品描述。 有关填写此特征的详细信息，请参阅知识库中的 |
| 臭氧。视频背景：链接 | 21845 | ❌ 否 | ⚠️ 需手动配置 - 背景视频 URL |
| 组合成类似的产品 | 22390 | ❌ 否 | ⚠️ 需手动配置 - 用于商品关联 |
| 欧亚经济联盟的HS编码 | 22232 | ❌ 否 | ⚠️ 需手动配置 - 从列表中选择一个值。 如果您不知道指定哪个代码，则需要联系海关服务或海关代表。 |
| PDF 文件 | 8790 | ❌ 否 | ⚠️ 需手动配置 - 上传 PDF 文件 |
| PDF文件名称 | 8789 | ❌ 否 | ⚠️ 需手动配置 - 无描述 |

---

## 配置指南

### 数据来源（source）格式

```
- 1688-tt.product_info.color       # 从 1688 商品数据获取
- 1688-tt.copy_writing             # 从文案获取
- ozon-pricer.price_rub            # 从价格计算模块获取
- ozon-image-translator.images     # 从图片翻译模块获取
- fixed                            # 固定值（使用 fallback）
- auto_generate                    # 自动生成（使用 transform）
- (空)                             # 无数据来源，跳过
```

### 转换规则（transform）

```
- extract_title                    # 提取俄文标题
- extract_description              # 提取俄文描述
- extract_hashtags                 # 提取俄文标签
- color_smart                      # 智能颜色转换
- material_smart                   # 智能材质转换
- age_smart                        # 智能年龄转换
- oc#YYYY_MM_DD-hh_mm_ss          # 自动生成型号
- sku_auto                         # 自动生成 SKU
```

## 使用示例

```bash
# 测试映射
node scripts/map.js toy_set

# 执行完整上传流程
https://detail.1688.com/offer/XXX.html op -w 200g -p 10
```
