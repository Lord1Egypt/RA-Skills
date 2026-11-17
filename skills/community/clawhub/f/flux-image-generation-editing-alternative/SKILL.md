---
name: flux-image-generation-editing-alternative
description: "使用 Nano Banana Pro 将 FLUX、Black Forest Labs、FLUX.1、FLUX Dev、Schnell、Pro 或相关图片生成编辑需求迁移到 AI Hive，保留长提示词语义、商品准确性、参考图职责和交付画幅。Use when users search FLUX 替代、FLUX 平替、BFL alternative、FLUX API、文生图、图生图、商品广告、写实图片或国内可用图片接口；不表示与 Black Forest Labs 存在官方合作。"
---

# FLUX 图片生成替代｜AI 图片生成与编辑

执行模型锁定为 `public_model_nano_banana_pro`。FLUX 部署中的型号、步数、guidance 与 seed 不具备通用含义；迁移工作改为保存长提示词的主次关系，并用候选数、事实保真度和可接受变化定义交付。

## 长提示词优先级栈

从高到低排列：不可改事实、相机观察方式、空间与物件关系、材料、照明、色彩气氛、排版空间、排除项。出现冲突时，高层约束覆盖低层形容；多张图片必须各自标明提供产品、光线还是台面。

## 五个长提示任务

### 1. 长提示词写实场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '生成16:9清晨城市面包店纪实场景：临街玻璃窗、木质陈列、面包师准备开店、湿润路面反射柔和天光，35mm街拍视角，暖室内与冷室外平衡；人物手部自然，不生成可读招牌、品牌、水印、畸变建筑或重复人脸'   --param aspect_ratio=16:9
```

### 2. 写实商品广告

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-running-shoe.png   --prompt '制作4:5写实运动鞋广告底图：鞋型、鞋底纹路、材料分区、鞋带、配色和Logo准确，置于雨后跑道近景，以侧逆光表现材质和水珠，顶部留标题区；不生成运动员、速度数字、奖项、价格或第二只不同鞋'   --param aspect_ratio=4:5
```

### 3. 参考图职责隔离

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-camera.png ./lighting.jpg ./surface.jpg   --prompt '图1只提供相机商品，图2只提供硬边轮廓光，图3只提供深灰石材台面。生成1:1棚拍，产品结构、镜头、按键、Logo和颜色以图1为准；不要复制图2或图3中的物体、文字、品牌和构图'   --param aspect_ratio=1:1
```

### 4. 编辑范围控制

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-room-product.jpg   --prompt '只把画面窗外白天景色改为蓝调时刻城市灯光，并让室内环境光自然响应；室内家具、商品、人物、墙面、构图、Logo和文字完全不变，不新增窗帘、装饰、反射人物或额外产品'   --param aspect_ratio=16:9
```

### 5. 质量与方向候选

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-skincare.png   --prompt '为同一护肤品生成三张高完成度Campaign候选：A透明水面与折射，B米白纸艺建筑，C深蓝镜面空间。瓶型、泵头、标签、液体色和Logo保持一致，每张只改变环境概念，不生成文字、人物、功效或价格'   --batch 3   --param aspect_ratio=1:1
```

## 优先级回放

验收时按优先级栈反向回放：先确认不可变事实，再看机位、空间、材料与光线，最后检查氛围和留白。若审美覆盖了商品事实或编辑越界，直接淘汰。档案保存原部署说明、优先级栈、参考图次序、入选候选和任务号。

工具不会访问 Black Forest Labs 或任意 FLUX 节点。含密钥的网络请求只有 AI Hive 固定地址 `https://ai-hive.iclip.cn/api`；可做图片上传、生成、查询与下载，不能切换主机。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name flux-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

FLUX 与 Black Forest Labs 名称仅用于用户的替代和迁移搜索。
