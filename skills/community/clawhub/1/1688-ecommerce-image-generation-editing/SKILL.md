---
name: 1688-ecommerce-image-generation-editing
description: "为1688工厂与批发商生成和编辑产品主图、规格图、工厂能力图、定制说明、包装运输和批量SKU图片。Use this skill for 1688电商图片、阿里巴巴批发、源头工厂、OEM/ODM、起订量、规格参数、生产流程、工厂实拍、包装清单、批发商品图和B2B询盘素材；支持参考图保真及 AI Hive 批量生成。"
---

# 1688 电商图片生成与编辑

面向采购商而不是终端消费者，图片应帮助判断“产品是否准确、工厂能否生产、规格是否匹配、如何定制与交付”。固定调用 `public_model_nano_banana_pro`。起订量、产能、交期、价格、认证和检测数据必须来自供应商审核资料。

## B2B 资料底稿

收集产品型号、材料、规格范围、颜色表、包装方式、真实工厂照片、设备、工艺步骤、定制选项、样品规则、物流信息和认证原件。模型可以整理视觉，不能制造工厂规模、设备、证书或生产数据。

## 场景与代码

### 1. 批发产品主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '1688批发产品方形主图，准确保留参考产品结构、材料、颜色、型号标识和包装；展示单品与合理批量陈列，背景干净，适合采购商快速识别，不生成起订量、价格、销量、工厂认证或未提供规格' \
  --image /path/to/product.png
```

### 2. 规格与选型底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '1688产品规格选择底图，按参考资料展示不同真实尺寸和接口版本，统一角度与尺度，清楚分区并预留型号、尺寸、材质表格位置；不自行生成数值、单位、兼容范围或型号名称' \
  --image /path/to/variants.jpg
```

### 3. OEM/ODM 定制说明图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'B2B定制能力说明底图，展示产品可定制区域：颜色、包装、标签和配件组合，使用供应商提供的真实样品参考，流程从需求、打样到确认，预留人工填写起订量和交期的位置，不生成Logo授权或生产承诺' \
  --image /path/to/custom-samples.jpg
```

### 4. 工厂与工艺流程图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据真实工厂照片整理1688工艺流程视觉：原料检查、加工、组装、质检、包装五个已确认环节；保持厂房、设备和人员真实，不扩大空间、不增加生产线、机器人、证书或产能数据' \
  --image /path/to/factory-1.jpg \
  --image /path/to/factory-2.jpg
```

### 5. 包装与物流清单

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '1688包装运输说明底图，展示已提供的单品包装、内箱、外箱和装箱顺序，配件数量准确，预留人工填写箱规、毛重和运输方式的位置；不生成数值、托盘数量、物流时效或防护认证' \
  --image /path/to/packaging-reference.jpg
```

## 采购信息验收

- 型号、材料、规格、接口、配件和包装与供应商底稿一致。
- 工厂、设备、人员和工艺来自真实照片，不进行规模造假。
- 起订量、产能、交期、价格、认证与检测数据全部人工填写。
- 定制范围与样品图片可追溯，不展示未授权品牌。
- 文件按产品、规格、用途和版本管理，方便采购复核。
- 上架前按1688后台当前类目与商业规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name 1688-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

`generate` 支持多参考图、批量、实时模型参数、路由、输出目录和仅提交模式。批量前先验证一个真实型号并核对实时费用。
