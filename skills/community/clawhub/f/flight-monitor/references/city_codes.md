# City IATA Codes Reference

Complete mapping of Chinese cities (and major international destinations) to IATA airport codes
used by the `query_flights.py` script.

## Domestic China

| City | Code | Notes |
|------|------|-------|
| 北京 Beijing | BJS | Covers both PEK (Capital) and PKX (Daxing) |
| 上海 Shanghai | SHA | Covers both PVG (Pudong) and SHA (Hongqiao) |
| 广州 Guangzhou | CAN | Baiyun Airport |
| 深圳 Shenzhen | SZX | Bao'an Airport |
| 杭州 Hangzhou | HGH | Xiaoshan Airport |
| 成都 Chengdu | CTU | Tianfu / Shuangliu |
| 三亚 Sanya | SYX | Phoenix Airport |
| 西安 Xi'an | SIA | Xianyang Airport |
| 昆明 Kunming | KMG | Changshui Airport |
| 重庆 Chongqing | CKG | Jiangbei Airport |
| 武汉 Wuhan | WUH | Tianhe Airport |
| 南京 Nanjing | NKG | Lukou Airport |
| 厦门 Xiamen | XMN | Gaoqi Airport |
| 青岛 Qingdao | TAO | Jiaodong Airport |
| 大连 Dalian | DLC | Zhoushuizi Airport |
| 沈阳 Shenyang | SHE | Taoxian Airport |
| 长沙 Changsha | CSX | Huanghua Airport |
| 郑州 Zhengzhou | CGO | Xinzheng Airport |
| 哈尔滨 Harbin | HRB | Taiping Airport |
| 乌鲁木齐 Urumqi | URC | Diwopu Airport |
| 贵阳 Guiyang | KWE | Longdongbao Airport |
| 福州 Fuzhou | FOC | Changle Airport |
| 南昌 Nanchang | KHN | Changbei Airport |
| 太原 Taiyuan | TYN | Wusu Airport |
| 海口 Haikou | HAK | Meilan Airport |
| 兰州 Lanzhou | LHW | Zhongchuan Airport |
| 西宁 Xining | XNN | Caojiapu Airport |
| 呼和浩特 Hohhot | HET | Baita Airport |
| 石家庄 Shijiazhuang | SJW | Zhengding Airport |
| 南宁 Nanning | NNG | Wuxu Airport |
| 合肥 Hefei | HFE | Xinqiao Airport |
| 济南 Jinan | TNA | Yaoqiang Airport |
| 天津 Tianjin | TSN | Binhai Airport |
| 烟台 Yantai | YNT | Penglai Airport |
| 温州 Wenzhou | WNZ | Longwan Airport |
| 宁波 Ningbo | NGB | Lishe Airport |
| 赣州 Ganzhou | KOW | Huangjin Airport |

## International (Common Destinations)

| City | Code |
|------|------|
| 东京 Tokyo | TYO |
| 大阪 Osaka | OSA |
| 首尔 Seoul | SEL |
| 新加坡 Singapore | SIN |
| 曼谷 Bangkok | BKK |
| 香港 Hong Kong | HKG |
| 台北 Taipei | TPE |
| 澳门 Macau | MFM |
| 纽约 New York | NYC |
| 洛杉矶 Los Angeles | LAX |
| 伦敦 London | LON |
| 巴黎 Paris | PAR |
| 悉尼 Sydney | SYD |
| 迪拜 Dubai | DXB |

## Adding New Cities

To add a city not in the list, update the `CITY_CODES` dict in `query_flights.py`:

```python
CITY_CODES["城市名"] = "CODE"
```
