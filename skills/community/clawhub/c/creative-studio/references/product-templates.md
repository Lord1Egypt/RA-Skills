# 产品模板 - Product Templates

## 产品配置 YAML Schema

所有产品详情页通过 YAML 配置文件生成。必填字段标记 `*`。

```yaml
product:
  name: "永磁变频螺杆空压机 YDV-75"           # * 中文名称
  name_en: "PM VSD Screw Air Compressor YDV-75"  # 英文名称
  category: "变频空压机"                        # * 产品分类
  brand: "萤火虫"                               # 品牌（默认萤火虫）
  description: >-                               # * 中文描述（1-2句）
    采用高效永磁电机与智能变频控制技术，
    实现按需供气，综合节能率达30%以上。
  description_en: >-                            # 英文描述
    Features high-efficiency PM motor with smart
    VFD control, achieving 30%+ energy savings.
  specs:                                        # * 技术参数表
    - label: "功率 / Power"
      value: "75 kW"
    - label: "排气量 / FAD"
      value: "14.0 m³/min"
    - label: "排气压力 / Pressure"
      value: "0.8 MPa"
    - label: "变频范围 / VFD Range"
      value: "20-100%"
    - label: "噪音 / Noise"
      value: "72±3 dB(A)"
    - label: "重量 / Weight"
      value: "1850 kg"
  features:                                     # 产品特点（3-6个）
    - icon: "zap"
      title: "高效节能"
      title_en: "High Efficiency"
      desc: "IE5永磁电机，比异步电机节能10-15%"
      desc_en: "IE5 PM motor, 10-15% more efficient"
    - icon: "cpu"
      title: "智能控制"
      title_en: "Smart Control"
      desc: "7寸触摸屏，实时监控运行数据"
      desc_en: "7\" touchscreen with real-time monitoring"
    - icon: "volume"
      title: "超静音设计"
      title_en: "Ultra Quiet"
      desc: "全封闭隔音罩，噪音低至72dB"
      desc_en: "Fully enclosed soundproof, as low as 72dB"
  images:
    main: "products/YDV-75_main.png"             # 主图路径
    thumbnails:                                  # 缩略图列表
      - "products/YDV-75_1.png"
      - "products/YDV-75_2.png"
      - "products/YDV-75_3.png"
  metrics:                                       # 顶部指标卡（可选）
    - value: "30%+"
      label: "综合节能率"
      label_en: "Energy Savings"
    - value: "IE5"
      label: "能效等级"
      label_en: "Efficiency Grade"
  cta:
    phone: "13825202084"
    contact_person: "邹先生"
    website: "www.fireflies.net.cn"
```

## 各产品类型的规格字段

### 永磁变频螺杆空压机
```
功率 (kW), 排气量 (m³/min), 排气压力 (MPa), 变频范围 (%),
噪音 dB(A), 冷却方式, 启动方式, 外形尺寸 L×W×H (mm), 重量 (kg)
```

### 冷冻式干燥机（冷干机）
```
处理气量 (Nm³/min), 工作压力 (MPa), 入口温度 (℃), 压力露点 (℃),
冷却方式, 制冷剂, 电源, 外形尺寸 (mm), 重量 (kg)
```

### 余热回收机
```
适用空压机功率 (kW), 热水产量 (L/h), 热水温度 (℃),
进水温度 (℃), 换热效率 (%), 外形尺寸 (mm), 重量 (kg)
```

### 制氮机
```
氮气产量 (Nm³/h), 氮气纯度 (%), 工作压力 (MPa),
进气压力 (MPa), 露点 (℃), 电源, 外形尺寸 (mm), 重量 (kg)
```

### 精密过滤器
```
处理气量 (Nm³/min), 过滤精度 (μm), 工作压力 (MPa),
接口尺寸, 外形尺寸 (mm), 重量 (kg)
```

## 详情页生成命令

```bash
# 中文详情页
python scripts/generate_detail_page.py --product-config product.yaml --lang zh -o detail_zh.html

# 英文详情页
python scripts/generate_detail_page.py --product-config product.yaml --lang en -o detail_en.html

# 双语详情页
python scripts/generate_detail_page.py --product-config product.yaml --lang both -o detail.html
```

## 图标映射表

| icon key | 含义 | Emoji 备选 |
|----------|------|-----------|
| zap | 节能/电力 | ⚡ |
| cpu | 智能/控制 | 🖥️ |
| volume | 静音 | 🔇 |
| shield | 安全/可靠 | 🛡️ |
| thermometer | 冷却/温度 | 🌡️ |
| wrench | 维护/耐用 | 🔧 |
| leaf | 环保 | 🌿 |
| gauge | 仪表/监控 | 📊 |
| droplet | 过滤/净化 | 💧 |
| wind | 气动/气流 | 💨 |
