# 高德开放平台地理信息服务

> 🤖 支持平台：飞书 / 微信（文字）
> 
> 地理编码、POI搜索、路径规划、导航距离等地理信息服务

---

## ⚠️ 首次使用必读

**使用前必须配置高德开放平台 API Key**，否则无法运行！

配置方式：
1. 获取 Key：https://console.amap.com/dev/key/app
2. 设置环境变量：`export AMAP_API_KEY="your-key"` 和 `AMAP_SECRET_KEY="your-secret"`（如需签名）
3. 或创建配置文件：`cp config.example.txt config.txt` 并填入 Key
4. 验证：`python3 scripts/amap_geo.py --action geo --address "北京市朝阳区"`

详见下方「首次使用配置」章节。

---

## 功能

当用户询问以下内容时，自动调用高德地理信息 API：
1. **地理编码**：地址 → 经纬度
2. **逆地理编码**：经纬度 → 地址
3. **POI搜索**：搜索地点、周边检索
4. **路径规划**：步行/驾车/公交路线
5. **距离测量**：两点间距离

## 触发方式

用户发送以下任一方式都会触发：
- `北京市朝阳区的经纬度`
- `附近有什么医院`
- `从国贸到中关村怎么走`
- `北京到上海多远`
- `搜索附近的餐厅`
- `定位一下`

---

## 首次使用配置

### 1. 获取高德 API Key

1. 注册高德开放平台：https://console.amap.com/dev/key/app
2. 创建应用，获取 Web服务 API Key
3. 配置签名密钥（可选，用于高级功能）

### 2. 关于数字签名

**高德部分 API 需要数字签名验证**：

```
签名算法：MD5(key + params + secret) → 32位小写MD5值

步骤：
1. 将所有请求参数（除sign外）按key字母顺序排序
2. 拼接为：key1value1key2value2...
3. 在拼接字符串前加上 API Key，末尾加上 SecretKey
4. 对整个字符串计算 MD5
```

**是否需要签名？**
- 基础服务（地理编码、POI搜索）：只需 API Key
- 高级服务（路径规划等）：需要签名
- 脚本会自动判断并添加签名

### 3. 配置方式

**方式一：环境变量（推荐）**
```bash
export AMAP_API_KEY="your-api-key"
export AMAP_SECRET_KEY="your-secret-key"  # 如需签名
```

**方式二：配置文件**
```bash
cp config.example.txt config.txt
# 编辑 config.txt，填入你的 Key
```

### 4. 验证

```bash
# 地理编码
python3 scripts/amap_geo.py --action geo --address "北京市朝阳区"

# POI搜索
python3 scripts/amap_geo.py --action poi --keywords "餐厅" --city "北京"

# 路径规划
python3 scripts/amap_geo.py --action direction --from "116.4074,39.9042" --to "116.4274,39.9042"
```

---

## 使用方式

### 命令行参数

```bash
# 地理编码（地址→坐标）
python3 scripts/amap_geo.py --action geo --address "北京市朝阳区"

# 逆地理编码（坐标→地址）
python3 scripts/amap_geo.py --action regeo --location "116.4074,39.9042"

# POI搜索
python3 scripts/amap_geo.py --action poi --keywords "餐厅" --city "北京"

# 周边搜索
python3 scripts/amap_geo.py --action around --location "116.4074,39.9042" --keywords "银行"

# 路径规划（驾车）
python3 scripts/amap_geo.py --action direction --from "116.4074,39.9042" --to "116.4274,39.9042"

# 距离测量
python3 scripts/amap_geo.py --action distance --from "116.4074,39.9042" --to "116.4274,39.9042"
```

### 返回格式

输出格式化文本，便于阅读。

---

## 技术细节

### API 端点

| 功能 | 端点 | 说明 |
|------|------|------|
| 地理编码 | `/v3/geocode/geo` | 地址→坐标 |
| 逆地理编码 | `/v3/geocode/regeo` | 坐标→地址 |
| POI搜索 | `/v3/place/text` | 关键字搜索 |
| 周边搜索 | `/v3/place/around` | 圆形区域搜索 |
| 驾车路径 | `/v3/direction/driving` | 驾车路线 |
| 步行路径 | `/v3/direction/walking` | 步行路线 |
| 公交路径 | `/v3/direction/transit` | 公交路线 |
| 距离测量 | `/v3/direction/material` | 直线距离 |

### 签名算法

```
签名 = MD5(api_key + sorted_params + secret_key)
```

---

## 文件结构

```
amap_geoservice/
├── SKILL.md              # 本文件
├── config.example.txt    # 配置示例
├── scripts/           # 脚本目录
│   └── amap_geo.py    # 主脚本
└── references/        # 参考文档
    └── README.md        # 详细说明
```

---

## 常见问题

### Q: 提示"签名错误"
A: 检查 SecretKey 是否正确配置

### Q: 提示"服务无效"
A: 检查 API Key 类型是否为 Web服务，且已开通对应服务

### Q: POI搜索无结果
A: 尝试更精确的关键字，或使用城市adcode限定范围

---

## 常用城市 AdCode

| 城市 | AdCode |
|------|--------|
| 北京 | 110000 |
| 上海 | 310000 |
| 广州 | 440100 |
| 深圳 | 440300 |
| 成都 | 510100 |
| 武汉 | 420100 |
| 杭州 | 330100 |

---

## 贡献

欢迎提交 Issue 和 PR！
