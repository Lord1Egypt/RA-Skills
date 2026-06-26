# 国家代码映射表

用户说中文国家名时，agent 需要转换为 ISO 3166-1 alpha-2 代码传给 API。

## 常用国家（高频）

| 代码 | 中文 | English |
|------|------|---------|
| US | 美国 | United States |
| GB | 英国 | United Kingdom |
| CA | 加拿大 | Canada |
| AU | 澳大利亚 | Australia |
| DE | 德国 | Germany |
| FR | 法国 | France |
| JP | 日本 | Japan |
| KR | 韩国 | South Korea |
| CN | 中国 | China |
| HK | 香港 | Hong Kong |
| TW | 台湾 | Taiwan |
| SG | 新加坡 | Singapore |
| MY | 马来西亚 | Malaysia |
| TH | 泰国 | Thailand |
| VN | 越南 | Vietnam |
| ID | 印度尼西亚 | Indonesia |
| PH | 菲律宾 | Philippines |
| IN | 印度 | India |
| BR | 巴西 | Brazil |
| MX | 墨西哥 | Mexico |
| SA | 沙特阿拉伯 | Saudi Arabia |
| AE | 阿联酋 | United Arab Emirates |
| RU | 俄罗斯 | Russia |
| ES | 西班牙 | Spain |
| IT | 意大利 | Italy |
| NL | 荷兰 | Netherlands |
| SE | 瑞典 | Sweden |
| NO | 挪威 | Norway |
| PL | 波兰 | Poland |
| TR | 土耳其 | Turkey |
| EG | 埃及 | Egypt |
| NG | 尼日利亚 | Nigeria |
| ZA | 南非 | South Africa |
| KE | 肯尼亚 | Kenya |
| AR | 阿根廷 | Argentina |
| CO | 哥伦比亚 | Colombia |
| CL | 智利 | Chile |
| PE | 秘鲁 | Peru |
| NZ | 新西兰 | New Zealand |
| IE | 爱尔兰 | Ireland |
| IL | 以色列 | Israel |
| PK | 巴基斯坦 | Pakistan |
| BD | 孟加拉 | Bangladesh |
| KH | 柬埔寨 | Cambodia |
| MM | 缅甸 | Myanmar |
| LA | 老挝 | Laos |

## 区域快捷映射

用户说区域名称时，agent 应展开为对应的国家代码列表：

| 用户说法 | 展开为 |
|----------|--------|
| 东南亚 | TH,VN,ID,PH,MY,SG,KH,MM,LA |
| 欧洲 | GB,DE,FR,ES,IT,NL,SE,NO,PL,PT,IE,AT,CH,BE,DK,FI,GR,CZ,RO,HU |
| 中东 | SA,AE,QA,KW,BH,OM,JO,IL,EG,IQ |
| 拉美 / 南美 | BR,MX,AR,CO,CL,PE,EC,VE |
| 北美 | US,CA |
| 东亚 | JP,KR,CN,HK,TW |
| 南亚 | IN,PK,BD,LK,NP |
| 非洲 | NG,ZA,KE,EG,GH,ET,TZ |

> 多国家搜索时用逗号分隔传入 `country_code` 参数，如 `US,CA,GB`
