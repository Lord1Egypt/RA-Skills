# 高德开放平台地理信息服务 for OpenClaw

地理编码、POI搜索、路径规划、距离测量等地理信息服务

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Key

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

### 3. 测试

```bash
# 地理编码
python3 scripts/amap_geo.py --action geo --address "北京市朝阳区"

# POI搜索
python3 scripts/amap_geo.py --action poi --keywords "餐厅" --city "北京"

# 路径规划
python3 scripts/amap_geo.py --action direction --from "116.4074,39.9042" --to "116.4274,39.9042"
```

### 4. 集成到 OpenClaw

在 OpenClaw 的 `SOUL.md` 或 `AGENTS.md` 中添加触发指令。

## 目录结构

```
amap_geoservice/
├── SKILL.md              # 技能说明（OpenClaw 读取）
├── config.example.txt    # 配置示例
├── scripts/           # 脚本目录
│   └── amap_geo.py  # 主脚本
└── references/        # 参考文档
    └── README.md        # 本文件
```

## 获取高德 API Key

1. 访问 https://console.amap.com/dev/key/app
2. 注册/登录账号
3. 创建应用 → 添加 Web服务 API Key
4. 获取 Key 和 Secret（Secret 用于签名验证）

## 功能列表

| 操作 | 说明 | 签名 |
|------|------|------|
| geo | 地理编码（地址→坐标） | ❌ |
| regeo | 逆地理编码（坐标→地址） | ❌ |
| poi | POI关键字搜索 | ❌ |
| around | 周边搜索 | ❌ |
| direction | 驾车路线规划 | ✅ |
| walking | 步行路线规划 | ❌ |
| distance | 距离测量 | ✅ |

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

## 常见问题

**Q: 提示"签名错误"**
- 检查 SecretKey 是否正确
- 某些操作需要签名，请确保已配置

**Q: 提示"服务无效"**
- 检查 API Key 类型是否为 Web服务
- 检查是否已开通对应服务

**Q: POI搜索无结果**
- 尝试更精确的关键字
- 或使用 citycode 限定城市范围

## License

MIT
