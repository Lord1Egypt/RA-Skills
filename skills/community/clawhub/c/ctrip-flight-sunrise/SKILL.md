# 携程机票查询 Skill

## 概述
用于从携程网站搜索机票信息，获取地点、时间、价格、航班等结构化数据，支持比价分析、直飞/中转识别等功能。

## 技术实现
- **数据来源**: https://flights.ctrip.com
- **认证方式**: Cookie (FVP cookie from flights.ctrip.com)
- **数据提取**: 解析页面 JavaScript 中的 JSON 数据
- **支持功能**: 单程搜索、多日期比价

## 核心能力
1. **机票搜索** - 根据出发地、目的地、日期搜索航班
2. **数据提取** - 解析航班信息（航空公司、时刻、价格、机型等）
3. **结构化存储** - 输出 JSON 格式的航班数据
4. **比价分析** - 多日期、多航班价格对比
5. **低价监控** - 监控特定航线价格变化

## 搜索脚本使用

```bash
# 基本搜索
python3 scripts/ctrip_flight.py -d 北京 -a 上海 -t 2026-04-01

# 输出JSON文件
python3 scripts/ctrip_flight.py -d 北京 -a 上海 -t 2026-04-01 -o result.json

# 多日期比价
python3 scripts/ctrip_flight.py -d 北京 -a 上海 -t 2026-04-01 --compare 2026-04-01,2026-04-02,2026-04-03
```

## 搜索参数
| 参数 | 说明 | 示例 |
|------|------|------|
| -d, --departure | 出发城市 | 北京 |
| -a, --arrival | 到达城市 | 上海 |
| -t, --date | 出发日期 (YYYY-MM-DD) | 2026-04-01 |
| -c, --cabin | 舱位类型 (y/c/f) | y (经济舱) |
| -o, --output | 输出JSON文件路径 | result.json |
| --compare | 多日期对比，逗号分隔 | 2026-04-01,2026-04-02 |

## 输出格式
```json
{
  "searchParams": {
    "departure": "BJS",
    "departureName": "北京",
    "arrival": "SHA",
    "arrivalName": "上海",
    "date": "2026-04-01",
    "cabin": "y"
  },
  "flights": [
    {
      "flightNo": "HO1254",
      "airline": "吉祥航空",
      "airlineCode": "HO",
      "depTime": "2026-04-01 21:25:00",
      "arrTime": "2026-04-01 23:35:00",
      "duration": 130,
      "depAirport": "大兴",
      "depAirportCode": "PKX",
      "arrAirport": "浦东",
      "arrAirportCode": "PVG",
      "planeType": "空客320",
      "stops": 0,
      "isDirect": true,
      "price": 450
    }
  ],
  "statistics": {
    "totalFlights": 11,
    "directFlights": 11,
    "transitFlights": 0,
    "lowestPrice": 450,
    "highestPrice": 550,
    "avgPrice": 516
  },
  "searchTime": "2026-03-27T18:07:42"
}
```

## Cookie 配置
当前使用预设的 FVP cookie。如需更新：
1. 在 Chrome 中登录携程 flights.ctrip.com
2. 打开开发者工具 (F12) -> Application -> Cookies
3. 复制 FVP cookie 的值
4. 更新脚本中的 `self.cookie` 变量

## 已知限制
- Cookie 有时效性，可能需要定期更新
- 部分特殊航班数据可能不完整
- 经停航班的价格数据可能比直飞航班少

## 城市代码支持
支持中国主要城市：
北京(BJS), 上海(SHA), 广州(CAN), 深圳(SZX), 成都(CTU), 杭州(HGH), 南京(NKG), 武汉(WUH), 西安(XIY), 重庆(CKG), 厦门(XMN), 长沙(CSX), 昆明(KMG), 大连(DLC), 青岛(TAO), 天津(TSN), 郑州(CGO), 福州(FOC), 沈阳(SHE), 哈尔滨(HRB) 等

## 文件结构
```
skills/ctrip-flight/
├── skill.md           # 本文档
├── README.md          # 使用说明
└── scripts/
    ├── ctrip_flight.py    # 主搜索脚本
    └── ctrip_search.py    # 备用搜索脚本
```
