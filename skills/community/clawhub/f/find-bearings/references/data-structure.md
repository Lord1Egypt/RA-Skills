# 轴承数据结构

## 目录结构

```
data/
├── models/              # 轴承型号数据
│   ├── deep_groove.json     # 深沟球轴承
│   ├── cylindrical.json     # 圆柱滚子轴承
│   ├── tapered.json         # 圆锥滚子轴承
│   ├── angular_contact.json # 角接触球轴承
│   ├── spherical.json       # 调心滚子轴承
│   ├── needle.json          # 滚针轴承
│   └── thrust.json          # 推力轴承
│
└── brands/              # 品牌信息
    ├── skf.json
    ├── nsk.json
    ├── fag.json
    ├── ntn.json
    ├── timken.json
    ├── nbc.json
    └── zwz.json
```

## 轴承型号数据格式

```json
{
  "model": "6204-2RS",
  "type": "deep_groove_ball",
  "type_name": "深沟球轴承",
  "dimensions": {
    "d": 20,      // 内径 (mm)
    "D": 47,      // 外径 (mm)
    "B": 14       // 宽度 (mm)
  },
  "load_ratings": {
    "C": 12700,   // 基本额定动载荷 (N)
    "C0": 6600    // 基本额定静载荷 (N)
  },
  "speed_limits": {
    "grease": 15000,  // 脂润滑极限转速 (rpm)
    "oil": 18000      // 油润滑极限转速 (rpm)
  },
  "weight": 0.106,      // 重量 (kg)
  "seal": "2RS",        // 密封形式
  "cage": "钢冲压",      // 保持架材质
  "clearance": "CN",    // 游隙等级
  "precision": "P0",    // 精度等级
  "cross_reference": {
    "SKF": "6204-2RS1",
    "NSK": "6204DDU",
    "FAG": "6204.2RSR",
    "NTN": "6204LLU"
  },
  "applications": ["电机", "泵", "齿轮箱", "家用电器"],
  "features": ["双面密封", "防尘防水", "免维护"]
}
```

## 品牌数据格式

```json
{
  "name": "SKF",
  "full_name": "Svenska Kullagerfabriken",
  "country": "瑞典",
  "founded": 1907,
  "website": "https://www.skf.com",
  "description": "全球领先的轴承制造商，以高品质和创新技术著称",
  "product_lines": [
    {
      "series": "6000",
      "name": "深沟球轴承",
      "features": ["通用型", "高速", "低噪音"],
      "applications": ["电机", "泵", "齿轮箱"]
    },
    {
      "series": "7200",
      "name": "角接触球轴承",
      "features": ["高刚性", "高速", "承受联合载荷"],
      "applications": ["机床主轴", "涡轮增压器"]
    }
  ],
  "specialties": ["高速轴承", "精密轴承", "轴承单元"],
  "model_prefix": {
    "basic": "",
    "explorers": "E",
    "energy_efficient": "E2"
  }
}
```

## 型号对照表格式

```json
{
  "standard_model": "6204",
  "brand_models": {
    "SKF": "6204",
    "NSK": "6204",
    "FAG": "6204",
    "NTN": "6204",
    "KOYO": "6204",
    "NACHI": "6204",
    "TIMKEN": "204",
    "ZWZ": "6204",
    "LYC": "6204"
  },
  "suffix_mapping": {
    "2RS": {
      "SKF": "2RS1",
      "NSK": "DDU",
      "FAG": "2RSR",
      "NTN": "LLU",
      "KOYO": "2RS"
    },
    "ZZ": {
      "SKF": "2Z",
      "NSK": "ZZ",
      "FAG": "2ZR",
      "NTN": "ZZ",
      "KOYO": "ZZ"
    }
  }
}
```
