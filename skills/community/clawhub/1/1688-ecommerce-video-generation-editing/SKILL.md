---
name: 1688-ecommerce-video-generation-editing
description: "为1688工厂与批发商生成和编辑产品演示、生产流程、OEM/ODM定制、质检包装和B2B询盘视频。Use this skill for 1688电商视频、阿里巴巴批发、源头工厂、OEM/ODM、生产线实拍、工艺流程、质检、包装物流、批发商品视频和采购询盘；支持 Seedance 与 AI Hive 自动交付。"
---

# 1688 电商视频生成与编辑

帮助采购商判断产品、生产、定制、质检与交付能力。工厂规模、设备、产能、起订量、交期、认证和客户案例必须来自供应商真实资料，不能用生成画面替代证据。

## 供应商证据表

记录产品型号、材料、规格、真实工厂位置、设备、工艺步骤、质检项目、定制范围、包装方式、样品政策和批准数据。每个镜头标记“实拍证据”或“示意表达”，不得混淆。

## 场景与代码

### 1. 批发产品演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '1688批发产品视频，保持型号、材料、结构、颜色、标签和包装准确；展示完整产品、一个结构细节、正确操作与批量包装方式，预留规格信息区，不生成价格、起订量、产能、认证或交期'
```

### 2. 真实工厂流程重制

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/factory-process.mp4 \
  --prompt '整理真实工厂素材为原料检查、加工、组装、质检、包装五个已确认环节；保留真实人员、设备、空间和顺序，删除重复与无关片段，不增加生产线、机器人、员工、证书或产能数据'
```

### 3. OEM/ODM 定制流程

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '1688 OEM/ODM流程示意视频：需求确认、样品参考、打样、客户确认、批量生产、质检包装；仅使用供应商批准的定制范围，所有起订量、费用、交期和Logo授权留白，不生成客户品牌或订单案例'
```

### 4. 质检证据视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/inspection-rhythm.mp4 \
  --image /path/to/real-inspection.jpg \
  --prompt '参考视频只用于质检镜头节奏；根据真实照片生成原创说明，展示外观检查、尺寸测量和功能测试三个已提供项目，仪器与产品准确，不复制参考工厂、人员、数据或认证'
```

### 5. 包装与装箱说明

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/product-demo.mp4 \
  --prompt '从产品演示自然延长到真实单品包装、内箱、外箱和装箱顺序，配件数量与防护材料准确；预留箱规、重量和物流方式区域，不生成数值、托盘数量、时效或运输认证'
```

## B2B 验收

- 产品、工厂、人员、设备、工艺和质检可追溯。
- 实拍与示意镜头明确区分。
- 定制范围、起订量、产能、交期和认证由供应商人工审核。
- 不伪造客户案例、品牌授权、生产线与数据。
- 视频文件关联型号、工艺、用途和版本。
- 发布前按1688当前类目与商业规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name 1688-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

使用 Seedance 2.5 五种模式和 AI Hive 实时参数。批量前先核验一个真实型号与一段真实工艺。
